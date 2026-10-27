# Which compliance did the instrument measure?

**Research question.** Can repeated load/travel measurements distinguish an
assumed specimen modulus from an unknown series frame compliance?

**Prediction.** One length identifies only their sum. Ignoring the frame reduces
the inferred modulus. Fitting an unjustified zero intercept introduces further
bias. Two lengths identify both terms if area/material/frame stay constant.

**Controls.** Keep assumed area10^-6 m², modulus200 GPa, frame compliance10^-7 m/N,
zero offset2 micrometers and load grid0..100 N fixed. Change only length from.1 m
to.2 m. Add independent pseudorandom uniform errors in±50 nm with seed421.
These are synthetic values; no instrument was operated.

**Procedure/instrumentation.** Run experiment.py from the root command in the
lesson, save stdout in a new file, and retain Python/platform, parameters, seed
and code hashes. Inspect raw load/travel pairs. Fit slope/intercept, then compare
naive, frame-corrected and two-length inversions. Separately evaluate the bond
energy/force/tangent curve to expose its nonlinear branch.

**Actual observation.** [observed.json](evidence/observed.json) is the executed
protocol; its timestamp and code hashes identify this run.

| Length | Apparent E, frame ignored | Corrected with known frame | Incorrect forced-zero-intercept E |
| --- | --- | --- | --- |
|.1 m |166.770712 GPa |200.149844 GPa |159.106851 GPa |
|.2 m |181.877924 GPa |200.072290 GPa |177.230554 GPa |

The two-length inversion gave199.994796 GPa and frame compliance
9.96126606×10^-8 m/N. Its closeness to the inputs in this one seed does not
establish calibration or unbiased performance over all seeds. The raw record
also retains the two exact one-length parameter pairs with identical total
compliance. The assumed bond law's force peak occurs at r/r0=1.23969849; its
ideal-chain modulus is100 GPa, not a measured material constant.

**Interpretation.** The structural observation equation, rather than random
scatter, explains the large apparent-modulus error. The intervention changed a
coefficient of specimen compliance while preserving the assumed frame term.
Residual fit uncertainty alone would miss this systematic error.

**Alternative explanations/limits.** Real grips can change compliance with load
or specimen length. Force error, drift, diameter variation, temperature, bending
and slippage can break the observation model. The toy energy ignores lateral
geometry, many-body interactions, thermal motion and defects. No fracture,
fatigue, creep or hardware safety conclusion follows.

**Follow-ups.** Sweep the seed and noise amplitude and retain the whole error
distribution; reduce the length difference to expose conditioning; give the
second specimen a1% area error; introduce a quadratic frame term; compare direct
specimen extensometry with actuator travel in a properly specified future
physical protocol. Label all simulated outputs as simulations. A real protocol
needs calibrated load/length/area instruments and apparatus limits before use.
