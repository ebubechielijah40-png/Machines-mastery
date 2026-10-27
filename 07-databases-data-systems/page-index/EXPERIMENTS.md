# Page shape, access work and transaction evidence

## Questions and protocol

Can a byte-serialized tree reduce examined pages? Does sorting before building
change its shape? Do checksums make a multi-page update atomic? Predict all three
before running from the root:

```sh
python3 -m unittest discover -s 07-databases-data-systems/page-index -v
python3 07-databases-data-systems/page-index/experiment.py
python3 07-databases-data-systems/page-index/experiment_rebuild.py
```

The [saved index run](evidence/observed.json) uses4096 unique integer keys, ASCII
decimal values, page sizes128/256/512/1024, fixed shuffle seed4081 and the same
102 point queries and100-row range in each case. Build ascending, shuffled and
bulk variants; reopen serialized bytes; count page decode requests, page images,
height, leaf count, serialized bytes and elapsed build time. These are actual
logical work counters. They are not disk reads, filesystem latency, flash writes
or an OS cache model. Byte-cell capacity reserves24 bytes even for short values.

## Actual observations

| Page bytes | Method | Height in edges | Leaf pages | Point requests total | Range requests | Snapshot bytes |
| --- | --- | --- | --- | --- | --- | --- |
|128|ascending|4|2048|510|55|314404|
|128|shuffled|4|1745|510|46|259748|
|128|bulk|4|1366|510|39|194596|
|256|ascending|3|1024|408|29|288292|
|256|shuffled|3|800|408|25|221220|
|256|bulk|3|586|408|19|158500|
|512|ascending|2|585|306|18|313380|
|512|shuffled|2|407|306|13|216612|
|512|bulk|2|293|306|11|154148|
|1024|ascending|2|273|306|10|286756|
|1024|shuffled|2|196|306|8|205860|
|1024|bulk|2|137|306|7|143396|

A point lookup requests height+1 pages in this no-cache model, explaining the
multiples of102. Range lookup pays a descent and leaf traversal; denser leaves
reduce its work. Bulk construction packs more rows into each leaf, but must
have sorted unique input. Its cost includes that prerequisite when starting
from unsorted data. A larger page can reduce height while reading more bytes
per request; page-count reduction alone is not a latency prediction.

Insertion traces retain every page after keys10,20,30,25,5,15,35. At128 bytes
the fourth key splits a full leaf into[10,20] and[25,30]; separator25 routes
queries to the right subtree for keys≥25. The later15 insertion creates a third
leaf and root separators15,25. Use this trace as an independent hand-drawing task.

The mixed-snapshot experiment replaces one page image with another from a later
valid tree and retains valid checksums. The decoded tree has30 rows and passes
structural validation, but key0 is'new' while key29 is'old'. This is a successful
counterexample to checksum-implies-transaction reasoning. It does not demonstrate
an actual interrupted durable write; no fsync or atomic publication is implemented.

## Rebuild from the authoritative WAL

[rebuild.json](evidence/rebuild.json) records an actual read-only scan of all171
prefix lengths from the seven-byte WAL header through byte177. For each prefix,
recover only complete committed transactions, build a fresh index, and compare
all rows to an independent expected state. The observed groups were:

| Complete transactions | First–last cut | Logical rows |
| --- | --- | --- |
|0|7–64|empty|
|1|65–122|0:'old',29:'old'|
|2|123–176|0:'new',29:'new'|
|3|177|−2:'é',29:'new'|

No cut admitted half of a committed pair. The protocol doesn't skip records based
on a checkpoint or modify the source log. It rebuilds a secondary structure
from the existing WAL authority; it does not add page logging, background
checkpoints, concurrent writers or durable index replacement.

## Interpretation and extensions

The hypotheses about logical access and bulk shape are supported for the stated
workload. Variable-length cells, value overflow, skewed ranges, a buffer pool and
real storage can change engineering conclusions. Repeat with different values,
page sizes and key distributions; record bytes decoded as well as requests.
For a crash-safe published index, first design an authority/version protocol,
then inject failure at every publication step. Never label the present checksum
or rebuild tests a power-failure guarantee.
