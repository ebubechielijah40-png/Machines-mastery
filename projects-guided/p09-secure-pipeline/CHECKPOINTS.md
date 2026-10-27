# Security checkpoints

Use A0–A8 in the [build guide](README.md). Demonstrate each result with an independent input or attack mutation.

- Strict bounded schema rejects duplicates, booleans where integers are required, unexpected fields and wrong units.
- Manual HMAC construction matches the RFC4231 independent vector; production-path authentication uses stdlib.
- Valid tag on forbidden stream rejects; replay/out-of-order rejects without consuming next sequence.
- Exact25001/1000 output and transform version are bound in the processor entry.
- Output mutation and reordering reject; every partial final-line cut fails closed.
- A complete valid prefix opens without a trusted tip and rejects against the former final tip.
- Fsync failure poisons the object; reopening resolves observed bytes before a retry.
- A false correctly tagged synthetic measurement is accepted, demonstrating the truth boundary.
- Reconstruct the invariant without notes and state every unimplemented authority/durability feature.
