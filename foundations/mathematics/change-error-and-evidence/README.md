# Change, numerical error, and evidence

Prepared original unit F-NUM. Learner mastery: NOT STARTED. This bounded unit
teaches the mathematics needed to distrust a plausible numerical output for the
right reason. It does not replace a calculus or statistics course. The broader
foundation remains PARTIAL. Source claims are mapped in [SOURCES](SOURCES.md);
the calculations below are original derivations.

## The concrete problem

A robot crosses a nominal 10 m track in 2 s. Its software reports 5 m/s. Another
implementation prints 5.000000000000000 m/s. Neither output says how carefully
distance/time were measured. Meanwhile a simulator estimates instantaneous
velocity by subtracting two nearby positions. Making the time step extremely
small can make that estimate worse. We need to distinguish three questions:

1. What exact quantity does our mathematical model define?
2. How faithfully does finite arithmetic implement it?
3. How well do the observations support the model of the real system?

An exact computation on a biased input can answer the first two and fail the
third. This distinction connects numerical methods to electronics measurement,
ML gradient checks, control simulation, and experimental reproducibility.

## Prerequisite bridge

Read [counting and units](../counting-and-units/README.md) and
[finite representations](../finite-representations/README.md) first. Here is the
remaining algebra you need. A function maps an allowed input to one output:
`s(t)=t*t` maps a time to a position in a model with a declared coefficient.
Changing `t` changes `s`; evaluating a function is different from solving for its
input. `(t+h)^2=t^2+2th+h^2` follows by multiplying both factors. A ratio `a/b`
requires `b != 0`. Squaring a quantity squares its units.

The symbol Σ means add the indexed terms. For four values, Σx_i=x_1+x_2+x_3+x_4.
An average is their sum divided by four. A square root is the nonnegative number
whose square is its argument. These definitions suffice for the worked examples.

| Dependency | What is assumed here |
| --- | --- |
| Mathematics | Signed arithmetic, fractions, variables; needed algebra is taught above |
| Physics | Distance in m and duration in s; no mechanics theorem assumed |
| Electronics | Not required; later RC application supplies its circuit assumptions |
| Chemistry/materials | Not required for synthetic numerical experiments |
| Statistics/probability | Introduced below; independence must be justified in a real experiment |
| Programming | Python functions, loops, lists, exceptions; reference code is readable alongside derivations |
| Prior systems | Binary approximation from finite representations; no OS knowledge needed |

If these operations cannot yet be explained unaided, study them before treating
the dependent hardware or optimization lesson as ready. Reading this page is not
evidence of passing that gate.

## 1. From average change to local change

For a position function s(t), the average velocity over `[t,t+h]` is

\[
D_h^+s(t)=\frac{s(t+h)-s(t)}{h},\quad h>0.
\]

The numerator is a displacement, not the absolute position. Its units are m;
dividing by s yields m/s. Earlier measurements over intervals are sufficient
when we only need an average. To describe change at one instant we ask whether
these averages approach a single value as the interval shrinks.

Define the derivative s'(t) as the limit of the quotient as h tends to zero,
including consistent approach from both sides when both are in the domain.
This is not substitution of zero: a quotient with zero denominator is undefined.
A limit L means that outputs can be made arbitrarily close to L by restricting
nonzero h sufficiently near zero.

Take `s(t)=a*t^2`, where a=1 m/s². At t=2 s, s=4 m; at t=2.1 s, s=4.41 m.
The finite-interval velocity is 0.41/0.1=4.1 m/s. Expand before taking a limit:

\[
\frac{a(t+h)^2-at^2}{h}
=\frac{2ath+ah^2}{h}=2at+ah\longrightarrow 2at.
\]

Every cancellation used h nonzero. At t=2 s the instantaneous velocity is 4 m/s.
The forward estimate exceeds it by a*h, here 0.1 m/s. Halving h halves this
particular model error. This is a derived property of this polynomial, not a
promise about every function or machine.

A central estimate uses both sides:

\[
D_h^0s(t)=\frac{s(t+h)-s(t-h)}{2h}.
\]

Expanding the two squares gives 4ath/(2h)=2at exactly in real arithmetic. That
special exactness can hide numerical weaknesses. For `f(x)=x^3`, expansion gives
forward `3x²+3xh+h²`, central `3x²+h²`, and derivative `3x²`. Thus, at x=1,
central truncation error is h², while forward error is 3h+h². This is why our
experiment uses a cubic rather than a quadratic.

**Counterexample:** for f(x)=|x| at x=0, the central quotient is zero at every h,
but the right-hand quotient is +1 and the left-hand quotient is -1. There is no
derivative. A stable-looking numerical answer is insufficient to establish one.

## 2. Finite arithmetic changes the experiment

Our exact algebra assumes arbitrarily precise numbers. A binary float stores
a finite significand and exponent, so its spacing depends on magnitude. On a
typical binary64 implementation, 1.0+1e-20 rounds back to 1.0. Observe this with
Python; inspect `sys.float_info` rather than assuming every runtime has the same
format. Goldberg's inspected floating-point discussion supports the distinction
between rounding and cancellation [S-FLOAT].

If two evaluations each carry absolute error bounded by δ, subtracting them
can leave numerator error as large as 2δ. Dividing by h gives a bound 2δ/h for
that component of the forward error. This elementary bound follows by applying
the triangle inequality to the two evaluation errors. It is not a universal
δ bound for arbitrary user functions.

For the cubic central quotient, a useful model is therefore

\[
E(h)\approx Ah^2+B\epsilon/h.
\]

The first contribution shrinks; the second grows. Equating their magnitudes
suggests h on the order of ε^(1/3) when A and B have comparable scale. It is a
step-selection heuristic, not an optimum for an unknown function. Evaluation
noise, units, very small derivatives, discontinuities, and input rounding change
the constants or invalidate the model. There can also be fortunate exact
cancellation at individual steps; error need not increase monotonically.

Read `difference` in [numerics.py](numerics.py). Its inputs are a function, point,
positive step and method. Its outputs are a finite slope or an exception. It
checks finite endpoints, distinguishability, finite evaluations and finite slope.
It uses the *actual representable span*, `right-left`, in the denominator. If
rounding makes the central endpoints asymmetric, it measures the secant around
their midpoint, which is near the requested point. No error bound or smoothness
proof is returned. Function-domain exceptions propagate; do not hide them as zero.

Operation count is O(1) evaluations, but their cost belongs to the supplied f.
The helper has no mutable global state. Use per-request functions in concurrent
software and record their versions and data; this helper cannot make a stateful
or nondeterministic f reproducible. Reject unreasonable workloads at a service
boundary rather than exposing arbitrary callable execution to untrusted users.

## 3. What repeated measurements can estimate

Let x_i=μ+b+e_i, where μ is the target, b is an unknown common offset, and e_i
is fluctuating error with zero mean. For independent e_i with common variance
σ², the average error has variance

\[
\operatorname{Var}\!\left(\frac1n\sum_i e_i\right)
=\frac1{n^2}\sum_i\operatorname{Var}(e_i)=\frac{\sigma^2}{n}.
\]

Variance is expected squared distance from a mean. Cross terms vanish here
because independence with zero means gives E[e_i e_j]=0 for distinct i,j.
Independence is stronger than necessary; uncorrelated errors suffice for this
calculation. Correlated drift makes the omitted covariance terms matter.

Estimate sample variance by s²=Σ(x_i-x̄)²/(n-1). Why n-1? Let m=μ+b be the population mean of the observations; it includes
the common offset. Expanding around m gives
Σ(x_i-x̄)²=Σ(x_i-m)²-n(x̄-m)². Expectations under independent, identical
draws are nσ²-σ²=(n-1)σ². Dividing by n would systematically underestimate σ²
in this model. The estimated standard error of the mean (SEM) is s/√n. This
derivation agrees with NIST's inspected Appendix A.4–A.5 [S-UNCERTAINTY].

For synthetic timing readings `[0.98,1.00,1.02,1.00]` s:

1. Mean =4.00/4=1.00 s.
2. Deviations are -0.02,0,+0.02,0 s.
3. Sum of squared deviations =0.0008 s².
4. Sample variance =0.0008/3≈0.000266667 s².
5. SEM =√(0.000266667/4)≈0.008165 s.

Adding +0.10 s to every reading shifts the mean to 1.10 s and leaves all
deviations unchanged. The estimated SEM remains the same. Precision of repeated
measurements has not detected the offset. Calibration, a reference or a revised
measurement model is needed. SEM is neither a bound on total error nor a
95% interval. No confidence interval is implemented here.

Copying each observed reading 100 times also does not provide 400 independent
observations. The formula produces a smaller number, but its interpretation is
invalid. Similar pseudoreplication occurs with duplicate ML examples, repeated
sensor readings of one event, and repeated requests served from the same cache.

The implementation uses two passes: an accurately accumulated mean, then squared
centered deviations. The alternative `Σx²-(Σx)²/n` subtracts large nearby terms.
For readings near 10^9 with spread near one, rounding can overwhelm the variance.
Compare against an exact Fraction oracle in the tests. Two passes still have
finite range/rounding limitations; `fsum` is not exact real arithmetic [S-PY-MATH].

## 4. How uncertainty moves through a computation

Speed v=d/t has two inputs. The distance sensitivity with t fixed is 1/t.
For a small time perturbation Δt with d fixed, exact algebra gives

\[
\frac{d}{t+\Delta t}-\frac dt
=\frac{-d\Delta t}{t(t+\Delta t)}\approx-\frac d{t^2}\Delta t.
\]

The approximation replaces t+Δt by t and requires |Δt| much smaller than |t|.
Adding the first-order effects gives Δv≈Δd/t-dΔt/t². Squaring and averaging this
linear expression yields

\[
u_v^2=(u_d/t)^2+(d u_t/t^2)^2
-2(d/t^3)\operatorname{Cov}(d,t).
\]

Write covariance as ρ u_d u_t, where -1≤ρ≤1. Covariance records whether input
deviations tend to move together. For 10 m, 2 s, u_d=0.1 m and u_t=0.02 s,
uncorrelated contributions each have magnitude 0.05 m/s. Their root sum of
squares is √0.005≈0.07071 m/s. The output standard uncertainty is in m/s.
Adding uncertainties directly would be a different, worst-case-bound model.

With perfect positive correlation and these equal relative uncertainties, the
linear contributions cancel. Perfect negative correlation reinforces them to
0.1 m/s. In a real instrument, justify ρ; do not tune it to reduce a reported
uncertainty. NIST's propagation formula includes covariance and is explicitly
first order [S-UNCERTAINTY]. Near t=0, large relative uncertainty or a distribution
crossing zero destroys this approximation; a tiny calculated value is no rescue.

## 5. Guided build and experiment

Python 3.10+ standard library is sufficient. From the repository root:

```sh
python3 -m unittest discover -s foundations/mathematics/change-error-and-evidence -v
python3 foundations/mathematics/change-error-and-evidence/experiment.py
```

Before opening the implementation, build these milestones in a scratch copy:

1. Expand the quadratic and cubic differences on paper. Predict errors at h=0.1
   and 0.01. Deliver the expansions and units.
2. Implement a forward secant. Add finite-input and indistinguishable-step
   rejection. Intentionally remove the latter; record the misleading outcome.
3. Implement central secants. Test a linear function, cubic, and |x| at zero.
   Explain why the last test must not assert the existence of a derivative.
4. Implement mean, centered sample variance and SEM. Check a four-value dataset
   by hand, then translate and rescale it; variance must scale quadratically.
5. Derive speed sensitivities and include correlation. Compare with a small
   direct perturbation; increase the perturbation until linearization fails.
6. Run the experiment protocol below. Deliver raw JSON, predictions, failure
   interpretation, and a short account of what it does not establish.

**Question:** does decreasing h always improve a derivative estimate, and does
a smaller SEM establish a more accurate measurement?

**Hypotheses:** central cubic error initially decreases approximately with h²;
rounding eventually changes that trend. Adding a constant measurement offset
changes the mean while preserving SEM. Copying records can reduce the reported
SEM without adding information.

**Controls:** same cubic, x=1, Python executable, method per comparison and
deterministic synthetic arrays. **Independent variables:** step, common offset,
copy count. **Instrumentation:** absolute error against derivative 3; Fraction
oracle for variance; metadata records Python and platform. **Procedure:** run
the script once; retain all 18 step rows, including rejections. Never replace
failed rows with an expected value. **Measurements:** error, mean, variance, SEM.

Actual agent-run evidence and interpretation are in [RESULTS](RESULTS.md).
This is a deterministic software experiment, not a physical timing measurement
or evidence of learner competence. Alternate explanations for the derivative
curve include endpoint rounding and cancellation in evaluations; a single
curve cannot estimate a universal error law. Repeat with a different polynomial,
large x, and a noisy evaluation function as follow-ups.

Attempt [EXERCISES](EXERCISES.md), consult [HINTS](HINTS.md) only after an attempt,
then compare [SOLUTIONS](SOLUTIONS.md). The final transfer task connects to
[RC dynamics](../../../hardware-electronics-mastery/02_RC_TRANSIENTS.md).
