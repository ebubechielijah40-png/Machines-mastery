import cmath
import math
import random
import unittest
from fourier import MAX_POINTS,circular_convolution,direct_dft,fft,fft_counted,inverse


class FourierTests(unittest.TestCase):
    def assertVector(self,a,b,tol=1e-9):
        self.assertEqual(len(a),len(b))
        for x,y in zip(a,b):self.assertLessEqual(abs(x-y),tol)

    def test_hand_four_point_result_and_sign(self):
        self.assertVector(fft([1,2,3,4]),[10,-2-2j,-2,-2+2j])
        self.assertVector(direct_dft([1,2,3,4]),[10,-2-2j,-2,-2+2j])

    def test_random_complex_cases_against_definition(self):
        rng=random.Random(1965)
        for n in [1,2,4,8,16,32,64,128]:
            data=[complex(rng.uniform(-1,1),rng.uniform(-1,1)) for _ in range(n)]
            self.assertVector(fft(data),direct_dft(data),tol=1e-9)
            self.assertVector(inverse(fft(data)),data)

    def test_impulse_constant_and_single_frequency(self):
        for n in [1,2,4,8,32]:
            self.assertVector(fft([1]+[0]*(n-1)),[1]*n)
            self.assertVector(fft([1]*n),[n]+[0]*(n-1))
            if n>1:
                tone=[cmath.exp(-2j*math.pi*t/n) for t in range(n)]
                expected=[0]*n;expected[1]=n
                self.assertVector(fft(tone),expected)

    def test_counts_and_input_not_mutated(self):
        for n in [1,2,8,64]:
            original=list(range(n));snapshot=original[:]
            result,counts=fft_counted(original)
            self.assertEqual(original,snapshot)
            self.assertEqual(counts['butterflies'],n*(n.bit_length()-1)//2)

    def test_parseval_and_shift_structure(self):
        data=[2,-1,3,0,1,2,-2,1];n=len(data)
        transformed=fft(data)
        self.assertAlmostEqual(sum(abs(z)**2 for z in transformed)/n,sum(abs(x)**2 for x in data))
        shifted=data[-1:]+data[:-1]
        self.assertVector(fft(shifted),[z*cmath.exp(2j*math.pi*k/n) for k,z in enumerate(transformed)])

    def test_convolution_against_independent_nested_loops(self):
        a=[1,2,0,1,0,0,0,0];b=[3,1,2,0,0,0,0,0];n=len(a)
        expected=[sum(a[j]*b[(i-j)%n] for j in range(n)) for i in range(n)]
        self.assertVector(circular_convolution(a,b),expected)

    def test_invalid_lengths_nonfinite_and_resource_caps(self):
        for data in [[],[1,2,3],[math.nan],[math.inf],[object()],range(MAX_POINTS+1)]:
            with self.subTest(data=str(data)[:40]),self.assertRaises(ValueError):fft(data)
        with self.assertRaises(ValueError):circular_convolution([1,2],[1])


if __name__=='__main__':unittest.main(verbosity=2)
