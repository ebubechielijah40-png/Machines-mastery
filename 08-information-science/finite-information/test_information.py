import itertools,math,unittest
from information import distribution,entropy,joint_information

class InformationTests(unittest.TestCase):
    def test_literal_entropy_cases_and_weight_scaling(self):
        self.assertEqual(entropy([1,0]),0)
        self.assertEqual(entropy([1,1]),1)
        self.assertEqual(entropy([1,1,1,1]),2)
        self.assertAlmostEqual(entropy([1,2,1]),1.5)
        self.assertEqual(entropy([5,10,5]),entropy([1,2,1]))
    def test_independent_and_perfect_prediction_tables(self):
        independent=joint_information([[1,1],[1,1]])
        self.assertEqual(independent['mutual_information'],0)
        self.assertEqual(independent['h_x_given_y'],1)
        for table in [[[1,0],[0,1]],[[0,1],[1,0]]]:
            result=joint_information(table)
            self.assertEqual(result['mutual_information'],1)
            self.assertEqual(result['h_x_given_y'],0)
    def test_binary_flip_analytic_identity(self):
        for flip in [0,.01,.1,.25,.5,.75,.9,1]:
            result=joint_information([[(1-flip)/2,flip/2],[flip/2,(1-flip)/2]])
            expected=1-entropy([flip,1-flip])
            self.assertAlmostEqual(result['mutual_information'],expected)
            # Independent direct KL form: sum p(x,y) log2 p(x,y)/(p(x)p(y)).
            terms=[p*math.log2(p/.25) for p in [(1-flip)/2,flip/2,flip/2,(1-flip)/2] if p]
            self.assertAlmostEqual(result['mutual_information'],math.fsum(terms))
    def test_invalid_weights_and_joint_shapes(self):
        for weights in [[],[0,0],[-1,2],[float('nan'),1],[float('inf')],[True,1],[10**1000],[1e308,1e308],itertools.repeat(1)]:
            with self.assertRaises(ValueError):entropy(weights)
        for table in [[],[[]],[[1],[1,2]],[[0,0],[0,0]],[itertools.repeat(1)],itertools.repeat([1])]:
            with self.assertRaises(ValueError):joint_information(table)

if __name__=='__main__':unittest.main(verbosity=2)
