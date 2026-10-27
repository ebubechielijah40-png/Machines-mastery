# Author review and separate-reader corrections

The decision lesson,code,practice and source scopes were prepared on2026-10-25.
Author review checked exact threshold/power arithmetic,the finite composite-null
coupling,the first-hit recurrence and conservation,minimum-n search's retained
earlier failures,and the distinction between bounded operation counts and growing
rational bit cost. Current full-unit execution is27 tests PASS; the
[integrated raw record](evidence/decision-observed-integrated-2026-10-25.json)
matches all five executable source hashes. This is author review; the integrating
reader makes any domain gate decision separately.

Two concrete issues were identified by the integrating root reader and repaired:

1. A manually constructedUpperTest with critical=-1 could silently select the
   final tail by Python negative indexing. Numeric record validation now rejects
   invalid count/type/probability/size ranges; a regression preserves the case.
   Documentation also states that a manually supplied size is not calibration
   evidence. Only the factory derives a calibrated threshold and size from the
   exact null distribution; a manual but range-valid poor threshold is explicitly
   tested to have actual rejection31/32 rather than its asserted size0.
2. Existing `coverage` converted an exact rational target tofloat before checking
   interval membership. With n=1,Wald only produces[0,0]or[1,1],so every interior
   rational parameter must have coverage0. A target1/2^1100 rounded to0 and gave
   an incorrect answer near1; its complement likewise rounded to1. The target
   now remains Fraction and is compared against the actual binary-floating
   endpoints. New symmetric extreme-target regressions assert exact coverage0.
   This does not make the approximate theoretical interval formulas exact.

The first raw decision observation and the intermediate reviewed record retain
their earlier hashes and test scope. The integrated record fingerprints the
repairs; original2026-10-23 observations remain historical and untouched.

Remaining limits are explicit: iid/constant-parameter sampling is assumed;
nonrejection does not validate a null; power depends on the declared alternative;
bounded planning is not a proof of global impossibility; post hoc direction,
horizon or analysis selection needs its own error accounting; exact conditional
arithmetic does not establish causality or a calibrated physical process.
General sequential likelihood methods,confidence sequences,continuous inference,
causal identification and real study validation remain broader work.
