# Design: Quorum Consensus Engine

## Objective
Provide an educational, fully deterministic consensus engine capable of demonstrating consensus guarantees, leader election, log replication, partition resilience, and cryptographic peer authentication under controllable network fault injection.

## State Transitions
Each node transitions between three roles:
- `FOLLOWER`: Passively receives heartbeats and appends entries from the leader; responds to candidate vote requests.
- `CANDIDATE`: Increments term, votes for self, and requests votes from peers after heartbeat timeout.
- `LEADER`: Establishes authority via heartbeats; appends incoming client writes to its log; commits entries once replicated across a majority quorum.

## Idempotent Client Interface
- Every client write carries `(client_id, request_id)`.
- The state machine maintains a deduplication table `client_responses[(client_id, request_id)]`.
- Replayed writes return the cached result immediately with status `COMMITTED_IDEMPOTENT`, avoiding duplicate state mutation.
