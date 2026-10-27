"""Finite repeated-search work and wrong-loop counterexamples; no timing ranking."""
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import platform
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parent/'code'))
import dp


def search(target, memoize):
    calls = 0
    def visit(amount):
        nonlocal calls
        calls += 1
        if amount == 0:
            return 0
        return 1 + min(recur(amount-c) for c in (1,3,4) if c <= amount)
    recur = lru_cache(None)(visit) if memoize else visit
    begin = time.perf_counter()
    value = recur(target)
    return dict(optimum=value, evaluated_states_or_calls=calls,
                elapsed_seconds=time.perf_counter()-begin)


def main():
    runs=[]
    for amount in (4,8,12,16,20):
        naive, memo = search(amount,False), search(amount,True)
        witness = dp.min_coins([1,3,4],amount)
        assert naive['optimum'] == memo['optimum'] == len(witness)
        assert sum(witness) == amount
        runs.append(dict(target=amount,naive=naive,memoized=memo,reference_witness=witness))
    ordered=[1,0,0,0]
    for amount in range(1,4):
        for coin in (1,2):
            if coin <= amount: ordered[amount] += ordered[amount-coin]
    bad_knapsack=[0]*5
    for capacity in range(2,5):
        bad_knapsack[capacity]=max(bad_knapsack[capacity],3+bad_knapsack[capacity-2])
    bad_route=[0,None,None]
    for u,v,w in [(0,1,2),(1,2,-5)]:
        if bad_route[u] is not None: bad_route[v]=bad_route[u]+w
    return {'observed_at_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'platform':platform.platform(),
            'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                      [Path(__file__),Path(dp.__file__)]},
            'runs':runs,
            'counterexamples':{
                'ordered_instead_of_unordered':{'wrong':ordered[3],'correct':dp.coin_combinations([1,2],3)},
                'ascending_01_capacity':{'wrong':bad_knapsack[4],'correct':dp.knapsack([2],[3],4)[0]},
                'same_layer_hop_relaxation':{'wrong':bad_route[2],'correct':dp.bounded_route(3,[(0,1,2),(1,2,-5)],0,2,1)}},
            'limits':'Fixed finite CPU work observations; no benchmark ranking or learner mastery evidence.'}


if __name__=='__main__':print(json.dumps(main(),indent=2))
