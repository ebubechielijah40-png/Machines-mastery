# Checkable solutions

1. Input tag/body remain caller-owned. init duplicates both; changes to caller
   storage do not change Packet. The first test checks [1,2,3] and hdr after the
   input arrays are changed. Editing packet.body does not edit the source array.
2. Invalid→none, first failure→none, second failure→free tag, success→caller owns
   both. Without registration before allocation2, try returns through a path
   that has lost the only cleanup owner of the successful first allocation.
3. Budgets1,2: OutOfMemory at tag.4: OutOfMemory at body, tag rewound.8,16: success,
   end7 before cleanup,0 after. All failed paths end0 for these byte allocations.
   Exact raw traces are in evidence/observed.json; there is no RSS measurement.
4. A defer inside init would execute on successful return too, freeing memory
   still referenced by Packet. errdefer leaves successful ownership to the caller.
5. clone can call Packet.init(new_allocator, self.tag, self.body). Tests must
   mutate clone/original separately and run checkAllAllocationFailures over the
   clone scenario, cleaning the successful result. Two structs alone do not
   prove two allocations exist.
6. Register errdefer for body after its successful acquisition, then allocate3.
   On allocation3 error, reverse cleanup releases body and tag. Extend the
   successful destructor as well. Each finite acquisition prefix has an owner.
7. A const slice view forbids writes through that view. Another valid mutable
   alias can still edit the underlying storage sequentially; const does not
   create an owned deep snapshot or enforce Rust-style exclusive borrowing.
8. Both allocator context and backing array cease to be valid when that helper
   returns. Pass in an allocator/buffer whose owner outlives the Packet, or use
   a longer-lived heap allocator and an explicit deinit policy.
9. FixedBufferAllocator can rewind only its latest allocation in this scope.
   End position is not a registry of every logical lifetime. A second free of
   an already freed block violates ownership; reset is a separate whole-arena
   action permitted only after all users finish.
10. The reference tests cover all listed paths, including allocation-failure
    injection and separate success/failure state checks. Reconstruction should
    supply an independent failure-prefix table rather than copy implementation
    branches into an identical oracle.
11. A borrowed parser can return descriptors into input with no output-byte
    allocation. Input must stay live and follow the agreed mutation policy
    until every view is finished. A long-lived queued packet might therefore
    need an owned copy despite the parser's attractive no-copy interface.
