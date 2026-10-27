# Actual model-serving design

This is a serial teaching prototype. `predict` consumes a global token, validates
features, scales with frozen training parameters, evaluates a logistic model and
retains a success latency. `predict_batch` loops through `predict`; it is not a
queue, timed dispatch mechanism or vectorized inference engine. `max_batch_size`
is stored but not enforced by that helper.

The token bucket has no lock or fairness queue. Use it only in the single-thread
lab; it does not protect concurrent callers or prevent starvation. Rate limiting
and bounding running/waiting work are different mechanisms; the
[operation workbench](../operation-workbench/README.md) teaches the latter.

A200-feature-vector deque bounds recent drift input. It does not bound the
latency list, which grows for every successful call. PSI threshold.25 is a chosen
synthetic guard, not calibrated evidence of model failure, causality or safety.
