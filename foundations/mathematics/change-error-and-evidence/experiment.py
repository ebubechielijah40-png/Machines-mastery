"""Emit reproducible synthetic evidence to stdout; no physical observations."""
import json
import math
import platform
import sys
from dataclasses import asdict
from numerics import difference, summarize, speed_uncertainty


def main():
    rows=[]
    for exponent in range(1,19):
        h=10.0**-exponent
        row={'h':h}
        for method in ['forward','central']:
            try:
                estimate=difference(lambda x:x*x*x,1,h,method)
                row[method]={'estimate':estimate,'absolute_error':abs(estimate-3)}
            except ValueError as exc:
                row[method]={'rejected':str(exc)}
        rows.append(row)
    noise=[-.02,0,.02,0]
    base=[1+x for x in noise]
    biased=[x+.1 for x in base]
    # Repeated blocks are deliberately correlated, not independent samples.
    pseudoreplication=[x for x in base for _ in range(100)]
    shifted=[1e9+i for i in [1,2,3,4]]
    naive=(sum(x*x for x in shifted)-sum(shifted)**2/len(shifted))/(len(shifted)-1)
    print(json.dumps({'environment':{'python':sys.version,'platform':platform.platform()},
        'kind':'synthetic deterministic mechanism experiment',
        'derivative_cubic_at_one':rows,
        'base':asdict(summarize(base)), 'bias_added':asdict(summarize(biased)),
        'copied_records_not_independent':asdict(summarize(pseudoreplication)),
        'large_offset_variance':{'naive':naive,'two_pass':asdict(summarize(shifted))},
        'speed':dict(zip(['estimate','standard_uncertainty'],speed_uncertainty(10,2,.1,.02)))}, indent=2))


if __name__ == '__main__': main()
