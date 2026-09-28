# Experiment atlas

Every experiment records question, hypothesis, setup, variables, procedure, raw output, analysis, alternative explanations, and limitations.

## Systems
- cache locality: sequential vs randomized access;
- allocation: many small allocations vs pooled reuse;
- concurrency: reproduce a race and fix with synchronization;
- scheduler: CPU-bound vs I/O-bound process behavior;
- virtual memory: working-set growth and page-fault observation using local tools;
- filesystem: buffered vs flushed writes and crash-consistency discussion.

## Networking
- TCP message framing across partial reads/writes;
- latency/throughput under concurrent clients;
- timeout/retry amplification;
- bounded queue/backpressure under burst traffic;
- DNS/cache expiration reasoning;
- local TLS failure modes.

## Databases/data systems
- indexed vs non-indexed query;
- transaction isolation interleavings;
- WAL/recovery toy model;
- batch size vs throughput/latency;
- duplicate/out-of-order event handling;
- schema migration compatibility;
- partition/skew effects.

## Security
- hash vs HMAC integrity;
- replay/freshness;
- password-KDF cost;
- authorization matrix tests;
- audit-log tampering;
- rate-limiting behavior;
- key-rotation simulation.

## AI/ML
- overfit a tiny dataset intentionally;
- learning-rate/batch-size sweep;
- data leakage demonstration;
- distribution shift;
- class imbalance and metric choice;
- inference latency vs batch size;
- model version rollback.

## Algorithms
Use `algorithmic-problem-solving/REAL_WORLD_COMPLEXITY_LABS.md`.

## Biology
- k-mer state-space growth;
- alignment scoring sensitivity;
- drift simulation vs population size;
- numerical integration step-size sensitivity;
- batch-effect/leakage toy study.

## Quantum
- phase/interference;
- Bell correlations in an ideal simulator;
- exponential statevector memory scaling;
- finite-shot sampling error;
- depth vs simplified noise.

## Physical machines
For each machine category: energy accounting, one state/response curve, one failure signature, and one model-vs-observation discrepancy. Physical work only with safe equipment and verified limits.
