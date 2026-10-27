# Solutions and transfer reasoning

The hand lost-update trace is A-load, B-load, A-add, B-add, A-store, B-store.
Both locals become one and both stores publish one. Choosing A's three positions
out of six gives 20 schedules. Final two requires a load to see the other's
stored one; that store must precede the load, forcing one complete three-step
increment before the other starts. Only A-all then B-all or the reverse qualify.
The remaining 18 lose one update; none ends at zero because both stores publish
at least one.

Store-only locking still permits A-load, B-load, A-add, B-add, A-lock, A-store,
A-unlock, B-lock, B-store, B-unlock. No lock overlap occurs, yet both stores write
one. A whole critical section excludes the second load until the first store
and release. Atomic fetch-add instead performs one read-modify-write shared
transition. An atomic variable used in two separate operations does not compose
those operations into a transaction.

C's data-race rule is a language constraint, not a scheduler option. The real
split experiment uses sequentially consistent atomic accesses and a gate that
forces both loads before either store. Each worker writes its own output slot,
and main reads those slots after joining both. The mutex case protects the
plain counter; joins precede main's final plain read. No observed natural race
frequency or relaxed-memory conclusion follows.

Lost-wakeup witness: consumer acquires, sees empty, releases without registering;
producer acquires, puts, notifies nobody, releases; consumer registers and blocks.
The predicate is true but no producer work remains. Combining release with
registration removes that gap relative to a producer using the same mutex.

If-recheck witness: consumer acquires, sees empty, atomically waits; the model
permits a wake without data; consumer reacquires and consumes without checking.
It violates nonempty-before-consume. With while, the same wake returns to check,
sees empty and waits again; the later producer put/notify can then allow progress.
This argument separates safety from fairness: an unfair scheduler can still
withhold execution indefinitely.

For a two-slot FIFO, maintain 0≤count≤2, head/tail in {0,1}, and exactly count
live items in FIFO order. Producer waits while count=2; consumer while count=0.
A put writes at tail, advances tail modulo2 and increments count under the mutex;
a get reads head, advances it and decrements count. Exact sequence tests across
wraparound are necessary. The current implementation does not supply this build;
these equations are a transfer solution outline, not fabricated test evidence.

With two consumers, a woken consumer can lose the race for the mutex to another
consumer that takes the item. Returning from wait therefore cannot authorize an
unconditional get. It must reacquire and test the persistent predicate.

A reconstruction passes only with fresh expected traces, correct model/host
labels, defined C synchronization, lifecycle cleanup and a tested transfer.
The source files are runnable references, not evidence that the learner has
performed the reconstruction.
