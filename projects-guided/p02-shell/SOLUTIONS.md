# Solutions and independent reasoning

## Lexer trace

`prog '' 'x y'|next` becomes `[['prog', '', 'x y'], ['next']]`.
The empty quotes set active but append no character. Closing single quotes
restores unquoted state. The unquoted pipe finishes both the current word and
command. An end-of-input pipe would leave an empty required command and is
rejected. Literal quoted pipes append to the current word.

## Backpressure explanation

Let a finite pipe hold K bytes and producer output exceed K. If the parent
waits before starting the consumer, the producer can block waiting for space;
the parent waits for producer exit; no running participant drains bytes.
Starting the consumer first removes this dependency cycle. Merely increasing K
changes the payload that triggers it. It does not repair the ordering rule.

## Failure and status

For a producer that prints a prefix then exits 7 and a consumer that counts
all bytes and exits zero, a valid runner returns codes `(7, 0)`. Returning only
zero loses an observable failure. A policy such as “any nonzero stage fails”
is reasonable for some batch pipelines but must be specified; it is separate
from process creation and byte transport correctness.

If a second executable is missing, the first child already exists. The
reference enters cleanup, kills it if still running, waits for it, and closes
its stdout. The original launch error remains the caller-visible failure.
A descendant created by that first child is beyond this implementation's
cleanup guarantee.

## Deadline derivation

With m stages and independent per-wait timeout T, worst-case waiting can
approach mT. With one deadline d = start + T, the ith wait uses d − now; the
intended wait budget covers the collection. API overhead, process creation,
and cleanup are outside a hard real-time guarantee, so measured time may
exceed T. A negative/NaN/infinite timeout must be rejected before children start.

## Directory state

`cd` in a child changes that child's cwd. Future siblings inherit or receive
their own cwd; their parent's state has not changed. Here the Shell object
stores the selection and each launch receives it explicitly. A relative path
is resolved against that stored directory, not the host cwd at arbitrary times.

## Transfer: three stages

Use producer `b'abcd'`, uppercase transformer, and length counter. The expected
final bytes are `b'4\n'`, with three zero codes. Parent-held intermediate
streams can close after each downstream process has inherited the read end.
The last output is a temporary file. A meaningful test must also make the
middle stage fail and check its retained code; the same final byte count alone
would not prove that it ran correctly.

## Reconstruction from memory

A passing reconstruction includes the finite grammar, active empty-word state,
ordered child list, shared deadline, ownership cleanup, literal argument test,
large-output test, and a documented limit. Compare behavior rather than line
count with the reference. Reimplementing this in C requires explicit fork/exec
or spawn/error-reporting, dup2, close, and wait handling; Python's lifecycle
wrapper has not taught those C error paths automatically.
