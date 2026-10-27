"""Bounded supplied synthetic target. Concealment is a study convention.

No physical device is operated. Fresh calls reset the target. Open reveal only
after recording hypotheses, interventions and holdout predictions.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import sys


def number(value,name,low,high):
    if type(value) not in (int,float):raise ValueError(name+' must be numeric')
    try:result=float(value)
    except (ValueError,OverflowError):raise ValueError(name+' must be finite') from None
    if not math.isfinite(result) or not low<=result<=high:raise ValueError(name+' outside bounds')
    return result


def query(case='amber',mode='release',*,values=None,coordinate=.01,velocity=0.,drive=0.,dt=.05,samples=201,noise_bound=0.,seed=11):
    if type(case) is not str or case not in ('amber','slate','glass','copper'):raise ValueError('unknown case')
    if type(mode) is not str or mode not in ('release','calibrate','balance'):raise ValueError('unknown mode')
    coordinate=number(coordinate,'coordinate',-1,1);velocity=number(velocity,'velocity',-10,10)
    drive=number(drive,'drive',-10,10);dt=number(dt,'dt',1e-5,1)
    noise_bound=number(noise_bound,'noise_bound',0,1)
    if type(samples) is not int or not 2<=samples<=4096 or (samples-1)*dt>60:raise ValueError('bounded sample count/horizon required')
    if type(seed) is not int or not 0<=seed<2**32:raise ValueError('uint32 seed required')
    if mode=='release':
        if values is not None:raise ValueError('values only for calibration/balance')
    else:
        if type(values) not in (list,tuple) or not 2<=len(values)<=32:raise ValueError('2..32 intervention values required')
        limit=1 if mode=='calibrate' else 10
        values=[number(x,'value',-limit,limit) for x in values]
    spec=importlib.util.spec_from_file_location('_hidden_plant',Path(__file__).with_name('reveal')/'plant.py')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module.observe(case,mode,values,coordinate,velocity,drive,dt,samples,noise_bound,seed)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',default='amber');parser.add_argument('--mode',default='release')
    parser.add_argument('--values',type=float,nargs='+');parser.add_argument('--coordinate',type=float,default=.01)
    parser.add_argument('--velocity',type=float,default=0);parser.add_argument('--drive',type=float,default=0)
    parser.add_argument('--dt',type=float,default=.05);parser.add_argument('--samples',type=int,default=201)
    parser.add_argument('--noise-bound',type=float,default=0);parser.add_argument('--seed',type=int,default=11)
    try:print(json.dumps(query(**vars(parser.parse_args())),allow_nan=False))
    except ValueError as error:parser.error(str(error))
