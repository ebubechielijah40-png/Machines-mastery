"""Separate-reader cases for recovery, pooled order statistics and alert policy.

This script is not imported by the implementation or its author's tests.
It records malformed-summary acceptance separately to preserve review findings.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]
UNIT=ROOT/'production-systems-engineering/labs/operation-workbench'
sys.path.insert(0,str(UNIT))
from operations import OperationStore,Observation
from recovery import create_backup,restore_backup,checked_state
from telemetry import aggregate,merge,quantile_upper_bound,burn_alert,validate


def observation(i,t,status='ok'):
    return Observation(str(i),0,0,0,t,status,None)


def accepted(value):
    try:validate(value)
    except ValueError:return False
    return True


def main():
    with tempfile.TemporaryDirectory() as directory:
        base=Path(directory);path=base/'live.db';store=OperationStore(path)
        replies=[store.apply(name,delta)[0] for name,delta in [('Q',-7),('R',11),('S',-4)]]
        assert replies==[-7,4,0]
        create_backup(path,base/'zero-total')
        # Actual abrupt process exit inside the after-commit hook, before reply.
        code="from operations import OperationStore;import os,sys;s=OperationStore(sys.argv[1]);s.apply('uncertain',6,hook=lambda phase:os._exit(17) if phase=='after_commit' else None)"
        child=subprocess.run([sys.executable,'-c',code,str(path)],cwd=UNIT,capture_output=True,timeout=5)
        assert child.returncode==17,child.stderr
        assert OperationStore(path).apply('uncertain',6)==(6,True)
        try:restore_backup(base/'zero-total',base/'rejected.db',known_receipts=[('uncertain',6,6)])
        except ValueError:stale_rejected=True
        else:raise AssertionError('known newer receipt lost')
        restored=restore_backup(base/'zero-total',base/'restored.db',known_receipts=[('Q',-7,-7),('R',11,4),('S',-4,0)])
        assert restored['counter']==0
        restored_store=OperationStore(base/'restored.db')
        assert restored_store.apply('R',11)==(4,True)
        # A zero total does not mean an empty history: all3 identities survive.
        assert len(checked_state(base/'restored.db')['operations'])==3
        recovery=dict(original_replies=replies,actual_abrupt_exit_code=child.returncode,
                      unknown_reply_retry=[6,True],stale_generation_rejected=stale_rejected,
                      restored=restored,zero_total_retained_operations=3)
    values=[2,5,6,10,11]
    rows=[observation(i,t) for i,t in enumerate(values)]
    shards=[aggregate(rows[:1],8,(5,10)),aggregate(rows[1:4],8,(5,10)),aggregate(rows[4:],8,(5,10))]
    pooled=merge(shards)
    assert pooled['le_counts']==[2,4] and pooled['overflow']==1 and pooled['latency_sum_ns']==34
    bounds=[]
    for q in (Fraction(1,5),Fraction(3,5),Fraction(1)):
        exact=sorted(values)[(q.numerator*len(values)+q.denominator-1)//q.denominator-1]
        bound=quantile_upper_bound(pooled,q)
        expected=next((b for b in (5,10) if exact<=b),None)
        assert bound==expected
        bounds.append(dict(q=str(q),independently_sorted_value=exact,reported_upper=bound))
    short=aggregate([observation(i,1,'ok' if i<8 else 'overload') for i in range(10)],5)
    long=aggregate([observation(i,1,'ok' if i<38 else 'overload') for i in range(40)],5)
    mixed=burn_alert(short,long)
    assert (mixed['short_burn_exact'],mixed['long_burn_exact'],mixed['alert'])==('4','1',False)
    sustained=aggregate([observation(i,1,'ok' if i<36 else 'overload') for i in range(40)],5)
    assert burn_alert(short,sustained)['alert']
    contradiction=aggregate([observation(i,1,'overload') for i in range(10)],5)
    contradiction['good']=10
    impossible_empty=aggregate([],5);impossible_empty['latency_sum_ns']=1
    oversized=None
    try:oversized=aggregate([],10**31)
    except ValueError:oversized_returned=False;oversized_valid=False
    else:oversized_returned=True;oversized_valid=accepted(oversized)
    print(json.dumps(dict(source_sha256={name:hashlib.sha256((UNIT/name).read_bytes()).hexdigest() for name in ('operations.py','recovery.py','telemetry.py','local_service.py','release_drill.py')},
                         runtime=dict(python=sys.version,sqlite=sqlite3.sqlite_version),
                         recovery=recovery,pooled_order_statistic_checks=bounds,
                         exact_alert_counterexample=mixed,
                         corruption_boundary=dict(impossible_good_status_accepted=accepted(contradiction),
                                                  empty_nonzero_sum_accepted=accepted(impossible_empty),
                                                  oversized_deadline_returned=oversized_returned,
                                                  oversized_deadline_output_validates=oversized_valid),
                         limits='Finite local reader probes only. No physical storage failure, remote operation, learner mastery or external expert certification.'),indent=2))


if __name__=='__main__':main()
