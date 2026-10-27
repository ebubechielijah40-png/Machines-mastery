# An authenticated history is a claim about origin and transformation

A checksum answers whether bytes match an expected digest. It does not answer who authorized those bytes. If an adversary can replace both a record and its adjacent unkeyed hash, the check still passes. This unit builds a local authenticated provenance ledger that makes the trust assumptions visible. It uses synthetic temperature records, standard-library HMAC-SHA256 for authentication, an original HMAC construction exercise, strict schemas, exact unit conversion and an authenticated hash chain. It does not implement a cipher or SHA-256 compression from scratch.

Entry gate: finish [stream boundaries](../../06-networking/stream-boundaries/LESSON.md), then the [scientific pipeline](../../projects-guided/p08-scientific-pipeline/README.md). Be able to distinguish a measurement's stated units, its uncertainty and its source identity. For binary operations, compute `0x0b XOR 0x36 = 0x3d`; for functions, explain how composing `H(outer || H(inner || message))` differs from concatenating independent digests.

## Assets and adversary before algorithms

Our asset is a sequence of accepted observation claims and their exact derived Celsius values. A producer knows its own secret key; a processor knows configured producer keys and a different ledger key. The processor's policy allows `sensor` to write only stream `room`; a trusted caller supplies the read principal. The local attacker can submit bytes, replay captured envelopes or edit stored files after the process closes. It does not know either secret in the security model. The executable experiment deliberately publishes demo keys and uses no real private data, so its files provide no actual secrecy against readers of the repository.

| Threat | Mechanism exercised | Residual assumption |
| --- | --- | --- |
| Alter a measurement or its declared producer | Producer HMAC binds all record fields | Secret distribution and trusted verification code |
| Valid producer writes a forbidden stream | Explicit producer-to-stream policy | Policy supplied by trusted operator |
| Reuse an old valid message | Next per-producer sequence must equal last+1 | Durable history; no silent rollback |
| Substitute output or reorder entries | Processor HMAC binds output, transform, index and prior digest | Processor key not compromised |
| Delete a complete suffix | Compare latest digest with trusted external tip | Tip stored outside the attacker's editable ledger |
| Producer submits a false but correctly tagged value | Not detected | Independent measurement evidence is required |

Authentication establishes possession of a key under this model. Authorization asks whether that principal may perform this action. The Python `snapshot('analyst')` parameter is an assumed trusted local identity, not a login protocol; any caller controlling that argument can impersonate a reader. Neither role checking nor HMAC encrypts the record.

## One unambiguous record

The exact schema is `v`, `producer`, `stream`, `seq`, `value_milli_c`, `unit`. Integers are type checked so Python `True == 1` cannot silently satisfy the protocol. Identifier alphabets and lengths, numeric ranges and byte budgets are bounded. Unknown fields, duplicate JSON keys, NaN/Infinity, excessive nesting, non-ASCII wire bytes and malformed envelopes reject. A JSON parser that silently keeps the last duplicate field can otherwise verify one interpretation while another component reads a different one.

The authenticated input is the validated semantic record serialized with sorted keys, compact separators, ASCII escaping and no NaNs. This is a deliberately restricted repository format, not a claim to implement every cross-language JSON canonicalization standard. Reformatting the wire JSON without changing its unique validated values does not change the MAC input. Ambiguous objects never reach canonicalization.

For example, an observation with `value_milli_c=25001` represents exactly `25001/1000` Celsius, or 25.001 °C. The transform stores `{numerator:25001, denominator:1000, unit:'celsius'}`. Integer input and rational output avoid relying on a cross-language floating-point text convention. Schema range `[-50000,150000]` milli-Celsius is an educational policy boundary; it is not a sensor calibration certificate or proof that 120 °C actually occurred.

## What HMAC constructs

RFC 2104 §2 defines a nested keyed hash [S1]. For SHA-256 the block is 64 bytes. If the key is longer, hash it first; then zero-pad to 64 bytes. Let the result be `K0`. Compute

\[
\operatorname{HMAC}_K(m)=H((K_0\oplus\text{opad})\,\|\,H((K_0\oplus\text{ipad})\,\|\,m)).
\]

Each ipad byte is `0x36`; each opad byte is `0x5c`. With a first key byte `0x0b`, the corresponding inner byte is `0x3d` and outer byte `0x57`. The two layers distinguish their roles; an unkeyed `H(m)` permits anyone to replace a message and compute its new hash. This construction explanation and vector testing are not a proof of SHA-256 or HMAC security.

[manual_hmac_sha256](pipeline.py) implements this construction over `hashlib.sha256`; the running pipeline uses `hmac.new` and `hmac.compare_digest`. The test uses RFC 4231 §4.2's independently published vector: key `0b` repeated 20 times, message `Hi There`, output `b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7` [S2]. More key lengths are compared with the standard-library implementation. A matching vector checks one mechanism case, not resistance to all attacks. Domain strings `MM-PROVENANCE-RECORD-v1\0` and `MM-PROVENANCE-LEDGER-v1\0` separate producer observations from processor ledger objects; separate keys further separate authority.

Because producer and verifier share a MAC key, either can generate valid tags. A third party cannot infer which holder authored a record. This ledger therefore offers no public signature or third-party nonrepudiation claim. Losing secrecy of either relevant key invalidates the corresponding adversary assumption.

## State, replay and the history invariant

The durable line contains a `core` and a processor tag. The core binds index, previous entry digest, authenticated observation, transform identifier and exact output. Entry digest is SHA-256 over the entire canonical entry, including its processor tag. The initial previous digest is 64 zero hex digits, a public genesis marker.

After accepting `n` lines, the invariant is: `count=n`, `tip` equals the digest of line `n`, `last[p]` equals the final accepted sequence for producer `p`, and the snapshot equals the last exact transform for each producer/stream. Loading verifies every line from genesis and reconstructs that state. A producer's next sequence is global across that producer's authorized streams, not separate per stream. Sequence 2 cannot arrive before sequence 1; a retry of sequence 1 is rejected after it commits. Supporting out-of-order arrivals would require a different replay-window protocol.

A chain alone cannot prove that its last entry still exists. If a valid two-line file becomes its original first line, every remaining tag and link is still valid. An `expected_tip` taken from outside that editable file detects the rollback. Saving the tip in the same replaceable directory under the same attacker authority defeats that assumption. The lab does not implement an external checkpoint service.

## Writes and uncertain outcomes

Ingest verifies bytes, schema, producer tag, permission and sequence before writing. It writes a complete JSONL record with a write-all loop, calls `fsync`, and only then updates in-memory state. If writing or synchronization raises, the object is poisoned: reopen and reconcile rather than assume the append did not happen. A test injects fsync failure after bytes were written; state remains at zero, but reopening sees one full line. This is a controlled error-path observation, not a real power-loss durability experiment.

An incomplete trailing line fails closed. Automatically removing it might remove evidence of failure or conceal tampering. This lab requires a human recovery decision. It has no writer lock, transactional external checkpoint update, parent-directory synchronization, key rotation or historical policy versions. Callers must exclusively own the path and object. A changed policy or key configuration can prevent reopening previously valid history because current configuration verifies all history. This is an explicit versioning gap, not automatic revocation support.

## Executed investigation

From repository root:

```sh
python3 -m unittest discover -s security-cryptography-mastery/provenance -p test_pipeline.py -v
python3 security-cryptography-mastery/provenance/experiment.py
```

Question: which alterations distinguish authenticated provenance from physical truth? Hold keys, record schema and transformation fixed; vary tampering, replay, unauthorized stream, an authenticated implausible value, and suffix deletion. The [actual JSON](evidence/observed.json) records replay as `SequenceError`, forbidden stream as `AuthorizationError`, mutation as `IntegrityError`, and a correctly signed 120000 milli-Celsius value as accepted. A complete-prefix rollback reopened without a trusted tip, and failed with the previously retained latest tip. The decoder reconstructed the request from three-byte chunks before ingestion; this connects framing to authentication without pretending to deploy a network service.

Reproduction checks an implementation's observable behavior under these assumptions. It cannot show secret-key security by trying a few modifications, establish actual sensor truth, or certify hostile filesystem/concurrency safety. Continue with [exercises](EXERCISES.md), [project milestones](../../projects-guided/p09-secure-pipeline/README.md), and [privacy release](../../13-privacy/count-release/LESSON.md).

## Continue beyond the single-writer plaintext model

Build [encrypted history, static key epochs and an independently remembered head](PROTECTED_HISTORY.md)
after completing this unit. The continuation preserves this smaller standard-library
mechanism and separately requires cryptography50.0.2. It adds explicit GHASH learning,
library AEAD/signatures, actual competing processes/crash phases, separated practice
and a controlled whole-authority rollback counterexample. A same-host witness is
a model with an independence assumption, not a protected remote authority.
