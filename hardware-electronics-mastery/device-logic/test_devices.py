from decimal import Decimal,localcontext
import itertools,math,unittest
from devices import (Q,carriers,conductivity,nmos_current,resistor_load_dc,transient,
                     gate_network,timing_slacks,ripple_add)

class DeviceTests(unittest.TestCase):
    def test_neutrality_mass_action_and_compensation(self):
        for ni in (1e10,1e16,1e20):
            for d in (0,1e10,1e16,1e20,1e25):
                for donors,acceptors in ((d,0),(0,d),(d,d)):
                    c=carriers(ni,donors,acceptors);n,p=c.values()
                    self.assertTrue(math.isclose(n*p,ni*ni,rel_tol=1e-14))
                    self.assertLessEqual(abs((n-p)-(donors-acceptors)),8*math.ulp(max(n,p)))
        self.assertEqual(carriers(1e16,1e23,1e23),carriers(1e16))

    def test_majority_root_against_decimal(self):
        with localcontext() as ctx:
            ctx.prec=70
            ni=Decimal('1e10');d=Decimal('1e25');n=(d+(d*d+4*ni*ni).sqrt())/2
            c=carriers(float(ni),float(d));self.assertAlmostEqual(c['electrons_per_m3']/float(n),1)
            self.assertAlmostEqual(c['holes_per_m3']/float(ni*ni/n),1)

    def test_conductivity_units(self):
        self.assertAlmostEqual(conductivity(1e20,1e16,.1,.05)/(Q*(1e19+5e14)),1)

    def test_current_regions_continuity_and_finite_difference(self):
        beta,vt,vg=1e-3,1,3
        self.assertEqual(nmos_current(vt,5,beta,vt),0)
        self.assertEqual(nmos_current(vg,0,beta,vt),0)
        self.assertAlmostEqual(nmos_current(vg,1,beta,vt),.0015)
        self.assertAlmostEqual(nmos_current(vg,2,beta,vt),.002)
        self.assertEqual(nmos_current(vg,2,beta,vt),nmos_current(vg,20,beta,vt))
        h=1e-5;v=1.2
        derivative=(nmos_current(vg,v+h,beta,vt)-nmos_current(vg,v-h,beta,vt))/(2*h)
        self.assertAlmostEqual(derivative,beta*(vg-vt-v),places=12)
        for v in (1.99999999,2.00000001):self.assertTrue(math.isclose(nmos_current(vg,v,beta,vt),.002,rel_tol=1e-12))

    def test_resistor_load_kcl_and_quadratic_oracle(self):
        for vin in (0,1,1.5,2,3,4,5):
            result=resistor_load_dc(vin,5,10000,1e-3,1);out=result['output_V']
            self.assertTrue(0<=out<=5)
            self.assertAlmostEqual((5-out)/10000,nmos_current(vin,out,1e-3,1),places=15)
        # At vin5 the root is in triode: .0005*v²-.0041*v+.0005=0.
        expected=.001/(.0041+math.sqrt(.0041**2-4*.0005*.0005))
        self.assertAlmostEqual(resistor_load_dc(5,5,10000,1e-3,1)['output_V'],expected,places=13)

    def test_transient_rc_limit_convergence_and_energy_residual(self):
        errors=[]
        for dt,n in ((1e-9,100),(5e-10,200)):
            result=transient(0,0,5,10000,1e-11,1e-3,1,dt,n)
            observed=result['trace'][-1]['output_V'];exact=5*(-math.expm1(-1))
            errors.append(abs(observed-exact));energy=result['energy']
            self.assertTrue(math.isclose(energy['balance_residual_J'],energy['predicted_euler_residual_J'],rel_tol=1e-10,abs_tol=1e-23))
        self.assertGreater(errors[0]/errors[1],1.99)
        self.assertLess(errors[0]/errors[1],2.02)
        with self.assertRaises(ValueError): transient(0,0,5,10000,1e-11,1e-3,1,1e-6,1)

    def test_gate_complements_and_adder_exhaustive(self):
        for a,b in itertools.product((0,1),repeat=2):
            self.assertEqual(gate_network('nand',a,b),1-(a&b))
            self.assertEqual(gate_network('nor',a,b),1-(a|b))
        for a in range(256):
            for b in range(256):
                out,carry=ripple_add(a,b,8);self.assertEqual(out+256*carry,a+b)

    def test_setup_hold_and_skew_signs(self):
        params=dict(period_s=10e-9,cq_min_s=.2e-9,cq_max_s=1e-9,logic_min_s=.3e-9,
                    logic_max_s=5e-9,setup_s=1e-9,hold_s=.4e-9)
        r=timing_slacks(**params);self.assertAlmostEqual(r['setup_slack_s']/1e-9,3)
        self.assertAlmostEqual(r['hold_slack_s']/1e-9,.1)
        skewed=timing_slacks(**params,skew_s=.2e-9)
        self.assertAlmostEqual(skewed['setup_slack_s']/1e-9,3.2)
        self.assertLess(skewed['hold_slack_s'],0)
        slower=timing_slacks(**dict(params,period_s=100e-9),skew_s=.2e-9)
        self.assertAlmostEqual(slower['hold_slack_s'],skewed['hold_slack_s'])

    def test_invalid_inputs(self):
        for bad in (None,True,'1',float('nan'),float('inf'),10**1000):
            with self.assertRaises(ValueError):carriers(bad)
            with self.assertRaises(ValueError):nmos_current(2,bad,1,1)
            with self.assertRaises(ValueError):resistor_load_dc(2,5,bad,1,1)
        with self.assertRaises(ValueError):carriers(1e-300,1e25)
        with self.assertRaises(ValueError):nmos_current(2,-1,1,1)
        with self.assertRaises(ValueError):gate_network('nand',True,0)
        with self.assertRaises(ValueError):ripple_add(256,0,8)
        with self.assertRaises(ValueError):timing_slacks(1,2,1,0,0,0,0)

if __name__=='__main__':unittest.main(verbosity=2)
