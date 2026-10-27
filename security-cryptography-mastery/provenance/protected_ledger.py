"""Original bounded encrypted history and separate monotonic witness model.

AES-GCM and Ed25519 are supplied by cryptography, not homemade primitives.
Trusted private paths/configuration; same-host separation is not rollback
protection. Encryption keys MUST be exclusive to one witness nonce allocator.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import hmac
import os
from pathlib import Path
import re
import sqlite3
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey,Ed25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pipeline import IntegrityError,AuthorizationError,SequenceError,ZERO,canonical,decode,_identifier,_tag,_record,transformed

MAX_ENTRIES=10000
MAX_FRAME=32768
OBS_DOMAIN=b'MM-EPOCH-OBS-v1\0'
FRAME_DOMAIN=b'MM-ENCRYPTED-HISTORY-v1\0'
RECEIPT_DOMAIN=b'MM-WITNESS-CONFIG-HEAD-v1\0'


class RollbackDetected(IntegrityError):pass


def key32(value):
    if type(value) is not bytes or len(value)!=32:raise ValueError('exactly32 key bytes required')


def bounded(value,minimum=1,maximum=MAX_ENTRIES):
    if type(value) is not int or not minimum<=value<=maximum:raise ValueError('bounded integer required')


@dataclass(frozen=True)
class WriterEpoch:
    producer:str
    key_id:str
    key:bytes
    first:int
    last:int
    streams:frozenset

    def __post_init__(self):
        _identifier(self.producer);_identifier(self.key_id);key32(self.key)
        bounded(self.first);bounded(self.last)
        if self.first>self.last:raise ValueError('reversed epoch')
        if type(self.streams) is not frozenset or not 1<=len(self.streams)<=32:raise ValueError('bounded frozen streams required')
        for name in self.streams:_identifier(name)


@dataclass(frozen=True)
class EncryptionEpoch:
    key_id:str
    key:bytes
    first:int
    last:int

    def __post_init__(self):
        _identifier(self.key_id);key32(self.key);bounded(self.first);bounded(self.last)
        if self.first>self.last:raise ValueError('reversed epoch')


@dataclass(frozen=True)
class Configuration:
    writers:tuple
    encryption:tuple

    def __post_init__(self):
        if type(self.writers) is not tuple or type(self.encryption) is not tuple:raise TypeError('immutable epoch tuples required')
        if not 1<=len(self.writers)<=64 or not 1<=len(self.encryption)<=64:raise ValueError('epoch count budget exhausted')
        if any(type(e) is not WriterEpoch for e in self.writers) or any(type(e) is not EncryptionEpoch for e in self.encryption):raise TypeError('epoch records required')
        for collection in (self.writers,self.encryption):
            if len({e.key_id for e in collection})!=len(collection):raise ValueError('duplicate key ID')
            if len({e.key for e in collection})!=len(collection):raise ValueError('distinct epoch key material required')
        if {e.key for e in self.writers}&{e.key for e in self.encryption}:raise ValueError('separate authentication/encryption roles required')
        for collection in [self.encryption]+[tuple(e for e in self.writers if e.producer==p) for p in {e.producer for e in self.writers}]:
            previous=0
            for epoch in sorted(collection,key=lambda e:e.first):
                if epoch.first!=previous+1:raise ValueError('epochs must be contiguous from1')
                previous=epoch.last

    def fingerprint(self):
        obj={'writers':[dict(producer=e.producer,key_id=e.key_id,key_sha256=hashlib.sha256(e.key).hexdigest(),first=e.first,last=e.last,streams=sorted(e.streams)) for e in self.writers],
             'encryption':[dict(key_id=e.key_id,key_sha256=hashlib.sha256(e.key).hexdigest(),first=e.first,last=e.last) for e in self.encryption]}
        return hashlib.sha256(canonical(obj)).hexdigest()

    def writer(self,producer,key_id,sequence,stream):
        for epoch in self.writers:
            if (epoch.producer,epoch.key_id)==(producer,key_id) and epoch.first<=sequence<=epoch.last and stream in epoch.streams:return epoch
        raise AuthorizationError('writer epoch/stream does not authorize this sequence')

    def cipher(self,index,key_id=None):
        for epoch in self.encryption:
            if epoch.first<=index<=epoch.last and (key_id is None or epoch.key_id==key_id):return epoch
        raise AuthorizationError('no matching encryption epoch')


def sign_versioned(key,key_id,producer,stream,sequence,value_milli_c):
    key32(key);_identifier(key_id)
    record=dict(v=1,producer=producer,stream=stream,seq=sequence,value_milli_c=value_milli_c,unit='milli_celsius')
    _record(record);bounded(sequence)
    body=dict(key_id=key_id,record=record)
    return canonical({**body,'tag':hmac.new(key,OBS_DOMAIN+canonical(body),hashlib.sha256).hexdigest()})


def verify_observation(raw,configuration):
    obj=decode(raw,8192)
    if type(obj) is not dict or set(obj)!={'key_id','record','tag'}:raise IntegrityError('exact epoch observation required')
    _identifier(obj['key_id']);_tag(obj['tag']);_record(obj['record']);bounded(obj['record']['seq'])
    r=obj['record'];epoch=configuration.writer(r['producer'],obj['key_id'],r['seq'],r['stream'])
    body=dict(key_id=obj['key_id'],record=r)
    expected=hmac.new(epoch.key,OBS_DOMAIN+canonical(body),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(obj['tag'],expected):raise IntegrityError('writer MAC mismatch')
    return obj


@contextmanager
def connection(path):
    path=Path(path)
    if path.exists() and path.stat().st_size>64*1024*1024:raise IntegrityError('database byte budget exceeded')
    db=sqlite3.connect(path,timeout=5,isolation_level=None)
    try:
        db.execute('PRAGMA synchronous=FULL');db.execute('PRAGMA busy_timeout=5000')
        yield db
    finally:db.close()


class Witness:
    """Authorized-call model with separately trusted monotonic state/key.

    There is no remote authentication protocol here. Restoring this authority
    together with the ledger violates the monotonic-state assumption.
    """
    def __init__(self,path,ledger_id,configuration_sha256,private_seed):
        _identifier(ledger_id);_tag(configuration_sha256);key32(private_seed)
        self.path=Path(path);self.ledger_id=ledger_id;self.configuration_sha256=configuration_sha256
        self.signer=Ed25519PrivateKey.from_private_bytes(private_seed)
        self.public_key=self.signer.public_key().public_bytes_raw()
        with connection(path) as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('CREATE TABLE IF NOT EXISTS witness(singleton INTEGER PRIMARY KEY CHECK(singleton=1),ledger TEXT,config TEXT,public_key BLOB,n INTEGER,tip TEXT,counter INTEGER)')
            row=db.execute('SELECT ledger,config,public_key FROM witness').fetchone()
            expected=(ledger_id,configuration_sha256,self.public_key)
            if row is None:db.execute('INSERT INTO witness VALUES(1,?,?,?,?,?,0)',(*expected,0,ZERO))
            elif row!=expected:raise IntegrityError('authority identity/configuration mismatch')
            db.execute('COMMIT')

    def head(self,challenge):
        key32(challenge)
        with connection(self.path) as db:n,tip=db.execute('SELECT n,tip FROM witness WHERE singleton=1').fetchone()
        bounded(n,0);_tag(tip)
        body=dict(ledger=self.ledger_id,config=self.configuration_sha256,n=n,tip=tip,challenge=challenge.hex())
        return dict(body=body,signature=self.signer.sign(RECEIPT_DOMAIN+canonical(body)).hex())

    def reserve_nonce(self):
        with connection(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            counter,=db.execute('SELECT counter FROM witness WHERE singleton=1').fetchone()
            bounded(counter,0,2**63-2);counter+=1
            db.execute('UPDATE witness SET counter=? WHERE singleton=1',(counter,));db.execute('COMMIT')
        return (b'\0'*4+counter.to_bytes(8,'big')).hex()

    def advance(self,expected_n,expected_tip,next_tip):
        bounded(expected_n,0,MAX_ENTRIES-1);_tag(expected_tip);_tag(next_tip)
        with connection(self.path) as db:
            db.execute('BEGIN IMMEDIATE');current=db.execute('SELECT n,tip FROM witness WHERE singleton=1').fetchone()
            if current==(expected_n+1,next_tip):db.execute('COMMIT');return
            if current!=(expected_n,expected_tip):raise RollbackDetected('authority compare-and-set conflict')
            db.execute('UPDATE witness SET n=?,tip=? WHERE singleton=1',(expected_n+1,next_tip));db.execute('COMMIT')


def verify_receipt(receipt,public_key,ledger_id,configuration_sha256,challenge):
    key32(public_key);key32(challenge);_identifier(ledger_id);_tag(configuration_sha256)
    if type(receipt) is not dict or set(receipt)!={'body','signature'}:raise IntegrityError('exact receipt required')
    body=receipt['body']
    if type(body) is not dict or set(body)!={'ledger','config','n','tip','challenge'}:raise IntegrityError('exact receipt body required')
    if (body['ledger'],body['config'],body['challenge'])!=(ledger_id,configuration_sha256,challenge.hex()):raise IntegrityError('receipt identity/configuration/challenge mismatch')
    bounded(body['n'],0);_tag(body['tip'])
    signature=receipt['signature']
    if type(signature) is not str or re.fullmatch('[0-9a-f]{128}',signature) is None:raise IntegrityError('bounded signature required')
    try:Ed25519PublicKey.from_public_bytes(public_key).verify(bytes.fromhex(signature),RECEIPT_DOMAIN+canonical(body))
    except (InvalidSignature,ValueError) as error:raise IntegrityError('authority signature invalid') from error
    return dict(body)


class ProtectedLedger:
    def __init__(self,path,ledger_id,configuration,witness,pinned_witness_key):
        _identifier(ledger_id);key32(pinned_witness_key)
        if type(configuration) is not Configuration:raise TypeError('Configuration required')
        self.path=Path(path);self.ledger_id=ledger_id;self.config=configuration;self.witness=witness;self.pinned=pinned_witness_key
        if self.path.resolve()==witness.path.resolve():raise ValueError('separate authority store required')
        with connection(path) as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('CREATE TABLE IF NOT EXISTS metadata(singleton INTEGER PRIMARY KEY CHECK(singleton=1),ledger TEXT,config TEXT)')
            db.execute('CREATE TABLE IF NOT EXISTS entries(n INTEGER PRIMARY KEY,raw BLOB NOT NULL)')
            row=db.execute('SELECT ledger,config FROM metadata').fetchone();expected=(ledger_id,configuration.fingerprint())
            if row is None:db.execute('INSERT INTO metadata VALUES(1,?,?)',expected)
            elif row!=expected:raise IntegrityError('ledger identity/configuration mismatch')
            self._reconcile(db);db.execute('COMMIT')

    def _read(self,db):
        rows=db.execute('SELECT n,length(raw) FROM entries ORDER BY n LIMIT ?',(MAX_ENTRIES+1,)).fetchall()
        if len(rows)>MAX_ENTRIES or any(type(size) is not int or not 1<=size<=MAX_FRAME for _,size in rows):raise IntegrityError('entry/frame budget exceeded')
        entries=[];last={};previous=ZERO;seen=set()
        for position,(index,_) in enumerate(rows,1):
            if type(index) is not int or position!=index:raise IntegrityError('noncontiguous index')
            raw,=db.execute('SELECT raw FROM entries WHERE n=?',(index,)).fetchone();frame=decode(raw,MAX_FRAME)
            if type(frame) is not dict or set(frame)!={'header','ciphertext'}:raise IntegrityError('exact encrypted frame required')
            header=frame['header'];fields={'v','ledger','n','previous','producer','writer_key','sequence','stream','encryption_key','nonce','request_digest'}
            if type(header) is not dict or set(header)!=fields:raise IntegrityError('exact authenticated header required')
            if type(header['v']) is not int or header['v']!=1 or type(header['n']) is not int or header['n']!=index:raise IntegrityError('version/position mismatch')
            if header['ledger']!=self.ledger_id or header['previous']!=previous:raise IntegrityError('ledger/previous link mismatch')
            for name in ('producer','writer_key','stream','encryption_key'):_identifier(header[name])
            bounded(header['sequence']);_tag(header['previous']);_tag(header['request_digest'])
            if type(header['nonce']) is not str or re.fullmatch('[0-9a-f]{24}',header['nonce']) is None:raise IntegrityError('96-bit nonce required')
            if type(frame['ciphertext']) is not str or len(frame['ciphertext'])%2 or not 32<=len(frame['ciphertext'])<=MAX_FRAME:raise IntegrityError('bounded ciphertext required')
            try:ciphertext=bytes.fromhex(frame['ciphertext'])
            except ValueError as error:raise IntegrityError('invalid ciphertext hex') from error
            epoch=self.config.cipher(index,header['encryption_key']);nonce=bytes.fromhex(header['nonce'])
            if (epoch.key_id,nonce) in seen:raise IntegrityError('nonce reused in retained history')
            seen.add((epoch.key_id,nonce))
            try:plain=AESGCM(epoch.key).decrypt(nonce,ciphertext,FRAME_DOMAIN+canonical(header))
            except InvalidTag as error:raise IntegrityError('encrypted frame authentication failed') from error
            payload=decode(plain,8192)
            if type(payload) is not dict or set(payload)!={'observation','output'}:raise IntegrityError('exact plaintext required')
            observation=verify_observation(canonical(payload['observation']),self.config);r=observation['record']
            if (r['producer'],observation['key_id'],r['seq'],r['stream'])!=(header['producer'],header['writer_key'],header['sequence'],header['stream']):raise IntegrityError('plaintext/header identity differs')
            if r['seq']!=last.get(r['producer'],0)+1:raise SequenceError('retained producer sequence gap')
            if header['request_digest']!=hashlib.sha256(canonical(observation)).hexdigest():raise IntegrityError('request digest mismatch')
            if canonical(payload['output'])!=canonical(transformed(r)):raise IntegrityError('transformed value mismatch')
            previous=hashlib.sha256(canonical(frame)).hexdigest();last[r['producer']]=r['seq']
            entries.append(dict(index=index,digest=previous,observation=observation,output=payload['output'],nonce=header['nonce']))
        return entries,last

    def _reconcile(self,db):
        entries,last=self._read(db);challenge=os.urandom(32)
        head=verify_receipt(self.witness.head(challenge),self.pinned,self.ledger_id,self.config.fingerprint(),challenge)
        n=head['n'];tip=entries[n-1]['digest'] if 0<n<=len(entries) else ZERO
        if n>len(entries) or tip!=head['tip']:raise RollbackDetected('local history differs from independent authority')
        for entry in entries[n:]:
            self.witness.advance(n,head['tip'],entry['digest']);n+=1;head['tip']=entry['digest']
        return entries,last

    def append(self,raw,*,fault=None):
        observation=verify_observation(raw,self.config);record=observation['record'];request=canonical(observation)
        with connection(self.path) as db:
            db.execute('BEGIN IMMEDIATE');entries,last=self._reconcile(db)
            for entry in entries:
                old=entry['observation']['record']
                if (old['producer'],old['seq'])==(record['producer'],record['seq']):
                    if canonical(entry['observation'])!=request:raise SequenceError('conflicting same-sequence retry')
                    db.execute('COMMIT');return dict(index=entry['index'],digest=entry['digest'],replay=True)
            if record['seq']!=last.get(record['producer'],0)+1:raise SequenceError('new observation is not next sequence')
            index=len(entries)+1;bounded(index);epoch=self.config.cipher(index);nonce=self.witness.reserve_nonce()
            # Extra guard for a counter inconsistent with retained local history.
            # It cannot remember encryptions absent after whole-history rollback.
            if nonce in {entry['nonce'] for entry in entries}:raise IntegrityError('authority nonce repeats retained history')
            if fault:fault('after_nonce')
            header=dict(v=1,ledger=self.ledger_id,n=index,previous=entries[-1]['digest'] if entries else ZERO,
                        producer=record['producer'],writer_key=observation['key_id'],sequence=record['seq'],stream=record['stream'],
                        encryption_key=epoch.key_id,nonce=nonce,request_digest=hashlib.sha256(request).hexdigest())
            plain=canonical(dict(observation=observation,output=transformed(record)))
            ciphertext=AESGCM(epoch.key).encrypt(bytes.fromhex(nonce),plain,FRAME_DOMAIN+canonical(header))
            frame=canonical(dict(header=header,ciphertext=ciphertext.hex()))
            if len(frame)>MAX_FRAME:raise IntegrityError('frame budget exceeded')
            db.execute('INSERT INTO entries VALUES(?,?)',(index,frame))
            if fault:fault('before_commit')
            db.execute('COMMIT')
        if fault:fault('after_commit')
        with connection(self.path) as db:
            db.execute('BEGIN IMMEDIATE');self._reconcile(db);db.execute('COMMIT')
        if fault:fault('after_witness')
        return dict(index=index,digest=hashlib.sha256(frame).hexdigest(),replay=False)

    def snapshot(self):
        with connection(self.path) as db:
            db.execute('BEGIN IMMEDIATE');entries,_=self._reconcile(db);db.execute('COMMIT')
        values={}
        for entry in entries:
            r=entry['observation']['record'];values[r['producer']+'/'+r['stream']]=dict(entry['output'])
        return dict(count=len(entries),tip=entries[-1]['digest'] if entries else ZERO,values=values,entries=entries)

    def backup(self,destination):
        destination=Path(destination);fd=os.open(destination,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
        try:
            with connection(self.path) as source,connection(destination) as target:source.backup(target)
        except BaseException:destination.unlink(missing_ok=True);raise
        return destination
