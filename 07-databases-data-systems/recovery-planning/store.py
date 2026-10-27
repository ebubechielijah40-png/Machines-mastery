"""Original cooperating-client POSIX store: B+ checkpoint plus suffix WAL.

LOCK is a never-renamed inode. CURRENT selects exactly one generation; the
reader never guesses an older fallback after selected-state corruption. Trusted
private directories only. This is not a power-failure or network-FS certificate.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

INDEX=Path(__file__).resolve().parents[1]/'page-index'
sys.path.insert(0,str(INDEX))
from bplus import BPlusIndex,MAX_IMAGE_BYTES,key_number,value_bytes
from rebuild import wal_module

MAX_WAL_BYTES=16*1024*1024
MAX_OPERATIONS=1000
MAX_GENERATIONS=1000
GENERATION=re.compile(r'[0-9a-f]{32}\Z')


class StoreError(ValueError):pass
class ConflictError(RuntimeError):pass
class BusyError(RuntimeError):pass


@dataclass(frozen=True)
class Snapshot:
    rows:dict
    version:int
    generation:str
    suffix_transactions:int
    suffix_bytes:int
    trailing_bytes:int


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')


def bounded_read(path,limit):
    with path.open('rb') as stream:data=stream.read(limit+1)
    if len(data)>limit:raise StoreError('configured byte limit exceeded')
    return data


def sync_directory(path):
    descriptor=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(descriptor)
    finally:os.close(descriptor)


def write_new(path,data):
    with path.open('xb',buffering=0) as stream:
        wal_module()._write_all(stream,data);os.fsync(stream.fileno())


def checked_operations(operations):
    out=[]
    for raw in operations:
        if len(out)>=MAX_OPERATIONS:raise ValueError('at most1000 operations')
        if type(raw) not in (list,tuple) or not raw:raise ValueError('operation tuple/list required')
        if raw[0]=='put' and len(raw)==3:
            _,key,value=raw;key_number(key)
            if type(value) is not str:raise ValueError('UTF-8 string value required')
            value_bytes(value.encode('utf-8'));out.append(('put',key,value))
        elif raw[0]=='delete' and len(raw)==2:
            key_number(raw[1]);out.append(('delete',raw[1]))
        else:raise ValueError('put(key,text) or delete(key) required')
    if not out:raise ValueError('empty transaction not represented')
    return out


def apply(rows,operations):
    for operation in operations:
        if operation[0]=='put':rows[operation[1]]=operation[2]
        else:rows.pop(operation[1],None)


def tree_for(rows,page_size):
    return BPlusIndex.from_sorted(((k,v.encode('utf-8')) for k,v in sorted(rows.items())),page_size)


class Store:
    def __init__(self,directory,*,create=False,page_size=128):
        self.directory=Path(directory)
        if type(create) is not bool:raise ValueError('create must be boolean')
        if create:self.directory.mkdir(parents=True,exist_ok=True)
        if not self.directory.is_dir():raise StoreError('store directory missing')
        if create:
            with self.lock(exclusive=True):
                if not (self.directory/'CURRENT').exists():
                    if any(self.directory.glob('index-*.bpi')) or any(self.directory.glob('wal-*.wal')):
                        raise StoreError('orphan files without CURRENT: investigate explicitly')
                    self._publish({},0,page_size)
        if not (self.directory/'CURRENT').is_file():raise StoreError('CURRENT missing')

    @contextmanager
    def lock(self,*,exclusive,blocking=True):
        if type(exclusive) is not bool or type(blocking) is not bool:raise ValueError('boolean lock flags required')
        descriptor=os.open(self.directory/'LOCK',os.O_RDWR|os.O_CREAT,0o600)
        try:
            flags=fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
            try:fcntl.flock(descriptor,flags|(0 if blocking else fcntl.LOCK_NB))
            except BlockingIOError:raise BusyError('incompatible cooperating lock') from None
            yield
        finally:os.close(descriptor)

    def _load(self):
        try:
            raw=bounded_read(self.directory/'CURRENT',1024);envelope=json.loads(raw)
            if type(envelope) is not dict or set(envelope)!={'body','sha256'} or raw!=canonical(envelope):
                raise StoreError('exact canonical manifest required')
            body=envelope['body']
            if type(body) is not dict or set(body)!={'format','generation','base_version','index_sha256'}:
                raise StoreError('manifest body differs')
            generation=body['generation']
            if body['format']!='MMGEN1' or type(generation) is not str or not GENERATION.fullmatch(generation):
                raise StoreError('invalid format/generation')
            if type(body['base_version']) is not int or not 0<=body['base_version']<2**64:
                raise StoreError('invalid global version')
            if envelope['sha256']!=hashlib.sha256(canonical(body)).hexdigest():raise StoreError('manifest checksum differs')
            image=bounded_read(self.directory/f'index-{generation}.bpi',MAX_IMAGE_BYTES)
            if body['index_sha256']!=hashlib.sha256(image).hexdigest():raise StoreError('selected index digest differs')
            tree=BPlusIndex.loads(image);rows={k:v.decode('utf-8') for k,v in tree.range()}
            path=self.directory/f'wal-{generation}.wal'
            if path.stat().st_size>MAX_WAL_BYTES:raise StoreError('suffix WAL budget exceeded')
            module=wal_module();report=module.recover(path)
            # recover().data is relative to EMPTY state. Replaying its final
            # dictionary would resurrect base keys deleted by suffix tombstones.
            with path.open('rb') as stream:
                stream.seek(len(module.FILE_MAGIC))
                for _ in range(report.transactions):
                    _,_,size=module.HEADER.unpack(stream.read(module.HEADER.size))
                    original=json.loads(stream.read(size).decode('utf-8'));stream.read(module.CHECKSUM.size)
                    operations=checked_operations([(op[0],int(op[1]),*op[2:]) for op in original])
                    if any(str(op[1])!=rawop[1] for op,rawop in zip(operations,original)):
                        raise StoreError('noncanonical suffix key')
                    apply(rows,operations)
            tree_for(rows,tree._pages.page_size)
            version=body['base_version']+report.transactions
            if version>=2**64:raise StoreError('global version exhausted')
            return Snapshot(rows,version,generation,report.transactions,path.stat().st_size,report.trailing_bytes),tree._pages.page_size,report.valid_end
        except (OSError,UnicodeError,ValueError,TypeError,KeyError) as error:
            if isinstance(error,StoreError):raise
            raise StoreError(str(error)) from error

    def snapshot(self):
        with self.lock(exclusive=False):return self._load()[0]

    def commit(self,operations,*,expected_version=None,phase=lambda stage:None):
        checked=checked_operations(operations)
        if expected_version is not None and (type(expected_version) is not int or not 0<=expected_version<2**64):
            raise ValueError('expected_version must be uint64 or None')
        with self.lock(exclusive=True):
            before,page_size,_=self._load()
            if before.trailing_bytes:raise StoreError('incomplete suffix: inspect/repair before append')
            if expected_version is not None and expected_version!=before.version:raise ConflictError('stale version: reread and recompute')
            if before.version==2**64-1:raise StoreError('global version exhausted')
            candidate=before.rows.copy();apply(candidate,checked);tree_for(candidate,page_size)
            module=wal_module();frame=module.encode_transaction(before.suffix_transactions+1,[(op[0],str(op[1]),*op[2:]) for op in checked])
            if before.suffix_bytes+len(frame)>MAX_WAL_BYTES:raise StoreError('checkpoint before retry: WAL budget exhausted')
            with (self.directory/f'wal-{before.generation}.wal').open('ab',buffering=0) as stream:
                module._write_all(stream,frame);phase('after-append');os.fsync(stream.fileno());phase('after-commit-sync')
            return before.version+1

    def repair_tail(self):
        with self.lock(exclusive=True):
            before,_,valid_end=self._load()
            if before.trailing_bytes:
                with (self.directory/f'wal-{before.generation}.wal').open('r+b',buffering=0) as stream:
                    stream.truncate(valid_end);os.fsync(stream.fileno())
            return before.trailing_bytes

    def _publish(self,rows,version,page_size,phase=lambda stage:None):
        if sum(1 for _ in self.directory.iterdir())>MAX_GENERATIONS*3:
            raise StoreError('generation budget exhausted: investigate/collect')
        generation=uuid.uuid4().hex;image=tree_for(rows,page_size).dumps()
        write_new(self.directory/f'index-{generation}.bpi',image);phase('after-index-sync')
        write_new(self.directory/f'wal-{generation}.wal',wal_module().FILE_MAGIC);phase('after-wal-sync')
        sync_directory(self.directory);phase('after-generation-directory-sync')
        body=dict(format='MMGEN1',generation=generation,base_version=version,index_sha256=hashlib.sha256(image).hexdigest())
        temporary=self.directory/f'current-{generation}.tmp'
        write_new(temporary,canonical(dict(body=body,sha256=hashlib.sha256(canonical(body)).hexdigest())))
        phase('after-manifest-temp-sync');os.replace(temporary,self.directory/'CURRENT');phase('after-manifest-replace')
        sync_directory(self.directory);phase('after-manifest-directory-sync')
        return generation

    def checkpoint(self,*,collect=False,phase=lambda stage:None):
        if type(collect) is not bool:raise ValueError('collect must be boolean')
        with self.lock(exclusive=True):
            before,page_size,_=self._load()
            if before.trailing_bytes:raise StoreError('inspect/repair incomplete suffix first')
            generation=self._publish(before.rows,before.version,page_size,phase);removed=0
            if collect:
                for pattern in ('index-*.bpi','wal-*.wal','current-*.tmp'):
                    for path in self.directory.glob(pattern):
                        if path.name not in {f'index-{generation}.bpi',f'wal-{generation}.wal'}:
                            path.unlink();removed+=1;phase('after-old-unlink')
                sync_directory(self.directory);phase('after-collection-directory-sync')
            return dict(generation=generation,base_version=before.version,old_suffix_bytes=before.suffix_bytes,removed_files=removed)
