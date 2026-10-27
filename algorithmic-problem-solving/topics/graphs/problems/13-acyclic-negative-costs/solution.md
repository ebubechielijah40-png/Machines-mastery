# Solution — Acyclic negative costs

Each route to a vertex ends at an earlier predecessor; all predecessor optima are known before relaxation outward. Thus the minimum-over-last-edges recurrence is correct by induction on topological position. O(V+E) time and O(V) distance/order state beyond input. Dijkstra's nonnegative cut argument is unnecessary here, but using numeric ID order instead of a valid topology can read unfinished predecessor values.

The complete executable mechanism is [`dag_shortest_paths`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
