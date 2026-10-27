# Data security: identity, authority, history and recovery

Start with [scientific ingestion](../projects-guided/p08-scientific-pipeline/README.md), then build [authenticated provenance](../projects-guided/p09-secure-pipeline/README.md). The scientific pipeline records exact input bytes and code/configuration identity. The security pipeline asks which authority can authorize a claim, which transformation was accepted, and what history survives failure. The same bytes can be reproducible, authentic and false; these properties must be assessed separately.

This guide first explains the preserved single-writer plaintext mechanism.
Then build [protected history](../security-cryptography-mastery/provenance/PROTECTED_HISTORY.md),
which adds a distinct encrypted transactional mechanism with fixed historical
key epochs and a local model of an independent witness. The first mechanism's
limits below must not be silently transferred into guarantees for the second.

## Content identity versus trusted origin

Let a manifest contain raw-data digest `h=SHA256(data)`. A verifier recomputes h and compares it with the manifest. If both are independently trusted, mismatch detects changed content. If an attacker can replace data and manifest, it can compute a new matching h. The unkeyed digest therefore needs a trusted anchor. The implemented pipeline adds producer HMAC over a restricted canonical record and processor HMAC over exact transformation output and history position. It uses standard-library cryptographic primitives; no homemade encryption is supplied.

Canonical form is part of the protocol. Duplicate JSON fields are rejected, strings/integers have explicit bounds and units are fixed. A Celsius value is the exact rational `value_milli_c/1000`. Floats are avoided here because a cross-language rounding/serialization policy would otherwise become an additional authentication assumption. The [lesson](../security-cryptography-mastery/provenance/LESSON.md) works the representation and HMAC construction, and links independent source vectors.

## Authorization and replay are separate state

A valid tag identifies a key holder under the secret-key assumption. A producer-to-stream policy decides permitted writes. A next-sequence check rejects captured old messages and unaccepted order. Sequence is per producer across its allowed streams, not per stream. These checks occur before append, so rejected attempts do not consume history positions. Read permission is a local trusted-principal parameter, not a session or password system.

Reopening verifies every retained entry and reconstructs snapshot state. It checks processor tag, index, previous digest, producer authentication, current policy, sequence and exact output. The configured max-entry count and line-length limit bound loading. A new key/policy configuration may prevent old records reopening because history is checked against current authority; historical configuration and rotation remain a real design gap.

## Durability has an uncertain-outcome state

Write all line bytes, sync, then acknowledge in-memory acceptance. A failure can occur after some or all bytes were written. The object poisons itself and requires reopen/reconciliation. The test injects a synchronization failure after a full write: the old in-memory count stays zero while a reopen sees one line. This is not a power-cut experiment, parent-directory durability test or complete transaction protocol.

An incomplete last line fails closed rather than silently truncating it. A complete valid prefix opens unless an external expected tip disagrees. Thus local chain verification detects many substitutions/reorderings but cannot alone establish freshness or availability. Concurrent writers, hostile path replacement, protected backups, atomic checkpoint publication and disaster recovery are unimplemented. A logical JSONL append format is not an operating-system append-only guarantee.

## Confidentiality and minimization remain different

Tags and hashes do not hide values. Anyone allowed to read these plaintext files sees producer, stream and measurements. Real confidentiality requires a separately reviewed encryption/key/access design; logs and backups must receive the same analysis. The synthetic lab deliberately publishes keys for reproduction and must not be used as a data protection service. Privacy release further asks what permitted outputs reveal about contributors, addressed in the [count lesson](../13-privacy/count-release/LESSON.md).

Assessment: reconstruct the write/reopen invariant, run mutation/replay/rollback/partial-write cases, and explain what an attacker can still do after obtaining each key or replacing each file. Use the linked project's separately stored exercises/hints/solutions and actual evidence. The bounded unit is STRONG; data security remains PARTIAL pending encryption, real identity, key lifecycle, concurrent persistence, protected retention/backups and deployment validation.

## Continue through confidentiality and remembered authority

The [new original chapter](../security-cryptography-mastery/provenance/PROTECTED_HISTORY.md)
provides the encryption/static-epoch/concurrent-persistence mechanisms that the
first build deliberately omits. It derives nonce/commit/reconciliation states,
teaches a polynomial bridge and explicit GHASH, separates encrypted payload from
visible context, and supplies20 additional exercises with separated hints and
solutions. The actual process experiment and its source fingerprints are linked
there. Do not use its public demo keys for private data.

Before exiting, show why a newer witness rejects an old local ledger, why
rolling back both stores defeats that premise, and why changing AAD does not
repair a repeated encryption key/nonce. An authenticated external service,
dynamic authorization transitions, custody/erasure, protected retention and
production operation still require further work and separate validation. Domain
classification is owned by the unchanged-scope dashboard review, not inferred
from this chapter or its passing tests.
