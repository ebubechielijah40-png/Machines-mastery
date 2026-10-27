# Dynamic programming: preserve the information a future decision needs

A brute-force search repeatedly solves the same remaining problem. Dynamic
programming replaces those repeated branches with a state table. The difficult
step is choosing what makes two remaining problems equivalent. Too little state
combines histories with different legal futures; too much state keeps the
exponential search under another name. Read [functions and algebra](../../../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md),
[logic and induction](../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md)
and [Python](../../../02-programming/python-entry/README.md) first.

This unit has [twenty distinct precise contracts](PROBLEMS.md), an original
[executable library](code/dp.py), separate hints/derivations/fixed tests for every
problem, and a [finite-search oracle suite](code/test_dp.py). The problems span
optimization, feasibility, counting, interval, sequence, layered graph, subset
and minimax states. They do not complete every algorithm or every DP technique.

## Derive a state from a failed choice

Suppose a warehouse has unlimited package sizes1,3,4 and needs exactly6 units.
Largest-first picks4+1+1, three packages;3+3 uses two. Greedy choice has no proof
that its locally largest step can be extended to a global optimum.

Define M[a] as the minimum package count for **exactly** amount a, with M[0]=0
and unreachable states represented by None. Any positive solution ends in some
package c≤a; removing it leaves a valid solution to a−c. Conversely adding c to
any such solution builds one for a. Therefore

\[
M[a]=\min_{c\leq a,\ M[a-c]\text{ reachable}}(1+M[a-c]).
\]

Amounts grow from1 to the target, so every dependency has already been solved.
For a=0…6 the values are0,1,2,1,1,2,2. Retain the winning last package to
reconstruct a witness. An empty witness() is valid for target0; None means
impossible. Using0 for both would confuse an optimal empty solution with failure.

Induct on a: all smaller states are optimal by hypothesis. Every feasible final
package is considered; its optimal prefix cannot be worse than any competing
prefix. Taking the minimum thus gives a lower bound attained by a construction.
This is a correctness argument, not just a table trace. For C sizes and target A,
the code evaluates O(CA) candidates and keeps O(A) cells and predecessor entries.
Since binary input encodes A in O(log A) bits, this is pseudopolynomial, not
polynomial in encoded numeric input size.

## Same resources, different question: count combinations

Counting3+1 and1+3 as distinct asks for ordered sequences. The unordered bundle
contract counts one multiplicity vector. Define W after processing a denomination
prefix. Initially W[0]=1: one empty choice. For each c, traverse amounts upward
and add W[a−c] to W[a]. Old entries mean no c; the updated smaller amount means
at least one c with unlimited repetition. Each vector has exactly one number of
c copies, so it is counted once. For denominations1,2 and target3 the combinations
are1+1+1 and1+2: two. Amount-first iteration counts three ordered strings instead.
An iteration order can be part of semantics, not just a performance preference.

For0/1 knapsack, by contrast, each item is usable once. Let K[i,c] be the best
value using the first i items with capacity at most c. Either skip the ith item,
or use its value plus K[i−1,c−weight]. Both branches read the previous item layer.
For one weight2,value3 item and capacity4, the answer is3. A one-dimensional
ascending-capacity rewrite reads its own new value and incorrectly returns6.
Descending capacity preserves the old layer. The reference retains full rows
because reconstructing chosen indices is an explicit output requirement.

## Sequence states: a prefix pair is a coordinate

For edit distance D[i,j], interpret the state as the minimum unit-cost edits from
a[:i] to b[:j]. Bases D[i,0]=i and D[0,j]=j express deleting/inserting every
character. The final operation is delete, insert, or match/replace, giving

\[
D[i,j]=\min(D[i-1,j]+1, D[i,j-1]+1,
D[i-1,j-1]+[a_{i-1}\ne b_{j-1}]).
\]

For'ab'→'ac', rows including the empty prefix are[0,1,2],[1,0,1],[2,1,1]. The
answer is1, changing b to c. A maximum instead of a minimum plainly fails even
'a'→'a': costly insert/delete detours are not the objective. Retaining two rows
costs O(|b|) cells while evaluating O(|a||b|) candidates. This reference returns
cost only; edit-script reconstruction needs retained decisions or another method.
Unicode code points are compared; a user-perceived grapheme can occupy several
code points, so this is not a language-aware spelling model.

Longest common subsequence L[i,j] has a different objective: if final characters
match use L[i−1,j−1]+1; otherwise max(L[i−1,j],L[i,j−1]); empty-prefix bases0.
A subsequence preserves order without requiring contiguous positions. For'abc'
and'ac', the witness'ac' has length2. Zero-cost arbitrary replacement would make
'a' and'b' have edit cost0 while LCS length0; it is not the insert/delete-only
LCS equivalence. The source map records these source-note discrepancies rather
than copying them into the implementation.

## Intervals, graph layers and subsets

A matrix chain state needs both interval endpoints. For dimensions10,100,5,50,
(A0A1)A2 costs10·100·5 +10·5·50=7500 scalar multiplications. A0(A1A2)
costs100·5·50+10·100·50=75000. For interval[i,j), choose final split k and add
its two interval optima plus dims[i]·dims[k]·dims[j]. Single-matrix cost is0.
Increasing interval length gives a valid dependency order. There are O(n²)
states and O(n) split choices each, hence O(n³) scalar-operation counts. The
output parenthesization preserves operand order; arbitrary reordering is illegal.

A cheapest walk with a hop limit needs D[k,v], the best cost at v with **exactly**
k edges. Read only layer k−1 while producing k. On0→1 cost2,1→2 cost−5, one
in-place pass could claim a cost−3 route from0 to2 under budget1, despite using
two edges. Retained layers reject it. Compare target costs across0…H for an
'at most' contract. Negative cycles do not create unbounded value under finite H;
rejecting all repeated vertices would solve a different problem.

For one-to-one assignment, mask records which jobs have already been consumed.
Worker index is mask.bit_count(); no extra worker dimension is needed. Extending
with an unused job sets one bit. There are2^n masks and at most n transitions
each; the reference caps n at16. A cheapest job chosen independently for each
worker can use the same job twice and fail the defining constraint.

## Minimax inversion and arithmetic cost

Egg-drop asks for the worst-case drops needed with destructible probes and a
fixed monotone threshold. Instead of trying every first floor in a floor-count
state, let R[e,m] count floors distinguishable with e probes and m moves. A drop
has a break branch R[e−1,m−1], the tested floor, and a survive branch R[e,m−1].
Thus R[e,m]=R[e−1,m−1]+1+R[e,m−1]. Zero probes or zero moves resolve0 floors.
Descending e retains the previous move layer. For two probes, successive
coverages are1,3,6,10, so ten floors require four drops. A decision tree achieves
this bound by testing just above the lower branch's covered segment.

Python integer addition is exact but not constant-time at every magnitude.
Counting parenthesizations or legal bit strings grows integer bit length. State
and transition counts are useful; a real runtime analysis must also include bit
operations, allocation and witness output. Most functions assume finite,
locally trusted teaching inputs rather than imposing a universal service budget.
Set explicit input limits before exposing them through an API. None is an
untrusted-input sandbox or a memory-safe resource quota for arbitrary generators.

## Build and investigate

Attempt the problem prompts before hints or solutions. For each, supply a state
meaning, exhaustive final-choice cases, base cases, acyclic evaluation order,
proof and reconstructed output check. A witness with the right score but illegal
indices is a failure. Ties need a documented choice policy, not necessarily the
same witness as a different correct solver.

```sh
python3 algorithmic-problem-solving/topics/dynamic-programming/run_all_tests.py
python3 algorithmic-problem-solving/topics/dynamic-programming/experiment.py
```

The suite uses BFS of actual edit strings, enumeration of subsets/routes/syntax
trees/permutations and a floor-based minimax oracle. These avoid merely copying
the same recurrence into the test. [EXPERIMENTS](EXPERIMENTS.md) compares repeated
search against memoized state work and retains wrong-loop counterexamples.
[Sources](SOURCES.md) distinguish inspected lecture mechanisms from original
extensions. The per-problem derivations supply separated solutions; your final
memory challenge is to reconstruct three different state families and explain
which changed constraint would force each state to grow.
