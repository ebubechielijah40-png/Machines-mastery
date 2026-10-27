# Statistics: a calculation is conditional on collection

Study [finite probability and inference](probability-inference/README.md) after
[algebra and discrete counting](../mathematics/core/README.md). It replaces the
previous repeated templates with explicit probability models, exact finite
computations, experiments, counterexamples and separate assessments.

A sensor's repeated reading can be modeled as Y_i=μ+b+ε_i, where μ is the target,
b is shared calibration bias and ε_i is varying noise. Under zero-mean independent
noise, averaging reduces the noise variance but leaves b. Duplicating one Y_i
many times reduces neither its actual random variation nor its calibration bias.
Thus a very small computed standard error can describe a faulty collection model.
The [numerical measurement unit](../mathematics/change-error-and-evidence/README.md)
derives centered variance, standard error and covariance propagation and records
synthetic bias experiments with their limitations.

The probability unit makes three kinds of reasoning explicit:

1. A finite **model** assigns masses to outcomes. Conditioning, Bayes and moments
   follow from those masses. The model is not established merely by arithmetic.
2. A sampling **procedure** maps observations to an estimate, interval or test.
   Its repeated-sample error behavior depends on the generating process. Exact
   binomial enumeration exposes both Wald and Wilson coverage variation.
3. An **interpretation** connects the result to a claim. A tail probability is
   conditional on a null; it is not a posterior probability that the null is true.
   Permuting groups requires an assignment/exchangeability justification; it does
   not turn a confounded comparison into a causal experiment.

The worked fault model keeps prior prevalence, detector sensitivity and false
positives separate. A positive result can have a low posterior fault probability
when nonfaults dominate the population. Changing deployment prevalence or detector
behavior changes that calculation. It must be re-evaluated under the new process.

Follow the [experiment protocol](probability-inference/EXPERIMENTS.md). It compares
interval coverage by exact enumeration and then breaks the iid assumption while
holding every observation's marginal probability fixed. Retained outputs are
actual synthetic executions; no factory, patient or physical measurement is claimed.
Use [16 exercises](probability-inference/EXERCISES.md), the separated hints and
solutions, and the reconstruction task to test understanding beyond formula recall.

Continue to model training/evaluation, privacy release experiments or scientific
measurement pipelines only after stating their sampling and selection assumptions.
Regression coefficients describe a fitted model; attributing a causal effect
needs design or additional identification assumptions. Low training loss and a
narrow interval are not by themselves evidence of a useful model.

Remaining scope includes full continuous distributions, likelihood/asymptotic theory,
power, sequential analysis, causal identification and general dependent processes.
The route above prepares a concrete finite starting point and marks those gaps.
