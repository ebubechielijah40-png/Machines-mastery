"""Original synthetic targets. No empirical physical parameters are claimed."""
import math
import random

# inertia, loss, stiffness, detector gain, detector offset, interpretation
CASES={'amber':(2.,.8,18.,1000.,25.,'mechanical'),
       'slate':(.75,.3,6.75,700.,-12.,'mechanical'),
       'glass':(2.,.8,18.,1000.,25.,'electrical'),
       'copper':(1.25,1.,5.,-400.,10.,'electrical')}


def observe(case,mode,values,coordinate,velocity,drive,dt,samples,noise_bound,seed):
    a,b,c,g,o,_=CASES[case];rng=random.Random(seed)
    def reading(q):return o+g*q+rng.uniform(-noise_bound,noise_bound)
    if mode=='calibrate':return dict(mode=mode,coordinates=values,readings=[reading(q) for q in values])
    if mode=='balance':return dict(mode=mode,drives=values,readings=[reading(u/c) for u in values])
    alpha=b/(2*a);omega=math.sqrt(c/a-alpha*alpha);equilibrium=drive/c
    cosine=coordinate-equilibrium;sine=(velocity+alpha*cosine)/omega
    return dict(mode=mode,dt=dt,readings=[reading(equilibrium+math.exp(-alpha*i*dt)*(cosine*math.cos(omega*i*dt)+sine*math.sin(omega*i*dt))) for i in range(samples)])
