# C++ exceptions and resource invariants

An exception transfers control out of the ordinary success path. A resource owner
must preserve its invariant during that transfer, rather than rely on a delete
written after the operation that can throw. In the [RAII build](units/resource-lifetime/README.md),
two completed local owners are constructed before a controlled runtime_error.
Their destructors release resources in reverse order and the live counter returns0.
[Actual evidence](units/resource-lifetime/observed.json) covers this path at O0,
O2 and UBSan; it is not an unexecuted promise about all failures.

Assignment's strong guarantee means a failed attempt leaves the target's old
value intact. The reference takes a by-value parameter: constructing its deep copy
can fail before changing the target. A nonthrowing swap then commits the new owner,
and the parameter releases the previous target storage on exit. This ordering is
the mechanism. Declaring a mutating body noexcept is not a replacement for arranging
safe state transitions, nor a promise that parameter copying cannot throw.

A destructor should not propagate another failure during unwinding. The audit
uses fixed-capacity nonallocating storage to avoid turning cleanup logging into
another allocation. The lab does not force allocation failure or test custom
allocator exceptions; [an explicit failpoint exercise](units/resource-lifetime/EXERCISES.md)
is the next check. Draw normal, precommit-failure and successful-commit transitions
and identify which object owns each allocation at each point. Assertions express
internal test invariants; recoverable API errors such as an invalid index use a
defined exception. Catch only errors whose contract you can handle.
