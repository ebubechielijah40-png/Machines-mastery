import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import sys
import tempfile
import unittest
from store import Store,StoreError,ConflictError,BusyError,wal_module,canonical
from stream import consume,OFFSET_KEY,SOURCE_KEY
from planner import Plan,choose_plan,execute_join,exact_cardinality

HERE=Path(__file__).resolve().parent


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.path=Path(self.temp.name)/'db';self.store=Store(self.path,create=True)
    def tearDown(self):self.temp.cleanup()

    def test_dictionary_history_and_deletion_across_checkpoints(self):
        rng=random.Random(20261025);expected={}
        for version in range(1,81):
            batch=[]
            for _ in range(rng.randrange(1,5)):
                key=rng.randrange(-20,21)
                if rng.randrange(3):
                    value=str(rng.randrange(1000));expected[key]=value;batch.append(('put',key,value))
                else:expected.pop(key,None);batch.append(('delete',key))
            self.assertEqual(self.store.commit(batch),version)
            if version%7==0:self.store.checkpoint(collect=bool(version%2))
            current=Store(self.path).snapshot();self.assertEqual((current.rows,current.version),(expected,version))
        self.store.checkpoint(collect=True)
        self.assertEqual(self.store.snapshot().suffix_transactions,0)
        self.assertEqual(len(list(self.path.glob('index-*.bpi'))),1)
        self.assertEqual(len(list(self.path.glob('wal-*.wal'))),1)

    def test_suffix_tombstone_is_not_lost(self):
        self.store.commit([('put',1,'base'),('put',2,'kept')]);self.store.checkpoint()
        self.store.commit([('delete',1),('put',3,'new')])
        self.assertEqual(self.store.snapshot().rows,{2:'kept',3:'new'})

    def test_stale_optimistic_transaction_is_rejected(self):
        self.store.commit([('put',1,'10')]);before=self.store.snapshot()
        self.store.commit([('put',1,'11')],expected_version=before.version)
        with self.assertRaises(ConflictError):self.store.commit([('put',1,'11')],expected_version=before.version)
        now=self.store.snapshot();self.store.commit([('put',1,str(int(now.rows[1])+1))],expected_version=now.version)
        self.assertEqual(self.store.snapshot().rows[1],'12')

    def test_all_publication_process_crash_boundaries(self):
        self.store.commit([('put',i,str(i)) for i in range(12)]);expected=self.store.snapshot()
        phases=['after-index-sync','after-wal-sync','after-generation-directory-sync','after-manifest-temp-sync','after-manifest-replace','after-manifest-directory-sync','after-old-unlink','after-collection-directory-sync']
        for phase in phases:
            with self.subTest(phase=phase):
                old=self.store.snapshot().generation
                child=subprocess.run([sys.executable,str(HERE/'crash_worker.py'),str(self.path),'checkpoint',phase],capture_output=True,timeout=15)
                self.assertEqual(child.returncode,-signal.SIGKILL,child.stderr)
                recovered=Store(self.path).snapshot()
                self.assertEqual((recovered.rows,recovered.version),(expected.rows,expected.version))
                self.assertEqual(recovered.generation==old,phase in phases[:4])
                with self.store.lock(exclusive=True,blocking=False):pass

    def test_actual_append_kill_is_not_physical_power_loss(self):
        self.store.commit([('put',1,'old'),('put',2,'old')])
        for phase in ['after-append','after-commit-sync']:
            child=subprocess.run([sys.executable,str(HERE/'crash_worker.py'),str(self.path),'commit',phase],capture_output=True,timeout=15)
            self.assertEqual(child.returncode,-signal.SIGKILL)
            self.assertEqual(self.store.snapshot().rows,{1:'new',2:'new'})

    def test_every_cut_of_next_frame_requires_explicit_tail_repair(self):
        self.store.commit([('put',1,'base')]);self.store.checkpoint(collect=True)
        before=self.store.snapshot();path=self.path/f'wal-{before.generation}.wal'
        frame=wal_module().encode_transaction(1,[('put','1','next'),('put','2','next')])
        for cut in range(len(frame)+1):
            path.write_bytes(wal_module().FILE_MAGIC+frame[:cut]);recovered=self.store.snapshot()
            self.assertEqual(recovered.rows,{1:'next',2:'next'} if cut==len(frame) else {1:'base'})
            if 0<cut<len(frame):
                with self.assertRaises(StoreError):self.store.commit([('put',3,'x')])
                self.assertEqual(self.store.repair_tail(),cut)
                self.assertEqual(self.store.snapshot().trailing_bytes,0)

    def test_selected_corruption_must_not_guess_an_old_generation(self):
        self.store.commit([('put',1,'old')]);self.store.checkpoint()
        self.store.commit([('put',1,'new')]);self.store.checkpoint()
        selected=self.store.snapshot();path=self.path/f'index-{selected.generation}.bpi'
        raw=bytearray(path.read_bytes());raw[-1]^=1;path.write_bytes(raw)
        with self.assertRaisesRegex(StoreError,'digest'):self.store.snapshot()
        self.assertGreater(len(list(self.path.glob('index-*.bpi'))),1)

    def test_manifest_path_digest_and_canonical_schema(self):
        path=self.path/'CURRENT';original=path.read_bytes();obj=json.loads(original)
        obj['body']['generation']='../outside';obj['sha256']=hashlib.sha256(canonical(obj['body'])).hexdigest();path.write_bytes(canonical(obj))
        with self.assertRaises(StoreError):self.store.snapshot()
        path.write_bytes(original+b' ')
        with self.assertRaises(StoreError):self.store.snapshot()
        path.write_bytes(original[:-1])
        with self.assertRaises(StoreError):self.store.snapshot()

    def test_bad_operations_do_not_mutate_authority(self):
        before={p.name:p.read_bytes() for p in self.path.iterdir()}
        for ops in [[],[('put',True,'x')],[('put',1,'é'*13)],[('put',1,'\ud800')],[('delete',2**64)],[('put',1,3)],[('erase',1)]]:
            with self.subTest(ops=repr(ops)),self.assertRaises(ValueError):self.store.commit(ops)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.path.iterdir()})

    def test_shared_locks_and_nonblocking_exclusion_in_processes(self):
        script="from store import Store,BusyError;import sys;s=Store(sys.argv[1]);\ntry:\n with s.lock(exclusive=sys.argv[2]=='x',blocking=False):print('acquired')\nexcept BusyError:print('busy')"
        env=dict(os.environ,PYTHONPATH=str(HERE))
        def attempt(mode):return subprocess.check_output([sys.executable,'-c',script,str(self.path),mode],env=env,text=True,timeout=10).strip()
        with self.store.lock(exclusive=False):self.assertEqual((attempt('s'),attempt('x')),('acquired','busy'))
        with self.store.lock(exclusive=True):self.assertEqual(attempt('s'),'busy')

    def test_two_real_writers_keep_all_transactions(self):
        script="from store import Store;import sys;s=Store(sys.argv[1]);start=int(sys.argv[2]);\nfor i in range(20):s.commit([('put',start+i,str(i))])"
        env=dict(os.environ,PYTHONPATH=str(HERE))
        children=[subprocess.Popen([sys.executable,'-c',script,str(self.path),str(start)],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE) for start in (0,100)]
        for child in children:
            _,err=child.communicate(timeout=30);self.assertEqual(child.returncode,0,err)
        snapshot=self.store.snapshot();self.assertEqual(snapshot.version,40)
        self.assertEqual(snapshot.rows,{start+i:str(i) for start in (0,100) for i in range(20)})


class PipelineAndPlannerTests(unittest.TestCase):
    def test_stream_replay_checkpoint_source_gap_and_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            store=Store(directory,create=True);consume(store,'A',[(1,0,2),(2,1,3),(3,0,-1)]);store.checkpoint(collect=True)
            result=consume(Store(directory),'A',[(2,1,3),(3,0,-1),(4,1,2)])
            self.assertEqual(result['applied_events'],1)
            self.assertEqual(store.snapshot().rows,{OFFSET_KEY:'4',SOURCE_KEY:'A',0:'1',1:'5'})
            before=store.snapshot()
            for source,events in [('B',[(5,0,1)]),('A',[(6,0,1)]),('A',[(5,0,1),(7,0,1)])]:
                with self.assertRaises(ValueError):consume(store,source,events)
            self.assertEqual(store.snapshot(),before)

    def test_stream_unknown_reply_retry_not_double_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            store=Store(directory,create=True)
            child=subprocess.run([sys.executable,str(HERE/'crash_worker.py'),directory,'consume','after-commit-sync'],capture_output=True,timeout=15)
            self.assertEqual(child.returncode,-signal.SIGKILL)
            result=consume(store,'source-A',[(1,0,4),(2,1,7),(3,0,-1)])
            self.assertEqual(result['applied_events'],0)
            self.assertEqual(store.snapshot().rows,{OFFSET_KEY:'3',SOURCE_KEY:'source-A',0:'3',1:'7'})

    def test_stream_history_against_batch_sums(self):
        rng=random.Random(257);events=[(i,rng.randrange(5),rng.randrange(-4,6)) for i in range(1,41)];expected={}
        for _,group,delta in events:expected[group]=expected.get(group,0)+delta
        with tempfile.TemporaryDirectory() as directory:
            store=Store(directory,create=True)
            for end in range(4,41,4):consume(store,'fixed',events[max(0,end-7):end]);store.checkpoint(collect=True)
            rows=store.snapshot().rows
            self.assertEqual({k:int(v) for k,v in rows.items() if k>=0},expected);self.assertEqual(rows[OFFSET_KEY],'40')

    def test_100_bag_joins_against_cartesian_oracle(self):
        rng=random.Random(81)
        for _ in range(100):
            left=[(rng.randrange(5),str(i)) for i in range(rng.randrange(12))];right=[(rng.randrange(5),str(i)) for i in range(rng.randrange(12))]
            expected=sorted(a+b for a in left for b in right if a[0]==b[0])
            plan=choose_plan(len(left),len(right),left_distinct=len({x[0] for x in left}),right_distinct=len({x[0] for x in right}),memory_rows=2000)
            self.assertEqual(sorted(execute_join(left,right,plan)['rows']),expected)
            self.assertEqual(exact_cardinality(left,right),len(expected))
            self.assertEqual(sorted(execute_join(left,right,Plan('nested',None,0,0,0))['rows']),expected)

    def test_grant_stale_statistics_and_output_bounds(self):
        self.assertEqual(choose_plan(20,30,left_distinct=10,right_distinct=10,memory_rows=19).algorithm,'nested')
        plan=choose_plan(20,30,left_distinct=10,right_distinct=10,memory_rows=20)
        self.assertEqual((plan.algorithm,plan.build_side),('hash','left'))
        with self.assertRaises(ValueError):execute_join([(1,'a')]*21,[(1,'b')]*30,plan)
        with self.assertRaises(ValueError):execute_join([(1,'a')]*400,[(1,'b')]*400,Plan('hash','left',1,1,400))
        for n in (-1,True,2001):
            with self.assertRaises(ValueError):choose_plan(n,1,left_distinct=1,right_distinct=1,memory_rows=10)

    def test_uniform_estimate_fails_on_skew(self):
        left=[(0,'hot')]*90+[(i,str(i)) for i in range(1,11)];right=left[:]
        plan=choose_plan(100,100,left_distinct=11,right_distinct=11,memory_rows=100)
        self.assertEqual(plan.estimated_matches,909);self.assertEqual(exact_cardinality(left,right),8110)
        self.assertEqual(len(execute_join(left,right,plan)['rows']),8110)


if __name__=='__main__':unittest.main()
