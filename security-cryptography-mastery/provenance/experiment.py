"""Connect original local framing and authenticated transformation mechanisms."""
from pathlib import Path
import json,platform,sys,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'06-networking/code'))
from framing import Decoder,encode
from pipeline import (Pipeline,IntegrityError,AuthorizationError,SequenceError,canonical,sign_observation)


def main():
    keys={'sensor':b's'*32};processor=b'p'*32;policy={'sensor':{'room'}}
    with tempfile.TemporaryDirectory() as temporary:
        path=Path(temporary)/'ledger.jsonl';request=sign_observation(keys['sensor'],'sensor','room',1,25001)
        wire=encode(request);d=Decoder(8192);frames=[]
        for offset in range(0,len(wire),3):frames.extend(d.feed(wire[offset:offset+3]))
        d.finish()
        with Pipeline(path,keys,processor,policy) as p:
            tip=p.ingest(frames[0]);snapshot=p.snapshot('analyst')
            outcomes={}
            for name,raw in [('replay',request),('unauthorized_stream',sign_observation(keys['sensor'],'sensor','outside',2,25001))]:
                try:p.ingest(raw);outcomes[name]='unexpected acceptance'
                except (IntegrityError,AuthorizationError,SequenceError) as exc:outcomes[name]=type(exc).__name__
            altered=json.loads(request);altered['record']['value_milli_c']=99000
            try:p.ingest(canonical(altered));outcomes['tamper']='unexpected acceptance'
            except IntegrityError as exc:outcomes['tamper']=type(exc).__name__
            p.ingest(sign_observation(keys['sensor'],'sensor','room',2,120000))
            outcomes['authenticated_false_measurement']='accepted within schema; truth not verified'
            latest_tip=p.tip
        full=path.read_bytes();first=full.splitlines(keepends=True)[0];path.write_bytes(first)
        with Pipeline(path,keys,processor,policy) as p:prefix_count=p.count
        try:
            with Pipeline(path,keys,processor,policy,expected_tip=latest_tip):pass
            checkpoint_result='unexpected acceptance'
        except IntegrityError:checkpoint_result='trusted-tip mismatch rejected'
        print(json.dumps({'kind':'synthetic local authenticated provenance experiment',
          'environment':{'python':sys.version,'platform':platform.platform()},'demo_keys_public':True,
          'framed_request_bytes':len(wire),'decoder_peak_pending':d.peak_pending,
          'accepted_tip_after_first':tip,'exact_first_output':snapshot,'failure_probes':outcomes,
          'complete_suffix_deletion_without_checkpoint_accepted_prefix_entries':prefix_count,
          'with_trusted_tip':checkpoint_result,'source_truth_verified':False},indent=2))

if __name__=='__main__':main()
