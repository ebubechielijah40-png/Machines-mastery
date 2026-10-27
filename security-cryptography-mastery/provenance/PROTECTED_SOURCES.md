# Inspected source scopes —2026-10-25

The protocol, teaching examples, toy polynomial bridge, code, assessments and
local experiments are original repository work. No full standard, paper, source
PDF or extracted website is redistributed. Inspection is limited to the scopes
below; links are verification references, not required outside tutorials.

| Primary source | Inspected scope | Claim/use and boundary |
| --- | --- | --- |
| Morris Dworkin, NIST SP800-38D, November2007, [GCM and GMAC](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf) | §§6.3–6.5, selected §7.1 steps, §8 uniqueness and AppendixA | Field/GHASH/counter/tag structure and nonce requirement; does not validate this ledger protocol or prove our code secure |
| NIST CSRC, [GCM worked values](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/AES_GCM.pdf) | GCM-AES128 Examples1–2, PDF pages1–3 | Exact key/IV/plaintext/ciphertext/GHASH/tag test values; no document date asserted where unavailable |
| Python Cryptographic Authority, [AEAD API50.0.2](https://cryptography.io/en/50.0.2/hazmat/primitives/aead/) | AESGCM constructor/encrypt/decrypt, tag/context/nonce rules and InvalidTag | Library boundary; AES/Ed25519 implementation is delegated, not reconstructed |
| Python Cryptographic Authority, [Ed25519 API50.0.2](https://cryptography.io/en/50.0.2/hazmat/primitives/asymmetric/ed25519/) | Sign/verify, from_private_bytes, raw public-key serialization | Exact key/signature interfaces; no complete elliptic-curve lesson or remote PKI claim |
| SQLite project, [Transaction](https://www.sqlite.org/lang_transaction.html) | §§2.1–2.2, simultaneous writers and IMMEDIATE transactions | Local serialization/busy semantics; not distributed consensus or host-power-failure evidence |

The linked APIs are pinned to50.0.2; actual execution used cryptography50.0.2,
Python3.12.14 and SQLite3.53.1. SQLite documentation is live. Local installed
distribution metadata identifies PyCA/contributors and license expression
`Apache-2.0 OR BSD-3-Clause`; package bytes are not bundled. Other cited works
retain their own rights. Public access does not grant a blanket redistribution
license. RFC8032 metadata and introductory material were inspected for context;
no full RFC reconstruction or RFC test-vector execution is claimed here.

Source claims are distinct from original protocol assumptions. The independently
remembered witness, immutable configuration, exclusive allocator key domain,
authorized witness calls and trusted paths are declared model premises, not
guarantees obtained from these sources. Finite tests and published vectors do
not establish production security, learner mastery or real measurement truth.
