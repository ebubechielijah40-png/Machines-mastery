# 09 — Transformers

A Transformer block combines token-wise feed-forward computation with attention-mediated communication between positions.

A common decoder-only block is conceptually:

```text
x
├─ norm → causal self-attention → + residual
└─ norm → MLP                  → + residual
```

The residual stream is the evolving representation carried through the network. Attention moves information between positions; the MLP transforms information independently at each position after communication.

## Positional information

Pure self-attention without positional information is permutation-equivariant: reordering tokens reorders outputs. Language needs order, so positional information is injected through learned embeddings, sinusoidal schemes, rotary representations, relative biases, or related methods.

## Training versus generation

During training on a sequence, causal masking allows all next-token predictions to be computed in parallel because the true prefix is known. During autoregressive generation, each new token depends on previously generated tokens, making decoding sequential across time even though computation within one step is highly parallel.

## KV cache

At generation step `t`, keys and values for earlier tokens need not be recomputed for every layer. A KV cache stores them. This exchanges memory for computation and changes serving economics dramatically.

## Build target

Implement a tiny decoder-only Transformer with:
- token embeddings;
- positional representation;
- causal multi-head attention;
- MLP;
- residual paths;
- normalization;
- vocabulary projection;
- cross-entropy loss.

First train on a tiny character corpus so every tensor can be inspected.

## Complete bounded trained build

[The trainable one-block decoder](training/README.md) now supplies every forward
operation, parameter gradients, tokenizer/embedding interface, causal shifted
objective, optimizer, serialization and generation. It explicitly differs from
the2017 encoder-decoder and does not reproduce that paper. Follow its stages
from scalar derivatives rather than copying a model class without derivation.
