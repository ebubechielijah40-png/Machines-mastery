"""Measure local warm SQLite queries; preserve actual samples, no fixed speed claims."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import sqlite3
import statistics
import tempfile
import time
from service import Ledger


def profile(ledger, keys):
    samples=[]; answers=[]
    cpu_start=time.process_time_ns();start=time.perf_counter_ns()
    for key in keys:
        t=time.perf_counter_ns();answers.append(ledger.total(key));samples.append(time.perf_counter_ns()-t)
    elapsed=time.perf_counter_ns()-start
    ordered=sorted(samples)
    def percentile(p): return ordered[max(0,math.ceil(p*len(ordered))-1)]
    return {"samples_ns":samples,"p50_ns":percentile(.50),"p95_ns":percentile(.95),"p99_ns":percentile(.99),
            "wall_ns":elapsed,"cpu_ns":time.process_time_ns()-cpu_start,
            "throughput_calls_s":len(keys)/(elapsed/1e9),"answer_digest":hashlib.sha256(json.dumps(answers).encode()).hexdigest(),
            "metrics":ledger.metrics.copy()}


def run(sizes):
    result={"kind":"agent artifact benchmark, not learner experiment", "environment":{"python":platform.python_version(),"platform":platform.platform(),"sqlite":sqlite3.sqlite_version},
            "method":"three trials; deterministic 100 hot-key requests, one process, warm OS cache; no network", "datasets":[]}
    keys=[i%10 for i in range(100)]
    for n in sizes:
        with tempfile.TemporaryDirectory(prefix="mm-ledger-") as temp:
            path=Path(temp)/"events.db";ledger=Ledger(path)
            t=time.perf_counter_ns()
            with ledger.db:
                ledger.db.executemany("INSERT INTO events VALUES (?,?,?)", ((i,i%1000,(i%11)-5) for i in range(n)))
            insert_ns=time.perf_counter_ns()-t
            entry={"rows":n,"insert_ns":insert_ns,"bytes_before_index":path.stat().st_size,"stages":{}}
            def measure(stage):
                ledger.cache.clear();ledger.metrics={k:0 for k in ledger.metrics}
                entry['stages'][stage]=[profile(ledger,keys) for _ in range(3)]
            entry['plan_before']=ledger.db.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM events WHERE account=?",(0,)).fetchall()
            measure('scan')
            t=time.perf_counter_ns();ledger.add_index();entry['index_build_ns']=time.perf_counter_ns()-t
            entry['bytes_after_index']=path.stat().st_size
            entry['plan_after']=ledger.db.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM events WHERE account=?",(0,)).fetchall()
            measure('index')
            ledger.capacity=16;measure('bounded_cache')
            digests={trial['answer_digest'] for trials in entry['stages'].values() for trial in trials}
            if len(digests)!=1: raise AssertionError('performance change altered answers')
            entry['process_maxrss_kib_linux']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            ledger.close();result['datasets'].append(entry)
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--rows',type=int,nargs='+',default=[1000,100000,1000000]);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if any(n<=0 or n>2000000 for n in args.rows): parser.error('rows must be 1..2000000 for this bounded lab')
    data=run(args.rows)
    with args.output.open('x') as f: json.dump(data,f,indent=2);f.write('\n')
    for e in data['datasets']:
        print(e['rows'],{stage:round(statistics.median(x['p50_ns'] for x in trials)/1000,2) for stage,trials in e['stages'].items()},'median trial p50 microseconds')
