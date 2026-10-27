"""Inspectable Laplace count/budget mechanism for synthetic teaching experiments.

The real-valued mathematical mechanism is proved in LESSON.md. This finite-float
sampler and in-memory accountant are NOT a certified private release service.
Random seeds, finite support, crash/reset, access control and side channels matter.
"""
import math
import itertools
import random

MICROS=1_000_000


def count_bits(bits):
    data=list(itertools.islice(bits,100_001))
    if len(data)>100_000:raise ValueError('teaching input bound exceeded')
    if any(type(x) not in (int,bool) or x not in (0,1) for x in data):
        raise ValueError('each record must contribute exactly zero or one')
    return sum(data)


def laplace_quantile(u,scale):
    if not isinstance(u,(int,float)) or not math.isfinite(u) or not 0<u<1:
        raise ValueError('uniform input must be strictly between zero and one')
    if not isinstance(scale,(int,float)) or not math.isfinite(scale) or scale<=0:
        raise ValueError('scale must be finite and positive')
    result=scale*math.log(2*u) if u<.5 else -scale*math.log(2*(1-u))
    if not math.isfinite(result):raise ValueError('noise exceeds representable float range')
    return result


def laplace_noise(scale,rng):
    # Exclude endpoints rather than call log(0). This discrete float support is
    # one reason the continuous proof cannot certify this sampler exactly.
    for _ in range(1024):
        u=rng.random()
        if 0<u<1:return laplace_quantile(u,scale)
    raise ValueError('RNG did not produce an interior uniform value')


def log_density_ratio(z,count_a,count_b,scale):
    """Analytic real-Laplace log p_a(z)/p_b(z), not a float sampler proof."""
    if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in [z,count_a,count_b,scale]) or scale<=0:
        raise ValueError('finite arguments and positive scale required')
    ratio=(abs(z-count_b)-abs(z-count_a))/scale
    if not math.isfinite(ratio):raise ValueError('density-ratio arithmetic exceeds float range')
    return ratio


def clip_public(value,lower,upper):
    if not all(math.isfinite(x) for x in [value,lower,upper]) or lower>upper:
        raise ValueError('finite public bounds in order required')
    return min(upper,max(lower,value))


class Budget:
    """Exact integer-microepsilon accounting for the declared conservative sum.

    Budget is one object for a fixed protected dataset/neighbor relation. No
    persistence, concurrency or automatic population identity is implemented.
    """
    def __init__(self,total_micros):
        if type(total_micros) is not int or not 1<=total_micros<=1_000_000_000:
            raise ValueError('total microepsilon must be a positive bounded integer')
        self.total=total_micros;self.spent=0

    @property
    def remaining(self):return self.total-self.spent

    def release(self,bits,epsilon_micros,*,rng=None):
        if type(epsilon_micros) is not int or epsilon_micros<=0:
            raise ValueError('epsilon micro-units must be a positive integer')
        count=count_bits(bits)
        if epsilon_micros>self.remaining:raise ValueError('privacy budget exhausted')
        epsilon=epsilon_micros/MICROS
        self.spent+=epsilon_micros  # conservative reservation even on later RNG failure
        return count+laplace_noise(1/epsilon,rng if rng is not None else random.SystemRandom())
