from stats_lab import *
def run():
    assert mean([1,2,3])==2
    assert abs(variance([1,2,3])-1)<1e-12
    lo,hi=bootstrap_mean_ci([1,2,3,4,5],500,2); assert lo<=3<=hi
    print('stats lab: PASS')
if __name__=='__main__': run()
