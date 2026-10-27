from fractions import Fraction
import hashlib,json,unittest
from measurement_pipeline import MAX_BYTES,parse_samples,summarize

RAW=b'seq,value_milli_c\n1,25000\n2,25002\n3,24998\n'

class MeasurementTests(unittest.TestCase):
    def test_hand_derived_exact_three_point_example(self):
        out=summarize(RAW,offset_milli_c=-10,calibration_u_milli_c=5)
        self.assertEqual(out['corrected_mean_milli_c'],{'numerator':24990,'denominator':1})
        self.assertEqual(out['sample_variance_milli_c_squared'],{'numerator':4,'denominator':1})
        self.assertEqual(out['repeatability_variance_of_mean_milli_c_squared'],{'numerator':4,'denominator':3})
        self.assertEqual(out['combined_variance_milli_c_squared'],{'numerator':79,'denominator':3})
        self.assertAlmostEqual(out['combined_standard_uncertainty_celsius'],(79/3)**.5/1000)
    def test_offset_moves_mean_not_scatter_or_uncertainty(self):
        a=summarize(RAW,offset_milli_c=0,calibration_u_milli_c=5)
        b=summarize(RAW,offset_milli_c=50,calibration_u_milli_c=5)
        self.assertEqual(b['corrected_mean_milli_c']['numerator']-a['corrected_mean_milli_c']['numerator'],50)
        self.assertEqual(a['combined_variance_milli_c_squared'],b['combined_variance_milli_c_squared'])
    def test_zero_scatter_does_not_remove_calibration_uncertainty(self):
        out=summarize(b'seq,value_milli_c\n1,25000\n2,25000\n',calibration_u_milli_c=5)
        self.assertEqual(out['sample_variance_milli_c_squared']['numerator'],0)
        self.assertEqual(out['combined_variance_milli_c_squared'],{'numerator':25,'denominator':1})
    def test_source_identity_changes_with_bytes_even_same_values(self):
        altered=RAW.replace(b'25002',b'24998').replace(b'3,24998',b'3,25002')
        self.assertEqual(sorted(parse_samples(RAW)),sorted(parse_samples(altered)))
        self.assertNotEqual(summarize(RAW)['input_sha256'],summarize(altered)['input_sha256'])
        self.assertEqual(summarize(RAW)['input_sha256'],hashlib.sha256(RAW).hexdigest())
        self.assertEqual(json.dumps(summarize(RAW),sort_keys=True),json.dumps(summarize(RAW),sort_keys=True))
    def test_independent_variance_oracle_small_samples(self):
        for values in [[0,1],[3,5,8],[-4,-1,9,11]]:
            raw=('seq,value_milli_c\n'+''.join(f'{i},{x}\n' for i,x in enumerate(values,1))).encode()
            n=len(values);pair_differences=sum((a-b)**2 for a in values for b in values)
            oracle=Fraction(pair_differences,2*n*(n-1))
            self.assertEqual(summarize(raw)['sample_variance_milli_c_squared'],{'numerator':oracle.numerator,'denominator':oracle.denominator})
    def test_schema_order_units_rows_range_and_truncation(self):
        for raw in [b'',RAW[:-1],RAW.replace(b'milli_c',b'celsius'),RAW.replace(b'2,25002',b'1,25002'),
                    RAW.replace(b'25000',b'025000'),RAW.replace(b'25000',b'25000.0'),
                    RAW.replace(b'25000',b'150001'),RAW.replace(b'25000',b'-0'),
                    RAW+b'\n',b'x'*(MAX_BYTES+1),b'seq,value_milli_c\n1,0\n']:
            with self.assertRaises(ValueError):parse_samples(raw)
        for kwargs in [{'offset_milli_c':True},{'calibration_u_milli_c':-1},{'offset_milli_c':10001}]:
            with self.assertRaises(ValueError):summarize(RAW,**kwargs)

if __name__=='__main__':unittest.main(verbosity=2)
