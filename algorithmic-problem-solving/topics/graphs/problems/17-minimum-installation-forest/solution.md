# Solution — Minimum installation forest

The cheapest edge crossing a component cut can replace a crossing edge in a spanning optimum without increasing cost. Accepting it and unioning components preserves a partial optimum; skipping same-component edges avoids cycles. O(Elog E) sorting plus union/find costs; O(V+E) storage. A shortest-path tree minimizes a different objective. Negative weights are valid because a forest cannot repeatedly exploit a cycle.

The complete executable mechanism is [`minimum_spanning_forest`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
