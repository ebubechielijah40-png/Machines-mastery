# What the model-serving counters measure

`requests_total` counts calls, including rejected calls. Successful, rate-limited
and schema-error counters record their corresponding branches. `batches_executed`
counts calls to the serial helper, not dynamic dispatches. `drift_alerts` counts
checks exceeding a chosen PSI threshold, not distinct production incidents.

`latency_samples_ns` accumulates successful inference intervals in an unbounded
list. It excludes rejected calls, waiting before the function and external
transport. It is not rolling telemetry or an all-offer latency distribution.
The historical empty result uses0.0, which must not be read as a measured empty
window latency. Historical percentile indexing is the code's declared convention,
not necessarily another library's percentile convention.

Use [population-correct pooled histograms and explicit empty windows](../operation-workbench/RECOVERY_AND_OBSERVABILITY.md)
for the developed bounded operational mechanism. This older helper remains a
finite inference/drift study, not a complete observability implementation.
