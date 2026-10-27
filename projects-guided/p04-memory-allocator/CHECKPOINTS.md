# Implementation milestones

| Gate | Learner build | Checkable outcome |
| --- | --- | --- |
| A0 | Write the interval invariant and request contract | Correct 7/9-byte hand trace, explicit byte-only storage rule |
| A1 | Implement initialization and independent partition checks | One free `[0,256)`; gap/overlap/zero-size test fixtures rejected |
| A2 | Implement first fit with exact match | Allocating 256 succeeds once; second allocation fails |
| A3 | Add rounding and splitting | Requests 7 and 9 occupy offsets 0 and 8, sizes 8 and 16 |
| A4 | Release exact starts and coalesce | Interior/double release rejected; freeing both restores one block |
| A5 | Add live-byte preservation and independent overlap checks | Generated traces retain all payload tags |
| A6 | Measure fragmentation under an adversarial layout | Total free 128, largest free 8, request 16 fails |
| A7 | Reconstruct, then change geometry safely | Fresh implementation passes independent traces for a declared new capacity |

Use the provided header as an interface if needed, but attempt `arena.c`
without copying the reference. Do not use system malloc for bookkeeping in this
build: the point is to make allocation state visible.

Rubric, 20 points: invariant and proof 4, allocation/release mechanics 4,
independent tests 4, experiment interpretation 4, reconstruction/transfer 4.
Each category ranges from absent (0), vocabulary only (1), ordinary working
case (2), edge/failure explanation (3), to an independently verified transfer
(4). Any overlapping live allocations, lost payload, or unsupported arbitrary-
object claim blocks a passing build regardless of total. Tests passing at one
optimization level alone do not establish correct C semantics.
