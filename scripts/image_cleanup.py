"""Fail-closed reference-image cleanup, with explicit human visual review.

No OCR/semantic QA is claimed. Unknown sources wait for inspection; clean sources
are byte-preserving no-ops; edits wait for before/after approval. Never publish a
candidate merely because the CLI succeeded. Cache is private, outside public/.
"""
import contextlib
import fcntl
import hashlib
import json
import logging
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
from PIL import Image

LOG = logging.getLogger('aronshare.image_cleanup')
# Scheduler redirects stderr too; make cached/processed/failed states visible even
# when its entrypoint has not configured Python logging.
if not LOG.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[image-cleanup] %(levelname)s %(message)s'))
    LOG.addHandler(handler)
LOG.setLevel(logging.INFO)
LOG.propagate = False
SKILL_SCRIPT = Path('/home/ubuntu/.hermes/skills/creative/baoyu-image-gen/scripts/main.ts')
PROVIDER = 'codex-cli'
VERSION = 'overlay-review-v1'
PROMPT = ('Edit the supplied reference image, not a new illustration or mockup. '
          'Remove only superimposed third-party promotional watermark overlays. '
          'Preserve genuine product logos, UI text, layout, screenshots, subjects, '
          'author attribution and all non-overlay content. Do not redesign, invent '
          'features, add branding, crop or recompose. Keep the reference aspect ratio. '
          'If no overlay is present, leave the image unchanged. Reconstruct only '
          'the pixels obscured by the overlay. Human comparison is required; do not '
          'claim the edited image is pixel-identical to the original.')

class CleanupError(RuntimeError): pass
class ReviewRequired(CleanupError): pass

def scratch_root():
    p = Path(os.environ.get('TMPDIR') or Path.home()/'.hermes/cache/scratch')
    p.mkdir(parents=True, exist_ok=True)
    return p

def digest(data): return hashlib.sha256(data).hexdigest()

def validate_image(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size > 32*1024*1024:
        raise CleanupError('Missing or oversized image')
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            if min(im.size) < 32 or im.width*im.height > 40_000_000:
                raise CleanupError('Invalid image dimensions')
            im.load()
            if getattr(im, 'n_frames', 1) != 1:
                raise CleanupError('Animated images need separate review; not flattened silently')
            return im.size
    except CleanupError: raise
    except Exception as exc: raise CleanupError(f'Invalid image: {exc}') from exc

def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.image-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)

def fingerprint():
    # Include provider implementation, wrapper, config and prompt/version, not URL.
    h = hashlib.sha256((VERSION + PROVIDER + PROMPT).encode())
    for p in sorted(SKILL_SCRIPT.parent.rglob('*.ts')):
        h.update(str(p.relative_to(SKILL_SCRIPT.parent)).encode())
        h.update(p.read_bytes())
    config = Path.home()/'.baoyu-skills/baoyu-image-gen/EXTEND.md'
    if config.is_file(): h.update(config.read_bytes())
    h.update(os.environ.get('BAOYU_CODEX_IMAGEGEN_BIN', '').encode())
    return h.hexdigest()

def baoyu_command(source, output):
    w, h = validate_image(source)
    divisor = math.gcd(w, h)
    bun = shutil.which('bun')
    launcher = [bun] if bun else ['npx', '-y', 'bun']
    return launcher + [str(SKILL_SCRIPT), '--provider', PROVIDER,
                       '--prompt', PROMPT, '--ref', str(Path(source).resolve()),
                       '--image', str(Path(output).resolve()), '--ar', f'{w//divisor}:{h//divisor}',
                       '--quality', '2k']

def run_baoyu(source, output, timeout=420, retries=1):
    """Bound the whole process group; no shell; each attempt gets an absent output."""
    if not SKILL_SCRIPT.is_file(): raise CleanupError('Main baoyu skill is missing')
    config = Path.home()/'.baoyu-skills/baoyu-image-gen/EXTEND.md'
    if not config.is_file(): raise CleanupError('Baoyu EXTEND.md setup required')
    timeout = max(1, min(int(timeout), 900))
    retries = max(0, min(int(retries), 1))
    env = os.environ.copy()
    env.update(BAOYU_CODEX_IMAGEGEN_RETRIES='1',
               BAOYU_CODEX_IMAGEGEN_TIMEOUT_MS=str(timeout*1000),
               BAOYU_CODEX_IMAGEGEN_BIN=str(SKILL_SCRIPT.parent/'codex-imagegen/main.ts'),
               TMPDIR=str(scratch_root()))
    # Our content/version-bound reviewed cache is authoritative, not the wrapper's
    # optional path-based cache. The wrapper rejects retries=0, so pin it to 1;
    # the outer process-group deadline bounds all nested retries combined.
    env.pop('BAOYU_CODEX_IMAGEGEN_CACHE_DIR', None)
    for attempt in range(retries+1):
        Path(output).unlink(missing_ok=True)
        # Private unique cwd avoids project-local provider/config surprises.
        with tempfile.TemporaryDirectory(prefix='baoyu-run-', dir=scratch_root()) as work:
            # Keep original bytes, but give the reference its real format suffix;
            # provider MIME inference must not mistake .img WebP/JPEG for PNG.
            with Image.open(source) as image:
                suffix = {'PNG': '.png', 'JPEG': '.jpg', 'WEBP': '.webp'}.get(image.format)
            if suffix is None:
                raise CleanupError('Reference format needs explicit PNG/JPEG/WebP conversion review')
            reference = Path(work)/('reference'+suffix)
            reference.write_bytes(Path(source).read_bytes())
            with open(Path(work)/'cli.log', 'wb') as log:
                proc = subprocess.Popen(baoyu_command(reference, output), cwd=work, env=env,
                                        stdout=log, stderr=log, start_new_session=True)
                try:
                    code = proc.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                    code = -1
            if code == 0 and Path(output).is_file(): return
            LOG.warning('failed provider=%s attempt=%s exit=%s', PROVIDER, attempt+1, code)
    raise CleanupError('Baoyu reference edit failed or timed out; no original fallback')

class CleanupStore:
    def __init__(self, root=None):
        self.root = Path(root or os.environ.get('ARONSHARE_IMAGE_REVIEW_DIR') or
                         Path.home()/'.cache/aronshare/image-review')

    def entry(self, source):
        validate_image(source)
        raw = Path(source).read_bytes()
        return self.root / digest((digest(raw)+fingerprint()).encode())

    @contextlib.contextmanager
    def locked(self, source):
        entry = self.entry(source)
        entry.mkdir(parents=True, exist_ok=True, mode=0o700)
        with open(entry/'lock', 'a') as lock:
            # Never wait forever on another review/generation process.
            deadline = time.monotonic()+5
            while True:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline: raise CleanupError('Image review entry busy')
                    time.sleep(.1)
            try:
                raw = Path(source).read_bytes()
                if not (entry/'original.img').exists(): atomic_write(entry/'original.img', raw)
                if digest((entry/'original.img').read_bytes()) != digest(raw):
                    raise CleanupError('Original cache hash mismatch')
                yield entry
            finally: fcntl.flock(lock, fcntl.LOCK_UN)

    def read(self, entry):
        try:
            record = json.loads((entry/'review.json').read_text())
            if record.get('fingerprint') != fingerprint() or record.get('source_sha256') != digest((entry/'original.img').read_bytes()):
                raise CleanupError('Review record is stale or belongs to a different source')
            return record
        except FileNotFoundError: return {'state': 'inspection_required'}
        except Exception as exc: raise CleanupError('Corrupt or stale review record') from exc

    def save(self, entry, **record):
        record.update(version=VERSION, provider=PROVIDER, fingerprint=fingerprint(),
                      source_sha256=digest((entry/'original.img').read_bytes()))
        atomic_write(entry/'review.json', json.dumps(record, ensure_ascii=False, indent=2).encode())

    def inspect(self, source, decision, *, reviewer, note):
        """Call only after actual visual inspection; clean means no removable overlay."""
        if decision not in ('clean', 'needs_edit', 'rejected') or not reviewer.strip() or not note.strip():
            raise ValueError('Explicit decision, reviewer and inspection note required')
        with self.locked(source) as entry:
            (entry/'candidate.png').unlink(missing_ok=True)
            self.save(entry, state=decision, reviewer=reviewer, note=note)
        return entry

    def approve(self, source, *, reviewer, note):
        """Human must compare original/candidate for remaining overlays and UI drift."""
        if not reviewer.strip() or not note.strip(): raise ValueError('Reviewer and comparison note required')
        with self.locked(source) as entry:
            record = self.read(entry)
            if record['state'] != 'review_required': raise CleanupError('No pending candidate')
            candidate = entry/'candidate.png'
            validate_image(candidate)
            if digest(candidate.read_bytes()) != record.get('output_sha256'):
                raise CleanupError('Candidate changed since generation/import')
            self.save(entry, state='approved', output_sha256=record['output_sha256'],
                      reviewer=reviewer, note=note, edit_provenance=record.get('edit_provenance'))
        return candidate

    def import_candidate(self, source, edited, *, provenance):
        """Register a real external --ref edit for review, never auto-approve it.

        provenance should describe the actual command/reference and output path.
        This API does not assert that an arbitrary external image came from baoyu.
        """
        if not provenance.strip(): raise ValueError('Actual edit provenance required')
        validate_image(edited)
        with self.locked(source) as entry:
            self._candidate(entry, edited, provenance)
        return entry

    def _candidate(self, entry, edited, provenance):
        w,h = validate_image(entry/'original.img')
        ew,eh = validate_image(edited)
        if abs((ew/eh)/(w/h)-1) > .04: raise CleanupError('Edit changed aspect ratio; review rejected')
        data = Path(edited).read_bytes()
        atomic_write(entry/'candidate.png', data)
        self.save(entry, state='review_required', output_sha256=digest(data), edit_provenance=provenance)
        LOG.warning('processed review_required entry=%s', entry)

    def prepare(self, source):
        """Return reviewed image path, or raise. Never return an unreviewed source."""
        with self.locked(source) as entry:
            record = self.read(entry)
            state = record['state']
            if state == 'clean':
                LOG.info('cached clean_noop entry=%s', entry)
                return entry/'original.img'
            if state == 'approved':
                p = entry/'candidate.png'
                validate_image(p)
                if digest(p.read_bytes()) != record.get('output_sha256'):
                    raise CleanupError('Approved output hash mismatch')
                LOG.info('cached approved entry=%s', entry)
                return p
            if state == 'needs_edit':
                try:
                    with tempfile.TemporaryDirectory(prefix='aronshare-edit-', dir=scratch_root()) as work:
                        output = Path(work)/'candidate.png'
                        run_baoyu(entry/'original.img', output)
                        self._candidate(entry, output, 'baoyu main.ts --provider codex-cli --ref original.img')
                except Exception as exc:
                    self.save(entry, state='failed', error=str(exc),
                              reviewer=record.get('reviewer'), note=record.get('note'))
                    LOG.error('failed entry=%s error=%s', entry, exc)
                    raise CleanupError(f'Cleanup failed; publication blocked: {exc}') from exc
            elif state == 'inspection_required':
                self.save(entry, state=state)
            raise ReviewRequired(f'{state if state != "needs_edit" else "review_required"}: {entry}; publication blocked')

def prepare_image(source):
    return CleanupStore().prepare(source)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['status', 'inspect', 'prepare', 'import', 'approve'])
    parser.add_argument('--source', type=Path)
    parser.add_argument('--edited', type=Path)
    parser.add_argument('--decision', choices=['clean', 'needs_edit', 'rejected'])
    parser.add_argument('--reviewer', default='')
    parser.add_argument('--note', default='')
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    store = CleanupStore(args.cache)
    if args.action == 'status':
        for record in sorted(store.root.glob('*/review.json')):
            state = json.loads(record.read_text())
            print(json.dumps(dict(entry=str(record.parent), **state), ensure_ascii=False))
        return 0
    if args.source is None: parser.error('--source required')
    try:
        if args.action == 'inspect':
            print(store.inspect(args.source, args.decision, reviewer=args.reviewer, note=args.note))
        elif args.action == 'import':
            if args.edited is None: parser.error('--edited required')
            print(store.import_candidate(args.source, args.edited, provenance=args.note))
        elif args.action == 'approve':
            print(store.approve(args.source, reviewer=args.reviewer, note=args.note))
        else:
            print(store.prepare(args.source))
        return 0
    except (CleanupError, ValueError) as exc:
        LOG.error('%s', exc)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
