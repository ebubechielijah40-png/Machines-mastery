# Library engineering decisions

Version contracts before changing return conventions or mutation policy.
Validate IDs/weights at the boundary; preserve immutable snapshots when callers
could mutate a graph concurrently. Choose representation from actual density,
update frequency and query mix. A cache or precomputed closure trades maintenance
and memory for query cost; changed edges need explicit invalidation.

Measure validation, allocation, traversal, output construction and peak memory
under a declared workload. A faster wrong algorithm is not an optimization.
Recursive DFS can exhaust Python call depth; an iterative stack requires the
same entry/exit state needed by low-link calculations. Do not silently replace
it with a reachability-only stack. Retain independent tiny oracles during changes.
This local library has no public deployment/authentication boundary.
