"""Finite serial chunking and synthetic drift benchmark; no dynamic batching."""
import argparse
import json
from pathlib import Path
import platform
import time

from pipeline import (
    FeatureSchemaValidator,
    LogisticRegressionSGD,
    StandardScaler,
    generate_synthetic_data,
)
from service import ModelServer


def run_benchmark():
    result = {
        "kind": "agent model serving benchmark; no learner evidence",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "scenarios": {},
    }

    # Setup model and server
    X_train, y_train = generate_synthetic_data(n_samples=500, seed=42)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_norm = scaler.transform(X_train)

    model = LogisticRegressionSGD(n_features=4, lr=0.08, l2_reg=0.001)
    model.fit(X_train_norm, y_train, epochs=50, seed=42)

    validator = FeatureSchemaValidator(expected_dim=4, min_val=-1000.0, max_val=1000.0)

    # 1. Batch size scalability: 1, 4, 16, 64
    test_vectors, _ = generate_synthetic_data(n_samples=200, seed=99)
    batch_sizes = [1, 4, 16, 64]
    batch_results = {}

    for bsize in batch_sizes:
        server = ModelServer(
            model=model,
            scaler=scaler,
            validator=validator,
            baseline_features=X_train,
            max_batch_size=bsize,
            rate_limit_cap=1000,
        )
        t_start = time.perf_counter_ns()
        # Feed batches
        for i in range(0, len(test_vectors), bsize):
            chunk = test_vectors[i:i + bsize]
            server.predict_batch(chunk)
        elapsed_ns = time.perf_counter_ns() - t_start

        percentiles = server.get_latency_percentiles()
        req_per_sec = (len(test_vectors) / (elapsed_ns / 1e9)) if elapsed_ns > 0 else 0.0

        batch_results[f"batch_size_{bsize}"] = {
            "total_requests": len(test_vectors),
            "batches_executed": server.metrics["batches_executed"],
            "wall_time_ns": elapsed_ns,
            "throughput_req_per_sec": req_per_sec,
            "latency": percentiles,
        }

    result["scenarios"]["batch_scaling"] = batch_results

    # 2. Data Drift Monitoring scenario: Normal vs Covariate Shift
    server_drift = ModelServer(
        model=model,
        scaler=scaler,
        validator=validator,
        baseline_features=X_train,
        rate_limit_cap=1000,
    )

    # Ingest 100 normal samples
    normal_samples, _ = generate_synthetic_data(n_samples=100, seed=101)
    for x in normal_samples:
        server_drift.predict(x)
    normal_drift = server_drift.check_drift()

    # Ingest 100 shifted samples (covariate shift)
    shifted_samples = [
        [x[0] + 180.0, x[1] + 15.0, x[2] + 80.0, x[3] + 90.0]
        for x in normal_samples
    ]
    for x in shifted_samples:
        server_drift.predict(x)
    shifted_drift = server_drift.check_drift()

    result["scenarios"]["drift_detection"] = {
        "normal_traffic": normal_drift,
        "shifted_traffic": shifted_drift,
        "drift_alerts_triggered": server_drift.metrics["drift_alerts"],
    }

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Output path for benchmark JSON.')
    args = parser.parse_args()

    bench_data = run_benchmark()
    with args.output.open('x') as f:
        json.dump(bench_data, f, indent=2)
        f.write('\n')
    print(f"PASS: recorded model serving benchmark to {args.output}")
