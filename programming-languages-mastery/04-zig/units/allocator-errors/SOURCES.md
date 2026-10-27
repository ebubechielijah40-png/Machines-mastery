# Source and version boundaries

Inspected2026-10-23. This unit is explicitly pinned to Zig0.13.0, not the current
unversioned language. The packet, failure matrix and exercises are original.

1. Zig project, [Language Reference0.13.0](https://ziglang.org/documentation/0.13.0/),
   selected Slices, defer, Error Union Type, try, errdefer and Common errdefer
   Slip-Ups sections. Supports view/error/scope facts; not full language coverage.
2. Exact0.13.0 official distribution source lib/std/heap.zig, FixedBufferAllocator
   lines372–493: init/allocator/alloc/isLastAllocation/free/reset. Inspected directly
   in the checksummed downloaded compiler distribution. This supports the narrow
   latest-byte-allocation rewind explanation; not every allocator/alignment case.
3. Same distribution lib/std/testing.zig, checkAllAllocationFailures lines1032–1110:
   baseline allocation count, induced failure prefixes and allocated/freed-byte
   checks. Supports what the native test harness actually checks, not a universal
   program leak-proof certificate.

The web standard-library app returned only its loading shell; raw GitHub fetches
were denied. Neither was claimed as an inspected implementation. The actual
versioned source above was available locally in the official distribution.
Its selected file hashes and official archive hash are in SOURCE_VERIFICATION.json.
No compiler distribution/full standard-library file is bundled with this unit.
Zig's source license is upstream's; public access does not assign blanket rights
to this repository. No source passage or external exercise set is reproduced.
