# Assumptions: Model Serving System

## Baseline and Environment Assumptions
1. **Numerical Stability:** Exponential input to the sigmoid is clamped to $[-20.0, 20.0]$ to eliminate floating-point overflow and underflow exceptions.
2. **Feature Scale:** Features are assumed to follow approximately unimodal, finite-variance distributions during normal operation.
3. **Drift Horizon:** A sample window of 50–200 inferences is assumed sufficient to detect macroscopic distributional shift via PSI without excessive memory allocation.
4. **Single-Node In-Process:** The serving prototype executes within a single Python runtime without distributed coordination or external RPC overhead.
5. **No Concept Inversion:** The relationship between features and labels $P(Y|X)$ is assumed stable in baseline conditions; covariate shift $P(X)$ is detected as an indicator of potential predictive degradation.
