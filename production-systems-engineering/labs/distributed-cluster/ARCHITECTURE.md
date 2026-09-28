# Architecture: Distributed Consensus Simulation

## Component Layout

```text
+--------------------------------------------------------------+
|                    Deterministic Network                     |
|  - Discrete tick clock                                       |
|  - Priority delivery queue                                   |
|  - Fault injectors: drop_rate, partitions                    |
+--------------------------------------------------------------+
       ^                         ^                         ^
       |                         |                         |
+---------------+         +---------------+         +---------------+
|    Node 1     |         |    Node 2     |         |    Node 3     |
| - Raft engine |         | - Raft engine |         | - Raft engine |
| - Log store   |         | - Log store   |         | - Log store   |
| - State mach. |         | - State mach. |         | - State mach. |
| - HMAC auth   |         | - HMAC auth   |         | - HMAC auth   |
+---------------+         +---------------+         +---------------+
```

## Data and Message Flow
1. **Client Submission:** Client submits `client_write(key, val, cid, rid)` to leader.
2. **Local Append:** Leader appends entry to its local log and sets `match_index[leader] = len(log) - 1`.
3. **Replication Broadcast:** Leader sends `APPEND_ENTRIES` RPC to all follower nodes via `DeterministicNetwork`.
4. **Follower Ingestion:** Followers verify term and consistency, append to local logs, and respond with `APPEND_REPLY`.
5. **Quorum Commitment:** When `matches >= (N // 2) + 1`, leader advances `commit_index`, applies entry to `state_machine`, and broadcasts updated commit index.
