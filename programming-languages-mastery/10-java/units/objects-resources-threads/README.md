# Java: references, resource cleanup and a compound update

Garbage collection does not decide when a file must close, a final reference does
not make an array immutable, and volatile does not make read-modify-write atomic.
This original build separates those mechanisms with fifteen executable checks.
Start with [Python aliases](../../../08-python/units/objects-and-aliases/README.md)
and [synchronization](../../../../05-operating-systems/synchronization/README.md).
No Java experience is assumed beyond the syntax introduced here.

## Read the types and object operations

A class declares fields, constructors and methods. new allocates an object and
runs its constructor; a reference variable names access to that object. A byte[]
reference points to an array object. Assignment copies the reference value, not
all array elements. static members belong to the class; an instance member uses
its receiver object. private restricts access in source; final prevents the field
from being reassigned after initialization under its rules. It does not recursively
freeze referenced objects. throws declares a possible checked exception; throw
actually completes execution abruptly with an exception object.

The deliberately broken AliasedPacket stores the caller's array reference in a
final field. Construct it from[3,5], then set source[0]=8: its first byte becomes8.
The correct Packet clones input in the constructor, so its first byte stays3.
But construction copying alone is insufficient: an accessor returning its private
array would leak writable access. snapshot() returns another clone. Mutating that
snapshot to42 leaves Packet unchanged. The ownership invariant is that no caller
retains a writable array alias through this API; it is a design property, not an
inference from the word final.

Java arguments are passed by value. For a reference argument, the copied value
is a reference. A method can mutate an accessible shared object's contents, but
reassigning its local parameter to a different Packet does not reassign the
caller's variable. The rebind example demonstrates that distinction. Null, empty
and oversized arrays are rejected before a Packet is constructed.

## Cleanup follows scope, even when cleanup itself fails

Resource implements AutoCloseable. Its constructor appends open:A or open:B to
a shared trace; use() appends use:name; close() appends close:name and deliberately
throws. try-with-resources initializes A then B, runs the body and closes successful
resources in reverse order. The body deliberately throws body failed. Expected
trace is open:A,open:B,use:A,use:B,close:B,close:A.

Which exception reaches catch? The body failure stays primary. Both closing
failures are preserved as suppressed exceptions, with B's first because it closes
first. Throwing from close does not prevent the remaining successful resource
from being closed. This prevents cleanup errors from silently erasing the original
failure, although a caller can still mishandle the exception by ignoring its details.

Automatic memory reclamation is different: reachability and the collector govern
heap storage reclamation, not prompt release of a file/socket/transaction. This
lab never invokes GC to “prove” when resources close. Its deterministic lexical
cleanup is observable even when the resources are only tracing stand-ins.

## Visibility does not combine two separate atomic accesses

The broken counter declares volatile int value. Two threads each read value into
a local previous, synchronize at a barrier, then write previous+1. Both reads are
forced to occur before either write. Starting from0, both locals are0 and both
writes store1. The final counter is1 after both threads are joined. All volatile
accesses have their language memory semantics; this is not C-style undefined
non-atomic racing used to manufacture a counterexample.

Volatile visibility/ordering does not combine the read and write into one operation.
AtomicInteger.incrementAndGet performs the compound atomic update, yielding2
for the two calls. Alternatively synchronized(monitor) around the whole increment
serializes that critical section and also yields2. Locking only the final assignment
would leave the earlier duplicate reads outside the protected operation.

Thread.start and successful join contribute happens-before ordering; a monitor
unlock orders a later lock on the same monitor, and volatile writes order relevant
later reads. These relations constrain allowed observations rather than prescribing
one physical instruction stream. No single test enumerates the full Java memory
model. The barrier controls this particular lost-update schedule; observed runtime
speed or JIT mode is not the reason the counterexample is correct.

The runPair helper captures worker failures, joins with bounded waits, attempts
interrupt/join cleanup on a timeout and reports an error. It does not promise that
arbitrary user code obeys interruption or that every deadlocked application can
be recovered inside the same process. The outer runner also bounds execution.

## Compile, execute and inspect a lower layer

```sh
python3 programming-languages-mastery/10-java/units/objects-resources-threads/run.py
```

The runner uses java com.sun.tools.javac.Main when the compiler module is present,
even if the javac launcher is absent. It compiles with --release17 and -Xlint:all
into a temporary directory, executes ordinary and -Xint interpreter modes, then
uses javap through jdk.jdeps to inspect Packet bytecode. A Java runtime without the
compiler module remains BLOCKED; the script never treats a version string as a
successful compilation.

Actual OpenJDK17.0.20 evidence is in [observed.json](evidence/observed.json): both
modes printed checks=15, the reverse cleanup trace, and volatile_split:1,
atomic:2,monitor:2. Disassembly exposed arraylength checks and clone calls.
Bytecode is not final native assembly; -Xint versus mixed mode agreement supplies
no throughput, GC-pause or all-optimizer proof.

Build in milestones: reproduce aliasing; establish constructor and accessor
ownership; derive the cleanup trace including suppressed failures; force the
split volatile schedule; repair the whole update; inspect bytecode; reconstruct
from memory. Attempt [practice](EXERCISES.md), [hints](HINTS.md) and
[solutions](SOLUTIONS.md) in order. [Sources](SOURCES.md) identify exact official
language/API scopes. Broad JVM layout, class loading, GC/JIT, ABI, framework and
production concurrency instruction remains unfinished.
