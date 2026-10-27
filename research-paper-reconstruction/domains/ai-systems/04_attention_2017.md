# Attention Is All You Need — investigate the mechanism and its evidence

**Classification: PARTIAL research reconstruction; STRONG executable mechanism
companion.** Primary full text inspected; translation training and benchmarks
have **not** been reproduced. Original instruction below accompanies, rather
than replaces, the paper. Source A17 and exact inspection scope are recorded in
[the verification record](../../../16-machine-learning/labs/SOURCES.md).

## 1. Historical context

[SOURCE A17 §1–2] The paper addresses sequence transduction previously built
with recurrent or convolutional networks, often with attention. [EXPLANATION]
Separate *what computes a representation* from *what connects positions*: an
attention connection inside a recurrent system does not remove its recurrence.
Draw both dependency graphs before judging the proposed change.

## 2. The unresolved problem

[SOURCE A17 §1] Sequential recurrent dependencies restrict within-example
training parallelism. [DERIVED] For `h_t=f(h_(t-1),x_t)`, computing `h_5`
requires `h_4` even if all `x` are available. Five cores cannot independently
compute the five states by pretending those dependencies are absent.

## 3. Why the problem mattered

[EXPLANATION] A dependency bottleneck can leave parallel arithmetic resources
idle. This matters when sequence length, memory and wall-clock budgets limit
experiments. Parallelism, arithmetic count and statistical quality are different
quantities: reducing one cannot stand in as evidence about the others.

## 4. Previous approaches

[SOURCE A17 §2] Recurrence, convolution and attention-augmented transducers are
the comparison context. [EXERCISE] Construct a chain graph for a recurrent
encoder and a width-3 convolution graph. On eight positions, count the shortest
path from the first to the last position. State whether padding, dilation or
layer stacking changes your count. This is a graph exercise, not a benchmark.

## 5. Their limitations

[DERIVED] In a length-n chain, the first-to-last path contains n−1 edges.
In one local convolution, distant positions may have no connecting path at
all. A dense all-pairs interaction directly connects positions but requires
more pairs as n grows. Therefore a shorter dependency path can trade away
resource efficiency. This tradeoff must be measured under a workload.

## 6. The research question

[EXPLANATION] Treat the question as: can an attention-based transduction
architecture achieve competitive translation while changing training execution
constraints? This framing demands both quality and resource evidence. It does
not ask whether attention alone is a sufficient theory of intelligence.

## 7. Central insight

[SOURCE A17 §3] The Transformer combines attention with feedforward layers,
residual connections, normalization and positional encodings. [EXPLANATION]
The proposed system is a composition. Implementing one attention head isolates
one mechanism; it does not establish the full composition's behavior.

## 8. Mathematical mechanism

[DERIVED] Let q have d coordinates; there are m compatible keys and v-wide
values. Compute scores `s_j=q·k_j/sqrt(d)`, normalized weights a, then
`o=sum_j a_j v_j`. See [the complete worked derivation](../../../16-machine-learning/labs/DERIVATION.md)
for every intermediate, a numerical counterexample, the variance assumptions,
and derivatives `dL/dq`, `dL/dK`, `dL/dV`. That material is original local algebra,
not a copied paper explanation.

A useful invariant is convexity: each output coordinate is between the minimum
and maximum permitted payload coordinates, because weights are nonnegative and
sum to one. This does not bound a subsequent output projection or residual
addition. Test the invariant at precisely the layer where it applies.

## 9. Architecture or algorithm

[SOURCE A17 §3.1] The original architecture has an encoder and autoregressive
decoder. [EXPLANATION] A decoder-only toy omits cross-attention and cannot be
silently called the original architecture. Draw three interfaces separately:
encoder self-attention, decoder masked self-attention, and decoder queries over
encoder keys/values. For each draw the input origin, shape and information
boundary. The supplied toy only implements isolated causal self-attention.

## 10. Experimental design

[SOURCE A17 §5–6] WMT14 translation tests and architecture variants form the
reported empirical setting. [EXPLANATION] To reproduce one result, first freeze
the exact dataset release, train/development/test split, normalization,
tokenization, model settings, randomization, optimizer, stopping rule,
checkpoint selection and decoder settings. A matching architecture name is
insufficient. Preserve training logs and checkpoint provenance before choosing
the best run; otherwise the evaluation procedure can quietly change.

For a low-cost local investigation, instead freeze all toy inputs and change
one factor: scaling, future masking, cache state or perturbation size. The
[executed protocol](../../../16-machine-learning/labs/EXPERIMENT.md) separates
predictions, observations, interpretation and untested alternatives.

## 11. Baselines and metrics

[SOURCE A17 Table 2] BLEU compares translation outputs; earlier model families
are listed as baselines. [EXPLANATION] A fair local mechanism baseline is a
simple independent implementation or analytic answer, not a huge pretrained
model. Cache tests compare newest-prefix outputs with full-prefix computation;
derivative tests compare analytic derivatives with central differences. Record
absolute tolerances and shapes. A speed claim additionally needs the same
machine, workload, precision, trial procedure and outputs.

## 12. Actual reported results

[SOURCE A17 Table 2; **reported, not reproduced**]

| Model | EN–DE BLEU | EN–FR BLEU |
| --- | ---: | ---: |
| ConvS2S | 25.16 | 40.46 |
| Transformer base | 27.3 | 38.1 |
| Transformer big | 28.4 | 41.8 |

The source's §6.1 prose instead gives **41.0** for big EN–FR. Preserve this
internal discrepancy; do not silently harmonize it. All values above are
identified as **Table 2** values, not independently verified measurements.

## 13. What the evidence supports

[INFERENCE] Table 2 supports a comparison among its specified reported
systems/tasks/metrics. Differences between rows are not clean single-variable
causal effects: data preparation, compute and selection can differ. The base
EN–FR row is lower than ConvS2S; “every Transformer beats every baseline” is
already contradicted by those entries. For architecture attribution, study
controlled variants and residual confounds rather than only the best row.

## 14. What the evidence does not establish

[EXPLANATION] Translation quality does not establish factual truth,
robustness to arbitrary distributions, privacy, safe tool use or optimality on
all hardware. A toy's passing tests establish none of the paper's benchmark
numbers. The causal mask is a local information constraint; future information
in preprocessing can still leak through otherwise valid input vectors.

## 15. Limitations and alternative explanations

[INFERENCE] Selection of tasks, hyperparameters and checkpoints constrains
interpretation. A quality increase could reflect a beneficial interaction among
components rather than one component alone. Measure error bars across seeds,
check test-set reuse and compare resource budgets before generalizing. These
are analysis obligations here; they are not invented author-reported findings.

Our implementation has its own limits: single head, fixed projections, no
training, no feedforward block, no positions, no dropout, no batches or padding.
It validates finite inputs but has no context capacity or resource sandbox.

## 16. Subsequent developments

Verified primary identities of [BERT](05_bert_2018.md),
[GPT-3](06_gpt3_2020.md) and [FlashAttention](12_flashattention_2022.md)
provide concrete follow-up reading. Their detailed empirical claims are
**UNVERIFIED — verification required** in this execution window. Do not infer
that the original paper established every later architecture or kernel idea.
Local incremental K/V reuse is an engineering exercise, not a claim about the
2017 paper's original contributions.

## 17. Reproduction requirements

**Full result: NOT REPRODUCED.** It needs exact source/data/configuration,
compatible compute, a faithfully implemented training/evaluation pipeline,
licensed data access, reproducible checkpoints and uncertainty analysis.
No full-model training command is supplied because that pipeline does not yet
exist here. That is an explicit backlog item, not a hidden dependency.

**Bounded mechanism: executed.** Python 3.10+, standard library, synthetic
vectors; run the commands below from the repository root. No network required.

```sh
python3 -m unittest discover -s 16-machine-learning/labs -v
python3 16-machine-learning/labs/experiment_attention.py
```

[Raw JSON](../../../16-machine-learning/labs/evidence/2026-10-22-attention.json)
and [test output](../../../16-machine-learning/labs/evidence/2026-10-22-tests.txt)
record the actual environment and observations. These are mechanism evidence.

## 18. Implementation exercises

Attempt [14 progressively harder problems](../../../16-machine-learning/labs/EXERCISES.md):
scalar arithmetic and shape tracking; VJP reconstruction; independent cache
checks; variance counterexample; projection-matrix gradients; experimental
replication; preprocessing leakage; unaided reconstruction. Hints and solutions
are separated. Build [the guided attention stage](../../../projects-guided/ai-autodiff-transformer/README.md)
before attempting the still-incomplete full Transformer stages.

## 19. Connections to other research

The derivative exercise connects to the [backprop entry](01_backprop_1986.md)
through the chain rule. The state-reuse experiment connects to the
[FlashAttention entry](12_flashattention_2022.md) through the broader question
of data movement, but they are different mechanisms: retaining projected state
across generation steps is not a tiled GPU attention kernel. A local cache
comparison cannot verify FlashAttention's reported performance.

## 20. Open questions and next evidence

- What fails first when learned projections become ill-conditioned: input
  validation, score saturation, gradient precision or the optimizer? Add
  a trained toy plus instrumentation before answering empirically.
- When does K/V reuse outperform newest-query-only recomputation in this
  implementation? Measure repeated trials and memory, not just operation counts.
- How do upstream normalization statistics break causal prediction? Inject
  future-only changes into a synthetic pipeline and test the entire boundary.
- Can a small controlled transduction dataset separate position information
  from content routing? Write train/test splits and falsifiable predictions
  before training.

No answers or numerical model results are claimed for these unrun studies.
