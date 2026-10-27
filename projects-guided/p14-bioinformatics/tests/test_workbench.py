import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
CLI = PROJECT / 'solutions' / 'workbench.py'


class WorkbenchTests(unittest.TestCase):
    def run_cli(self, text, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.fasta'
            path.write_bytes(text.encode('utf-8'))
            return subprocess.run([sys.executable, str(CLI), str(path), *args],
                                  text=True, capture_output=True, timeout=5)

    def test_end_to_end_local_and_provenance(self):
        text = '>a\nTTACGTAA\n>b\nGGACGTCC\n'
        p = self.run_cli(text, '--mode', 'local')
        self.assertEqual(p.returncode, 0, p.stderr)
        result = json.loads(p.stdout)
        self.assertEqual(result['score'], 8)
        self.assertEqual(result['input_sha256'], hashlib.sha256(text.encode()).hexdigest())
        self.assertEqual(result['a_span'], [2, 6])
        self.assertEqual(len(result['implementation_sha256']), 3)
        self.assertEqual(result['a_aligned'], 'ACGT')

    def test_end_to_end_global(self):
        p = self.run_cli('>a\nAG\n>b\nACG\n', '--mismatch', '-1')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['score'], 2)

    def test_bad_inputs_and_resource_caps(self):
        cases = [('ACGT', []), ('>a\nAX\n>b\nAA', []), ('>a\nAA', []),
                 ('>a\nAA\n>a\nAA', []), ('>a\n\n>b\nAA', []),
                 ('>a\nAA\n>b\nAA', ['--max-cells', '8']),
                 ('>a\nAA\n>b\nAA', ['--max-bytes', '4']),
                 ('>a\nAA\n>b\nAA', ['--gap', '1'])]
        for text, args in cases:
            with self.subTest(text=text, args=args):
                p = self.run_cli(text, *args)
                self.assertEqual(p.returncode, 2)
                self.assertEqual(p.stdout, '')

    def test_only_literal_unknown_symbol_semantics(self):
        p = self.run_cli('>a\nN\n>b\nA')
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['score'], -3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
