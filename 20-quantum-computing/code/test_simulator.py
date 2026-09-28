from simulator import *

def approx(a,b,e=1e-10): return abs(a-b)<e

def run():
    s=State(1); s.apply1(0,H); assert all(approx(x,.5) for x in s.probs())
    s.apply1(0,H); assert approx(s.probs()[0],1.0)
    t=State(1); t.apply1(0,H).apply1(0,Z).apply1(0,H); assert approx(t.probs()[1],1.0)
    b=State(2); b.apply1(0,H).cnot(0,1); p=b.probs(); assert approx(p[0],.5) and approx(p[3],.5) and approx(p[1],0) and approx(p[2],0)
    assert approx(b.norm(),1.0)
    print('quantum simulator: PASS')
if __name__=='__main__': run()
