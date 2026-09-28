# Generation and validation contract

Each real problem has prompt.md, hints.md, solution.md and tests/. Prompt contains original/attributed statement, constraints, examples, edges and follow-ups without revealing the algorithm. Solution contains brute force, why it works/why it is costly, better and optimal/near-optimal approaches, stepwise derivation, invariant, proof, time/space with cost model, failed approaches and counterexamples, final executable implementation, alternatives for hard cases, tests and CS connections.

Release only after independent test oracles, exhaustive small cases where feasible, varied distributions and manual complexity review. Provide measured naive versus improved growth at increasing n; timings, memory method, repeats and environment must come from actual runs. Big-O is not a clock reading. Constants, caches, runtime overhead and input distribution can dominate small n; a benchmark alone cannot prove an asymptotic bound.

Applications: hashes → cache/index; heaps → scheduler; graphs → routing/dependency; tries → autocomplete; queues → work processing; dynamic programming → constrained optimization; Bloom-filter extensions → storage filtering; sorting → ingestion; binary search → ordered index. The production lab demonstrates a measured index/cache investigation; future topic releases must add their own code and comparisons.
