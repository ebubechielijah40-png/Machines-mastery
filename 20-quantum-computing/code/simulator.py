"""Tiny ideal statevector simulator for learning only."""
from __future__ import annotations
import cmath, math, random

SQRT2=math.sqrt(2)
X=((0j,1+0j),(1+0j,0j))
Z=((1+0j,0j),(0j,-1+0j))
H=((1/SQRT2,1/SQRT2),(1/SQRT2,-1/SQRT2))

class State:
    def __init__(self,n:int):
        if n<1: raise ValueError('n>=1')
        self.n=n; self.amp=[0j]*(1<<n); self.amp[0]=1+0j
    def apply1(self,q:int,u):
        if not 0<=q<self.n: raise IndexError(q)
        step=1<<q
        for base in range(0,1<<self.n,step*2):
            for off in range(step):
                i=base+off; j=i+step; a,b=self.amp[i],self.amp[j]
                self.amp[i]=u[0][0]*a+u[0][1]*b
                self.amp[j]=u[1][0]*a+u[1][1]*b
        return self
    def cnot(self,control:int,target:int):
        if control==target: raise ValueError('control != target')
        for i in range(1<<self.n):
            if (i>>control)&1 and not ((i>>target)&1):
                j=i|(1<<target); self.amp[i],self.amp[j]=self.amp[j],self.amp[i]
        return self
    def probs(self):
        return [abs(a)**2 for a in self.amp]
    def norm(self):
        return sum(self.probs())
    def sample(self,shots=1,seed=0):
        rng=random.Random(seed); p=self.probs(); out=[]
        for _ in range(shots):
            r=rng.random(); c=0.0
            for i,x in enumerate(p):
                c+=x
                if r<=c+1e-15: out.append(i); break
        return out
