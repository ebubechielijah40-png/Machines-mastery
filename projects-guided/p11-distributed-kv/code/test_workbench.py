import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from workbench import scenario,unique_object


class WorkbenchTests(unittest.TestCase):
    def test_partition_exchange_duplicate_and_causal_write(self):
        events=[dict(op='put',node='A',key='x',value='red'),dict(op='put',node='B',key='x',value='blue'),
                dict(op='send',node='A',**{'as':'a0'}),dict(op='send',node='B',**{'as':'b0'}),
                dict(op='deliver',node='A',message='b0'),dict(op='deliver',node='B',message='a0'),
                dict(op='deliver',node='A',message='b0'),dict(op='put',node='A',key='x',value='green'),
                dict(op='send',node='A',**{'as':'a1'}),dict(op='deliver',node='B',message='a1')]
        result=scenario(dict(nodes=['A','B'],events=events))
        self.assertFalse(result['trace'][6]['state_changed'])
        for name in ['A','B']:self.assertEqual(result['replicas'][name]['visible'],{'x':'green'})
        self.assertGreater(result['trace'][9]['clock'],result['trace'][8]['send_counter'])

    def test_deletion_is_retained_and_empty_string_is_a_value(self):
        result=scenario(dict(nodes=['A'],events=[dict(op='put',node='A',key='x',value=''),
            dict(op='read',node='A'),dict(op='delete',node='A',key='x'),dict(op='read',node='A')]))
        self.assertEqual(result['trace'][1]['visible'],{'x':''})
        self.assertEqual(result['trace'][3]['visible'],{})
        self.assertIsNone(result['replicas']['A']['records'][0]['value'])

    def test_schema_identity_and_message_boundaries(self):
        bad=[dict(nodes=['A','A'],events=[]),dict(nodes=['A'],events=[dict(op='deliver',node='A',message='absent')]),
             dict(nodes=['A'],events=[dict(op='read',node='B')]),dict(nodes=['A'],events=[dict(op=[],node='A')]),
             dict(nodes=['A'],events=[dict(op='put',node='A',key='x',value=None)])]
        for document in bad:
            with self.assertRaises(ValueError):scenario(document)
        with self.assertRaises(ValueError):json.loads('{"nodes":[],"nodes":[]}',object_pairs_hook=unique_object)

    def test_real_cli_success_and_rejection(self):
        entry=Path(__file__).with_name('workbench.py')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'scenario.json'
            path.write_text(json.dumps(dict(nodes=['A'],events=[dict(op='put',node='A',key='k',value='v')])))
            p=subprocess.run([sys.executable,str(entry),str(path)],capture_output=True,text=True,timeout=3)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout)['replicas']['A']['visible'],{'k':'v'})
            path.write_text('{"nodes":["A"],"nodes":["B"],"events":[]}')
            p=subprocess.run([sys.executable,str(entry),str(path)],capture_output=True,text=True,timeout=3)
            self.assertEqual(p.returncode,2)
            self.assertIn('duplicate JSON field',p.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
