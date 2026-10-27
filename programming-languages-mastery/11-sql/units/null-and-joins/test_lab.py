from contextlib import closing
import unittest
from lab import QUERIES,database,observe,truth_rows

# Independent three-valued truth functions, no SQL or SQLite call.
def tri_and(a,b):
    if a==0 or b==0:return 0
    if a is None or b is None:return None
    return 1

def tri_or(a,b):
    if a==1 or b==1:return 1
    if a is None or b is None:return None
    return 0

class NullTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=observe()
    def test_all_nine_truth_combinations(self):
        for row in self.data['truth']:
            a,b=row['a'],row['b']
            self.assertEqual(row['and'],tri_and(a,b));self.assertEqual(row['or'],tri_or(a,b))
            self.assertEqual(row['not_a'],None if a is None else 1-a)
    def test_comparison_null_and_presence(self):
        rows=self.data['observations'];self.assertEqual(rows['equals_null'],[]);self.assertEqual(rows['is_null'],[(11,)])
    def test_antijoin_does_not_confuse_unknown_with_nonmember(self):
        rows=self.data['observations'];self.assertEqual(rows['not_in'],[]);self.assertEqual(rows['not_exists'],[(1,),(3,)])
        self.assertEqual(rows['empty_not_in'],[(1,)])
    def test_left_join_filter_location(self):
        rows=self.data['observations'];self.assertEqual(rows['left_filter_on'],[(1,10,5),(2,None,None),(3,None,None)])
        self.assertEqual(rows['left_filter_where'],[(1,10,5)])
    def test_aggregate_counts_rows_and_nonnull_separately(self):
        self.assertEqual(self.data['observations']['counts'],[(1,2,2,1,5),(2,1,1,1,0),(3,1,0,0,None)])
        self.assertEqual(self.data['observations']['empty_aggregate'],[(0,0,None,0.0)])
    def test_unique_distinct_and_bound_data(self):
        rows=self.data['observations'];self.assertTrue(rows['duplicate_nonnull_rejected']);self.assertEqual(rows['distinct_nulls'],[(None,),(1,)])
        self.assertEqual(rows['bound_data'],[("x'); DROP TABLE customers;--",)]);self.assertEqual(rows['customers_after_bind'],3)
    def test_not_exists_matches_set_definition_with_nullable_blocked(self):
        import itertools
        with closing(database()) as db:
            for values in itertools.product((1,2,3,None),repeat=3):
                db.execute('DELETE FROM blocked');db.executemany('INSERT INTO blocked VALUES (?)',[(x,) for x in values])
                expected=[(x,) for x in (1,2,3) if x not in {v for v in values if v is not None}]
                self.assertEqual(db.execute(QUERIES['not_exists']).fetchall(),expected)

if __name__=='__main__':unittest.main()
