# 20 — Project ladder and mastery gates

Do these in order. Each project has a build, experiment, failure, and reconstruction phase.

## P1 — Linear learner
Implement linear/logistic regression, gradient descent, tests, and a data-leakage experiment.

## P2 — Autodiff engine
Implement scalar reverse-mode autodiff. Validate every primitive against finite differences. Add branched-graph accumulation tests.

## P3 — MLP from scratch
Train XOR and a small classification dataset. Log gradients/activations. Break initialization and learning rate intentionally.

## P4 — Tiny tokenizer
Implement character and BPE-like tokenization. Compare compression and sequence lengths across prose/code/multilingual samples.

## P5 — Tiny Transformer
Implement causal self-attention and a decoder-only Transformer. Train a character-level language model. Inspect tensors and attention, not just generated text.

## P6 — Inference server
Add KV-cache-aware generation or a simplified cache model, batching, metrics, timeouts, and load testing.

## P7 — Local RAG
Index repository documents, build a gold retrieval set, evaluate retrieval separately, then add generation. Test poisoned and stale documents.

## P8 — Tool-using agent
Build a constrained local agent with explicit tool schemas, state, verifier, stop conditions, and failure injection.

## P9 — Reconstruct from memory
Without source, recreate the architecture of the tiny Transformer and agent runtime. Compare against your implementation and document false assumptions.

## Mastery gate
You are not done when code runs. You must be able to explain tensor shapes, derive gradients for a small network, predict attention masks, estimate memory/complexity, diagnose training failure, distinguish retrieval from generation failure, and state what the system cannot guarantee.
