"""Separate-reader hand-derived finite decision probes, no model data required."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
UNIT=ROOT/'foundations/statistics/probability-inference'
sys.path.insert(0,str(UNIT))
from decision import UpperTest,minimum_n,monitor_upper,rejection_probability,upper_test
from probability import coverage,wald


def main():
    # For three trials P(K>=2)=3p²(1-p)+p³. This polynomial is independent
    # of the author's binomial-tail and active-state recurrence implementations.
    rule=upper_test(3,Q(1,10),Q(3,100))
    assert rule.critical==2 and rule.size==Q(7,250)
    assert rejection_probability(rule,Q(3,10))==Q(27,125)
    assert rejection_probability(rule,Q(1,20))==Q(29,4000)
    # An all-one alternative is detected once the smallest nonempty null event
    # 2^-n can fit alpha. For alpha=1/20 that first occurs at n=5.
    plan=minimum_n(Q(1,2),Q(1),alpha=Q(1,20),target_power=Q(1),max_n=10)
    assert plan.selected.n==5 and all(x.power==0 for x in plan.evaluated[:-1])
    assert plan.evaluated[-1].power==1
    # Union(first five ones, K8>=7): their overlap has mass1/64.
    union=Q(1,32)+Q(9,256)-Q(1,64)
    repeat=monitor_upper(8,policy='repeat')
    final=monitor_upper(8,policy='final')
    spend=monitor_upper(8,policy='spend')
    assert repeat.rejection_probability==union==Q(13,256)
    assert final.rejection_probability==Q(9,256)
    assert spend.rejection_probability==Q(1,256)
    assert repeat.first_crossing[4]==Q(1,32) and repeat.first_crossing[7]==Q(5,256)
    assert repeat.survival[-1]==Q(243,256)
    tiny=Q(1,2**1100)
    assert coverage(1,tiny,wald)==0 and coverage(1,1-tiny,wald)==0
    try:UpperTest(5,Q(1,2),Q(1,20),-1,Q(0))
    except ValueError:rejected_negative=True
    else:raise AssertionError('negative threshold silently changes tail selection')
    result={'status':'PASS','three_trial_size':str(rule.size),'three_trial_power_p03':str(Q(27,125)),
            'minimum_n_all_one_alternative':plan.selected.n,
            'eight_look':{p:str(x.rejection_probability) for p,x in [('repeat',repeat),('final',final),('spend',spend)]},
            'independent_union_probability':str(union),'negative_threshold_rejected':rejected_negative,
            'interior_tiny_probability_wald_coverage':'0 for both p and1-p',
            'reviewed_sha256':{name:hashlib.sha256((UNIT/name).read_bytes()).hexdigest() for name in
                ('decision.py','DECISION_DESIGN.md','DECISION_SOLUTIONS.md')},
            'limits':'Separate team reader of selected finite contracts; no physical process, causal inference or universal sequential testing claim.'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
