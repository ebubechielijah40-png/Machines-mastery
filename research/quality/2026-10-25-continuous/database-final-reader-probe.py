"""Independent reader probes, not author test fixtures or a durability proof."""
from collections import Counter
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]
UNIT=ROOT/'07-databases-data-systems/recovery-planning'
sys.path.insert(0,str(UNIT))
from store import Store,StoreError,ConflictError,wal_module
from planner import Plan,execute_join
from stream import consume,OFFSET_KEY,SOURCE_KEY,MAX_TOTAL


def file_state(directory):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path(directory).iterdir() if p.is_file()}


def main():
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'database';store=Store(path,create=True)
        store.commit([('put',1,'initial'),('put',2,'retained')]);store.checkpoint()
        store.commit([('delete',1),('put',1,'middle'),('delete',1),
                      ('put',-(1<<63),'low'),('put',(1<<63)-1,'high')])
        expected={2:'retained',-(1<<63):'low',(1<<63)-1:'high'}
        assert store.snapshot().rows==expected
        before=file_state(path)
        try:store.commit([('put',2,'stale')],expected_version=1)
        except ConflictError:pass
        else:raise AssertionError('stale plan accepted')
        assert file_state(path)==before
        orphan=path/('index-'+'f'*32+'.bpi');orphan.write_bytes(b'unselected evidence')
        assert store.snapshot().rows==expected
        published=store.checkpoint(collect=True)
        assert not orphan.exists() and Store(path).snapshot().rows==expected
        current=store.snapshot();wal=path/f'wal-{current.generation}.wal'
        module=wal_module();frame=bytearray(module.encode_transaction(1,[('put','2','damage')]))
        frame[-1]^=1;wal.write_bytes(module.FILE_MAGIC+frame)
        original=wal.read_bytes();corruption_refusals=0
        for operation in (store.snapshot,store.repair_tail):
            try:operation()
            except StoreError:corruption_refusals+=1
            else:raise AssertionError('complete bad frame treated as an incomplete tail')
        assert wal.read_bytes()==original
    # Deliberately duplicate complete output rows. Polynomial multiplicities
    # provide an oracle independent from a Cartesian executable join.
    join_cases=0
    for left_counts in itertools.product(range(3),repeat=3):
        for right_counts in itertools.product(range(3),repeat=3):
            keys=(-3,0,8)
            left=[(key,'L') for key,n in zip(keys,left_counts) for _ in range(n)]
            right=[(key,'R') for key,n in zip(keys,right_counts) for _ in range(n)]
            expected=Counter({(key,'L',key,'R'):a*b for key,a,b in zip(keys,left_counts,right_counts) if a*b})
            for plan in (Plan('nested',None,0,0,0),Plan('hash','left',0,0,6),Plan('hash','right',0,0,6)):
                actual=execute_join(left,right,plan)
                assert Counter(actual['rows'])==expected
                assert sum(expected.values())==len(actual['rows'])
                join_cases+=1
    with tempfile.TemporaryDirectory() as directory:
        store=Store(directory,create=True)
        events=[(1,MAX_TOTAL,MAX_TOTAL),(2,MAX_TOTAL,-MAX_TOTAL),(3,0,-7)]
        first=consume(store,'reader-partition',events);store.checkpoint(collect=True)
        replay=consume(Store(directory),'reader-partition',events)
        expected={SOURCE_KEY:'reader-partition',OFFSET_KEY:'3',MAX_TOTAL:'0',0:'-7'}
        assert store.snapshot().rows==expected and replay['applied_events']==0
        before=file_state(directory)
        try:consume(store,'reader-partition',[(5,0,1)])
        except ValueError:pass
        else:raise AssertionError('source gap accepted')
        assert file_state(directory)==before
    print(json.dumps(dict(environment=dict(python=sys.version,platform=platform.platform()),
                         source_sha256={n:hashlib.sha256((UNIT/n).read_bytes()).hexdigest() for n in ('store.py','planner.py','stream.py')},
                         repeated_put_delete_and_extreme_keys=True,stale_rejection_preserved_all_bytes=True,
                         ignored_unselected_orphan_collected=True,selected_complete_corruption_refusals=corruption_refusals,
                         corrupt_frame_preserved=True,duplicate_polynomial_join_cases=join_cases,
                         forced_join_algorithms=['nested','hash-left','hash-right'],
                         exact_zero_total_stream_retained=dict(first=first,replay=replay,rows=expected),
                         source_gap_preserved_all_bytes=True,
                         limitations='Finite separate-reader checks in a trusted local POSIX directory; no physical power-loss, event-time/window implementation, remote effects or learner mastery.'),indent=2))


if __name__=='__main__':main()
