# Synchronization: protect a transition, then wait for a predicate

The [scheduler lesson](../SELF_CONTAINED_GUIDE.md) explains how executions can
interleave. That alone does not make shared state safe. This original unit adds
an inspectable two-thread transition model, a condition-wait model, and actual
C11 thread experiments. Study the [C lifetime and toolchain lesson](../../04-computer-systems/compile-link/README.md)
first: C undefined behavior must not be confused with a permitted toy outcome.

This is a STRONG bounded synchronization build. It does not implement a
hardware mutex, model weak memory, prove fairness, or complete concurrency as
a domain. [SOURCES.md](SOURCES.md) identifies inspected primary scopes.
Attempt [exercises](EXERCISES.md) before [hints](HINTS.md) and
[solutions](SOLUTIONS.md).

## 1. Two correct local computations can produce a wrong shared answer

Two workers each intend to increment a counter initially zero. Decompose one
increment into three model transitions:

1. `load`: copy shared x to this worker's local register r.
2. `add`: replace its local r with r + 1.
3. `store`: replace x with that worker's r.

Each transition is indivisible in this **sequentially consistent model**.
Local state belongs to one worker; only x is shared. The intended invariant at
a completed operation boundary is `x = number of completed increments`.

| Step | Worker | Action | Local A | Local B | Shared x |
| --- | --- | --- | --- | --- | --- |
| 0 | — | initial | 0 | 0 | 0 |
| 1 | A | load | 0 | 0 | 0 |
| 2 | B | load | 0 | 0 | 0 |
| 3 | A | add | 1 | 0 | 0 |
| 4 | B | add | 1 | 1 | 0 |
| 5 | A | store | 1 | 1 | 1 |
| 6 | B | store | 1 | 1 | 1 |

Nothing tore a byte and each worker added correctly. The algorithm lost an
update because its read and write were separate shared-state operations.
Locking only `store` still permits both loads to observe zero, followed by two
serialized stores of one. It protects individual writes without protecting the
read-modify-write invariant.

## 2. Enumerate rather than wait for a lucky failure

Both workers preserve load-before-add-before-store. Select three of six total
positions for A; B occupies the rest. There are

\[
\binom{6}{3} = 6!/(3!3!) = 20
\]

possible order-preserving interleavings. A final value of two requires one
worker's store before the other's load. That permits only the two fully serial
orders. The other 18 end at one. The model enumerates every path and tests the
histogram against a separate combinations-based unroller. It preserves a
counterexample trace rather than relying on random timing.

**18/20 is not an observed probability.** An OS scheduler does not choose these
paths uniformly, and one model transition is not a fixed-duration machine
instruction. Path counts describe this finite transition system only.

`whole_lock` adds atomic acquire before load and release after store. Only one
worker owns the critical section at a time. The second must therefore load the
first worker's completed value, so the final value is two. The model's lock
acquire is a primitive state transition; hardware atomic instructions, OS wait
queues, cache coherence and contention policy are not implemented underneath it.

`fetch_add` instead makes the entire increment one shared transition. It also
ends at two. This illustrates the distinction between an atomic **operation**
and an atomic **variable**: separate atomic loads and stores do not combine
into an indivisible transaction.

## 3. A defined C experiment makes the same distinction observable

[threads.c](code/threads.c) uses C11 atomic objects, not unsynchronized ordinary
integers, for the split case. Each worker atomically loads the counter, records
its loaded value, announces readiness and waits on an atomic gate. Main opens
the gate only after both loads have occurred. Both loaded values are therefore
zero before either store. Each worker then atomically stores its local value
plus one. The observed final value is one by construction.

The other cases use `atomic_fetch_add`, or a mutex covering an ordinary counter's
whole increment. Main joins both workers before reading their recorded data.
All atomic operations here use the default sequentially consistent ordering;
we are not testing relaxed ordering. The ordinary mutex-protected counter is
accessed under the same mutex, and the final read occurs after joins.

A C program with two unsynchronized threads updating a plain `int` would have
a C data race and undefined behavior. Its possible behavior cannot correctly
be characterized merely as the 20 paths above. `volatile` would not repair that
contract. The real split experiment deliberately avoids this mistake while
retaining the logical lost-update failure.

Run from the repository root, with Python 3.12+, a C11 compiler, C11 threads and
GCC/Clang-style sanitizer support:

```bash
python -m unittest discover -s 05-operating-systems/synchronization/code -p 'test_*.py' -v
python 05-operating-systems/synchronization/code/experiment.py
```

The harness compiles at O0, O2 and O1 with UBSan using `-pthread`, then executes
the real programs. Missing C11 thread or sanitizer support is a scoped blocker,
not permission to claim all runs passed. The [raw record](evidence/observed.json)
separates model paths from actual compiler/process output.

## 4. Mutual exclusion does not answer “when may I proceed?”

A one-slot buffer has state `full` and `slot`. A consumer needs `full == true`;
a producer needs `full == false`. A mutex makes checking/changing those fields
consistent. A consumer that sleeps while holding the mutex prevents a producer
from filling the slot. Releasing it and then separately going to sleep creates
a different race:

1. Consumer checks empty while holding the mutex.
2. Consumer releases it but has not registered as a waiter.
3. Producer fills the slot and notifies; no waiter exists, so no notification
   is saved as a future credit.
4. Consumer registers and blocks. The item is present, but no future producer
   action remains to wake it.

This is a lost wakeup, a progress failure. The notification is not the data;
the persistent predicate is. A condition wait must release the mutex and
register waiting as one coordinated operation relative to the producer's
locked state change. On return it reacquires the mutex before the caller
examines protected state again.

## 5. Wake means recheck, not permission to consume

[conditions.py](code/conditions.py) gives the consumer explicit states:
lock → check → wait/consume → unlock. Producer states are acquire → put →
notify → release. In the correct variant, waiting atomically releases/registers,
and waking leads to reacquire and **check again**. This model optionally permits
one wake without a predicate change. It is a deliberately bounded robustness
assumption, not an observation that the local C runtime spontaneously woke.

Replacing the recheck with unconditional consume after waking fails when that
optional event occurs: the consumer attempts to remove an item from an empty
buffer. This is a safety failure. Splitting release and registration instead
produces a blocked terminal state with `full == true`: a liveness failure.
They are different bugs, with different counterexample traces.

A wakeup also need not grant an item in a larger system: another consumer may
acquire the mutex first and consume it. The robust pattern is to hold the mutex,
loop while the predicate is false, wait, then recheck on every return. This unit
models one producer and one consumer; multiple consumers are a transfer task,
not an already enumerated claim.

## 6. Actual producer/consumer build

[condition.c](code/condition.c) transports values 1 through 100 through one slot.
Both workers use the same mutex for all slot/full/stopping accesses. Producer
waits while full; consumer waits while empty. After changing the predicate they
broadcast on one condition variable. Broadcast wakes all current waiters; the
while checks decide whether each may proceed. Using one broad notification is
simple at this size but can cause unnecessary wakeups when many workers exist.

The consumer asserts the exact next value, not just the final sum: an equal sum
could hide duplication and omission. It also records sum 5050 and verifies the
buffer is empty after both joins. Wait counts are actual observations that can
vary with host scheduling. They do not count every context switch or prove a
particular wakeup was spontaneous.

Initialization and thread creation can fail. The program stops a partially
created pair under the mutex, broadcasts so an existing waiter can leave,
joins created threads, and destroys resources only after use. Unrecoverable
thread API errors abort the experiment rather than continuing with uncertain
synchronization state. The outer harness imposes a process timeout. Neither
finite enumeration nor these runs prove progress under an unfair scheduler.

## Build gates and evidence standard

| Gate | Learner artifact | Evidence required |
| --- | --- | --- |
| A0 | State/invariant and hand lost-update trace | Correct final one with both locals shown |
| A1 | Independent schedule enumeration | 20 legal split paths, explained serial outcomes |
| A2 | Whole-lock and store-only variants | Invariant argument and store-only counterexample |
| A3 | Defined C split/RMW/mutex experiment | Actual raw outputs, flags, loaded values and joins |
| A4 | Condition predicate and atomic wait transitions | Separate empty-consume and lost-wakeup traces |
| A5 | One-slot C buffer | Exact sequence, count, sum, final-empty tests |
| A6 | Reconstruction without notes | Fresh models plus a transfer case and independent expected trace |

[EXPERIMENTS.md](EXPERIMENTS.md) supplies controlled protocols and interpretation.
Weak memory, lock-free reclamation, scheduler fairness, priority inversion,
condition cancellation and multiprocessor performance remain unbuilt. This
unit supplies a mechanism bridge to them, not completion evidence for them.
