from linear_model import *
def run():
    xs=[-2,-1,0,1,2]; ys=[2*x+1 for x in xs]
    w,b=fit(xs,ys,0.05,500)
    assert abs(w-2)<1e-3 and abs(b-1)<1e-3
    assert mse(w,b,xs,ys)<1e-5
    print('linear model: PASS')
if __name__=='__main__': run()
