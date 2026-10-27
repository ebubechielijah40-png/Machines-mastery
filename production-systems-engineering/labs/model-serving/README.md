# Model serving: serial inference, drift and admission counters

Runnable teaching prototype, not a hosted cloud endpoint. Learner NOT STARTED.

This local single-threaded prototype provides feature validation, standard scaling, logistic regression with stochastic gradient descent, a serial batch helper, Population Stability Index (PSI) monitoring and a single-thread token bucket. It does not implement a dynamic batching queue, concurrent admission safety, bounded lifetime telemetry retention or a public serving boundary.

## Prerequisites and Quickstart

Study [prerequisite bridge](PREREQUISITE_BRIDGE.md), [design](DESIGN.md), and [architecture](ARCHITECTURE.md) before inspecting code.

Run automated tests and benchmarks from the repository root:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/model-serving/tests -v
python3 production-systems-engineering/labs/model-serving/benchmark.py --output /tmp/my-serving-benchmark.json
```

## Structure and Evidence

- [DESIGN.md](DESIGN.md): Feature schema contracts, logistic regression SGD model, and drift monitoring.
- [ARCHITECTURE.md](ARCHITECTURE.md): Actual serial request pipeline and state limits.
- [ASSUMPTIONS.md](ASSUMPTIONS.md): Numerical stability limits, feature distributions, and drift thresholds.
- [BENCHMARKS.md](BENCHMARKS.md): Measured latency percentiles (p50/p95/p99) across batch sizes 1, 4, 16, 64.
- [EXPERIMENTS.md](EXPERIMENTS.md): Prepared learner protocols separating hypotheses from observations.
- [FAILURES.md](FAILURES.md): Covariate drift injection, NaN/Inf poisoning, and schema violation handling.
- [OBSERVABILITY.md](OBSERVABILITY.md): Latency tracking, rate limiting metrics, and PSI drift alarms.
- [SCALABILITY.md](SCALABILITY.md): Actual memory growth and the distinction between serial chunking and proposed batching.
- [SECURITY.md](SECURITY.md): Selected in-process rejection checks and single-thread limiter limitations.
- [ADR-001.md](ADR-001.md): Unimplemented batching proposal, explicitly separated from current code.
- [POSTMORTEMS.md](POSTMORTEMS.md): Labeled synthetic schema-change exercise; no real production incident.
- [RESULTS.md](RESULTS.md): Raw execution evidence from benchmark runs.
- [SOURCES.md](SOURCES.md): Primary references on ML serving, PSI statistics, and gradient descent.
