"""Serial local inference/drift prototype with accumulated success latencies."""
import collections
import math
import time
from typing import Dict, List, Optional, Tuple

from pipeline import FeatureSchemaValidator, LogisticRegressionSGD, StandardScaler


class PopulationStabilityIndex:
    """Computes PSI across numeric feature distributions to detect production data drift."""

    def __init__(self, baseline_samples: List[float], n_bins: int = 5):
        self.n_bins = n_bins
        sorted_base = sorted(baseline_samples)
        n = len(sorted_base)
        self.bin_edges = []
        for i in range(1, n_bins):
            idx = int(i * n / n_bins)
            self.bin_edges.append(sorted_base[idx])
        self.expected_pcts = self._calc_pcts(sorted_base)

    def _calc_pcts(self, values: List[float]) -> List[float]:
        counts = [0] * self.n_bins
        for v in values:
            placed = False
            for b_idx, edge in enumerate(self.bin_edges):
                if v <= edge:
                    counts[b_idx] += 1
                    placed = True
                    break
            if not placed:
                counts[-1] += 1
        total = len(values) if values else 1
        # Add epsilon smoothing to avoid log(0)
        eps = 1e-4
        return [(c / total) + eps for c in counts]

    def compute_psi(self, current_samples: List[float]) -> float:
        actual_pcts = self._calc_pcts(current_samples)
        psi = 0.0
        for a, e in zip(actual_pcts, self.expected_pcts):
            psi += (a - e) * math.log(a / e)
        return max(0.0, psi)


class TokenBucketRateLimiter:
    def __init__(self, capacity: int = 50, refill_rate_per_sec: float = 20.0):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate_per_sec
        self.last_update = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        delta = now - self.last_update
        self.last_update = now
        self.tokens = min(float(self.capacity), self.tokens + delta * self.refill_rate)
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class ModelServer:
    def __init__(self, model: LogisticRegressionSGD, scaler: StandardScaler,
                 validator: FeatureSchemaValidator, baseline_features: List[List[float]],
                 max_batch_size: int = 16, rate_limit_cap: int = 100):
        self.model = model
        self.scaler = scaler
        self.validator = validator
        self.max_batch_size = max_batch_size
        self.rate_limiter = TokenBucketRateLimiter(capacity=rate_limit_cap, refill_rate_per_sec=float(rate_limit_cap))

        # Drift monitors per feature dimension
        self.drift_monitors = []
        n_features = len(baseline_features[0])
        for col_idx in range(n_features):
            col_vals = [row[col_idx] for row in baseline_features]
            self.drift_monitors.append(PopulationStabilityIndex(col_vals))

        self.recent_features_window: collections.deque = collections.deque(maxlen=200)
        self.latency_samples_ns: List[int] = []

        self.metrics = {
            "requests_total": 0,
            "requests_successful": 0,
            "rate_limited": 0,
            "schema_errors": 0,
            "batches_executed": 0,
            "drift_alerts": 0,
        }

    def predict(self, feature_vector: List[float]) -> Tuple[bool, Optional[int], Optional[float], Optional[str]]:
        self.metrics["requests_total"] += 1
        t_start = time.perf_counter_ns()

        if not self.rate_limiter.allow():
            self.metrics["rate_limited"] += 1
            return False, None, None, "RATE_LIMIT_EXCEEDED"

        valid, err = self.validator.validate(feature_vector)
        if not valid:
            self.metrics["schema_errors"] += 1
            return False, None, None, f"SCHEMA_VALIDATION_ERROR: {err}"

        # Record feature sample for drift monitoring
        self.recent_features_window.append(list(feature_vector))
        norm_x = self.scaler.transform_one(feature_vector)
        prob = self.model.predict_proba_one(norm_x)
        pred = 1 if prob >= 0.5 else 0

        elapsed = time.perf_counter_ns() - t_start
        self.latency_samples_ns.append(elapsed)
        self.metrics["requests_successful"] += 1
        return True, pred, prob, None

    def predict_batch(self, vectors: List[List[float]]) -> List[Tuple[bool, Optional[int], Optional[float], Optional[str]]]:
        self.metrics["batches_executed"] += 1
        results = []
        for vec in vectors:
            results.append(self.predict(vec))
        return results

    def check_drift(self) -> Dict[str, float]:
        if len(self.recent_features_window) < 50:
            return {"status": "INSUFFICIENT_SAMPLES", "max_psi": 0.0}

        max_psi = 0.0
        n_features = len(self.drift_monitors)
        psi_per_feature = {}
        for col_idx in range(n_features):
            current_vals = [row[col_idx] for row in self.recent_features_window]
            psi = self.drift_monitors[col_idx].compute_psi(current_vals)
            psi_per_feature[f"feature_{col_idx}_psi"] = psi
            if psi > max_psi:
                max_psi = psi

        is_drift = max_psi > 0.25
        if is_drift:
            self.metrics["drift_alerts"] += 1

        res = {"status": "DRIFT_DETECTED" if is_drift else "STABLE", "max_psi": max_psi}
        res.update(psi_per_feature)
        return res

    def get_latency_percentiles(self) -> Dict[str, float]:
        if not self.latency_samples_ns:
            return {"p50_ms": 0.0, "p95_ms": 0.0, "p99_ms": 0.0}
        sorted_samples = sorted(self.latency_samples_ns)
        n = len(sorted_samples)
        p50 = sorted_samples[int(n * 0.50)] / 1e6
        p95 = sorted_samples[int(n * 0.95)] / 1e6
        p99 = sorted_samples[min(n - 1, int(n * 0.99))] / 1e6
        return {"p50_ms": p50, "p95_ms": p95, "p99_ms": p99}
