# Exact contract and remaining work

The caller supplies a valid initialized Arena and preserves its lifetime. The
implementation manages leases over a 256-byte unsigned-character array, in
8-byte quanta, with out-of-band metadata. It does not call malloc/mmap/brk,
return pages to an OS, implement realloc/calloc, or support concurrent access.
Payload is for byte buffers; eight-byte alignment does not establish support
for arbitrary C typed objects or over-aligned types.

Client bounds and lease lifetime remain obligations. The allocator cannot
prevent out-of-bounds writes, erase data on release, protect live regions from
one another, or detect all stale-pointer releases after address reuse. Reinitializing
an arena with live leases invalidates the logical ownership contract. Null,
interior, and currently free block starts are rejected; this differs from the
standard library free contract and must not be substituted for it.

The tests cover bounded deterministic traces at the observed compiler/settings.
UBSan and O0/O2 agreement do not prove portability or the absence of all undefined
behavior. No concurrency, latency, cache behavior or production allocator
performance has been measured. The wider allocator project remains PARTIAL.
