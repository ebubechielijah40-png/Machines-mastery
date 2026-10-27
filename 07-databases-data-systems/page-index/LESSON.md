# A page is a representation; a tree is a set of invariants

## 1. The access problem before the name

Suppose keys0 through4095 identify synthetic measurements. Each key maps to
small metadata. An unordered dictionary gives convenient equality lookup, but
"keys2000 through2099, in order" needs ordered work. A sorted contiguous list
supports binary search, yet an insertion near the front shifts many elements.
A binary tree can avoid those shifts, but following one key per node can visit
many separate storage blocks. The engineering question is how to keep many
routing choices inside each bounded transfer unit while retaining ordered data.

A B+ index organizes a sorted relation into leaves and internal routing pages.
Leaves contain values. Internal keys divide key space into intervals. The
"plus" convention used here also links leaves in order so a range can descend
once and continue along its neighboring pages. This is an access mechanism;
SQL meanings, transaction atomicity and hardware durability require other rules.

Do not imagine the Python dictionary that stores our page bytes is the index
algorithm. It only maps page identifiers to opaque byte strings. `get(25)` does
not ask that dictionary for key25. It first asks for root page3, interprets its
separator25 and follows its stored child identifier to leaf2.

## 2. Quantities and the deliberately small format

A **byte offset** locates a byte within a page; a **page identifier** chooses a
whole page. Page sizeB is in bytes. A key is a signed64-bit integer ordered
numerically. A value is0 to24 arbitrary bytes; its length is not a character
count. UTF-8 `é` occupies two bytes. A page identifier is a bounded positive
integer. Zero is reserved as the end-of-leaf-chain marker.

Our original format uses page sizes128,256,512,1024,2048 or4096 bytes. These
teaching sizes and layouts are not SQLite's file format. The very small option
makes splits happen before a learner has inserted hundreds of records.

| Offset | Bytes | Page-header meaning |
| --- | --- | --- |
|0|4|ASCII magic `BPI1`|
|4|1|Kind1 leaf or2 internal|
|5|1|Reserved, exactly zero|
|6|2|Number of keys, unsigned big-endian|
|8|4|This page's identifier|
|12|4|Leaf successor, or the first child for an internal page|
|16 onward|variable|Fixed-width cells|
|last4|4|CRC32 over the preceding bytes|

A leaf cell holds an8-byte signed key, a1-byte value length and a24-byte value
field, for33 bytes. Bytes beyond the declared value length must be zero. An
internal cell holds an8-byte separator and a4-byte child identifier, for12 bytes.
The first child is already in the header. Unused page bytes must also be zero.
Canonical padding lets the parser reject many malformed representations; it is
not secrecy or cryptographic authentication.

The maximum key counts follow from the space equation, not from a magic order:

\[
L=\left\lfloor\frac{B-16-4}{33}\right\rfloor,\qquad
I=\left\lfloor\frac{B-16-4}{12}\right\rfloor.
\]

ForB=128, L=3 and I=9, so an internal page can have10 children. A full leaf uses
16+3×33+4=119 bytes, leaving9 zero padding bytes. A full internal page uses all
128 bytes. Even an empty value reserves24 bytes. Variable-size slotted cells,
overflow pages and compaction would change these capacities and the split rule;
they are intentionally outside this implementation.

### Decode one page by hand

Take leaf7, successor8, keys−2 and9, values `b'A'` and `b'\x00B'`.
Its first16 bytes are:

```text
42504931 01 00 0002 00000007 00000008
```

The groups mean magic, kind, reserved, count, identity and successor. The first
key at offset16 is `fffffffffffffffe`: its signed interpretation is−2. Offset24
stores length1; offset25 stores `41`; the following23 value-field bytes are zero.
The second cell starts at16+33=49. Do not sort the encoded signed key bytes as
unsigned strings: that would place negative keys after positive keys. The codec
decodes the signed integers before ordering them.

The snapshot begins with32 bytes containing magic/version/page size/root/page
count/page budget/row count, then a4-byte header CRC, then pages1 throughP.
Pagej starts at byte36+(j−1)B. The exact total is36+PB. Truncation and trailing
bytes both violate this format; there is no "guess where the next page starts"
recovery scan.

## 3. The invariant makes routing correct

An internal page with separators `s0,...,s(k−1)` has children `c0,...,ck`.
Its child intervals are:

\[
(-\infty,s_0),\quad[s_0,s_1),\quad\dots,\quad[s_{k-1},+\infty).
\]

Within the ancestor's interval, each separator is exactly the minimum key in its
right child's subtree. Separators increase strictly. Every nonroot leaf contains
at least ceil(L/2) entries; every nonroot internal page contains at least
floor(I/2) separators. The root may be a small leaf, or an internal page with
at least two children. All leaves have the same depth. Every child has exactly
one parent, every page is reachable, and leaf successor links agree with that
left-to-right order.

To find a keyx, binary-search the separators for the first value **greater than**
x. Its position chooses the child. Thus equality goes right. With root `[25]`,
`x=25` chooses child1. Using "first separator greater than or equal to x" would
choose child0 and can miss an existing record. At a leaf, instead find the first
key greater than or equal to x, then check equality. These are the different
contracts of `bisect_right` and `bisect_left` used in the reference.

Why is descent sound? The root interval contains every key. If the current page
is responsible for an interval containingx, sorted separators assign exactly one
child interval containingx. The invariant says every descendant key lies in that
interval. Repeating this step preserves responsibility until a leaf is reached.
If that leaf lacksx, no other leaf's disjoint interval can containx. This is a
proof about a valid tree; the snapshot loader checks the premise before exposing
untrusted bytes as an index.

## 4. Insertion is a local repair that can propagate

First descend to the responsible leaf. If the key already exists, replace its
value; the row count does not increase. Otherwise insert it in sorted order.
If its key count stays at mostL, only that leaf changes.

WhenL=3, insert10,20,30. Root leaf1 is `[10,20,30]`. Inserting25 produces the
transient sequence `[10,20,25,30]`, which cannot be encoded into one page. Split
at floor(4/2)=2:

| Page | Kind and keys | Pointer consequence |
| --- | --- | --- |
|1|leaf `[10,20]`|successor becomes2|
|2|leaf `[25,30]`|successor is the old successor, zero|
|3|new root `[25]`|children are1 and2|

The separator25 is **copied** into the root. It remains a leaf key with its value.
Moving25 out of the leaf would destroy the record even though a routing key with
the same number still existed. No smaller key can enter the right half; no larger
key belongs to the left half. Both new leaves satisfy the minimum occupancy.
Only a new root increases the tree's height, so all leaf depths increase together.

Next insert5: leaf1 becomes `[5,10,20]`. Insert15: its sorted four keys split into
leaf1 `[5,10]` and new leaf4 `[15,20]`. Root3 becomes `[15,25]` with children
`[1,4,2]`; links become1→4→2. Physical page numbers need not be key order. Sorting
page IDs would visit values in the wrong order. The actual trace is retained in
[evidence/observed.json](evidence/observed.json).

### What an internal split removes

If a parent overflows, it hasI+1 separators andI+2 children. Choose middle
indexm=floor((I+1)/2). Its separatorp moves to the next parent; the old page
keeps keys beforem and children throughm, while the new right page keeps keys
afterm and children starting atm+1. The right page's first subtree still has
minimump, butp is no longer needed to distinguish children *inside that page*.

ForI=9, imagine separators `[10,20,30,40,50,55,60,70,80,90]`. Move55 upward;
left keys are `[10,20,30,40,50]` with six children, right keys `[60,70,80,90]`
with five children. Both have at least four separators. Every record remains in
a leaf. This is the distinction between moving an internal routing boundary and
losing leaf data. Recurse along the existing search path; untouched subtrees keep
their invariants.

## 5. A failure must not expose half a split

A split may need a right leaf, a modified old leaf and a new root. Suppose the
page budget allows only two pages. After filling the initial three-key root,
a fourth insertion can allocate its right leaf, then discover there is no room
for the new root. Publishing the modified old leaf first would lose reachability.

The reference's `_Edit` stages encoded changes and a proposed next identifier.
Validation/allocation failures discard that edit. Only after all necessary pages
are valid are its bytes installed and the root/row count changed. Tests compare
the entire pre/post snapshot after this resource failure.

This is scoped single-threaded exception handling. It is not a disk transaction,
a lock protocol, a guarantee against Python `MemoryError` during publication, or
a process-crash recovery argument. Concurrent calls or external modification of
private page maps violate the contract. The existing WAL project's fsync/unknown
outcome rules remain separate.

## 6. A range descends once, then follows leaves

`range(a,b)` meansa≤key<b and returns materialized ordered pairs. It descends
usinga, skips smaller entries in the first leaf, emits entries untilb, and follows
successor links as necessary. A missinga is normal: the next larger key can still
belong to the result. Equal or reversed finite endpoints return an empty list.
`None` is an unbounded endpoint, so `range(MAX_KEY,None)` can include the largest
representable key without inventing an out-of-range sentinelMAX_KEY+1.

The output occupiesO(q) Python memory forq returned rows. This implementation
is not a streaming cursor. A production iterator needs a rule for concurrent
splits/deletes and snapshot visibility; merely yielding one row at a time does
not supply that rule.

LetF=I+1 andf=floor(I/2)+1. Except at the root, branching is at leastf and at mostF.
If hequals the number of root-to-leaf edges, an occupied tree of height h≥1 has
at least2f^(h−1) leaves and at mostF^h leaves. With minimum leaf occupancyl and
maximumL:

\[
2l f^{h-1}\le N\le L F^h.
\]

This bounds height logarithmically inN for fixed capacities. A point lookup
requests h+1 pages; a range adds the leaves it visits, possibly one last leaf to
observe the stopping boundary. These are **logical page requests**, not measured
device reads. The model decodes complete byte pages, so CPU decoding work is
O(B) per requested page, not just the logarithmic within-page comparison cost.
Full validation and snapshot serialization additionally inspect all pages.

## 7. Bulk loading needs a valid final tail

Repeated insertion is correct but repeatedly descends and maintains free space.
If input is already strictly sorted, construct leaves, then parents bottom-up.
The code checks order/uniqueness; sorting itself is the caller's responsibility.

Naively chunking ten rows into capacity-three leaves yields sizes3,3,3,1. The
last leaf violates the minimum of two. Instead chooseg=ceil(N/L), divideN by g,
and distribute the remainder: sizes3,3,2,2. Every group differs in size by at most
one. At internal levels, group child pointers with capacityF and derive each
separator from the right child's known minimum. The final root may have fewer
children than other internal pages.

Why does balancing the tail suffice? For a level requiring at least two groups,
N>(g−1)c for group capacityc. HenceN/g>c−c/g≥c/2. Balanced group sizes therefore
meet the half-full requirement (rounding according to leaf/child capacity).
The root exception handles a single group. Repeating bottom-up preserves equal
leaf depth because all children of a new level came from the same prior level.

The reference materializes up to100,000 rows. It is not an external sort or an
out-of-core bulk loader. Its byte pages remain in a Python mapping, even after a
snapshot round trip through a temporary file.

## 8. Parsing is an adversarial graph problem too

A CRC check alone does not prove a valid index. The loader first bounds the byte
image, validates header fields and exact size, then decodes every fixed-position
page. It next checks the page graph and key constraints with an iterative
traversal: no dangling edge, cycle, shared child or orphan; no underfull nonroot;
correct subtree bounds and exact separator minima; equal depths; matching row
count; and an exact ordered leaf chain.

An iterative validator matters because an attacker can describe a deep invalid
graph. Recursive parsing could hit Python's recursion limit before reporting its
invalidity. Limits are16MiB per snapshot,65,535 pages and100,000 live rows. The API
accepts an already materialized byte string: an enclosing file/network reader must
also bound bytes *before* allocating them. This library has no network endpoint.

A checksum-valid page can still point to the wrong existing page. A valid index
can also be stale. Changing a snapshot's values and recomputing CRCs defeats any
"tamper protection" claim: CRC32 is a corruption checksum, not authentication.
Actual tests include both single-bit damage and re-encoded semantic corruptions;
passing those finite cases does not prove every corrupt input is rejected.

## 9. A structurally valid mixed state is accepted

Build thirty records with values `old`, save the image, then set keys0 and29 to
`new`. Construct a file with the new header/pages but the old page containing29.
Each page retains its own correct checksum. Order, occupancy, row count and links
still satisfy every invariant. The actual loader accepts key0=`new`, key29=`old`.

This is not a failed transaction implementation: the index does not implement
multi-key transactions at all. It is a direct counterexample to the incorrect
inference "all checksums pass, therefore the batch is atomic". Snapshot writes
can similarly truncate or mix without an atomic publication/recovery protocol.
Never overwrite authoritative data with `Path.write_bytes(index.dumps())` and
claim power-loss safety.

The [read-only rebuild bridge](rebuild.py) instead trusts the existing WAL's
complete transaction boundary, replays its full accepted prefix, converts its
canonical integer-key/UTF-8-value subset, sorts live rows and bulk-loads an index.
A torn final transaction contributes none of its operations. A corrupted complete
frame raises the WAL's corruption error rather than being skipped. Numeric order
is deliberate: string key `10` sorts before `2`, while integer10 sorts after2.
Noncanonical spellings such as `01` are rejected to avoid two strings silently
collapsing to one integer key.

Discarding a cache and replaying the authoritative log is safe under that log's
existing assumptions, but costs full-history replay plus sorting live state.
Skipping replay requires a separately verified checkpoint identity/transaction
position and an atomic relationship to the source. That mechanism is not supplied
here. Deleting historical WAL frames because an index file "looks valid" is an
incorrect extension.

## 10. Connect to engineering choices

Larger pages increase fanout and may reduce height, but transfer/decode more
bytes at once. Short keys and records improve occupancy; arbitrary-length values
need overflow or indirection. A secondary index stores references rather than
silently duplicating an authoritative record, and those references need stable
identity through record movement. Different collations change comparator semantics
and must agree with the query's ordering/equality contract.

Deletion would require a new occupancy/separator/link/free-page policy. Borrowing
or merging must preserve both the routing graph and the leaf chain, and page reuse
would require protection against stale references. None of those operations is
hidden inside an unsupported `delete` method. The learner's extension must add
new tests/proofs and a changed format/version when necessary.

Do the reconstruction challenge in [the exercises](EXERCISES.md), then explain
why the existing [query/isolation](../query-isolation/README.md) and
[WAL](../../projects-guided/p07-storage-engine/README.md) mechanisms solve different
parts of a database. A fast access path cannot decide whether a transaction's
business invariant, permissions or isolation requirement is correct.
