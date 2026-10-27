# Hints — read after attempting a checkpoint

A1: A word's presence cannot be inferred from its length. Set an `active` flag
when opening quotes, including quotes that contain no characters.

A3: Make a table with parent, producer, and consumer as rows; pipe read/write
handles as columns. Cross out each handle immediately when it is no longer
needed. Launch the consumer before waiting for the producer.

A4: A pipeline is a collection of processes, not one exit code. Keep ordered
process objects and preserve their ordered statuses.

A5: Establish the deadline once with monotonic time. Each wait gets the time
remaining. Cleanup belongs in a path reached after success and after error.

A6: A builtin must mutate the state used by later launches. Passing a per-call
cwd keeps the host's global directory untouched.

Reconstruction: write down invariants before API names: no empty executable,
no parent pipe copy held unnecessarily, every started direct child reaped,
and no output/status pair discarded accidentally. Then choose APIs.
