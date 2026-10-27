from fractions import Fraction
import math
import unittest
from oracle import query
from reconstruction import Calibration,Model,calibrate,stiffness,fit_free,model_from_fit


def identify(case,dt=.05,noise=0):
    calibration=query(case,'calibrate',values=[-.02,.02])
    cal=calibrate(*[v for pair in zip(calibration['coordinates'],calibration['readings']) for v in pair])
    balance=query(case,'balance',values=[-.3,.6])
    k=stiffness(balance['drives'][0],balance['readings'][0],balance['drives'][1],balance['readings'][1],cal)
    observation=query(case,dt=dt,samples=min(201,int(10/dt)+1),noise_bound=noise)
    fit=fit_free([cal.coordinate(y) for y in observation['readings']],dt)
    return cal,model_from_fit(fit,k),fit


class PlantTests(unittest.TestCase):
    def test_calibration_negative_gain_and_two_equilibria(self):
        cal=calibrate(-.01,14,.01,6)
        self.assertEqual((cal.gain,cal.offset),(-400,10))
        self.assertEqual(cal.coordinate(8),.005)
        self.assertAlmostEqual(stiffness(0,10,1,-70,cal),5)

    def test_exact_fraction_recurrence_recovers_poles(self):
        a,c=Fraction(3,4),Fraction(-1,4);z=[Fraction(1),Fraction(0)]
        for _ in range(18):z.append(a*z[-1]+c*z[-2])
        fit=fit_free([float(x) for x in z],.2)
        self.assertAlmostEqual(fit.coefficient_a,float(a),places=13)
        self.assertAlmostEqual(fit.coefficient_c,float(c),places=13)
        self.assertAlmostEqual(fit.decay,math.log(2)/.2,places=12)
        self.assertAlmostEqual(fit.frequency,math.acos(.75)/.2,places=12)
        self.assertLess(fit.residual_rms,1e-15)

    def test_independent_rk4_first_order_state(self):
        # Integrate state equations; no trig/exponential closed-form oracle.
        model=Model(2,.8,18);q,v=.017,-.03;h=.0005;u=.25
        def slope(q,v):return v,(u-.8*v-18*q)/2
        for _ in range(6000):
            p1=slope(q,v);p2=slope(q+h*p1[0]/2,v+h*p1[1]/2)
            p3=slope(q+h*p2[0]/2,v+h*p2[1]/2);p4=slope(q+h*p3[0],v+h*p3[1])
            q+=h*(p1[0]+2*p2[0]+2*p3[0]+p4[0])/6
            v+=h*(p1[1]+2*p2[1]+2*p3[1]+p4[1])/6
        self.assertAlmostEqual(q,model.response(3,.017,-.03,.25),places=12)

    def test_four_cases_and_unseen_forced_holdout(self):
        expected={'amber':(2,.8,18),'slate':(.75,.3,6.75),'glass':(2,.8,18),'copper':(1.25,1,5)}
        for case,truth in expected.items():
            cal,model,fit=identify(case)
            for observed,wanted in zip((model.inertia,model.loss,model.stiffness),truth):self.assertAlmostEqual(observed,wanted,places=9)
            hold=query(case,coordinate=-.013,velocity=.027,drive=.31,dt=.037,samples=101)
            error=max(abs(cal.coordinate(y)-model.response(i*.037,-.013,.027,.31)) for i,y in enumerate(hold['readings']))
            self.assertLess(error,1e-10)

    def test_topology_is_not_identified_by_port(self):
        for mode,kwargs in [('calibrate',dict(values=[-.1,.02])),('balance',dict(values=[0,1])),('release',dict(coordinate=.2,velocity=-.3,drive=.4,dt=.17,samples=101))]:
            self.assertEqual(query('amber',mode,**kwargs),query('glass',mode,**kwargs))

    def test_free_response_does_not_set_coefficient_scale(self):
        a,b=Model(2,.8,18),Model(6,2.4,54)
        for i in range(60):self.assertAlmostEqual(a.response(i*.1,.01,0),b.response(i*.1,.01,0),places=15)
        self.assertNotAlmostEqual(a.response(1,0,0,1),b.response(1,0,0,1),places=5)

    def test_alias_frequencies_share_pure_cosine_samples(self):
        alpha,omega,h=.2,3.,.2;k=18
        def model(f):
            m=k/(alpha*alpha+f*f)
            return Model(m,2*alpha*m,k)
        a,b=model(omega),model(omega+2*math.pi/h)
        for i in range(41):self.assertAlmostEqual(a.response(i*h,.01,-alpha*.01),b.response(i*h,.01,-alpha*.01),places=13)
        self.assertGreater(abs(a.response(.071,.01,-alpha*.01)-b.response(.071,.01,-alpha*.01)),.005)

    def test_offset_error_fails_transfer(self):
        cal,model,_=identify('amber')
        wrong=Calibration(cal.gain,0)
        observation=query('amber')
        try:bad=model_from_fit(fit_free([wrong.coordinate(y) for y in observation['readings']],.05),18)
        except ValueError:return
        self.assertGreater(abs(bad.response(1,-.013,.027,.31)-model.response(1,-.013,.027,.31)),1e-3)

    def test_noise_is_reproducible_not_a_confidence_bound(self):
        a=query(noise_bound=.2,seed=10);b=query(noise_bound=.2,seed=10);clean=query()
        self.assertEqual(a,b)
        self.assertTrue(all(abs(x-y)<=.2 for x,y in zip(a['readings'],clean['readings'])))

    def test_unexcited_and_wrong_regimes_refused(self):
        for z in ([0]*10,[1]*10,[2.**i for i in range(10)]):
            with self.assertRaises(ValueError):fit_free(z,.1)
        for values in [(0,1,1),(1,-1,1),(1,2,1)]:
            with self.assertRaises(ValueError):Model(*values)

    def test_oracle_public_bounds(self):
        for kwargs in [dict(dt=True),dict(samples=True),dict(samples=4097),dict(dt=1,samples=62),dict(seed=-1),dict(coordinate=float('nan')),dict(mode='balance',values=[0]),dict(case=[]),dict(values=[0,1])]:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):query(**kwargs)

    def test_reconstruction_numeric_boundaries(self):
        for args in [(0,1,0,2),(0,1,1,1)]:
            with self.assertRaises(ValueError):calibrate(*args)
        for coordinates,dt in [([1]*4,.1),([0]*5000,.1),([float('inf')]*6,.1),([1]*6,0),([1]*6,True)]:
            with self.assertRaises(ValueError):fit_free(coordinates,dt)
        with self.assertRaises(ValueError):Calibration(1e-320,0).coordinate(1e300)
        with self.assertRaises(ValueError):Model(2,.8,18).response(61)


if __name__=='__main__':unittest.main()
