# Applied domain laboratory plan

These are scoped domain labs; the [event ledger](labs/event-ledger/README.md), [distributed cluster](labs/distributed-cluster/README.md), and [model serving](labs/model-serving/README.md) labs are executable now, alongside the [growth complexity benchmark](../algorithmic-problem-solving/experiments/growth/README.md). Each needs internal prerequisites before learner execution.

## algorithms

Implement naive and improved search/deduplication, count operations and measure growth; vary distribution and sizes. Apply hashes in a bounded cache, heaps to a scheduler, graphs to routing, tries to autocomplete, queues to jobs, sorting to ingestion and dynamic programming to constrained optimization. Runnable exemplar: [algorithmic growth experiment](../algorithmic-problem-solving/experiments/growth/README.md).

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## operating-systems

Create processes/threads, inspect descriptors, pipes, signals, IPC, scheduling, allocation and virtual memory. Reproduce a local race/deadlock with time limits, diagnose using evidence, repair and compare. Tools and commands require source/version inspection before execution.

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## memory-and-hardware

Compare allocation, copying, buffering, sequential/random access, loop ordering and branch workloads. Record workload, compiler flags, assembly, CPU time and memory method; do not infer cache misses from wall time alone. Memory maps/leaks/fragmentation need bounded storage and actual observations.

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## networking

Local socket service with framing, timeouts, slow clients, restarts, delays and request bursts; measure latency/throughput/connections/errors. A local in-process call is not a network benchmark.

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## data-systems

Generate 1k/100k/1m rows; measure ingestion, serialization, validation, cleaning, storage/index/query costs, batch versus streaming, concurrent writes, transactions, lineage/schema evolution. Inject duplicates, ordering changes, missing/corrupted records and partial processing. Design recovery and reconcile counts. Runnable exemplar: [event ledger lab](labs/event-ledger/README.md).

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## databases

Inspect a slow-query plan, normalization/denormalization, indexes, isolation, locking, pool bounds, pagination and migrations. The “50 million records / 12 seconds” scenario is synthetic until a dataset and measurement are supplied. Do not invent its root cause. Runnable exemplar: [event ledger lab](labs/event-ledger/README.md).

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## distributed-systems

Use a deterministic local transport to delay/drop/duplicate/reorder messages between replicas. Compare leader/follower, retries/idempotency, conflicting updates, eventual reads and partitions. No simplified model certifies production consensus. Runnable exemplar: [distributed cluster lab](labs/distributed-cluster/README.md).

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## security-and-privacy

Build a local synthetic application with deliberately broken authorization/input checks, then demonstrate, detect, mitigate and regression-test it. Threat model, trust boundaries and data minimization first. Plan key rotation/revocation, audit, rate limits and authorization-dependency failure without attacking external systems or using real secrets.

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## ai-ml

Build data splits, baseline, feature pipeline, training/evaluation/inference and a local serving interface. Vary size/complexity/rate/batch/features and measure quality, train/inference cost and memory. Inject shift/noise/missing features/imbalance/leakage/overfit/underfit; distinguish production drift from training loss. Pin model/data versions and privacy/security boundaries. Runnable exemplar: [model serving lab](labs/model-serving/README.md).

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.

## embedded-robotics

Trace sensor → ADC → firmware → decision → actuator → feedback. Inject simulated delay/dropout/saturation before real hardware, then use verified low-energy equipment if available. Measure jitter/error/power only with actual instruments and limits.

Required cycle: hypothesis → controlled baseline → code change → new measurement → failure/recovery → explanation of limits.
