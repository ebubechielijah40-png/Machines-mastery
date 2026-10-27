from collections import Counter
from fractions import Fraction as F
import itertools
import math
import unittest
from probability import FiniteDistribution, posterior, binomial, wilson, wald, coverage, exact_upper_tail, permutation_test


class ProbabilityTests(unittest.TestCase):
    def test_conditioning_exact_counts_and_zero_event(self):
        die=FiniteDistribution({i:F(1,6) for i in range(1,7)})
        self.assertEqual(die.condition(lambda x:x>=4).event(lambda x:x%2==0),F(2,3))
        with self.assertRaises(ValueError):die.condition(lambda x:x>6)
        self.assertEqual(die.expectation(),F(7,2))
        self.assertEqual(die.variance(),F(35,12))

    def test_independence_is_not_disjointness(self):
        model=FiniteDistribution({x:F(1,4) for x in itertools.product([0,1],repeat=2)})
        a=lambda x:x[0]==1;b=lambda x:x[1]==1
        self.assertEqual(model.event(lambda x:a(x) and b(x)),model.event(a)*model.event(b))
        one=FiniteDistribution({0:F(1,2),1:F(1,2)})
        self.assertNotEqual(one.event(lambda x:x==0 and x==1),one.event(lambda x:x==0)*one.event(lambda x:x==1))

    def test_bayes_from_independent_integer_contingency_table(self):
        #100 faults:90 positive;9900 healthy:198 positive.
        self.assertEqual(posterior(F(1,100),F(9,10),F(1,50)),F(90,288))
        with self.assertRaises(ValueError):posterior(0,1,0)

    def test_binomial_against_all_binary_sequences(self):
        for n in range(7):
            counts=Counter(map(sum,itertools.product([0,1],repeat=n)))
            model=binomial(n,F(1,2))
            self.assertEqual(model.masses,{k:F(counts[k],2**n) for k in range(n+1)})
            self.assertEqual(model.expectation(),F(n,2))
            self.assertEqual(model.variance(),F(n,4))

    def test_degenerate_binomial_and_tail(self):
        self.assertEqual(binomial(3,0).masses[0],1)
        self.assertEqual(binomial(3,1).masses[3],1)
        self.assertEqual(exact_upper_tail(3,4,F(1,2)),F(5,16))

    def test_wilson_derives_score_inequality_and_symmetry(self):
        for n in [1,5,20,100]:
            for k in range(n+1):
                lo,hi=wilson(k,n)
                self.assertTrue(0<=lo<=hi<=1)
                other=wilson(n-k,n)
                self.assertAlmostEqual(lo,1-other[1])
                self.assertAlmostEqual(hi,1-other[0])
                for p in [lo,hi]:
                    # Original quadratic inequality, independent of interval formula.
                    self.assertAlmostEqual(n*(k/n-p)**2,1.959963984540054**2*p*(1-p),places=10)

    def test_wald_zero_count_failure_and_actual_coverage(self):
        self.assertEqual(wald(0,5),(0,0))
        self.assertGreater(wilson(0,5)[1],0)
        self.assertLess(coverage(5,F(1,50),wald),F(1,2))
        self.assertTrue(0<=coverage(5,F(1,50),wilson)<=1)

    def test_score_interval_contains_exact_parameter_endpoints(self):
        for n in range(1,1001):
            self.assertEqual(wilson(0,n)[0],0.)
            self.assertEqual(wilson(n,n)[1],1.)
        for n in [1,2,5,20,100]:
            self.assertEqual(coverage(n,0),1)
            self.assertEqual(coverage(n,1),1)

    def test_entropy_and_support(self):
        uniform=FiniteDistribution({i:F(1,4) for i in range(4)})
        self.assertEqual(uniform.entropy_bits(),2)
        self.assertEqual(FiniteDistribution({0:1,1:0}).entropy_bits(),0)
        tiny=F(1,2**2000)
        self.assertTrue(math.isfinite(FiniteDistribution({0:tiny,1:1-tiny}).entropy_bits()))

    def test_coverage_preserves_target_beyond_float_resolution(self):
        tiny=F(1,2**1100)
        # At n=1 Wald returns [0,0] or [1,1]; no interior rational parameter
        # belongs to either interval, even if float(p) rounds to0 or1.
        for p in (tiny,1-tiny):
            self.assertEqual(coverage(1,p,wald),0)

    def test_distribution_mass_invariant_cannot_be_mutated(self):
        original={0:F(1,2),1:F(1,2)}
        model=FiniteDistribution(original)
        original[0]=1
        self.assertEqual(model.masses[0],F(1,2))
        with self.assertRaises(TypeError):model.masses[0]=1
        seen=[]
        model.condition(lambda x:seen.append(x) is None and x==0)
        self.assertEqual(seen,[0,1])

    def test_permutation_null_and_exact_extreme_labels(self):
        self.assertEqual(permutation_test([1,1],[1,1])['p_value'],1)
        result=permutation_test([0,0],[1,1])
        self.assertEqual(result['assignments'],6)
        self.assertEqual(result['p_value'],F(1,3))

    def test_invalid_models_and_no_silent_renormalization(self):
        for masses in [{},{0:F(1,3),1:F(1,3)},{0:-1,1:2}]:
            with self.assertRaises(ValueError):FiniteDistribution(masses)
        for args in [(True,1),(2,-.1),(-1,.5)]:
            with self.assertRaises(ValueError):binomial(*args)
        for args in [(1,0),(2,1),(True,2)]:
            with self.assertRaises(ValueError):wilson(*args)
        with self.assertRaises(ValueError):wilson(1,2,math.nan)
        for z in [1e-300,math.inf,1e300,1+0j,True]:
            with self.assertRaises(ValueError):wilson(1,2,z)
        with self.assertRaises(ValueError):wilson(1,10**10)


if __name__=='__main__':unittest.main(verbosity=2)
