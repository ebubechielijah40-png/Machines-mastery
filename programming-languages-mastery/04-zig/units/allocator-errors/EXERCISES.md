# Zig allocator/error tasks

1. Draw the two input views and two owned output allocations. Which four byte
   sequences change when the caller edits its original tag and body?
2. Fill the failure matrix without reading the implementation. Why must tag
   cleanup be registered before trying the body allocation?
3. Predict the1,2,4,8,16-byte budget experiment for tag=tag/body=DATA. Check both
   the outcome and end_index after cleanup; do not infer physical memory usage.
4. Explain why replacing errdefer with defer in init would break the successful
   return. State the ownership lifetime of the returned tag.
5. Add an explicit clone using a caller-supplied allocator. Inject failure in
   both clone allocations and test independence from the original Packet.
6. Add a third fallible allocation and extend the failure matrix. Demonstrate
   cleanup if that third acquisition fails; do not merely test the success case.
7. Why does `const view` not mean an immutable globally owned allocation? Show
   a safe sequential aliasing example using a separate mutable view.
8. A helper creates a FixedBufferAllocator over its local array and returns a
   Packet using it. Identify both lifetime violations without executing an
   invalid access. Design a corrected caller-owned arena interface.
9. Explain why freeing an older fixed-buffer allocation might not change its
   end. Why is freeing the same logically freed allocation again not a repair?
10. Reconstruct init/deinit from memory, including invalid input, zero body,
    first failure, second failure and successful cleanup tests.
11. Transfer: design a tag/body network parser that returns only borrowed slices.
    Which allocation paths disappear and which backing-buffer lifetime becomes
    the caller's responsibility? Do not confuse no-copy with no-lifetime-rule.
