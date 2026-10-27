# Solution — Cycle witness

An edge to a gray ancestor closes the parent-chain route. Black vertices are finished, so an edge to one can be shared downstream structure without a cycle. Explicit iterator frames preserve entry/finish events. O(V+E) time/O(V) stack/color/parents. The diamond 0→1→3 and 0→2→3 exposes the incorrect rule that every already-seen destination is a cycle.

The complete executable mechanism is [`directed_cycle`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
