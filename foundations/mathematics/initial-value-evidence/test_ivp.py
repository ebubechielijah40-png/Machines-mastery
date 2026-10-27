from fractions import Fraction as Q
import itertools
import math
import random
import unittest
from ivp import (ContractError,adaptive_rk4,decay_step,integrate_fixed,
                 oscillator_energy,oscillator_step)


def pulse(t,_):
    if not .1 < t < .15:
        return (0.,)
    u = (t-.1)/.05
    return (12012/.05*u**6*(1-u)**6,)


class IVPTests(unittest.TestCase):
    def test_fraction_linear_amplification(self):
        rng = random.Random(7349)
        for _ in range(40):
            y,rate,h = Q(rng.randrange(-12,13),4),Q(rng.randrange(-8,9),4),Q(1,8)
            z = rate*h
            for method,mult in [('euler',1+z),('heun',1+z+z*z/2),
                ('rk4',1+z+z*z/2+z**3/6+z**4/24)]:
                out = integrate_fixed(lambda t,s:(float(rate)*s[0],),0,float(h),
                                      (float(y),),steps=1,method=method)
                self.assertAlmostEqual(out.states[-1][0],float(y*mult),places=13)

    def test_discrete_euler_oracle(self):
        r = integrate_fixed(lambda t,s:(-s[0],),0,1,(1,),steps=8,method='euler')
        self.assertEqual(r.states[-1][0],float(Q(7,8)**8))
        self.assertNotEqual(r.states[-1][0],math.exp(-1))

    def test_manufactured_nonautonomous_polynomial(self):
        r = integrate_fixed(lambda t,s:(1+2*t+3*t*t,),0,2,(2,),steps=5)
        self.assertAlmostEqual(r.states[-1][0],16,places=12)

    def test_order_on_exact_decay(self):
        for method,lo,hi in [('euler',1.9,2.2),('heun',3.9,4.3),('rk4',15.9,17.2)]:
            errs = [abs(integrate_fixed(lambda t,s:(-s[0],),0,1,(1,),steps=n,
                                        method=method).states[-1][0]-math.exp(-1)) for n in (16,32)]
            self.assertGreater(errs[0]/errs[1],lo)
            self.assertLess(errs[0]/errs[1],hi)

    def test_decay_stability_is_not_positivity(self):
        self.assertEqual(decay_step(1,1,1.5),-.5)
        self.assertEqual(decay_step(1,1,2),-1)
        self.assertGreater(abs(decay_step(1,1,3)),1)
        self.assertAlmostEqual(decay_step(1,1000,.1,implicit=True),1/101)

    def test_forward_oscillator_energy(self):
        w,h,n = 2.,.05,150
        r = integrate_fixed(lambda t,s:(s[1],-w*w*s[0]),0,n*h,(1,0),steps=n,method='euler')
        self.assertAlmostEqual(oscillator_energy(*r.states[-1],w)/2,(1+h*h*w*w)**n,places=11)

    def test_symplectic_fraction_and_invariant(self):
        rng = random.Random(192)
        for _ in range(100):
            x,v,w,h = Q(rng.randrange(-20,21),8),Q(rng.randrange(-20,21),8),Q(3,2),Q(1,16)
            vn = v-h*w*w*x
            out = oscillator_step(float(x),float(v),float(w),float(h))
            for a,b in zip(out,(x+h*vn,vn)):
                self.assertAlmostEqual(a,float(b),places=14)
        x,v,w,h = 1.,.3,2.,.05
        invariant = lambda x,v:.5*(v*v+w*w*x*x-h*w*w*x*v)
        original = invariant(x,v)
        for _ in range(4000):
            x,v = oscillator_step(x,v,w,h)
        self.assertAlmostEqual(invariant(x,v),original,places=12)

    def test_adaptive_closed_form_and_call_count(self):
        r = adaptive_rk4(lambda t,s:(-5*s[0],),0,2,(1,),first_step=1,atol=1e-8,rtol=1e-8)
        self.assertGreater(r.rejected,0)
        self.assertEqual(r.field_calls,12*(r.accepted+r.rejected))
        self.assertLess(abs(r.states[-1][0]-math.exp(-10)),1e-7)
        self.assertEqual(r.times[-1],2)

    def test_unit_rescaling(self):
        a = adaptive_rk4(lambda t,s:(-s[0],),0,1,(1,),first_step=.4,atol=1e-6,rtol=1e-6)
        b = adaptive_rk4(lambda t,s:(-s[0],),0,1,(1000,),first_step=.4,atol=.001,rtol=1e-6)
        self.assertEqual((a.accepted,a.rejected),(b.accepted,b.rejected))
        self.assertAlmostEqual(a.states[-1][0],b.states[-1][0]/1000,places=12)

    def test_zero_duration_and_final_allowed_attempt(self):
        def bad(t,s):
            raise AssertionError('must not call')
        for fn,kw in [(integrate_fixed,{'steps':1}),(adaptive_rk4,{'first_step':1})]:
            r = fn(bad,2,2,(1,),**kw)
            self.assertEqual((r.accepted,r.field_calls),(0,0))
        r = adaptive_rk4(lambda t,s:(1,),0,1,(0,),first_step=1,max_attempts=1)
        self.assertAlmostEqual(r.states[-1][0],1)

    def test_resource_and_progress_boundaries(self):
        with self.assertRaisesRegex(ContractError,'field-call'):
            integrate_fixed(lambda t,s:s,0,1,(1,),steps=1,max_calls=3)
        with self.assertRaisesRegex(ContractError,'attempt budget'):
            adaptive_rk4(lambda t,s:(-s[0],),0,2,(1,),first_step=1,atol=1e-15,rtol=0,max_attempts=1)
        with self.assertRaisesRegex(ContractError,'min_step'):
            adaptive_rk4(lambda t,s:(-s[0],),0,2,(1,),first_step=1,atol=1e-15,rtol=0,min_step=.9)
        with self.assertRaisesRegex(ContractError,'mesh cannot advance'):
            integrate_fixed(lambda t,s:s,1e16,1e16+2,(1,),steps=4)

    def test_nonfinite_shape_and_bounded_iterator(self):
        for bad in [(),(math.inf,),(True,),('1',),itertools.repeat(1)]:
            with self.assertRaises(ContractError):
                integrate_fixed(lambda t,s:s,0,1,bad,steps=1)
        with self.assertRaises(ContractError):
            integrate_fixed(lambda t,s:itertools.repeat(1),0,1,(1,),steps=1)
        with self.assertRaises(ContractError):
            integrate_fixed(lambda t,s:(math.nan,),0,1,(1,),steps=1)
        with self.assertRaises(ContractError):
            adaptive_rk4(lambda t,s:s,0,1,(1,),first_step=1,atol=True)
        with self.assertRaises(ContractError):
            oscillator_energy(1e308,1,2)

    def test_smooth_pulse_local_agreement_failure(self):
        integral = sum(((-1)**j*math.comb(6,j)*Q(1,7+j) for j in range(7)),Q(0))
        self.assertEqual(integral,Q(1,12012))
        blind = adaptive_rk4(pulse,0,1,(0,),first_step=1,atol=1e-10,rtol=1e-10)
        self.assertEqual((blind.states[-1],blind.field_calls,blind.accepted),((0.,),12,1))
        known = adaptive_rk4(pulse,.1,.15,(0,),first_step=.05,atol=1e-10,rtol=1e-10)
        self.assertAlmostEqual(known.states[-1][0],1,places=7)


if __name__ == '__main__':
    unittest.main(verbosity=2)
