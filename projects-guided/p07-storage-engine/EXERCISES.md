# Assessments — attempt before opening solutions

## Basic understanding

1. Draw the path of one value through Python memory, a write request, the OS cache, and persistent storage. Which of these did a successful `recover()` actually observe?
2. Encode decimal 300 into four big-endian bytes. Why must a UTF-8 payload length use bytes instead of characters?
3. Compute the frame length and next offset for `[("put","a","1")]` starting after the file header. Show intermediate arithmetic.
4. What state follows `put(x,1),put(x,2),delete(y)` when `y` is absent? State the missing-key policy explicitly.
5. State the difference between a complete valid frame and the caller receiving its acknowledgement.

## Application

6. Trace both batches in the lesson. For cuts at bytes 0, 15, 16, 30, 53 and 54 of transaction 2, give the recovered map, valid boundary, and tail policy.
7. A parser validates each operation and immediately applies it. Construct a checksum-valid payload whose final operation is invalid and show the partial-state bug.
8. A caller receives a sync error during a transfer and retries the same logical operation on reopening. Give two possible histories. What extra state would make the retry safe?

## Reasoning and debugging

9. A complete frame has a bad checksum and is followed by a valid frame. Why is scanning forward unsafe? Why does the explicit repair option refuse this file?
10. A colleague deletes the last complete transaction and says recovery proves no data was lost because no corruption is reported. Explain the missing evidence and design one detection mechanism.

## Challenge, experiment, and transfer

11. Without reading the reference, derive a crash-safe compaction protocol. Enumerate interruptions before/after the replacement file is written, synced and installed. Explain directory-entry durability and why merely truncating the old file first fails. Do not claim you implemented this extension.
12. Predict the 55 byte-cut outcomes before running the experiment. Then measure five replay samples each for 100, 1,000 and 10,000 transactions while retaining 100 keys. Report medians and two alternative causes of a nonlinear result.
13. Two writers both recover last ID 8 and append transaction 9. Show at least two failure interleavings. Propose the smallest enforceable ownership contract for the local single-host case, and explain why naming the class `SingleWriter` is insufficient.

Use [hints](HINTS.md) only after saving an attempt; [worked solutions](solutions/EXERCISES.md) are separate.
