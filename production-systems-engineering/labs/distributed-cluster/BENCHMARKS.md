# Benchmarks: Distributed Consensus Performance

## Methodology
`benchmark.py` runs three distinct scenarios under controlled seeds:
1. **Baseline:** 0% packet loss, 1 tick network latency. Measures commit rate and messages per write.
2. **Lossy Network:** 10% packet drop rate. Demonstrates how message loss increases delivery latency and retry rounds.
3. **Partition Injected:** Node 1 isolated in minority $\{N_1\}$ while $\{N_2, N_3\}$ form a majority. Measures blocked writes in the minority vs. committed writes in the majority.

## Summary of Measured Results
From `research/distributed-cluster-benchmark.json`:
- **Baseline:** 100/100 writes committed in 300 simulated ticks (600 messages sent, 600 delivered, 0 dropped).
- **10% Loss:** 100/100 writes committed with 85 dropped packets absorbed and recovered by retry rounds.
- **Partition:** 20/20 writes committed before partition; in the minority partition, 20/20 write attempts were blocked from committing; in the majority partition, 20/20 writes were successfully committed by the newly elected leader.
