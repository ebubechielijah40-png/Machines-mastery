# Derive and build the engine

Write each prediction before opening the reference. Keep your attempts under `notes/`; no prepared artifact establishes mastery.

## A0 — expose the loss

Run `code/starter_memory.py`. Add a second key and explain why constructing a new store discards both. Deliver a diagram identifying process memory, OS cache, and persistent storage. Success: you can state which failures each layer survives without assuming a successful file read proves power-loss durability.

## A1 — persist individual operations

Design a binary record for a `put` with a value containing a newline and the character `雪`. Write and decode it without reading the whole file. Deliver a byte-offset table and a round-trip test. Success: lengths count encoded bytes, malformed sizes are bounded, and your reader does not use `eval` or `pickle`.

## A2 — derive batch atomicity

Persist `a=10,b=20`, then attempt one transaction setting `a=9,b=21`. Cut the second transaction after every byte. Predict recovered state before running. Success: no proper prefix exposes either update, and the full second frame exposes both. Explain why each operation must validate before either is applied.

## A3 — distinguish corruption from incomplete output

Flip one payload bit in a complete frame, insert a valid frame after it, and run recovery. Success: corruption is reported at its byte offset; the reader does not skip forward to the later frame. Add tests for unexpected IDs, unknown format version, excessive length, and valid-checksum malformed operations.

## A4 — acknowledgement is an event

Arrange `validate → write → sync → apply memory → acknowledge`. Inject a sync exception after the bytes are written. Success: the live object rejects further commits, while recovery may show the unacknowledged batch. Write the caller protocol you would need for safe retries; the reference does not implement request deduplication.

## A5 — repair deliberately

Open a file with a short final header. Recovery must leave the file unchanged; writing must refuse until an explicit incomplete-tail decision. Success: repair truncates to the recorded valid boundary and a later transaction can be replayed. Preserve the damaged fixture before repair. Explain why complete-frame deletion cannot be diagnosed by this format alone.

## B — independent reconstruction

Close all reference files. Reimplement from your offset table and invariants, then run equivalent tests against it. Use a different internal structure so copying is not mistaken for understanding. Deliver code, test output, failed attempts, and an unaided correctness explanation.

## C — controlled experiment

Run the documented byte-cut and replay-scaling experiment. Deliver your environment, all raw timing samples, units, median calculation, and explanation of why warm-cache replay timing does not measure write durability or physical disk throughput.

## D — extension with a changed requirement

Choose one: add an independently retained expected-last-ID check; design crash-safe compaction; add an idempotency key; or provide actual process-level exclusive locking. First write a failure scenario for the new requirement. Success requires new tests distinguishing your extension from the baseline. Document unimplemented operational concerns instead of relabeling the engine production-ready.

## Evaluation rubric

| Evidence | Ready for bounded project review | Needs correction |
| --- | --- | --- |
| Mechanism | Explains frame boundaries, byte lengths, replay induction and ack order unaided | Only repeats class/function names |
| Correctness | Normal, malformed, all-prefix, short-write and unknown-outcome tests pass | Tests only single-key happy paths |
| Experiment | Predictions, controls, actual outputs and limitations are distinct | Generated predictions are called observations |
| Failure reasoning | Distinguishes incomplete tail, corruption and unacknowledged success | Treats every exception as rollback |
| Transfer | Identifies a new race or failure and tests an extension | Reuses baseline assumptions silently |

Passing this review establishes evidence for this bounded project only. Delayed unaided reconstruction and transfer still require learner work.
