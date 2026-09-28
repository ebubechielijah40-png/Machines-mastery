# Scalability: Quorum Consensus and Cluster Growth

## Growth Bounds and Network Load

### 1. Cluster Size vs. Fault Tolerance
- A cluster of $N$ nodes tolerates $F$ failures where:
  $$N = 2F + 1$$
- For $N=3$: $F=1$, quorum $Q=2$.
- For $N=5$: $F=2$, quorum $Q=3$.
- For $N=7$: $F=3$, quorum $Q=4$.

### 2. Message Complexity
- Per client write, the leader broadcasts $N-1$ append messages and receives $N-1$ replies, giving $O(N)$ message overhead per transaction.
- Adding nodes increases read capacity and failure tolerance, but increases write replication traffic and election latency.

### 3. Log Compaction and Memory Growth
- Without log compaction, log memory scales linearly with transaction count: $O(T)$.
- In production, log snapshotting truncates entries older than the latest durable checkpoint, bounding memory to active transactions plus state machine size.
