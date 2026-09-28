# Prerequisite Bridge: Distributed Quorum Consensus

Learner NOT STARTED. Before engaging with this laboratory, ensure the following concepts are understood:

## 1. Network Asynchrony and Message Delivery
- Packets across networks experience variable delay, loss, duplication, and reordering.
- Reliable delivery over an unreliable network requires acknowledgments, timeouts, and idempotent retry logic.

## 2. Quorum Systems
- In a cluster of $N$ nodes, any majority quorum $Q = \lfloor N/2 \rfloor + 1$ satisfies the intersection property: any two majorities must overlap by at least one common node:
  $$|Q_1 \cap Q_2| \ge 1$$
- This intersection ensures that at least one node in any newly elected quorum possesses the most recently committed log entries.

## 3. Split-Brain Problem
- If a network partition divides a cluster into two disjoint subgraphs $G_1$ and $G_2$, both subgraphs could independently elect leaders and commit conflicting writes if a majority quorum were not enforced.
- Enforcing majority quorum guarantees that at most one partition (where $|G_k| \ge Q$) can commit writes.

## 4. State Machine Replication (SMR)
- If multiple deterministic state machines start in the same initial state and apply the exact same sequence of state transitions, they will end in the exact same final state.
