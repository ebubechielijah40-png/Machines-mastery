# 08 — Attention

Attention is content-dependent weighted retrieval.

For representation matrix `X`, learned projections produce queries `Q`, keys `K`, and values `V`. Scaled dot-product attention is

`Attention(Q,K,V)=softmax(QK^T/sqrt(d_k))V`.

## Why three roles?

- **query**: what information this position is looking for;
- **key**: how each candidate advertises what it contains;
- **value**: the content returned if selected.

The dot product measures compatibility. Softmax converts scores into normalized positive weights. The weighted sum mixes values.

## Why scale by sqrt(d_k)?

If independent query/key components have roughly unit variance, their dot product variance grows with dimension. Large logits drive softmax toward saturation, producing tiny gradients for most entries. Dividing by `sqrt(d_k)` controls the scale.

## Causal masking

Autoregressive language modeling must not let position `t` see future tokens. A causal mask assigns impossible attention to positions `>t` before softmax, commonly by adding a large negative value.

## Multi-head attention

Multiple heads use different learned projections, allowing different relation subspaces in parallel. Concatenated head outputs are projected back into model dimension. Heads are not guaranteed to map cleanly to human-interpretable roles.

## Complexity

Standard self-attention materializes an `n × n` score matrix, giving quadratic sequence-length cost in the basic formulation. This is why long-context systems care about efficient attention, sparsity, chunking, memory, and hardware-aware kernels.

## Lab

Implement single-head causal self-attention in plain Python/NumPy. Test:
1. weights on each row sum to ~1;
2. future positions receive zero probability after masking;
3. duplicate values produce the expected weighted mixture;
4. increasing sequence length demonstrates quadratic score-matrix growth.
