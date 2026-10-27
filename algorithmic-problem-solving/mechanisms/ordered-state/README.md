# Lookup, next priority and rank require different state

A list can answer a key lookup, find a minimum and count smaller keys. But scanning
it for every request costs linear work. This build constructs three mechanisms
and exposes the assumptions behind their faster cases. The original
[structures.py](structures.py) uses explicit hash buckets, an array heap and a
pointer-shaped binary search tree. Python dict, heapq and sorted are independent
test oracles, not their implementations.

Prerequisites: [Python](../../../02-programming/python-entry/README.md), integer
arithmetic, loops, [induction and invariants](../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md),
and arrays/pointers as representations. Read the sections in order, implement
before consulting the reference, then use [exercises](EXERCISES.md),
[hints](HINTS.md) and [solutions](SOLUTIONS.md). [SOURCES](SOURCES.md) maps inspected
lecture scopes; the concrete code, stability policy and experiments are original.

## A dictionary from buckets and equality

`ChainedMap` maps immutable byte strings to arbitrary caller-owned values. Begin
with four buckets and count0. A64-bit rolling prehash computes
`h=(257*h+byte) mod2^64`; bucket index is h mod capacity. Different keys can have
the same hash and bucket. Search compares actual key bytes in that bucket.
A hash match alone is not equality. Returning None for absence would conflict
with a legal stored None, so missing lookup/deletion raises KeyError.

For b'ab', h=97·257+98=25027, index3 at capacity4. Inserting b'a' has h97,index1.
Inserting b'e' has h101,index1 and appends to the same bucket; both must remain
retrievable. Overwriting b'a' changes only its value, not size. Deleting b'a'
removes that entry without losing b'e'. Mutable bytearray keys are rejected:
changing a key after placement would disconnect equality from its bucket.

Before a new key would make4·size>3·capacity, double capacity and recompute
bucket indices for every existing key. Reusing old indices would be wrong because
mod8 differs from mod4. The implementation constructs replacement buckets before
publishing them. Custom hash functions must be stable, deterministic and free of
side effects; arbitrary throwing callbacks are not a promised transactional
extension point. This is a single-threaded structure, not a lock-free map.

Under a uniform-distribution assumption, average bucket occupancy is α=n/m and
expected search work is O(1+α), plus the cost of hashing/comparing byte strings.
The rolling polynomial here is not a universal-hashing guarantee and not a
cryptographic primitive. A constant hash puts all n entries in one chain, causing
n(n−1)/2 key comparisons during distinct insertion. Doubling capacity cannot
repair identical hashes. Geometric growth bounds total rehashed entries by a
constant times n; that amortizes relocation, not adversarial equality comparisons.
The map does not shrink on delete, so retained capacity can exceed current size.

## A stable priority queue from an array

`StableHeap` stores `(priority, insertion serial, payload)`. Only priority and
serial are compared; two dictionary payloads need not be orderable. Equal
priorities emerge in insertion order. This is part of the contract, not a Python
side effect. Priorities are integers and Boolean is rejected as an accidental int.
For zero-based index i, parent=(i−1)//2 and children2i+1,2i+2. Every parent tuple
is at most each child tuple under lexicographic(priority,serial) order.

Push priorities5(A),2(B),2(C). After the first push root5A. The second appends2B
and exchanges it with its parent. The third appends2C and stops because2B has an
earlier serial. Popping returns B; move last2C to the root, compare children,
then return C before A. An incorrect `(priority,payload)` comparison can throw
for dictionaries or assign ties according to payload rather than arrival.

Push repairs only the new leaf-to-root path. Pop removes the root, moves the
last item to the root, chooses the smaller child and repairs one path downward.
Other subtrees remain heaps. Tree height is O(log n), so each path has that many
comparisons. Empty pop raises IndexError. Building from n items calls downward
repair on parents in reverse order; children are already heaps. At height h,
there are at most about n/2^(h+1) such nodes. Summing n·Σh h/2^(h+1)=O(n)
explains linear build despite a logarithmic worst-case single repair.

The backing array is heap ordered, not globally sorted. Finding an arbitrary
payload, deleting it or changing its priority needs another design or O(n) scan;
this unit does not promise those operations. Serial growth, integer comparison,
allocation and caller-owned mutable payloads still have engineering costs.

## A search tree with order statistics

`SearchTree` maps unique integer keys to values. Every key in a left subtree is
strictly smaller than its node; every key in the right is greater. Equal-key
insertion overwrites. Each node retains `size=1+left.size+right.size`. A lookup
chooses one child after comparison, costing O(height). Iterative traversal emits
increasing keys and avoids recursion failure on the tested skewed input.

Insert8,3,10,1,6,14,4,7,13. Root8 has left subtree keys1,3,4,6,7 of size5, right
subtree10,13,14 of size3, total9. `rank(7)` counts strictly smaller keys:
move left at8; at3 add size(left)+1=2; at6 add size(left)+1=2; stop below7,
giving4. `select(4)` returns key7: compare requested zero-based rank to each left
size, subtracting leftsize+1 on a right move. Rank accepts absent keys, while
select rejects a rank outside0…n−1.

Deleting a leaf detaches it. Deleting a one-child node splices its child to its
parent. For two children, choose the least key of the right subtree, copy that
key/value into the target node, then splice out the successor, which has no left
child. Recompute sizes along the complete affected path from the splice upward.
For deleting8 above, successor10 becomes the new root key, and old10 is replaced
by its right subtree14. Omitting a size repair can preserve lookup/order while
breaking rank/select: test the metadata as a distinct invariant.

No rotations or balancing are implemented. Inserting sorted keys0…n−1 creates a
chain of height n, and distinct insertion makes n(n−1)/2 comparisons. Calling
all BST operations O(log n) would be false for this implementation. A balanced
variant needs an additional height/color invariant and rotations that also repair
size metadata. Iteration avoiding Python recursion does not change quadratic work.

## Run, measure and transfer

```sh
python3 -m unittest discover -s algorithmic-problem-solving/mechanisms/ordered-state -v
python3 algorithmic-problem-solving/mechanisms/ordered-state/experiment.py
```

Six tests compare thousands of operation histories to independent maps/sorted
entries, including constant-hash collisions, stable ties with unorderable payloads,
all deletion shapes, absent keys and a1100-node skew. [EXPERIMENTS](EXPERIMENTS.md)
retains actual operation counts for hash collisions, heap construction and tree
shape. No single-host time is presented as a universal ranking.

Build a key/value symbol table, then a stable task scheduler, then rank/select
for ordered samples. Deliver state diagrams for your own examples, an invariant
proof, independent tests, raw experiment data and one deliberate failure. Each
mechanism earns one point for correct behavior, derivation, independent testing,
measured failure and unaided reconstruction, up to15. The reference's passing
suite alone earns no evidence that the learner reconstructed it.

For production use, budget key lengths and operations; choose a collision policy
appropriate to hostile keys, balance ordered trees, isolate concurrent ownership
and define iteration snapshots. `items()` returns a tuple snapshot whose values
still refer to caller-owned objects. None of these mechanisms is a persistent,
thread-safe, adversarially bounded storage engine. Continue to the
[byte-page B+ index](../../../07-databases-data-systems/page-index/README.md)
for external-page representation and durability limits.
