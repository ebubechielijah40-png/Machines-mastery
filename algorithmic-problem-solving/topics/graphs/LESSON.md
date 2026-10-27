# Graphs: representations, invariants, paths and obstructions

This original unit teaches twenty bounded graph contracts. It is a developed
part of an incomplete algorithms curriculum, not certification of all graph
algorithms. Read [the proof/discrete bridge](../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md)
first, then attempt [PROBLEMS](PROBLEMS.md) before [SOLUTIONS](SOLUTIONS.md).
[Sources](SOURCES.md) distinguish inspected teaching sources from local derivations.

## 1. Model an actual question before choosing an algorithm

A directed edge `u→v` can mean a packet may move from u to v, or task v cannot
start before u finishes. Those meanings lead to different questions: the first
asks about a route; the second about an ordering. A graph is a set of vertices
and connections, not an answer to either question. Here vertices are integer IDs
0 through n−1. An adjacency list `g[u]` lists outgoing neighbors. In an undirected
simple graph each edge appears in both endpoint lists, without loops or duplicate
entries. Weighted adjacency stores `(destination, integer cost)`.

A path follows edge direction. A simple path repeats no vertex. A walk may repeat
vertices. This distinction matters for negative cycles: a simple route has finite
length, while repeatedly traversing a negative-cost cycle can lower walk cost
without bound. `None` denotes unreachable in unweighted distance results; weighted
results use `+infinity` for unreachable and Bellman–Ford uses `-infinity` for
unbounded-below walks. A zero-cost path is not an unreachable path.

Storage is O(V+E) adjacency entries, versus O(V²) for a full matrix. Looking at all
outgoing neighbors costs the row length, not always O(V). A sparse chain with n
vertices has n−1 edges; a complete directed graph has n(n−1). "Linear in input"
therefore permits quadratic growth with vertex count for a dense input. Count
what the input actually contains before interpreting a benchmark.

The reference validates IDs and duplicate entries, and copies inputs to immutable
rows before work. Validation costs O(V+E) expected dictionary/set operations;
undirected symmetry is checked using sets. Returned lists/sets are newly owned.
No thread mutates another caller's graph here. Concurrent graph updates would
require snapshots/versioning or synchronization outside these algorithms.

## 2. Reachability and shortest unweighted paths

Maintain a frontier of discovered vertices and a visited set. Start with s.
Whenever removing u, inspect each outgoing v. If v is new, mark it *before*
adding it to the frontier. Marking on insertion prevents two parents from adding
v repeatedly. A stack follows one branch; a queue expands layers. Both discover
only reachable vertices because each new discovery extends an actual existing
path. Conversely, if a vertex remains undiscovered, take a shortest route to it;
the first undiscovered vertex on that route follows a discovered predecessor,
whose outgoing edge would have discovered it. Contradiction.

For minimum number of edges, use a FIFO queue. Suppose distances below k have
been processed and queue entries are at distance k or k+1. Every new neighbor
of distance-k u gets k+1. A shorter route would have a predecessor at distance
below k, which would have discovered it earlier. This inductive argument is why
first discovery fixes BFS distance; a stack has no equivalent layer invariant.

Worked graph: `0:[1,2], 1:[3], 2:[3,4], 3:[], 4:[]`. Initially queue `[0]`,
distance `[0,None,None,None,None]`. Removing 0 discovers 1 and 2 at distance1.
Removing 1 discovers 3 at distance2. Removing 2 does not rediscover3; it discovers
4 at distance2. Parents `[None,0,0,1,2]` reconstruct route0→1→3 by following
parents backward from3. A distance array alone does not record that route.

The source-to-itself path is `[s]` with zero edges. An unreachable target returns
None. A multi-source search initializes *all* source distances to zero: the same
proof establishes the minimum distance from any source. Empty sources reach
nothing. Nearest emergency depots and simultaneous wave propagation use this
contract; it is not equivalent to assigning all sources as consecutive visits.

With an adjacency list, each discovered vertex is removed once and each outgoing
edge is inspected once. Time O(V+E), auxiliary arrays/frontier O(V), plus the
input copy. Hash-table costs and arbitrary-precision arithmetic qualify this RAM
model; no exact CPU latency follows from it.

## 3. Components, parity, cycles and dependency order

Undirected connected components partition vertices by mutual reachability. Start
a search at every still-unvisited vertex and collect each reached set. In a
directed graph, one reachability set is not necessarily a component: 0→1 does
not imply 1 can return to0. Never silently discard direction.

Bipartition assigns each endpoint of an edge opposite colors. Set a root color0;
a neighbor must be1, its neighbor0. The color encodes path-length parity. If an
edge joins equal colors, the two discovered routes plus that edge contain an odd
cycle, so no two-color assignment exists. A triangle fails; a four-cycle succeeds.
An isolated vertex can take either color. All components must be checked.

For task dependencies, define indegree as the number of not-yet-emitted
predecessors. Emit any zero-indegree vertex, then remove its outgoing obligations.
Invariant: every emitted task has no remaining unmet predecessor. If vertices
remain but no zero-indegree choice exists, repeatedly follow a remaining
predecessor. Finite vertices force a repetition, hence a cycle. Conversely,
a cycle can never emit its first vertex. This proves Kahn's topological test.
Multiple valid orders may exist; numeric lexicographic minimization is not
promised by a FIFO queue.

Worked dependencies0→2,1→2,2→3. Indegrees `[0,0,2,1]`; emit0 gives2 an indegree1,
not0. Emit1 then2 becomes ready. Any answer placing2 before1 violates the edge
invariant even if it contains every vertex exactly once.

To return a cycle witness, DFS tracks white/unvisited, gray/current ancestors,
and black/finished vertices. An edge to a gray vertex closes a route through
current parent links; an edge to a black vertex need not be a cycle. In the
diamond0→1→3 and0→2→3, a second visit toward finished3 must not report a cycle.
Our implementation uses explicit iterator frames so DFS finishing events occur
at the correct time, without depending on Python recursion for this contract.

Strong components use mutual reachability. Collapse each strong component into
one vertex: the resulting graph is acyclic, since a cycle of components would
make them mutually reachable and therefore one component. DFS finish order
selects a source component of this collapsed graph before its successors when
processed in decreasing finish time. Searching the reversed graph from that
component cannot escape into a predecessor already excluded by the order;
it reaches exactly its members. Repeat on unassigned vertices. This derives
the two-pass SCC method used here. Test partitions by mutual reachability,
not by memorizing an implementation's order of sets.

## 4. Relaxation: weighted shortest paths

Let d[v] be a best-known cost. An edge u→v of weight w offers a candidate
`d[u]+w`; taking the smaller value is relaxation. Every finite candidate must
come from a real route. The question is when that candidate becomes final.

With nonnegative weights, remove the smallest tentative distance from a heap.
If it were not optimal, choose the first unsettled vertex on a cheaper route.
Its predecessor was settled, and relaxing their edge would have given a
candidate no larger than that cheaper route. Nonnegative remaining costs are
what make that comparison valid. It contradicts removal of a larger minimum.
This is the Dijkstra proof. Negative edges invalidate the proof, so the API
rejects them *before* searching, even if a particular input happens to work.

Worked weighted graph0→1 cost7,0→2 cost2,2→1 cost1. Removing0 queues `(7,1)` and
`(2,2)`. Removing2 improves1 to3 and queues `(3,1)`. After settling1 at3, stale
heap entry `(7,1)` must be ignored. Marking1 final when first enqueued would
incorrectly return7. Binary heap with lazy entries costs O((V+E)log(V+E)) in
this implementation, with O(V+E) possible heap entries. It is not a decrease-key
heap promising only V queue entries.

For edge weights0 or1, a deque is enough: a zero-cost relaxation goes to the
front, a unit-cost relaxation to the back. Nonstale removals proceed in distance
order; stale `(old_distance,vertex)` entries are discarded. Edge weights2 or-1
are rejected. A normal BFS queue would minimize edge count, not total cost.

For arbitrary integer weights, define d_k[v] as minimum walk cost using at most
k edges. Either that route already used at most k−1 edges, or its last edge u→v
extends such a route: `d_k[v]=min(d_(k−1)[v], min_u(d_(k−1)[u]+w_uv))`. The
reference copies the previous row so every pass has this exact interpretation.
Without reachable negative cycles, remove nonnegative cycles from an optimal
walk; a simple optimum has at most V−1 edges. After V−1 passes, a further
improvement witnesses a reachable negative cycle. Every vertex reachable from
such a witness has cost unbounded below, hence -infinity. A disconnected negative
cycle does not poison distances from a source that cannot reach it.

Example0→1 cost1,1→2 cost-3,2→1 cost1 gives cycle cost-2. Repeating it arbitrarily
lowers costs to1 and2, but not to an isolated3. Output `[0,-inf,-inf,+inf]` makes
that distinction explicit. Bellman–Ford here costs O(V(V+E)) including row copies;
with reachable-vertex preprocessing the usual O(VE) presentation follows.

## 5. A DAG turns global questions into local recurrences

A topological order ensures all predecessors have finished before a vertex's
value is used. For source-to-target path count, initialize count[source]=1 for
the empty path. Each edge adds count[u] to count[v]. Every path to v has one
last edge, so those predecessor classes are disjoint and exhaustive. A cycle
would permit repeated walks and breaks this finite recurrence; reject it.

For a diamond0→1→3 and0→2→3, counts become `[1,1,1,2]`. Reachability is not count:
a visited boolean loses the fact that3 has two route prefixes. Counts may grow
exponentially in V, so Python big-integer bit cost is outside constant-word
operation counts.

DAG shortest paths replace addition-of-counts by minimum-of-costs, allowing
negative weights because there are no cycles to repeat. Critical-path scheduling
replaces minimum by maximum: if each vertex u takes duration t[u], its earliest
finish is `t[u]+max(finish[p] for predecessors p)`, with an empty maximum zero.
For durations `[2,3,7,1]` on the diamond, finishes are `[2,5,9,10]`. This assumes
unlimited workers, no setup/communication delay and nonpreemptive dependency
completion. It is a lower bound for a resource-limited machine scheduler, not
an actual resource-constrained schedule.

## 6. Connections whose removal disconnects a system

In undirected DFS, discovery[u] records when u was first visited. low[u] is the
earliest discovery index reachable from u's DFS subtree by descending tree edges
and then using at most one nonparent back edge. Child low values propagate upward;
a back edge supplies its ancestor's discovery index.

A tree edge(u,v) is a bridge exactly when `low[v]>discovery[u]`: v's subtree has
no alternate route to u or any earlier ancestor. If it did, deleting the tree
edge would leave that alternate route. Conversely, any alternate route crossing
out of the subtree would supply the missing back-edge escape. For a nonroot u,
`low[v]>=discovery[u]` means removing u isolates that child's subtree, so u is
an articulation vertex. A DFS root is special: it is a cut vertex iff it has at
least two DFS children. Merely using the nonroot test incorrectly marks a root
with one child. A triangle has no bridges/cut vertices; attaching a leaf at
vertex2 creates bridge(2,3) and cut vertex2.

This reference is for simple graphs. Parallel undirected edges require tracking
edge IDs rather than skipping every edge toward the parent. Recursion is bounded
to500 vertices; larger inputs must use an iterative frame implementation. The
independent tests delete edges/vertices and recompute connectivity by partition
merging; they do not repeat the low-link recurrence as an "oracle."

## 7. A cheapest connecting forest

Sort undirected weighted edges. Add an edge only when its endpoints are in
different current components; union their components. It cannot create a cycle.
Why is its greedy cost safe? Consider the cut separating one component from the
others. The cheapest eligible crossing edge can replace a crossing edge in any
spanning optimum; replacement maintains connectivity and cannot increase cost.
Repeat the exchange argument after each accepted edge. This establishes a
minimum spanning tree in each connected component, hence a minimum forest.
A disconnected graph is not an error under this declared contract.

Negative weights are allowed; they do not create the unbounded-walk problem
because a forest cannot repeat cycles. O(Elog E) sorting dominates union/find
with path compression/rank for this small reference; it retains an edge list and
component arrays. A minimum spanning tree is not a shortest-path tree: one
minimizes total installed connection cost, the other source-to-vertex route cost.

## 8. Flow and matching: capacity and reassignment

A flow obeys capacity limits and conservation at intermediate vertices. A residual
edge is remaining opportunity to increase a forward flow or undo a previous one.
After sending f units u→v, reduce residual(u,v) by f and increase residual(v,u)
by f. Omitting that reverse capacity can trap a poor early choice permanently.
BFS chooses an augmenting source-to-sink route; its bottleneck is the smallest
residual capacity along it. Integer capacities keep each augmentation integral.

When no residual route remains, let S be vertices reachable from source in the
residual graph. Sink is outside S. Every original edge from S to its complement
is saturated, while opposite-direction flow must net correctly across the cut.
Conservation says total source flow equals net crossing flow, equal to this cut's
capacity. Any possible flow is at most any cut capacity. We have constructed
equal lower/upper certificates: the current flow is maximal. The tests enumerate
all source/sink cuts on four vertices independently. The dense matrix BFS scans
V entries per removed vertex; do not quote sparse complexity for this code.

Bipartite matching is unit-capacity assignment with separate left/right entities.
If one left vertex wants an occupied right vertex, recursively try reassigning its
current owner. A per-search visited-right set prevents loops. Each successful
augmenting path increases matching size by one. If a larger matching existed,
the symmetric difference with the present matching would contain an alternating
path with one more unmatched-to-matched edge, which our augmenting search would
find. This explains maximum cardinality, not maximum preference score. Bounded
recursion and small controlled inputs are explicit; hostile graph sizes need
request quotas before allocation.

## 9. Closure and limits of the model

Transitive closure asks every pair's reachability. Start with self-reachability
and explicit edges. After phase k, permit intermediate vertices only among0..k.
A route either avoids k, or splits into i→k and k→j. Thus the update
`reach[i][j] |= reach[i][k] and reach[k][j]` follows by partitioning routes.
Time O(V³), storage O(V²). Repeating BFS from each source is a useful alternative
with O(V(V+E)) time, particularly for sparse graphs.

All results concern the supplied graph and chosen objective. A road cost may
change after measurement, a dependency may be missing, capacities may be stale,
and a reachable host may not be authorized. Correct graph arithmetic cannot
repair wrong measurement, semantics, authorization or a violated resource model.
Use stable input snapshots, provenance, integer/overflow policies, cancellation
or timeout budgets, and actual workload measurements in production.

Run [the tests](code/test_graph_algorithms.py) and [experiment](EXPERIMENT.md).
Then rebuild BFS, DAG recurrence and one obstruction certificate from memory.
A transfer pass requires choosing the right model on a new situation and
explaining why the wrong plausible algorithm fails; memorizing twenty names
is insufficient.
