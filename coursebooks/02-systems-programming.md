# Systems Programming — from source contracts to OS state

A running program connects several different machines: a language's abstract
rules, a compiler/linker's artifacts, an instruction set, and an operating
system's resource state. A useful systems programmer can identify which layer
owns a failure and design an experiment at that layer. This original coursebook
supplies a connected route through executable repository units; it does not
claim to reconstruct every chapter of an external book or complete every area
of systems programming.

Use Python 3.12+ for the models and a C11 compiler for the C builds. GNU nm,
objdump and readelf enable the recorded object investigation. The bounded
examples run locally without root access or extra packages. Each chapter has
an entry question, a worked bridge, an implementation and a checkable exit.
Keep each unit's solutions closed until attempting its exercises.

## 1. A value, a byte and a contract

Entry question: why can the same address-looking number be safe in one context
and invalid in another? A number alone says neither which object it designates
nor which operations are permitted. A C pointer-length interface adds part of
that missing contract: the caller supplies a region that remains alive, with at
least n readable bytes; the function promises how many it will read and how it
will report failure. The caller cannot make an invalid region valid merely by
supplying a convenient n.

Start with [the C parser unit](../programming-languages-mastery/01-c/units/01-byte-parser/LESSON.md),
then [the compile/link lesson](../04-computer-systems/compile-link/README.md).
The latter implements `sum_bytes(data, length, output)` without hiding the loop
in a library. For bytes 3,5,7, the local state moves 0 → 3 → 8 → 15. The loop
invariant is that after i iterations, total equals the sum of the first i
bytes, and no output has yet been published. A null output is rejected. A null
data pointer is allowed only for length zero, where the loop reads nothing.

Publishing only after validation makes failure atomic with respect to the
output: rejection leaves its previous value unchanged. This does not create
transactional isolation between threads; it is a sequential function contract.
Distinguish those meanings of “atomic.” Signed `3*x+y` also needs a range
precondition, even if the current machine instruction happens to wrap. The C
abstract contract and one observed instruction are different evidence layers.

Exit: explain zero length and failure preservation, reconstruct the loop,
and write a counterexample to a function that reads `data[0]` before checking
length. The [separate exercises](../04-computer-systems/compile-link/EXERCISES.md)
require these explanations before transfer to another byte mechanism.

## 2. Why compiling is not linking

Suppose main calls `sum_bytes`, while its definition lives in sum.c. Compiling
main.c can succeed because the header supplies a declaration and type contract.
The resulting object still contains an unresolved symbol and relocation work.
A declaration is enough to compile the caller; it is not the implementation
needed to finish the executable.

The [actual toolchain investigation](../04-computer-systems/compile-link/run.py)
compiles main.c and sum.c separately at O0 and O2, records symbols/disassembly/
relocations, deliberately attempts the incomplete link, then links both and
runs the result. The missing-definition failure is expected evidence. A failed
compiler command caused by a missing semicolon would be an entirely different
failure and would not satisfy that experiment.

A relocation is deferred address-dependent work associated with an artifact
location and referenced symbol. In the recorded x86-64 caller, readelf exposes
entries referring to sum_bytes, affine, a counter and the output routine. Their
precise names/types belong to the observed toolchain. The formal ELF/psABI
sources were inaccessible in that run, so the lesson explicitly avoids claiming
a complete ABI specification reconstruction.

Exit: identify the tool output that distinguishes a missing declaration,
missing definition and runtime failure. Rebuild without one object, predict
the failing stage, and account for an external runtime symbol rather than
assuming every U entry is a repository bug.

## 3. Descend to instructions, then return to semantics

On the recorded machine, optimized `affine(4,5)` computes 3×4+5 with an address-
arithmetic instruction followed by addition; no memory read is implied by that
use of the instruction. The mathematical result is 17. The local disassembly
shows which registers this compiler chose for that call contract; it does not
establish every platform's calling convention.

Optimization can remove apparent source structure while preserving required
observable behavior for valid inputs. A variable need not occupy a permanent
stack slot just because it has a source name. Conversely, observing a stack
slot in one O0 build does not prove that “C variables live on the stack.”
Compare actual O0/O2 output and articulate what stays invariant: the accepted
input/output behavior under the function's stated preconditions.

Exit: point to the instruction that contributes 3x, explain where y enters,
and identify a statement you cannot infer from this short trace, such as cache
latency, complete stack-unwinding behavior or all ABI rules. The lesson's
[source map](../04-computer-systems/compile-link/SOURCES.md) records inspected
resources and unavailable evidence separately.

## 4. Allocation is an ownership model over intervals

The [arena project](../projects-guided/p04-memory-allocator/README.md) supplies
256 byte-buffer bytes and explicit metadata. It turns an implicit question
“is this address free?” into inspectable intervals with used/free states.
Request 7 rounds to 8; request 9 rounds to 16. Allocating them reserves `[0,8)`
and `[8,24)`. The remaining interval `[24,256)` is free.

The partition invariant requires ordered, contiguous, positive-size blocks
covering the whole arena, with no adjacent free intervals after coalescing.
This is stronger than a total-size sum. If a bug creates an eight-byte gap and
an eight-byte overlap, the sum remains 256 while two owners can alias bytes.
Tests therefore retain independent live intervals and payload tags as well as
checking allocator metadata.

Releasing a lease changes logical ownership, not the C lifetime of the declared
backing array. Stale addresses can alias later allocations. Eight-byte alignment
does not make the unsigned-character array interchangeable with malloc's
allocated storage for every C type. These distinctions prevent the model from
teaching an incorrect general allocator contract.

Exit: derive split/coalesce preservation, demonstrate 128 free bytes with no
16-byte hole, and interpret [actual snapshots](../projects-guided/p04-memory-allocator/evidence/observed.json).
Then reconstruct from the header and tests without copying arena.c. System
allocation, typed storage and concurrency remain a later project stage.

## 5. Share execution time without losing work

An OS scheduling model needs arrivals, remaining work, ready state, a selection
rule and accounting. The [OS guide](../05-operating-systems/SELF_CONTAINED_GUIDE.md)
derives these before introducing metrics. For A(0,5), B(1,2), C(2,1), round robin
with q=2 runs A 0–2, B 2–4, C 4–5, A 5–7, A 7–8. A waits three ticks despite
starting immediately; response and waiting measure different things.

Turnaround is finish minus arrival. In the no-I/O model it is service plus
waiting, so waiting is turnaround minus service. Useful service must total
8 no matter how the queue is ordered. With switching overhead, elapsed time
can exceed 8 while useful service remains 8. Inspect the timeline partition
rather than optimizing a single aggregate number.

The [kernel workbench](../projects-guided/p05-mini-kernel-labs/README.md) makes
these transition rules reproducible JSON inputs and outputs. Its raw-input
hash identifies bytes; it does not certify the model. An actual execution of
the Python scheduler is still a model run, not a host scheduling measurement.

Exit: derive both FCFS/RR metrics, change one arrival boundary rule and produce
a counterexample, then use conservation tests to detect lost or duplicated
service. A real scheduler adds interrupts, unknown future service, I/O and
multiple CPUs; none follows automatically from passing this model.

## 6. Translation is also access authority

Divide virtual address 45 by page size 16: VPN 2, offset 13. Mapping VPN 2 to
physical frame 7 yields PA 125. Only page identity changes; offset stays 13.
The [translator](../05-operating-systems/code/models.py) adds sparse two-level
mapping, read/write/execute permissions, user access and an LRU translation cache.

A TLB miss asks for a table lookup. A missing mapping is a NOT_PRESENT fault;
a disallowed access to an existing mapping is PROTECTION. These are distinct
branches. Cached translations carry authority, so a hit cannot skip permission
checks. Mapping changes invalidate affected cached entries through the supported
API. Real multicore invalidation requires further protocols absent here.

Exit: derive a new 10-bit/32-byte-page geometry, test all original 256 virtual
addresses against a direct oracle, and demonstrate a stale-cache bug in a
separate learner copy. The workbench's access traces make its limit visible:
there is no payload RAM, instruction execution or actual CPU privilege change.

## 7. Compose actual processes by accounting for handles

The [shell project](../projects-guided/p02-shell/README.md) now crosses to real
host processes. A character parser distinguishes a quoted `|` from an operator
and retains `''` as an empty argument. The runner passes argument vectors directly
to Popen, connects pipes, starts all children, waits and closes what it owns.

A finite pipe exposes a dependency: a large producer can wait for space while
a parent waits for producer exit. If the consumer has not started, neither can
make progress. Launching all stages before waiting removes that dependency.
EOF is also a resource-state event: every writer must close, rather than a
special byte appearing in the stream. The [actual host observations](../05-operating-systems/EXPERIMENTS.md)
compare duplicate/open offsets, pipe EOF and child directory/status.

A `cd` child cannot update the state used by future sibling launches. The
teaching Shell keeps a logical cwd in its own object and passes it per launch.
A failure halfway through creating a pipeline must clean up the children that
already exist. These ownership paths are part of correctness, not optional
polish after the happy path works.

Exit: test literal metacharacters, a large real pipeline, producer failure,
missing second-stage executable and timeout; preserve all stage statuses.
The current reference handles direct children, not a descendant sandbox or
interactive terminal job control. Its output memory cap is checked after
execution and does not bound temporary disk growth.

## 8. Reconstruct a coherent investigation

Choose a byte-processing command with two translation units and compose it
with a counting consumer. Before running it, predict its symbol dependencies,
byte/output contract, allocation leases, process state and descriptor ownership.
Inject one failure at a time: missing object, bad input length in a controlled
learner copy, allocation exhaustion, failed producer and retained pipe writer.
For each, name the observable symptom and the layer whose invariant failed.
Do not intentionally invoke unsafe memory accesses in the reference tests.

Submit source, exact build/run commands, raw results, independent assertions,
an explanation of each failure and a fresh reconstruction without notes.
[The systems check runner](../05-operating-systems/run_checks.py) executes the
bounded reference suites; its report is evidence of those commands only.

This coursebook's developed route is STRONG within its stated scope. The wider
systems course remains PARTIAL: formal ABI reconstruction, caches/performance,
concurrency and memory ordering, filesystems, networking, drivers, actual kernel
boot and production diagnostics need additional substantive units. The route
ends with an honest frontier rather than silently assigning mastery to those
unbuilt mechanisms.
