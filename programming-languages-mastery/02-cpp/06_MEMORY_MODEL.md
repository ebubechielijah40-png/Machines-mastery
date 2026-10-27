# C++ object lifetime and unique resource ownership

This developed bounded topic is taught in [resource-lifetime](units/resource-lifetime/README.md),
with an actual C++17 owner, deep copy, move, copy-and-swap assignment and exception
cleanup tests. The whole concurrency/atomic memory model and ABI remain incomplete.

A pointer value and a resource obligation are different things. Copying a pointer
copies an address representation; it does not decide which object releases the
allocation. Buffer therefore maintains a unique-owner invariant: one nonempty
object owns one allocation; an empty moved source owns none. A deep copy creates
another allocation, while a move transfers the original ownership state and empties
the source. Bounds check failures and dangling references are also different:
a once-valid reference can outlive a later assignment that releases its allocation.

Trace a(2), b copied from a, c moved from b: there are two live allocations after
the copy and still two after the move. b is empty. c and a release separate resources;
b releases nothing. [The source](units/resource-lifetime/resource.cpp) instruments
those states without relying on pointer-address coincidence. All three actual
compiler configurations, including UBSan, are recorded in
[observed.json](units/resource-lifetime/observed.json).

First draw that ownership graph, then rebuild its copy/move constructors without
notes. Give a counterexample showing why range checking alone cannot establish
lifetime safety. [Exercises](units/resource-lifetime/EXERCISES.md),
[hints](units/resource-lifetime/HINTS.md), [solutions](units/resource-lifetime/SOLUTIONS.md)
and [inspected source scope](units/resource-lifetime/SOURCES.md) are separate.
Do not infer multithread visibility, atomic ordering, object layout or every
standard-library moved-from guarantee from this bounded owner.
