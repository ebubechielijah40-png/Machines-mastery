# Rust ownership practice

Do not open the solutions before making a trace and a prediction.

1. Draw binding→Vec→allocation before and after Packet::new(vec![3,4]). Which
   later uses of the old vector variable compile?
2. Trace two calls to view, their last uses, and a later set. Move the last view
   use after set and predict the compiler's objection.
3. For a two-byte packet, predict set(2,8), the returned error and final bytes.
   Supply a test that distinguishes rejection from partial mutation.
4. Compare the time/space contracts of view and clone for n bytes. Explain why
   moving a handle is not the same operation as cloning the owned bytes.
5. Constructor failure consumes the supplied vector. Design a different API
   that returns the rejected vector alongside the reason; write its signature.
6. Predict both drop-order tests without running them. Distinguish local bindings
   from fields of one aggregate.
7. Repair each compile-fail case while preserving its intended output. State
   where extra allocation is introduced and where an access interval changes.
8. Add append_byte with an explicit4096-byte contract. A rejected append must
   preserve the packet. Test length4095,4096 and an initially invalid constructor.
9. Explain what joining the worker establishes and what this experiment never
   established about scheduling, panic recovery or shared caches.
10. Rebuild the successful mechanism from memory. Include invalid-length,
    rejected-mutation and clone-independence tests without copying the reference.
11. Change the experiment to u64 elements. Predict which capacities are unspecified
    and which length/sum/value properties can be tested independently.
12. Transfer: a caller requests an indefinitely retained view while another caller
    edits the vector. Propose an owned snapshot or synchronized shared design and
    name its copying/coordination cost. Do not add unsafe casts as a shortcut.
