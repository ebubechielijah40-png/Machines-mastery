# Executed numerical investigations

[The raw2026-10-25 run](evidence/observed-2026-10-25.json) contains actual UTC
time, Python/platform, unrounded values, retained energy samples and SHA256 of
the three executable source files. [The test log](evidence/tests-2026-10-25.txt)
records13 passing tests. These are newly executed **synthetic numerical models**;
no lost earlier observations, physical cart measurements or hardware timing
measurements were substituted. [experiment.py](experiment.py) reproduces the
procedure; preserve a new filename for a later run.

## Refine a mesh, measure a defined error

Question: how does endpoint error change whenh is halved fory'=-y,y₀=1,t_end=1?
Hypothesis: for this smooth nonstiff problem, Euler/Heun/RK4 approach error
ratios2/4/16. Hold model, initial state, endpoint, arithmetic and exact oracle
exp(-1) fixed; vary method and number of steps. Instrument absolute endpoint
error and field calls. Predictions are made from the local-order reasoning,
while the exact solution supplies an independent comparison.

| Steps | Euler error | Heun error | RK4 error |
| --- | --- | --- | --- |
| 8 | .0242705 | .00105380 | 8.30751e-7 |
| 16 | .0118053 | .000251098 | 4.92811e-8 |
| 32 | .00582415 | .0000613022 | 3.00081e-9 |
| 64 | .00289292 | .0000151459 | 1.85123e-10 |

The actual ratios support the stated prediction on these meshes. Equal steps
are not equal work: Euler spendsN,Heun2N andRK4 4N evaluations. A follow-up
should hold evaluation budget fixed. Another should investigate where roundoff
competes with truncation on much finer meshes. The current experiment neither
locates that crossover nor proves nonlinear RK4 order universally.

## A tiny fast state can dominate failure

Question: can an initially1e-6 mode destabilize an otherwise plausible slow
trajectory? Hold y'₁=-y₁,y'₂=-1000y₂,y₀=(1,1e-6),t_end=1 fixed; vary equal
step count and scalar forward/backward Euler. Predict growth whenever the fast
forward multiplier has magnitude>1. Record both components, rather than hiding
the fast component behind slow-state error.

| Steps | Forward fast state | Backward fast state | Forward slow error |
| --- | --- | --- | --- |
| 50 | 8.66323e57 | 7.74525e-73 | .00370976 |
| 200 | 2.58225e114 | 2.34288e-162 | .000921619 |
| 1000 | 0 | 9.33264e-308 | .000184016 |

At1000 forward steps,hk_fast=1 makes that numerical state zero after one step.
The exact mathematical fast state remains positive; its log magnitude,
log(1e-6)-1000=-1013.81551056, is retained because ordinaryexp underflows.
A printed zero is not a proof of exact extinction. Backward stability at a
coarse mesh does not resolve the fast transient accurately. This diagonal
controlled model excludes coupling and nonlinear stiffness; follow-ups should
introduce a justified coupling and measure its slow-state consequences.

## Conservation, amplitude and phase

Question: do smallh or bounded energy establish an accurate oscillator?
Holdω=2s⁻¹,x₀=1m,v₀=0,m=1kg,h=.05s,t_end=100s fixed. Change only integration
rule. Measure physical energy, the fixed-step modified invariant and endpoint
position error againstcos(ωt). Expected: Euler injects energy; symplectic Euler
preserves its modified quadratic while allowing phase slip.

| Rule | Final energy(J) | Endpoint position error(m) | Energy range(J) |
| --- | --- | --- | --- |
| Forward Euler | 8.7857241e8 | 3211.90264 | 2…8.7857241e8 |
| RK4 | 1.99994451 | .000151793 | 1.99994451…2 |
| Velocity-first symplectic Euler | 2.09965103 | .112612897 | 1.90476193…2.10526315 |

Maximum symplectic modified-energy drift is6.4393e-15 in this run, compatible
with finite arithmetic; physical energy oscillates. This confirms the stated
distinction on this model, not a universal conservation claim for nonlinear,
damped, forced or variable-step systems. RK4's smaller error here is not
universal superiority. Follow-ups should hold computation budget fixed, extend
the time horizon and separate phase from amplitude rather than inspecting
energy alone. No conservation law of real apparatus was measured.

## Adaptation reduces error here but cannot certify it

Holdy'=-5y,y₀=1,t_end=2,first_h=1 and the controller fixed; vary both absolute
and relative tolerance together. Predict more evaluations and lower endpoint
error for tighter values on this smooth case.

| Tolerance | Accepted/rejected | Field calls | Endpoint absolute error |
| --- | --- | --- | --- |
| 1e-4 | 9/2 | 132 | 3.13175825e-6 |
| 1e-8 | 44/3 | 564 | 6.37566463e-9 |
| 1e-12 | 261/4 | 3180 | 5.53077243e-12 |

The last error exceeds the absolute tolerance. The controller estimates local
agreement; it does not bound accumulated error by that same number. Counts
include rejected attempts. Component unit scaling is checked separately by
the metre/millimetre test, since inconsistent tolerances confound such a comparison.

For the lesson's smooth normalized pulse, one[0,1]attempt accepts0 after12calls,
despite exact integral1. Every sampled time lies outside(.1,.15). Supplying its
known support gives1.0000000004178091 after996calls with the same method and
tolerances. The independent exact polynomial integral checks a competing
explanation such as incorrect normalization. The contrast changes information
about the input interval; it does not demonstrate automatic feature detection.

The falsified claim is that two agreeing finite-sampling paths certify global
accuracy. A deliberately adversarial pulse does not estimate a typical miss
rate or show that adaptive integration is generally ineffective. Follow-ups
can impose a maximum step justified by known forcing bandwidth, supplied event
boundaries, or interval/derivative bounds. Each introduces additional information
or assumptions requiring evidence. Model/parameter/measurement uncertainty
remains separate from all these discretization experiments.

## Reproduce without overwriting history

```bash
python3 foundations/mathematics/initial-value-evidence/experiment.py > /tmp/ivp-new-run.json
python3 -m unittest discover -s foundations/mathematics/initial-value-evidence -v
```

Compare the deterministic numeric fields with a justified tolerance; timestamps,
platform strings and source hashes are provenance, not equality targets after
code/environment changes. No third-party Python dependency, external dataset,
account or instrument is required.
