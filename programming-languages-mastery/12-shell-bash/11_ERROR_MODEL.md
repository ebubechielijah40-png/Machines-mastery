# Bash pipeline status is a separate contract

A command reports an exit status independent of what its output looks like.
For `false | true`, default Bash uses the last command's status0, so failure of
the producer is invisible to that single status. Enabling pipefail makes the
pipeline return the rightmost nonzero status, here1. The
[local experiment](units/argument-boundaries/lab.py) executes both forms and stores
[actual observations](units/argument-boundaries/observed.json) under Bash5.2.21.
Local `help set` was inspected to verify this option's documented rule.

Do not infer successful complete processing merely because a consumer prints
something. State whether a wrapper must detect any producer/consumer failure,
then test its status handling. A status is also not an exception automatically
caught by Python or a guarantee that generated files are complete. The build
uses subprocess check=True around controlled successful helpers, while pipeline
failure status is deliberately printed/captured for assertions.

Exercise: replace a producer with an explicitly failing local command and ensure
a downstream consumer can still exit0. Demonstrate the two status outcomes, then
state a recovery policy for partially written output. This unit does not pretend
that set-e, traps, signals and arbitrary shell control-flow exceptions are fully
taught by a one-line option. See [source limits](units/argument-boundaries/SOURCES.md).
