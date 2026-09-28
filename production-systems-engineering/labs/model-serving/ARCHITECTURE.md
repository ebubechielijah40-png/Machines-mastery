# Architecture: Production ML Serving Pipeline

## Component Pipeline

```text
Request Input Vector
         |
         v
+-------------------------------+
|  Token Bucket Rate Limiter    | ---> (Rejected: RATE_LIMIT_EXCEEDED)
+-------------------------------+
         | (allowed)
         v
+-------------------------------+
|  Feature Schema Validator     | ---> (Rejected: SCHEMA_ERROR / NaN)
+-------------------------------+
         | (valid)
         +--------------------------------------+
         |                                      |
         v                                      v
+-------------------------------+      +-------------------------------+
|     Z-Score Standardization   |      |  Sliding Window Drift Monitor |
+-------------------------------+      |  - Binned PSI computation     |
         |                             |  - Drift alert if PSI > 0.25  |
         v                             +-------------------------------+
+-------------------------------+
|   Logistic Regression Model   |
|   - Vector dot product        |
|   - Clamped sigmoid proba     |
+-------------------------------+
         |
         v
Prediction & Latency Telemetry
```

## State & Isolation
- The model weights and scaling parameters are strictly read-only during inference.
- The drift monitor updates an in-memory bounded ring buffer (`maxlen=200`).
- Latency samples are collected in an in-memory list for percentile calculations.
