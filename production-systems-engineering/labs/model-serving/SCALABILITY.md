# Scalability: Batching and Throughput Limits

## Tradeoffs in Dynamic Batching

### 1. Throughput vs. Latency (Little's Law)
- Per-item inference incurs per-call dispatch and interpreter overhead.
- Grouping inputs into micro-batches amortizes fixed loop overhead, increasing maximum system throughput (requests per second).
- However, waiting to assemble a batch introduces artificial queue wait time, increasing individual request latency (p99).

### 2. Memory Footprint
- Model weights: $O(D)$ where $D$ is feature dimension (negligible for linear models).
- Drift monitor buffer: $O(W \times D)$ where $W$ is the sliding window size (bounded ring buffer).
- Predictable, constant memory allocation prevents out-of-memory crashes under heavy sustained request volume.
