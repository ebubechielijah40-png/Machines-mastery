# Assumptions: Distributed Cluster

## Fault and Environment Model
1. **Crash-Recovery:** Nodes may crash, become disconnected, or restart. Memory state is held in-process for this simulation; persistence across process restarts is modeled logically.
2. **Non-Byzantine:** Nodes do not intentionally forge malicious messages. Cryptographic HMAC authentication defends against simulated spoofing and tampering.
3. **Partially Synchronous Network:** Messages experience discrete tick latencies ($L \ge 1$). Delivery is not guaranteed when packet loss or partitions are active.
4. **Finite Cluster Size:** Cluster membership is fixed ($N = 3$ in tests/benchmarks); dynamic reconfiguration is excluded from this baseline.
5. **Single In-Memory Process:** The simulation executes deterministically inside a single Python process to eliminate wall-clock race conditions and nondeterministic operating system scheduling.
