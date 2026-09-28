# Security and cryptography labs

All labs are local and defensive. Do not test third-party systems without authorization.

## Lab 1 — integrity vs authenticity
1. Hash a file with SHA-256.
2. Modify one byte and compare digests.
3. Now imagine an attacker replaces both file and digest. Explain why plain hashing did not authenticate the file.
4. Repeat with HMAC using a secret key and verify modification failure.

## Lab 2 — replay and freshness
Implement a signed/MACed message format containing `sender`, `counter`, and `payload`. Keep the largest accepted counter per sender. Replay an old valid message and verify rejection. Then reason about restart/crash persistence.

## Lab 3 — password storage
Use Python `hashlib.pbkdf2_hmac` only as a standard-library learning example. Generate a unique salt, vary iteration count, measure verification cost, and explain the availability/security tradeoff. In production follow current platform/library guidance rather than copying the lab parameters.

## Lab 4 — authenticated channel model
Build a local client/server that frames messages and authenticates them with HMAC. Introduce bit flips, truncation, reordering, and replay. Record which failures are detected and which need additional state.

## Lab 5 — threat model a database service
List assets, entry points, principals, trust boundaries, abuse cases, logging needs, backup/recovery assumptions, and key material. Then map mitigations to threats. Do not accept “use encryption” as a complete answer.

## Lab 6 — timing leakage demonstration
Write two string-comparison functions: early-exit and constant-structure using `hmac.compare_digest`. Measure many runs locally. Treat noisy timing differences carefully: a benchmark is evidence about your environment, not a universal proof.
