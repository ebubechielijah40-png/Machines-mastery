"""Controlled synthetic concurrency/crash/rollback and nonce-boundary evidence."""
import hashlib
import json
from pathlib import Path
import platform
import signal
import sqlite3
import subprocess
import sys
import tempfile
import cryptography
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pipeline import IntegrityError
from protected_demo import resources,observation,configuration
from protected_ledger import Witness,ProtectedLedger,RollbackDetected

HERE=Path(__file__).resolve().parent


def backup_file(source,destination):
    with sqlite3.connect(source) as src,sqlite3.connect(destination) as dst:src.backup(dst)


def run():
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);rotate=root/'rotate';rotate.mkdir();config,witness,ledger=resources(rotate)
        for seq in range(1,5):ledger.append(observation(seq,25000+seq))
        snapshot=ledger.snapshot();assert snapshot['count']==4
        with sqlite3.connect(rotate/'ledger.db') as db:
            frames=[json.loads(raw) for raw, in db.execute('SELECT raw FROM entries ORDER BY n')]
        history=dict(count=4,writer_key_ids=[f['header']['writer_key'] for f in frames],
                     encryption_key_ids=[f['header']['encryption_key'] for f in frames],
                     final_values=snapshot['values'])
        concurrent=root/'concurrent';concurrent.mkdir();resources(concurrent)
        children=[subprocess.Popen([sys.executable,str(HERE/'protected_worker.py'),str(concurrent),'append',producer],stdout=subprocess.PIPE,stderr=subprocess.PIPE) for producer in ('alpha','beta')]
        statuses=[]
        for child in children:
            _,error=child.communicate(timeout=20);statuses.append(child.returncode);assert child.returncode==0,error
        _,_,joined=resources(concurrent);joined_state=joined.snapshot()
        assert joined_state['count']==12 and len({e['nonce'] for e in joined_state['entries']})==12
        kills=[]
        for stage in ('after_nonce','before_commit','after_commit','after_witness'):
            case=root/stage;case.mkdir();resources(case)
            child=subprocess.run([sys.executable,str(HERE/'protected_worker.py'),str(case),'kill',stage],capture_output=True,timeout=10)
            assert child.returncode==-signal.SIGKILL,child.stderr
            _,_,reopened=resources(case);retry=reopened.append(observation(1));state=reopened.snapshot()
            kills.append(dict(stage=stage,exit_code=child.returncode,retry_was_replay=retry['replay'],recovered_count=state['count'],retained_nonce=state['entries'][0]['nonce']))
            assert state['count']==1
        # Current external authority rejects an old ledger prefix.
        rollback=root/'rollback';rollback.mkdir();c,w,l=resources(rollback);l.append(observation(1))
        old=l.backup(rollback/'old-ledger.db');backup_file(w.path,rollback/'old-authority.db')
        l.append(observation(2))
        try:ProtectedLedger(old,'observations',c,w,w.public_key)
        except RollbackDetected:old_local_rejected=True
        else:raise AssertionError('old local prefix accepted against current authority')
        # Deliberately violate authority independence: rolling back BOTH stores
        # leaves no retained external fact against which to detect the rollback.
        old_witness=Witness(rollback/'old-authority.db','observations',c.fingerprint(),b'w'*32)
        rolled=ProtectedLedger(old,'observations',c,old_witness,old_witness.public_key)
        whole_pair_count=rolled.snapshot()['count'];assert whole_pair_count==1
        # Independent, elementary XOR evidence: different AAD does not change
        # the reused counter-mode keystream under the same key and nonce.
        key=b'k'*32;nonce=b'n'*12;first=b'A'*32;second=b'B'*32
        ca=AESGCM(key).encrypt(nonce,first,b'ledger-A');cb=AESGCM(key).encrypt(nonce,second,b'ledger-B')
        xor=lambda a,b:bytes(x^y for x,y in zip(a,b))
        leaked=xor(ca[:-16],cb[:-16])==xor(first,second);assert leaked
        return dict(environment=dict(python=sys.version,cryptography=cryptography.__version__,sqlite=sqlite3.sqlite_version,platform=platform.platform()),
                    source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('pipeline.py','protected_ledger.py','gcm_mechanics.py','protected_demo.py','protected_worker.py','protected_experiment.py')},
                    rotations=history,concurrent=dict(child_exit_codes=statuses,entries=joined_state['count'],unique_nonces=len({e['nonce'] for e in joined_state['entries']})),
                    process_kills=kills,rollback=dict(old_ledger_current_authority_rejected=old_local_rejected,both_stores_rolled_back_undetected_count=whole_pair_count),
                    same_key_nonce_different_aad_exposes_plaintext_xor=leaked,
                    limitations='Public demo keys, synthetic data, authorized same-host processes. Witness rollback resistance and key exclusivity are assumptions. No physical power-loss, remote PKI or production security evidence.')


if __name__=='__main__':print(json.dumps(run(),indent=2))
