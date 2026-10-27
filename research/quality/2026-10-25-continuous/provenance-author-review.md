# Provenance author preparation —2026-10-25

Scope: unchanged data-security card; preserve the original plaintext/HMAC unit
and add a bounded protected-history mechanism. New files under
security-cryptography-mastery/provenance cover library AES-GCM, explicit GHASH,
immutable epochs, local serialized append/idempotent replay, nonce reservations,
signed context-bound witness heads and crash/rollback experiments.

Actually executed:25 tests, including5 preserved contracts and20 new tests;
two real writer processes; four actualSIGKILL phases; inspected NIST values;
independent polynomial representation oracle;16 tag-length/context cases;
whole-pair rollback and repeated-key/nonce counterexamples. Raw evidence and
commands are in PROTECTED_EXPERIMENTS.md. The code adds a guard refusing a nonce
already retained locally before encryption and binds configuration into every
signed head, repairing two identified risks in the prior lost draft design.

Preparation review checked that no tag is returned as plaintext before the AEAD
library verifies it; key IDs/policy are authenticated; epochs retain old-key
interpretation; writers revalidate before append; failures consume reservations;
same-sequence retries preserve original digest; context/pinned-key checks precede
acceptance; and same-host authority limitations are explicit. This is author
review, not independent qualitative approval. No score or scope is changed here.

Remaining broad work: dynamic authorization/key transitions, protected remote
authority, availability/failover, actual key custody/erasure, archival migration,
general cryptography, scalable append verification and physical durability.
The local model is not a production-ready security implementation or deployed
infrastructure. Parent/root must assess whether its unchanged foundational gate
has meaningful breadth and record remaining limitations honestly.

## Integration erratum

Fresh independent replay established9 preserved pipeline tests plus16 protected-history tests,25 total. The earlier5+20 breakdown above was incorrect and is preserved as historical author reporting, not current validation evidence. Current logs and provenance-final-reader records are authoritative.
