"""Actually run bounded host work; all timings belong to this synthetic workload."""
from collections import Counter
from dataclasses import asdict
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import select
import sqlite3
import subprocess
import sys
import tempfile
import time
from operations import BoundedService, OperationStore, UnknownOutcome, evaluate

BASE = Path(__file__).resolve().parent

def load_case(directory, label, delay_ms, interval_ms):
    store = OperationStore(directory / (label + '.db'))
    start = time.perf_counter_ns()
    cpu = time.process_time_ns()
    futures = []
    with BoundedService(store, workers=2, capacity=6, deadline_ms=30) as service:
        for i in range(40):
            planned = start + i * interval_ms * 1_000_000
            remaining = planned - time.perf_counter_ns()
            if remaining > 0:
                time.sleep(remaining / 1e9)
            futures.append(service.submit(str(i), 1, issued_ns=planned, delay_ms=delay_ms))
        records = [f.result(timeout=5) for f in futures]
    elapsed = time.perf_counter_ns() - start
    assert len(records) == len(service.records) == service.offered == 40
    state = store.snapshot()
    assert state['counter'] == sum(r.status == 'ok' for r in records)
    return dict(label=label, controlled=dict(count=40, workers=2, running_plus_waiting_capacity=6,
               injected_processing_delay_ms=delay_ms, planned_arrival_interval_ms=interval_ms, good_deadline_ms=30),
               measurement=dict(wall_ms=elapsed / 1e6, process_cpu_ms=(time.process_time_ns()-cpu)/1e6,
                                completions_per_wall_second=40/(elapsed/1e9)),
               sli=evaluate(records, 30_000_000), state=state,
               observations=[{**asdict(r), 'issued_ns':r.issued_ns-start, 'offered_ns':r.offered_ns-start,
                              'started_ns':r.started_ns-start, 'ended_ns':r.ended_ns-start} for r in records])


def crash_case(directory, phase):
    path = directory / (phase + '.db')
    child = subprocess.Popen([sys.executable, str(BASE/'crash_child.py'), str(path), phase],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        ready, _, _ = select.select([child.stdout], [], [], 5)
        if not ready:
            raise RuntimeError('child did not reach controlled phase')
        observed_phase = child.stdout.readline().strip()
        if observed_phase != phase:
            raise RuntimeError('child exited before controlled phase: ' + observed_phase)
        child.kill()
        _, stderr = child.communicate(timeout=5)
    finally:
        if child.poll() is None:
            child.kill(); child.wait(timeout=5)
    fresh = OperationStore(path)
    before_retry = fresh.snapshot()
    reply = fresh.apply('crash-operation', 7)
    after_retry = fresh.snapshot()
    assert before_retry['counter'] == (0 if phase=='before_commit' else 7)
    assert reply == (7, phase=='after_commit')
    assert after_retry['counter'] == 7
    return dict(fault='actual directly spawned application-process kill', observed_phase=observed_phase,
                child_exit=child.returncode, stderr=stderr, before_retry=before_retry,
                retry_reply=list(reply), after_retry=after_retry,
                limitation='Not an OS crash, power cut, damaged filesystem or storage-device test.')


def run():
    with tempfile.TemporaryDirectory(prefix='mm-operation-') as tmp:
        directory = Path(tmp)
        cases = [load_case(directory, 'light', 1, 4),
                 load_case(directory, 'slow_dependency', 12, 4),
                 load_case(directory, 'paced_slow_dependency', 12, 8)]
        crashes = [crash_case(directory, phase) for phase in ('before_commit', 'after_commit')] if os.name=='posix' else [{'status':'BLOCKED','reason':'POSIX selectable child pipes required for this controlled coordinator'}]
    return dict(observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                environment=dict(python=sys.version, platform=platform.platform(),sqlite=sqlite3.sqlite_version,
                                 perf_counter=vars(time.get_clock_info('perf_counter'))),
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [BASE/'operations.py',BASE/'experiment.py',BASE/'crash_child.py']},
                scope='Actual local finite threaded workloads and controlled process crashes. No public endpoint, production traffic, SLA or physical power-failure guarantee.',
                cases=cases, crash_cases=crashes)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
