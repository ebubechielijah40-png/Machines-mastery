# Reference checks

1. Capacities are floor((B-20)/33) leaf keys and floor((B-20)/12) internal
separators. For128 bytes:3,9;256:7,19;512:14,41. Internal children are separators+1.
2. The header is magic BPI1,leaf1,reserved0,count2,page7,next8. First cell starts16;
second starts49. Its signed key encodings and value lengths are in the lesson.
3. The leading bit of negative signed64 encodings is1, so bytewise unsigned order
would place them after positive encodings. Numeric signed comparison is required.
4–5. Equality goes right via bisect_right on separators. The root owns the whole
key interval; each chosen child owns exactly its separator-defined subinterval.
Induction preserves responsibility until the unique possible leaf is reached.
6. After25, root3 separates25 and leaves1:[10,20],2:[25,30]. After5 then15, root3
has[15,25], children[1,4,2] and leaves1:[5,10],4:[15,20],2:[25,30].
7. Every value remains in a leaf. Copying a leaf boundary creates a route without
removing the record; an internal promoted boundary no longer separates children
inside either split page and moves to their parent.
8. A staged allocation that exhausts the budget must not publish modified old
pages. Tests compare exact snapshot bytes. This is single-thread exception safety,
not a disk transaction, memory-allocation-failure proof or process-crash guarantee.
9. Return existing keys k with15≤k<30. Absent endpoint keys are not errors;
unbounded None avoids an overflowing maximum-key sentinel.
10. At height h≥1, root has at least2 children; later internal levels have at least
f children, giving at least2f^(h-1) leaves and2l f^(h-1) records. Maximum fanoutF
and leaf sizeL give N≤L F^h. Point descent requests h+1 logical pages.
11. Four balanced groups give3,3,2,2. Naive3,3,3,1 leaves the last page underfull.
Derive separators from right-subtree minima while forming each parent level.
12. Graph validation separately rejects shared parentage/cycles/orphans, bound or
separator errors, unequal leaf depths and mismatched successor ordering. CRC alone
establishes none of those semantics.
13. The actual counterexample loads key0=new,key29=old with valid page checksums
and tree shape. It disproves the asserted implication from page validity to batch
atomicity; no transaction mechanism was implemented in this index.
14. Full source replay exposes only complete accepted WAL transactions. The tests
check every cut from file magic onward, numeric key order, incompatible spellings,
UTF-8 byte limits, stale-index discard and complete-frame corruption rejection.
15. Skipping replay needs evidence that snapshot contents correspond exactly to a
particular source transaction prefix, plus atomic publication/recovery rules.
Current code deliberately replays all history instead.
16. Metrics count logical encode/decode requests, serialized bytes and host build
time. OS cache, device latency and physical writes are not modeled by those counts.
17–18. A deletion extension needs its own complete state and failure argument.
A reconstruction passes only with original reasoning and independent observed
contracts, not because its private layout matches the reference Python objects.
