# Failures: Production ML Failure Injection

## Simulated Failure Modes

### 1. Covariate Drift (Distribution Shift)
- **Mechanism:** Injected feature values deviate significantly from training means ($\Delta \mu > 3\sigma$).
- **Consequence:** Predictions become uncalibrated; true accuracy drops while model reports false confidence.
- **Handling:** The PSI monitor detects statistical distribution divergence ($PSI > 0.25$) and triggers an alert for retraining or routing to fallback rules.

### 2. Malformed / Poisoned Feature Payloads
- **Mechanism:** Client submits input vector containing `NaN`, `Inf`, strings, or unexpected dimensional lengths.
- **Consequence:** Floating-point crash or unhandled runtime exceptions inside matrix math.
- **Handling:** Strict schema validation interceptor rejects malformed payloads before normalization, incrementing `schema_errors`.

### 3. Traffic Spikes and Resource Starvation
- **Mechanism:** Burst of requests exceeding processing capacity.
- **Consequence:** Latency degradation and memory buildup in request queues.
- **Handling:** Token-bucket rate limiter sheds excess load (`RATE_LIMIT_EXCEEDED`) to protect service SLOs.
