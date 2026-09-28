# Observability: Cluster Telemetry and Metrics

## Instrumented Metrics

### Node-Level Metrics
- `writes_total`: Cumulative client write attempts.
- `writes_committed`: Entries reaching majority consensus and applied to the state machine.
- `replays_handled`: Duplicate client requests detected and resolved idempotently.
- `elections_started`: Number of times the node transitioned to `CANDIDATE`.
- `terms_advanced`: Increments of `current_term` triggered by election or peer message.
- `security_violations`: Messages rejected due to token mismatch or replayed nonce.

### Network-Level Metrics
- `sent`: Total messages enqueued.
- `delivered`: Messages successfully received by non-partitioned target nodes.
- `dropped_loss`: Packets discarded by probabilistic packet loss.
- `dropped_partition`: Packets intercepted by active partition barriers.
- `tampered_rejected`: Messages rejected by security checks at destination nodes.
