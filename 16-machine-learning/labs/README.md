# Attention laboratory — run, inspect, break, reconstruct

Prerequisites: vectors, dot products, exponentials, probabilities, loops and functions. If missing, study the worked definitions in [Attention from first principles](../21_ATTENTION_FROM_FIRST_PRINCIPLES.md) first.

Run from repository root:

```sh
python3 16-machine-learning/labs/attention.py
python3 -m unittest discover -s 16-machine-learning/labs -v
```

This lab intentionally implements a *single-head*, **causally masked**, *untrained* attention operation without NumPy. It does not constitute a trained language model.

The developed companion now supplies the [complete derivative/cache derivation](DERIVATION.md),
[separate exercises](EXERCISES.md), [hints](HINTS.md), [solutions](SOLUTIONS.md),
[executed experiment](EXPERIMENT.md) and [inspected source map](SOURCES.md).
Incremental K/V reuse is implemented in `CausalCache`; rebuild it independently
before consulting the reference. Multi-head training and a complete Transformer
remain unfinished.

## Investigations

1. Predict the first row of attention weights before running. Explain why it is `[1,0,0]` regardless of scores.
2. Replace the final token by `[999, -999]`. Predict whether output positions 0 and 1 change. Verify against `test_no_lookahead_leakage`.
3. Toggle `scale=False`. Compare the final row's probability distribution, and explain why division by `sqrt(d_k)` matters as feature dimension increases. Repeat with different matrices.
4. Set `W_V` to all zeros. What happens to the outputs? Why can the attention weights remain nonzero?
5. Scale every query and key by a factor of ten. Does softmax become more concentrated? Explain why.
6. Add a padding mask of your own, with tests. Define a clear rule for sequences with no visible keys.
7. Add an incremental KV-cache implementation. Test equivalence to full causal computation and measure the computation/memory tradeoff. Do **not** assume equivalence without running tests.
8. Implement multi-head attention and test that concatenated heads have the expected dimension. Add an output projection.
9. Benchmark sequence lengths 8, 16, 32, 64 and 128; write measured times into your own `RESULTS.md`. Explain the quadratic interaction count for full attention.
10. Rebuild attention without looking at `attention.py`; prove correctness on a tiny two-token case by hand.

Tests demonstrate local properties only: they do not prove semantic understanding, model convergence, all input safety, or production readiness. Record real observations; don't fabricate outcomes.
