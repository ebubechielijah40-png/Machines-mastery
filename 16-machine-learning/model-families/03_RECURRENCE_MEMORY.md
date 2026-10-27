# A state that carries information through time

Read binary likelihood and derivatives in [unit 1](01_BINARY_LEARNING.md) first.
A vector classifier needs a fixed number of coordinates. A sensor stream instead
arrives one reading at a time. Retaining every reading costs growing storage;
using only the newest reading discards history. A recurrence supplies a fixed-size
state, updated by a shared rule. That compression is both its capability and a
source of failure. The derivation below is original; inspected foundations and
scope are in [SOURCES](SOURCES.md).

## Define the machine before training it

Our input is a nonempty sequence of scalars x1,…,xT. Our state is a scalar h,
initially zero. Five parameters are shared at every step:

\[
a_t=u x_t+r h_{t-1}+b,\qquad h_t=\tanh a_t,\quad h_0=0,
\qquad z=v h_T+c,\quad P(y=1\mid x)=\sigma(z).
\]

The tuple in `ScalarRNN` is `(u,r,b,v,c)`. The state lies in [−1,1] in floating
point; mathematically finite tanh arguments give a value strictly between them.
Output probability describes the declared binary label, not the probability of
the input sequence. This is a many-input, one-output classifier. Reusing weights
makes sequence length independent of parameter count. It does not guarantee
that a fixed scalar can preserve every property of an arbitrary history.

Take `(u,r,b,v,c)=(1,.5,0,2,0)` and input `(1,0)`:

1. a1=1 and h1≈.761594.
2. a2=.5h1≈.380797 and h2≈.363400.
3. z=2h2≈.726799, probability≈.674102.
4. For y=1, loss=log(1+exp(−z))≈.394373.

The zero second input still changes state: recurrence is not a rule that stores a
value until the next nonzero reading. With r=.5, repeated blanks contract toward
zero. With r sufficiently above one, this nonlinear rule can have two stable
nonzero states, retaining a sign across blanks. Neither behavior says what will
happen when a later, large input reverses the sign.

## Unroll time to derive every gradient

Think of T copies of the same computation connected in order. Their **values**
are different; the parameters are shared. Let d=σ(z)−y. At the output,

\[
\partial_v L=d h_T,\quad \partial_c L=d,\quad g_T=d v.
\]

Here g_t means ∂L/∂h_t. At each step in reverse order define

\[
\delta_t=g_t(1-h_t^2),\quad
\partial_u L=\sum_t\delta_t x_t,\quad
\partial_r L=\sum_t\delta_t h_{t-1},\quad
\partial_b L=\sum_t\delta_t,\quad
\partial_{x_t}L=\delta_t u,\quad g_{t-1}=\delta_t r.
\]

Every sum is essential: changing u changes every use of u. Overwriting the
accumulator with the last step's contribution differentiates a different graph.
Using updated parameters halfway through the reverse pass also differentiates a
different graph. Cache forward states, accumulate with the old parameter tuple,
then return a complete new tuple. `gradients` implements exactly that contract.

For the two-step example, d≈−.325898, g2≈−.6518,
δ2≈−.5657 and δ1≈−.1188. Thus ∂rL≈−.4308, ∂uL≈−.1188,
∂bL≈−.6845, ∂vL≈−.1184 and ∂cL≈−.3259. Rounding explains
small differences when checking these numbers. Perturb each of the five
parameters by ±1e−6 and compare the central difference to the analytic result.
Then perturb each input. A parameter-only check would miss an incorrect input
adjoint that a downstream interpretability tool might rely upon.

## Why a distant influence disappears or grows

For t<T, the state sensitivity is the product

\[
\frac{\partial h_T}{\partial h_t}
=\prod_{j=t+1}^{T}r(1-h_j^2).
\]

If every absolute factor is at most q<1, its magnitude is at most q^(T−t).
A bound is sufficient, not necessary. For a *linear* state with transition .5,
the first-state sensitivity after 32 positions is .5^31≈4.657e−10. At1.5 it
is1.5^31≈287626.6. In the actual tanh model, saturation contributes small
`1-h*h` factors, so |r|>1 alone does not prove exploding gradients. A large
recurrent coefficient can simultaneously create persistent forward state and
small local derivatives near stable saturated states.

Whole-vector clipping replaces gradient g by g·min(1,C/||g||). It bounds the
update length by rate·C. It cannot restore an influence that already vanished,
and it changes the step direction only through a common scale. Clipping each
coordinate separately is a different operation. `batch_step` rejects nonfinite
adjoints and validates every new parameter before returning any update.

Full reverse differentiation here costs O(T) time and O(T) cached state per
sequence with five parameters. Truncating the reverse pass would reduce temporal
credit assignment; it is an approximation, not the full gradient used here.
A vector hidden state would replace r by a matrix and scalar products by products
of state Jacobians. Gated states offer additional paths but need their own
implementation and evidence; this unit does not claim to implement LSTM or GRU.

## Investigation: memory under a changed input

Before running [experiment.py](experiment.py), predict three separate things:
blank extension, a large late distractor, and the first-input derivative at the
initialization. The actual training set has only six noiseless sequences: each
starts with ±1 and has total length2,4 or8; remaining inputs are zero. The label
is the initial sign. The reference trains900 full-batch steps with rate.15 and
norm cap1. A held blank extension tests the learned transition repeatedly; it
is a very limited extrapolation test, not a new source of realistic data.

The [saved run](evidence/observed-2026-10-23.json) fits all six training examples
and retains both signs through128 blank steps. Yet the four late-distractor cases
have accuracy.5. Initial first-input loss sensitivity falls from about−.08674 at
length2 to−1.160e−39 at128. Explain how these observations can coexist by tracing
forward state and reverse sensitivity separately. Do not describe the initialized
model's sensitivity as the trained model's sensitivity.

A changed experiment should freeze its rule before observing performance: choose
a distribution of distractor magnitudes, training lengths and noise; keep a
separate evaluation seed; record each change. Compare to the trivial classifier
that stores the first input exactly. If exact first-sign retention is the whole
application, that hand-written baseline may be preferable. Learning a mechanism
is not automatically an engineering improvement.

Complete exercises13–18, then reconstruct the reverse loop without looking at
`discriminative.py`. The acceptance condition is agreement with independent
central differences for all parameters and inputs, plus an explanation of a
retention failure under a declared changed condition.
