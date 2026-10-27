# From a ringing trace to a falsifiable machine model

A detector rises, crosses its baseline, and rings down. Is it a spring, an
electrical resonator, a delayed feedback controller, or an instrument artifact?
Recognizing a curve is not reconstructing a machine. A useful investigation
asks which controlled interventions separate the surviving explanations and
which claims remain unidentifiable at the observed boundary.

This original investigation extends the supplied hidden-state and native binary
cases to a physical-style port. It is a fully executed software experiment,
not physical reverse engineering of an unknown device. Read the [prompt](prompt.md)
before the reveal. The reference is intentionally limited to a linear,
constant-coefficient, underdamped second-order model, an affine detector and
constant drives. A good fit cannot establish that every real system belongs
to that family.

## Prerequisites and a useful entry task

Study [quantities/units](../../../foundations/mathematics/counting-and-units/README.md),
[algebra, maps and calculus](../../../foundations/mathematics/core/README.md), and
[initial-value dynamics](../../../foundations/mathematics/initial-value-evidence/README.md).
The [RC transient unit](../../../hardware-electronics-mastery/02_RC_TRANSIENTS.md)
connects an equation to measurement loading. You need to solve two linear
equations, interpret a derivative, multiply complex conjugates and distinguish
an initial value from a parameter. The bridge below introduces the remaining
mechanisms rather than requiring an external identification tutorial.

Entry task: if a detector reads15 at q=-.01 and35 at q=.01, determine its gain,
offset and reading at q=0. Answer:1000counts/Q,25counts,25counts. Explain why
subtracting25 must precede converting a free-response reading into a coordinate.

## Declare the boundary before choosing an internal story

The inputs are reset initial coordinate q0, initial rate v0 and a constant
drive u. The hidden state is `(q,v)` and the observed output is a detector
reading y. Under the proposed model,

\[
\dot q=v,\qquad a\dot v=u-bv-cq,\qquad y=gq+o+\epsilon.
\]

a and c are positive; b is nonnegative; the chosen reference requires
`b²<4ac`. The detector gain g is nonzero and may be negative. The offset o is
not a mechanical displacement. The chosen pseudo-noise ε is in detector counts.
This equation has two state variables because the future depends on both
position and velocity; knowing q alone does not identify whether the system
is moving toward or away from equilibrium.

For a mass connected to an ideal linear spring and viscous damper, Newton's
force balance gives `m q''=u-b q'-k q`, so a=m,c=k. For a series ideal RLC
port whose coordinate is capacitor charge, define current I=q'. Resistor,
inductor and capacitor drops are `RI`, `L I'`, `q/C`; summing them gives
`L q''+R q'+q/C=u`. Then a=L,b=R,c=1/C. The selected primary foundation
scopes are in [SOURCES](SOURCES.md); our identification procedure and numerical
cases are original constructions rather than reconstructions of those sources.

| Quantity | Mechanical interpretation | Electrical interpretation |
| --- | --- | --- |
| q | displacement,m | charge,C |
| v=q' | velocity,m/s | current,A |
| u | force,N | applied voltage,V |
| a | mass,kg | inductance,H |
| b | viscous coefficient,Ns/m | resistance,Ω |
| c | stiffness,N/m | inverse capacitance,1/F |

Multiply the governing equation by v. Product differentiation gives

\[
\frac{d}{dt}\left(\tfrac12av^2+\tfrac12cq^2\right)=uv-bv^2.
\]

The terms are stored energy, input power and dissipated power once units have
been assigned consistently. With u=0 and b≥0, this ideal model cannot create
energy. The numerical values of a,b,c alone do not reveal which physical unit
mapping applies. A real reconstruction needs evidence about ports, material,
motion or fields in addition to an input/output law.

## Separate instrument calibration from plant dynamics

With ε=0, two known references solve y=gq+o:

`g=(y1-y0)/(q1-q0)` and `o=y0-gq0`.

For copper, q=-.01 maps to14counts and q=.01 to6counts. Therefore
g=(6−14)/.02=−400counts/Q, o=10counts. A reading8 represents
`(8−10)/(−400)=.005Q`. A negative detector response is not negative stiffness.

The two-point calculation assumes an affine, stable instrument and trustworthy
reference coordinates. A third reference is a falsification probe for curvature;
repeated references can expose drift. When noisy, closer references make
`q1-q0` small and amplify reading error. The supplied clean calibration is an
ideal premise, not a claim of calibrated real apparatus.

At a settled constant drive, q'=q''=0, so `u=cq`. Two drive/reading pairs give
`c=(u1-u0)/(q1-q0)` after calibration. Differences eliminate a constant external
bias only if that bias does not change between trials. This balance mode returns
the exact ideal equilibrium; the software does not simulate waiting until a
system has physically settled. A real experiment must establish a settling
criterion and uncertainty rather than declaring the last sample equilibrium.

## Derive a recurrence rather than numerically differentiating noisy samples

For a zero-drive release, try q=e^(st). Dividing by the nonzero exponential
gives `a s²+b s+c=0`. Complete the square to write roots as

\[
s=-\alpha\pm i\omega,\qquad
\alpha=b/(2a),\qquad \omega=\sqrt{c/a-\alpha^2}.
\]

Thus q(t)=e^(-αt)[Acos(ωt)+Bsin(ωt)]. q(0)=q0 sets A=q0;
differentiation gives `q'(0)=-αA+ωB=v0`, hence `B=(v0+αq0)/ω`.
The decay is not periodic even though its trigonometric factor repeats.

Uniform samples z_n=q(nh) are a combination of powers of
`λ=e^((-α+iω)h)` and its conjugate. Each power satisfies

`z[n+2]-(λ+conj(λ))z[n+1]+λconj(λ)z[n]=0`.

Define r=e^(-αh), θ=ωh. Then the real recurrence is

\[
z_{n+2}=A_dz_{n+1}+C_dz_n,
\qquad A_d=2r\cos\theta,\quad C_d=-r^2.
\]

This relation eliminates unknown initial sine/cosine weights. It avoids explicit
second differences divided by h², which amplify detector noise, but it does
not eliminate measurement error: noisy z[n] and z[n+1] are noisy regressors too.

For the clean amber fit with h=.05s, actual reconstructed values are
`A_d=1.957963917608469`, `C_d=-.9801986733067636`. Therefore
`r=sqrt(-C_d)≈.990049833749`, `α=-log(r)/h≈.2/s`, and
`ω=acos(A_d/(2r))/h≈2.993325909419rad/s`. From balance c≈18U/Q,
`a=c/(α²+ω²)≈2Us²/Q`, `b=2aα≈.8Us/Q`. Intermediate coefficients, raw
observations and hashes are preserved in the [executed record](EXPERIMENTS.md).

## Fit the recurrence and inspect its assumptions

Let x_n=z[n+1], y_n=z[n], t_n=z[n+2]. Minimize the squared residual
`S=Σ(t_n-A_d x_n-C_d y_n)²`. Setting each partial derivative to zero gives

\[
\begin{bmatrix}\sum x^2&\sum xy\\\sum xy&\sum y^2\end{bmatrix}
\begin{bmatrix}A_d\\C_d\end{bmatrix}
=\begin{bmatrix}\sum xt\\\sum yt\end{bmatrix}.
\]

Writing X=Σx²,Y=Σy²,Z=Σxy,P=Σxt,Q=Σyt and D=XY−Z²,
`A_d=(PY−QZ)/D`, `C_d=(QX−PZ)/D`. These are two-by-two elimination formulas,
not a hidden optimization library. The code first divides samples by their
maximum magnitude to reduce overflow/underflow without changing the ideal
coefficients; it returns residual RMS in the original coordinate unit.

If the two regressor columns are proportional, D=0 and many coefficients fit.
The diagnostic `D/(XY)` is an uncentered squared-angle separation, not a sample
correlation coefficient or confidence level. The implementation refuses
separation≤1e-12 as an explicit numerical heuristic. Normal equations square
the design matrix's condition number; QR/SVD and uncertainty-aware methods are
follow-up implementations, not capabilities supplied here. A nonzero determinant
also does not guarantee that the proposed physical model is true.

## Distinguish estimation from identification

Three counterexamples constrain what can be concluded.

1. **Coefficient scale.** Multiplying `(a,b,c)` by any positive factor leaves
   free dynamics unchanged after division by a. Models(2,.8,18) and(6,2.4,54)
   have the same free trace for the same initial state. A known constant drive
   distinguishes them because equilibrium u/c changes. Free decay identifies
   ratios b/a,c/a under the model, not all three absolute coefficients.
2. **Sampling aliases.** For a pure cosine release with v0=−αq0, frequencies
   ω and ω+2π/h have identical samples at nh. The principal `acos` branch
   returns a value between0 andπ/h and cannot prove the true frequency lies
   there. The experiment's3rad/s and34.4159265rad/s pair matches on h=.2s
   but differs by~.01719Q at t=.071s. An independently justified band bound
   or a new noncommensurate interval is additional evidence. Known initial
   velocity/other interventions can add constraints that this recurrence fit
   does not use; do not generalize one alias construction beyond its premises.
3. **Internal topology.** Amber and glass have identical numeric coordinate
   laws, detector maps and supported interventions. Their reveal assigns
   different physical interpretations. No query of that port can select
   one interpretation. Report the equivalence class, not a guessed internal
   diagram. More data of the same kind cannot answer a structurally absent
   question.

## Why faster sampling can make this estimator worse

In the actual controlled experiment, horizon10s, amplitude, calibration, balance
and bounded noise magnitude stay fixed while h takes .2,.05,.005s. Two seeds
are retained separately. At smaller h, neighboring noiseless samples become
nearly proportional. Changes due to dynamics shrink relative to the fixed
noise in each reading. This finite noisy-regressor estimator can then infer
excess damping or leave its allowed pole family despite receiving more samples.

For seed11 and .2count noise, estimated loss is~.8757 at h=.2 versus~5.3378
at h=.05; h=.005 is refused. The true fixture's loss is.8. These outcomes
are observations of this algorithm and noise model, not a theorem that sampling
faster is bad. A different estimator, smoothing, larger amplitude, calibrated
noise model or richer excitation can change the result. Reusing one seed does
not make the six trials independent physical replications.

Omitting the offset also permits a plausible-looking but false fit: this run's
inertia≈114.045 instead of2 and changed-drive holdout error≈.03883Q. A low
one-step residual alone is weak evidence when the instrument model is wrong.
Test a held-out initial state and drive, inspect structured residuals, and
predeclare acceptance tolerances instead of selecting them after seeing errors.

## Guided reconstruction, validation and transfer

1. Draw the observable boundary and write at least three alternative mechanisms.
   Record one intervention that could distinguish each pair and one that cannot.
2. Infer detector gain/offset from references, test a third coordinate and
   explain the unit conversion. Include a negative-gain case.
3. Use balance differences to identify c; derive the free recurrence by hand.
   Implement the2×2 solve and explicit singular/regime refusal.
4. Build the predictor from recovered a,b,c. Before querying, record predictions
   for q0=-.013,v0=.027,u=.31 at101 samples spaced .037s.
5. Execute clean holdout, offset mistake, fixed-horizon noise and alias/scale
   counterexamples. Save actual raw observations, source hashes and conditions.
6. Reveal the targets, identify what your evidence supported and what it could
   not establish, then rebuild the calibration, recurrence and predictor without
   the reference. Transfer to another supplied port and explain new assumptions.

Deliver the hypotheses log, independent predictor, tests, predictions, raw
records, failure interpretations and limits. Rubric:25points for boundary/units
and instrument reasoning;20 for derivation;20 for independent tests/holdout;
15 for negative controls;10 for reproducible evidence;10 for equivalence classes
and memory reconstruction. A passing total cannot compensate for inventing
physical measurements or asserting a unique topology from an equivalent port.

Use [exercises](EXERCISES.md), [hints](HINTS.md) and [explained solutions](SOLUTIONS.md)
in that order. The reference is [reconstruction.py](reconstruction.py); tests
include an exact Fraction recurrence and independently integrated first-order
RK4 state, not only comparison of two copies of the closed form.

```sh
python3 -m unittest discover -s reverse-engineering-systems/exercises/03-hidden-plant -v
python3 reverse-engineering-systems/exercises/03-hidden-plant/experiment.py
```

The local API caps horizon, count, values and input types, and the estimator
caps count/magnitude/conditioning. It is not an adversarial-code sandbox.
O(N) fitting uses O(N) stored samples and floating arithmetic. Real instrument
uncertainty, sampling jitter, backlash, friction, nonlinear stiffness, saturation,
hidden feedback, coupling, thermal drift and loading require new models and
measurements. No unknown hardware should be powered merely because this software
experiment is reproducible. [The physical-method chapter](../../21_MECHANICAL_ANALYSIS.md)
explains the transfer boundary, and [the reveal](reveal/README.md) maps the
synthetic coefficients after the investigation.
