"""Actual controlled recovery evidence and checksum-authority counterexample."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
from fractions import Fraction
from operations import OperationStore,Observation
from recovery import canonical,checked_state,create_backup,verify_backup,restore_backup,digest_file
from telemetry import aggregate,merge,quantile_upper_bound,burn_alert


def run():
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);path=root/'live.db';store=OperationStore(path)
        store.apply('A',5);store.apply('B',7)
        anchor=sqlite3.connect(path,isolation_level=None)
        try:
            anchor.execute('PRAGMA wal_checkpoint(TRUNCATE)');anchor.execute('PRAGMA wal_autocheckpoint=0')
            anchor.execute('BEGIN IMMEDIATE');anchor.execute('UPDATE counter SET value=16 WHERE id=1')
            anchor.execute("INSERT INTO operations VALUES('D',4,16)");anchor.commit()
            shutil.copyfile(path,root/'naive.db')
            naive=checked_state(root/'naive.db')['counter']
            create_backup(path,root/'consistent')
            consistent=verify_backup(root/'consistent')[1]['counter']
            assert (naive,consistent)==(12,16)
        finally:anchor.close()
        store.apply('C',-3)
        try:restore_backup(root/'consistent',root/'refused.db',known_receipts=[('C',-3,13)])
        except ValueError:stale_refused=True
        else:raise AssertionError('missing newer receipt not detected')
        # An attacker who can rewrite every unkeyed check can create a consistent
        # but false snapshot. This is our own disposable test database.
        shutil.copytree(root/'consistent',root/'rewritten')
        dbpath=root/'rewritten/snapshot.db'
        with sqlite3.connect(dbpath) as db:
            db.execute("UPDATE operations SET delta=8,result=20 WHERE request_id='D'")
            db.execute('UPDATE counter SET value=20')
        altered_state=checked_state(dbpath)
        manifest_path=root/'rewritten/MANIFEST.json';manifest=json.loads(manifest_path.read_text())
        manifest.update(database_sha256=digest_file(dbpath),state_sha256=hashlib.sha256(canonical(altered_state)).hexdigest(),counter=20,database_bytes=dbpath.stat().st_size)
        manifest_path.write_bytes(canonical(manifest)+b'\n')
        rewritten_accepted=verify_backup(root/'rewritten')[1]['counter']==20
        try:restore_backup(root/'rewritten',root/'also-refused.db',known_receipts=[('D',4,16)])
        except ValueError:external_conflict=True
        else:raise AssertionError('external receipt mismatch not detected')
        def row(i,latency,status='ok'):return Observation(str(i),0,0,0,latency,status,None)
        a=aggregate([row(i,1) for i in range(99)],100,(1,100))
        b=aggregate([row(99,100)],100,(1,100));pooled=merge([a,b])
        short=aggregate([row(i,1,'ok' if i<9 else 'overload') for i in range(10)],5)
        long=aggregate([row(i,1,'ok' if i<27 else 'overload') for i in range(30)],5)
        return dict(environment=dict(python=sys.version,sqlite=sqlite3.sqlite_version),
                    source_sha256={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('operations.py','recovery.py','telemetry.py','recovery_experiment.py')},
                    wal_only_commit=dict(naive_main_copy_counter=naive,consistent_backup_counter=consistent),
                    stale_snapshot_refused=stale_refused,
                    unkeyed_authority_counterexample=dict(fully_rewritten_snapshot_passed_consistency=rewritten_accepted,external_receipt_blocked_promotion=external_conflict),
                    histogram=dict(pooled_p95_upper=quantile_upper_bound(pooled,Fraction(95,100)),incorrect_mean_of_shard_p95=50.5,pooled=pooled),
                    alert=burn_alert(short,long),
                    limitations='Synthetic local data and clocks. No physical fault, authenticated remote authority, service-scale reliability or statistical calibration of the alert.')


if __name__=='__main__':print(json.dumps(run(),indent=2))
