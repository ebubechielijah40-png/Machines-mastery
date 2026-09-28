# Postmortem: Silent Accuracy Degradation Caused by Feature Schema Shift

## Incident Summary
- **Simulated Condition:** Upstream data pipeline changed unit scale for feature 0 (from seconds to milliseconds, a $\times 1000$ magnitude jump), without updating the serving interface.
- **Observed Behavior:** The model continued producing predictions without raising Python exceptions, but predicted output distributions collapsed toward 1.0, rendering classification useless.
- **Impact:** Significant regression in model accuracy; false positives surged in downstream decision systems.
- **Root Cause:** Absence of pre-inference range checks allowed out-of-distribution values to saturate the sigmoid function into its asymptotic regime ($\approx 1.0$).
- **Detection:** Population Stability Index (PSI) jumped to $> 1.8$, triggering an automated drift alarm.
- **Mitigation & Repair:**
  1. Updated `FeatureSchemaValidator` with strict numerical bounds $[min\_val, max\_val]$ to fail fast on anomalous inputs.
  2. Integrated automated PSI drift monitoring to alert on gradual covariate shifts before accuracy collapse.
