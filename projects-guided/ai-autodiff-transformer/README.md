# Guided project — autodiff to tiny Transformer

This project is a staircase, not one code dump.

**Current classification: STRONG bounded local build; PARTIAL production project.**
Scalar autodiff, XOR, tokenization, learned embeddings, a trainable causal
multi-head decoder, SGD, generation, checkpointing and actual synthetic
training/evaluation are supplied. The independently tested attention VJP/cache
remains a separate mechanism. Whole-decoder caching, a concurrent serving layer,
large data and broad language evaluation are not completed by this build.

1. Scalar autodiff with gradient checks.
2. MLP that solves XOR.
3. Matrix/tensor operations (or transition to NumPy/PyTorch only after tracing shapes by hand).
4. Character tokenizer and embedding table.
5. Single-head causal attention.
6. Multi-head attention + MLP + residual block.
7. Tiny decoder-only Transformer.
8. Train on a tiny corpus.
9. Implement sampling and compare greedy/temperature/top-k.
10. Add a minimal KV-cache experiment.
11. Serve locally and load-test.
12. Rebuild architecture from memory.

Every stage requires tests, an experiment log, and a “what I predicted / what happened / why” entry. Do not proceed when you cannot explain tensor shapes and gradient paths.

## Developed build: one causal head, derivatives and reusable state

Problem: a current token must mix earlier information without reading the future;
the mechanism must expose local gradients and avoid repeatedly projecting the
same previous keys/values during incremental generation. Learning objectives are
to derive routing, enforce the information boundary, validate a vector-Jacobian
product and distinguish retained state from full-prefix recomputation.

Prerequisites: dot products, exponentials, probabilities and the chain rule.
The [numerical bridge](../../foundations/mathematics/change-error-and-evidence/README.md)
teaches derivative/error checking; [the worked attention derivation](../../16-machine-learning/labs/DERIVATION.md)
develops the shapes and local derivatives. Python3.10+ standard library is sufficient.
All inputs are synthetic, dimensionless vectors. No trained weights or external
API credentials are required.

Architecture: token row→three fixed projections→permitted prefix K/V→scaled scores
→stable normalized weights→payload sum. `CausalCache` retains projected keys/values
for one sequence. Its arrays are caller-owned mutable state; output gradients
enter an isolated VJP, not a complete neural training graph.

| Milestone / learner task | Observable completion criterion | Reference after an attempt |
| --- | --- | --- |
| Derive a two-key forward pass and every shape | Hand weights sum to one and output equals the declared payload mixture | DERIVATION worked case |
| Implement stable normalization | Equal-score and large-common-offset cases agree with independent arithmetic; reject empty/nonfinite rows | softmax and Decimal test |
| Enforce causality before normalization | Mutating only a future token cannot change previous outputs; each permitted row remains normalized | causal_attention and leakage test |
| Derive/implement q/K/V VJP | Every input coordinate agrees with central differences within a justified tolerance; explain saturation limitations | attention_backward and gradient tests |
| Build incremental projected state | Each step equals the newest output of full-prefix computation; failed steps leave state unchanged | CausalCache and cache tests |
| Investigate scaling and state reuse | Retain predictions/raw output; separate derived operation counts from noisy elapsed times | executed EXPERIMENT |

Before opening the [reference implementation](../../16-machine-learning/labs/attention.py),
attempt the [exercises](../../16-machine-learning/labs/EXERCISES.md).
[Hints](../../16-machine-learning/labs/HINTS.md) and
[solutions](../../16-machine-learning/labs/SOLUTIONS.md) are separate.
From the repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/labs -v
python3 16-machine-learning/labs/experiment_attention.py
```

Debug tasks: deliberately normalize before masking, mix up key/value widths,
retain a failed cache step, and reuse one cache for two sequences. Predict each
failure, write a counterexample and repair it. Shared-state reuse can cross an
information/privacy boundary even if every local arithmetic operation is correct.

Performance: distinguish one complete causal call from recomputing every prefix
during generation. Cached score pairs across n generated tokens still grow
quadratically; K/V memory grows linearly in context. Pure Python scalar loops,
input validation and copies can dominate small timings. No production latency,
batching, concurrency or memory-isolation guarantee is supplied. Deployment is
not part of this isolated mechanism; context quotas, session isolation, errors,
observability and safe request handling are separate production work.

Deliver: original implementation, hand trace, independent tests, failure/repair
log, experiment JSON and limitations. Rubric: forward arithmetic20%, causality20%,
derivative derivation/check20%, cache state invariants20%, evidence/limits20%.
Correctly rejecting an unsupported case counts; hiding it as zero does not.
Passing the reference tests alone does not establish unaided reconstruction.

Reconstruction challenge: close the source and rebuild the head/VJP/cache from
a blank file with unequal key and payload widths. Explain a single-visible-key
case where q/K gradients vanish, and a preprocessing path that could leak the
future despite a correct causal mask.

Sources and execution evidence: [inspected source map](../../16-machine-learning/labs/SOURCES.md),
[raw mechanism experiment](../../16-machine-learning/labs/evidence/2026-10-22-attention.json),
[research dossier](../../research-paper-reconstruction/domains/ai-systems/04_attention_2017.md).
This is not a reproduction of translation BLEU or a complete GPT/Transformer.


## Developed continuation: train the whole small decoder

Complete [the scalar-to-training lesson](../../16-machine-learning/training/README.md)
after the causal-head milestones above. It derives stable cross-entropy and
its `p-one_hot(target)` gradient, one-hot/embedding equivalence, learned position
rows, multi-head shapes, residual paths and the shifted next-token objective.
The executable [TinyDecoder](../../16-machine-learning/training/tiny_models.py)
uses one pre-normalized tanh block with bounded dimensions; these are declared
variations from the inspected 2017 paper rather than a reproduction of it.

| Milestone / original learner task | Observable evidence |
| --- | --- |
| Fit a training-only character map; derive lookup gradients | Round trip known symbols, reject unknown characters and preserve the map with weights |
| Learn byte-pair merges in a separate small tokenizer | Replaying frozen merge order round-trips unseen UTF-8 text; explain the word-boundary difference |
| Compose two causal heads and residual/feed-forward paths | Every shape agrees; changing future tokens leaves previous logits unchanged |
| Shift targets by one and derive stable NLL | Hand logits[ln2,ln3] give loss-ln(.6), gradients[.4,-.4]; no copying objective |
| Train548 scalars on the declared three-symbol pattern | Save an actual loss/gradient trace with seeds, corpus/hash and optimizer settings |
| Evaluate before any held-data optimization | Report clean held loss separately from reversed-pattern shift and deliberately contaminated scores |
| Generate and round-trip a local checkpoint | Seeded sampling and top-k1 behavior are reproducible with the same vocabulary/configuration |
| Rebuild and extend | Unaided smaller decoder; new corpus and explicit unsupported-case analysis |

From repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/code -p test_autodiff.py -v
python3 -m unittest discover -s 16-machine-learning/training -v
python3 16-machine-learning/training/experiment_training.py
```

Preserve your attempt before consulting [exercises](../../16-machine-learning/training/EXERCISES.md),
[hints](../../16-machine-learning/training/HINTS.md) and
[solutions](../../16-machine-learning/training/SOLUTIONS.md). The tests combine
hand arithmetic, finite differences at sampled weights, future mutation,
atomic optimizer rejection, token contracts and numeric checkpoint round trips.
They do not exhaustively verify every parameter or numeric input.

Actual [experiment data](../../16-machine-learning/training/evidence/training-2026-10-22.json)
shows training NLL1.1959→.0121, clean held phase NLL1.1019→.1149 and
reversed-pattern NLL1.0555→4.5927. The small pattern is learned while the reversed
pattern gets worse. Deliberately optimizing the held string later lowers its
score but invalidates its held-out interpretation. Read [the full protocol](../../16-machine-learning/training/EXPERIMENTS.md)
for controls and limitations. These are local synthetic observations, not broad
language competence, benchmarks or independently reproduced paper results.

Keep whole-block KV caching as an explicit later extension: learned position
conventions and per-layer state must match full-prefix computation. The old
single-head cache cannot simply be assumed correct for this whole decoder.
Serving/load-testing is also separate; the model has no request isolation or
remote interface. Extend to [retrieval/tool control](../../16-machine-learning/retrieval-agents/README.md)
only after distinguishing learned parameters, external evidence and mutable
session state. Additional source scopes are [recorded here](../../16-machine-learning/training/SOURCES.md).
