# Hints after an original attempt

A1: each operation owns a local rule. For product xy, the contribution to x is
upstream*y and to y is upstream*x. If the two objects are identical, both additions
still occur. The list of graph parents and the backward operands need not have
identical multiplicity conventions.

A2: reverse a postorder in which each node follows its inputs. A visited identity
set prevents revisiting a shared node. Reset adjoints before the pass; saving and
adding old leaf adjoints is different from keeping every old intermediate.

A3: add the two equal-sign inequalities, then the two unequal-sign inequalities.
Composing two affine layers does not create nonlinear decision boundaries.

A4: at a tanh unit the derivative is1-output^2. Work backward through output,
output weights, hidden units and input weights. Each training row reaches shared
parameter objects, so row contributions add before the averaging scale is applied.

A5: vary finite-difference h over several powers of ten rather than interpreting
one mismatch automatically as a derivative bug. Capture the pre-update forward
operands; rebuild the graph after changing parameters.

A6/A7: write what information the model may see before choosing an evaluation
score. A low loss can be produced by correct pattern learning, target leakage or
repeated fitting to the evaluation set; distinguish them with a controlled test.
[Full mathematical solutions](../../16-machine-learning/training/SOLUTIONS.md)
are separate from this hint sheet.
