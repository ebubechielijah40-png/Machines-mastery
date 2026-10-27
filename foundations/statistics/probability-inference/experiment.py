"""Execute finite coverage and sampling-model counterexamples; no real observations."""
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
import json
from pathlib import Path
import platform
import random
import sys

from probability import binomial,coverage,posterior,permutation_test,wald,wilson


def run():
    intervals=[]
    for n in [5,20,100]:
        for p in [F(1,50),F(1,5),F(1,2)]:
            row={'n':n,'true_p':str(p)}
            for name,interval in [('wald',wald),('wilson',wilson)]:
                exact=coverage(n,p,interval)
                model=binomial(n,p)
                mean_width=sum(float(mass)*(interval(k,n)[1]-interval(k,n)[0])
                               for k,mass in model.masses.items())
                row[name]={'coverage_fraction':str(exact),'coverage_float':float(exact),
                           'expected_width_float':mean_width}
            intervals.append(row)
    # Same marginal p=.2 for every apparent observation; only dependence changes.
    seed=7241;rng=random.Random(seed);n=20;replicates=4000;target=F(1,5)
    counts={'iid':0,'one_bit_copied_20_times':0}
    for _ in range(replicates):
        independent=sum(rng.random()<float(target) for _ in range(n))
        copied=n*int(rng.random()<float(target))
        for key,k in [('iid',independent),('one_bit_copied_20_times',copied)]:
            lo,hi=wilson(k,n)
            counts[key]+=lo<=float(target)<=hi
    groups=permutation_test([0,0],[1,1])
    return {'schema_version':1,'kind':'executed synthetic finite-model experiments',
            'executed_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'platform':platform.platform(),
            'coverage_enumeration':intervals,
            'fault_model':{'prior':'1/100','sensitivity':'9/10','false_positive':'1/50',
                           'posterior':str(posterior(F(1,100),F(9,10),F(1,50)))},
            'zero_failures_n5':{'wald':wald(0,5),'wilson':wilson(0,5)},
            'permutation_four_positions':{k:str(v) if isinstance(v,F) else v for k,v in groups.items()},
            'dependence_counterexample':{'seed':seed,'replicates':replicates,'n':n,'marginal_p':str(target),
                 'interval':'Wilson nominal95%, incorrectly treating copied observations as iid',
                 'covered_counts':counts,
                 'empirical_coverage':{k:v/replicates for k,v in counts.items()},
                 'exact_iid_coverage':str(coverage(n,target)),
                 'exact_copied_coverage':0},
            'limits':['All data are synthetic; no detector, factory or human observations.',
                      'Exact masses do not make normal-score coverage uniformly95%.',
                      'Float interval endpoints may affect inclusion near a boundary.',
                      'One seed and4000 replicates illustrate dependence, not a general empirical theorem.',
                      'Python pseudorandomness is adequate for this reproducible simulation, not a secure RNG.']}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(run(),indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding='utf-8')
    else:
        print(result,end='')
