"""Create-only consistent SQLite generations in trusted private POSIX paths.

Checksums detect accidental damage, not hostile replacement. Restore only into
an unused offline path. The caller owns immutable generations and exclusivity.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import time
from operations import validate_request

MAX_BYTES=32*1024*1024
MAX_OPERATIONS=10000
FIELDS={'format','created_utc','sqlite','database_sha256','state_sha256',
        'counter','operation_count','database_bytes'}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')


def read_only(path):
    path=Path(path).resolve(strict=True)
    if not path.is_file() or not 0<path.stat().st_size<=MAX_BYTES:
        raise ValueError('bounded existing database required')
    return sqlite3.connect(path.as_uri()+'?mode=ro',uri=True,timeout=.1,isolation_level=None)


def checked_state(path):
    """One read transaction; do not repair missing schema or rows."""
    db=read_only(path)
    try:
        db.execute('PRAGMA query_only=ON');db.execute('BEGIN')
        if db.execute('PRAGMA quick_check').fetchall()!=[('ok',)]:
            raise ValueError('SQLite structural check failed')
        tables=db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
        if tables!=[('counter',),('operations',)]:raise ValueError('unexpected tables')
        if db.execute("SELECT name FROM sqlite_master WHERE type IN ('trigger','view')").fetchone():
            raise ValueError('unexpected trigger/view')
        for table,names in [('counter',['id','value']),('operations',['request_id','delta','result'])]:
            if [r[1] for r in db.execute('PRAGMA table_info('+table+')')]!=names:
                raise ValueError('schema columns differ')
        counters=db.execute('SELECT id,value FROM counter').fetchall()
        if len(counters)!=1 or counters[0][0]!=1 or type(counters[0][1]) is not int:
            raise ValueError('one integer counter required')
        rows=db.execute('SELECT request_id,delta,result FROM operations ORDER BY request_id LIMIT ?', (MAX_OPERATIONS+1,)).fetchall()
        if len(rows)>MAX_OPERATIONS:raise ValueError('operation budget exhausted')
        seen=set()
        for identity,delta,result in rows:
            validate_request(identity,delta)
            if identity in seen or type(result) is not int or not -10**12<=result<=10**12:
                raise ValueError('invalid retained receipt')
            seen.add(identity)
        value=counters[0][1]
        if not -10**12<=value<=10**12 or value!=sum(r[1] for r in rows):
            raise ValueError('counter/delta invariant failed')
        db.commit();return {'counter':value,'operations':rows}
    finally:db.close()


def digest_file(path):
    path=Path(path)
    if not 0<path.stat().st_size<=MAX_BYTES:raise ValueError('bounded file required')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync_directory(path):
    if os.name!='posix':raise RuntimeError('POSIX directory sync required')
    descriptor=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(descriptor)
    finally:os.close(descriptor)


def create_backup(source,generation,*,timeout_seconds=5):
    """Create NEW generation; manifest is last. Time checked between API steps.

    This cannot interrupt a stalled native/OS call. Page count and final bytes
    are checked; no hard quota on temporary disk consumption is promised.
    """
    if type(timeout_seconds) not in (int,float) or not 0<timeout_seconds<=30:
        raise ValueError('timeout must lie in(0,30]seconds')
    generation=Path(generation);generation.mkdir()
    target=generation/'snapshot.db';src=dst=None;started=time.monotonic()
    try:
        src=read_only(source);dst=sqlite3.connect(target)
        def progress(status,remaining,total):
            if total>MAX_BYTES//512 or time.monotonic()-started>timeout_seconds:
                raise TimeoutError('backup step budget exhausted')
        src.backup(dst,pages=8,progress=progress,sleep=.01)
        if dst.execute('PRAGMA journal_mode=DELETE').fetchone()[0].lower()!='delete':
            raise RuntimeError('self-contained snapshot required')
        dst.close();dst=None;src.close();src=None
        state=checked_state(target)
        manifest=dict(format='mm-operation-snapshot-v1',
                      created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      sqlite=sqlite3.sqlite_version,database_sha256=digest_file(target),
                      state_sha256=hashlib.sha256(canonical(state)).hexdigest(),
                      counter=state['counter'],operation_count=len(state['operations']),
                      database_bytes=target.stat().st_size)
        with target.open('rb') as stream:os.fsync(stream.fileno())
        with (generation/'MANIFEST.json').open('xb') as stream:
            stream.write(canonical(manifest)+b'\n');stream.flush();os.fsync(stream.fileno())
        sync_directory(generation);sync_directory(generation.parent)
        return manifest
    except BaseException:
        if src is not None:src.close()
        if dst is not None:dst.close()
        shutil.rmtree(generation)
        raise


def verify_backup(generation):
    generation=Path(generation);path=generation/'MANIFEST.json'
    if not path.is_file() or not 0<path.stat().st_size<=4096:
        raise ValueError('complete bounded manifest required')
    manifest=json.loads(path.read_bytes())
    if type(manifest) is not dict or set(manifest)!=FIELDS or manifest['format']!='mm-operation-snapshot-v1':
        raise ValueError('exact manifest schema required')
    target=generation/'snapshot.db'
    if digest_file(target)!=manifest['database_sha256']:raise ValueError('byte digest mismatch')
    state=checked_state(target)
    if (hashlib.sha256(canonical(state)).hexdigest()!=manifest['state_sha256'] or
        type(manifest['counter']) is not int or manifest['counter']!=state['counter'] or
        type(manifest['operation_count']) is not int or manifest['operation_count']!=len(state['operations']) or
        type(manifest['database_bytes']) is not int or manifest['database_bytes']!=target.stat().st_size):
        raise ValueError('logical snapshot evidence mismatch')
    return manifest,state


def restore_backup(generation,destination,*,known_receipts=()):
    """Only promote a new offline file if external original receipts agree."""
    receipts=[]
    for row in known_receipts:
        if len(receipts)>=MAX_OPERATIONS:raise ValueError('receipt budget exhausted')
        if type(row) not in (tuple,list) or len(row)!=3:raise ValueError('receipt triple required')
        identity,delta,result=row;validate_request(identity,delta)
        if type(result) is not int or not -10**12<=result<=10**12:raise ValueError('integer original result required')
        receipts.append((identity,delta,result))
    manifest,state=verify_backup(generation)
    retained={r[0]:(r[1],r[2]) for r in state['operations']}
    if any(retained.get(identity)!=(delta,result) for identity,delta,result in receipts):
        raise ValueError('external receipt absent/conflicting; do not promote')
    destination=Path(destination)
    if any(Path(str(destination)+suffix).exists() for suffix in ('','-wal','-shm','-journal')):
        raise FileExistsError('unused offline destination and sidecars required')
    created=False
    try:
        with destination.open('xb') as dst,(Path(generation)/'snapshot.db').open('rb') as src:
            created=True;shutil.copyfileobj(src,dst);dst.flush();os.fsync(dst.fileno())
        if digest_file(destination)!=manifest['database_sha256'] or checked_state(destination)!=state:
            raise ValueError('restored bytes/state differ')
        sync_directory(destination.parent)
        return dict(counter=state['counter'],operation_count=len(state['operations']),matched_external_receipts=len(receipts))
    except BaseException:
        if created:destination.unlink(missing_ok=True)
        raise
