# Benchmarks: Model Serving Latency and Dynamic Batching

## Methodology
`benchmark.py` measures:
1. **Dynamic Batching:** Executes 200 inference requests across batch sizes 1, 4, 16, 64. Records total wall time, throughput in requests per second, and latency percentiles (p50, p95, p99).
2. **Drift Detection Sensitivity:** Feeds 100 baseline samples followed by 100 covariate-shifted samples, computing PSI across all feature dimensions.

## Summary of Measured Results
From `research/model-serving-benchmark.json`:
- **Inference Latency:** Per-item inference takes ~10–15 microseconds; p50, p95, and p99 remain sub-millisecond across all batch configurations.
- **Batch Scaling Throughput:** Batch processing achieves ~65,000–90,000 requests per second in pure Python without external dependencies.
- **Drift Detection:**
  - Normal traffic: Maximum feature PSI < 0.10, status reported as `STABLE`.
  - Shifted traffic: Maximum feature PSI > 0.30, status immediately switches to `DRIFT_DETECTED` and triggers metric alert.
