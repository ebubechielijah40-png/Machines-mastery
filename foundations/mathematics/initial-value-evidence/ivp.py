"""Bounded original IVP mechanisms. Local agreement is not an error certificate.

Callbacks and iterators are trusted to return; budgets cannot interrupt them.
All time variables are caller-declared consistent units; forward spans only.
"""
from dataclasses import dataclass
from itertools import islice
import math


class ContractError(ValueError):
    pass


def finite(x, name='number'):
    if isinstance(x, (bool, str, bytes, bytearray)):
        raise ContractError(name + ' must be a finite real number')
    try:
        out = float(x)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ContractError(name + ' is not representable') from exc
    if not math.isfinite(out):
        raise ContractError(name + ' must be finite')
    return out


def integer(x, name, maximum):
    if type(x) is not int or not 1 <= x <= maximum:
        raise ContractError(f'{name} must be an integer in 1..{maximum}')
    return x


def vector(values, name, dimension=None):
    try:
        out = tuple(finite(v, name) for v in islice(iter(values), 9))
    except TypeError as exc:
        raise ContractError(name + ' must be iterable') from exc
    if not 1 <= len(out) <= 8 or (dimension is not None and len(out) != dimension):
        raise ContractError(name + ' must have the expected 1..8 coordinates')
    return out


@dataclass(frozen=True)
class Trajectory:
    times: tuple
    states: tuple
    field_calls: int
    accepted: int
    rejected: int = 0


class Field:
    def __init__(self, function, dimension, max_calls):
        if not callable(function):
            raise ContractError('field must be callable')
        self.function, self.dimension = function, dimension
        self.limit = integer(max_calls, 'max_calls', 10_000_000)
        self.calls = 0

    def __call__(self, t, y):
        if self.calls == self.limit:
            raise ContractError('field-call budget exhausted')
        self.calls += 1
        return vector(self.function(t, y), 'field output', self.dimension)


def shift(y, slope, h):
    return vector((a + h*b for a,b in zip(y,slope)), 'stage state', len(y))


def advance(f, t, y, h, method):
    k1 = f(t,y)
    if method == 'euler':
        return shift(y,k1,h)
    if method == 'heun':
        k2 = f(t+h,shift(y,k1,h))
        return shift(y,tuple(a/2+b/2 for a,b in zip(k1,k2)),h)
    k2 = f(t+h/2,shift(y,k1,h/2))
    k3 = f(t+h/2,shift(y,k2,h/2))
    k4 = f(t+h,shift(y,k3,h))
    return shift(y,tuple(a/6+b/3+c/3+d/6 for a,b,c,d in zip(k1,k2,k3,k4)),h)


def initial(function, start, end, state, max_calls):
    start,end = finite(start,'start'),finite(end,'end')
    if end < start or not math.isfinite(end-start):
        raise ContractError('finite forward time span required')
    y = vector(state,'initial state')
    return start,end,y,Field(function,len(y),max_calls)


def integrate_fixed(function,start,end,state,*,steps,method='rk4',max_calls=1_000_000):
    """Endpoint mesh may have slightly unequal floating spacings."""
    if method not in ('euler','heun','rk4'):
        raise ContractError('method must be euler, heun or rk4')
    steps = integer(steps,'steps',100_000)
    start,end,y,f = initial(function,start,end,state,max_calls)
    times,states = [start],[y]
    if start == end:
        return Trajectory(tuple(times),tuple(states),0,0)
    for j in range(1,steps+1):
        following = end if j == steps else start+(end-start)*(j/steps)
        h = following-times[-1]
        if h <= 0:
            raise ContractError('mesh cannot advance in floating-point time')
        y = advance(f,times[-1],y,h,method)
        times.append(following);states.append(y)
    return Trajectory(tuple(times),tuple(states),f.calls,steps)


def adaptive_rk4(function,start,end,state,*,first_step,atol=1e-8,rtol=1e-6,
                 min_step=1e-14,max_attempts=20_000,max_calls=1_000_000):
    """One full versus two half RK4 steps:12 calls per attempt, fine accepted.

    Error estimate |fine-coarse|/15 is a smooth local asymptotic heuristic.
    It can miss features entirely and does not certify global/model error.
    """
    start,end,y,f = initial(function,start,end,state,max_calls)
    h,min_step,rtol = finite(first_step),finite(min_step),finite(rtol)
    if h <= 0 or min_step <= 0 or rtol < 0:
        raise ContractError('positive steps and nonnegative rtol required')
    attempts = integer(max_attempts,'max_attempts',100_000)
    absolute = ((finite(atol,'atol'),)*len(y) if isinstance(atol,(int,float))
                else vector(atol,'atol',len(y)))
    if any(a <= 0 for a in absolute):
        raise ContractError('absolute tolerances must be positive')
    times,states,rejected = [start],[y],0
    if start == end:
        return Trajectory(tuple(times),tuple(states),0,0)
    for _ in range(attempts):
        t = times[-1]
        h = min(h,end-t)
        following = end if h == end-t else t+h
        h = following-t
        middle = t+h/2
        if not t < middle < following:
            raise ContractError('step cannot advance representable stage times')
        coarse = advance(f,t,y,h,'rk4')
        half = advance(f,t,y,middle-t,'rk4')
        fine = advance(f,middle,half,following-middle,'rk4')
        ratios = []
        for old,new,rough,a in zip(y,fine,coarse,absolute):
            scale = finite(a+rtol*max(abs(old),abs(new)),'error scale')
            difference = finite(new-rough,'step difference')
            ratios.append(abs(difference)/15/scale)
        error = max(ratios)
        accept = error <= 1
        if accept:
            y = fine
            times.append(following);states.append(y)
            if following == end:
                return Trajectory(tuple(times),tuple(states),f.calls,len(times)-1,rejected)
        else:
            rejected += 1
        factor = 5 if error == 0 else min(5,max(.2,.9*error**(-.2)))
        proposed = h*factor
        if not accept and proposed < min_step:
            raise ContractError('rejected step below min_step')
        h = max(min_step,proposed)
    raise ContractError('attempt budget exhausted')


def decay_step(y,rate,h,*,implicit=False):
    """Only scalar y'=-rate*y, rate>=0; not a general implicit solver."""
    y,rate,h = finite(y),finite(rate),finite(h)
    if rate < 0 or h <= 0 or type(implicit) is not bool:
        raise ContractError('nonnegative rate, positive h, bool implicit required')
    z = finite(rate*h,'rate*h')
    return finite(y/(1+z) if implicit else y*(1-z),'decay output')


def oscillator_step(x,v,omega,h):
    """Velocity-first symplectic Euler; unforced undamped constant frequency."""
    x,v,omega,h = map(finite,(x,v,omega,h))
    if omega < 0 or h <= 0:
        raise ContractError('nonnegative omega and positive h required')
    vn = finite(v-h*omega*omega*x,'new velocity')
    return finite(x+h*vn,'new position'),vn


def oscillator_energy(x,v,omega):
    """Joules only with explicitly assumed mass1kg, SI x,v,omega inputs."""
    x,v,omega = map(finite,(x,v,omega))
    if omega < 0:
        raise ContractError('omega must be nonnegative')
    wx = omega*x
    return finite(.5*(v*v+wx*wx),'energy')
