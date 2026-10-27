# Reasoning checks

1. After a:one allocation. After deep copy b:two. Moving b to c:still two, owned
   by a and c, b empty. c releases b's former allocation; b releases none; a releases
   its own. Names/addresses need not match the resource trace ID.
2. Pointer copy creates two release obligations for one allocation. Releasing
   either makes the other's pointer invalid; releasing again is undefined behavior.
3. Copy assignment first allocates the parameter copy, swaps it into a, then the
   parameter releases a's old allocation. Self-move first empties a into the
   parameter, then swaps that allocation back. This implementation preserves a's
   value. An exception during parameter copying occurs before the noexcept body.
4. Assignment destroys the old allocation when the swapped-out parameter dies.
   r is dangling. It carries no dynamic ownership/lifetime check, regardless of
   whether its original numeric index was in bounds.
5. A correct failpoint test checks both value equality and unchanged live count
   after the thrown allocation attempt. No partial pointer overwrite may happen
   before the successful temporary exists. This extension remains learner work.
6. A vector member makes element storage release/copy/move the member's obligation.
   A checked accessor can delegate to vector::at; explicit raw-owner special members
   become unnecessary for a simple value wrapper.
7. A unique file-handle wrapper commonly deletes copying and transfers ownership
   in move. If duplication is provided it must handle OS duplication failure and
   clarify shared file offset/state; array-copy semantics cannot be assumed.
