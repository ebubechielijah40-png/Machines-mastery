"""Actual deterministic synthetic IVP experiments; stdout is fresh JSON."""
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
from ivp import adaptive_rk4,decay_step,integrate_fixed,oscillator_energy,oscillator_step


def pulse(t,_):
    if not .1 < t < .15:
        return (0.,)
    u=(t-.1)/.05
    return (12012/.05*u**6*(1-u)**6,)


def main():
    refinement=[]
    for method in ('euler','heun','rk4'):
        for n in (8,16,32,64):
            r=integrate_fixed(lambda t,s:(-s[0],),0,1,(1,),steps=n,method=method)
            refinement.append(dict(method=method,steps=n,h=1/n,value=r.states[-1][0],
                exact=math.exp(-1),error=abs(r.states[-1][0]-math.exp(-1)),calls=r.field_calls))
    stiff=[]
    for n in (50,200,1000):
        for implicit in (False,True):
            y=[1.,1e-6]
            for _ in range(n):
                y=[decay_step(v,k,1/n,implicit=implicit) for v,k in zip(y,(1,1000))]
            stiff.append(dict(steps=n,implicit=implicit,slow=y[0],fast=y[1],
                slow_error=abs(y[0]-math.exp(-1)),exact_fast_log_magnitude=math.log(1e-6)-1000))
    oscillation=[]
    w,h,n=2.,.05,2000
    for method in ('euler','rk4','symplectic'):
        if method=='symplectic':
            states=[(1.,0.)]
            for _ in range(n):
                states.append(oscillator_step(*states[-1],w,h))
        else:
            states=integrate_fixed(lambda t,s:(s[1],-w*w*s[0]),0,n*h,(1,0),steps=n,method=method).states
        energies=[oscillator_energy(*s,w) for s in states]
        modified=[.5*(v*v+w*w*x*x-h*w*w*x*v) for x,v in states]
        oscillation.append(dict(method=method,omega=w,h=h,steps=n,final_time=n*h,
            final_energy=energies[-1],min_energy=min(energies),max_energy=max(energies),
            position_error=abs(states[-1][0]-math.cos(w*n*h)),
            max_modified_energy_drift=max(abs(e-modified[0]) for e in modified),
            sample_times=[i*h for i in range(0,n+1,20)],energy_samples=energies[::20]))
    adaptive=[]
    for tolerance in (1e-4,1e-8,1e-12):
        r=adaptive_rk4(lambda t,s:(-5*s[0],),0,2,(1,),first_step=1,atol=tolerance,rtol=tolerance)
        adaptive.append(dict(tolerance=tolerance,accepted=r.accepted,rejected=r.rejected,calls=r.field_calls,
            final=r.states[-1][0],absolute_error=abs(r.states[-1][0]-math.exp(-10))))
    blind=adaptive_rk4(pulse,0,1,(0,),first_step=1,atol=1e-10,rtol=1e-10)
    informed=adaptive_rk4(pulse,.1,.15,(0,),first_step=.05,atol=1e-10,rtol=1e-10)
    here=Path(__file__).resolve().parent
    out=dict(schema_version=1,actual_run_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version,platform=platform.platform(),kind='Synthetic numerical models; no physical measurements',
        source_sha256={n:hashlib.sha256((here/n).read_bytes()).hexdigest() for n in ('ivp.py','test_ivp.py','experiment.py')},
        refinement=refinement,stiff=stiff,oscillation=oscillation,adaptive=adaptive,
        pulse=dict(exact_integral=1,blind_final=blind.states[-1][0],blind_calls=blind.field_calls,
            blind_accepted=blind.accepted,informed_final=informed.states[-1][0],informed_calls=informed.field_calls,
            limit='Known support supplied by the designer; no automatic feature detection.'))
    print(json.dumps(out,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
