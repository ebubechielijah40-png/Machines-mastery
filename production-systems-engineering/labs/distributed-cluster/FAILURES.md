# Failures: Fault Injection and Split-Brain Prevention

## Simulated Failure Modes

### 1. Packet Loss and Timeouts
- **Mechanism:** `DeterministicNetwork.drop_rate` randomly discards messages.
- **Consequence:** Heartbeats or replication acknowledgments are lost.
- **Handling:** Periodic leader heartbeats retransmit missing log entries based on `next_index[peer]`.

### 2. Network Partitions and Split-Brain Rejection
- **Mechanism:** `DeterministicNetwork.partition(group_a, group_b)` simulates a bidirectional link severed between subsets.
- **Consequence:** A leader isolated in a minority group cannot gather acknowledgments from $\lfloor N/2 \rfloor + 1$ nodes.
- **Handling:** The minority leader appends locally but never advances `commit_index`, preventing split-brain state pollution.

### 3. Partition Healing and Log Rollback
- **Mechanism:** `DeterministicNetwork.heal_partitions()` restores full connectivity.
- **Consequence:** The former leader receives an `APPEND_ENTRIES` RPC containing a higher term from the newly elected majority leader.
- **Handling:** The former leader steps down to follower, rewinds its log to overwrite uncommitted entries, and syncs committed entries.
