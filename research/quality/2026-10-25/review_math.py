"""Separate-reader probes; formulas differ from author test structures."""
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
UNIT=ROOT/'foundations/mathematics/initial-value-evidence'
spec=importlib.util.spec_from_file_location('reviewed_ivp',UNIT/'ivp.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)


def mul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(2)),Q(0)) for j in range(2)] for i in range(2)]


def main():
    checks=0
    for w in map(Q,('1/2','1','2','3')):
        for h in map(Q,('1/8','1/4','1/2','1')):
            a=[[1-h*h*w*w,h],[-h*w*w,Q(1)]]
            metric=[[w*w,-h*w*w/2],[-h*w*w/2,Q(1)]]
            transpose=[list(x) for x in zip(*a)]
            assert mul(mul(transpose,metric),a)==metric
            checks+=1
    result=m.adaptive_rk4(lambda t,y:(1+y[0]*y[0],),0,.7,(0,),first_step=.5,atol=1e-11,rtol=1e-11)
    nonlinear_error=abs(result.states[-1][0]-math.tan(.7))
    assert nonlinear_error<1e-8
    calls=[]
    def counted(t,y):
        calls.append(t);return(1.,)
    try:m.adaptive_rk4(counted,0,1,(0,),first_step=1,max_calls=11)
    except m.ContractError:pass
    else:raise AssertionError('budget should fail')
    assert len(calls)==11
    a,b=.12,.14
    def pulse(t,y):
        if not a<t<b:return(0.,)
        u=(t-a)/(b-a)
        return(12012*u**6*(1-u)**6/(b-a),)
    integral=Q(math.factorial(6)**2,math.factorial(13))*12012
    assert integral==1
    blind=m.adaptive_rk4(pulse,0,1,(0,),first_step=1,atol=1e-10,rtol=1e-10)
    informed=m.adaptive_rk4(pulse,a,b,(0,),first_step=b-a,atol=1e-10,rtol=1e-10)
    assert blind.states[-1][0]==0 and blind.field_calls==12
    assert abs(informed.states[-1][0]-1)<1e-7
    out={'status':'PASS','independent_fraction_metric_identities':checks,
         'nonlinear_tangent_oracle_error':nonlinear_error,'nonlinear_calls':result.field_calls,
         'budget11_actual_calls':len(calls),'different_support':[a,b],
         'pulse_exact_integral':str(integral),'blind':blind.states[-1][0],
         'informed':informed.states[-1][0],
         'reviewed_sha256':{n:hashlib.sha256((UNIT/n).read_bytes()).hexdigest() for n in ('ivp.py','README.md','SOLUTIONS.md')},
         'limits':'Separate team reader; selected mechanism probes, not universal solver correctness or specialist accreditation.'}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
