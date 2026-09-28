from __future__ import annotations

def predict(w,b,x): return w*x+b

def mse(w,b,xs,ys):
    if len(xs)!=len(ys) or not xs: raise ValueError
    return sum((predict(w,b,x)-y)**2 for x,y in zip(xs,ys))/len(xs)

def gradients(w,b,xs,ys):
    n=len(xs)
    if n!=len(ys) or not n: raise ValueError
    dw=sum(2*(predict(w,b,x)-y)*x for x,y in zip(xs,ys))/n
    db=sum(2*(predict(w,b,x)-y) for x,y in zip(xs,ys))/n
    return dw,db

def fit(xs,ys,lr=0.01,steps=1000):
    w=b=0.0
    for _ in range(steps):
        dw,db=gradients(w,b,xs,ys); w-=lr*dw; b-=lr*db
    return w,b
