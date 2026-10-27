# Solution — Negative cost routes

Without reachable negative cycles a shortest walk can discard nonnegative cycles, so a simple optimum has at most V−1 edges. Copies make each relaxation pass precisely the k-edge recurrence. A further improvement witnesses unbounded cost; traverse outward to mark all affected vertices. O(V(V+E)) time including row copies, O(V+E) normalized input plus O(V) distances. A disconnected negative cycle must not contaminate the source's reachable region.

The complete executable mechanism is [`bellman_ford`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
