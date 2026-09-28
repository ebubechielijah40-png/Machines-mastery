# Distributed Cluster: Quorum Consensus and Network Failure Injection

Runnable teaching prototype, not a production consensus engine. Learner NOT STARTED.

This laboratory implements a replicated state machine with Raft-like leader election, log replication, and majority quorum consensus over a deterministic simulated network. It provides executable mechanisms for fault injection, network partitions, split-brain prevention, HMAC peer authentication, and anti-replay protection.

## Prerequisites and Quickstart

Study [prerequisite bridge](PREREQUISITE_BRIDGE.md), [design](DESIGN.md), and [architecture](ARCHITECTURE.md) before inspecting the code.

Run automated tests and the benchmark suite from the repository root:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/distributed-cluster/tests -v
python3 production-systems-engineering/labs/distributed-cluster/benchmark.py --output /tmp/my-cluster-benchmark.json
```

## Structure and Evidence

- [DESIGN.md](DESIGN.md): Consensus state machine, message types, and term transitions.
- [ARCHITECTURE.md](ARCHITECTURE.md): Component interactions, network simulation, and log replication.
- [ASSUMPTIONS.md](ASSUMPTIONS.md): Synchrony bounds, crash-recovery model, and non-Byzantine failure assumptions.
- [BENCHMARKS.md](BENCHMARKS.md): Measured write commit throughput under 0% loss, 10% packet loss, and partition scenarios.
- [EXPERIMENTS.md](EXPERIMENTS.md): Prepared learner protocols separating hypotheses from observations.
- [FAILURES.md](FAILURES.md): Network partition injection, split-brain mitigation, and log divergence reconciliation.
- [OBSERVABILITY.md](OBSERVABILITY.md): Term tracking, election counters, message drop metrics, and replication lag.
- [SCALABILITY.md](SCALABILITY.md): Quorum overhead as cluster size grows ($N=3, 5, 7$), message complexity $O(N)$.
- [SECURITY.md](SECURITY.md): Inter-node HMAC tokens, monotonic nonces, replay rejection, and audit metrics.
- [ADR-001.md](ADR-001.md): Architectural decision record on quorum consensus vs. primary-backup replication.
- [POSTMORTEMS.md](POSTMORTEMS.md): Blameless postmortem analyzing a split-brain incident prevented by quorum requirements.
- [RESULTS.md](RESULTS.md): Raw execution evidence from local benchmark runs.
- [SOURCES.md](SOURCES.md): Primary references and conceptual foundations.
