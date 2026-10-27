# Train a small learning machine, from scalar derivatives to next-token generation

This original sequence closes a specific gap: the repository previously asked the
learner to train an MLP and a Transformer without supplying a complete trainable
build. Here the reference is a **real trained toy**, with a declared corpus,
loss, optimizer, split, checkpoint and actual observations. It is not a pretrained
LLM, a natural-language benchmark or a reproduction of the 2017 paper.

## Entry bridge and progression

Study [algebra/functions](../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md),
[vectors and maps](../../foundations/mathematics/core/03_VECTORS_MAPS.md),
[calculus/optimization](../../foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md)
and [numerical derivative/error checks](../../foundations/mathematics/change-error-and-evidence/README.md).
Before proceeding, multiply a 2×2 matrix by a vector, expand a polynomial
finite difference and explain why probabilities sum to one. Missing ability is
an actual prerequisite gap, not something the word “embedding” repairs.
No physics, chemistry, electronics or operating-system theorem is needed for
these synthetic arithmetic experiments. Python functions, lists and loops are
required; all model dimensions are explicit.

The working path is scalar computational graph → reverse derivatives → SGD →
nonlinear MLP → token IDs/embeddings → causal attention → multi-head block →
next-token objective → generation → independent evaluation. Attempt one stage
before looking at its reference. Later statistical learning, CNN/RNN systems,
large-scale distributed training and alignment are not completed by this toy.

## 1. The graph remembers operations, not just answers

For `x=3`, let `u=x*x+1` and `L=u*u`. Forward values are `u=10`, `L=100`.
A small change in x changes both occurrences in x*x, so `du/dx=2x=6`.
The outer square has `dL/du=2u=20`; multiply local effects to get120.
Reverse mode begins with `dL/dL=1`, visits operations after their consumers,
and **adds** contributions where several paths share an input.

Read [autodiff.py](../code/autodiff.py). A Value contains numeric data, an
adjoint `grad`, references to input nodes and a small local backward closure.
The closure uses the numeric operands captured at forward time. A topological
postorder supplies the correct reverse order. An iterative traversal avoids
recursion limits. Neither keeping only the final numeric answer nor running
local derivatives in arbitrary order preserves this dependency information.

The implemented primitive derivatives are addition1/1, multiplication y/x,
constant-power `p*x^(p-1)`, tanh `1-tanh(x)^2`, exponential `exp(x)` and positive
logarithm `1/x`. Subtraction/division compose those primitives. For a constant
power0, this implementation defines x^0=1 and derivative0, including x=0;
that programming convention does not settle every mathematical use of0^0.
Fractional powers outside the real differentiable domain are rejected or can
raise a range/domain exception. This is finite scalar arithmetic, not symbolic
algebra, interval differentiation or a tensor library.

**Repeated backward matters.** The old engine left intermediate adjoints from
its previous traversal. Our default `backward()` resets every reachable node
before differentiating. Repeating the same pass returns120 again, rather than
silently compounding old internal values. `accumulate=True` deliberately adds
this pass to previous **leaf** adjoints only; internal adjoints always reset.
This supports summing losses from separate microbatches if they use the same
leaf parameters. A parameter update changes numbers; rebuild the forward graph
before calculating a new loss. Reusing an old forward value after an update is
not a new model evaluation.

## 2. Why a hidden nonlinear layer is useful: XOR

Encode each input as-1/+1 and label the equal-sign rows-1, unequal-sign rows+1.
A single affine threshold cannot fit all four rows. Negative predictions at
(-1,-1) and(1,1) require `b-w1-w2<0` and `b+w1+w2<0`, hence b<0 after adding.
Positive predictions at(-1,1) and(1,-1) require the opposite b>0. Contradiction.

The supplied MLP computes

\[
h_j=\tanh(w_{1j}x_1+w_{2j}x_2+b_j),\quad
\hat y=\tanh\!\left(\sum_j v_jh_j+c\right),\quad
L=\frac14\sum_r(\hat y_r-y_r)^2.
\]

Its four hidden units can create nonlinear features. Without tanh between the
layers, multiplying affine maps just produces another affine map and preserves
the impossibility. The derivative of one squared error is `2*(prediction-target)`;
reverse mode routes that through output tanh, output weights, hidden tanh and
input weights. We average row losses so changing batch size does not multiply
our nominal objective scale automatically.

SGD proposes `parameter -= learning_rate * gradient`. A gradient points toward
local increase, so a sufficiently small negative step can reduce a smooth loss;
it is not a guarantee for every step size or nonconvex landscape. Random
initial weights break hidden-unit symmetry. All-zero hidden/output weights can
make several units behave identically or block a useful gradient path.

The experiment fits **all four XOR rows**. Calling the fit “held-out
classification accuracy” would be false. This is an optimization demonstration,
not evidence of generalization to an unobserved truth table or real task.

## 3. From text to integer IDs to vectors

The character tokenizer fits an ordered vocabulary from **training text only**.
For training characters c,a,b it assigns a→0,b→1,c→2 after sorting. Encoding
`cab` yields[2,0,1], and decoding returns the original text. A new character x
raises an unknown-character error. Fitting a new vocabulary on evaluation text
can alter every ID and break existing model parameters; changing only the
printed symbol list does not preserve the model interface.

An embedding matrix E has shape V×d. Token ID i selects row E_i. Equivalently,
a one-hot row with a single1 at i times E selects the same row. Lookup avoids
materializing the mostly-zero vector. The selected row consists of shared
learnable Values: repeated occurrences accumulate gradients into the same row.
An embedding coordinate is an optimization parameter, not a preassigned word
meaning. Unseen vocabulary rows do not become semantically trained by allocation.

Position also needs representation. Without positions, ordinary content-only
attention treats a permitted collection symmetrically; different orders can
become indistinguishable. This toy adds a learned position row P_t to each
selected token row: x_t=E_token+P_t. Its context is limited to four input tokens.
The learned positions are a deliberate variation; they are not the original
paper's sine/cosine rule [T17,§3.5]. During windowed generation, positions restart
within the cropped context; the model promises no unbounded memory.

The separate [byte-pair tokenizer](bpe.py) implements a second interface for
comparison: begin with UTF-8 bytes, repeatedly replace the most frequent
adjacent pair using a deterministic tie rule, then replay those merges at
encoding time. Bytes cover unseen Unicode text, but resulting tokenization can
be inefficient. Fewer token IDs do not alone establish a better learner.

## 4. Derive the block before treating it as a name

Read [the full attention/VJP worked unit](../labs/DERIVATION.md) before this
stage. Our one-block decoder first normalizes each token vector, then makes
query, key and value projections. With model width d=8 and two heads, each head
uses four coordinates. For current position t and permitted position j≤t:

\[
s_{tj}=q_t\cdot k_j/\sqrt4,\quad
 a_{tj}=\frac{e^{s_{tj}}}{\sum_{r=0}^{t}e^{s_{tr}}},\quad
 o_t=\sum_{j=0}^{t}a_{tj}v_j.
\]

We **do not construct future entries** in that denominator. Zeroing probabilities
after a full-sequence softmax would let future scores change the normalization.
For the first position there is one key, so its weight is1; q/K changes cannot
change that routing. The previous lab checks that exact edge independently.

Each head returns four values. Concatenating the two heads returns eight, which
an8×8 output matrix mixes before a residual addition. The same projection
matrices are used at every position; positions are not separate networks. The
next sublayer normalizes again, applies an8→12 affine map, tanh, then12→8 and
another residual addition. A final normalization and8→V map supply logits.
All parameters, including the learned embeddings and positions, receive gradients
from the same scalar next-token loss.

Normalization here means μ=Σx/d, σ²=Σ(x-μ)²/d and z=(x-μ)/sqrt(σ²+ε), ε=10^-5.
The mean is removed and variance becomes σ²/(σ²+ε), **not exactly one**.
A constant vector has zero centered output without division by zero. This toy
omits learnable normalization scale/offset. Its pre-normalized block, tanh
activation and single decoder stack differ from the inspected2017 architecture's
post-normalization/ReLU/encoder-decoder arrangement. We reproduce useful
mechanisms, not its model settings or empirical results.

Parameter count is inspectable by flattening the matrices and bias lists. The
experimental configuration has548 scalars. It deliberately has no dropout,
padding mask, tied embedding/output matrix, KV cache, optimizer moments,
quantization, GPU kernels or distributed training. The earlier cache lab remains
an independently tested mechanism; a whole-block cache would also need layer-
specific state and positional conventions, not only a pasted list of token IDs.

## 5. Next-token loss is a complete training contract

For sequence `[a,b,c,a,b]`, inputs are `[a,b,c,a]` and labels `[b,c,a,b]`.
At position0 only a may influence the prediction of b. The t-th target is
one position **after** the last visible input. A correct mask with unshifted
labels can train copying, producing misleadingly low loss while solving the
wrong task. Test both the information boundary and the label construction.

For logits z and target y, define

\[
p_i=\frac{e^{z_i}}{\sum_j e^{z_j}},\quad
 \ell=-\log p_y=\log\sum_j e^{z_j}-z_y.
\]

Subtract m=max(z) first. Then `log(sum(exp(z-m)))-(z_y-m)` gives the same real
quantity with bounded exponential arguments. The derivative is
`d loss/d z_i = p_i - 1[i=y]`. It follows by differentiating log-sum-exp and
subtracting the selected coordinate. For logits[ln2,ln3], target1,
p=[0.4,0.6], loss≈0.5108256 and gradients[0.4,-0.4]. This independent hand
oracle tests both output probabilities and reverse paths.

Average negative log-likelihood (NLL) is in nats per predicted token. Perplexity
is exp(NLL) under the **same tokenizer and evaluation protocol**. Different
vocabulary segmentation changes that denominator; raw token perplexities are
not automatically comparable across tokenizers. A model trained to predict
these strings is rewarded for their patterns, not for factual truth.

Global norm clipping computes sqrt(Σg²). If it exceeds c, multiply all gradients
by c/norm, preserving direction while shortening the step. It does not repair
wrong gradients or an excessive learning rate. Proposed SGD updates are checked
before mutating parameters, so a rejected nonfinite update does not partially
change the model. Extremely large squared-gradient norms can still overflow;
no arbitrary-range arithmetic guarantee is supplied.

## 6. Generation, persistence and evaluation

At each generation step, evaluate the last permitted context, take its final
logits, divide by a positive temperature, retain optional top-k candidates,
normalize and draw one token. Append it to the input before the next step.
A seed controls a pseudorandom stream, not semantic correctness. With temperature
0.5, logits[ln2,ln3] give weights proportional to4 and9; top-k1 always selects
index1 independently of the seed. Top-k may remove an important low-probability
alternative, and higher temperature is not calibrated uncertainty estimation.

`save/load` round-trips numeric parameters/configuration with a version tag.
The loader enforces an exact schema, rejects Boolean/nonfinite parameters and
reads at most1MB plus one byte before rejecting oversized local artifacts.
Token decoding and SGD materialize iterable inputs once, so generators follow
the same semantics as lists; duplicate optimizer parameter identities are rejected.
The tokenizer's symbol-to-ID mapping must be retained alongside it; numeric
weights alone do not identify text semantics. The format is a locally controlled
teaching JSON file, not an authenticated model supply chain, arbitrary-file
loader sandbox, resumable optimizer checkpoint or concurrent service.

A clean evaluation uses data not optimized against, freezes preprocessing,
records overlap and reports distribution shifts separately. Our tiny corpus is
explicitly synthetic: training `abcab`,`bcabc`, held-out phase `cabca`, and
reversed-pattern shift `acbac`. The held phase is only one string, not a robust
statistical estimate. The experiment deliberately optimizes on the held string
after reporting the clean result, labels its later score contaminated, and
shows how an apparently better “test” number can destroy the protocol.

## 7. Build, test, investigate and reconstruct

Python3.10+ standard library; from repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/code -p test_autodiff.py -v
python3 -m unittest discover -s 16-machine-learning/training -v
python3 16-machine-learning/training/experiment_training.py
```

The [experiment protocol/results](EXPERIMENTS.md) separates predictions from
actual raw measurements. [EXERCISES](EXERCISES.md), [HINTS](HINTS.md) and
[SOLUTIONS](SOLUTIONS.md) are separate. Start the MLP milestones in
[the neural project](../../projects-guided/p12-neural-net/README.md), then
[the decoder project](../../projects-guided/ai-autodiff-transformer/README.md).

A serious submission contains hand calculations, original forward/backward code,
independent finite differences, a causal future-mutation test, actual training
logs, frozen token mapping/split and a failure interpretation. Rebuild the full
small pipeline from blank files before consulting reference tests. Passing its
reference is implementation evidence; unaided explanation and transfer remain
learner work. Source inspection boundaries are in [SOURCES](SOURCES.md).
