# Build a page index in stages

First attempt the hand traces without opening bplus.py. Save predictions before
running the experiment. Keys are signed64 integers and values are at most24 bytes.

1. Derive leaf/internal capacities for128,256 and512-byte pages from the header,
   cells and CRC. Explain why character count is not value byte length.
2. Decode the lesson's first16 header bytes; locate both key/value cells by offset.
3. Explain why signed key order differs from lexicographic order of their bytes.
4. Derive the child chosen at equality with a separator. Supply a missing-key case.
5. Prove search preserves responsibility for the target interval through descent.
6. Trace inserts10,20,30,25,5,15 and draw both tree edges and leaf-successor edges.
7. Explain why a leaf separator is copied upward while an internal split boundary
   is removed from that internal page. Which pages still hold its record?
8. Force a page-budget failure during root splitting. Show the before/after
   serialized index is unchanged, and state which exception guarantees are absent.
9. Derive range[15,30), including cases where one or both endpoint keys are absent.
10. Prove the stated height bounds from minimum fanout and leaf occupancy.
11. Derive balanced bulk groups for10 rows at leaf capacity3. Why does naive
    capacity-sized chunking fail its final tail?
12. Construct a checksum-valid shared child, wrong separator, orphan, unequal depth
    or leaf-chain cycle and identify the invariant that rejects each.
13. Predict what a structurally valid old/new mixed snapshot can establish about
    atomicity. Execute the negative control before interpreting a passing CRC.
14. Rebuild from the canonical signed-integer/UTF-8 subset of a complete WAL.
    Include torn final transactions and a corrupted complete frame.
15. Explain why using an accepted stale index to skip source replay would need a
    new checkpoint identity/atomic-publication protocol.
16. Compare insertion and sorted bulk construction under fixed row count/page size.
    Distinguish logical page requests from actual device I/O.
17. Plan deletion: list the occupancy, separator, link, free-page and stale-reference
    invariants that must change. Do not claim it works before implementing/tests.
18. From blank files, reconstruct one leaf codec, point lookup, split and loader
    validation. Include a dictionary oracle and an intended corruption failure.

Acceptance rubric: byte/quantity precision4; invariants/proofs4; independent
oracles and failures4; controlled experiment and interpretation4; unaided
reconstruction/limits4. Author reference output does not supply a learner score.
