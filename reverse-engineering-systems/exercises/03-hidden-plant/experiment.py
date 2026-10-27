"""Run a controlled synthetic investigation; print raw observations as JSON."""
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
from oracle import query
from reconstruction import Calibration,Model,calibrate,stiffness,fit_free,model_from_fit

HERE=Path(__file__).resolve().parent


def identify(case,dt=.05,noise=0.,seed=11):
    calibration=query(case,'calibrate',values=[-.02,.02])
    cal=calibrate(calibration['coordinates'][0],calibration['readings'][0],calibration['coordinates'][1],calibration['readings'][1])
    balance=query(case,'balance',values=[-.3,.6])
    k=stiffness(balance['drives'][0],balance['readings'][0],balance['drives'][1],balance['readings'][1],cal)
    release=query(case,dt=dt,samples=round(10/dt)+1,noise_bound=noise,seed=seed)
    fit=fit_free([cal.coordinate(y) for y in release['readings']],dt)
    model=model_from_fit(fit,k)
    holdout=query(case,coordinate=-.013,velocity=.027,drive=.31,dt=.037,samples=101)
    errors=[cal.coordinate(y)-model.response(i*.037,-.013,.027,.31) for i,y in enumerate(holdout['readings'])]
    return dict(calibration=asdict(cal),model=asdict(model),fit=asdict(fit),
                holdout_max_absolute_error=max(map(abs,errors)),
                release=release,holdout=holdout,balance=balance)


def run():
    clean={case:identify(case) for case in ('amber','slate','glass','copper')}
    noisy=[]
    for dt in (.2,.05,.005):
        for seed in (11,17):
            row=dict(dt=dt,samples=round(10/dt)+1,horizon_seconds=10,noise_bound_counts=.2,seed=seed)
            try:
                fitted=identify('amber',dt,.2,seed)
                row.update(status='fit',model=fitted['model'],fit=fitted['fit'],holdout_max_absolute_error=fitted['holdout_max_absolute_error'])
            except ValueError as error:row.update(status='refused',reason=str(error))
            noisy.append(row)
    alpha,omega,h=.2,3.,.2;k=18
    def alias_model(w):
        m=k/(alpha*alpha+w*w);return Model(m,2*alpha*m,k)
    low,high=alias_model(omega),alias_model(omega+2*math.pi/h)
    alias=dict(low_frequency=omega,high_frequency=omega+2*math.pi/h,dt=h,
               grid_max_absolute_difference=max(abs(low.response(i*h,.01,-alpha*.01)-high.response(i*h,.01,-alpha*.01)) for i in range(41)),
               off_grid_time=.071,off_grid_absolute_difference=abs(low.response(.071,.01,-alpha*.01)-high.response(.071,.01,-alpha*.01)))
    a,b=Model(2,.8,18),Model(6,2.4,54)
    scale=dict(free_max_difference=max(abs(a.response(i*.1,.01)-b.response(i*.1,.01)) for i in range(100)),
               forced_at_one_second=[a.response(1,0,0,1),b.response(1,0,0,1)])
    original=clean['amber'];wrong=Calibration(original['calibration']['gain'],0)
    release=original['release']
    try:
        fit=fit_free([wrong.coordinate(y) for y in release['readings']],.05)
        bad=model_from_fit(fit,18)
        offset=dict(status='fit',model=asdict(bad),fit=asdict(fit),
                    holdout_max_absolute_error=max(abs((y-original['calibration']['offset'])/original['calibration']['gain']-bad.response(i*.037,-.013,.027,.31)) for i,y in enumerate(original['holdout']['readings'])))
    except ValueError as error:offset=dict(status='refused',reason=str(error))
    return dict(environment=dict(python=sys.version,platform=platform.platform()),
                source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('oracle.py','reconstruction.py','reveal/plant.py','experiment.py','test_plant.py')},
                clean=clean,noise_interval_investigation=noisy,alias_counterexample=alias,
                coefficient_scale_counterexample=scale,omitted_offset=offset,
                equal_port_observations_amber_glass=clean['amber']['release']==clean['glass']['release'],
                limitations='Executed software observations of supplied synthetic systems; no physical apparatus, empirical noise law, confidence guarantee or unique internal topology.')


if __name__=='__main__':print(json.dumps(run(),indent=2,allow_nan=False))
