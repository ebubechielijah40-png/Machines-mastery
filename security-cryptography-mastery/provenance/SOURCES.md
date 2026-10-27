# Primary sources and verified scope

RFC scopes inspected 2026-10-22; Python interfaces inspected 2026-10-23. Record and ledger schema, attacks, code, unit conversion and recovery experiments are original local work. No external paper's empirical results are claimed to have been reproduced.

| ID | Resource | Exact inspected scope and use | Limit |
| --- | --- | --- | --- |
| S1 | H. Krawczyk, M. Bellare, R. Canetti, RFC 2104, *HMAC: Keyed-Hashing for Message Authentication*, February 1997, [§2](https://www.rfc-editor.org/rfc/rfc2104.html#section-2), §3 | Key normalization, ipad/opad nested construction; key-management assumptions | Historic MD5/SHA-1 discussion is not adopted as current guidance; this lab uses SHA-256 and does not reproduce a cryptographic security proof |
| S2 | M. Nystrom, RFC 4231, *Identifiers and Test Vectors for HMAC-SHA-224, HMAC-SHA-256, HMAC-SHA-384, and HMAC-SHA-512*, December 2005, [§4.2](https://www.rfc-editor.org/rfc/rfc4231.html#section-4.2) | Case 1 HMAC-SHA256 expected bytes independently checks manual construction | One vector plus stdlib differential tests is correctness evidence, not certification |
| S3 | Python Software Foundation, Python 3.12 [hmac](https://docs.python.org/3.12/library/hmac.html) and [json](https://docs.python.org/3.12/library/json.html) interfaces used by code | `new`, `hexdigest`, `compare_digest`; `dumps` sorted keys/separators/ensure_ascii/allow_nan; `loads` object_pairs_hook and parse_constant | Does not certify a general canonicalization scheme, whole-program constant-time execution or every accepted JSON object |

RFC sources retain IETF Trust terms. Their algorithms and one short test vector are used with attribution; explanatory text and implementations here are original. SHA-256 compression and cryptographic primitives are provided by the Python standard library. Existing `../code/crypto_lab.py` similarly wraps library primitives and is not relabeled as a hand-built cipher.

Unit classification: STRONG within the single-writer, local, synthetic teaching scope, with explicit recovery and checkpoint limits. Security, data security and cryptography as complete fields remain PARTIAL. AEAD, public-key primitives, PKI, protocol key exchange, side-channel resistance, key lifecycle, concurrent storage and post-quantum implementation remain substantial unfinished work.

The [protected-history continuation](PROTECTED_HISTORY.md) now develops selected
AEAD/key-epoch/concurrent-storage/witness mechanisms, with its own
[newly inspected source scopes](PROTECTED_SOURCES.md) and
[actual experiments](PROTECTED_EXPERIMENTS.md). That original build does not
close all the broader cryptography/operational requirements listed above.
