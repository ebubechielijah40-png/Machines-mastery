from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from service import Ledger


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=str(Path(self.temp.name)/"data.db")
        self.ledger=Ledger(self.path,capacity=2,indexed=True)
    def tearDown(self):
        self.ledger.close();self.temp.cleanup()
    def test_idempotency_and_conflict(self):
        self.assertTrue(self.ledger.ingest(1,2,5))
        self.assertFalse(self.ledger.ingest(1,2,5))
        with self.assertRaises(ValueError): self.ledger.ingest(1,2,6)
        self.assertEqual(self.ledger.total(2),5)
    def test_rollback_and_recovery(self):
        self.ledger.ingest(1,0,3)
        with self.assertRaises(RuntimeError): self.ledger.ingest(2,0,7,fail=True)
        self.assertEqual(self.ledger.total(0),3)
        self.assertTrue(self.ledger.ingest(2,0,7))
        self.assertEqual(self.ledger.total(0),10)
    def test_cache_invalidation_and_capacity(self):
        self.assertEqual(self.ledger.total(0),0)
        self.ledger.ingest(1,0,5)
        self.assertEqual(self.ledger.total(0),5)
        for i in range(10): self.ledger.total(i)
        self.assertLessEqual(len(self.ledger.cache),2)
    def test_two_instances_expose_stale_cache(self):
        self.assertEqual(self.ledger.total(0),0)
        other=Ledger(self.path)
        try: other.ingest(1,0,8)
        finally: other.close()
        self.assertEqual(self.ledger.total(0),0)  # documented single-writer violation
        self.ledger.cache.clear()
        self.assertEqual(self.ledger.total(0),8)
    def test_lock_failure_is_bounded(self):
        other=sqlite3.connect(self.path)
        try:
            other.execute("BEGIN IMMEDIATE")
            with self.assertRaises(sqlite3.OperationalError): self.ledger.ingest(1,0,5)
            other.rollback()
            self.assertTrue(self.ledger.ingest(1,0,5))
        finally: other.close()
    def test_untrusted_values_rejected(self):
        for args in [(True,0,1),(-1,0,1),(1,1000,1),(1,0,"1; DROP TABLE events")]:
            with self.assertRaises(ValueError): self.ledger.ingest(*args)
    def test_restart_persistence_and_order(self):
        for event_id in [3,1,2]: self.ledger.ingest(event_id,0,event_id)
        second=Ledger(self.path)
        try: self.assertEqual(second.total(0),6)
        finally: second.close()


if __name__ == "__main__": unittest.main()
