"""Analytic, finite-difference, shared-path and repeated-pass contracts."""
import math
import unittest
from autodiff import Value


def test_product_chain():
    x,w = Value(3),Value(2)
    y=(x*w+1)**2
    y.backward()
    assert abs(y.data-49)<1e-6
    assert abs(w.grad-42)<1e-6
    assert abs(x.grad-28)<1e-6


def test_branch_accumulates():
    x=Value(4)
    (x*x+x).backward()
    assert abs(x.grad-9)<1e-6


class AutodiffTests(unittest.TestCase):
    def test_original_contracts(self):
        test_product_chain()
        test_branch_accumulates()

    def test_repeated_pass_and_explicit_leaf_accumulation(self):
        x=Value(3); y=(x*x+1)**2
        y.backward(); self.assertEqual(x.grad,120)
        y.backward(); self.assertEqual(x.grad,120)
        y.backward(accumulate=True); self.assertEqual(x.grad,240)
        y.backward(seed=2); self.assertEqual(x.grad,240)

    def test_different_roots_accumulate_only_leaves(self):
        x=Value(2); a=x*x; b=a*a; c=a+1
        b.backward(); self.assertEqual(x.grad,32)
        c.backward(accumulate=True); self.assertEqual(x.grad,36)
        self.assertEqual(a.grad,1)

    def test_elementary_derivatives_against_central_differences(self):
        scalar=lambda x:math.log(math.exp(x)+2)+math.tanh(x*x-1)/(x+3)
        x=Value(.4)
        y=(x.exp()+2).log()+(x*x-1).tanh()/(x+3)
        y.backward();h=1e-5
        self.assertAlmostEqual(x.grad,(scalar(.4+h)-scalar(.4-h))/(2*h),places=8)

    def test_constant_power_zero_and_shared_edges(self):
        x=Value(0); (x**0).backward();self.assertEqual(x.grad,0)
        z=Value(2); ((z+z)*(z+z)).backward();self.assertEqual(z.grad,16)

    def test_snapshot_local_derivative_and_rebuild_contract(self):
        x=Value(3); y=x*x; x.data=4
        y.backward();self.assertEqual(x.grad,6)
        (x*x).backward();self.assertEqual(x.grad,8)

    def test_deep_iterative_traversal(self):
        x=Value(1); y=x
        for _ in range(2000): y=y+1
        y.backward();self.assertEqual(x.grad,1)

    def test_domain_rejection(self):
        for x in [math.nan, math.inf]:
            with self.assertRaises(ValueError): Value(x)
        with self.assertRaises(ValueError):Value(0).log()
        with self.assertRaises(ValueError):Value(0)**-1
        with self.assertRaises(ValueError):Value(-1)**.5


if __name__=='__main__':unittest.main(verbosity=2)
