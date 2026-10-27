# Exercises: authenticated provenance

1. Hand-trace a valid producer's seq1 on room, seq2 on room, replay of seq1, and seq3 on forbidden outside. Record count, last-sequence, tip-change and output-change after each attempt.
2. Compute the first inner/outer pad bytes for keys beginning `00 ff 0b`. Explain the >64-byte key branch. Test the manual construction using an independently specified vector, not the pipeline's own generated tag.
3. Construct a mutation that preserves valid JSON but changes units or producer. Why must every semantics-bearing field be bound by the tag? What is the risk of ignoring unknown fields?
4. An implementer checks `record['seq'] == 1` without checking its type. Supply a JSON counterexample exploiting Python's equality rules. Find another schema field needing an exact integer check.
5. Remove the last complete ledger line, then truncate midway through that line. Predict behavior with and without an independently stored latest tip before running either case.
6. Inject an fsync exception after a full write. Explain why a retry using the same sequence may be rejected after reopening. Design an idempotency contract that could return the previous result instead.
7. Identify the trusted identity source for reads in this local model. Design a real boundary where authenticated session identity reaches authorization without taking the principal from an untrusted request field.
8. Reconstruct from memory: canonical record validation, HMAC verification, permission check, next-sequence check, exact transform, authenticated append and reopen validation. Submit independent vectors and a mutation matrix.
9. Transfer: sign a microscopy image digest and metadata. List three biological or physical claims that remain unsupported even when the signature and hash verify.
