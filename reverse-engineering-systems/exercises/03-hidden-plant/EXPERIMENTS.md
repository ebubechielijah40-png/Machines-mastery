# Executed synthetic investigation

Research question: which port parameters and internal claims survive calibration,
equilibrium, free release and changed-drive prediction? Secondary question: does
finer sampling necessarily improve this explicit noisy-regressor estimator?

Predictions from the model: clean calibrated releases plus equilibrium identify
the restricted principal-band coefficients; free release alone cannot identify
absolute coefficient scale or physical topology. A chosen alias pair matches on
one grid. Omitting the detector offset should fail intervention transfer.
At fixed noise magnitude, finer sampling can produce ill-conditioned regressors;
no monotonic accuracy improvement is guaranteed.

Controlled procedure: all four targets use clean references[-.02,.02]Q and
balance drives[-.3,.6]U. Fit a10s release at q0=.01Q,v0=0,u=0,h=.05s.
Reserve101 samples at h=.037s,q0=-.013,v0=.027,u=.31 for holdout. The separate
noise investigation keeps horizon10s and amplitude/reference/balance fixed,
changes h=.2,.05,.005s, applies.2count noise and retains seeds11 and17 separately.
The noise traces are different pseudorandom realizations, not matched physical
noise across sampling grids. Record that alternative explanation and limit.

Instrumentation: public oracle calls, exact Fraction recurrence tests, a separate
first-order RK4 state integration, known synthetic coefficients after reveal,
raw detector arrays, fit residual RMS/Gram separation, holdout absolute errors,
actual Python/platform versions and executable SHA256 hashes.

Executed from repository root:

```sh
python3 -m unittest discover -s reverse-engineering-systems/exercises/03-hidden-plant -v
python3 reverse-engineering-systems/exercises/03-hidden-plant/experiment.py
```

Raw [observation JSON](evidence/observed-2026-10-25.json) and
[12-test log](evidence/tests-2026-10-25.txt) are actual retained runs. A new run
should use stdout or a new filename; preserve the historical evidence. Tests
passing is not learner mastery, an all-input proof or physical validation.

| Actual case | Recovered(a,b,c),rounded | Changed-drive maximum absolute error,Q |
| --- | --- | ---: |
| amber | (2,.8,18) | 7.74e-15 |
| slate | (.75,.3,6.75) | 2.05e-14 |
| glass | (2,.8,18) | 7.74e-15 |
| copper | (1.25,1,5) | 1.97e-13 |

For seed11 at.2count noise, estimated loss is.8757175 at h=.2 and5.3377878 at
h=.05; h=.005 refuses a fit outside the conjugate-pole model. Seed17 gives
.9267808,5.3685449,and refusal respectively. The noiseless fixture's loss is.8.
The small-step fit's additional samples do not cure errors in its regressors.
These six cases are not statistical confidence intervals or universal estimator
comparisons. Calibration is intentionally noiseless, so the experiment does not
measure calibration uncertainty or a real detector's spectral properties.

The omitted-offset run fits a≈114.0446,b≈29.1770 with holdout error.0388252Q.
Its finite training residual does not establish the correct coordinate origin.
The alias pair3 and34.4159265rad/s differs by≤9.65e-17Q on h=.2s samples
but by.0171891Q at t=.071s. Models(2,.8,18) and(6,2.4,54) agree freely but
respond differently to a common nonzero drive. Amber/glass clean port observations
are equal. Thus actual numerical outcomes support the constructed nonuniqueness
claims under their declared premises, not unique internal reverse engineering.

Limitations: authored analytic fixtures, exact reset/settled balance, affine
detector, chosen pseudo-noise, fixed coefficients, constant drives, floating
normal equations and principal-band interpretation. No physical trials, hidden
controller rejection, real calibration, frequency-bound certification or unknown
firmware reconstruction took place. Independent sources were inspected only in
the [listed scopes](SOURCES.md).

Follow-up: predeclare an amplitude/noise grid, add a cubic stiffness mutant to
test residual/holdout refutation, compare QR and noise-aware estimators, implement
piecewise forcing with state-continuous segments, then design a genuinely
authorized instrumented apparatus study with uncertainty and loading evidence.
