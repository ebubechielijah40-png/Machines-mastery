# 11 — Language modeling

An autoregressive language model estimates a distribution over the next token:

`P(x_1,...,x_T)=Π_t P(x_t | x_<t)`.

Training commonly uses teacher forcing: for every position, the model sees the true prefix and is penalized by cross-entropy for the next token. This converts raw text into a large self-supervised prediction problem.

## Perplexity

Perplexity is `exp(average negative log-likelihood)` under a tokenization/model setup. It is useful for comparing models under consistent conditions, but not a universal intelligence score. Tokenization differences can make raw perplexities incomparable.

## Generation

The model outputs logits. A decoding rule transforms them into a token choice:
- greedy: choose maximum logit;
- temperature: rescale logits before softmax;
- top-k: restrict to k highest candidates;
- top-p: restrict to a probability-mass nucleus;
- sampling: draw stochastically.

Generation quality therefore depends on both the learned distribution and decoding policy.

## Hallucination mechanism

Next-token prediction optimizes likelihood under training/evaluation distributions, not truth verification. A fluent continuation can be statistically plausible without being factually grounded. Retrieval, tools, verification, and evaluation alter the system around the model; they do not magically convert likelihood into truth.

## Build and observe the whole contract

[The scalar-to-decoder sequence](training/README.md) derives stable cross-entropy
and p-minus-one-hot gradients, implements shifted causal targets, performs actual
synthetic training, generates tokens and preserves clean versus deliberately
contaminated evaluation. For input[a,b,c], targets[b,c,next] differ from copying
[a,b,c]. Test that offset as well as the causal mask. The experiment's three-symbol
model learns a cyclic pattern and fails its reversed-pattern distribution. Its
low training loss is not natural-language understanding or factual reliability.
