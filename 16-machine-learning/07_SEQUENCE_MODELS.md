# 07 — Sequence models before Transformers

Sequences introduce order and variable context. A recurrent neural network updates hidden state `h_t=f(x_t,h_{t-1})`, so history is compressed into a fixed-size evolving representation.

This creates both power and difficulty. Information must survive repeated state transitions. Gradients must also travel through those transitions during backpropagation through time, producing vanishing/exploding-gradient problems.

LSTM/GRU architectures introduce gated pathways that make retention and forgetting learnable. They improved long-range sequence modeling but retain sequential computation: token `t+1` depends on completion of token `t`, limiting training parallelism.

## Experiment

Create a synthetic task: predict whether the first bit of a length-N sequence was 1. Increase N. Compare a simple RNN and a gated recurrent unit. Track accuracy and gradient norms as N grows.

## Why attention emerged

Instead of forcing all history through one recurrent state, attention allows a query to select information directly from a set of prior representations. That changes path length between distant positions and enables much more parallel computation.
