# Mandatory reference-image review / watermark cleanup

## Enforced paths

- Actual user crontab: `30 9 * * * /usr/bin/python3 /home/ubuntu/aronshare-resource-hub/scripts/daily_20_pipeline.py`; logs go to `daily_pipeline.log`.
- Daily and master cover acquisition → `cover_crawler.generate_cover_for_post` → `image_cleanup.prepare_image` → existing letterbox/AronShare branding → atomic installation.
- Daily **actual `item['content']`** → `image_ingestion.localize_images` → reviewed local body assets → post write. Failure skips the entire post, never retains remote originals as fallback.
- Frontend `pipeline.covers.download` → same gate, before RGB conversion/branding. Cleanup errors propagate.
- Frontend `pipeline.build.write_post` (also called by `pipeline.enrich` and migration) → same body/media gate. Explicit remote covers are refused. Existing historical covers are not bulk reprocessed; master still preserves existing covers.
- `pipeline.ai_clean_image` is only a bridge. Misleading text-to-mockup generation functions were removed.

This does NOT claim to police arbitrary manual file copying, historical images, or external deployment commands. No UI, DB, historical source article/image, deployment or scheduler configuration was changed by this implementation.

## Review states (fail closed)

Cache default: `/home/ubuntu/.cache/aronshare/image-review`, overridable with `ARONSHARE_IMAGE_REVIEW_DIR` (same value must be used by reviewer and pipeline).

1. First acquisition stores exact bytes in a private cache entry, marks `inspection_required`, and blocks publication. There is **no reliable autonomous semantic watermark detector implemented**.
2. Inspect `original.img` visually. Call `inspect(..., 'clean', reviewer=..., note=...)` only when no removable third-party overlay is visible. `prepare()` then returns the unchanged original, without AI.
3. For a visible third-party overlay, record `needs_edit`. `prepare()` runs main-profile baoyu with explicit `--provider codex-cli --ref <original-byte-copy>`, preserving original aspect and genuine logos/UI/credit, not inventing screenshots.
4. Generated output is only a candidate: `review_required` still blocks publication. Compare original/candidate for remaining overlays, invented/missing text, UI drift, logos and content before calling `approve()`.
5. Failed edits become `failed` and do not incur new generation cost on every cron. After resolving the issue, explicitly inspect/reset to `needs_edit` to retry. Rejected images remain blocked.

**Operational consequence:** new images pause scheduled publication until a human/vision-capable reviewer makes the explicit decisions above. The gate is mandatory, not an opt-in flag. It does not silently pretend unattended visual QA succeeded. Reasons and cache paths appear in cron logs. `status` lists review records for triage.

Pillow verifies decoding, bounds, animation refusal and aspect ratio, NOT watermark absence or semantic fidelity. AI edits cannot be guaranteed pixel-identical; preserve article source credit separately (ingestion leaves it intact). No-watermark images need inspection, not expensive blind edits.

## Commands / API

Use the existing interpreter with Pillow:

```sh
PY=/home/ubuntu/.venvs/resource_crawler/bin/python3
GATE=/home/ubuntu/aronshare-resource-hub/scripts/image_cleanup.py
$PY "$GATE" status
$PY "$GATE" inspect --source /path/original.png --decision clean --reviewer Aron --note 'Visually checked; no third-party overlay'
$PY "$GATE" inspect --source /path/original.png --decision needs_edit --reviewer Aron --note 'Repeated diagonal overlay visible'
$PY "$GATE" prepare --source /path/original.png
# Above returns exit 2 until candidate visually approved. It can invoke real AI.
$PY "$GATE" approve --source /path/original.png --reviewer Aron --note 'Compared original/candidate; overlay removed; genuine UI/text/logos retained'
$PY "$GATE" prepare --source /path/original.png
```

Import the parent's independently generated real sample **without another AI call**:

```python
import sys
sys.path.insert(0, '/home/ubuntu/aronshare-resource-hub/scripts')
from image_cleanup import CleanupStore
store = CleanupStore()
source = '/home/ubuntu/.hermes/cache/scratch/aronshare-watermark-clean/11442-reference.png'
edited = '/home/ubuntu/.hermes/cache/scratch/aronshare-watermark-clean/11442-cleaned.png'
store.import_candidate(source, edited, provenance='Actual baoyu main.ts --provider codex-cli --ref 11442-reference.png; externally generated output')
# Only the reviewer who actually inspected the images should approve:
store.approve(source, reviewer='parent-agent', note='Actual before/after visual comparison: WWW.ABSKOOP.COM overlay removed; UI retained')
reviewed_path = store.prepare(source)  # cache hit, no AI call
```

Import provenance is an operator attestation, not cryptographic proof of how the external image was generated. Cache keys bind exact original bytes + prompt + provider/version + installed baoyu TypeScript and user EXTEND config. A PNG conversion and the original WebP have different hashes: register each actual acquired original explicitly if needed; approval is not automatically transferred across files/encodings. Output hashes are checked on every reuse. Originals remain cached and source files are untouched.

## Bounds and limitations

- At most two outer process-group attempts, 420 seconds each by default (API caps timeout to 900 seconds and retries to one). Entire child process group is killed on timeout, including nested baoyu retries. The bundled wrapper's retry setting is pinned to 1 because its provider ignores zero.
- Unique scratch paths follow `TMPDIR`; actual reference is a byte-identical file with the proper PNG/JPEG/WebP extension, avoiding MIME misidentification of cache `.img` files. Other formats/animations fail explicitly rather than silently flattening.
- Cache entry lock waits at most 5 seconds. Pending candidates are never regenerated until reviewer action.
- Atomic image/post writes; no dirty-original fallback after generation, validation or review failure. All images in one body batch must pass before any body asset is installed.
- Inline Markdown and quoted-src HTML images plus frontmatter `media` images are localized. Reference-style Markdown, responsive/embedded image markup and unsupported formats stop the post for manual normalization. This is deliberately conservative, not a complete Markdown renderer or HTML sanitizer.
- Existing reviewed body assets may require inspection again if later re-ingested after lossy format conversion, since exact bytes changed. No automatic approval of derivatives is claimed.
- Existing historical images and the two 11442 stylized body assets were not mass-cleaned. No third-party watermark finding is inferred for them.

## Offline verification

```sh
cd /home/ubuntu/aronshare-resource-hub
PYTHONDONTWRITEBYTECODE=1 /home/ubuntu/.venvs/resource_crawler/bin/python3 -m unittest discover -s tests -v
```

Tests use explicitly synthetic image fixtures and mocked network/AI-process seams, not fake evidence of real AI quality. They exercise mandatory cover/body/media gates, daily skip-before-write, frontend cover/write/enrich routes, remote cover rejection, reference flags, content/prompt/provider-version invalidation, pending approval, tampering, timeout process-group termination, bounded retries, missing/stale outputs, unsupported markup and atomic/no-fallback behavior. Actual Baoyu output quality is verified separately by the parent reviewer.
