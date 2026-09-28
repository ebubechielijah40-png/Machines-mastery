# Experiments: Distributed Cluster

Learner state: **NOT STARTED**. These experiments are prepared protocols. The existing benchmark JSON under `research/` is agent-run material validation and does not count as learner evidence.

## Experiment 1 — Quorum survival under packet loss

**Question:** How much packet loss can the simplified cluster tolerate before commit latency or success changes materially?

**Hypothesis:** Moderate independent packet loss should increase retries and simulated completion time while preserving safety as long as a majority can still communicate.

**Independent variable:** deterministic network drop rate.

**Dependent variables:** committed writes, simulated ticks to completion, messages sent/delivered/dropped, retry rounds.

**Controls:** same cluster size, seed, write count and message latency.

**Procedure:**

1. Run the baseline with zero loss and save a new output file.
2. Repeat with increasing bounded loss rates supported by the benchmark or a learner-owned extension.
3. Keep the random seed fixed for one comparison series, then repeat with different seeds.
4. Do not change election/heartbeat constants during the first comparison.
5. Plot or tabulate completion time and delivery counts against loss rate.
6. Inspect whether any committed history diverges between nodes.

**Failure criterion:** any two nodes apply conflicting committed values at the same log position, or a minority partition commits without quorum.

**Observed result:** **NOT YET OBSERVED by learner.**

## Experiment 2 — Minority partition cannot commit

Predict what happens when the current leader is isolated from the other two nodes. Then use the existing partition test or a learner-written scenario to measure:

- minority append attempts;
- minority commit index;
- majority election term;
- majority successful commits;
- state after healing.

Explain the distinction between **accepting a local write into volatile/uncommitted state** and **committing a replicated write**. A local append is not proof of durable consensus.

**Observed result:** **NOT YET OBSERVED by learner.**

## Experiment 3 — Heal and reconcile divergent uncommitted state

Create a bounded history in which the isolated former leader has an uncommitted suffix. Heal the partition and trace every state transition required to converge. Record term changes, role changes, log lengths and commit indexes before/after healing.

The learner must explain why discarding an uncommitted suffix is permitted while rewriting an already committed prefix would violate the safety model.

**Observed result:** **NOT YET OBSERVED by learner.**

## Production transfer

The simulator deliberately omits real sockets, durable storage, fsync semantics, membership changes, snapshots, clock drift, process crashes, Byzantine behavior and real cryptographic key management. After the bounded experiments, list which conclusions transfer to a real consensus implementation and which remain properties only of this model.
