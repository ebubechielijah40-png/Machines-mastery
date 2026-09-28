from pid_sim import *
def run():
    xs=simulate(PID(2.0,.2,.5),steps=2000)
    assert abs(xs[-1]-1.0)<0.15
    print('pid sim: PASS')
if __name__=='__main__': run()
