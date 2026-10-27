import math
import unittest
from run_stack import build_report

class StackTests(unittest.TestCase):
    def test_connected_report_preserves_mechanism_meaning(self):
        r=build_report()
        self.assertEqual(r['alignment']['score'],10)
        self.assertEqual(r['alignment']['a'],'AAAAAAAA')
        self.assertAlmostEqual(r['distance']['substitutions_per_site'],-.75*math.log(2/3))
        self.assertAlmostEqual(r['population']['summary']['mean_frequency'],.5)
        self.assertAlmostEqual(r['population']['summary']['expected_heterozygosity'],.5*(.75**3))
        self.assertEqual(r['tree']['root']['height'],3)
        self.assertEqual(len(r['fixture_sha256']),64)
        self.assertTrue(all(len(x)==64 for x in r['implementation_sha256'].values()))

if __name__=='__main__':unittest.main(verbosity=2)
