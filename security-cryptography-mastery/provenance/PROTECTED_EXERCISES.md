# Protected-history exercises

Predict before running the reference. Keep your threat model with each answer.

1. A valid producer key signs25001milli-celsius from an uncalibrated sensor.
   Which authenticity, truth and confidentiality claims can be made?
2. Two producers each submit sequences1…6. Explain why alpha's sequence5 need
   not be global position5. Give a legal global order containing all12 entries.
3. Alpha-old authorizes1–2, alpha-new3–10000. Classify an old-key sequence3,
   a correctly signed new-key sequence3, and an old MAC with only its ID changed.
4. In the two-bit polynomial bridge, compute `11+10`, `11×10` and `11×11`
   modulo `x²+x+1`. Explain why integer multiplication/modulo is unsuitable.
5. For empty context and empty ciphertext, derive the GHASH state and the
   full tag's relationship to the encrypted pre-counter block.
6. Context has1byte and ciphertext has2bytes. Write the final16-byte length
   block as hexadecimal. Why are lengths measured in bits?
7. Same key/nonce encrypts32 A bytes and32 B bytes under different context.
   Predict the XOR of ciphertext payloads and explain what valid tags do not fix.
8. A new position1 reserves nonce1 then dies before local commit. Trace local
   state, authority state and the next retry. Why are nonce gaps acceptable?
9. For `(local count,witness count)=(2,1),(2,3),(2,2)`, explain the reopen
   decision. Include the case where equal counts have different digests.
10. Restore matching old copies of both stores. Can a fresh challenge alone
    detect rollback? Identify the missing evidence rather than inventing it.
11. An administrator appends a new epoch to the in-memory configuration after
    opening an existing ledger. Should its metadata still match? Design the
    minimum additional transition evidence a real migration would require.
12. A receipt has a valid signature but refers to another configuration.
    Another receipt has the expected configuration but yesterday's challenge.
    State both rejection rules. Why pin the public key separately?
13. Compare distributing a producer HMAC key to an analyst with distributing
    only the witness's public verification key. Which enables new signatures?
14. An old producer key is stolen after rotation. Distinguish MAC validity,
    sequence authorization, conflicting retries and substitution below a
    separately protected witness head.
15. The witness cannot be reached. A colleague proposes deleting its local
    representation and recreating a fresh one. Explain the safety/availability
    tradeoff and the consequence for nonce reservations.
16. Write an independent assertion for concurrent output that tolerates any
    legal interleaving while detecting a missing beta sequence or duplicate nonce.
17. At most10000 frames of32768bytes are individually allowed. Compute their
    raw upper product and explain why a pre-open64MiB file check is not an OS
    disk quota, hard running-time guarantee or proof of final database size.
18. For25123milli-celsius, derive the exact output object. Give two input/schema
    cases that should fail before accepting an observation.
19. Match one claim each to the inspected GCM standard, NIST vector, library
    API, SQLite transaction documentation and actual local experiment. Which
    source establishes the security of a remotely deployed witness here?
20. Without reading the reference, draw/rebuild the nonce→local commit→witness
    state machine. Transfer it to an external job effect: what remains outside
    the transaction, and what evidence would be required before a retry?
