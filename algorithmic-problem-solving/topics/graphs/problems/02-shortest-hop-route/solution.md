# Solution — Shortest hop route

FIFO removal processes nondecreasing edge distance. If a first-discovered route were too long, its shorter predecessor would have been removed earlier and discovered it. Follow parents backward to construct the path. O(V+E) search and O(V) arrays; path construction O(path length). DFS can choose a longer route. Equal-length alternatives are allowed; tests must accept valid optima rather than force an unspecified tie.

The complete executable mechanism is [`shortest_path`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
