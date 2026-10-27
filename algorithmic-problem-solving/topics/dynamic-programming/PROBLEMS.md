# Twenty distinct dynamic-programming contracts

These are complete bounded statements, not problem seeds. Attempt prompts before
opening hints or reference implementations. The release covers optimization,
reachability, counting, sequence/interval/layer/subset states and minimax inversion.
It does not complete every DP technique or the full algorithms curriculum.

| Contract | Objective and output |
| --- | --- |
| [Minimum standard packages](problems/01-package-count/prompt.md) | `min_coins`: A warehouse has unlimited packages of each distinct positive integer size. |
| [Count unordered replenishment bundles](problems/02-unordered-bundles/prompt.md) | `coin_combinations`: For distinct positive denominations and an exact nonnegative target, count multiplicity vectors of unlimited denominations. |
| [Select one copy of each payload](problems/03-payload-selection/prompt.md) | `knapsack`: Given parallel positive integer weights and integer values, choose a subset of item indices with total weight at most capacity and maximum value. |
| [Reconcile an exact ledger amount](problems/04-exact-subset/prompt.md) | `subset_sum`: Choose each nonnegative integer record amount at most once to total target exactly. |
| [Choose nonadjacent maintenance days](problems/05-maintenance-days/prompt.md) | `nonadjacent`: Each day has an integer benefit. |
| [Recover a common event order](problems/06-common-event-order/prompt.md) | `lcs`: Given two Unicode strings, return a longest common subsequence. |
| [Minimum unit-cost text corrections](problems/07-correction-cost/prompt.md) | `edit_distance`: Return the minimum number of single-code-point insertions, deletions or replacements needed to transform string a into b. |
| [Retain a strictly increasing sample subsequence](problems/08-increasing-samples/prompt.md) | `lis`: Given integer samples in arrival order, return indices of a longest strictly increasing subsequence. |
| [Count monotone routes around blocked cells](problems/09-obstacle-routes/prompt.md) | `grid_paths`: Given a rectangular Boolean blocked grid, count paths from top-left to bottom-right moving only right or down. |
| [Choose a minimum-cost monotone inspection route](problems/10-costed-grid/prompt.md) | `grid_cost`: For a rectangular integer cost grid, move right/down from top-left to bottom-right, paying every visited cell including both endpoints. |
| [Choose compatible weighted reservations](problems/11-reservation-value/prompt.md) | `weighted_intervals`: Each job is(start,end,value), with integer start<end and half-open occupancy[start,end). |
| [Plan a dense matrix multiplication chain](problems/12-matrix-plan/prompt.md) | `matrix_chain`: Given positive dimensions d of length n+1 for nonempty chain A0…A(n−1), return(minimum scalar multiplications,parenthesization). |
| [Lay out a bounded technical label](problems/13-line-break-cost/prompt.md) | `justify`: Given positive word lengths and a nonnegative line width, break words into consecutive lines with one space between words. |
| [Cut a reversible-symbol log into palindromes](problems/14-palindrome-segments/prompt.md) | `palindrome_cuts`: Partition a Unicode string into nonempty palindromic substrings with minimum cuts. |
| [Find a cheapest route with a hop budget](problems/15-hop-bounded-route/prompt.md) | `bounded_route`: In a directed graph with n≥1, integer weighted edges, valid source/target and nonnegative hop budget, return minimum(cost,vertex_walk) using at most that many edges, or None. |
| [Minimum-cost one-to-one assignment](problems/16-one-to-one-workers/prompt.md) | `assignment`: A square integer cost matrix gives the cost of assigning worker i to job j. |
| [Count legal binary control records](problems/17-legal-bit-records/prompt.md) | `binary_no_adjacent`: Count binary strings of length n≥0 with no adjacent1 bits. |
| [Count ordered pattern embeddings](problems/18-pattern-embeddings/prompt.md) | `subsequence_count`: Count choices of distinct increasing source indices whose characters spell pattern. |
| [Count true Boolean parenthesizations](problems/19-boolean-plans/prompt.md) | `boolean_parenthesizations`: Given a nonempty list of actual Boolean literals and exactly one fewer operators from &,|,^, count complete binary parenthesizations evaluating to True. |
| [Minimax tests for a monotone breakage threshold](problems/20-breakage-threshold/prompt.md) | `egg_drop`: There are floors1…F and a fixed unknown threshold from0…F. |
