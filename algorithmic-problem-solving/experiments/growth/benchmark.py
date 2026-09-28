"""Bounded growth demonstrations with independent operation counts and timings."""
import argparse
import bisect
import json
import platform
from pathlib import Path
import time
import tracemalloc


def naive_duplicate(values):
    comparisons=0
    for i in range(len(values)):
        for j in range(i):
            comparisons+=1
            if values[i]==values[j]: return True,comparisons
    return False,comparisons


def set_duplicate(values):
    seen=set();visits=0
    for value in values:
        visits+=1
        if value in seen:return True,visits
        seen.add(value)
    return False,visits


def tree_nodes(depth):
    if depth==0:return 1
    return 1+tree_nodes(depth-1)+tree_nodes(depth-1)


def measure(fn):
    # Separate memory instrumentation from timing to avoid conflating its overhead.
    times=[];value=None
    for _ in range(5):
        start=time.perf_counter_ns();value=fn();times.append(time.perf_counter_ns()-start)
    tracemalloc.start();fn();_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {'samples_ns':times,'peak_traced_bytes_separate_run':peak,'result':value}


def run():
    result={'kind':'agent bounded algorithm measurement; no learner evidence','python':platform.python_version(),'platform':platform.platform(),'cases':[]}
    for n in (16,64,256,1024):
        values=list(range(n)); shuffled=values[::2]+values[1::2]
        cases={
            'constant_index': lambda:values[n//2],
            'binary_search': lambda:bisect.bisect_left(values,n-1),
            'linear_sum': lambda:sum(values),
            'sort': lambda:sorted(shuffled)[-1],
            'quadratic_unique_check': lambda:naive_duplicate(values),
            'expected_linear_hash_check': lambda:set_duplicate(values),
        }
        for name,fn in cases.items():
            sample=measure(fn);sample.update(name=name,n=n,distribution='unique increasing, except sort uses even/odd interleave')
            result['cases'].append(sample)
        assert naive_duplicate(values)==(False,n*(n-1)//2)
        assert set_duplicate(values)==(False,n)
        assert naive_duplicate([1,1])[0] and set_duplicate([1,1])[0]
    for depth in (6,10,14):
        sample=measure(lambda:tree_nodes(depth));assert sample['result']==2**(depth+1)-1
        sample.update(name='exponential_recursion',n=depth,distribution='full binary recursion tree')
        result['cases'].append(sample)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    with args.output.open('x') as f:json.dump(run(),f,indent=2);f.write('\n')
    print('PASS: actual timing/memory samples and independent operation-count checks recorded')
