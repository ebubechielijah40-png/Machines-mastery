# Hints — use after a recorded attempt

1. A MAC proves a relationship to key possession, not sensor calibration.
2. Project global entries onto one producer; compare that subsequence.
3. The key ID is included in the authenticated envelope.
4. Replace x² by x+1; XOR cancels equal terms.
5. The appended length block is zero too.
6. One byte is8bits; each length has an eight-byte big-endian field.
7. Cancel the repeated keystream algebraically before considering tags.
8. Count reservations separately from entries.
9. The witness's remembered digest must identify a prefix that exists locally.
10. Ask which entity remembers the missing newer fact.
11. Metadata stores a fixed fingerprint; signing a transition is a new protocol.
12. Signature validity and expected-context equality are separate checks.
13. Ask what secret is required to create each authenticator.
14. A forged record is not automatically the next authorized record.
15. Restarting a process differs from erasing its durable authority state.
16. Check per-producer projections and nonce-set size, not one scheduler order.
17. Multiply before converting units; SQLite pages/indexes add overhead.
18. Preserve numerator/denominator; reject Boolean sequence values.
19. A vector checks an algorithm case; a local process test has another scope.
20. A database commit does not roll back a physical or remote side effect.
