# Security and cryptography mastery

This track connects security goals to concrete mechanisms and failure models. It is defensive and authorized. The central discipline is to state **assets, adversary capabilities, trust boundaries, assumptions, and evidence** before choosing a control.

Study order:

1. Security properties and threat modeling
2. Randomness, entropy, and key material
3. Hashes and commitments
4. MACs and authenticated messages
5. Symmetric encryption and AEAD
6. Public-key encryption and signatures
7. Key exchange, certificates, and PKI
8. Protocol composition (TLS concepts)
9. Authentication/authorization/session security
10. Storage/database/data-pipeline security
11. Operational security, logging, response, recovery
12. Cryptographic limits and post-quantum transition

Use the developed [authenticated provenance unit](provenance/LESSON.md) and [guided pipeline build](../projects-guided/p09-secure-pipeline/README.md). `HANDBOOK.md` and `LABS.md` retain broader reading/lab scope; their presence is not evidence that every cryptographic mechanism is implemented.

## Connected implementation path

Follow [measurement and content identity](../projects-guided/p08-scientific-pipeline/README.md), [HMAC-authenticated provenance](provenance/LESSON.md), then [privacy count release](../13-privacy/count-release/LESSON.md). These units include original derivations, executable work, actual evidence and separated learner solutions. The crypto helpers in `code/crypto_lab.py` wrap library primitives and are not hand-built ciphers. The overall track remains PARTIAL; see each source record and the repository scorecard for scoped evidence.
