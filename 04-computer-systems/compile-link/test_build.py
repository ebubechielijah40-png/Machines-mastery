import unittest
from run import investigate
class BuildTests(unittest.TestCase):
    def test_separate_compilation_link_failure_and_runtime_contract(self):
        report=investigate()
        failed=[r for r in report['records'] if r['exit_code']]
        self.assertEqual(len(failed),2)
        self.assertTrue(all('sum_bytes' in r['stderr'] for r in failed))
        self.assertEqual(sum(r['stdout']=='sum=15 calls=1 affine=17\n' for r in report['records']),2)
if __name__=='__main__':unittest.main(verbosity=2)
