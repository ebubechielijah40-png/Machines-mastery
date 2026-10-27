"""Separate-reader failure, epoch-interleaving and counter-boundary probes."""
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]
UNIT=ROOT/'security-cryptography-mastery/provenance'
sys.path.insert(0,str(UNIT))
from protected_ledger import (Configuration,WriterEpoch,EncryptionEpoch,Witness,
    ProtectedLedger,sign_versioned,verify_receipt,IntegrityError)


def main():
    config=Configuration((
        WriterEpoch('gamma','g-old',b'G'*32,1,3,frozenset({'tank'})),
        WriterEpoch('gamma','g-new',b'H'*32,4,8,frozenset({'tank'})),
        WriterEpoch('delta','d-only',b'I'*32,1,8,frozenset({'tank'}))),(
        EncryptionEpoch('c-one',b'J'*32,1,4),EncryptionEpoch('c-two',b'K'*32,5,16)))
    def observation(producer,sequence):
        key,kid=(b'I'*32,'d-only') if producer=='delta' else ((b'G'*32,'g-old') if sequence<=3 else (b'H'*32,'g-new'))
        return sign_versioned(key,kid,producer,'tank',sequence,20000+sequence)
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory)
        witness=Witness(root/'w.db','reader-ledger',config.fingerprint(),b'L'*32)
        ledger=ProtectedLedger(root/'l.db','reader-ledger',config,witness,witness.public_key)
        schedule=[('gamma',1),('gamma',2),('delta',1),('gamma',3),('delta',2),('delta',3),('gamma',4),('delta',4)]
        for producer,seq in schedule:ledger.append(observation(producer,seq))
        snapshot=ledger.snapshot()
        projections={producer:[e['observation']['record']['seq'] for e in snapshot['entries'] if e['observation']['record']['producer']==producer] for producer in ('gamma','delta')}
        assert projections=={'gamma':[1,2,3,4],'delta':[1,2,3,4]}
        with sqlite3.connect(root/'l.db') as db:
            encryption_ids=[json.loads(raw)['header']['encryption_key'] for raw, in db.execute('SELECT raw FROM entries ORDER BY n')]
        assert encryption_ids==['c-one']*4+['c-two']*4
        retry=ledger.append(observation('gamma',2));assert retry['replay'] and retry['index']==2
        challenge=b'Q'*32;receipt=witness.head(challenge)
        assert verify_receipt(receipt,witness.public_key,'reader-ledger',config.fingerprint(),challenge)['n']==8
        try:verify_receipt(receipt,witness.public_key,'reader-ledger',config.fingerprint(),b'R'*32)
        except IntegrityError:stale_challenge_rejected=True
        else:raise AssertionError('replayed challenge accepted')
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);witness=Witness(root/'w.db','reader-ledger',config.fingerprint(),b'L'*32)
        ledger=ProtectedLedger(root/'l.db','reader-ledger',config,witness,witness.public_key)
        advance=witness.advance
        def unavailable(*args):raise ConnectionError('reader-injected authority unavailable')
        witness.advance=unavailable
        try:ledger.append(observation('gamma',1))
        except ConnectionError:uncertain=True
        else:raise AssertionError('injected authority failure not reached')
        with sqlite3.connect(root/'l.db') as db:local_before,=db.execute('SELECT count(*) FROM entries').fetchone()
        authority_before=witness.head(b'S'*32)['body']['n']
        assert (local_before,authority_before)==(1,0)
        witness.advance=advance
        reopened=ProtectedLedger(root/'l.db','reader-ledger',config,witness,witness.public_key)
        retry=reopened.append(observation('gamma',1));assert retry['replay']
        recovered=reopened.snapshot();assert recovered['count']==1 and recovered['entries'][0]['nonce']==(1).to_bytes(12,'big').hex()
        authority_after=witness.head(b'T'*32)['body']['n'];assert authority_after==1
        with sqlite3.connect(root/'w.db') as db:db.execute('UPDATE witness SET counter=?',(2**63-2,))
        last_nonce=witness.reserve_nonce();assert int(last_nonce,16)==2**63-1
        try:reopened.append(observation('gamma',2))
        except ValueError:exhaustion_rejected=True
        else:raise AssertionError('counter exhaustion not rejected')
        assert reopened.snapshot()['count']==1
    output=dict(source_sha256={name:hashlib.sha256((UNIT/name).read_bytes()).hexdigest() for name in ('protected_ledger.py','gcm_mechanics.py')},
                interleaving=schedule,producer_projections=projections,encryption_epoch_ids=encryption_ids,
                old_epoch_retry_original_index=2,stale_challenge_rejected=stale_challenge_rejected,
                authority_outage=dict(local_committed_before=local_before,witness_before=authority_before,
                                      witness_after_reopen=authority_after,original_nonce_retained=True,uncertain_ack_observed=uncertain),
                nonce_exhaustion=dict(last_reserved_hex=last_nonce,next_append_rejected=exhaustion_rejected,local_count_after=1),
                limits='Local separately selected finite probes. Authority access, monotonic custody and key exclusivity remain assumptions, not deployed infrastructure evidence.')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
