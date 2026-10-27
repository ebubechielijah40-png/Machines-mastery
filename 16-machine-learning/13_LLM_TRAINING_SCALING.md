# 13 — LLM training and scaling

Large language-model training is a systems problem wrapped around a learning objective.

## Data pipeline

```text
raw sources → filtering → deduplication → normalization → tokenization
→ sharding → batching → training → checkpoints → evaluation
```

Every arrow can change the learned distribution. Dataset quality, duplication, contamination, domain mix, and provenance matter as much as raw token count.

## Compute accounting

Training cost scales with parameter count, token count, architecture, precision, activation storage, optimizer state, and hardware utilization. A nominal FLOP estimate is not the same as wall-clock cost: communication, memory bandwidth, kernel efficiency, failures, and checkpoint I/O matter.

## Distributed training concepts

- **data parallelism** replicates the model and splits batches;
- **tensor/model parallelism** splits computation within layers;
- **pipeline parallelism** splits layers/stages;
- **sharded optimizer/state** reduces replica memory costs.

These introduce synchronization, communication, load-balancing, and failure-recovery concerns.

## Scaling laws

Empirical scaling laws describe regularities over certain regimes; they are not laws of nature. Use them to reason about tradeoffs among model size, data, and compute, but verify assumptions for the actual architecture/data regime.

## Experiment

Train the same tiny Transformer at several parameter counts and dataset sizes. Keep a fixed compute budget for one experiment. Measure training loss, validation loss, tokens/sec, peak memory, and wall time. Plot what actually scales on your hardware.
