"""Original local authenticated provenance pipeline; not a deployed service.

Producer MAC authenticates a declared observation. Processor MAC binds the exact
transform, output, sequence and previous entry digest. Neither establishes truth.
Caller must exclusively own the pathname/object; there is no multi-writer lock,
key distribution, confidentiality or durable external tip/checkpoint service.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
from pathlib import Path
import re

MAX_REQUEST=8192
MAX_ENTRY=32768
ZERO='0'*64
RECORD_DOMAIN=b'MM-PROVENANCE-RECORD-v1\0'
LEDGER_DOMAIN=b'MM-PROVENANCE-LEDGER-v1\0'

class IntegrityError(ValueError): pass
class AuthorizationError(ValueError): pass
class SequenceError(ValueError): pass


def canonical(value):
    """Restricted protocol objects contain only validated strings/integers/maps."""
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def _unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise IntegrityError('duplicate JSON field')
        result[key]=value
    return result


def _reject_constant(value):
    raise IntegrityError('nonfinite JSON numbers are forbidden')


def decode(raw,maximum):
    if not isinstance(raw,bytes):raise TypeError('wire payload must be bytes')
    if len(raw)>maximum:raise IntegrityError('wire payload exceeds byte budget')
    try:return json.loads(raw.decode('ascii'),object_pairs_hook=_unique_object,parse_constant=_reject_constant)
    except (ValueError,UnicodeError,RecursionError) as exc:raise IntegrityError('invalid protocol JSON') from exc


def _identifier(value):
    if not isinstance(value,str) or re.fullmatch(r'[A-Za-z0-9._-]{1,32}',value) is None:
        raise IntegrityError('identifier must be 1–32 restricted ASCII characters')


def _key(key):
    if not isinstance(key,bytes) or len(key)<32:raise ValueError('configured keys must contain at least 32 bytes')


def _tag(value):
    if not isinstance(value,str) or re.fullmatch('[0-9a-f]{64}',value) is None:
        raise IntegrityError('tag/digest must be 64 lowercase hexadecimal characters')


def manual_hmac_sha256(key,message):
    """Educational HMAC construction, SHA-256 compression delegated to hashlib.

    Pipeline authentication uses stdlib hmac, not this teaching implementation.
    """
    if not isinstance(key,bytes) or not isinstance(message,bytes):raise TypeError('bytes required')
    block=64
    if len(key)>block:key=hashlib.sha256(key).digest()
    padded=key+b'\0'*(block-len(key))
    inner=bytes(x^0x36 for x in padded)
    outer=bytes(x^0x5c for x in padded)
    return hashlib.sha256(outer+hashlib.sha256(inner+message).digest()).digest()


def _mac(key,domain,value):
    return hmac.new(key,domain+canonical(value),hashlib.sha256).hexdigest()


def _record(record):
    fields={'v','producer','stream','seq','value_milli_c','unit'}
    if not isinstance(record,dict) or set(record)!=fields:raise IntegrityError('wrong observation schema')
    if type(record['v']) is not int or record['v']!=1:raise IntegrityError('unsupported record version')
    _identifier(record['producer']);_identifier(record['stream'])
    if type(record['seq']) is not int or not 1<=record['seq']<2**63:raise IntegrityError('seq must be a positive bounded integer')
    if type(record['value_milli_c']) is not int or not -50000<=record['value_milli_c']<=150000:
        raise IntegrityError('synthetic temperature must be an integer in configured range')
    if record['unit']!='milli_celsius':raise IntegrityError('unit mismatch')


def sign_observation(key,producer,stream,seq,value_milli_c):
    _key(key)
    record=dict(v=1,producer=producer,stream=stream,seq=seq,value_milli_c=value_milli_c,unit='milli_celsius')
    _record(record)
    return canonical({'record':record,'tag':_mac(key,RECORD_DOMAIN,record)})


def verify_observation(envelope,keys,policy,last_sequences):
    if not isinstance(envelope,dict) or set(envelope)!={'record','tag'}:raise IntegrityError('wrong envelope schema')
    record=envelope['record'];_record(record);_tag(envelope['tag'])
    producer=record['producer']
    if producer not in keys:raise IntegrityError('unknown producer')
    if not hmac.compare_digest(envelope['tag'],_mac(keys[producer],RECORD_DOMAIN,record)):
        raise IntegrityError('producer MAC mismatch')
    if record['stream'] not in policy.get(producer,set()):raise AuthorizationError('producer cannot write that stream')
    if record['seq']!=last_sequences.get(producer,0)+1:raise SequenceError('replay or out-of-order observation')
    return record


def transformed(record):
    # Exact rational output avoids a float/cross-language serialization convention.
    return {'numerator':record['value_milli_c'],'denominator':1000,'unit':'celsius'}


def _write_all(stream,raw):
    view=memoryview(raw)
    while view:
        n=stream.write(view)
        if n is None or n<=0:raise OSError('write made no progress')
        view=view[n:]


class Pipeline:
    def __init__(self,path,producer_keys,processor_key,policy,readers=('analyst',),*,expected_tip=None,max_entries=10000):
        _key(processor_key)
        if type(max_entries) is not int or max_entries<1:raise ValueError('max_entries must be a positive integer')
        self.keys=dict(producer_keys)
        for producer,key in self.keys.items():_identifier(producer);_key(key)
        self.processor_key=processor_key
        self.policy={p:set(streams) for p,streams in policy.items()}
        for producer,streams in self.policy.items():
            _identifier(producer)
            for stream in streams:_identifier(stream)
        self.readers=set(readers)
        self.path=Path(path);self.last={};self.values={};self.tip=ZERO;self.count=0
        self.maximum=max_entries;self.poisoned=False;self._stream=None
        self._load()
        if expected_tip is not None:
            _tag(expected_tip)
            if not hmac.compare_digest(self.tip,expected_tip):raise IntegrityError('ledger differs from trusted expected tip')
        self._stream=self.path.open('ab',buffering=0)

    def _accept_entry(self,entry):
        if not isinstance(entry,dict) or set(entry)!={'core','processor_tag'}:raise IntegrityError('wrong entry schema')
        core=entry['core']
        if not isinstance(core,dict) or set(core)!={'index','previous','observation','transform','output'}:
            raise IntegrityError('wrong core schema')
        _tag(entry['processor_tag'])
        if not hmac.compare_digest(entry['processor_tag'],_mac(self.processor_key,LEDGER_DOMAIN,core)):
            raise IntegrityError('processor MAC mismatch')
        if type(core['index']) is not int or core['index']!=self.count+1 or core['previous']!=self.tip:
            raise IntegrityError('chain position/previous digest mismatch')
        if core['transform']!='milli-c-to-c/v1':raise IntegrityError('unsupported transformation')
        record=verify_observation(core['observation'],self.keys,self.policy,self.last)
        if canonical(core['output'])!=canonical(transformed(record)):raise IntegrityError('incorrect derived output')
        self.last[record['producer']]=record['seq']
        self.values[(record['producer'],record['stream'])]=transformed(record)
        self.tip=hashlib.sha256(canonical(entry)).hexdigest();self.count+=1

    def _load(self):
        if not self.path.exists():return
        with self.path.open('rb') as stream:
            while True:
                raw=stream.readline(MAX_ENTRY+1)
                if not raw:break
                if len(raw)>MAX_ENTRY or not raw.endswith(b'\n'):
                    raise IntegrityError('oversize or incomplete ledger line; inspect before recovery')
                if self.count>=self.maximum:raise IntegrityError('ledger entry budget exceeded')
                self._accept_entry(decode(raw[:-1],MAX_ENTRY))

    def ingest(self,raw):
        if self.poisoned or self._stream is None:raise RuntimeError('pipeline closed or poisoned; reopen and reconcile')
        if self.count>=self.maximum:raise IntegrityError('ledger entry budget exhausted')
        envelope=decode(raw,MAX_REQUEST)
        record=verify_observation(envelope,self.keys,self.policy,self.last)
        core={'index':self.count+1,'previous':self.tip,'observation':envelope,
              'transform':'milli-c-to-c/v1','output':transformed(record)}
        entry={'core':core,'processor_tag':_mac(self.processor_key,LEDGER_DOMAIN,core)}
        serialized=canonical(entry)+b'\n'
        if len(serialized)>MAX_ENTRY:raise IntegrityError('serialized entry too large')
        try:
            _write_all(self._stream,serialized)
            os.fsync(self._stream.fileno())
        except BaseException:
            self.poisoned=True
            raise
        # No state mutation before durable-content acknowledgement in this model.
        self._accept_entry(entry)
        return self.tip

    def snapshot(self,principal):
        if principal not in self.readers:raise AuthorizationError('principal cannot read observations')
        return {producer+'/'+stream:dict(value) for (producer,stream),value in self.values.items()}

    def close(self):
        if self._stream is not None:self._stream.close();self._stream=None
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
