"""Actual bounded subprocess/loopback/backup rehearsal; no remote side effects."""
from contextlib import contextmanager
import hashlib
import http.client
import json
import os
from pathlib import Path
import platform
import selectors
import sqlite3
import subprocess
import sys
import tempfile
import time
from recovery import create_backup,restore_backup

HERE=Path(__file__).resolve().parent


@contextmanager
def running(path,release='stable-v1'):
    child=subprocess.Popen([sys.executable,'-u',str(HERE/'local_service.py'),str(path),'--release',release],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        with selectors.DefaultSelector() as ready:
            ready.register(child.stdout,selectors.EVENT_READ)
            if not ready.select(5):raise TimeoutError('local release readiness timed out')
        raw=child.stdout.readline(1024)
        if not raw:raise RuntimeError('release exited before readiness')
        obj=json.loads(raw)
        if obj.get('release')!=release or type(obj.get('port')) is not int:raise ValueError('invalid readiness')
        yield child,obj['port']
    finally:
        if child.poll() is None:
            child.terminate()
            try:child.wait(timeout=2)
            except subprocess.TimeoutExpired:child.kill();child.wait(timeout=2)
        child.stdout.close();child.stderr.close()


def request(port,identity=None,delta=None):
    client=http.client.HTTPConnection('127.0.0.1',port,timeout=2)
    try:
        if identity is None:client.request('GET','/ready')
        else:
            body=json.dumps(dict(request_id=identity,delta=delta))
            client.request('POST','/op',body,{'Content-Type':'application/json'})
        response=client.getresponse();raw=response.read(4097)
        if len(raw)>4096:raise ValueError('response byte budget exhausted')
        obj=json.loads(raw)
        return response.status,obj
    finally:client.close()


def run_drill():
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);live=root/'live.db';events=[]
        with running(live) as (child,port):
            assert request(port,'A',5)[1]['result']==5
            assert request(port,'B',7)[1]['result']==12
            initial=request(port)[1];events.append(dict(stage='initial',**initial))
            create_backup(live,root/'g1')
            # Real process kill; committed state remains in this host's file/cache.
            child.kill();child.wait(timeout=2)
        with running(live,'mutant-current-response') as (_,port):
            mutant=request(port,'A',5)[1]
            assert mutant['result']==12 and mutant['result']!=5
            events.append(dict(stage='old_client_rejects_mutant',**mutant))
        with running(live) as (_,port):
            stable=request(port,'A',5)[1]
            assert stable['result']==5 and stable['duplicate']
            events.append(dict(stage='rollback_preserves_original_response',**stable))
            assert request(port,'C',4)[1]['result']==16
            try:restore_backup(root/'g1',root/'refused.db',known_receipts=[('C',4,16)])
            except ValueError:stale_refused=True
            else:raise AssertionError('stale snapshot promoted despite newer receipt')
            create_backup(live,root/'g2')
        started=time.perf_counter_ns()
        restored=restore_backup(root/'g2',root/'restored.db',known_receipts=[('A',5,5),('B',7,12),('C',4,16)])
        with running(root/'restored.db') as (_,port):
            check=request(port)[1]
            assert (check['counter'],check['operations'])==(16,3)
            assert request(port,'A',5)[1]['result']==5
            assert request(port,'C',4)[1]['result']==16
        elapsed=time.perf_counter_ns()-started
        return dict(environment=dict(python=sys.version,sqlite=sqlite3.sqlite_version,platform=platform.platform()),
                    source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('operations.py','recovery.py','telemetry.py','local_service.py','release_drill.py')},
                    actual_events=events,stale_backup_refused=stale_refused,restored=restored,
                    restore_start_through_health_and_shutdown_elapsed_ns=elapsed,
                    measured_boundary='Includes process startup, three HTTP requests and shutdown; not pure restore time or a service-wide RTO.',
                    limitations='Local trusted clients, synthetic identities, process kill only. No physical power loss, remote deployment, authentication, distributed failover or learner mastery.')


if __name__=='__main__':print(json.dumps(run_drill(),indent=2))
