from dataclasses import replace
import hashlib
import json
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pipeline import IntegrityError,AuthorizationError,SequenceError,canonical
from protected_ledger import Configuration,WriterEpoch,EncryptionEpoch,Witness,ProtectedLedger,RollbackDetected,sign_versioned,verify_receipt
from protected_demo import resources,configuration,observation
from gcm_mechanics import field_multiply,ghash,reconstructed_tag

HERE=Path(__file__).resolve().parent


class PrimitiveTests(unittest.TestCase):
    def test_inspected_nist_examples_and_explicit_ghash(self):
        key=bytes.fromhex('feffe9928665731c6d6a8f9467308308');nonce=bytes.fromhex('cafebabefacedbaddecaf888')
        self.assertEqual(AESGCM(key).encrypt(nonce,b'',b'').hex(),'3247184b3c4f69a44dbcd22887bbb418')
        plain=bytes.fromhex('d9313225f88406e5a55909c5aff5269a86a7a9531534f7da2e4c303d8a318a721c3c0c95956809532fcf0e2449a6b525b16aedf5aa0de657ba637b391aafd255')
        expected=bytes.fromhex('42831ec2217774244b7221b784d0d49ce3aa212f2c02a4e035c17e2329aca12e21d514b25466931c7d8f6a5aac84aa051ba30b396a0aac973d58e091473f59854d5c2af327cd64a62cf35abd2ba6fab4')
        self.assertEqual(AESGCM(key).encrypt(nonce,plain,b''),expected)
        self.assertEqual(ghash(bytes.fromhex('b83b533708bf535d0aa6e52980d53b78'),b'',expected[:-16]).hex(),'7f1b32b81b820d02614f8895ac1d4eac')
        self.assertEqual(reconstructed_tag(key,nonce,b'',expected[:-16]),expected[-16:])

    def test_independent_polynomial_reduction_and_length_binding(self):
        def oracle(a,b):
            reverse=lambda n:int(f'{n:0128b}'[::-1],2)
            a,b=reverse(a),reverse(b);product=0
            for i in range(128):
                if (b>>i)&1:product^=a<<i
            modulus=(1<<128)|(1<<7)|(1<<2)|(1<<1)|1
            for i in range(254,127,-1):
                if (product>>i)&1:product^=modulus<<(i-128)
            return reverse(product)
        for i in range(32):
            a=int.from_bytes(hashlib.sha256(f'a{i}'.encode()).digest()[:16],'big');b=int.from_bytes(hashlib.sha256(f'b{i}'.encode()).digest()[:16],'big')
            self.assertEqual(field_multiply(a,b),oracle(a,b))
        for aad in (b'',b'a',b'a'*16,b'a'*17):
            for plain in (b'',b'p',b'p'*16,b'p'*33):
                key=b't'*32;nonce=hashlib.sha256(aad+plain).digest()[:12]
                result=AESGCM(key).encrypt(nonce,plain,aad)
                self.assertEqual(reconstructed_tag(key,nonce,aad,result[:-16]),result[-16:])
        with self.assertRaises(ValueError):field_multiply(True,0)

    def test_different_aad_does_not_repair_reused_nonce(self):
        key=b'k'*32;nonce=b'n'*12;a=b'A'*32;b=b'B'*32
        first=AESGCM(key).encrypt(nonce,a,b'ledger-A');second=AESGCM(key).encrypt(nonce,b,b'ledger-B')
        self.assertEqual(bytes(x^y for x,y in zip(first[:-16],second[:-16])),bytes(x^y for x,y in zip(a,b)))
        with self.assertRaises(InvalidTag):AESGCM(key).decrypt(nonce,first,b'ledger-B')


class ProtectedTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.config,self.witness,self.ledger=resources(self.root)
    def tearDown(self):self.temp.cleanup()

    def test_history_rotations_and_exact_original_retry(self):
        for seq in range(1,5):self.ledger.append(observation(seq,25000+seq))
        snapshot=self.ledger.snapshot()
        self.assertEqual(snapshot['count'],4)
        self.assertEqual(snapshot['values']['alpha/room'],dict(numerator=25004,denominator=1000,unit='celsius'))
        retry=self.ledger.append(observation(1,25001))
        self.assertTrue(retry['replay']);self.assertEqual(retry['digest'],snapshot['entries'][0]['digest'])
        with self.assertRaises(SequenceError):self.ledger.append(observation(1,26000))

    def test_retired_key_new_sequence_and_stream_rejected(self):
        self.ledger.append(observation(1));self.ledger.append(observation(2))
        with self.assertRaises(AuthorizationError):self.ledger.append(sign_versioned(b'a'*32,'alpha-old','alpha','room',3,25001))
        with self.assertRaises(AuthorizationError):self.ledger.append(sign_versioned(b'b'*32,'alpha-new','alpha','lab',3,25001))
        self.ledger.append(observation(3));self.assertEqual(self.ledger.snapshot()['count'],3)

    def test_wrong_key_and_gap_do_not_mutate_history(self):
        with self.assertRaises(IntegrityError):self.ledger.append(sign_versioned(b'b'*32,'alpha-old','alpha','room',1,25001))
        with self.assertRaises(SequenceError):self.ledger.append(observation(2))
        self.assertEqual(self.ledger.snapshot()['count'],0)

    def test_fresh_receipt_binds_configuration_identity_and_key(self):
        challenge=b'q'*32;r=self.witness.head(challenge)
        self.assertEqual(verify_receipt(r,self.witness.public_key,'observations',self.config.fingerprint(),challenge)['n'],0)
        for ledger,config,nonce in [('other',self.config.fingerprint(),challenge),('observations','0'*64,challenge),('observations',self.config.fingerprint(),b'r'*32)]:
            with self.assertRaises(IntegrityError):verify_receipt(r,self.witness.public_key,ledger,config,nonce)
        r['body']['n']=1
        with self.assertRaises(IntegrityError):verify_receipt(r,self.witness.public_key,'observations',self.config.fingerprint(),challenge)
        with self.assertRaises(IntegrityError):ProtectedLedger(self.root/'ledger.db','observations',self.config,self.witness,b'x'*32)

    def test_valid_signed_authority_with_wrong_configuration_rejected(self):
        other=Witness(self.root/'different-authority.db','observations','0'*64,b'w'*32)
        with self.assertRaisesRegex(IntegrityError,'configuration'):
            ProtectedLedger(self.root/'new-ledger.db','observations',self.config,other,other.public_key)

    def test_ciphertext_header_and_suffix_tampering(self):
        for variant in ('cipher','header','delete'):
            with tempfile.TemporaryDirectory() as directory:
                _,_,ledger=resources(directory);ledger.append(observation(1))
                with sqlite3.connect(Path(directory)/'ledger.db') as db:
                    if variant=='delete':db.execute('DELETE FROM entries')
                    else:
                        raw,=db.execute('SELECT raw FROM entries').fetchone();obj=json.loads(raw)
                        if variant=='header':obj['header']['stream']='elsewhere'
                        else:
                            encrypted=bytearray.fromhex(obj['ciphertext']);encrypted[0]^=1;obj['ciphertext']=encrypted.hex()
                        db.execute('UPDATE entries SET raw=?',(canonical(obj),))
                with self.assertRaises(IntegrityError):ledger.snapshot()

    def test_old_backup_rejected_by_current_authority(self):
        self.ledger.append(observation(1));backup=self.ledger.backup(self.root/'old.db');self.ledger.append(observation(2))
        with self.assertRaises(RollbackDetected):ProtectedLedger(backup,'observations',self.config,self.witness,self.witness.public_key)
        with self.assertRaises(FileExistsError):self.ledger.backup(backup)

    def test_nonce_reservation_is_not_rolled_back_with_local_transaction(self):
        def fault(stage):
            if stage=='before_commit':raise OSError('injected failure')
        with self.assertRaises(OSError):self.ledger.append(observation(1),fault=fault)
        self.assertEqual(self.ledger.snapshot()['count'],0)
        self.ledger.append(observation(1))
        self.assertEqual(self.ledger.snapshot()['entries'][0]['nonce'],(2).to_bytes(12,'big').hex())

    def test_corrupted_counter_repetition_refused_before_encryption(self):
        self.ledger.append(observation(1))
        with sqlite3.connect(self.witness.path) as db:db.execute('UPDATE witness SET counter=0')
        with self.assertRaisesRegex(IntegrityError,'nonce repeats'):self.ledger.append(observation(2))
        self.assertEqual(self.ledger.snapshot()['count'],1)

    def test_after_commit_unknown_ack_reconciles_on_reopen(self):
        def fault(stage):
            if stage=='after_commit':raise OSError('reply lost')
        with self.assertRaises(OSError):self.ledger.append(observation(1),fault=fault)
        challenge=b'z'*32;self.assertEqual(self.witness.head(challenge)['body']['n'],0)
        _,_,reopened=resources(self.root)
        self.assertTrue(reopened.append(observation(1))['replay'])
        self.assertEqual(self.witness.head(challenge)['body']['n'],1)

    def test_two_actual_process_writers_serialize(self):
        children=[subprocess.Popen([sys.executable,str(HERE/'protected_worker.py'),str(self.root),'append',producer],stdout=subprocess.PIPE,stderr=subprocess.PIPE) for producer in ('alpha','beta')]
        for child in children:
            _,error=child.communicate(timeout=20);self.assertEqual(child.returncode,0,error)
        snapshot=self.ledger.snapshot();self.assertEqual(snapshot['count'],12)
        for producer in ('alpha','beta'):
            self.assertEqual([e['observation']['record']['seq'] for e in snapshot['entries'] if e['observation']['record']['producer']==producer],list(range(1,7)))
        self.assertEqual(len({e['nonce'] for e in snapshot['entries']}),12)

    @unittest.skipUnless(sys.platform.startswith('linux'),'SIGKILL observation requires Linux')
    def test_real_process_kill_before_and_after_commit(self):
        for stage,expected_nonce in [('after_nonce',2),('before_commit',2),('after_commit',1),('after_witness',1)]:
            with tempfile.TemporaryDirectory() as directory:
                resources(directory)
                child=subprocess.run([sys.executable,str(HERE/'protected_worker.py'),directory,'kill',stage],capture_output=True,timeout=10)
                self.assertEqual(child.returncode,-signal.SIGKILL,child.stderr)
                _,_,ledger=resources(directory);ledger.append(observation(1));snapshot=ledger.snapshot()
                self.assertEqual(snapshot['count'],1)
                self.assertEqual(snapshot['entries'][0]['nonce'],expected_nonce.to_bytes(12,'big').hex())

    def test_configuration_rejects_alias_keys_and_noncontiguous_epochs(self):
        a=self.config.writers[0];cipher=self.config.encryption[0]
        with self.assertRaises(ValueError):Configuration((a,), (replace(cipher,key=a.key),))
        with self.assertRaises(ValueError):Configuration((replace(a,first=2),),(cipher,))
        with self.assertRaises(ValueError):Configuration((a,replace(a,key_id='different',first=3,last=4)),(cipher,))
        with self.assertRaises(ValueError):WriterEpoch('alpha','a',b'a'*32,True,2,frozenset({'room'}))


if __name__=='__main__':unittest.main()
