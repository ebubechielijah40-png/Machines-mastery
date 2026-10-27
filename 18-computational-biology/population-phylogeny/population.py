"""Small exact finite-copy Wright-Fisher model; synthetic educational data only.

m counts gene copies (m=2N for a neutral ideal diploid autosomal locus).
The optional selection extension is haploid/copy fitness, NOT diploid dominance.
"""
import math
import random


def copies(m):
    if type(m) is not int or not 2 <= m <= 200:
        raise ValueError('this exact teaching model supports two through two hundred copies')
    return m


def count(i, m):
    if type(i) is not int or not 0 <= i <= m:
        raise ValueError('allele count must be an integer within population bounds')
    return i


def generations(t):
    if type(t) is not int or not 0 <= t <= 10000:
        raise ValueError('bounded nonnegative integer generations required')
    return t


def selected_frequency(p, selection=0):
    if isinstance(p,bool) or not isinstance(p,(int,float)) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('frequency must be finite in [0,1]')
    if isinstance(selection,bool) or not isinstance(selection,(int,float)) or not math.isfinite(selection) or selection <= -1:
        raise ValueError('copy fitness 1+s must be positive and finite')
    return (1+selection)*p/(1+selection*p)


def transition(m, i, selection=0):
    m=copies(m);i=count(i,m)
    p=selected_frequency(i/m,selection)
    return [math.comb(m,j)*p**j*(1-p)**(m-j) for j in range(m+1)]


def distribution(values):
    m=copies(len(values)-1)
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x < 0 for x in values):
        raise ValueError('finite nonnegative probabilities required')
    if abs(sum(values)-1)>1e-10:
        raise ValueError('distribution must sum to one; it is not silently normalized')
    return m,list(values)


def evolve(m, initial, t, selection=0):
    m=copies(m);initial=count(initial,m);t=generations(t)
    if t*(m+1)**2 > 20_000_000:
        raise ValueError('exact propagation work budget exceeded')
    kernel=[transition(m,i,selection) for i in range(m+1)]
    current=[float(i==initial) for i in range(m+1)]
    history=[current]
    for _ in range(t):
        current=[sum(current[i]*kernel[i][j] for i in range(m+1)) for j in range(m+1)]
        history.append(current)
    return history


def simulate(m, initial, t, seed=0, selection=0):
    m=copies(m);initial=count(initial,m);t=generations(t)
    if type(seed) is not int:raise ValueError('integer seed required')
    selected_frequency(initial/m,selection)
    rng=random.Random(seed);history=[initial];i=initial
    for _ in range(t):
        p=selected_frequency(i/m,selection)
        i=sum(rng.random()<p for _ in range(m))
        history.append(i)
    return history


def summary(values):
    m,values=distribution(values)
    mean=sum(i/m*p for i,p in enumerate(values))
    return {'mean_frequency':mean,
            'variance_frequency':sum((i/m-mean)**2*p for i,p in enumerate(values)),
            'expected_heterozygosity':sum(2*(i/m)*(1-i/m)*p for i,p in enumerate(values)),
            'loss_probability':values[0],'fixation_probability':values[-1],
            'total_probability':sum(values)}


def log_likelihood(m, observed_counts, selection=0):
    """Likelihood for consecutive complete-population counts, not noisy read counts."""
    m=copies(m)
    if not 2 <= len(observed_counts) <= 10001:
        raise ValueError('two through ten thousand and one consecutive counts required')
    for i in observed_counts:count(i,m)
    result=0.0
    for i,j in zip(observed_counts,observed_counts[1:]):
        p=selected_frequency(i/m,selection)
        if p in (0,1):
            if j != int(p*m):return -math.inf
        else:
            result+=math.lgamma(m+1)-math.lgamma(j+1)-math.lgamma(m-j+1)+j*math.log(p)+(m-j)*math.log1p(-p)
    return result
