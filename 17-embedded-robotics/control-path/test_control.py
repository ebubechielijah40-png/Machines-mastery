import math
import random
import unittest
from control_lab import Motor,BoundedPID,Sensor,closed_loop,reflected_inertia


class ControlTests(unittest.TestCase):
    def test_hand_first_derivative(self):
        got=Motor().derivative((1,3,0),6,.01)
        self.assertAlmostEqual(got[0],185)
        self.assertAlmostEqual(got[1],1.5)
        self.assertEqual(got[2],3)

    def test_energy_identity_independent_of_integrator(self):
        rng=random.Random(6);m=Motor()
        for _ in range(100):
            i,w,v,load=[rng.uniform(-3,3) for _ in range(4)]
            di,dw,_=m.derivative((i,w,0),v,load)
            stored_rate=m.inductance*i*di+m.inertia*w*dw
            net=v*i-m.resistance*i*i-m.damping*w*w-load*w
            self.assertAlmostEqual(stored_rate,net,places=11)

    def test_uncoupled_analytic_rl_and_mechanical_decay(self):
        m=Motor(k=0);state=(0.,2.,0.)
        for _ in range(100):state=m.step(state,1,.001)
        self.assertAlmostEqual(state[0],.5*(1-math.exp(-10)),places=8)
        self.assertAlmostEqual(state[1],2*math.exp(-.1),places=11)

    def test_zero_input_equilibrium_and_time_reversal_sign_symmetry(self):
        m=Motor();self.assertEqual(m.step((0,0,0),0,.001),(0,0,0))
        plus=m.step((1,2,3),4,.001,.1)
        minus=m.step((-1,-2,-3),-4,.001,-.1)
        for a,b in zip(plus,minus):self.assertAlmostEqual(a,-b)

    def test_voltage_limit_and_conditional_integration(self):
        c=BoundedPID(2,1,0,limit=3)
        for _ in range(100):self.assertEqual(c.step(10,0,.01),3)
        self.assertEqual(c.integral,0)
        d=BoundedPID(2,1,0,limit=3,anti_windup=False)
        for _ in range(100):d.step(10,0,.01)
        self.assertAlmostEqual(d.integral,10)

    def test_derivative_on_measurement_avoids_target_kick(self):
        c=BoundedPID(0,0,1)
        self.assertEqual(c.step(0,1,.1),0)
        self.assertEqual(c.step(100,1,.1),0)
        self.assertLess(c.step(100,2,.1),0)

    def test_quantization_bias_delay_and_seed(self):
        s=Sensor(delay_steps=2,bias=.1,quantum=.5)
        self.assertEqual([s.read(x) for x in [0,1,2,3]],[0,0,0,1])
        a,b=Sensor(noise_sd=.2,seed=7),Sensor(noise_sd=.2,seed=7)
        self.assertEqual([a.read(1) for _ in range(10)],[b.read(1) for _ in range(10)])

    def test_gear_inertia_from_energy_equivalence(self):
        self.assertEqual(reflected_inertia(.8,4),.05)
        self.assertAlmostEqual(.5*.8*(12/4)**2,.5*reflected_inertia(.8,4)*12**2)

    def test_windup_counterexample_and_steady_state(self):
        a=closed_loop(BoundedPID(1,2,0),steps=4000)
        b=closed_loop(BoundedPID(1,2,0,anti_windup=False),steps=4000)
        self.assertLess(abs(a[-1]['speed_rad_s']-2),.2)
        def error(rows):return sum(abs(r['speed_rad_s']-2)*.002 for r in rows if r['time_s']>=4)
        self.assertLess(error(a),error(b))
        self.assertTrue(all(abs(r['voltage_V'])<=6 for r in a+b))

    def test_invalid_parameters_and_failed_step_preserves_controller(self):
        for kwargs in [dict(inertia=0),dict(resistance=-1),dict(k=float('nan'))]:
            with self.assertRaises(ValueError):Motor(**kwargs)
        c=BoundedPID(1,1,1);before=c.__dict__.copy()
        for args in [(1,0,0),(float('inf'),0,.1)]:
            with self.assertRaises(ValueError):c.step(*args)
        self.assertEqual(c.__dict__,before)
        with self.assertRaises(ValueError):Sensor(delay_steps=True)
        with self.assertRaises(ValueError):Motor().step((0,0),1,.01)

if __name__=='__main__':unittest.main(verbosity=2)
