"""Small numerical mechanisms for the accompanying original lesson.

Finite real binary floats only; not interval arithmetic or a certified error bound.
Standard-library fsum is used for accumulation, not for differentiation or inference.
"""
from dataclasses import dataclass
import math


def finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f'{name} must be finite')
    return value


def difference(f, x, h, method='central'):
    """Estimate f'(x). Reject steps rounded back to x instead of returning zero.

    Uses actual representable endpoints in the secant denominator. With rounded
    asymmetric endpoints, central mode is the secant at their midpoint, near x.
    No automatic step selection, continuity test or error certification is implied.
    """
    x, h = finite(x, 'x'), finite(h, 'h')
    if h <= 0:
        raise ValueError('h must be positive')
    if method not in {'forward', 'central'}:
        raise ValueError('method must be forward or central')
    right = finite(x+h, 'right endpoint')
    left = x if method == 'forward' else finite(x-h, 'left endpoint')
    if right == x or (method == 'central' and left == x):
        raise ValueError('step is not distinguishable at this float magnitude')
    span = finite(right-left, 'endpoint span')
    if span <= 0:
        raise ValueError('endpoints must have positive separation')
    numerator = finite(f(right), 'f(right)')-finite(f(left), 'f(left)')
    return finite(numerator/span, 'difference')


@dataclass(frozen=True)
class Summary:
    n: int
    mean: float
    sample_variance: float
    sem: float


def summarize(values):
    """Two-pass sample variance; SEM assumes independent equal-distribution draws.

    Materializes the input: O(n) time/storage. Numbers must share declared units.
    The arithmetic result does not establish the assumptions behind SEM.
    Accumulation or squaring may raise OverflowError even if a mathematical
    summary is representable (for example fsum([1e308,1e308])). No automatic
    scaling or arbitrary-precision fallback is implemented.
    """
    data = tuple(finite(x, 'sample') for x in values)
    n = len(data)
    if n < 2:
        raise ValueError('at least two observations required for sample variance')
    mean = finite(math.fsum(data)/n, 'mean')
    variance = finite(math.fsum((x-mean)**2 for x in data)/(n-1), 'variance')
    return Summary(n, mean, variance, math.sqrt(variance/n))


def speed_uncertainty(distance, time, u_distance, u_time, correlation=0.0):
    """First-order standard uncertainty of distance/time, including covariance.

    Inputs: m, s, m, s, dimensionless correlation. Returns (m/s, m/s).
    Caller must justify small uncertainty, positive duration and correlation.
    """
    d, t, ud, ut, rho = (finite(x, name) for x, name in zip(
        [distance, time, u_distance, u_time, correlation], ['distance','time','u_distance','u_time','correlation']))
    if t <= 0 or ud < 0 or ut < 0 or not -1 <= rho <= 1:
        raise ValueError('need positive time, nonnegative uncertainties and correlation in [-1,1]')
    speed = finite(d/t, 'speed')
    # Evaluate using dimensionless relative time uncertainty. Forming t*t
    # needlessly over/underflows for otherwise representable output scales.
    a, b = finite(ud/t, 'distance contribution'), finite(-speed*(ut/t), 'time contribution')
    # a²+b²+2ρab = (a+ρb)² + (1-ρ²)b²; latter avoids a small negative
    # variance from cancellation at |ρ|=1. Still subject to float range limits.
    uncertainty = math.hypot(a+rho*b, math.sqrt(max(0.0, 1-rho*rho))*b)
    return speed, finite(uncertainty, 'uncertainty')
