# Solutions and invariant arguments

## Rounding and split trace

With quantum 8, 7 rounds to 8 and 9 rounds to 16. Allocation first replaces
`[0,256)` by used `[0,8)` and free `[8,256)`, then splits the second interval
at 24. The two allocations contain 16 requested bytes and reserve 24, so their
internal fragmentation is 8 bytes. Rounding 256 leaves 256; 0 and values over
256 are rejected before the addition used in rounding.

## Why split preserves the partition

Suppose a free interval starts at x with size s, and 0 < r ≤ s. For r < s,
`[x,x+r)` followed by `[x+r,x+s)` has positive sizes, the same union and no
overlap. Offsets and sizes remain aligned because r and s are multiples of 8.
Other intervals are unchanged. For r = s, mark used without adding a remainder.
An allocation cannot touch a prior live region if the incoming partition is valid.

## Why coalescing preserves it

Two neighboring free intervals share exactly one boundary. Replacing their
sizes s,t by s+t preserves their union and order. No live payload changes.
Repeated merging terminates because the block count decreases each time.
The resulting list has no adjacent free entries. Freeing the 7-byte block alone
cannot merge across the still-live 9-byte block; releasing that block joins all
three intervals into `[0,256)`.

## Fragmentation counterexample

Thirty-two 8-byte blocks fill the arena. Releasing even indices creates holes
`[0,8)`, `[16,24)`, …, `[240,248)`. There are sixteen, totaling 128 bytes,
but none can satisfy rounded size 16. The failure follows from contiguity, not
insufficient aggregate capacity. Once every odd block is released, adjacency
allows merging the full range. Stable raw pointers prevent transparent movement
of remaining live payloads unless the client contract changes.

## Pointer and lease distinction

An unrelated pointer is not subtracted from the arena base. The search compares
it with known starts and rejects it when none matches. `NULL` is rejected by
this API; unlike C's standard `free(NULL)`, this project reports false. A stale
pointer at a reused offset can match a new lease's start and is not detectable
from address bits alone. A handle `(slot, generation)` with a checked generation
can represent lease identity, but requires a changed API and wraparound policy.

## Independent checks and reconstruction

A live-region list outside allocator metadata can compare all region pairs
and retained byte tags. This detects an implementation returning the same live
region twice even if its own metadata checker remains satisfied. A reconstruction
must explain the partition invariant, arithmetic precheck, reverse insertion,
coalescing and byte-only storage contract, then pass an adversarial trace written
before reading the reference. A fresh implementation at a different capacity
is a transfer; matching formatting or line count is not.
