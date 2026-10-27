from collections import Counter
import itertools
import math
import random
import sqlite3
import unittest
from experiment import query_plans, snapshot_schedule
from relations import (distinct, grouped_numeric, hash_join, nested_join, project,
                       select, sql_and, sql_equal, sql_not, sql_or)


class RelationTests(unittest.TestCase):
    def test_three_valued_truth_against_real_sql(self):
        with sqlite3.connect(':memory:') as con:
            for a, b in itertools.product((True, False, None), repeat=2):
                row = con.execute('SELECT ? AND ?, ? OR ?', (a, b, a, b)).fetchone()
                self.assertEqual((sql_and(a, b), sql_or(a, b)), row)
            for value in (True, False, None):
                self.assertEqual(sql_not(value), con.execute('SELECT NOT ?', (value,)).fetchone()[0])
        self.assertIsNone(sql_equal(None, None))
        self.assertEqual(select([(1,), (None,), (2,)], lambda row: sql_equal(row[0], 1)), [(1,)])

    def test_projection_preserves_bag_until_distinct(self):
        rows = [('A', 1), ('A', 2), (None, 3), (None, 4)]
        self.assertEqual(project(rows, [0]), [('A',), ('A',), (None,), (None,)])
        self.assertEqual(distinct(project(rows, [0])), [('A',), (None,)])

    def test_join_multiplicity_and_null(self):
        left = [(1, 'a'), (1, 'b'), (None, 'unknown')]
        right = [(1, 2), (1, 3), (1, 4), (None, 9)]
        nested, hashed = nested_join(left, right), hash_join(left, right)
        self.assertEqual(len(hashed.rows), 6)
        self.assertEqual(Counter(nested.rows), Counter(hashed.rows))
        self.assertEqual(nested.comparisons, 12)
        self.assertEqual(hashed.comparisons, 6)
        self.assertFalse(hash_join([], right).rows)

    def test_random_join_differential_oracle_preserves_duplicates(self):
        rng = random.Random(42)
        with sqlite3.connect(':memory:') as con:
            con.execute('CREATE TABLE a(k INTEGER,v INTEGER)')
            con.execute('CREATE TABLE b(k INTEGER,v INTEGER)')
            for _ in range(30):
                left = [(rng.choice([None, 0, 1, 2]), rng.randrange(3)) for _ in range(rng.randrange(8))]
                right = [(rng.choice([None, 0, 1, 2]), rng.randrange(3)) for _ in range(rng.randrange(8))]
                con.execute('DELETE FROM a')
                con.execute('DELETE FROM b')
                con.executemany('INSERT INTO a VALUES(?,?)', left)
                con.executemany('INSERT INTO b VALUES(?,?)', right)
                expected = Counter(con.execute('SELECT a.k,a.v,b.k,b.v FROM a JOIN b ON a.k=b.k'))
                self.assertEqual(Counter(nested_join(left, right).rows), expected)
                self.assertEqual(Counter(hash_join(left, right).rows), expected)

    def test_group_counts_and_all_null_group_against_sql(self):
        rows = [('A', 2), ('A', None), ('A', 4), ('B', None), (None, 9)]
        with sqlite3.connect(':memory:') as con:
            con.execute('CREATE TABLE r(k TEXT,v REAL)')
            con.executemany('INSERT INTO r VALUES(?,?)', rows)
            expected = Counter(con.execute('SELECT k,COUNT(*),COUNT(v),SUM(v),AVG(v) FROM r GROUP BY k'))
            self.assertEqual(Counter(grouped_numeric(rows)), expected)
        self.assertEqual(grouped_numeric([]), [])

    def test_sql_outer_filter_and_not_in_counterexamples(self):
        with sqlite3.connect(':memory:') as con:
            con.executescript('CREATE TABLE d(id INTEGER);CREATE TABLE r(device INTEGER,v INTEGER);'
                              'INSERT INTO d VALUES(1),(2);INSERT INTO r VALUES(1,2);')
            on = list(con.execute('SELECT d.id,r.v FROM d LEFT JOIN r ON d.id=r.device AND r.v>1 ORDER BY d.id'))
            where = list(con.execute('SELECT d.id,r.v FROM d LEFT JOIN r ON d.id=r.device WHERE r.v>1 ORDER BY d.id'))
            self.assertEqual(on, [(1, 2), (2, None)])
            self.assertEqual(where, [(1, 2)])
            self.assertIsNone(con.execute('SELECT 5 NOT IN (1,NULL)').fetchone()[0])
            self.assertEqual(con.execute('SELECT NOT EXISTS(SELECT 1 WHERE 5=1 OR 5=NULL)').fetchone()[0], 1)

    def test_constraints_and_transaction_rollback(self):
        con = sqlite3.connect(':memory:', isolation_level=None)
        try:
            con.execute('PRAGMA foreign_keys=ON')
            con.executescript('CREATE TABLE d(id INTEGER PRIMARY KEY);'
                              'CREATE TABLE r(id INTEGER PRIMARY KEY,device INTEGER NOT NULL REFERENCES d(id),v INTEGER CHECK(v>=0));'
                              'INSERT INTO d VALUES(1);')
            for values in [(1, 2, 3), (1, None, 3), (1, 1, -1)]:
                with self.assertRaises(sqlite3.IntegrityError):
                    con.execute('INSERT INTO r VALUES(?,?,?)', values)
            # A SQL CHECK whose expression is NULL is not a NOT NULL constraint.
            con.execute('INSERT INTO r VALUES(1,1,NULL)')
            con.execute('BEGIN')
            con.execute('INSERT INTO r VALUES(2,1,5)')
            con.execute('ROLLBACK')
            self.assertEqual(list(con.execute('SELECT id FROM r')), [(1,)])
        finally:
            con.close()

    def test_real_wal_schedule_and_stale_application_update(self):
        result = snapshot_schedule()
        expected = [(1, 100), (2, 100)]
        self.assertEqual(result['initial_snapshot'], expected)
        self.assertEqual(result['during_uncommitted_transfer'], expected)
        self.assertEqual(result['same_snapshot_after_other_commit'], expected)
        self.assertEqual(result['new_read_after_rollback'], [(1, 90), (2, 110)])
        self.assertIsNotNone(result['stale_snapshot_upgrade'])
        self.assertIsNotNone(result['second_writer_attempt'])
        if result['stale_snapshot_upgrade']['code'] is not None:
            self.assertEqual(result['stale_snapshot_upgrade']['code'], 517)
        self.assertEqual(result['separate_statement_stale_read_result'], 80)
        self.assertEqual(result['atomic_relative_update_result'], 70)

    def test_index_preserves_ordered_result(self):
        result = query_plans()
        self.assertTrue(result['equal_ordered_results'])
        self.assertEqual(result['matching_rows'], 10)
        # Do not assert exact EXPLAIN text across SQLite releases.
        self.assertTrue(result['before'])
        self.assertTrue(result['after'])

    def test_narrow_interface_rejects_wrong_domains(self):
        for rows in [[(math.nan,)], [(True,)], [(1,), (1, 2)], [[1]]]:
            with self.assertRaises(ValueError): project(rows, [0])
        with self.assertRaises(ValueError): select([(1,)], lambda row: 1)
        with self.assertRaises(ValueError): project([(1,)], [1])
        with self.assertRaises(ValueError): grouped_numeric([('A', 'two')])
        with self.assertRaises(ValueError): sql_and(1, None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
