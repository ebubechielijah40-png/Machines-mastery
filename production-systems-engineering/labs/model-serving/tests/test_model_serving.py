"""Test suite for ML feature pipeline, model serving, drift monitoring (PSI), and resilience."""
import sys
import unittest
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB_DIR))

from pipeline import (
    StandardScaler,
    FeatureSchemaValidator,
    LogisticRegressionSGD,
    evaluate_classifier,
    generate_synthetic_data,
)
from service import ModelServer, PopulationStabilityIndex


class ModelServingTests(unittest.TestCase):
    def setUp(self):
        self.X_train, self.y_train = generate_synthetic_data(n_samples=400, seed=42)
        self.scaler = StandardScaler()
        self.scaler.fit(self.X_train)
        self.X_train_norm = self.scaler.transform(self.X_train)

        self.model = LogisticRegressionSGD(n_features=4, lr=0.08, l2_reg=0.001)
        self.model.fit(self.X_train_norm, self.y_train, epochs=40, seed=42)

        self.validator = FeatureSchemaValidator(expected_dim=4, min_val=-1000.0, max_val=1000.0)
        self.server = ModelServer(
            model=self.model,
            scaler=self.scaler,
            validator=self.validator,
            baseline_features=self.X_train,
            rate_limit_cap=200,
        )

    def test_pipeline_training_and_accuracy(self):
        X_test, y_test = generate_synthetic_data(n_samples=100, seed=99)
        X_test_norm = self.scaler.transform(X_test)
        y_prob = [self.model.predict_proba_one(x) for x in X_test_norm]
        y_pred = [1 if p >= 0.5 else 0 for p in y_prob]

        metrics = evaluate_classifier(y_test, y_pred, y_prob)
        self.assertGreater(metrics["accuracy"], 0.80)
        self.assertGreater(metrics["f1"], 0.80)
        self.assertLess(metrics["log_loss"], 0.50)

    def test_schema_validation_rejection(self):
        # 1. Dimension mismatch
        ok, pred, prob, err = self.server.predict([10.0, 20.0])
        self.assertFalse(ok)
        self.assertIn("Expected 4 features", err)

        # 2. NaN value
        ok, pred, prob, err = self.server.predict([float("nan"), 1.0, 2.0, 3.0])
        self.assertFalse(ok)
        self.assertIn("NaN or Infinite", err)

        # 3. Out-of-bounds value
        ok, pred, prob, err = self.server.predict([5000.0, 1.0, 2.0, 3.0])
        self.assertFalse(ok)
        self.assertIn("out of allowed bounds", err)

        self.assertEqual(self.server.metrics["schema_errors"], 3)

    def test_serial_batch_helper_and_prediction(self):
        batch = [self.X_train[i] for i in range(10)]
        results = self.server.predict_batch(batch)
        self.assertEqual(len(results), 10)
        for ok, pred, prob, err in results:
            self.assertTrue(ok)
            self.assertIn(pred, (0, 1))
            self.assertTrue(0.0 <= prob <= 1.0)
            self.assertIsNone(err)

    def test_drift_detection_psi(self):
        # Normal traffic from same distribution
        X_normal, _ = generate_synthetic_data(n_samples=60, seed=123)
        for x in X_normal:
            self.server.predict(x)
        normal_status = self.server.check_drift()
        self.assertEqual(normal_status["status"], "STABLE")
        self.assertLess(normal_status["max_psi"], 0.25)

        # Shifted traffic: Covariate shift (severe anomaly / distribution shift)
        shifted_features = [
            [x[0] + 250.0, x[1] + 30.0, x[2] + 150.0, x[3] + 200.0]
            for x in X_normal
        ]
        for x in shifted_features:
            self.server.predict(x)

        drift_status = self.server.check_drift()
        self.assertEqual(drift_status["status"], "DRIFT_DETECTED")
        self.assertGreater(drift_status["max_psi"], 0.25)
        self.assertGreaterEqual(self.server.metrics["drift_alerts"], 1)

    def test_rate_limiter(self):
        restricted_server = ModelServer(
            model=self.model,
            scaler=self.scaler,
            validator=self.validator,
            baseline_features=self.X_train,
            rate_limit_cap=5,
        )
        successes = 0
        limited = 0
        for _ in range(10):
            ok, _, _, err = restricted_server.predict([50.0, 1.0, 10.0, 20.0])
            if ok:
                successes += 1
            else:
                limited += 1
        self.assertEqual(successes, 5)
        self.assertEqual(limited, 5)
        self.assertEqual(restricted_server.metrics["rate_limited"], 5)


if __name__ == '__main__':
    unittest.main()
