# Build an authenticated provenance pipeline

Build an authorized local pipeline that accepts bounded authenticated observation claims, enforces producer permissions and replay order, transforms units exactly, appends an authenticated history, and verifies history on reopening. The executable mechanism is [pipeline.py](../../security-cryptography-mastery/provenance/pipeline.py); the complete [lesson](../../security-cryptography-mastery/provenance/LESSON.md) derives its design. This milestone project is implemented in a single-writer local scope. Confidentiality, network identity establishment, production filesystem hardening, key lifecycle and concurrent storage remain unimplemented.

Prerequisites are concrete: finish [bounded framing](../../06-networking/stream-boundaries/LESSON.md) and [scientific ingestion](../p08-scientific-pipeline/README.md); explain exact units, input-content identity, a next-sequence invariant and XOR. Tools are Python 3.12 standard library and a local temporary directory. All experiments use public literal demo keys and synthetic records. Do not use those keys or these unreviewed storage mechanisms for actual protected data.

## Architecture and decisions

A producer forms one versioned integer-only record and tags its canonical form. A decoder reconstructs its bytes from length frames. A processor validates the byte budget, strict schema, producer MAC, allowed stream and next per-producer sequence, in that order. It converts milli-Celsius to an exact rational Celsius output. A ledger entry binds the observation, transform/version, derived output, index and previous digest under a separate processor MAC. Reopening verifies from genesis and reconstructs the current snapshot.

This design deliberately distinguishes three questions. A hash identifies bytes; a MAC authenticates them under shared-secret assumptions; a measurement procedure establishes evidence about the physical world. None substitutes for the others. A producer can submit a false but correctly tagged observation. Producer and verifier can both generate producer MACs, so public nonrepudiation is not claimed. Read access takes a principal supplied by a trusted caller; it is not a credential verification system.

A valid history prefix remains valid after complete suffix deletion. The optional `expected_tip` checks a separately trusted final digest. It does not make that external checkpoint durable, fresh or unmodifiable; implementing that trust boundary is further work. A write/fsync exception creates an unknown outcome, so the object poisons itself and requires reopen/reconciliation.

## Derive and build the milestones

Keep learner code separate and predict each result before opening the runnable reference. Use [exercises](../../security-cryptography-mastery/provenance/EXERCISES.md), then the separately stored hints and solutions.

| Stage | Learner task | Observable acceptance |
| --- | --- | --- |
| A0: threat contract | Specify assets, attacker edits/submissions, key holders, caller identity, permitted streams and excluded goals | Classify mutation, replay, false signed measurement and file rollback without conflating them |
| A1: representation | Validate bounded exact fields and canonicalize semantic records | Duplicate keys, bool numerics, unknown units, extra fields and oversize payloads reject |
| A2: authentication | Derive HMAC pads and test the manual construction; use stdlib HMAC in the pipeline | Independent RFC 4231 vector matches; changed record bytes invalidate the tag |
| A3: authorization/order | Add producer-to-stream policy and next per-producer sequence | Correct tag on forbidden stream rejects; replay/out-of-order reject without state advance |
| A4: transformation/history | Preserve exact rational output and chain position; bind all fields with processor MAC | Output substitution and reordering reject on reopen |
| A5: failure recovery | Append fully, sync, then mutate in-memory state; poison on write/sync error | Injected fsync failure leaves uncertain durable outcome; reopening reconstructs bytes rather than guessing |
| A6: rollback investigation | Compare a valid prefix with and without independently retained latest tip | Prefix opens without expected tip and rejects with latest tip |
| A7: connected experiment | Transport a tagged request through three-byte frame fragments and the processor | Exact output is 25001/1000 Celsius; classify every attack probe in actual JSON |
| A8: reconstruction | Rebuild the core path without reference, then swap another learner's test vectors | Explain every trust assumption and demonstrate one guaranteed limitation |

## Run, inspect, and evaluate

From repository root:

```sh
python3 -m unittest discover -s security-cryptography-mastery/provenance -v
python3 security-cryptography-mastery/provenance/experiment.py
```

[Actual observations](../../security-cryptography-mastery/provenance/evidence/observed.json) include framed input, exact output, replay/authorization/tamper rejection, authenticated false claim acceptance, and trusted-tip rollback detection. [Tests](../../security-cryptography-mastery/provenance/evidence/tests.txt) cover every partial cut of the final ledger line, HMAC vector/oracle comparisons, output tampering, snapshots, bounds and injected synchronization failure. They do not simulate actual power loss or establish cryptographic security through trial attacks.

Deliver a threat table, canonical record trace, learner implementation, independent vectors, a mutation/recovery log, trusted-tip design and reconstruction notes. Rubric: representation/authentication 25%, permission/replay invariants 25%, history/recovery correctness 30%, evidence and honest limitations 20%. A solution that calls a valid MAC proof of physical truth or claims a hash chain prevents all deletion does not meet the interpretation criterion.

Safe extensions are historical key/policy versioning, idempotent exact-retry response lookup, an independently protected checkpoint store and transactional multi-writer storage. Each requires fresh failure tests and an updated adversary model. Encryption should use an established authenticated-encryption library and explicit key/nonce lifecycle rather than adapting HMAC into a cipher; no encryption is implemented in this batch. The next connected unit is [privacy-preserving count release](../../13-privacy/count-release/LESSON.md), whose disclosure threat differs from integrity.

The [primary source record](../../security-cryptography-mastery/provenance/SOURCES.md) specifies inspected RFC construction/vector scopes and standard-library dependencies. The bounded project is STRONG; the complete secure-pipeline scope, including confidentiality/deployment, is PARTIAL.
