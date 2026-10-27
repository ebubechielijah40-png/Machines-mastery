# 04 — Optimization

Training is an optimization process over a noisy objective. The optimizer does not “understand” the task; it follows information encoded in gradients and state.

## SGD

For mini-batch gradient `g_t`, SGD applies `theta_{t+1}=theta_t-eta*g_t`. Smaller batches produce noisier estimates that can help exploration but reduce hardware efficiency. Larger batches reduce variance but can require learning-rate changes and more memory.

## Momentum

Momentum maintains a velocity-like state so consistent gradients accumulate while oscillating components partly cancel. This matters in ravine-shaped loss surfaces where one direction is steep and another shallow.

## Adam

Adam maintains exponential moving averages of first and second moments of gradients and applies bias correction. It is convenient and robust across many problems, but “Adam works” is not an explanation: effective step size depends on gradient scale, epsilon, beta values, weight decay variant, batch statistics, and schedule.

## Learning-rate schedules

Warmup prevents large unstable updates while representations/optimizer statistics are immature. Decay reduces update magnitude later. Cosine schedules are common because they smoothly anneal without abrupt phase changes.

## Experiment matrix

Train the same small network with:
- SGD at three learning rates;
- momentum;
- Adam;
- identical optimizer with/without gradient clipping.

Log loss, gradient norm, parameter norm, wall time, and validation metric. Do not declare a winner from one random seed.

## Production concern

Optimization choices affect reproducibility, checkpoint compatibility, GPU memory, distributed communication, and recovery after interruption. A training system is an operational system as well as a mathematical one.
