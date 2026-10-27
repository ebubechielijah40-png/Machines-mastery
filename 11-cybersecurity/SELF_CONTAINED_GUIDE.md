# Security engineering through a bounded adversary model

Begin with the [authenticated provenance lesson](../security-cryptography-mastery/provenance/LESSON.md), whose prerequisite path leads through framing and measurement analysis. Security is a property relative to assets, adversary capabilities and assumptions. A control can be correct yet irrelevant to the attack being considered. This guide uses the implemented local pipeline to make those boundaries testable.

## Turn a goal into an invariant

“Secure the sensor data” leaves several different goals unresolved. Preserve confidentiality from disk readers? Prevent an unauthorized producer writing room data? Detect altered output? Reject replay? Survive interrupted writes? Preserve evidence of deletion? Each needs its own invariant and authority. The current implementation addresses bounded schema/authentication, a configured write policy, per-producer order and authenticated history verification under single-writer local assumptions. It does not encrypt or authenticate a remote login.

Trace one attack path. An attacker submits a captured valid seq1 record after seq1 committed. Syntax is valid and its producer tag verifies, so authentication alone would accept it. The remembered sequence invariant requires next=last+1, causing SequenceError before append. In a second path the authorized producer tags seq2 for forbidden stream outside. It passes authentication but fails the stream policy. A third path edits only the derived output in stored history: reopening fails the processor MAC or exact-transform validation. The test matrix independently exercises these distinctions.

Now change an assumption: let the attacker know the producer key. It can create a fresh valid observation tag; HMAC no longer distinguishes it from the intended producer. A remaining processor policy can still restrict streams, but cannot recover producer identity from that compromised key. This is why key distribution, isolation and lifecycle are part of a security system rather than details postponed by an algorithm choice.

## Bound the parser as a resource boundary

The network decoder checks length after four prefix bytes, before accepting an attacker-announced body. Its pending buffer bound does not cap returned messages or connection count. The JSON layer limits payload bytes, duplicate fields, numeric ranges and exact types. Python booleans compare equal to integers, so schema validation checks `type(x) is int`. Layered limits matter: a valid frame may still carry invalid JSON, and valid JSON may still contain an unauthorized request.

The [HTTP build](../projects-guided/p06-http-server/README.md) shows a separate ambiguity risk. Duplicate or competing length indicators can give recipients different boundaries. The narrow lab rejects unsupported body conventions and always closes one owned connection. It does not prove request-smuggling resistance in a proxy or implement a complete HTTP stack.

## Recovery and evidence limits

Injected fsync failure demonstrates an unknown outcome: in-memory state reports no accepted entry while reopening can find a complete written line. Reusing the still-open object is prohibited; reconcile from stored evidence. A hash chain verifies retained order but accepts a valid prefix after complete suffix deletion unless an independently trusted latest tip is supplied. “Append-only” is a logical format here, not a filesystem access-control guarantee against deletion.

The executed attacks are authorized local mutations of synthetic data and temporary files. Passing them supports specific behavior, not universal security. Source scopes for HMAC and vectors are in the [verification record](../security-cryptography-mastery/provenance/SOURCES.md). Use primary construction sources and independent expected values; a self-generated tag tested only against itself is weak evidence.

## Assessment and unfinished coverage

Complete the provenance exercises on identity, bool numerics, replay, rollback and uncertain writes before reading their separate hints/solutions. Reconstruct the adversary model and explain which control still works after each key/path assumption changes. Submit the actual failure matrix and one counterexample that remains accepted by design, such as an authenticated false measurement claim.

This bounded security-engineering path is STRONG; the cybersecurity domain remains PARTIAL. Memory-safety exploitation/defence, operating-system isolation, service identity, incident response, secure deployment, vulnerability management, AEAD, key rotation and side-channel analysis are not completed by the local pipeline.
