# From a fitting problem to binary probability

Suppose a monitor records measurements before a future fault and must estimate
whether the fault occurs. A rule such as “score greater than zero” produces a
label, but it does not state what changing the score means or how to fit it.
We first build a probability model, then choose actions separately. The
mathematics below also applies to the artificial examples in this directory;
no real fault dataset is used or validated here.

## State the object being fitted

Let x be a d-dimensional vector of features, y an observed integer0 or1,
w a parameter vector and b an intercept. Define z=wᵀx+b and

\[
 p_\theta(y=1\mid x)=\sigma(z)=\frac1{1+e^{-z}}.
\]

This chooses a conditional probability family. It does not prove that the real
world uses a linear log-odds relationship. The input feature definitions, their
units and the point in time when each is available are part of the model.
The identity p/(1−p)=eᶻ implies log(p/(1−p))=z. Adding1 to z multiplies the odds by
e, rather than adding a fixed amount to probability.

For conditionally independent labeled observations, the likelihood is
∏pᵢʸⁱ(1−pᵢ)¹⁻ʸⁱ. Taking negative logs turns the product into a sum. For one row,

\[
 \ell(z,y)=-y\log\sigma(z)-(1-y)\log(1-\sigma(z))
 =\log(1+e^z)-yz.
\]

The code evaluates the equivalent expression
max(z,0)−yz+log1p(exp(−|z|)). For z=1000 the raw exponential overflows on ordinary
binary64 arithmetic; this expression remains finite. Sigmoid likewise uses
exp(−z) for nonnegative z and exp(z)/(1+exp(z)) for negative z. Never obtain a
training loss by first rounding a probability to0 or1 and then taking log0.

## Derive the update completely

The derivative of log(1+eᶻ) is eᶻ/(1+eᶻ)=σ(z), so

\[
 \frac{\partial\ell}{\partial z}=p-y,\quad
 \frac{\partial\ell}{\partial w_j}=(p-y)x_j,\quad
 \frac{\partial\ell}{\partial b}=p-y.
\]

At w=(0,0), b=0, x=(3,−2), y=1, z=0 and p=.5. The loss is log2≈.693147;
the gradients are (−1.5,1) and −.5. A step with learning rate.1 gives
w=(.15,−.1), b=.05. The new score on this row is
.15×3+(−.1)×(−2)+.05=.7. Its probability increases to about.668188 and loss falls
to about.403186. This is a one-row fitting observation, not generalization.

For n rows, average the per-row gradients before updating. Duplicating every
row then leaves the mean update unchanged. Summing without dividing by n changes
the effective learning rate when batch size changes. `batch_step` returns a new
parameter tuple only after validating every proposed number. It cannot partially
mutate a parameter vector before rejecting a later invalid label.

Optional L2 regularization adds λ||w||²/2 to the mean objective and λw to its
weight gradient. The intercept remains unpenalized here. Declare the convention:
λ||w||², λ||w||²/2 and λ||w||²/(2n) have different coefficients. The probability
NLL in `metrics` excludes the regularization term; optimizer checkpoint `loss`
is the fitted objective and includes it. Penalization changes the selected
solution rather than supplying new observations.

## Capacity and geometry

The class1 region under threshold.5 is wᵀx+b≥0. In two dimensions it is one side
of a line. Consider XOR: label1 for (1,−1),(−1,1), label0 for (1,1),(−1,−1).
Assuming all four strict inequalities are satisfied, adding the two positive
constraints gives2b>0. Adding the negative constraints gives2b<0. They cannot both
hold. Increasing optimizer steps cannot remove this representation limit.
Introduce the explicit feature x₁x₂ or a hidden nonlinear network, then state
which assumption changed. The existing [XOR build](../training/README.md)
provides the neural comparison.

On strictly separable data, unregularized logistic likelihood can improve while
weight norms tend to infinity; a finite maximum need not exist. A fixed-step
training run has a stopping rule, not proof of convergence to a finite optimum.
A large step can also oscillate or saturate. Global gradient clipping computes
g←g·min(1,c/||g||₂). It bounds one update's norm by learning_rate×c; it does not
correct labels, produce missing features or restore a vanished gradient.

## Preprocessing is fitted state

`Standardizer.fit` stores training means and population scales
sⱼ=√(Σ(xᵢⱼ−μⱼ)²/n). Transform with (xⱼ−μⱼ)/sⱼ. A constant training column uses
scale1, so its training transform is zero. A new nonconstant value in that
column remains a new value; it is not silently discarded. The transform does
not update μ or s when evaluation rows arrive.

For training rows (1,4),(3,4), μ=(2,4), s=(1,1), so evaluation row (100,10)
becomes (98,6). Refitting on that row changes the model's data access and feature
coordinates. It is leakage even when labels were not used. Whether it inflates
or lowers a particular reported score is empirical; do not manufacture an
improvement simply because the procedure is invalid.

## Evaluation and incorrect shortcuts

Accuracy counts correct thresholded labels. NLL assesses assigned conditional
probability; Brier score averages (p−y)². An always-negative predictor has99%
accuracy on a sample with1% positives, while missing every positive. Thresholds
should reflect the use decision, error costs and constraints rather than being
inferred from accuracy alone. Calibration asks whether events assigned similar
probabilities occur at corresponding frequencies; neither a small training
Brier score nor a four-row reliability table certifies it.

A label-derived feature recorded after a target outcome cannot be supplied at
prediction time. Random splitting can reproduce that same leak in both halves.
The experiment deliberately writes a shortcut as4(2y−1), then flips its relation
in a paired held sample. Compare a stable-feature-only baseline. This is an
exactly specified artificial failure, not a causal estimate about hospitals,
Lagos or any real population.

Debug in this order: verify feature timestamps and split groups, inspect a
zero-parameter gradient, check every coordinate numerically, check mean-versus-
sum scaling, inspect probabilities and score margins, then tune the optimizer.
Retain subgroup/sample counts, data/schema hashes and the frozen transform in
an actual deployment. This bounded implementation supplies no deployment,
authentication, retraining, private-data or drift-response infrastructure.
