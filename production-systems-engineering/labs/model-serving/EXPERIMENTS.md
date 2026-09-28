# Experiments: Model Serving

Learner state: **NOT STARTED**. These are prepared local experiments. Existing benchmark files are agent-run validation evidence for the teaching material, not learner mastery.

## Experiment 1 — Batch size versus latency and throughput

**Question:** When does larger batching improve throughput enough to justify added queueing delay?

**Hypothesis:** Larger batches reduce per-item overhead up to a point, while request waiting time eventually dominates tail latency.

**Independent variable:** maximum batch size (and, in a learner extension, batch wait timeout).

**Dependent variables:** throughput, p50/p95/p99 request latency, queue depth and rejected requests.

**Controls:** same model parameters, feature set, request count, seed and machine.

**Procedure:** run batch sizes 1, 4, 16 and 64 to new output files; preserve all raw samples; compare throughput and tail latency rather than averages alone. Then explain why a single fastest benchmark does not define the correct production batch size.

**Observed result:** **NOT YET OBSERVED by learner.**

## Experiment 2 — Distribution shift without label feedback

Generate baseline feature traffic, then inject a controlled shift in one or more dimensions. Record PSI values and service alerts. Before running, predict which dimensions should trigger first.

Then answer: drift detection can tell us the input distribution changed, but can it prove accuracy fell without labels? State exactly what evidence would be needed to establish degraded predictive quality.

**Observed result:** **NOT YET OBSERVED by learner.**

## Experiment 3 — Malformed input and resource protection

Send bounded local requests with wrong dimensionality, `NaN`, `Inf`, extreme values and a request burst above the configured token-bucket capacity. Record rejection reason, counters and whether invalid data reaches normalization/model code.

The learner must distinguish correctness validation, security boundary validation and overload protection; they solve different failure modes.

**Observed result:** **NOT YET OBSERVED by learner.**

## Experiment 4 — Model change as a production migration

Create a second compatible model version or preprocessing configuration. Define a version identifier, expected feature schema and rollback condition. Route a bounded synthetic sample to each version and compare output distribution, latency and validation failures.

Do not describe this as canary deployment unless the implementation actually routes a controlled fraction and records comparable metrics. A design sketch alone is not execution evidence.

**Observed result:** **NOT YET OBSERVED by learner.**
