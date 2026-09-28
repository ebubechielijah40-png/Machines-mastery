# Observability: Model Serving Telemetry

## Instrumented Metrics

### Request Metrics
- `requests_total`: Total inference requests received.
- `requests_successful`: Requests passing validation and producing valid predictions.
- `rate_limited`: Inferences rejected due to token bucket depletion.
- `schema_errors`: Inferences rejected due to dimension, type, or bounds validation failures.
- `batches_executed`: Number of batch operations dispatched.

### Statistical & Health Metrics
- `drift_alerts`: Counter incremented whenever maximum feature PSI exceeds 0.25.
- `latency_percentiles`: Rolling p50, p95, and p99 inference durations in milliseconds.
- `psi_per_feature`: Individual feature-level PSI metrics for localized drift root-cause isolation.
