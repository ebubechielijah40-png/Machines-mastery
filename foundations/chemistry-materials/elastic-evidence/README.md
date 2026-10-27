# From atomic energy to a material measurement

A motor bracket can deflect even when its net force is zero. A tensile tester can
report a straight line and still give the wrong modulus. This unit derives both
behaviors, then uses a controlled synthetic experiment to separate specimen
compliance from instrument compliance. Its purpose is to connect matter,
mechanics, measurement and inference before treating a material property as a
trusted input to a machine design.

Read [algebra/functions](../../mathematics/core/01_ALGEBRA_FUNCTIONS.md),
[local derivatives and integration](../../mathematics/core/04_CALCULUS_OPTIMIZATION.md),
[force and energy](../../physics/MOTION_ENERGY.md) and
[variation versus bias](../../mathematics/change-error-and-evidence/README.md).
The uncertainty section additionally uses independent random errors and variance.
All numerical material and instrument parameters here are **assumptions**, not
measurements or certified specifications. [Sources and exact scope](SOURCES.md)
separate physical concepts from our original calculations.

## 1. Why atoms can form a stable spacing

An atom consists of a positive nucleus and electrons described by quantum
states. Electrons are not little planets following a classical orbit. A nucleus
contains protons and, except for the simplest hydrogen isotope, neutrons;
electron count determines the charge of an isolated atom. Atomic number counts
protons, not the total mass. Sharing or transferring electronic charge and
allowing it to occupy extended states gives different bonding descriptions.
These descriptions help organize observations; a short sketch does not solve a
many-electron quantum system.

Here is a deliberately specified *effective energy*, not a quantum calculation:

\[
 U(r)=\frac{D}{m-1}\left[\left(\frac{r_0}{r}\right)^m-
 m\frac{r_0}{r}\right],\qquad D>0,\ r>0,\ m>1.
\]

The separation is r in meters, D is an energy in joules and m is dimensionless.
The two terms have competing slopes. The steep positive term resists close
approach; the negative term favors a bound separation. The zero of energy is
at infinite separation. This is a normalized member of the attractive/repulsive
family in the inspected Roylance source, not a fit to any named material.

Set q=r0/r. At r=r0, q=1 and U=-D. The slope is

\[
 F_{\rm required}=\frac{dU}{dr}
 =\frac{Dm}{(m-1)r_0}(q^2-q^{m+1}).
\]

Why the derivative? Moving quasistatically by dr requires work F_required dr;
its integral equals the change in potential energy. The internal restoring
force is the **negative** of this derivative. Confusing the required external
force with the internal force reverses the stability argument.

At r0 the slope is zero. Differentiate again:

\[
 U''(r)=\frac{Dm}{(m-1)r_0^2}
 [(m+1)q^{m+2}-2q^3],\qquad k=U''(r_0)=\frac{Dm}{r_0^2}>0.
\]

For a small displacement x, Taylor expansion gives U(r0+x) approximately
-D+kx²/2, so the required force is approximately kx. The constant k has units
J/m²=N/m. The microscopic energy model therefore supplies a spring law near a
stable minimum. Zero slope alone is insufficient: an energy maximum also has
zero slope, but a small perturbation moves the system away.

With invented D=10^-19 J, r0=2×10^-10 m and m=8, k=20 N/m. A small x=10^-12 m
requires about2×10^-11 N in the linear approximation. Compute the exact value
before assuming the approximation is accurate. A quadratic approximation is
local; stretching toward infinity eventually costs only D, while a quadratic
spring predicts unbounded work. That disagreement identifies the approximation's
limit rather than a violation of energy conservation.

The maximum required tensile force occurs where U''=0:

\[
 r_{\rm peak}/r_0=[(m+1)/2]^{1/(m-1)}.
\]

For m=8 this ratio is about1.23969849 in the executed model. Under a fixed force
F, the relevant local energy is U(r)-Fr. A stationary separation is locally
stable only where U''>0. A displacement clamp changes the constraint; it can
hold a point on the descending force branch. Consequently a peak in this ideal
pair law is not a measured breaking load or a complete model of crack growth.

## 2. From a spring to a bar, with geometry made explicit

Consider n identical bonds in series per chain and p chains in parallel, with
spacing r0 and square cross-sectional cell area r0². Each chain has compliance
n/k; parallel chains share force, so the total compliance is n/(pk).
The length is L=nr0 and area A=pr0². Define axial stress σ=F/A and strain ε=δ/L.
Then

\[
 E=\frac{\sigma}{\epsilon}=\frac{k}{r_0}.
\]

This result follows from this particular ideal geometry. It gives100 GPa for
the invented bond parameters. Real crystals have directions, transverse
contraction, more neighbors and non-pair interactions; polymers can also have
important configurational/entropic elasticity. Substituting an atom spacing
into this toy expression does not determine a real material's modulus.

At the continuum level, take an assumed constant modulus E and use σ=Eε. Solving
F/A=Eδ/L yields

\[
 \delta=\frac{FL}{AE},\qquad C_s=\frac{\delta}{F}=\frac{L}{AE}.
\]

C_s is compliance in m/N; its reciprocal is structural stiffness in N/m.
Modulus E is in Pa=N/m². A long thin bar and a short thick bar of the same
material can have different stiffness while having the same assumed modulus.
That distinction prevents a common category error when comparing structures.

For L=.1 m, A=10^-6 m², E=200×10^9 Pa and F=50 N:

1. σ=50/(10^-6)=50×10^6 Pa.
2. ε=50×10^6/(200×10^9)=.00025.
3. δ=.1×.00025=25×10^-6 m=25 micrometers.
4. The quasistatic loading work is ∫0^δ (x/C_s)dx=Fδ/2=.000625 J.

Equal opposite end forces give zero net translation while leaving this internal
stress and stored energy. Zero net force does not mean zero internal force.
For compression the signed δ and F are negative, while Fδ/2 remains positive.
The axial formula omits buckling; it cannot certify a slender compressed column.

For several bars in series the same force crosses every element, so extensions
add and C_total=ΣC_i. In parallel all elements have the same extension and forces
add, so 1/C_total=Σ1/C_i. Derive these from the declared boundary conditions
before choosing a formula. The implementation compares them against exact
rational arithmetic. These relations also explain why fixture compliance can
contaminate a specimen measurement.

Elastic means recoverable deformation; linear means proportional response.
Those are different properties. Plastic strain remains after unloading. Fatigue,
creep, defects, corrosion and temperature can matter even when a small initial
slope looks linear. This unit has no plastic state, rate dependence or crack
geometry, and its declared strain envelope is an input assumption, not a measured
elastic limit. It rejects loads outside that envelope rather than extrapolating
silently.

## 3. The inverse problem: measuring the wrong spring accurately

Suppose an instrument reports actuator travel rather than specimen-only extension:

\[
 y_i=b+(C_s+C_f)F_i+e_i.
\]

Here b is a zero offset in meters, C_f is frame/grip compliance in m/N and e_i is
an additive measurement error. Even if e_i=0, fitting y against F identifies only
the total slope s=C_s+C_f. Repeating the same experiment reduces random scatter
but cannot reveal the separate terms.

At L=.1 m and A=10^-6 m², these two parameter pairs predict the same slope:

| Assumed modulus | Assumed frame compliance | Total slope |
| --- | --- | --- |
|200 GPa |10^-7 m/N |6×10^-7 m/N |
|250 GPa |2×10^-7 m/N |6×10^-7 m/N |

No number of exact observations at that one length distinguishes them. This is
**non-identifiability**, a property of the observation model. A lower numerical
residual does not supply the missing information.

If the frame is ignored, the first case gives apparent modulus
E_app=L/(As)=166.666… GPa. The input200 GPa has not changed; the interpretation
of the measured travel is wrong. If the frame compliance is independently known,
subtract it before inversion: E=L/[A(s-C_f)]. A nonpositive corrected compliance
contradicts this model and must be investigated.

A different experiment can identify both parameters. Keep the same cross section
and frame, but use lengths L1<L2:

\[
 s_2-s_1=\frac{L_2-L_1}{AE},\quad
 E=\frac{L_2-L_1}{A(s_2-s_1)},\quad C_f=s_1-\frac{L_1}{AE}.
\]

This argument requires the frame/grip behavior to stay the same. Changing grips,
slippage or specimen diameter can invalidate the cancellation. Very similar
lengths make s2-s1 small and amplify error. An unphysical negative fitted C_f is
retained as a diagnostic, not clipped to conceal a contradiction.

## 4. Fit an intercept and inspect the residuals

To minimize Σ(y_i-b-sF_i)², use the sample means and centered quantities:

\[
 S_{FF}=\sum(F_i-\bar F)^2,\quad
 s=\frac{\sum(F_i-\bar F)(y_i-\bar y)}{S_{FF}},\quad
 b=\bar y-s\bar F.
\]

A direct justification avoids memorizing a library command. After setting
b=mean(y)-s mean(F), expand the centered squared residual sum as a quadratic in
s. Completing the square leaves its minimum at the displayed ratio when S_FF>0.
All loads equal gives S_FF=0; there is then no identifiable slope. The residuals
must satisfy Σr_i≈0 and ΣF_i r_i≈0, which are independent checks on the fitted
normal equations. Small residuals still do not rule out an unobserved frame term.

Forcing b=0 gives s0=ΣF_i y_i/ΣF_i². If the true offset is positive, this adds
bΣF_i/ΣF_i² to the slope for positive loads. The apparent specimen becomes even
softer. This is an incorrect modeling constraint, not a floating-point bug.

With n>2 fixed accurately known loads and independent zero-mean errors of common
variance, estimate residual variance by s_e²=Σr_i²/(n-2), then standard uncertainty
of the fitted slope by u_s=s_e/√S_FF. The two lost degrees of freedom correspond
to the fitted intercept and slope. Correlated drift, force errors, nonlinear
response or a changing frame invalidate this simple uncertainty calculation.

For E=L/(AC_s), first-order propagation with independent input uncertainties gives

\[
 (u_E/E)^2\approx(u_L/L)^2+(u_A/A)^2+(u_{C_s}/C_s)^2.
\]

This follows by differentiating the product/reciprocal relation and combining
variances. It is a local approximation, not a guaranteed error bound. If
A=πd²/4, its relative sensitivity to diameter is2u_d/d; confusing diameter with
area underestimates geometric uncertainty. Common calibration errors introduce
covariance terms; independent repetition does not remove them.

## 5. Build, inspect and reconstruct

```sh
python3 -m unittest discover -s foundations/chemistry-materials/elastic-evidence -v
python3 foundations/chemistry-materials/elastic-evidence/experiment.py
```

[materials.py](materials.py) is runnable reference code. It uses SI inputs,
explicit finite-range rejection, bounded iterable lengths, immutable parameters
and no external packages. Tests independently check derivatives by central
differences, series/parallel and fits with exact Fractions, energy/sign/scaling,
identifiability and invalid inputs. Numerical agreement is evidence for declared
contracts, not proof of a material theory.

Build in milestones: (1) hand-calculate the bar case; (2) implement response and
unit checks; (3) derive and test bond derivatives; (4) write centered fitting with
independent residual checks; (5) retain the single-length counterexample;
(6) identify two lengths and examine residuals; (7) change a hidden assumption
and explain why the conclusion changes. Give each stage a test and a short
interpretation before consulting the reference.

Read the [experiment protocol and actual results](EXPERIMENTS.md). Attempt
[the exercises](EXERCISES.md) before opening [hints](HINTS.md) or
[solutions](SOLUTIONS.md). For the memory reconstruction, begin from a blank file,
rederive the compliance and inverse equations, rebuild an identifying experiment,
and explain why a perfect one-length fit cannot establish modulus.

This unit prepares material-property reasoning for
[transistor/logic models](../../../hardware-electronics-mastery/03_SEMICONDUCTORS_TRANSISTORS.md)
and [motor/control assumptions](../../../17-embedded-robotics/control-path/README.md).
Neither connection supplies the missing quantum chemistry, manufacturing,
nonlinear constitutive laws or real instrument calibration.
