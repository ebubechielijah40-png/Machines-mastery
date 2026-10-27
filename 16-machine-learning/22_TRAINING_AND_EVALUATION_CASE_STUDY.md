# Training a predictor and discovering when its apparent accuracy lies

## Why this exists

A model can minimize error on examples it has seen and still fail on new examples. The engineering goal is not merely a low training loss but evidence of performance on data representative of future use. A predictor is a function plus a data-generation and evaluation process; changing the data-generating process changes what performance claims mean.

## Derive linear regression

Assume a scalar input `x` and target `y`. Let prediction `ŷ = wx + b`. Squared error on example `i` is `(ŷ_i-y_i)^2`. Over `N` examples, mean squared error is `L = (1/N) Σ (wx_i+b-y_i)^2`. Differentiating gives `∂L/∂w = (2/N) Σ x_i(wx_i+b-y_i)` and `∂L/∂b = (2/N) Σ(wx_i+b-y_i)`. Gradient descent updates `w ← w-η∂L/∂w`, `b ← b-η∂L/∂b`. The learning rate η matters: too large may overshoot; too small may converge slowly. These statements assume the objective and gradient are implemented correctly; they do not imply every dataset has a reliable linear relationship.

## The measurement trap

Imagine a dataset of delivery durations. A model trained on weekday city-center deliveries might show low error. If evaluated only on randomly split records from the same period, it can appear reliable. But deployment includes holiday traffic, bad weather and new locations; the sample no longer represents the intended environment. No optimization algorithm repairs a broken measurement or sampling design automatically.

Data leakage is distinct: suppose the predictor includes `arrival_timestamp`, a field known only *after* delivery. It will look accurate offline yet cannot operate prospectively. A valid evaluation must define which information exists at prediction time.

## Experiment plan

1. Construct deterministic synthetic data `y = 2x+1+noise` using a fixed random seed; split before fitting any preprocessing parameters.
2. Train a linear model from initialized `w,b` by explicit gradients. Test that the gradient matches a finite-difference approximation on a small batch.
3. Compare train and held-out MSE; record actual values rather than expected claims.
4. Make a shifted test set `y=4x+1+noise` without retraining. Compare error; explain distribution shift.
5. Intentionally leak the target as a feature on an offline dataset, then forbid that feature at prediction time. Explain why the previous metric did not support the deployment claim.
6. Add feature scaling learned **only from training data**; compare convergence. Record what changed and what stayed constant.
7. Profile running time and memory as data size changes. Discuss scaling of one gradient step with `N` and feature count `d`.

## Production decision exercise

You're building an ETA service for users. Define an API request/response schema, what inputs are known before travel, acceptable error metrics (including percentiles and subgroups), a retraining trigger, logging that avoids retaining unnecessary personal data, and a fall-back ETA if the model service fails. A 1% improvement in training MSE by itself does not justify rollout. Propose an experiment that would justify it, including an independent evaluation set and rollback criterion.

## Questions and limits

- Why is training loss not an unbiased measure of generalization?
- What does a held-out test set establish, and what does it not establish about tomorrow's population?
- How would you discover leakage without seeing source code for the feature pipeline?
- Why is MSE particularly sensitive to unusually large errors?
- Derive the update for `w` on a single example `x=2,y=5,w=0,b=0,η=0.1`. (Check: gradient `-20`, so new `w=2`.)
- Explain how security boundaries apply when features contain sensitive user data.

This exercise does not prove any production model's effectiveness. Its synthetic measurements support only the particular generated cases and runtime environment. Consult the existing `code/linear_model.py` and its tests as one starting implementation, but do not treat passing tests as evidence of unbiased data collection.
