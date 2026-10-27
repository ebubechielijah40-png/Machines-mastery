# Actual local pipeline experiments

Run `python projects-guided/p02-shell/code/experiment.py` from the repository
root. It emits JSON containing environment, exact argv vectors, input size,
output, status, and elapsed observation. Committed data are in
[evidence/observed.json](evidence/observed.json); values were produced by actual
local child processes. Elapsed time is a host observation, not a benchmark.

## P1: Does pipeline launch order matter under backpressure?

Question: can a large producer finish when its consumer reads only after the
producer exits? Hypothesis: with finite pipes, sequential wait-before-launch
can block; launching all stages permits progress. Hold interpreter, payload,
and consumer fixed. Use 200,000 literal bytes, then count at the second stage.
The reference launches both before waiting. Measure output count, both codes,
and wall time; expect `200000\n` and `(0, 0)`. The committed run records the
actual successful path. It does not execute an unbounded hanging variant.
For the counterfactual, write a separate variant with a 0.2-second timeout and
mandatory cleanup, then preserve that failure record separately. Do not label
the unexecuted prediction a measurement.

Alternative explanation for success: a large pipe could absorb the payload.
Repeat with a larger but explicitly bounded payload and inspect the OS pipe
capacity if testing that explanation. Temporary disk throughput and host load
can alter elapsed time, so a single run cannot compare scheduler performance.

## P2: Is a shell metacharacter automatically executable syntax?

Pass `; $(unexecuted) *` as one argv item to a Python program that prints it and
exits 7. Control the executable and program text. Measure exact output and
status. Expect a literal line and code 7. The observed record includes both.
This supports absence of a second shell parser on this path; it does not imply
that every selected program treats every argument as harmless data.

## P3: Which directory changes?

Create an owned temporary child directory. Construct a Shell rooted at its
parent, execute `cd child`, then launch a child that prints cwd. Measure host
cwd before/after, Shell cwd, and child output. The run records a true unchanged
host cwd and a child directory matching Shell state. Temporary paths will vary.
This establishes the implementation's object-state behavior, not a general
rule that a process can never alter another process by any mechanism.

Follow-up: inject a producer exit 7 before EOF, compare last-stage-only and
all-stage success policies, and add a third transformation stage. Record every
argv and distinguish actual output from expected output in your lab notebook.
