# Zig0.13: allocate, acquire, fail, clean up

This is a developed original Zig0.13.0 build. The larger Zig route remains
PARTIAL. APIs changed in other Zig releases; this unit does not claim compatibility
with them. Begin after [C objects/pointers](../../../../foundations/programming/c-reading/README.md)
and [the byte arena](../../../../projects-guided/p04-memory-allocator/README.md).
You need scopes, functions, byte slices and the difference between a value and
the memory it describes. The new syntax is introduced below before the build.

## The engineering problem

A Packet needs an owned tag and an owned body. A request can fail before either
allocation, after the tag allocation, or after both allocations. A success-only
cleanup path leaks the tag when the second allocation fails. This is especially
important in bounded machines where memory exhaustion is an ordinary outcome.
Our design makes allocator choice and error cleanup explicit at the interface.
It does not implement a garbage collector or Rust-style borrow checker.

Inputs are one allocator, a tag of1..32 bytes and a body of0..4096 bytes. Outputs
are an owned Packet or an error. On success, the caller must call deinit exactly
once. On failure, no allocation acquired by the constructor remains owned by it.
The caller's input slices are borrowed during the call; the constructor duplicates
their bytes. No sensor truth, authentication or text encoding is inferred from
these byte lengths.

## Read Zig before reasoning about the build

`const std = @import("std")` names the standard library. `[]const u8` is a slice
whose elements cannot be written through that view; `[]u8` permits writes. Neither
slice owns its memory automatically. A struct value can contain slice descriptors
and an allocator handle. Copying that struct copies those handles; it does not
automatically duplicate or transfer ownership of the referenced allocations.

`!Packet` is an error union: either Packet or an error. `try operation()` returns
the error from the current function when the operation fails, otherwise extracts
the success value. `return error.BadTag` creates a named error. `defer` schedules
an action when its current scope exits. `errdefer` schedules it only when exiting
that scope by an error return. These actions are scope-bound, not process-wide
finally handlers. `self: *Packet` permits mutation of the Packet value itself.

In [packet.zig](packet.zig), validation precedes allocation. After acquiring
owned_tag, the next line registers its error cleanup. Successful acquisition of
owned_body leaves no later fallible operation before the return. On success,
errdefer does not free the tag: responsibility passes to the returned Packet.
The caller's defer then schedules ordinary deinit on its own scope exit.

## Derive the failure matrix

| Path | Live constructor-owned allocations immediately before return | Required action |
| --- | --- | --- |
| Invalid tag/body shape | None | Return the domain error before touching allocator |
| Tag allocation fails | None | Propagate OutOfMemory |
| Tag succeeds, body fails | Tag only | errdefer frees tag, then propagate error |
| Both succeed | Tag and body | Return Packet; caller owns their cleanup |
| Caller finishes with successful Packet | Body and tag initially live | Free body then tag; never access Packet again |

This matrix is a finite proof obligation for the written constructor. If a new
fallible checksum/index allocation is added after owned_body, it needs its own
error cleanup registration. Passing today's tests would not justify omitting
that new path. [broken.zig](broken.zig) intentionally omits the first cleanup;
the driver expects a nonzero MemoryLeakDetected result from failure injection.
This is a small process-local leak negative control, not a deliberate invalid
pointer dereference.

## Follow the bytes and allocator state

Use a fixed8-byte buffer, tag=tag and body=DATA. Both allocations contain u8,
so their alignment here is1. The first consumes3 bytes; the second4; the observed
end_index becomes7. Reverse cleanup frees the latest allocation first and then
the previous one, returning the observed byte end to0. With only4 bytes, the
first allocation succeeds and the second fails; errdefer returns the end to0.
With1 or2 bytes, even the tag fails. These exact observations are retained.

This rewind is a property of the inspected FixedBufferAllocator implementation
and these latest byte allocations. It is not a general statement that freeing
any earlier block recovers arbitrary holes. Alignment adjustments, interleaved
allocations and a different allocator can behave differently. A bump allocator
can mark an older allocation logically freed without moving its current end.
The destructor must not call free again merely because the end did not move.

The allocator handle also has a lifetime: its context and backing buffer must
outlive every Packet using it. Returning a Packet backed by a local stack arena
would violate that contract after the function returns. A slice containing
`const` elements does not extend the backing allocation's lifetime.

## Why deinit is a contract, not automatic ownership checking

The implementation writes undefined into the Packet after freeing both buffers.
This discourages accidental reuse and can expose mistakes under some safety
modes; it is not a general checked tombstone. Access after deinit is outside the
API contract. Copying a live Packet and calling deinit on both copies can still
create an invalid double free. The correct discipline is one cleanup owner and
borrowed views whose users finish before cleanup. Do not demonstrate a repair by
adding undefined pointer behavior to the normal suite.

To support real independent owners, implement an explicit clone that allocates
both buffers again. To support transfer, stop using the previous logical owner
and clearly document who now calls deinit. Zig does not prove that application
policy for you. Compare with Rust's rejected use-after-move, C++ move/copy members
and Java's copied references.

## Execute, debug, extend

```sh
zig version
python3 programming-languages-mastery/04-zig/units/allocator-errors/run.py
```

The driver accepts ZIG or --compiler and requires version0.13.0. It runs6 tests
in Debug and ReleaseSafe, checks the broken constructor's expected failure, and
runs the budget experiment. An unsupported/missing compiler reports BLOCKED,
exit2; it never silently treats another standard library as the pinned one.
Test binaries/cache live in temporary directories, not the public source tree.

[Read the experiment](EXPERIMENTS.md), then attempt [the tasks](EXERCISES.md)
before [hints](HINTS.md) or [solutions](SOLUTIONS.md). Rebuild the constructor
from its failure matrix without copying source. Add a third fallible resource
and inject every failure. An embedded application also needs bounded CPU work,
interrupt/concurrency policy, lifetime review and hardware evidence; this byte
packet build does not supply those automatically.
