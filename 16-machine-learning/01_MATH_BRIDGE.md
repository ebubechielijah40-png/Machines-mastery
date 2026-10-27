# 01 — Mathematics bridge for machine learning

## Why the mathematics exists

A model is a function with adjustable parameters. Learning means changing those parameters so that the function behaves better on a defined objective. That immediately creates four mathematical needs:

- **vectors/matrices** to represent many quantities and transformations compactly;
- **probability** to reason about uncertain observations and predictions;
- **calculus** to ask how a small parameter change changes the objective;
- **optimization** to turn those local changes into an update rule.

### Vectors and dot products

For inputs `x = [x1, x2, ...]` and weights `w`, a linear unit computes `z = w·x + b`. The dot product is not magic: it is a weighted accumulation. If `w=[2,-1]` and `x=[3,5]`, then `z=2*3-1*5=1`. Each weight states how strongly a coordinate contributes locally.

A matrix is many such linear combinations at once. If `W` has shape `(out, in)`, then `Wx` maps an `in`-dimensional representation to an `out`-dimensional representation. Neural networks repeatedly alternate learned linear maps with nonlinear transformations.

### Derivatives and gradients

Suppose `L(w)=(w-3)^2`. The derivative `dL/dw=2(w-3)` tells the local slope. At `w=8`, the derivative is positive: decreasing `w` lowers the loss. Gradient descent performs

`w_new = w - learning_rate * gradient`.

The gradient is a vector of partial derivatives, one for each adjustable parameter. It is local information: it does not guarantee the globally best solution.

### Probability

Classification often outputs numbers interpreted as probabilities. A probability model is not a confidence oracle. Its meaning depends on the data-generating process and calibration. Cross-entropy is useful because maximizing likelihood under common categorical assumptions becomes minimizing negative log-likelihood.

### Softmax

For logits `z_i`, softmax uses

`p_i = exp(z_i) / sum_j exp(z_j)`.

Subtracting `max(z)` before exponentiating leaves the ratios unchanged and improves numerical stability.

## Worked application: two-feature classifier

Let `x=[temperature, vibration]`. A linear score can be `z=0.4*temperature+1.2*vibration-10`. If `z` is passed through a sigmoid, we obtain a number in `(0,1)`. Training changes the coefficients so observed labels receive lower loss.

The important point is causal structure of the computation:

```text
measurement → numeric representation → weighted combination → nonlinear map
→ prediction → compare with label → loss → gradient → parameter update
```

## Experiments

1. Plot `L(w)=(w-3)^2` for `w=-10..10`; compare finite-difference slopes with `2(w-3)`.
2. Run gradient descent with learning rates `0.01`, `0.1`, `1.0`, `2.0`. Predict which converge, oscillate, or diverge before running.
3. Compute softmax on `[1000,1001,1002]` naively and with max subtraction. Explain overflow behavior.

## Exercises

1. Compute a dot product by hand, then with Python.
2. Derive the derivative of `(2w+1)^2` using the chain rule.
3. Explain why multiplying every softmax numerator and denominator by the same positive constant does not change the result.
4. Give a real example where a well-calibrated probability still does not establish causality.
5. Implement finite-difference gradient checking for a two-parameter function.
