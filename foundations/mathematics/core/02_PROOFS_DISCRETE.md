# Contracts, discrete models and proofs

Prerequisite: [algebra/functions](01_ALGEBRA_FUNCTIONS.md). This chapter develops
the reasoning used by the graph, parser, arithmetic, database and protocol labs.
An experiment can refute a universal claim with a counterexample. Passing finite
tests cannot establish that claim for every allowed input; a proof explains why
the implementation preserves the contract.

## 1. Propositions and quantifiers make the contract precise

A proposition is a statement with a truth value under a declared interpretation.
`n is even` is a predicate whose truth depends on n. `P and Q` requires both;
`P or Q` includes the case where both hold. `not P` reverses truth. The
implication P⇒Q is false exactly when P holds and Q fails. Its truth table is:

| P | Q | P⇒Q |
| --- | --- | --- |
| false | false | true |
| false | true | true |
| true | false | false |
| true | true | true |

An implication does not assert P. “If the checksum fails, reject” does not say
that a checksum will fail. Its converse Q⇒P is a different claim. A checksum
passing does not establish authenticity or correct measurement.

`∀x in D, P(x)` means every allowed x satisfies P. `∃x in D, P(x)` needs at
least one witness. The negation of∀xP(x) is∃x notP(x). A sorted array family
can refute an unconditional linear-time claim about quickselect with a
deterministic last-element pivot, while a thousand random arrays cannot prove
that worst-case claim. Other pivot rules need their own analysis; deterministic
median-of-medians can provide a worst-case linear bound.
“Every request eventually finishes” also needs a time/failure model; a timeout
test on one request cannot supply an unbounded liveness theorem.

## 2. Sets, relations and functions are different structures

A set records membership without order or duplicate multiplicity. A sequence
does preserve order and multiplicity. `{a,b}` equals `{b,a}`, but messages
`[put(x,1),put(x,2)]` and the reverse order can produce different states.
Deduplicating a sequence into a set may change the problem.

A binary relation is a subset of D×D. Reachability in a directed graph is a
relation: (u,v) belongs when a directed path exists. It may be reflexive if
zero-length paths count, and it is transitive by path concatenation. It is not
generally symmetric. A partial order is reflexive, antisymmetric and transitive;
two distinct elements may be incomparable. Causal order therefore does not
automatically define one total chronological order for concurrent events.

## 3. Four proof patterns, with actual examples

**Direct proof.** If m=2a and n=2b are even integers, m+n=2(a+b), so the sum is
even. The proof unfolds the definition and constructs its witness a+b.

**Contrapositive.** To show “n² even implies n even,” prove “n odd implies n²
odd.” Let n=2k+1; then n²=4k²+4k+1=2(2k²+2k)+1. Merely checking odd inputs
does not replace this argument over all integers.

**Contradiction.** A nonempty finite directed acyclic graph has a vertex of indegree zero.
Suppose every vertex has an incoming edge. Follow predecessors indefinitely.
Finiteness forces a repeated vertex; the repeated segment is a directed cycle,
contradicting acyclicity. This establishes why topological removal can start.

**Induction.** Claim1+2+...+n=n(n+1)/2 for n>=0. At n=0 both sides are0.
Assume it for n. Adding n+1 gives n(n+1)/2+(n+1)=(n+1)(n+2)/2, the next case.
The induction hypothesis is an explicitly permitted assumption for one step;
it is not assuming the whole claim. For a recursively defined algorithm,
strong induction may assume every smaller input size.

## 4. Loop invariants connect proofs to executable transitions

For Euclid's algorithm, start with nonnegative a,b. While b≠0 replace
`(a,b)` by `(b,a mod b)`. The invariant is equality of common-divisor sets:
if d divides both a and b, it divides a−qb; conversely if d divides b and
r=a−qb, it divides r+qb=a. Therefore gcd(a,b)=gcd(b,r).

The remainder satisfies0<=r<b, so the second component strictly decreases
until zero. At that point every divisor common to(a,0) divides a, giving gcd=a
when a>0. We define gcd(0,0)=0 as a computational convention and handle it
separately. With negative original inputs take absolute values before this
nonnegative proof. A loop invariant alone is insufficient: termination also
needs a decreasing well-founded quantity.

Worked trace: (84,30)→(30,24)→(24,6)→(6,0), result6. Extended Euclid also
tracks coefficients s,t with `a=s*a_original+t*b_original`. Subtracting the
same quotient multiple from coefficient rows preserves that equality. For
84 and30,6=3*30−84. The reference [discrete.py](discrete.py) records this
mechanism; tests compare gcd to an independent library oracle and verify the
coefficient identity rather than merely comparing final numbers.

Square-and-multiply maintains `result * base^exponent = original_base^original_exponent`
modulo m. For an odd exponent, move one base factor into result; then square
base and halve the remaining exponent. For an even exponent, only square and
halve. Positive m defines residue classes. The invariant proves correctness,
and integer halving proves termination. It does not prove constant-time behavior
or make this teaching code suitable for secret exponents.

## 5. Counting and asymptotic claims have assumptions

If one field has a choices and another has b independently selectable choices,
there are ab pairs. A w-bit word has2^w arrangements. Choosing k distinct
positions from n without order gives `n!/(k!(n-k)!)`: n! lists all ordered
positions; permutations within the chosen and unchosen groups are duplicates.
Factorial0!=1 makes choosing zero or all positions work.

A complete simple undirected graph has n(n−1)/2 edges: n vertices each pair
with n−1 others and every edge is counted twice. A directed simple graph
without self-loops instead permits n(n−1) edges. Using the wrong graph model
changes a memory budget by approximately a factor of two.

`f(n)=O(g(n))` means there are constants C,n₀ such that f(n)<=C g(n) for
all n>=n₀ in the declared domain. It is an eventual upper bound, not an exact
runtime. Θ bounds above and below; Ω is a lower bound. A worst-case bound
maximizes over all allowed inputs of size n. An expected bound requires a
distribution or algorithmic randomness. “Usually fast” without either is
not a mathematical expectation.

For a loop visiting each vertex and each adjacency-list edge once, operation
counts grow as V+E. An adjacency matrix scan can instead inspect V² entries,
even for a sparse graph. The representation is part of the analysis. Python
list slicing allocates references; arbitrary-precision arithmetic costs depend
on operand bit lengths. A RAM-model O(1) arithmetic operation is an assumption,
not a promise about giant integers or measured latency.

## 6. From proof to adversarial tests

Test the specification and the implementation through different structures.
For a tiny graph, enumerate every walk up to the vertex bound to check BFS
distances. For integer arithmetic, compare extended-GCD coefficients and
the divisibility definition as well as a library answer. For exponentiation,
compare tiny exponents to repeated multiplication before a fast oracle.

A proof that assumes valid adjacency IDs does not excuse failing to validate
IDs at the API boundary. A parser proof over a fixed buffer does not prove
behavior under later mutation or concurrent access. State assumptions in both
the lesson and the executable contract.

Run `python3 -m unittest discover -s foundations/mathematics/core -v`.
Attempt D1–D8 in [EXERCISES](EXERCISES.md); consult the separated hints/solutions.
Then use the graph problem release and causal-clock research project to transfer
these invariants. Continue to [vectors and maps](03_VECTORS_MAPS.md) when a
system contains several interacting quantities.
