# Build a replica reconciliation workbench

A partition lets two nodes accept conflicting writes. Your task is to derive
which state they should retain after communication resumes and demonstrate
exactly which guarantees follow. This is a complete bounded local build, using
an implemented [ordered-map mechanism](../../15-distributed-systems/ordering-reconciliation/README.md)
and a runnable [schedule interface](code/workbench.py). The wider replicated
network service remains PARTIAL: there is no consensus, durable membership,
network transport or crash recovery in this workbench.

Begin with [entry tasks](PREREQUISITES.md), then [milestones](CHECKPOINTS.md).
Write a design attempt and predicted trace before opening [hints](HINTS.md)
or [reference reasoning](SOLUTIONS.md). Python3.10+, standard library only.

```bash
python3 projects-guided/p11-distributed-kv/code/workbench.py projects-guided/p11-distributed-kv/example.json
python3 -m unittest discover -s projects-guided/p11-distributed-kv/code -v
python3 -m unittest discover -s 15-distributed-systems/ordering-reconciliation -v
```

The JSON scenario names1–8 unique nodes and at most200 explicit events. A put
or delete creates a new immutable stamped record. A send captures an Envelope
under a unique label; deliver can replay that captured message to another node.
A read exposes the visible map. Delaying deliver models a communication gap;
it does not simulate real network queues or measure packet loss. Exact field
schemas and duplicate JSON keys are checked; no retrieved text or input string
is executed as code.

Architecture: scenario parser → typed event dispatcher → replica clock/state
transition → trace/final snapshots. The core module lives in the domain unit
so the project and lesson share one inspected implementation. The dispatcher
adds controlled schedule execution rather than duplicating that mechanism.
All state is fresh per invocation. A rejected scenario produces no returned
partial result or external mutation, but this is not persistent transactional
atomicity.

[Tests](TESTS.md) and [experiments](EXPERIMENTS.md) compare visible values,
record stamps, clock progression, duplicates, deletions and malformed inputs.
[Raw observations](evidence/observed.json) retain the actual14-event example.
[Production limits](PRODUCTION.md) explains the missing engineering; [sources](SOURCES.md)
states the theoretical scope. Deliver code, invariant proof, predicted/actual
trace, an observed negative control and an unaided reconstruction.
