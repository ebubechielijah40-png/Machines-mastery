# 05 — Neural networks from first principles

A feed-forward neural network alternates learned affine transformations with nonlinear functions. Without the nonlinear step, a stack of linear layers collapses into one linear transformation.

## Neuron to multilayer perceptron

A neuron computes `z=w·x+b`, then `a=phi(z)`. A layer computes many such units in parallel. An MLP composes layers:

`x → W1x+b1 → phi → W2h+b2 → ... → output`.

The weights are not rules written by a programmer. They are numbers adjusted so the composed function lowers the training objective.

## Representation learning

Hidden activations are intermediate representations useful to downstream layers. “Feature learning” means optimization discovers transformations that make the objective easier—not that a neuron necessarily corresponds to one human concept.

## Initialization

If weights are all identical, symmetric units receive identical gradients and fail to diversify. Variance-aware initialization attempts to keep activation and gradient scales from systematically exploding or vanishing with depth.

## Normalization and residual paths

Normalization stabilizes activation statistics under specific assumptions. Residual connections give layers a direct identity-like route, making it easier to learn incremental transformations and propagate gradients through deep networks.

## Lab

The complete [MLP derivation and runnable build](training/README.md) proves the linear-boundary limitation, implements a two-layer tanh MLP using the scalar engine, differentiates its mean squared error and actually trains XOR. Use [the guided neural project](../projects-guided/p12-neural-net/README.md) and its separate exercises before inspecting the reference. All four XOR rows are training data; a good fit is not held-out generalization.

## Questions

- Why can a deep network still underfit?
- Why does zero training loss not imply useful deployment behavior?
- What information is lost when an activation saturates?
- Why can more parameters sometimes make optimization easier even though capacity rises?
