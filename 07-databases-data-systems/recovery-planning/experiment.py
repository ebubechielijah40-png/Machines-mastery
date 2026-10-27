"""Actual local publication/compaction/OCC/planning/stream observations."""
import hashlib
import json
from pathlib import Path
import platform
import signal
import subprocess
import sys
import tempfile
from store import Store,ConflictError,wal_module
from stream import consume,OFFSET_KEY,SOURCE_KEY
from planner import Plan,choose_plan,execute_join,exact_cardinality

HERE=Path(__file__).resolve().parent
PHASES=('after-index-sync','after-wal-sync','after-generation-directory-sync','after-manifest-temp-sync',
        'after-manifest-replace','after-manifest-directory-sync','after-old-unlink','after-collection-directory-sync')


def run():
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);store=Store(root/'publication',create=True)
        store.commit([('put',1,'base'),('put',2,'keep')]);store.checkpoint()
        store.commit([('delete',1),('put',3,'new')]);expected=store.snapshot();crashes=[]
        for phase in PHASES:
            before=store.snapshot()
            result=subprocess.run([sys.executable,str(HERE/'crash_worker.py'),str(store.directory),'checkpoint',phase],capture_output=True,timeout=15)
            after=Store(store.directory).snapshot()
            assert result.returncode==-signal.SIGKILL
            assert (after.rows,after.version)==(expected.rows,expected.version)
            old=after.generation==before.generation
            assert old==(phase in PHASES[:4])
            crashes.append(dict(phase=phase,exit_code=result.returncode,selected_old_generation=old,rows_match=True,version=after.version))
        compact=Store(root/'compact',create=True)
        for i in range(120):compact.commit([('put',i%40,str(i)),('put',(i+1)%40,str(i+1))])
        before=compact.snapshot();checkpoint=compact.checkpoint(collect=True);after=compact.snapshot()
        assert before.rows==after.rows and before.version==after.version==120
        compaction=dict(live_rows=len(after.rows),global_version=after.version,before_wal_bytes=before.suffix_bytes,
                        after_wal_bytes=after.suffix_bytes,after_suffix_transactions=after.suffix_transactions,
                        files_removed=checkpoint['removed_files'],selected_file_bytes=sum(p.stat().st_size for p in compact.directory.iterdir()))
        lost=Store(root/'lost',create=True);lost.commit([('put',0,'1')])
        a=lost.snapshot();b=lost.snapshot();lost.commit([('put',0,str(int(a.rows[0])+1))]);lost.commit([('put',0,str(int(b.rows[0])+1))])
        unsafe_result=int(lost.snapshot().rows[0]);assert unsafe_result==2
        guarded=Store(root/'guarded',create=True);guarded.commit([('put',0,'1')]);a=guarded.snapshot();b=guarded.snapshot()
        guarded.commit([('put',0,str(int(a.rows[0])+1))],expected_version=a.version)
        try:guarded.commit([('put',0,str(int(b.rows[0])+1))],expected_version=b.version)
        except ConflictError:stale_rejected=True
        else:raise AssertionError('stale update accepted')
        fresh=guarded.snapshot();guarded.commit([('put',0,str(int(fresh.rows[0])+1))],expected_version=fresh.version)
        assert guarded.snapshot().rows[0]=='3'
        left=[(0,'hot')]*90+[(i,str(i)) for i in range(1,11)];right=left[:]
        plan=choose_plan(100,100,left_distinct=11,right_distinct=11,memory_rows=100)
        joined=execute_join(left,right,plan);actual=exact_cardinality(left,right)
        assert len(joined['rows'])==actual==8110
        stale_plan=choose_plan(20,30,left_distinct=10,right_distinct=10,memory_rows=20)
        try:execute_join(left,right,stale_plan)
        except ValueError:grant_refused=True
        else:raise AssertionError('stale estimate bypassed row grant')
        stream=Store(root/'stream',create=True);events=[(1,0,4),(2,1,7),(3,0,-1)]
        consume(stream,'source-A',events);stream.checkpoint(collect=True)
        retry=consume(stream,'source-A',events)
        changed_past=consume(stream,'source-A',[(1,0,999),(2,1,999),(3,0,999)])
        assert retry['applied_events']==changed_past['applied_events']==0
        assert stream.snapshot().rows[0]=='3' and stream.snapshot().rows[1]=='7'
        # Byte-cut model is separate from the process-kill observation.
        cutstore=Store(root/'cuts',create=True);cutstore.commit([('put',1,'old')]);cutstore.checkpoint(collect=True)
        snapshot=cutstore.snapshot();walpath=cutstore.directory/f'wal-{snapshot.generation}.wal'
        frame=wal_module().encode_transaction(1,[('put','1','new'),('put','2','new')])
        cuts=0
        for cut in range(len(frame)+1):
            walpath.write_bytes(wal_module().FILE_MAGIC+frame[:cut]);rows=cutstore.snapshot().rows
            assert rows==({1:'new',2:'new'} if cut==len(frame) else {1:'old'});cuts+=1
        return dict(environment=dict(python=sys.version,platform=platform.platform()),
                    source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('store.py','planner.py','stream.py','crash_worker.py','experiment.py')},
                    process_crashes=crashes,compaction=compaction,
                    lost_update=dict(no_precondition_result=unsafe_result,intended_two_increment_result=3,stale_version_rejected=stale_rejected,recomputed_result=3),
                    skew=dict(plan=vars(plan),actual_join_rows=actual,actual_work=joined['actual_work'],stale_row_grant_refused=grant_refused),
                    stream=dict(exact_retry_applied=retry['applied_events'],mutated_past_also_skipped=changed_past['applied_events'],source_immutability_is_assumed=True),
                    byte_cut_model=dict(cases=cuts,complete_frame_bytes=len(frame),all_or_none=True),
                    limitations='Synthetic local trusted clients, POSIX cooperative locks, process kills and explicit byte cuts only; no physical power loss, NFS, hostile directory, distributed consensus, external exactly-once effects or learner mastery.')


if __name__=='__main__':print(json.dumps(run(),indent=2))
