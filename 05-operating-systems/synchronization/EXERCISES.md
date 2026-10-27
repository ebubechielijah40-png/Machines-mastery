# Attempt before opening hints or solutions

1. Hand trace two split increments ending at one. Name local and shared state
   separately at each step.
2. Derive the 20 schedules. Explain why the final-two count is two without
   using the program's output as your argument.
3. Give a store-only-lock trace ending at one despite no simultaneous lock owners.
4. State the invariant the whole critical section protects. Identify the exact
   operation that prevents the second worker from loading stale zero.
5. Explain why C atomic load followed by atomic store differs from atomic fetch-add.
   Explain why plain unsynchronized C int is not the same defined model.
6. Rebuild the forced-load experiment using an atomic gate. Document why the
   gate forces the two loaded values, and how main safely reads worker records.
7. Draw a lost-wakeup order with data present but consumer blocked. State what
   atomic wait registration removes from that order.
8. Under the model's one optional wake, give an if-recheck safety failure. Then
   trace how while rechecks and waits again instead.
9. Implement the one-slot buffer in a learner copy, retaining full/slot access
   under one mutex. Check the sequence as well as sum. Exercise partial thread-
   creation cleanup through an injected creation wrapper in your copy.
10. Transfer to a two-slot FIFO. Derive head/tail/count invariants, empty/full
    predicates and wraparound. Test at least two complete wraps, with exact
    item identity. Do not claim the current one-slot model already proves it.
11. Transfer to two consumers: after a wake, allow the other consumer to take
    the item first. Explain the necessary predicate recheck.
12. Reconstruct the models and one C build without notes. Before running,
    write one safety test, one progress counterexample and one stated limit.

Rubric, 20 points: state/derivation 4, locking invariant 4, condition predicates
and failure distinction 4, actual evidence/limits 4, reconstruction/transfer 4.
Each category scores 0 absent, 1 terms only, 2 ordinary working case, 3 explained
failure/edge case, 4 independent transfer. A plain-C data-race claim treated as
a finite permitted outcome set, or a model path frequency presented as a host
probability, blocks a passing result regardless of total.
