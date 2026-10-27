import math
import unittest
from discrete import extended_gcd,modular_power,page_count


class DiscreteTests(unittest.TestCase):
    def test_bezout_and_independent_gcd(self):
        for a in range(-25,26):
            for b in range(-25,26):
                g,s,t=extended_gcd(a,b)
                self.assertEqual(g,math.gcd(a,b));self.assertEqual(g,s*a+t*b)

    def test_modular_power_against_repeated_product(self):
        for base in range(-4,5):
            for exponent in range(9):
                for modulus in range(1,10):
                    self.assertEqual(modular_power(base,exponent,modulus),base**exponent%modulus)

    def test_page_budget_from_defining_inequality(self):
        for n in range(101):
            for p in range(1,17):
                k=page_count(n,p)
                if n:self.assertTrue((k-1)*p<n<=k*p)
                else:self.assertEqual(k,0)

    def test_input_contracts(self):
        for f,args in [(extended_gcd,(True,1)),(modular_power,(2,-1,3)),(modular_power,(2,1,0)),(page_count,(-1,4)),(page_count,(1,0))]:
            with self.assertRaises(ValueError):f(*args)


if __name__=='__main__':unittest.main(verbosity=2)
