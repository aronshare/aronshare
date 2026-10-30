"""Offline gate tests. Synthetic pixels are fixtures, never visual QA evidence."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import image_cleanup as gate

class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source.png'
        Image.new('RGB', (800, 400), 'navy').save(self.source)
        self.store = gate.CleanupStore(self.root / 'cache')

    def test_unknown_requires_inspection_and_never_runs_ai(self):
        with patch.object(gate, 'run_baoyu') as run:
            with self.assertRaises(gate.ReviewRequired):
                self.store.prepare(self.source)
            run.assert_not_called()

    def test_clean_noop_is_hash_bound_and_preserves_original(self):
        original = self.source.read_bytes()
        self.store.inspect(self.source, 'clean', reviewer='test', note='Fixture only')
        self.assertEqual(self.store.prepare(self.source).read_bytes(), original)
        Image.new('RGB', (800,400), 'red').save(self.source)
        with self.assertRaises(gate.ReviewRequired):
            self.store.prepare(self.source)

    def test_reference_command_and_pending_candidate(self):
        self.store.inspect(self.source, 'needs_edit', reviewer='test', note='Fixture overlay')
        def generate(source, output, **kwargs):
            Image.new('RGB',(800,400),'white').save(output)
        with patch.object(gate, 'run_baoyu', side_effect=generate) as run:
            with self.assertRaises(gate.ReviewRequired):
                self.store.prepare(self.source)
            self.assertEqual(run.call_count, 1)
            with self.assertRaises(gate.ReviewRequired):
                self.store.prepare(self.source)
            self.assertEqual(run.call_count, 1)
        self.store.approve(self.source, reviewer='test', note='Fixture comparison only')
        self.assertNotEqual(self.store.prepare(self.source).read_bytes(), self.source.read_bytes())
        cmd = gate.baoyu_command(self.source, self.root/'out.png')
        self.assertEqual(cmd[cmd.index('--ref')+1], str(self.source.resolve()))
        self.assertEqual(cmd[cmd.index('--provider')+1], 'codex-cli')
        self.assertNotIn('/profiles/', ' '.join(cmd))

    def test_failure_missing_output_and_tamper_never_pass(self):
        self.store.inspect(self.source, 'needs_edit', reviewer='test', note='Fixture')
        with patch.object(gate, 'run_baoyu', return_value=None):
            with self.assertRaises(gate.CleanupError): self.store.prepare(self.source)
        self.store.inspect(self.source, 'clean', reviewer='test', note='Fixture')
        p = self.store.prepare(self.source)
        p.write_bytes(b'tampered')
        with self.assertRaises(gate.CleanupError): self.store.prepare(self.source)

    def test_prompt_version_invalidates(self):
        self.store.inspect(self.source, 'clean', reviewer='test', note='Fixture')
        with patch.object(gate, 'PROMPT', gate.PROMPT+' revised'):
            with self.assertRaises(gate.ReviewRequired): self.store.prepare(self.source)

    def test_external_import_still_requires_approval(self):
        edited = self.root/'external.png'
        Image.new('RGB',(800,400),'white').save(edited)
        self.store.import_candidate(self.source, edited, provenance='TEST fixture, not AI evidence')
        with self.assertRaises(gate.ReviewRequired): self.store.prepare(self.source)
        self.store.approve(self.source, reviewer='test', note='Fixture only')
        with patch.object(gate, 'run_baoyu') as run:
            self.assertEqual(self.store.prepare(self.source).read_bytes(), edited.read_bytes())
            run.assert_not_called()
        self.store.entry(self.source).joinpath('candidate.png').write_bytes(self.source.read_bytes())
        with self.assertRaises(gate.CleanupError): self.store.prepare(self.source)

    def test_provider_version_invalidates(self):
        self.store.inspect(self.source, 'clean', reviewer='test', note='Fixture')
        with patch.object(gate, 'VERSION', 'new-provider-revision'):
            with self.assertRaises(gate.ReviewRequired): self.store.prepare(self.source)

    def test_failed_edit_is_not_retried_on_each_cron(self):
        self.store.inspect(self.source, 'needs_edit', reviewer='test', note='Fixture')
        with patch.object(gate, 'run_baoyu', side_effect=OSError('offline')) as run:
            for _ in range(2):
                with self.assertRaises(gate.CleanupError): self.store.prepare(self.source)
            self.assertEqual(run.call_count, 1)

    def test_output_aspect_change_rejected(self):
        edited=self.root/'wrong.png'
        Image.new('RGB',(400,800),'white').save(edited)
        with self.assertRaises(gate.CleanupError):
            self.store.import_candidate(self.source, edited, provenance='fixture')

    def test_runner_does_not_accept_stale_output_and_bounds_retry(self):
        from unittest.mock import MagicMock
        output=self.root/'stale.png'; output.write_bytes(self.source.read_bytes())
        proc=MagicMock(); proc.wait.return_value=0
        with patch.object(gate.subprocess,'Popen',return_value=proc) as launch:
            with self.assertRaises(gate.CleanupError):
                gate.run_baoyu(self.source, output, timeout=1, retries=10)
            self.assertEqual(launch.call_count,2)
            self.assertFalse(output.exists())
            for call in launch.call_args_list:
                self.assertIn('--ref',call.args[0])
                self.assertTrue(call.kwargs['start_new_session'])

    def test_runner_timeout_kills_process_group(self):
        from unittest.mock import MagicMock
        proc=MagicMock(pid=12345)
        proc.wait.side_effect=[gate.subprocess.TimeoutExpired('fixture',1), -9]
        with patch.object(gate.subprocess,'Popen',return_value=proc), patch.object(gate.os,'killpg') as kill:
            with self.assertRaises(gate.CleanupError):
                gate.run_baoyu(self.source, self.root/'absent.png', timeout=1,retries=0)
            kill.assert_called_once_with(12345,gate.signal.SIGKILL)

if __name__ == '__main__': unittest.main()
