# Solution — Nonnegative route cost

A cheaper unsettled route would cross from a settled predecessor to a first unsettled vertex, giving that vertex a tentative value no greater than the cheaper route. Nonnegative remaining edges yield the contradiction with the extracted minimum. Lazy stale entries are ignored. O((V+E)log(V+E)) time and O(V+E) state for this heap version. Negative edges invalidate the proof and are explicitly rejected.

The complete executable mechanism is [`dijkstra`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
