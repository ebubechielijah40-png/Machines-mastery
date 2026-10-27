"""Exact synthetic operating curves and stopping investigations; no RNG/data.

Default writes JSON to stdout. --output refuses to replace earlier observations.
"""
import argparse
from dataclasses import asdict,is_dataclass
from datetime import datetime,timezone
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import sys
from decision import minimum_n,monitor_upper,rejection_probability,upper_test


def portable(value):
    if isinstance(value,Q):
        return {'numerator':value.numerator,'denominator':value.denominator,'decimal':float(value)}
    if is_dataclass(value):
        return portable(asdict(value))
    if isinstance(value,dict):
        return {k:portable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [portable(v) for v in value]
    return value


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    if args.output and args.output.exists():
        ap.error('preserve earlier evidence: choose a new output path')
    p0,alpha=Q(1,2),Q(1,20)
    curves=[]
    for n in (5,6,10,20,40,80):
        test=upper_test(n,p0,alpha)
        curves.append({'test':test,'operating_curve':[
            {'actual_p':p,'rejection_probability':rejection_probability(test,p)}
            for p in (Q(0),Q(1,4),p0,Q(3,5),Q(7,10),Q(4,5),Q(1))]})
    plans=[minimum_n(p0,p1,alpha=alpha,target_power=Q(4,5),max_n=200)
           for p1 in (Q(3,5),Q(7,10),Q(4,5))]
    stopping=[]
    for horizon in (10,20,50,100):
        for policy in ('final','repeat','spend'):
            record=monitor_upper(horizon,p0,alpha=alpha,policy=policy)
            stopping.append({'monitor':record,'ever_rejected':record.rejection_probability,
                             'conservation':record.rejection_probability+record.survival[-1]})
    here=Path(__file__).resolve().parent
    output={'schema_version':1,'actual_run_utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version,'platform':platform.platform(),
        'kind':'Exact synthetic iid Bernoulli model enumeration; no physical observations or Monte Carlo estimates',
        'source_sha256':{name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in
                         ('probability.py','test_probability.py','decision.py','test_decision.py','decision_experiment.py')},
        'null_p':p0,'alpha':alpha,'operating_curves':curves,'sample_plans':plans,'monitoring':stopping,
        'limits':['Power is conditional on the declared alternative and iid model.',
                  'Exact arithmetic does not establish a physical sampling process.',
                  'Bounded minimum-n search is only within the declared upper bound.',
                  'Alpha spending is predeclared; overlap between looks is not treated as independence.']}
    text=json.dumps(portable(output),indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        # x mode also protects against a race between the earlier check and open.
        with args.output.open('x') as stream:
            stream.write(text)
    else:
        print(text,end='')


if __name__=='__main__':
    main()
