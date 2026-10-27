# From scoring labels to generating observations

A classifier estimates a conditional probability of a label. A generative model
assigns probabilities or densities to observations and can specify how to draw a
new one. This chapter builds two small examples: finite text transitions and a
continuous latent mixture. Neither is a reconstruction of a modern foundation
model. Start with [conditional probability](../../foundations/statistics/probability-inference/README.md)
and [binary likelihood](01_BINARY_LEARNING.md).

## Chain rule first; a memory assumption second

For characters x1,…,xT and an end marker E, the probability chain rule gives

\[
P(x_1,\ldots,x_T,E)=P(x_1\mid B)
\prod_{t=2}^{T}P(x_t\mid x_{<t})P(E\mid x_{\leq T}).
\]

B marks the start and is not a generated character. This factorization is exact.
A bigram *assumes* that each conditional depends on the immediately previous
character only. That replacement discards earlier history. Counts fit the
conditional table; smoothing reserves mass for transitions not seen in training.
With alphabet size V and smoothing α>0,

\[
P(j\mid i)=\frac{C_{ij}+\alpha}{\sum_k C_{ik}+\alpha(V+1)}.
\]

The additional outcome is E. There are V+1 rows (characters plus B) and V+1
columns (characters plus E). The final array index means different things on the
two axes; it is never an emitted extra character. A document of length T supplies
T+1 transitions, including termination. Empty documents contribute B→E.

Work an original example: alphabet `(a,b)`, documents `['ab','a','']`, α=1.
The B row has counts(a:2,b:0,E:1), giving probabilities(3/6,1/6,2/6).
The a row has(0,1,1), giving(1/5,2/5,2/5). The b row gives(1/4,1/4,2/4).
Therefore P('ab',E)=(1/2)(2/5)(1/2)=1/10. Its mean negative log likelihood,
including E, is log(10)/3≈.767528 nats per prediction. A likelihood across many
documents divides by total predictions, not the number of documents. Omitting
the end marker changes both the model and that denominator.

To sample, draw a uniform U∈[0,1), walk cumulative row probabilities, and choose
the first interval containing U. Stop on E; otherwise use the chosen character
as the next state. Positive smoothing gives every finite state a positive end
probability. With finitely many rows its minimum is positive, so the probability
of never ending is zero in the mathematical model. A finite safety budget can
still cut off an actual generated sample. `sample` returns `terminated=False`
when this happens; it must not falsely append E or call the truncated string an
unconditioned terminated draw.

## A structural failure survives more training

Training documents in the experiment begin with a or b, contain a run of x, and
end with the same initial symbol. Once the current state is x, the model has the
same row regardless of the initial character. It cannot choose a closing symbol
based on that first character. The equal a/b conditional probability given that
the next symbol is a or b is exactly.5 for these balanced counts. Some generated
samples happen to match; they do not establish a remembered dependency.

A larger n-gram retains a longer fixed suffix but expands table size toward
V^n. A recurrent state or an attention model supplies different context
representations, with other costs. Continue to [the trained decoder](../training/README.md)
after reproducing this finite count model. Better output fluency does not remove
the need to specify an evaluation task and a held-out distribution.

## Mixtures: a hidden cause for each observation

A density has units inverse to its input. A Gaussian density can exceed1; its
integral, rather than its point value, is one. For K components define positive
weights πk summing to1, means μk and variances sk²>0:

\[
p(x)=\sum_{k=1}^{K}\pi_k\frac{1}{\sqrt{2\pi s_k^2}}
\exp\!\left[-\frac{(x-\mu_k)^2}{2s_k^2}\right].
\]

A generative interpretation first draws a component Z from π, then a value from
that Gaussian. Z is unobserved in fitting. Assigning each point to its nearest
mean treats an uncertain hidden assignment as certain and ignores component
variance and prior mass. Instead Bayes' rule gives a *responsibility*

\[
r_{ik}=P(Z_i=k\mid x_i)=\frac{\pi_k\phi(x_i;\mu_k,s_k^2)}
{\sum_j\pi_j\phi(x_i;\mu_j,s_j^2)}.
\]

For equal weights, equal unit variances and means−1,+1, x=0 has responsibilities
(.5,.5). At x=1 they are(1/(1+e²),e²/(1+e²))≈(.119203,.880797).
A fractional responsibility is not a fractional physical observation; it is a
weight in an expected complete-data objective.

## Derive the EM update

Freeze responsibilities computed under the old parameters. The parameter-varying
part of the expected complete log likelihood is

\[
Q=\sum_{i,k}r_{ik}\left[\log\pi_k-\tfrac12\log s_k^2
-\frac{(x_i-\mu_k)^2}{2s_k^2}\right]+\text{constant}.
\]

Let Nk=Σi rik. A Lagrange multiplier enforces Σπk=1; solving Nk/πk=λ gives
πk=Nk/N. Differentiating in μk gives Σi rik(xi−μk)=0, hence its weighted mean.
Differentiating in variance gives its weighted squared residual mean. With an
explicit lower bound ε, the constrained optimum is

\[
\pi_k'=N_k/N,\quad\mu_k'=\frac{\sum_i r_{ik}x_i}{N_k},\quad
s_k'^2=\max\!\left(\epsilon,\frac{\sum_i r_{ik}(x_i-\mu_k')^2}{N_k}\right).
\]

The new mean must be used for the new residuals. All components update from the
same old responsibility matrix. Updating one component in place and then
recomputing some responsibilities implements a different algorithm.

For two points−1,+1 and initial means−1,+1, unit variances and equal weights,
let q=1/(1+e²). Each component has mass1. The new means are∓(1−2q)
≈∓.761594, weights remain.5 and both variances are1−.761594²≈.419974.
Work this step independently before using `em_step`.

Why can likelihood improve? For any fixed normalized q(k), concavity of log gives
logΣk p(x,k) ≥ Σk q(k)log[p(x,k)/q(k)]. The posterior makes the bound tight at
the old parameters. Maximizing Q with q fixed raises that bound; the new
likelihood is at least the new bound. This argument assumes exact arithmetic,
valid normalized responsibilities and an actual maximizing step in the declared
feasible set. Floating-point tolerances and zero effective component mass need
explicit handling. `em_step` rejects zero mass and requires the initial variances
to respect the same floor. Monotonicity is neither a global optimum guarantee
nor a generalization guarantee.

## Numerical and statistical failure cases

Directly exponentiating very negative log scores can produce all zeros. The code
subtracts their maximum before normalization. To evaluate log density it uses
`m+log(sum(exp(score-m)))`. It validates data bounds and variances. These measures
reduce arithmetic failures; they do not make every extreme inference accurate.

Identical initial components stay identical under the same update and can remain
a single broad mode. Permuting component labels preserves the density, so compare
matched components or densities rather than raw index order. With repeated data,
shrinking a component variance raises its density without bound when no floor is
imposed. A floor changes the model. Negative average log density is possible and
not evidence that a probability exceeded one. Changing physical measurement units
also changes density values; compare models using the same units and data.

Sampling uses a categorical draw followed by an explicit Box–Muller normal:
Z=sqrt(−2log(1−U1)) cos(2πU2). Then X=μ+sqrt(variance)Z. A fixed seed makes
this implementation's stream reproducible in the stated environment; twelve
plausible samples do not validate its whole distribution. Test moments with
uncertainty, tail probabilities and sensitivity to sample count separately.

The [experiment protocol](EXPERIMENTS.md) retains both separated and identical
initializations, held density, variance-floor failures and finite generated
samples. Complete exercises19–24 and reconstruct the EM update and count table
without their references. Modern latent autoencoders, adversarial training and
diffusion require additional mechanisms and remain outside this completed unit.
