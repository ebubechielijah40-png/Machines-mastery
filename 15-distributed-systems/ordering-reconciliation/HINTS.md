# Hints

1. Receiving is another assignment; ask which write each replica sees last.
2. Receipt must be above both5 and2. Unrelated local counters need no messages.
3. Each expression selects the largest member of the same set. A receipt is
   a new event even when no map value changes.
4. Use equal counters to isolate the declared origin-ID tie rule.
5. Missing has no record stamp; an old live value can then become the maximum.
6. A state snapshot omits local events that did not write a winning record.
7. Build the entire candidate state before publishing it.
8. A signature can authenticate an origin without proving its counter obeys
   the protocol; a reset identity can reuse a previously valid stamp.
9. A money-transfer application needs conservation and transaction semantics,
   not just one deterministic selected balance after conflicting overwrites.
