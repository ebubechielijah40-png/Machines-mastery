from rc_lab import *
import math

def run():
    assert abs(rc_charge(5,1000,1e-6,0)-0)<1e-12
    tau=1000*1e-6
    v=rc_charge(5,1000,1e-6,tau)
    assert abs(v/5-(1-math.exp(-1)))<1e-12
    t=time_to_threshold(5,1000,1e-6,v)
    assert abs(t-tau)<1e-12
    print('rc_lab: PASS')
if __name__=='__main__': run()
