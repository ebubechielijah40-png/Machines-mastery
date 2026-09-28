# Real-world complexity and scalability labs

For every core algorithm family, write an executable benchmark that doubles input size and records runtime/memory. Plot or tabulate ratios. Compare empirical behavior to asymptotic predictions without claiming exact agreement.

Required comparisons:
- linear scan vs binary search (including sort/preparation cost);
- list membership vs hash-set membership;
- O(n²) pair scan vs indexed O(n) approach;
- insertion sort vs merge/standard library sort across small/large sizes;
- BFS/DFS memory on wide/deep graphs;
- naive recursion vs memoized DP;
- array sequential access vs randomized access to expose locality;
- heap top-k vs full sorting;
- database indexed vs non-indexed query (use SQLite);
- stream processing with fixed window vs unbounded retained history.

Record machine/environment, data generator, warmup/repetitions, median and tail values where relevant, and sources of measurement noise. Big-O predicts growth under a computational model; benchmarking observes a particular implementation/hardware/runtime.
