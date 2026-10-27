# Scientific reasoning through a measurement pipeline

A reproducible computation answers whether stated inputs and rules produce a result. Scientific validity also asks whether those inputs, rules and assumptions represent the phenomenon. This guide develops that distinction through the [measurement pipeline](../projects-guided/p08-scientific-pipeline/README.md), which supplies a full worked model, runnable implementation, independent tests, a synthetic experiment and exercises.

## Observation, competing model, discriminating experiment

Suppose repeated temperature readings scatter around one value. Model A has independent reading errors. Model B adds an uncertain offset shared across all readings. Both can produce similar short batches. A mean alone does not distinguish them. Derive their prediction before simulating: averaging n independent errors reduces their variance by n; a shared offset remains unchanged. The implemented experiment holds per-reading standard deviation at 2 milli-Celsius, calibration standard deviation at 5, and 10000 synthetic trials; it varies n and compares shared versus independent calibration draws.

The predictions are `25+4/n` and `29/n` in milli-Celsius squared. [Actual calculations](../projects-guided/p08-scientific-pipeline/evidence/observed.json) show the shared model near 25 at n=100 while the independent model is near .29. This establishes behavior of the executed synthetic models. It does not establish that a physical instrument's errors are independent, Gaussian or stationary. A real discriminating experiment would interleave reference standards, record elapsed time and environmental conditions, and compare independent instruments or randomized conditions.

## A model includes units and uncertainty

Three synthetic readings 25000,25002,24998 milli-Celsius have mean25000 and sample variance4 milli-Celsius squared. Adding a -10 milli-Celsius correction changes the mean to24990, not the scatter. Under the stated model the mean's repeatability variance is4/3, and a common calibration standard uncertainty5 contributes25 once. Combined standard uncertainty is `sqrt(79/3)/1000` Celsius. The [measurement source record](../projects-guided/p08-scientific-pipeline/SOURCES.md) traces standard uncertainty/covariance concepts to inspected NIST scopes. The numerical example and scalar derivation are original.

A confidence claim needs distributional and estimation conditions; `±u` is not automatically95% coverage. A calibrated estimate is also different from an authenticated statement: a valid MAC can preserve a false measurement claim perfectly. The [provenance counterexample](../security-cryptography-mastery/provenance/LESSON.md) makes that failure observable.

## Keep an evidence ledger

For each investigation write the question, competing hypotheses, controlled/varied variables, procedure, instrumentation, predicted behavior, actual output location, interpretation, alternatives, limitations and follow-up. Use the executable experiment's own environment metadata. If a trial was not executed, label it proposed and do not invent observations. If source access failed, record that failure without claiming verification.

Separate three kinds of check. A literal-vector test can refute an implementation error. A mathematical derivation proves a property under assumptions. A controlled empirical study tests how a phenomenon matches those assumptions under observed conditions. Passing one kind does not silently substitute for the other two. The [privacy unit](../13-privacy/count-release/LESSON.md) illustrates this sharply: utility moments and density grids cannot certify every output event of a finite sampler.

## Assessment and progression

First complete the measurement project's hand derivation and independent variance oracle. Next predict the correlation experiment before running it. Then attempt its transfer problem about drift without timestamps. Finally reproduce the authenticated-false-claim case and explain which uncertainty remains. The project's separate hints and solutions support independent checking.

Reconstruction challenge: without notes, write the two competing models, derive both variance curves, identify their units, list one real confounder, and design a new observation that can distinguish it. This guide and bounded project are STRONG for the stated mechanism. The scientific-reasoning domain remains PARTIAL: causal identification, randomized trials, formal hypothesis testing, multiple comparisons, power analysis and research ethics need further substantive units.
