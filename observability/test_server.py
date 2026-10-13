import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('dashboard', Path(__file__).with_name('server.py'))
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)


class EvidenceTest(unittest.TestCase):
    def test_partial_run_and_real_evidence_without_unrelated_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / 'evaluation/results/llmlingua-test'
            directory.mkdir(parents=True)
            (root / '.env').write_text('SECRET=should-not-be-exported')
            (directory / 'trace.jsonl').write_text(json.dumps({'kind': 'workflow_start'})+'\n')
            result = dashboard.snapshot(root)
            self.assertIsNone(result['runs'][0]['result'])
            self.assertEqual(result['runs'][0]['trace'][0]['kind'], 'workflow_start')
            self.assertNotIn('should-not-be-exported', json.dumps(result))
            (directory / 'result.json').write_text(json.dumps({'model': 'fixed-model'}))
            self.assertEqual(dashboard.snapshot(root)['runs'][0]['result']['model'], 'fixed-model')


if __name__ == '__main__':
    unittest.main()
