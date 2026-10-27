# Twenty graph problems — released bounded contracts

These original problems exercise different objectives and invariants. Shared mechanisms and full worked traces are in [LESSON](LESSON.md); solutions are separate. No other topic's twenty-problem quota is claimed by this graph release. Run the complete independent oracle suite with `python3 -m unittest discover -s algorithmic-problem-solving/topics/graphs/code -v`.

| No. | Problem / API |
| --- | --- |
| 01 | [Reachability](problems/01-reachability/prompt.md) / `reachable` |
| 02 | [Shortest hop route](problems/02-shortest-hop-route/prompt.md) / `shortest_path` |
| 03 | [Nearest depot](problems/03-nearest-depot/prompt.md) / `multi_source_distances` |
| 04 | [Failure islands](problems/04-failure-islands/prompt.md) / `components` |
| 05 | [Two group compatibility](problems/05-two-group-compatibility/prompt.md) / `bipartition` |
| 06 | [Build order](problems/06-build-order/prompt.md) / `topological_order` |
| 07 | [Cycle witness](problems/07-cycle-witness/prompt.md) / `directed_cycle` |
| 08 | [Mutual reachability](problems/08-mutual-reachability/prompt.md) / `strongly_connected` |
| 09 | [Nonnegative route cost](problems/09-nonnegative-route-cost/prompt.md) / `dijkstra` |
| 10 | [Negative cost routes](problems/10-negative-cost-routes/prompt.md) / `bellman_ford` |
| 11 | [Free or unit transitions](problems/11-free-or-unit-transitions/prompt.md) / `zero_one_distances` |
| 12 | [Count workflow routes](problems/12-count-workflow-routes/prompt.md) / `dag_path_count` |
| 13 | [Acyclic negative costs](problems/13-acyclic-negative-costs/prompt.md) / `dag_shortest_paths` |
| 14 | [Unlimited worker critical path](problems/14-unlimited-worker-critical-path/prompt.md) / `critical_path` |
| 15 | [Single link failures](problems/15-single-link-failures/prompt.md) / `bridges` |
| 16 | [Single node failures](problems/16-single-node-failures/prompt.md) / `articulation_points` |
| 17 | [Minimum installation forest](problems/17-minimum-installation-forest/prompt.md) / `minimum_spanning_forest` |
| 18 | [Capacity throughput](problems/18-capacity-throughput/prompt.md) / `maximum_flow` |
| 19 | [Maximum compatible assignment](problems/19-maximum-compatible-assignment/prompt.md) / `bipartite_matching` |
| 20 | [All pairs reachability](problems/20-all-pairs-reachability/prompt.md) / `transitive_closure` |
