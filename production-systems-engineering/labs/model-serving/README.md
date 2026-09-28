# Resilient Model Serving: Dynamic Batching and Production Drift Detection

Runnable teaching prototype, not a hosted cloud endpoint. Learner NOT STARTED.

This laboratory provides an end-to-end production ML serving pipeline: feature validation, standard scaling, logistic regression classification with stochastic gradient descent from first principles, dynamic micro-batching, Population Stability Index (PSI) data drift monitoring, and token-bucket rate limiting.

## Prerequisites and Quickstart

Study [prerequisite bridge](PREREQUISITE_BRIDGE.md), [design](DESIGN.md), and [architecture](ARCHITECTURE.md) before inspecting code.

Run automated tests and benchmarks from the repository root:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/model-serving/tests -v
python3 production-systems-engineering/labs/model-serving/benchmark.py --output /tmp/my-serving-benchmark.json
```

## Structure and Evidence

- [DESIGN.md](DESIGN.md): Feature schema contracts, logistic regression SGD model, and drift monitoring.
- [ARCHITECTURE.md](ARCHITECTURE.md): Request pipeline, dynamic batching queue, and telemetry emission.
- [ASSUMPTIONS.md](ASSUMPTIONS.md): Numerical stability limits, feature distributions, and drift thresholds.
- [BENCHMARKS.md](BENCHMARKS.md): Measured latency percentiles (p50/p95/p99) across batch sizes 1, 4, 16, 64.
- [EXPERIMENTS.md](EXPERIMENTS.md): Prepared learner protocols separating hypotheses from observations.
- [FAILURES.md](FAILURES.md): Covariate drift injection, NaN/Inf poisoning, and schema violation handling.
- [OBSERVABILITY.md](OBSERVABILITY.md): Latency tracking, rate limiting metrics, and PSI drift alarms.
- [SCALABILITY.md](SCALABILITY.md): Throughput vs. queue latency trade-off (Little's Law) and micro-batching.
- [SECURITY.md](SECURITY.md): Input dimension bounds, float range clamping, and DoS mitigation via rate limiting.
- [ADR-001.md](ADR-001.md): Architectural decision record on dynamic batching vs. immediate per-item inference.
- [POSTMORTEMS.md](POSTMORTEMS.md): Blameless postmortem analyzing a production schema change that degraded model accuracy.
- [RESULTS.md](RESULTS.md): Raw execution evidence from benchmark runs.
- [SOURCES.md](SOURCES.md): Primary references on ML serving, PSI statistics, and gradient descent.
