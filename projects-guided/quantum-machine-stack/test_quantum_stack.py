import unittest
from run_stack import build_report

class StackTests(unittest.TestCase):
    def test_gate_representations_noise_and_recovery_share_contract(self):
        r=build_report()
        self.assertLess(r['vector_density_residual'],1e-10)
        for p in r['vector_gate_probabilities']:self.assertAlmostEqual(p,.5)
        self.assertAlmostEqual(r['noise']['output_purity'],.68)
        self.assertEqual(r['recovery']['syndrome'],(1,1))
        self.assertAlmostEqual(r['recovery']['overlap_squared'],1)
        self.assertAlmostEqual(r['recovery']['logical_X_probability'],.028)
        self.assertTrue(all(len(x)==64 for x in r['implementation_sha256'].values()))

if __name__=='__main__':unittest.main(verbosity=2)
