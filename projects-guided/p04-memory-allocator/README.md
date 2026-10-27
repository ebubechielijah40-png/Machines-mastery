# Build an interval allocator over a fixed byte arena

A storage request asks for a contiguous region that remains reserved until its
owner releases it. The interesting work is deciding which region, recording
ownership, and restoring reusable space without overlapping a live allocation.
This project implements those mechanisms in C over 256 existing bytes.
It does not replace `malloc`, grow the process heap, or allocate arbitrary C
objects. Its returned regions are for byte buffers only.

Complete [entry checks](PREREQUISITES.md), then attempt the
[build milestones](CHECKPOINTS.md) before reading [hints](HINTS.md) or
[solutions](SOLUTIONS.md). The preceding [compile/link lab](../../04-computer-systems/compile-link/README.md)
provides the actual C toolchain investigation used here.

## 1. Start with intervals rather than addresses

Number the arena bytes 0 through 255. A block is a half-open interval
`[offset, offset + size)` with a `used` flag. The metadata array stores blocks
in increasing offset order. Addresses are derived only when returning a region:
`arena.bytes + offset`. Metadata is outside the payload, so writing within an
allocated byte region cannot overwrite its own block header. Out-of-bounds
writes remain a client error; separation is not memory protection.

The representation invariant is stronger than “the total size is 256”:

1. There is at least one block, and no more than the metadata capacity.
2. The first block begins at zero; each next offset equals the previous end.
3. Each size is positive and a multiple of eight; the final end is 256.
4. No two adjacent blocks are free after an operation completes.

Together these prove a complete, ordered, nonoverlapping partition. A sum alone
would allow a gap and a compensating overlap. [arena_check](code/arena.c) checks
this invariant after every operation in the generated trace test.

## 2. Round a request without hiding arithmetic assumptions

For request n and alignment quantum a = 8, the smallest suitable size is

\[
r(n) = a\left\lceil n/a\right\rceil
     = a\left\lfloor(n+a-1)/a\right\rfloor.
\]

The equality follows by writing n = qa + s with 0 ≤ s < a. If s = 0 the
quotient stays q; otherwise adding a − 1 raises it to q + 1. Request 7 reserves
8 bytes; request 9 reserves 16. Their internal fragmentation is 1 and 7 bytes.
The reference first rejects n = 0 and n > 256, so `n + 7` cannot overflow
`size_t` on an implementation capable of holding this arena. A generic allocator
would need an explicit maximum-size overflow guard before addition.

`_Alignas(8)` aligns the arena start and all offsets remain multiples of eight.
That is the project's storage layout rule, not a promise that every possible C
type is supported. The backing array has a declared unsigned-character type;
alignment alone does not turn it into the untyped allocated storage returned
by `malloc`. Keep payload accesses as bytes or use `memcpy` to/from separately
declared typed objects. C lifetime, effective type, alignment, and pointer
arithmetic scopes are mapped in [SOURCES.md](SOURCES.md).

## 3. First fit and splitting, by hand

Initially the partition contains `[0,256) free`. Allocate 7 bytes. Scan from the
front until a free block holds the rounded size 8. Replace it with `[0,8) used`
and `[8,256) free`. Allocate 9 next: the first block is occupied; split the
remaining free interval into `[8,24) used` and `[24,256) free`.

| Operation | Partition after completion |
| --- | --- |
| initialize | free `[0,256)` |
| allocate 7 | used `[0,8)`, free `[8,256)` |
| allocate 9 | used `[0,8)`, used `[8,24)`, free `[24,256)` |
| free first | free `[0,8)`, used `[8,24)`, free `[24,256)` |
| free second | free `[0,256)` |

If a free block exactly matches r(n), there is no remainder. Never insert a
zero-length free block. If a remainder exists, shift later metadata right to
make room, save the remainder at the next slot, and mark the chosen block used.
The returned byte pointer has a fixed offset even if metadata entries move.

The scan and metadata shifts are each O(B), for B blocks, with O(1) additional
working storage. Capacity 256 and minimum block size 8 imply B ≤ 32; the array
allows 64 entries. The explicit metadata-capacity guard remains useful for
future geometry changes but is unreachable with a valid current partition.
Metadata consumes space in addition to the 256 payload bytes. The experiment
records `sizeof(struct Arena)` and `sizeof(struct Block)` on the observed host;
these sizes are ABI-dependent, not fixed by this lesson.

## 4. Release and coalescing

`arena_free` searches for exact equality with the start of a currently used
block. Interior pointers and pointers not matching any block start are rejected;
a current free block is rejected as a double release. The search compares
pointers without subtracting a potentially unrelated pointer. It then marks
the interval free and merges adjacent free intervals until none remain.

For contiguous intervals `[x,x+s)` and `[x+s,x+s+t)`, their union is exactly
`[x,x+s+t)`. Merging preserves coverage and cannot touch a used interval. The
implementation compacts the metadata array after a merge and checks the same
index again, because it may now have another free neighbor.

This is a logical lease over the backing array. Releasing a region does not end
the C lifetime of that unsigned-character array. The client nevertheless must
stop using the lease: later allocation can hand those same bytes to another
owner. A stale pointer can equal a newly allocated block start, so this API
cannot detect every stale release. A generation-tagged handle would need
identity beyond a raw address. Do not claim double-release checks solve reuse.

## 5. Free bytes are not necessarily usable bytes

Allocate all 32 blocks of 8 bytes, then release even-numbered blocks. Total free
space is 16 × 8 = 128 bytes, but the largest free interval is only 8. A request
for 16 must fail. This is external fragmentation: enough total space exists,
but the current layout cannot supply one contiguous region. Releasing the
remaining blocks allows coalescing to recover the full 256-byte interval.

For a snapshot with free total F and largest hole L, `1 − L/F` is a useful
layout indicator when F > 0. Here it is `1 − 8/128 = 0.9375`. It is not a
universal allocator-quality score: request distribution and object lifetime
matter. Copying live payloads could compact space but would invalidate raw
client pointers. Stable handles or a moving runtime change that tradeoff.

## Run and investigate

A C11 compiler supporting the observed sanitizer options and Python 3.12+ are
needed for the complete harness. From the repository root:

```bash
python projects-guided/p04-memory-allocator/code/run.py
python projects-guided/p04-memory-allocator/code/experiment.py
```

The first command compiles and executes the assertions at O0, O2, and with
undefined-behavior sanitization. [The test guide](TESTS.md) explains the
independent checks and limits. The second captures actual interval snapshots,
fragmentation and host structure sizes. [The experiment protocol](EXPERIMENTS.md)
separates predictions from observations.

Submit implementation, invariant argument, failing-layout trace, tests,
observed record, and a reconstruction from memory. The bounded byte-interval
unit can be STRONG; the general allocator project is PARTIAL until typed-storage
semantics, system allocation, concurrency and production failure modes are
developed and tested. [Limits](LIMITS.md) states the exact contract.
