# Postmortem: Silent Accuracy Degradation Caused by Feature Schema Shift

**Illustrative incident scenario — NOT an observed incident record.** No matching
execution trace was supplied for the accuracy, false-positive or PSI claims below.
They are hypotheses/illustrations and must not be cited as measured outcomes.
To convert this scenario into evidence, freeze a labeled evaluation set, retain
predictions before/after a controlled unit conversion, calculate the stated
metrics and link those outputs. Generic benchmark logs do not establish this
incident, and no live deployment is claimed.

## Incident Summary
- **Simulated Condition:** Upstream data pipeline changed unit scale for feature 0 (from seconds to milliseconds, a $\times 1000$ magnitude jump), without updating the serving interface.
- **Illustrative predicted behavior:** The model continues producing predictions without raising Python exceptions, while shifted features may saturate sigmoid predictions; quantify accuracy on a labeled set before claiming a measured collapse.
- **Impact:** Significant regression in model accuracy; false positives surged in downstream decision systems.
- **Root Cause:** Absence of pre-inference range checks allowed out-of-distribution values to saturate the sigmoid function into its asymptotic regime ($\approx 1.0$).
- **Detection:** Population Stability Index (PSI) jumped to $> 1.8$, triggering an automated drift alarm.
- **Mitigation & Repair:**
  1. Updated `FeatureSchemaValidator` with strict numerical bounds $[min\_val, max\_val]$ to fail fast on anomalous inputs.
  2. Integrated automated PSI drift monitoring to alert on gradual covariate shifts before accuracy collapse.
