from fractions import Fraction
from itertools import product
import unittest
from operations import Observation
from telemetry import aggregate,merge,quantile_upper_bound,burn_alert,validate


def record(i,latency,status='ok'):
    return Observation(str(i),0,0,0,latency,status,None)


class TelemetryTests(unittest.TestCase):
    def test_every_split_pools_exact_cumulative_counts(self):
        for values in product((0,1,2,5,10),repeat=5):
            rows=[record(i,x) for i,x in enumerate(values)]
            whole=aggregate(rows,5,(1,2,5))
            pooled=merge([aggregate(rows[:2],5,(1,2,5)),aggregate(rows[2:],5,(1,2,5))])
            self.assertEqual(pooled,whole)
            self.assertEqual(whole['le_counts'],[sum(x<=b for x in values) for b in (1,2,5)])

    def test_average_of_percentiles_is_wrong(self):
        a=aggregate([record(i,1) for i in range(99)],100,(1,100))
        b=aggregate([record(99,100)],100,(1,100))
        self.assertEqual(quantile_upper_bound(merge([a,b]),Fraction(95,100)),1)
        self.assertEqual((quantile_upper_bound(a,Fraction(95,100))+quantile_upper_bound(b,Fraction(95,100)))/2,50.5)

    def test_two_window_policy_and_empty_denominators(self):
        short=aggregate([record(i,1,'ok' if i<9 else 'overload') for i in range(10)],5)
        long=aggregate([record(i,1,'ok' if i<27 else 'overload') for i in range(30)],5)
        out=burn_alert(short,long)
        self.assertTrue(out['alert']);self.assertEqual((out['short_burn_exact'],out['long_burn_exact']),('2','2'))
        empty=aggregate([],5)
        self.assertEqual(burn_alert(empty,long)['status'],'insufficient_population')
        self.assertIsNone(quantile_upper_bound(empty,Fraction(1,2)))

    def test_overflow_and_schema_conservation(self):
        out=aggregate([record(1,11)],5,(1,10))
        self.assertIsNone(quantile_upper_bound(out,Fraction(1)))
        self.assertEqual(out['overflow'],1)
        bad={**out,'overflow':0}
        with self.assertRaises(ValueError):validate(bad)
        with self.assertRaises(ValueError):merge([out,aggregate([],6,(1,10))])
        with self.assertRaises(ValueError):aggregate([record(0,1,'arbitrary-id')],5)

    def test_bounds_finite_windows_and_non_boolean_counts(self):
        for bounds in [(),(1,1),(2,1),(True,)]:
            with self.assertRaises(ValueError):aggregate([],1,bounds)
        with self.assertRaises(ValueError):aggregate((record(i,1) for i in range(5001)),1)
        out=aggregate([],1);out['count']=True
        with self.assertRaises(ValueError):validate(out)

    def test_reader_corruption_and_composition_regressions(self):
        out=aggregate([record(1,1,'overload')],5);out['good']=1
        with self.assertRaises(ValueError):validate(out)
        out=aggregate([],5);out['latency_sum_ns']=1
        with self.assertRaises(ValueError):validate(out)
        with self.assertRaises(ValueError):aggregate([],10**31)


if __name__=='__main__':unittest.main()
