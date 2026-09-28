"""Production ML feature pipeline, logistic regression training with SGD, and evaluation from first principles."""
import math
import random
from typing import Dict, List, Optional, Tuple


class StandardScaler:
    def __init__(self):
        self.mean: List[float] = []
        self.std: List[float] = []

    def fit(self, X: List[List[float]]):
        n_features = len(X[0])
        n_samples = len(X)
        self.mean = [sum(row[i] for row in X) / n_samples for i in range(n_features)]
        self.std = []
        for i in range(n_features):
            variance = sum((row[i] - self.mean[i]) ** 2 for row in X) / n_samples
            self.std.append(math.sqrt(variance) if variance > 1e-9 else 1.0)

    def transform(self, X: List[List[float]]) -> List[List[float]]:
        return [[(row[i] - self.mean[i]) / self.std[i] for i in range(len(row))] for row in X]

    def transform_one(self, x: List[float]) -> List[float]:
        return [(x[i] - self.mean[i]) / self.std[i] for i in range(len(x))]


class FeatureSchemaValidator:
    def __init__(self, expected_dim: int, min_val: float = -1000.0, max_val: float = 1000.0):
        self.expected_dim = expected_dim
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, x: List[float]) -> Tuple[bool, Optional[str]]:
        if not isinstance(x, (list, tuple)):
            return False, "Feature vector must be a sequence"
        if len(x) != self.expected_dim:
            return False, f"Expected {self.expected_dim} features, got {len(x)}"
        for i, val in enumerate(x):
            if not isinstance(val, (int, float)):
                return False, f"Feature at index {i} is not a numeric value"
            if math.isnan(val) or math.isinf(val):
                return False, f"Feature at index {i} contains NaN or Infinite value"
            if val < self.min_val or val > self.max_val:
                return False, f"Feature at index {i} ({val}) out of allowed bounds [{self.min_val}, {self.max_val}]"
        return True, None


class LogisticRegressionSGD:
    def __init__(self, n_features: int, lr: float = 0.05, l2_reg: float = 0.001):
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.lr = lr
        self.l2_reg = l2_reg

    @staticmethod
    def sigmoid(z: float) -> float:
        if z < -20.0:
            return 0.0
        if z > 20.0:
            return 1.0
        return 1.0 / (1.0 + math.exp(-z))

    def predict_proba_one(self, x: List[float]) -> float:
        z = self.bias + sum(w * xi for w, xi in zip(self.weights, x))
        return self.sigmoid(z)

    def predict_one(self, x: List[float], threshold: float = 0.5) -> int:
        return 1 if self.predict_proba_one(x) >= threshold else 0

    def fit(self, X: List[List[float]], y: List[int], epochs: int = 50, seed: int = 42):
        rng = random.Random(seed)
        indices = list(range(len(X)))
        for _ in range(epochs):
            rng.shuffle(indices)
            for idx in indices:
                xi = X[idx]
                yi = y[idx]
                p = self.predict_proba_one(xi)
                err = p - yi
                for j in range(len(self.weights)):
                    grad = err * xi[j] + self.l2_reg * self.weights[j]
                    self.weights[j] -= self.lr * grad
                self.bias -= self.lr * err


def evaluate_classifier(y_true: List[int], y_pred: List[int], y_prob: List[float]) -> Dict[str, float]:
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    total = len(y_true)

    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Cross-entropy log loss
    eps = 1e-15
    log_loss = -sum(
        yt * math.log(max(eps, min(1.0 - eps, p))) + (1 - yt) * math.log(max(eps, min(1.0 - eps, 1.0 - p)))
        for yt, p in zip(y_true, y_prob)
    ) / total if total > 0 else 0.0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "log_loss": log_loss,
    }


def generate_synthetic_data(n_samples: int = 500, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    rng = random.Random(seed)
    X = []
    y = []
    for _ in range(n_samples):
        # 4 features: request_rate, error_rate, payload_kb, latency_ms
        c = rng.choice([0, 1])
        if c == 0:
            feat = [
                rng.gauss(50.0, 10.0),
                rng.gauss(1.0, 0.5),
                rng.gauss(10.0, 2.0),
                rng.gauss(20.0, 5.0),
            ]
        else:
            feat = [
                rng.gauss(120.0, 25.0),
                rng.gauss(8.0, 2.0),
                rng.gauss(40.0, 10.0),
                rng.gauss(80.0, 15.0),
            ]
        X.append(feat)
        y.append(c)
    return X, y
