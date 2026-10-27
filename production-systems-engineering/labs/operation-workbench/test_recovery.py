import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from operations import OperationStore
from recovery import create_backup,restore_backup,verify_backup,checked_state,digest_file


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.path=self.root/'live.db';self.store=OperationStore(self.path)
        self.store.apply('A',5);self.store.apply('B',7)
    def tearDown(self):self.temp.cleanup()

    def test_consistent_backup_restore_and_original_response(self):
        create_backup(self.path,self.root/'g1')
        self.store.apply('C',-3)
        result=restore_backup(self.root/'g1',self.root/'restored.db',known_receipts=[('A',5,5),('B',7,12)])
        restored=OperationStore(self.root/'restored.db')
        self.assertEqual(restored.apply('A',5),(5,True))
        self.assertEqual(restored.snapshot()['counter'],12)
        self.assertEqual(result['matched_external_receipts'],2)

    def test_wal_only_commit_is_not_captured_by_naive_main_copy(self):
        anchor=sqlite3.connect(self.path,isolation_level=None)
        try:
            anchor.execute('PRAGMA wal_checkpoint(TRUNCATE)')
            anchor.execute('PRAGMA wal_autocheckpoint=0')
            anchor.execute('BEGIN IMMEDIATE')
            anchor.execute('UPDATE counter SET value=16 WHERE id=1')
            anchor.execute("INSERT INTO operations VALUES('D',4,16)");anchor.commit()
            shutil.copyfile(self.path,self.root/'naive.db')
            self.assertEqual(checked_state(self.root/'naive.db')['counter'],12)
            create_backup(self.path,self.root/'correct')
            self.assertEqual(verify_backup(self.root/'correct')[1]['counter'],16)
        finally:anchor.close()

    def test_newer_external_receipt_blocks_stale_restore(self):
        create_backup(self.path,self.root/'g1');self.store.apply('C',4)
        with self.assertRaisesRegex(ValueError,'external receipt'):
            restore_backup(self.root/'g1',self.root/'refused.db',known_receipts=[('C',4,16)])
        self.assertFalse((self.root/'refused.db').exists())

    def test_conflicting_original_response_blocks_promotion(self):
        create_backup(self.path,self.root/'g1')
        with self.assertRaises(ValueError):
            restore_backup(self.root/'g1',self.root/'refused.db',known_receipts=[('A',5,12)])

    def test_create_only_snapshot_and_restore_preserve_existing(self):
        create_backup(self.path,self.root/'g1');manifest=(self.root/'g1/MANIFEST.json').read_bytes()
        with self.assertRaises(FileExistsError):create_backup(self.path,self.root/'g1')
        self.assertEqual((self.root/'g1/MANIFEST.json').read_bytes(),manifest)
        with self.assertRaises(FileExistsError):restore_backup(self.root/'g1',self.path)
        sidecar=self.root/'target.db-wal';sidecar.write_bytes(b'evidence')
        with self.assertRaises(FileExistsError):restore_backup(self.root/'g1',self.root/'target.db')
        self.assertEqual(sidecar.read_bytes(),b'evidence')

    def test_byte_and_logical_damage_are_separate_checks(self):
        create_backup(self.path,self.root/'g1');dbpath=self.root/'g1/snapshot.db'
        original=dbpath.read_bytes();damaged=bytearray(original);damaged[-1]^=1;dbpath.write_bytes(damaged)
        with self.assertRaises(ValueError):verify_backup(self.root/'g1')
        dbpath.write_bytes(original)
        with sqlite3.connect(dbpath) as db:db.execute('UPDATE counter SET value=999')
        manifest=json.loads((self.root/'g1/MANIFEST.json').read_text());manifest['database_sha256']=digest_file(dbpath)
        (self.root/'g1/MANIFEST.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,'counter/delta'):verify_backup(self.root/'g1')

    def test_missing_manifest_and_input_contracts(self):
        (self.root/'incomplete').mkdir()
        with self.assertRaises(ValueError):verify_backup(self.root/'incomplete')
        for timeout in (0,True,float('nan'),31):
            with self.assertRaises(ValueError):create_backup(self.path,self.root/'bad',timeout_seconds=timeout)
        with self.assertRaises(FileNotFoundError):create_backup(self.root/'missing',self.root/'failed')
        self.assertFalse((self.root/'failed').exists())


if __name__=='__main__':unittest.main()
