import itertools
import math
from fractions import Fraction
import random
import unittest
from linear import dot, matvec, matmul, transpose, identity, solve, quadratic_loss_gradient, gradient_steps


class LinearTests(unittest.TestCase):
    def assertVectorClose(self,a,b,tol=1e-9):
        self.assertEqual(len(a),len(b))
        for x,y in zip(a,b):self.assertLessEqual(abs(x-y),tol)

    def test_worked_map_and_composition_order(self):
        a=[[2,1],[0,3]];b=[[1,0],[-1,1]];x=[2,1]
        self.assertEqual(matvec(a,x),[5,3])
        self.assertEqual(matmul(b,a),[[2,1],[-2,2]])
        self.assertEqual(matvec(matmul(b,a),x),matvec(b,matvec(a,x)))
        self.assertNotEqual(matmul(a,b),matmul(b,a))

    def test_rectangular_map_independent_basis_column_oracle(self):
        rng=random.Random(608)
        for m,n,k in [(1,3,2),(3,2,4),(4,1,3)]:
            a=[[rng.randrange(-3,4) for _ in range(n)] for _ in range(m)]
            b=[[rng.randrange(-3,4) for _ in range(k)] for _ in range(n)]
            product=matmul(a,b)
            for j in range(k):
                column=[sum(a[i][r]*b[r][j] for r in range(n)) for i in range(m)]
                self.assertEqual([product[i][j] for i in range(m)],column)
            self.assertEqual(matmul(identity(m),a),a)
            self.assertEqual(matmul(a,identity(n)),a)

    def test_complex_inner_product_and_unitary_norm(self):
        z=[1+2j,3-1j]
        self.assertEqual(dot(z,z),15)
        self.assertEqual(dot(z,[2j,1]),dot([2j,1],z).conjugate())
        h=[[1/math.sqrt(2),1/math.sqrt(2)],[1/math.sqrt(2),-1/math.sqrt(2)]]
        self.assertAlmostEqual(dot(matvec(h,z),matvec(h,z)).real,dot(z,z).real)
        self.assertEqual(transpose([[1j,2]],True),[[-1j],[2]])

    def test_linearity_exhaustive_small_integer_inputs(self):
        a=[[2,-1],[3,1]]
        for x in itertools.product(range(-2,3),repeat=2):
            for y in itertools.product([-1,0,1],repeat=2):
                lhs=matvec(a,[2*x[i]-3*y[i] for i in range(2)])
                ax,ay=matvec(a,x),matvec(a,y)
                self.assertEqual(lhs,[2*ax[i]-3*ay[i] for i in range(2)])

    def test_pivot_and_exact_fraction_cramers_oracle(self):
        for a,b in [([[0,2],[3,4]],[6,15]),([[3,2],[1,-2]],[7,-3]),([[7,-5],[-4,9]],[2,3])]:
            (aa,bb),(cc,dd)=a;u,v=b
            det=aa*dd-bb*cc
            expected=[Fraction(u*dd-bb*v,det),Fraction(aa*v-u*cc,det)]
            self.assertVectorClose(solve(a,b),list(map(float,expected)))

    def test_system_scaling_and_residual(self):
        a=[[4,1,2],[1,5,-1],[2,-1,6]];known=[2,-3,1]
        b=matvec(a,known)
        for scale in [1e-150,1.0,1e150]:
            aa=[[v*scale for v in row] for row in a]
            self.assertVectorClose(solve(aa,[v*scale for v in b]),known)

    def test_singular_inconsistent_and_tolerance(self):
        for a,b in [([[1,2],[2,4]],[3,6]),([[1,2],[2,4]],[3,7]),([[0,0],[1,1]],[0,1])]:
            with self.assertRaises(ValueError):solve(a,b)
        with self.assertRaises(ValueError):solve([[1,1],[1,1+1e-14]],[2,2])
        with self.assertRaises(ValueError):solve([[1]],[1],rtol=1j)

    def test_gradient_every_coordinate_by_finite_difference(self):
        a=[[2,1],[-1,3],[4,-2]];b=[1,2,-1];x=[.7,-.2]
        loss,g=quadratic_loss_gradient(a,b,x)
        self.assertGreater(loss,0)
        for j in range(2):
            plus=x[:];minus=x[:];h=1e-5;plus[j]+=h;minus[j]-=h
            fd=(quadratic_loss_gradient(a,b,plus)[0]-quadratic_loss_gradient(a,b,minus)[0])/(2*h)
            self.assertAlmostEqual(g[j],fd,places=7)

    def test_convergence_and_deliberate_instability(self):
        stable=gradient_steps([[1]],[3],[0],.25,80)
        self.assertLess(abs(stable[-1]['x'][0]-3),1e-9)
        self.assertTrue(all(b['loss']<=a['loss'] for a,b in zip(stable,stable[1:])))
        unstable=gradient_steps([[1]],[3],[0],2.1,10)
        self.assertGreater(unstable[-1]['loss'],unstable[0]['loss'])

    def test_shape_numeric_and_input_immutability(self):
        for f,args in [(matvec,([[]],[1])),(matmul,([[1,2]],[[1,2]])),(dot,([1],[1,2])),(solve,([[1,2]],[1])),(identity,(True,)),(matvec,([[math.nan]],[1])),(matvec,([[True]],[1]))]:
            with self.assertRaises(ValueError):f(*args)
        a=[[0,1],[1,2]];b=[2,5];before=[r[:] for r in a]
        solve(a,b);self.assertEqual(a,before);self.assertEqual(b,[2,5])


if __name__=='__main__':unittest.main(verbosity=2)
