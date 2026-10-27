import hashlib,hmac,json,random,tempfile,unittest
from pathlib import Path
from unittest import mock
from pipeline import (Pipeline, IntegrityError, AuthorizationError, SequenceError,
                      canonical,sign_observation,manual_hmac_sha256)

KEYS={'s1':b'a'*32,'s2':b'b'*32}; PROCESSOR=b'p'*32
POLICY={'s1':{'room'},'s2':{'outside'}}

class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'ledger.jsonl'
    def pipeline(self,**kw):return Pipeline(self.path,KEYS,PROCESSOR,POLICY,**kw)
    def test_hmac_known_vector_and_independent_library(self):
        expected='b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'
        self.assertEqual(manual_hmac_sha256(bytes.fromhex('0b'*20),b'Hi There').hex(),expected)
        rng=random.Random(5)
        for length in [0,1,32,64,65,150]:
            key=bytes(rng.randrange(256) for _ in range(length));message=b'observation'
            self.assertEqual(manual_hmac_sha256(key,message),hmac.new(key,message,hashlib.sha256).digest())
    def test_ingest_reload_exact_transform_and_read_authz(self):
        with self.pipeline() as p:
            tip=p.ingest(sign_observation(KEYS['s1'],'s1','room',1,25001))
            self.assertEqual(p.snapshot('analyst')['s1/room'],{'numerator':25001,'denominator':1000,'unit':'celsius'})
            with self.assertRaises(AuthorizationError):p.snapshot('stranger')
        with self.pipeline(expected_tip=tip) as p:
            self.assertEqual(p.count,1);self.assertEqual(p.last,{'s1':1})
            p.ingest(sign_observation(KEYS['s1'],'s1','room',2,26000))
    def test_mutation_substitution_replay_and_role_fail_without_state_change(self):
        with self.pipeline() as p:
            raw=sign_observation(KEYS['s1'],'s1','room',1,25000)
            envelope=json.loads(raw);envelope['record']['value_milli_c']=30000
            with self.assertRaises(IntegrityError):p.ingest(canonical(envelope))
            with self.assertRaises(AuthorizationError):p.ingest(sign_observation(KEYS['s1'],'s1','outside',1,25000))
            with self.assertRaises(SequenceError):p.ingest(sign_observation(KEYS['s1'],'s1','room',2,25000))
            self.assertEqual(p.count,0)
            p.ingest(raw)
            with self.assertRaises(SequenceError):p.ingest(raw)
            self.assertEqual(p.count,1)
    def test_duplicate_fields_invalid_types_and_bounded_payloads(self):
        with self.pipeline() as p:
            for raw in [b'{"tag":"a","tag":"b"}',b'{'*1200,b'x'*8193,b'not json']:
                with self.assertRaises(IntegrityError):p.ingest(raw)
            for seq,value in [(True,1),(1,True),(0,1),(1,150001)]:
                with self.assertRaises(IntegrityError):sign_observation(KEYS['s1'],'s1','room',seq,value)
    def test_processor_output_chain_and_whole_prefix_substitution(self):
        with self.pipeline() as p:
            p.ingest(sign_observation(KEYS['s1'],'s1','room',1,20000))
            tip=p.ingest(sign_observation(KEYS['s1'],'s1','room',2,21000))
        original=self.path.read_bytes();lines=original.splitlines(keepends=True)
        obj=json.loads(lines[0]);obj['core']['output']['numerator']=999
        self.path.write_bytes(canonical(obj)+b'\n'+lines[1])
        with self.assertRaises(IntegrityError):self.pipeline()
        self.path.write_bytes(lines[1]+lines[0])
        with self.assertRaises(IntegrityError):self.pipeline()
        self.path.write_bytes(lines[0])
        with self.pipeline() as p:self.assertEqual(p.count,1)  # prefix truncation without trusted tip undetected
        with self.assertRaises(IntegrityError):self.pipeline(expected_tip=tip)
    def test_every_truncated_last_line_fails_closed(self):
        with self.pipeline() as p:p.ingest(sign_observation(KEYS['s1'],'s1','room',1,20000))
        original=self.path.read_bytes()
        for cut in range(1,len(original)):
            self.path.write_bytes(original[:cut])
            with self.assertRaises(IntegrityError):self.pipeline()
    def test_unknown_sync_outcome_poisoned_then_recovered(self):
        p=self.pipeline()
        try:
            raw=sign_observation(KEYS['s1'],'s1','room',1,25000)
            with mock.patch('pipeline.os.fsync',side_effect=OSError('injected sync failure')):
                with self.assertRaises(OSError):p.ingest(raw)
            self.assertTrue(p.poisoned);self.assertEqual(p.count,0)
            with self.assertRaises(RuntimeError):p.ingest(raw)
        finally:p.close()
        with self.pipeline() as p:
            self.assertEqual(p.count,1)  # completed bytes visible despite failed sync acknowledgement
            with self.assertRaises(SequenceError):p.ingest(raw)
    def test_authenticated_false_measurement_is_still_accepted(self):
        with self.pipeline() as p:
            p.ingest(sign_observation(KEYS['s1'],'s1','room',1,120000))
            self.assertEqual(p.snapshot('analyst')['s1/room']['numerator'],120000)
            # No real instrument truth is checked; a producer can lie within schema.
    def test_entry_budget_and_snapshot_copy(self):
        with self.pipeline(max_entries=1) as p:
            raw=sign_observation(KEYS['s1'],'s1','room',1,25000);p.ingest(raw)
            snapshot=p.snapshot('analyst');snapshot['s1/room']['numerator']=0
            self.assertEqual(p.snapshot('analyst')['s1/room']['numerator'],25000)
            with self.assertRaises(IntegrityError):p.ingest(sign_observation(KEYS['s1'],'s1','room',2,26000))

if __name__=='__main__':unittest.main(verbosity=2)
