# Repeated samples, bootstrap estimates and confidence-interval failure

A computed mean is exact for its input numbers, but its relation to an unknown
population depends on how those numbers were observed. More decimal places do
not fix a biased sample. This unit teaches a small resampling mechanism from
its probability model, then computes a concrete case in which a nominal95%
interval fails badly. It connects statistical inference to honest
[ML evaluation](../../16-machine-learning/training/EXPERIMENTS.md): repetition
of a calculation is not independence of its evidence.

## Prerequisites and question

Begin with [probability/inference](../../foundations/statistics/probability-inference/README.md),
[algebra/functions](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md)
and Python sequences/loops. Define the target before choosing a statistic.
For iid observations X1,...,Xn from a common distribution with mean μ and finite
variance σ², the sample mean is Xbar=ΣXi/n. We ask how its sampling variation
can be estimated when the distribution is unknown. The iid assumption rules
out treating several readings of one shared object as unrelated observations.
All examples below are dimensionless synthetic values, not physical measurements.

## 1. Separate population, observed sample and repeated calculation

If X1 and X2 are independent Bernoulli(p), possible samples are00,01,10,11.
Their means are0,.5,.5,1, with probabilities(1-p)²,p(1-p),p(1-p),p². At p=.5,
this is1/4,1/4,1/4,1/4 over samples and1/4,1/2,1/4 over mean values. This is a
**sampling distribution**, obtained by repeating the observation procedure.
An observed sample[0,1] supplies mean.5. It does not reveal that true p=.5;
many populations could have produced it.

For iid observations, E(Xbar)=μ by linearity. Independence gives
Var(Xbar)=ΣVar(Xi)/n²=σ²/n. Covariances otherwise add terms:
`Var(Xbar)=(ΣVar(Xi)+2Σi<j Cov(Xi,Xj))/n²`.
Positive shared variation can therefore make independent-row uncertainty too
small. Repeating a recorded row100 times is not equivalent to observing100
independent objects.

Why sample variance divides by n-1: expand
`Σ(Xi-Xbar)²=ΣXi²-n*Xbar²`. Its expectation is
`n(σ²+μ²)-n(σ²/n+μ²)=(n-1)σ²`. Dividing by n-1 removes this bias under the
stated assumptions. For[0,1], mean.5, squared deviations sum.5 and sample
variance.5. The empirical distribution's variance instead divides by n, giving.25.
These denominators answer different questions.

## 2. Replace the unknown distribution with an explicit empirical model

Assign mass1/n to each observed occurrence. Draw n values **with replacement**
from that finite distribution and recompute the statistic. Repeat B times.
This is the basic empirical bootstrap mechanism inspected in Efron1979,§2;
its calculation is not a universal guarantee about every statistic or sample.
[S1] A permutation without replacement preserves a sample mean exactly and
cannot represent its resampling uncertainty.

For observed[0,1], every ordered resample is visible by hand:

| Resample | Mean | Conditional probability |
| --- | ---: | ---: |
|00 |0 |1/4 |
|01 |.5 |1/4 |
|10 |.5 |1/4 |
|11 |1 |1/4 |

The conditional mean is.5 and variance is
`(.25+.0+.0+.25)/4=.125`. In general the empirical single-draw variance is
`(n-1)*s²/n`; independent resampled draws give conditional mean variance
`(n-1)*s²/n²`. This is an exact statement **under the empirical model**, not
a proof that it equals unknown-population sampling variance. The distinction
is testable in the small enumeration before introducing random simulation.

[stats_lab.py](../code/stats_lab.py) supplies finite numeric validation, mean,
sample variance, bounded exact enumeration for n≤6, seeded resampling and
quantiles. Each resample is n random indices; multiplicities matter. Exact
enumeration costs n^n samples and O(n*n^n) arithmetic, explaining the small
bound. Monte Carlo costs O(Bn) time and O(B) stored means. Increasing B reduces
simulation error conditional on the **same sample**; it does not collect new
population observations or repair a missing subgroup.

## 3. Declare a quantile convention before naming an interval

For sorted resampled statistics z1≤...≤zB, the implementation uses the empirical
CDF's left inverse: q(p)=z[max(1,ceil(pB))], with one-based indexing. At p=0 it
returns the minimum. It does not interpolate linearly. For[0,.5,.5,1], q(.25)=0,
q(.5)=.5 and q(1)=1. Other conventions may differ in small samples, so record
the rule rather than assuming a library's printed endpoints are interchangeable.

The percentile interval is `[q(alpha/2),q(1-alpha/2)]`. This unit implements
that specific rule. A95% label describes a nominal repeated-sampling target;
it is not a95% probability that a fixed frequentist parameter moves into this
one observed interval. Whether its actual coverage approaches the target needs
assumptions and evidence. A symmetric bootstrap distribution is not enough to
establish small-sample coverage.

## 4. An exact failure: rare events never observed

Let true Bernoulli p=.1 and sample size n=5. All-zero data occurs with probability
`.9^5=.59049`. Its empirical distribution assigns all mass to0. Every resample
is all zeros, so every percentile interval is[0,0] for any B. It misses p=.1.
Consequently coverage is **at most**`1-.59049=.40951`, already far below95%.
A million resamples cannot invent the missing event under this model.

We can calculate full coverage without Monte Carlo. If the original sample
contains k successes, its probability is `C(n,k)*p^k*(1-p)^(n-k)`. The empirical
model has success probability k/n, so the bootstrap success count K* follows
Binomial(n,k/n). Compute its exact lower/upper quantiles and divide by n. Add
the original-sample probabilities only for intervals containing true p:

`coverage = Σk Pp(K=k) * 1[lower(k) ≤ p ≤ upper(k)]`.

The [experiment](experiment.py) performs that finite sum and retains every k
case. This is an independently inspectable counterexample, not an estimate
from lucky simulation or a claim copied from a paper table. Discreteness and
boundary degeneracy matter; a nominal percentage alone supplies no correction.
Larger n can change coverage, but there is no monotonic/exact95% promise here.

## 5. From arithmetic correctness to scientific evidence

The test suite checks hand values, exact sample multiplicities, empirical
quantiles, seeded Monte Carlo, affine equivariance, degeneracy and the independent
upper bound. It also rejects invalid alpha/repetition counts, nonfinite values,
Boolean data and unsupported enumeration size. These validate a bounded mechanism.
They cannot show that a real collection process was random, uncensored or
representative. Finite floats also have range/rounding limits.

For engineering latency measurements, a burst of requests may share a cache,
queue or dependency failure. A row bootstrap assumes those dependencies away.
A block/cluster resampling design needs the actual unit of independence and
its own coverage study; it is not implemented here. For ML, duplicated examples,
shared subjects, time leakage and tuning on the held set create related evidence
problems. Freeze preprocessing/splits and identify the independent sampling unit
before claiming a confidence interval validates generalization.

## Run, assess and reconstruct

Python3.10+ standard library, from repository root:

```sh
python3 -m unittest discover -s 10-data-science/code -v
python3 10-data-science/bootstrap-evidence/experiment.py
```

Use [exercises](EXERCISES.md), then separate [hints](HINTS.md) and
[solutions](SOLUTIONS.md). Deliver your exact two-row enumeration, original code,
actual random counts, the rare-event proof and a real sampling-design critique.
Rubric: assumptions25%, probability derivation25%, independent tests20%, actual
evidence/limits20%, unaided transfer10%. Rebuild exact Bernoulli coverage from
blank files before comparing the reference. [Actual observations](EXPERIMENTS.md)
and [source scopes](SOURCES.md) are separate; no physical data, general-purpose
inference package or paper-result reproduction is claimed.
