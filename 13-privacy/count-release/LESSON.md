# Count release: sensitivity, noise and the price of repetition

A dashboard should disclose an aggregate without making one person's participation decisive. Removing names is insufficient: if an attacker knows every other contribution, two exact count queries can reveal the remaining contribution. Differential privacy specifies a limit on how much the output distribution changes between neighboring datasets. This unit derives the ideal real-valued Laplace count mechanism, implements a transparent finite-float teaching sampler and budget model, and deliberately shows where a simulator is weaker than a private release service.

Prerequisites: absolute value, logarithms, basic integration, probability densities, expectation and variance. Before reading the proof, compute `|10-11|`, `exp(.5)` and the mean of squared deviations. Use [algebra](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md) and [calculus](../../foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md) for missing operations. Complete [scientific measurement analysis](../../projects-guided/p08-scientific-pipeline/README.md) to distinguish noisy observations, model assumptions and actual evidence. The threat here concerns information released about people, not message tampering; [authenticated provenance](../../security-cryptography-mastery/provenance/LESSON.md) protects a different property.

## Continuous probability bridge

A density is a nonnegative function whose integral over all real values is1.
Probability over an interval is the area under the density, not its height at
an endpoint: `P(a<=Z<=b)=integral_a^b p(z) dz`. A single point can have probability
zero even when values near it can occur, so the finite model's zero-mass
conditioning rule does not by itself define conditioning for continuous data.
An integral over an infinite range means a limit of finite-range integrals.

For the Laplace density below, integrating each exponential half gives1/2,
which checks normalization. The moment calculation uses integration by parts:
the product derivative `(uv)'=u'v+uv'`, integrated and rearranged, gives
`integral u dv = uv - integral v du`. Choose u=z and dv=exp(-z/b)dz/b to
obtain E|Z|=b; the endpoint term vanishes as the upper limit grows. Choosing
u=z² gives `E[Z²]=2b*integral_0^infinity z*exp(-z/b)/b dz=2b²`, using the
same doubled-half integral as E|Z|. These are properties of the ideal continuous density; the
finite sampler's exact distribution still needs separate analysis.

## Specify who receives protection

Represent a dataset D as a finite multiset of rows, each contributing a bit 0 or 1 to a count `q(D)=sum bits`. Our adjacency relation allows adding or removing one row. The L1 sensitivity is

\[
\Delta q=\sup_{D\sim D'} |q(D)-q(D')|=1.
\]

Adding a zero changes nothing; adding a one changes the count by one, so one is both a bound and an attainable maximum. The guarantee protects one **person** only if each person contributes at most one bounded row. If one person contributes k rows, person-level sensitivity can be k. Enforcing contribution bounds and population identity is part of a real system, absent from this list-of-bits API.

A randomized mechanism M is pure ε-differentially private for this adjacency if, for every neighboring pair and every possible measurable output event S,

\[
\Pr[M(D)\in S]\le e^\varepsilon\Pr[M(D')\in S].
\]

Swap D and D' to obtain the reverse inequality. Smaller ε constrains distinguishability more tightly. It does not mean a given person has probability ε of being identified, or that no information about a population can be learned. The definition quantifies over all neighboring datasets and events, not merely a sampled histogram [P1].

## Derive a distribution, then its sampler

Let real-valued noise Z have Laplace density `p(z)=exp(-|z|/b)/(2b)` with b>0. Return `q(D)+Z` with `b=Δq/ε`. At a candidate output t, the likelihood ratio is

\[
\frac{p_D(t)}{p_{D'}(t)}
=\exp((|t-q(D')|-|t-q(D)|)/b)
\le \exp(|q(D)-q(D')|/b)
\le e^\varepsilon.
\]

The first bound is the triangle inequality; integrating this pointwise inequality over any event gives the definition. Choosing b too small invalidates the bound. For counts 10 and 11, ε=.5 and b=2, the maximum absolute log ratio is .5. If b=.5 instead, outputs beyond either count can have absolute log ratio 2: the promised .5 guarantee fails. This counterexample is more informative than observing an attractive noisy chart.

To derive inverse-transform sampling, integrate the density. For z<0, `F(z)=.5 exp(z/b)`; for z>=0, `F(z)=1-.5 exp(-z/b)`. Setting F(z)=u for u uniform on (0,1) gives

\[
F^{-1}(u)=\begin{cases}b\ln(2u),&u<.5\\-b\ln(2(1-u)),&u\ge .5.\end{cases}
\]

At u=.25 and .75 this returns -b ln2 and +b ln2; at .5 it is zero. [count_release.py](count_release.py) implements these branches explicitly, rejects log endpoints and keeps inputs bounded. This mechanism is built from the equations; it is not a wrapper around a DP library.

Symmetry gives E[Z]=0. To find error magnitude, integrate the positive half and double: `E|Z| = integral_0^infinity z*exp(-z/b)/b dz = b` after one integration by parts. A second integration yields `E[Z²]=2b²`, hence variance 2b². At ε=.5 for a sensitivity-one count, predicted mean absolute error is 2 counts and variance 8 counts squared. A negative released count is mathematically allowed. Clipping with fixed public bounds is post-processing of an already released value; choosing a bound from the private dataset can itself disclose information. In particular, a private dataset size is not automatically a public clipping limit.

## Repetition changes the guarantee

For independent releases with privacy parameters ε1,...,εk, a joint density factorizes. Each neighboring likelihood ratio is bounded by its own `exp(εi)`, so their product is at most `exp(sum εi)`. This proves the conservative additive composition used here [P2]. More general adaptive composition requires controlling conditional mechanisms; arbitrary correlated noise cannot be justified by this simple independent-product argument.

Averaging k independent noisy counts leaves the mean unchanged and reduces noise variance from `2b²` to `2b²/k`. It also spends kε under this accounting. One hundred ε=.5 releases have a conservative total ε=50, and averaging their b=2 noises has variance .08. “Just average until the answer stabilizes” silently changes the privacy promise.

The `Budget` class tracks integer microepsilon: 100000 represents .1. Ten such releases spend exactly 1000000 units; an eleventh is rejected. Integer accounting avoids cumulative float-rounding drift in the declared sum. It is scoped to one fixed dataset/protected population and one object; it does not automatically recognize equivalent datasets. It reserves cost before random sampling, conservatively retaining the reservation on RNG failure. Real accounting must survive restarts, coordinate competing requests and bind query/population identity. None is implemented here.

## Mathematical proof versus executable limits

The proof is for continuous real noise. Python's finite uniform generator and floating computations have finite support and rounding behavior. Their exact output distribution is not the real Laplace distribution, and the triangle-inequality proof does not certify that finite sampler. Default `SystemRandom` is preferable to a predictable seed for a real security boundary, but changing the RNG alone does not solve finite precision, accounting or access control.

The synthetic experiment uses published fixed seeds solely for reproduction. If a real release used a known seed, an attacker could regenerate its noise and subtract it. Reusing the same seed on neighboring counts yields identical noise, making the outputs differ by exactly one; a test demonstrates this failure. A pretty empirical noise histogram or a finite density grid cannot prove differential privacy for all output events. Use a vetted mechanism/accounting implementation and a reviewed threat model for actual private data; this educational code explicitly makes no production DP certificate.

## Controlled computation and actual observations

Question: do noise utility and repetition match the derived model in a bounded synthetic simulation? Hold sensitivity one, seed policy and 20000 draws per ε fixed; vary ε across .1,.5,1,2. Instrument empirical mean error, mean absolute error and population variance; separately run 2000 averages of 100 fresh ε=.5 noises. No sensitive population data is used.

```sh
python3 -m unittest discover -s 13-privacy/count-release -v
python3 13-privacy/count-release/experiment.py
```

The recorded [observations](evidence/observed.json) gave MAE 9.90755 versus predicted 10 at ε=.1, 1.99486 versus 2 at .5, .99698 versus 1 at 1, and .49700 versus .5 at 2. These are executed fixed-seed finite-sample computations; Monte Carlo variation and floating arithmetic explain small deviations. A grid's maximum log-density ratio matched .5 for the analytic density, while the separate seed-reuse test demonstrates a failure that a utility metric would miss. The tenth .1 release exhausted the declared budget and the next denied.

Follow up by implementing a discrete, rigorously analyzed mechanism and durable accounting, then assessing contribution bounds and side channels. These are remaining requirements, not properties inferred from this simulation. Attempt [exercises](EXERCISES.md) before [hints](HINTS.md) and [solutions](SOLUTIONS.md). [Source scopes](SOURCES.md) distinguish inspected theory from independently executed work.
