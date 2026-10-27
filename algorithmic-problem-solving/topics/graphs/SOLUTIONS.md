# Graph solutions — consult after an attempt

The [mechanism lesson](LESSON.md) proves shared invariants. Each entry below fixes its own contract, assumptions, counterexample and costs. Reference code is original in `code/graph_algorithms.py`, with independent exhaustive oracles in the adjacent test module.

## 01. Reachability

Every new vertex extends a real route. If a reachable vertex were missed, the first missed vertex on a route would follow a processed predecessor, a contradiction. O(V+E) time and O(V) visited/frontier beyond the normalized input. A disconnected vertex is absent, while the source is always present. A stack suffices; shortest route length is a different contract.

## 02. Shortest hop route

FIFO removal processes nondecreasing edge distance. If a first-discovered route were too long, its shorter predecessor would have been removed earlier and discovered it. Follow parents backward to construct the path. O(V+E) search and O(V) arrays; path construction O(path length). DFS can choose a longer route. Equal-length alternatives are allowed; tests must accept valid optima rather than force an unspecified tie.

## 03. Nearest depot

A conceptual zero-cost super-source would connect every depot. Initializing the actual queue with all depots establishes the same distance-zero frontier without adding a vertex. The BFS layer proof then applies. O(V+E+S) time including source enumeration, O(V) auxiliary state. Running one source after another while keeping old nonzero labels can preserve the wrong distances. An empty source set yields all None, not a fabricated origin.

## 04. Failure islands

Mutual reachability is an equivalence relation in an undirected graph. The traversal from a new root finds precisely its equivalence class; no edge connects two returned classes. O(V+E) total scan, because assigned vertices are never searched as new roots. O(V) visited/output beyond input. Directed reachability does not have the symmetry needed for this proof; asymmetric adjacency is rejected rather than silently reinterpreted.

## 05. Two group compatibility

Along a rooted traversal, color encodes path parity. An equal-color edge would close an odd cycle, which cannot alternate two colors all the way around. Conversely, if no conflict occurs every edge satisfies the required relation. Check every component. O(V+E) time/O(V) state. A triangle is a counterexample to assuming every undirected graph is bipartite; an isolated vertex is not a failure.

## 06. Build order

A zero-indegree choice has no unmet predecessor. Removing it preserves that invariant. If tasks remain without such a choice, repeatedly following a predecessor must eventually repeat a vertex, establishing a cycle. O(V+E) time/O(V) state. Numeric sorting of task IDs is not a valid general solution; IDs need not encode dependencies. Returning only an acyclic prefix must not be mislabeled a complete order.

## 07. Cycle witness

An edge to a gray ancestor closes the parent-chain route. Black vertices are finished, so an edge to one can be shared downstream structure without a cycle. Explicit iterator frames preserve entry/finish events. O(V+E) time/O(V) stack/color/parents. The diamond 0→1→3 and 0→2→3 exposes the incorrect rule that every already-seen destination is a cycle.

## 08. Mutual reachability

Collapse each true strong component; the collapsed graph has no cycle, since a component cycle would imply mutual reachability. DFS finish order places a source component ahead of successors. Reverse-edge searches in that order isolate one component at a time. O(V+E) time/storage. A one-direction edge does not merge its endpoints. Compare returned partitions as sets of sets, not an arbitrary traversal order.

## 09. Nonnegative route cost

A cheaper unsettled route would cross from a settled predecessor to a first unsettled vertex, giving that vertex a tentative value no greater than the cheaper route. Nonnegative remaining edges yield the contradiction with the extracted minimum. Lazy stale entries are ignored. O((V+E)log(V+E)) time and O(V+E) state for this heap version. Negative edges invalidate the proof and are explicitly rejected.

## 10. Negative cost routes

Without reachable negative cycles a shortest walk can discard nonnegative cycles, so a simple optimum has at most V−1 edges. Copies make each relaxation pass precisely the k-edge recurrence. A further improvement witnesses unbounded cost; traverse outward to mark all affected vertices. O(V(V+E)) time including row copies, O(V+E) normalized input plus O(V) distances. A disconnected negative cycle must not contaminate the source's reachable region.

## 11. Free or unit transitions

The deque preserves distance priority: a zero edge stays at the current distance and a unit edge advances one layer. Stale labels are skipped, so a poor first discovery can improve. O(V+E) graph work in the standard deque argument and O(V+E) normalized input/queued labels. Ordinary BFS would prefer fewer edges and return cost1 to vertex1 in the worked graph, missing the free two-edge route.

## 12. Count workflow routes

Partition paths into v by their last edge u→v. These classes are disjoint, so count[v] is the sum of predecessor counts. Initialize one empty prefix at source and process a topological order. O(V+E) arithmetic operations/O(V) state; bit complexity grows with the count. A visited boolean loses multiple prefixes, while a cycle makes unbounded-walk counts a different problem.

## 13. Acyclic negative costs

Each route to a vertex ends at an earlier predecessor; all predecessor optima are known before relaxation outward. Thus the minimum-over-last-edges recurrence is correct by induction on topological position. O(V+E) time and O(V) distance/order state beyond input. Dijkstra's nonnegative cut argument is unnecessary here, but using numeric ID order instead of a valid topology can read unfinished predecessor values.

## 14. Unlimited worker critical path

For every dependency u→v update earliest_start[v]=max(earliest_start[v],finish[u]); then finish[v]=start[v]+duration[v]. Induction on topology proves feasibility and optimality under unlimited workers. O(V+E) time/O(V) state. Summing all durations ignores parallelism; taking the shortest predecessor ignores an unmet slow one. Resource-limited scheduling can finish later and is not solved by this function.

## 15. Single link failures

low[child] is the earliest ancestor reachable from its subtree through tree descent and one nonparent back edge. An escape above/equal parent means an alternate route; low[child]>discovery[parent] means no escape, hence the tree edge is a bridge. O(V+E) time/O(V) DFS state after validation; this recursive reference caps V at500. Parallel edges need edge IDs and are rejected; skipping all parent edges would be wrong for a multigraph.

## 16. Single node failures

For nonroot u, a child v with low[v]>=discovery[u] cannot escape without u, so removing u separates that subtree. A root has no ancestor side and is a cut vertex only with at least two DFS children. O(V+E) time/O(V) state, V≤500 for this recursive reference. Applying the nonroot test blindly wrongly marks a root with one child; an isolated vertex is not an articulation point.

## 17. Minimum installation forest

The cheapest edge crossing a component cut can replace a crossing edge in a spanning optimum without increasing cost. Accepting it and unioning components preserves a partial optimum; skipping same-component edges avoids cycles. O(Elog E) sorting plus union/find costs; O(V+E) storage. A shortest-path tree minimizes a different objective. Negative weights are valid because a forest cannot repeatedly exploit a cycle.

## 18. Capacity throughput

Augment by the smallest residual capacity on a BFS path. When no path remains, let S be residual-source-reachable vertices. Every S→outside capacity is saturated and conservation makes net crossing flow equal the flow value. Any flow is bounded by that cut, so equality certifies optimality. Dense BFS scans O(V²); an O(V³E) upper bound accounts for this implementation, with O(V²) residual storage. A forward-only residual model can get stuck below optimum.

## 19. Maximum compatible assignment

A successful augmenting path adds one assignment while preserving uniqueness. If a larger matching existed, its symmetric difference with the current one would contain an augmenting alternating path. Searching every new left vertex therefore reaches maximum cardinality. O(L*E) reference time, O(L+R) search/owner state; L≤500 because recursion is bounded. Greedily assigning0→0 without allowing reassignment strands left1 despite a size-two solution.

## 20. All pairs reachability

A route using only intermediate vertices through k either avoids k or splits into an i→k route and k→j route using earlier intermediates. This derives the boolean recurrence by induction. O(V³) time/O(V²) storage. Omitting the initial identity incorrectly loses empty paths. Repeated BFS is an alternative O(V(V+E)) approach and can be preferable on sparse adjacency lists.
