# Derive attention, its derivatives, and a cache

**Prepared unit: STRONG within this narrow mechanism.** This is original instruction,
not a complete Transformer course. Read [the motivating lesson](../21_ATTENTION_FROM_FIRST_PRINCIPLES.md)
first. The historical formula is verified against [source A17](SOURCES.md).
All worked numbers below are constructed examples, not paper measurements.

## Prerequisite bridge and the problem

You need multiplication, vectors, dot products, exponentials, derivatives, the
chain rule, and Python loops. A vector's order matters: `[2, 3]` is different
from `[3, 2]`. A dot product pairs corresponding coordinates before summation.
For differentiation, `df/dx` asks how fast `f` changes for a small change in `x`.
If `f(x)=h(g(x))`, a small change first multiplies by `g'(x)` and then by
`h'(g(x))`; multiplying those local effects gives the chain rule. The sum rule
adds effects from different paths. No physics, chemistry or physical units are
needed in this toy; all vectors here are dimensionless learned coordinates.
Probability means normalized nonnegative mixing coefficients, not truth.

We want one position to read a changing amount of earlier information without
squeezing it all through one fixed recurrent state. The read must remain
trainable and must obey an information boundary. Let there be `m` permitted
key/value pairs. A query and each key have width `d`; each value has width `v`.
The widths `d` and `v` may differ. Define a scale `c=sqrt(d)` (or set `c=1` for
an ablation), then:

\[
s_j=q^T k_j/c,\quad a_j=\frac{e^{s_j}}{\sum_{\ell=1}^{m}e^{s_\ell}},\quad
 o=\sum_{j=1}^{m}a_jv_j.
\]

The output has `v` coordinates. Changing `q` or `K` changes routing; changing
`V` changes payload. Neither operation alone creates a language model.

## Why subtracting the maximum works

For any finite constant `b`, multiply numerator and denominator by `exp(-b)`:

\[
\frac{e^{s_j-b}}{\sum_\ell e^{s_\ell-b}}=
\frac{e^{-b}e^{s_j}}{e^{-b}\sum_\ell e^{s_\ell}}=a_j.
\]

Choosing `b=max(s)` makes every exponential argument nonpositive. At least one
term is `exp(0)=1`, so a finite row cannot produce a zero denominator. Very
small probabilities may underflow to zero in floating point; this is not exact
real arithmetic. Inputs must still be finite: subtracting a maximum cannot
repair an already infinite dot product. Our implementation rejects such inputs
and intermediates, including overflow, instead of silently claiming a result.

**Worked case:** `s=[1000,1000+ln(3)]`. Direct exponentials overflow in common
binary64 arithmetic. After subtracting the maximum, exponentials are `[1/3,1]`;
normalizing gives `[1/4,3/4]`. Their sum is one, despite the large common offset.
A common offset changes neither weights nor output. Scaling all scores changes
the differences, so it generally changes the weights.

## Why the square-root scale has assumptions

Assume independent coordinates with `E[q_r]=E[k_r]=0`, unit variance, and
independence across coordinates and between q and k. Then
`E[q_r k_r]=0` and `Var(q_r k_r)=E[q_r²]E[k_r²]=1`. Covariances vanish under
these assumptions, so `Var(sum_r q_r k_r)=d`. Dividing by `sqrt(d)` makes that
variance one. This is an argument about a specified random model, not a bound
for arbitrary learned vectors.

**Counterexample:** choose every query/key coordinate as one. The first key
score is `d/sqrt(d)=sqrt(d)`; a zero second key scores zero. The first weight is
`1/(1+exp(-sqrt(d)))`, approaching one as `d` grows. Scaling moderates this
concentration but does not prevent it. The executable experiment deliberately
uses this counterexample, rather than claiming that any vectors satisfy the
independence assumptions.

## Differentiate the mechanism, one edge at a time

Suppose an upstream loss has supplied the vector `g = dL/do`. We want changes
to q, each key, and each value without recomputing a separate whole graph for
every scalar. First, value mixing is linear:

\[
\frac{\partial L}{\partial v_j}=a_jg,\qquad
 r_j\equiv\frac{\partial L}{\partial a_j}=g^T v_j.
\]

Next differentiate the softmax. The denominator depends on **every** score.
For the matching coordinate use the quotient rule; for other coordinates only
the denominator changes:

\[
\frac{\partial a_j}{\partial s_\ell}=a_j(\mathbf1[j=\ell]-a_\ell).
\]

A full Jacobian would have `m²` entries, but the chain rule lets us multiply it
by `r` without storing the matrix:

\[
 t_\ell\equiv\frac{\partial L}{\partial s_\ell}
 =a_\ell\left(r_\ell-\sum_j a_jr_j\right).
\]

Finally differentiate each dot product:

\[
\frac{\partial L}{\partial q}=\sum_j t_jk_j/c,\qquad
\frac{\partial L}{\partial k_j}=t_jq/c.
\]

`attention_backward` follows exactly these stages. It holds key selection
fixed: discrete changes in sequence length or mask selection are not variables
of this derivative. Gradients through `q=xW_Q` require another chain-rule step;
they are not returned by this isolated routine.

### Complete scalar worked example

Let `q=1`, `k=[0,ln(3)]`, `v=[2,6]`, `c=1`, and let `L=o`. Scores are
`[0,ln(3)]`, weights `[1/4,3/4]`, and output `o=5`. Since `g=1`,
`r=[2,6]`; its weighted mean is `5`. Thus `t=[(1/4)(2-5),(3/4)(6-5)]`
`=[-3/4,3/4]`. We obtain:

- `dL/dq = (3/4)ln(3)`;
- `dL/dk = [-3/4,3/4]`;
- `dL/dv = [1/4,3/4]`.

The score gradients sum to zero. This agrees with the offset invariance just
derived: increasing every score by the same amount leaves the output fixed.
With only one key, its weight is always one. q and K gradients must be zero;
the payload gradient remains `g`. This edge case catches a derivative that
incorrectly treats the softmax denominator as a constant.

## Masking is selection, not cleanup

At position i, call the primitive with pairs `0..i`, then append zeros to the
returned weight row for display. The forbidden values never enter its
normalization. For scores `[0,0,20]`, allowing only the first two entries gives
weights `[1/2,1/2]`. Normalizing all three and then deleting the third yields
a row sum near `4.12e-9`; most probability mass has been thrown away. Failing
to renormalize changes even a constant payload's output. Renormalizing after
softmax can still have poor numerical behavior after allowed terms underflow;
selecting first avoids this avoidable issue.

Causality of a layer is a conditional guarantee: earlier input vectors must
also be independent of future information. A perfect mask cannot undo future
labels already embedded into the input by an upstream data pipeline.

## Derive incremental decoding and its invariant

At generation step t we need only the newest query's output. Earlier inputs
and fixed projection matrices imply unchanged earlier keys and values. Retain
those projections instead of recomputing them. `CausalCache.step(token)`:

1. Projects the new token once into q, k and v.
2. Reads the old K/V prefix plus the new pair.
3. Computes the new output over precisely that permitted prefix.
4. Appends the pair only after the operation validates successfully.

**Invariant after t successful steps:** the stored arrays equal projections
of exactly the t accepted inputs, in insertion order. Prove by induction.
The empty state satisfies it. The step computes the next projection with the
same fixed matrices, reads the prefix guaranteed by induction, then appends.
Therefore its newest output equals the last row of a full causal call, subject
to floating-point tolerance. Rejected inputs leave state unchanged.

This does not cache a whole decoder. A real multilayer model must maintain
per-layer state and consistent positions, masks and model parameters. If
weights change, old projections are stale. Mixing two users in one cache leaks
state. Here every sequence gets its own instance; `clear()` resets it. The
class has no locking, eviction, batch management, positional encodings or
security boundary. Treat it as local educational state.

## Count work before interpreting timings

For n tokens, one triangular full call evaluates `n(n+1)/2` query/key pairs.
Incremental cached generation evaluates `1+2+...+n`, the same count. The cache
**does not speed up an isolated full-sequence call by changing that count**.
Its comparison is generation that repeatedly calls full attention on every
prefix and discards all but the last row. That naive alternative evaluates
`sum_{t=1}^n t(t+1)/2 = n(n+1)(n+2)/6` pairs. Projections fall from
`3*n(n+1)/2` vectors to `3*n` when cached. Another baseline could recompute
prefix K/V but only calculate the last query; it already avoids the cubic
score count while still repeating projections.

The cache stores `n*(d+v)` scalar payloads; Python object overhead adds more
bytes. Returning a full n-by-n weight display also consumes quadratic storage.
Actual speed depends on validation overhead, allocation, device and kernels.
No GPU speed claim follows from this Python experiment.

Attempt [the exercises](EXERCISES.md) before opening hints or solutions. Then
use [the experiment protocol](EXPERIMENT.md) to turn predictions into evidence.
