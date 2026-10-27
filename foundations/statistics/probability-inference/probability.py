"""Finite probability and declared binomial interval mechanisms.

Exact finite masses use Fraction; interval endpoints are floating-point normal
approximations. No claim of universal95% coverage or causal identification.
"""
from fractions import Fraction
import itertools
import math
from types import MappingProxyType


def probability(p):
    if isinstance(p,bool):raise ValueError('bool is not a probability parameter')
    try:p=Fraction(p)
    except (ValueError,TypeError,OverflowError,ZeroDivisionError) as exc:
        raise ValueError('expected a finite rational probability') from exc
    if not 0<=p<=1:raise ValueError('probability must lie in [0,1]')
    return p


class FiniteDistribution:
    def __init__(self,masses):
        self.masses=MappingProxyType({outcome:probability(p) for outcome,p in masses.items()})
        if not self.masses or sum(self.masses.values(),Fraction())!=1:
            raise ValueError('nonempty masses must sum exactly to one')

    def event(self,predicate):
        return sum((p for outcome,p in self.masses.items() if predicate(outcome)),Fraction())

    def condition(self,predicate):
        selected={x:p for x,p in self.masses.items() if predicate(x)}
        mass=sum(selected.values(),Fraction())
        if mass==0:raise ValueError('cannot condition on zero-probability event')
        return FiniteDistribution({x:p/mass for x,p in selected.items()})

    def expectation(self,value=lambda x:x):
        return sum((Fraction(value(x))*p for x,p in self.masses.items()),Fraction())

    def variance(self,value=lambda x:x):
        mean=self.expectation(value)
        return self.expectation(lambda x:(Fraction(value(x))-mean)**2)

    def entropy_bits(self):
        # Taking log2(float(p)) would fail if a positive rational underflowed
        # to float zero. Log the integer numerator/denominator separately.
        return -math.fsum(float(p)*(math.log2(p.numerator)-math.log2(p.denominator))
                          for p in self.masses.values() if p)


def posterior(prior,sensitivity,false_positive):
    p,s,f=map(probability,(prior,sensitivity,false_positive))
    evidence=p*s+(1-p)*f
    if evidence==0:raise ValueError('observed event has zero model probability')
    return p*s/evidence


def binomial(n,p):
    if type(n) is not int or not 0<=n<=1000:
        raise ValueError('n must be an integer between0 and1000')
    p=probability(p)
    return FiniteDistribution({k:Fraction(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)})


def _counts(k,n,z):
    if type(k) is not int or type(n) is not int or not 0<=k<=n or not 1<=n<=10**9:
        raise ValueError('need integer 0<=k<=n with 1<=n<=10**9')
    if isinstance(z,bool) or not isinstance(z,(float,int)) or not .01<=z<=10:
        raise ValueError('finite normal quantile .01<=z<=10 required by this float lab')


def wilson(k,n,z=1.959963984540054):
    """Normal-score inversion, not a guaranteed exact-coverage interval.

    Bound n and z to the declared teaching range; finite rational probabilities
    elsewhere do not make these floating-point endpoints exact.
    """
    _counts(k,n,z)
    p=k/n;weight=z/math.sqrt(n);scaled_square=weight*weight
    denominator=1+scaled_square
    center=(p+scaled_square/2)/denominator
    radius=weight*math.sqrt(p*(1-p)+scaled_square/4)/denominator
    # These endpoints follow exactly from the score inequality. Rounding the
    # formula can otherwise exclude p=1 when every outcome is a success.
    return (0. if k==0 else max(0.,center-radius),
            1. if k==n else min(1.,center+radius))


def wald(k,n,z=1.959963984540054):
    """Intentionally weak comparison interval; endpoints clipped for this lab."""
    _counts(k,n,z)
    p=k/n;radius=z*math.sqrt(p*(1-p)/n)
    return max(0.,p-radius),min(1.,p+radius)


def coverage(n,p,interval=wilson):
    """Enumerate finite sample counts, rather than claiming a simulation proves coverage."""
    model=binomial(n,p);target=probability(p)
    return model.event(lambda k:interval(k,n)[0]<=target<=interval(k,n)[1])


def exact_upper_tail(k,n,p):
    _counts(k,n,1.)
    return binomial(n,p).event(lambda observed:observed>=k)


def permutation_test(group_a,group_b):
    """Exact two-sided difference-of-means randomization over labeled positions.

    Requires exchangeable labels under a specified null; not a causal guarantee.
    Limited to16 observations to bound combinatorial enumeration.
    """
    a,b=list(map(Fraction,group_a)),list(map(Fraction,group_b))
    if not a or not b or len(a)+len(b)>16:
        raise ValueError('two nonempty groups with total size<=16 required')
    data=a+b;k=len(a);n=len(data)
    total=sum(data,Fraction())
    observed=abs(sum(a,Fraction())/k-sum(b,Fraction())/(n-k))
    extreme=count=0
    for indices in itertools.combinations(range(n),k):
        left=sum((data[i] for i in indices),Fraction())
        statistic=abs(left/k-(total-left)/(n-k))
        count+=1;extreme+=statistic>=observed
    return {'absolute_difference':observed,'p_value':Fraction(extreme,count),'assignments':count}
