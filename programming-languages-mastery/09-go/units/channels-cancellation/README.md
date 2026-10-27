# Go: channels transfer values; cancellation must release blocked work

A worker pool can compute every answer correctly and still leak goroutines when
the consumer stops reading. This unit derives an ownership and shutdown contract
for a finite indexed stream. Read [Python aliases](../../../08-python/units/objects-and-aliases/README.md),
[shared-state synchronization](../../../../05-operating-systems/synchronization/README.md)
and [stream lifecycle](../../../../06-networking/stream-boundaries/LESSON.md) first.
The runnable [pipeline.go](pipeline.go) and [tests](pipeline_test.go) are original;
[primary scopes](SOURCES.md) distinguish language guarantees from observations.

## Syntax needed to read the build

A package groups source files. func declares a function; `[]int64` is a slice of
64-bit signed integers. `value, err := call()` declares local results; an error
value must be handled explicitly. `go func(){...}()` starts a goroutine, whose
lifetime is not automatically joined by the caller. `make(chan T)` creates an
unbuffered channel of values of type T. `channel <- value` sends; `<-channel`
receives. A receive can return `(value, ok)`, with ok=false after a channel has
closed and its buffered data is exhausted. `defer` schedules cleanup when that
function returns. A `select` chooses a ready communication branch, or waits.
Writing the cancellation branch first does not give it priority.

These constructs describe concurrent operations, not one operating-system
thread per goroutine. The runtime schedules them; the tests do not establish
universal fairness, throughput or a specific goroutine-stack size.

## The value crossing a channel can still alias

A slice describes a window onto a backing array: it has length and capacity as
well as access to storage. Copying that value, including sending it through a
channel, does not recursively copy the backing array. In a sequential probe,
send a slice containing[1,2], set its first backing-array element to7, then
receive the slice: the receiver sees7. No concurrent race is needed to expose
this ownership fact.

Capacity matters to append. With length1,capacity2, two appends from the same
original slice can reuse the same second cell; the later append overwrites what
the earlier resulting slice observes. When an append exceeds capacity, it must
use sufficient new storage and copy existing elements; the old backing array
then stops receiving those later mutations. Do not make ownership depend on
whether a particular append happens to grow. Our API explicitly copies the
input before spawning any worker. The caller must avoid concurrent mutation
while that copy itself occurs; copying is not an atomic read of an arbitrarily
changing array.

## Trace the finite pipeline

Start accepts at most8192 inputs,1..16 workers and magnitudes≤10^6. Squaring then
fits int64: the largest result is10^12, below its signed upper bound. Validation
and input snapshot complete before goroutines start. Jobs carry an index and
value; results carry that index and its square. Workers may finish in a different
order, so Squares writes each result into answer[result.Index]. For[3,-2,5],
the ordered answer is[9,4,25], regardless of completion order.

One feeder owns closing jobs. Workers own sending results. A coordinator waits
for feeder plus all workers, then closes Results and Done. No worker closes a
channel that other workers may still send on. The invariant is one accepted job
per original index and, absent cancellation, exactly one result per job. The
collector's count check detects incomplete success instead of silently returning
zero-valued holes. Unbuffered channels bound queued channel values but do not
eliminate the finite input copy, result array or live worker state.

## Cancellation is a communication path, not a magic interrupt

Every potentially blocked send selects between its intended send and ctx.Done().
A worker waiting for a job also selects cancellation. If the consumer stops after
one result, it must cancel and await Done; otherwise remaining workers may block
forever trying to deliver results to a consumer that no longer receives.

Suppose the feeder is blocked sending the next job and a worker is blocked
sending a result. Closing the cancellation signal makes both blocking selects
eligible to return. Their deferred WaitGroup.Done calls release the coordinator,
which closes the output only after all possible senders have exited. Removing
the cancellation branch from either send leaves a distinct shutdown hole.

This does not promise that no result can arrive after cancellation becomes ready.
A select can choose another ready operation. Nor does context cancellation stop
an arbitrary function, undo an external write or guarantee a real-time shutdown
deadline. Here each calculation is bounded, and all communication points observe
cancellation. Squares drains/joins, then returns the context error and discards
partial output; Start exposes a streaming contract whose consumer must manage
its own partial observations.

Channel communication and close/join events also establish ordering needed for
visibility. Merely exiting a goroutine does not give every reader a synchronization
edge. Use the explicit protocol rather than repeatedly checking a shared flag.

## Build and test

```sh
python3 programming-languages-mastery/09-go/units/channels-cancellation/run.py
```

Put a trusted Go toolchain on PATH or supply --compiler or GO. The runner copies
only the three source/module files into a temporary directory, disables automatic
toolchain switching, runs normal tests, race-detector tests and go vet. Actual
[evidence](evidence/observed.json) records Go1.27.3, all9 tests passing in both
modes, and the finite observation. A clean race-detector run only checks executed
paths; it is not proof that every schedule or future change is race-free.

Milestones: write a sequential indexed oracle; implement a feeder and one worker;
add workers without losing index order; reproduce slice aliasing; add cancellation
to every blocking point; stop reading after one result and prove joining; then
rebuild without copying. Attempt [exercises](EXERCISES.md), [hints](HINTS.md) and
[solutions](SOLUTIONS.md) in that order. Broader Go interfaces, runtime/GC,
network cancellation, ABI and deployment instruction remain separate work.
