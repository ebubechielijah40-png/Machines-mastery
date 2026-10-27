# Solution — Reachability

Every new vertex extends a real route. If a reachable vertex were missed, the first missed vertex on a route would follow a processed predecessor, a contradiction. O(V+E) time and O(V) visited/frontier beyond the normalized input. A disconnected vertex is absent, while the source is always present. A stack suffices; shortest route length is a different contract.

The complete executable mechanism is [`reachable`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
