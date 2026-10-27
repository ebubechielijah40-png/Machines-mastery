# OS mechanisms: execution, scheduling, mappings and descriptors

This is an original connected unit with runnable models and actual local OS
observations. It follows [the compiled-program investigation](../04-computer-systems/compile-link/README.md).
It does not implement a kernel. The distinction matters: our scheduling/page
models specify hypothetical rules, while descriptor/subprocess experiments ask
what the running host actually does. Sources and their inspected scopes are in
[SOURCES](SOURCES.md); exercises and solutions are separate.

## 1. A program is not its execution

An executable file describes code/data to load. A running process additionally
has an instruction position, registers, mappings, open resources and lifecycle.
Many processes can run the same executable while holding different state. A
thread is an execution stream; threads in one process commonly share its address
space, making some communication cheap and some races possible. A single CPU
core executes only one selected stream at an instant in our simple model;
interleaving creates concurrency without requiring simultaneous execution.

A context switch preserves one runnable stream's execution state and restores
another's. A scheduling policy decides which eligible stream to select; the
mechanism performs that selection's necessary state transition. These are
separate questions. A timer may force a running program to give up the processor,
while I/O may cause it to block voluntarily. A blocked process is not ready merely
because its priority is high: its awaited condition must first become available.

For this unit use four lifecycle states: NEW before arrival, READY waiting for
CPU, RUNNING receiving CPU service and DONE after its declared burst completes.
A real OS also manages blocked states, exceptions, multiple cores and much more.
Our simulator deliberately has one CPU, fixed integer service requirements and
no I/O. Do not draw a production scheduler from a queue data structure alone.

## 2. Scheduling is a tradeoff between explicitly defined quantities

Let job i arrive at A_i, first run at S_i, and finish at F_i. Its required useful
CPU service is B_i. Under this no-I/O model:

\[
R_i=S_i-A_i,\quad T_i=F_i-A_i,\quad W_i=T_i-B_i.
\]

Response R measures delay until first service, turnaround T measures delay until
completion, and waiting W measures time not receiving useful CPU service. Their
units are simulation ticks. A tick is not automatically one second of host time.
A context-switch cost contributes to elapsed/waiting time, not job service.
These definitions agree with the inspected original OSTEP chapter [OS-SCHED];
our workload and calculations below are independently constructed.

Consider A(arrival0,burst5), B(1,2), C(2,1).

**FCFS:** arrivals join a FIFO queue; the running job finishes before another
starts. Timeline: A[0,5), B[5,7), C[7,8). Responses are0,4,5; turnarounds5,6,6;
waits0,4,5. The mean turnaround is17/3≈5.667 ticks. C is short but waits behind
work already selected. This is not an implementation error; it follows the rule.

**Round robin with quantum2:** each selected job runs for min(2,remaining). At
slice end, all arrivals through that instant enter the queue before an unfinished
current job rejoins. Timeline: A[0,2), B[2,4), C[4,5), A[5,7), A[7,8). Responses
are0,1,2; turnarounds8,3,3; waits3,1,2. Mean response improves to1 tick; A finishes
later. Consecutive slices of A occur when no competing work is ready.

Why specify the boundary order? B and C arrived while A ran. Requeueing A ahead
of them changes the schedule and reported fairness. “Round robin” without an
arrival/tie convention is insufficient to reproduce an exact trace. Equal
arrival times preserve input order in our implementation. Real systems often
have additional priority/CPU-affinity/wakeup rules.

For an idle period, the simulator jumps to the next arrival and records an IDLE
interval; it does not spend host CPU time waiting one tick at a time. First
service cannot precede arrival. Useful executed ticks for each job must equal
its declared burst exactly. The timeline partitions elapsed simulated time into
useful service, idle intervals and modeled switch cost. These conservation checks
are stronger than comparing only an average which might conceal a lost job.

## 3. Shorter quanta are not free

Suppose equal-length jobs repeatedly consume a quantum q and a switch costs c.
During a typical alternating cycle, useful fraction is approximately q/(q+c),
provided enough ready work keeps switches occurring. For q=1,c=1 that fraction
is1/2; for q=8,c=1 it is8/9. This is a model estimate, not a claim that a real
context switch always has constant cost. Caches, TLBs, predictor state and the
workload can change actual cost [OS-SCHED §7.7].

Our controlled sweep keeps three jobs with burst8 and varies q=1,2,4,8 with c=1.
Actual **model outputs** elapsed47,35,29,26 ticks are stored in
[evidence/observed.json](evidence/observed.json). Every run performs24 useful
job ticks; the difference is the modeled switch intervals. No initial switch is
charged; a change between different jobs with no idle gap incurs c. A single
job never pays a switch merely for continuing through another quantum.

This sweep supports the implemented cost accounting. It does not measure Linux
scheduling overhead. To measure that separately, define a real workload, timing
instrument, repetition count, affinity/noise controls and a meaningful baseline.
Do not label a Python list operation a hardware context switch.

Shortest-job-first motivates a different objective. If two jobs of lengths a≤b
are both ready at zero, executing a then b gives finish-sum2a+b; b then a gives
2b+a. The first is no larger because their difference is b−a≥0. Repeatedly
exchanging adjacent inverted pairs explains why ascending burst order minimizes
mean completion for known lengths, simultaneous arrivals, no overhead and no
preemption. Those restrictive premises are part of the argument. Unknown future
arrivals, I/O, starvation concerns or priorities can invalidate that choice.
We do not call this proof a production scheduling policy.

## 4. Virtual addresses let the same number mean different storage

If two programs both access virtual address0x2d, they need not access the same
physical location. Address translation adds a mapping context. Divide a virtual
address into a virtual page number (VPN) and an offset. For page size P:

\[
VPN=\lfloor VA/P\rfloor,\quad offset=VA\bmod P,\quad
PA=PFN\,P+offset.
\]

P must be explicit. With16-byte pages, VA0x2d=45 gives VPN2 and offset13. Map
VPN2→physical frame7: base7×16=112; physical address125=0x7d. The offset is
preserved because it selects a byte inside the mapped page. Confusing a page
number with a byte address creates a factor-of-P error.

Our address space has eight VA bits, partitioned as two directory bits, two
leaf-index bits and four offset bits. VPN2 is binary0010: directory00, leaf10.
Only used lower-level tables are allocated in the model. Real Linux page tables
are architecture-dependent hierarchies; the inspected kernel documentation
explains why sparse regions can avoid allocating all leaf mappings [OS-PAGES].
Our two-level,16-byte example is a teaching geometry, not Linux's page format.

Each model entry stores frame number, permissions, whether user-mode access is
allowed, and accessed/dirty flags. Translation checks the declared access:

1. Validate the virtual address and requested r/w/x operation.
2. Find a cached translation or walk directory/leaf indices.
3. If no mapping exists, raise NOT_PRESENT.
4. If permissions/user mode prohibit the access, raise PROTECTION.
5. Otherwise mark accessed; a successful write also marks dirty.
6. Combine frame base and offset and return the physical address.

A page fault is a control transfer requiring handling, not always proof of a bug.
A real kernel might allocate a page, implement copy-on-write, load data or reject
an invalid access. Our Fault exception deliberately performs none of those
repairs; callers must distinguish absence from protection failure. Mapping a
read-only page and requesting a write must not succeed merely because the address
translation was cached.

## 5. A TLB is cached authority as well as cached arithmetic

The model uses a fully associative LRU cache of VPN→entry, capacity2 by default.
A cache hit avoids the model table lookup, but still checks permissions. After
mapping VPN2 to frame7, the first0x2d read misses and the next read in the page
hits. Remapping VPN2 to frame9 invalidates that cache entry; the next0x2d access
must return9×16+13=157. A stale result125 would violate the current mapping.

In a real multicore system, remapping while other processors retain old
translations requires a coherence/invalidation protocol. A per-object dictionary
in our single-threaded model does not implement TLB shootdown, ASIDs, PCIDs,
huge-page rules or hardware memory ordering. These are explicit next topics,
not details that can be assumed correct because small address arithmetic passes.

Two model AddressSpace objects have separate tables/caches. One can map VPN0 to
frame3, another to frame20; their identical virtual addresses resolve differently.
Aliasing can also be intentional: multiple mappings can name the same frame.
Isolation depends on which mappings/permissions the privileged system installs,
not on the hexadecimal spelling of an address.

## 6. Descriptors are references, not the resource itself

A file descriptor is a process-local integer referring to an OS-managed open
resource. Duplicating it creates another reference, not an independent rewinded
file. The inspected Linux dup manual states that duplicated descriptors share
an open-file description and offset [OS-DUP]. A separate open generally obtains
its own description/offset.

**Actual local observation:** an owned temporary file contains `abcdef`.
Read2 bytes from the original descriptor→`ab`; read2 from its duplicate→`cd`;
read2 from a separately opened descriptor→`ab`. The shared original offset is4.
This discriminates “copied handle, shared position” from “independent file
position.” It does not prove every resource is seekable; pipes are not regular
files and do not support an ordinary file-position model.

A pipe has a read end and a write end. It transports bytes, without preserving
application message boundaries [OS-PIPE]. If it is empty while some writer
reference remains open, a blocking read waits; a nonblocking read can report
would-block. After every writer reference is closed and buffered data consumed,
read returns EOF. Closing one duplicate writer is insufficient.

The experiment creates a pipe, duplicates the writer, closes the first writer
and performs a nonblocking read. It observed would-block. After closing the last
writer it observed empty bytes/EOF. This is a real host observation, explicitly
separate from the scheduling/MMU simulations. The [shell project](../projects-guided/p02-shell/README.md)
uses exactly this lifetime rule: the parent closes pipe ends it no longer needs,
so its own references do not prevent downstream EOF.

## 7. Starting another program and waiting for it

A process-creation API starts a child execution; exec-style operations replace a
process's program image [OS-EXEC]. Replacing an image and creating a process are
not synonyms. Python's subprocess API exposes a portable parent/child interface;
its implementation can use platform-specific spawn mechanisms. Our observation
uses that API rather than claiming to rebuild fork/exec inside Python.

The actual child prints its requested temporary working directory and exits7.
The parent records output/return code and observes its own current directory
unchanged. A return code0 is a convention for success, not an interpretation of
all possible child outputs. The shell project retains every pipeline stage's
code because the last command can succeed while an earlier one fails.

When stdout/stderr are pipes, waiting without draining output can deadlock:
child waits for buffer space, parent waits for child completion. The official
subprocess documentation describes this boundary [OS-SUBPROCESS]. Our mini runner
uses disk-backed capture for final stdout/stderr, starts all pipeline children
before waiting and closes parent duplicates. This avoids that particular bounded
pipe-wait failure but introduces disk-resource limits. It is not a safe remote
code-execution service.

## 8. Guided investigation and assessment

From repository root, Python3.10+ standard library:

```sh
python3 -m unittest discover -s 05-operating-systems/code -v
python3 05-operating-systems/code/experiment.py
```

Milestones: derive both three-job traces; implement service accounting; add a
switch cost with explicit event ordering; derive all address fields; implement
mapping/protection and cache invalidation; run owned descriptor/subprocess
observations; then connect them in [the OS project](../projects-guided/p05-mini-kernel-labs/README.md).

The [experiment protocol](EXPERIMENTS.md) records hypotheses, controlled variables,
instrumentation, actual observations, alternative explanations and limits.
Attempt [EXERCISES](EXERCISES.md), consult [HINTS](HINTS.md), then
[SOLUTIONS](SOLUTIONS.md). The domain remains PARTIAL: this unit does not supply
complete synchronization, kernel privilege, filesystem, driver, virtualization
or multicore implementations. [WAL recovery](../projects-guided/p07-storage-engine/README.md)
provides a next storage/recovery mechanism, not a filesystem implementation.
