# Design: Model Serving and Production Drift Guard

## Objective
Provide an educational, zero-dependency production ML inference pipeline with robust schema validation, dynamic micro-batching, real-time drift detection, rate limiting, and observability.

## Pipeline Components
1. **Schema Validator:** Checks vector dimension, data types, nulls/NaNs/Infs, and bounded numeric ranges before computation.
2. **Standard Scaler:** Transforms raw inputs using frozen training parameters ($\mu, \sigma$).
3. **Logistic Regression Engine:** Pure-Python vector dot product with clamped sigmoid function to prevent floating-point overflow.
4. **Drift Monitor (PSI):** Sliding window of recent production feature samples compared against baseline quartiles/quantiles.
5. **Token Bucket Rate Limiter:** Protects the inference engine from sudden concurrency spikes and starvation.
