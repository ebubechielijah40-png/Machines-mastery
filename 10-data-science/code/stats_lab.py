import math, random

def mean(xs):
    if not xs: raise ValueError
    return sum(xs)/len(xs)
def variance(xs):
    if len(xs)<2: raise ValueError
    m=mean(xs); return sum((x-m)**2 for x in xs)/(len(xs)-1)
def bootstrap_mean_ci(xs,reps=2000,seed=1,alpha=.05):
    if not xs: raise ValueError
    rng=random.Random(seed); n=len(xs); vals=[]
    for _ in range(reps): vals.append(mean([xs[rng.randrange(n)] for __ in range(n)]))
    vals.sort(); lo=int((alpha/2)*reps); hi=min(reps-1,int((1-alpha/2)*reps)-1)
    return vals[lo],vals[hi]
