from fractions import Fraction as Q
import itertools
import unittest
from decision import UpperTest, minimum_n, monitor_upper, rejection_probability, upper_test


def enumerate_first_hit(boundaries,p):
    """Independent full paths; deliberately capped at12 in the test oracle."""
    n=len(boundaries)
    if n>12:
        raise ValueError('exponential oracle only for n<=12')
    first=[Q(0)]*n
    survived=Q(0)
    for bits in itertools.product((0,1),repeat=n):
        mass=p**sum(bits)*(1-p)**(n-sum(bits))
        k=0
        for look,bit in enumerate(bits):
            k+=bit
            if k>=boundaries[look]:
                first[look]+=mass
                break
        else:
            survived+=mass
    return tuple(first),survived


class DecisionTests(unittest.TestCase):
    def test_exact_worked_threshold_and_never_reject(self):
        r=upper_test(5,Q(1,2),Q(1,4))
        self.assertEqual((r.critical,r.size),(4,Q(3,16)))
        self.assertFalse(r.reject(3));self.assertTrue(r.reject(4))
        r=upper_test(4,Q(1,2),Q(1,20))
        self.assertEqual((r.critical,r.size),(5,0))

    def test_critical_minimality_by_independent_binary_paths(self):
        for n in range(1,9):
            for p0 in (Q(0),Q(1,3),Q(1,2),Q(1)):
                alpha=Q(1,10)
                rule=upper_test(n,p0,alpha)
                size=Q(0);previous=Q(0)
                for bits in itertools.product((0,1),repeat=n):
                    k=sum(bits);mass=p0**k*(1-p0)**(n-k)
                    if k>=rule.critical:size+=mass
                    if k>=rule.critical-1:previous+=mass
                self.assertEqual(size,rule.size)
                self.assertLessEqual(size,alpha)
                if rule.critical>0:self.assertGreater(previous,alpha)

    def test_exact_power_against_labeled_paths(self):
        rule=upper_test(6,Q(1,2),Q(1,10))
        p=Q(2,3)
        expected=sum((p**sum(b)*(1-p)**(6-sum(b)) for b in itertools.product((0,1),repeat=6)
                      if sum(b)>=rule.critical),Q(0))
        self.assertEqual(rejection_probability(rule,p),expected)

    def test_composite_null_operating_curve(self):
        rule=upper_test(30,Q(1,2),Q(1,20))
        values=[rejection_probability(rule,Q(i,20)) for i in range(21)]
        self.assertEqual(values,sorted(values))
        self.assertTrue(all(v<=rule.alpha for v in values[:11]))

    def test_boundary_alpha_and_degenerate_models(self):
        self.assertEqual((upper_test(5,0,0).critical,upper_test(5,0,0).size),(1,0))
        self.assertEqual((upper_test(5,1,0).critical,upper_test(5,1,0).size),(6,0))
        self.assertEqual((upper_test(5,Q(1,2),1).critical,upper_test(5,Q(1,2),1).size),(0,1))

    def test_power_not_monotone_in_every_sample_size(self):
        five=upper_test(5);six=upper_test(6)
        self.assertEqual((five.critical,six.critical),(5,6))
        self.assertGreater(rejection_probability(five,Q(7,10)),rejection_probability(six,Q(7,10)))

    def test_minimum_sample_plan_and_bounded_failure(self):
        plan=minimum_n(Q(1,2),Q(7,10),target_power=Q(4,5),max_n=100)
        self.assertIsNotNone(plan.selected)
        self.assertTrue(all(row.power<plan.target_power for row in plan.evaluated[:-1]))
        self.assertGreaterEqual(plan.evaluated[-1].power,plan.target_power)
        self.assertEqual(plan.evaluated[-1].n,plan.selected.n)
        short=minimum_n(Q(1,2),Q(7,10),max_n=4)
        self.assertIsNone(short.selected)
        self.assertEqual(len(short.evaluated),4)

    def test_first_crossing_dp_against_complete_path_oracle(self):
        for n in (1,5,8):
            for policy in ('final','repeat','spend'):
                for p in (Q(0),Q(1,3),Q(1,2),Q(1)):
                    result=monitor_upper(n,actual_p=p,alpha=Q(1,4),policy=policy)
                    first,survival=enumerate_first_hit(result.critical_counts,p)
                    self.assertEqual(result.first_crossing,first)
                    self.assertEqual(result.survival[-1],survival)
                    self.assertEqual(result.rejection_probability+survival,1)
                    self.assertLessEqual(result.transitions,n*(n+1))

    def test_final_look_matches_single_test(self):
        for p in (Q(1,3),Q(1,2),Q(2,3)):
            result=monitor_upper(25,actual_p=p,policy='final')
            self.assertEqual(result.rejection_probability,rejection_probability(upper_test(25),p))
            self.assertTrue(all(m==0 for m in result.first_crossing[:-1]))

    def test_ten_look_first_hit_hand_count(self):
        result=monitor_upper(10)
        # First hit at5: five ones, mass1/32. New hit at8: exactly one zero
        # among positions1..5 and ones elsewhere, five paths each mass1/256.
        self.assertEqual(result.first_crossing[4],Q(1,32))
        self.assertEqual(result.first_crossing[7],Q(5,256))
        self.assertEqual(sum(m for i,m in enumerate(result.first_crossing) if i not in (4,7)),0)
        self.assertEqual(result.rejection_probability,Q(13,256))

    def test_monitor_conservation_and_stopping_inflation(self):
        result=monitor_upper(60)
        for look,survival in enumerate(result.survival):
            self.assertEqual(sum(result.first_crossing[:look],Q(0))+survival,1)
        self.assertGreater(result.rejection_probability,Q(1,20))
        spent=monitor_upper(60,policy='spend')
        self.assertLessEqual(spent.rejection_probability,Q(1,20))
        self.assertGreater(result.rejection_probability,spent.rejection_probability)

    def test_spending_control_for_composite_null(self):
        for p in (Q(0),Q(1,4),Q(1,2)):
            r=monitor_upper(20,actual_p=p,policy='spend')
            self.assertLessEqual(r.rejection_probability,r.alpha)

    def test_invalid_parameters_and_arithmetic_budget(self):
        for n in (True,0,-1,201,2.5):
            with self.assertRaises(ValueError):upper_test(n)
        for p in (True,-Q(1,10),Q(11,10),Q(1,2**100)):
            with self.assertRaises(ValueError):upper_test(5,p)
        with self.assertRaises(ValueError):upper_test(5).reject(True)
        with self.assertRaises(ValueError):upper_test(5).reject(6)
        with self.assertRaises(ValueError):minimum_n(Q(1,2),Q(1,2))
        with self.assertRaises(ValueError):minimum_n(Q(1,2),Q(3,4),target_power=0)
        with self.assertRaises(ValueError):monitor_upper(5,policy='choose-after-data')
        with self.assertRaises(ValueError):enumerate_first_hit([1]*13,Q(1,2))

    def test_manual_record_cannot_silently_use_negative_index(self):
        for bad in (-1,7,True,2.5):
            with self.assertRaises(ValueError):UpperTest(5,Q(1,2),Q(1,20),bad,Q(0))
        with self.assertRaises(ValueError):UpperTest(5,Q(1,2),Q(1,20),5,Q(1,10))
        with self.assertRaises(ValueError):UpperTest(201,Q(1,2),Q(1,20),5,Q(0))
        # Manually chosen thresholds can be valid records without calibration.
        manual=UpperTest(5,Q(1,2),Q(1,20),1,Q(0))
        self.assertEqual(rejection_probability(manual,Q(1,2)),Q(31,32))


if __name__=='__main__':
    unittest.main(verbosity=2)
