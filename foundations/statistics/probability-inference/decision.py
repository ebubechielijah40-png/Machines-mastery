"""Exact bounded upper-binomial decisions and first-crossing probability DP.

This is a finite instructional model, not a trial-design recommendation. Trials
are iid Bernoulli, direction and policy are declared in advance. See lesson.
"""
from dataclasses import dataclass
from fractions import Fraction
from probability import binomial, probability

MAX_N = 200
MAX_RATIONAL_BITS = 64


def _count(n, name='n', *, zero=False):
    if type(n) is not int or not (0 if zero else 1) <= n <= MAX_N:
        raise ValueError(f'{name} must be an integer in {0 if zero else 1}..{MAX_N}')
    return n


def _p(value):
    p = probability(value)
    if max(p.numerator.bit_length(), p.denominator.bit_length()) > MAX_RATIONAL_BITS:
        raise ValueError('probability exceeds64-bit rational-input budget')
    return p


def _tails(n, p):
    masses = binomial(n, p).masses
    tails = [Fraction(0)] * (n + 2)
    for k in range(n, -1, -1):
        tails[k] = tails[k+1] + masses[k]
    return tuple(tails)


@dataclass(frozen=True)
class UpperTest:
    """Validated numeric record; only upper_test establishes its calibration.

    A manually supplied size is not a certificate that the threshold has that
    rejection probability. The factory derives both from exact null masses.
    """
    n: int
    p0: Fraction
    alpha: Fraction
    critical: int  # n+1 means never reject;0 means always reject
    size: Fraction

    def __post_init__(self):
        _count(self.n)
        p0, alpha = _p(self.p0), _p(self.alpha)
        # A derived tail can have far more bits than the bounded public input.
        size = probability(self.size)
        if type(self.critical) is not int or not 0 <= self.critical <= self.n+1:
            raise ValueError('critical count must be an integer in0..n+1')
        if size > alpha:
            raise ValueError('recorded size must not exceed alpha')
        object.__setattr__(self,'p0',p0)
        object.__setattr__(self,'alpha',alpha)
        object.__setattr__(self,'size',size)

    def reject(self, k):
        if type(k) is not int or not 0 <= k <= self.n:
            raise ValueError('observed k must be an integer in 0..n')
        return k >= self.critical


def upper_test(n, p0=Fraction(1,2), alpha=Fraction(1,20)):
    """Smallest critical c with P_p0(K>=c)<=alpha, including never-reject c=n+1."""
    n, p0, alpha = _count(n), _p(p0), _p(alpha)
    tails = _tails(n, p0)
    critical = next(k for k, tail in enumerate(tails) if tail <= alpha)
    return UpperTest(n, p0, alpha, critical, tails[critical])


def rejection_probability(test, p):
    if not isinstance(test, UpperTest):
        raise TypeError('UpperTest required')
    return _tails(test.n, _p(p))[test.critical]


@dataclass(frozen=True)
class OperatingPoint:
    n: int
    critical: int
    size: Fraction
    power: Fraction


@dataclass(frozen=True)
class SamplePlan:
    p0: Fraction
    p1: Fraction
    alpha: Fraction
    target_power: Fraction
    max_n: int
    selected: UpperTest | None
    evaluated: tuple


def minimum_n(p0, p1, *, alpha=Fraction(1,20), target_power=Fraction(4,5), max_n=MAX_N):
    """Ascending finite search. No hit means only not found within max_n.

    Power need not increase at EVERY integer n, due to changing critical counts;
    a binary search assuming monotonicity would not be justified.
    """
    p0, p1, alpha, target = map(_p, (p0,p1,alpha,target_power))
    max_n = _count(max_n,'max_n')
    if not p1 > p0 or target == 0:
        raise ValueError('require p1>p0 and positive target_power')
    rows, selected = [], None
    for n in range(1,max_n+1):
        test = upper_test(n,p0,alpha)
        power = rejection_probability(test,p1)
        rows.append(OperatingPoint(n,test.critical,test.size,power))
        if power >= target:
            selected = test
            break
    return SamplePlan(p0,p1,alpha,target,max_n,selected,tuple(rows))


@dataclass(frozen=True)
class Monitoring:
    horizon: int
    p0: Fraction
    actual_p: Fraction
    alpha: Fraction
    policy: str
    critical_counts: tuple
    first_crossing: tuple
    survival: tuple  # Includes initial mass1 at index0.
    transitions: int

    @property
    def rejection_probability(self):
        return sum(self.first_crossing, Fraction(0))


def monitor_upper(horizon, p0=Fraction(1,2), *, actual_p=None, alpha=Fraction(1,20), policy='repeat'):
    """Probability of first rejection under fixed predeclared count boundaries.

    final: one upper test at horizon; repeat: alpha at EACH look;
    spend: alpha/horizon at each look, a union-bound familywise control.
    No independence between overlapping looks is assumed.
    """
    n, p0, alpha = _count(horizon,'horizon'), _p(p0), _p(alpha)
    p = p0 if actual_p is None else _p(actual_p)
    if policy not in ('final','repeat','spend'):
        raise ValueError('policy must be final, repeat or spend')
    # Spending creates a derived rational, possibly>64bits. The public inputs
    # remain bounded; alpha/n has at most8 additional denominator bits.
    per_look = alpha / n if policy == 'spend' else alpha
    boundaries = []
    for look in range(1,n+1):
        if policy == 'final' and look < n:
            boundaries.append(look+1)
        else:
            tails = _tails(look,p0)
            boundaries.append(next(k for k,v in enumerate(tails) if v <= per_look))
    active = {0: Fraction(1)}
    survival, first, transitions = [Fraction(1)], [], 0
    for look, critical in enumerate(boundaries,1):
        candidates = {}
        for k,mass in active.items():
            for bit,weight in ((0,1-p),(1,p)):
                transitions += 1
                contribution = mass*weight
                if contribution:
                    candidates[k+bit] = candidates.get(k+bit,Fraction(0))+contribution
        hit = sum((mass for k,mass in candidates.items() if k >= critical), Fraction(0))
        active = {k:mass for k,mass in candidates.items() if k < critical}
        first.append(hit)
        survival.append(sum(active.values(),Fraction(0)))
        if sum(first,Fraction(0))+survival[-1] != 1:
            raise ArithmeticError('first-hit/survival conservation failed')
    return Monitoring(n,p0,p,alpha,policy,tuple(boundaries),tuple(first),tuple(survival),transitions)
