# Security and cryptography — deep handbook

## 1. Security starts with a model

Security is not a property called “secure.” A design protects particular assets against particular capabilities under particular assumptions. Start every exercise with: **what are we protecting, from whom, for how long, and what failures are acceptable?**

Confidentiality prevents unauthorized disclosure. Integrity prevents undetected unauthorized modification. Authenticity answers who/what produced a message under a stated credential model. Availability concerns useful service despite faults or attacks. Privacy concerns appropriate information processing and can conflict with observability or retention. These properties overlap but are not interchangeable.

### Example: telemetry pipeline
A sensor sends temperature readings to a server. Encryption can hide values in transit. A MAC or AEAD tag can detect tampering. Authentication can bind a message to a device credential. None of these proves the sensor measured the real temperature correctly. That is a measurement/provenance problem, not merely a cryptographic one.

## 2. Randomness and keys

Cryptography often assumes keys are unpredictable to an adversary. A deterministic pseudorandom generator can expand a small secret seed, but the seed must come from adequate entropy. A key stored in source control is not protected just because the algorithm is strong. Key lifecycle—generation, storage, rotation, revocation, backup, and destruction—is part of the system.

**Experiment:** generate many bytes with `secrets.token_bytes`, count byte frequencies, and observe that passing a simple frequency check does not prove cryptographic randomness. Statistical tests can detect some flaws; they cannot prove unpredictability.

## 3. Hash functions

A cryptographic hash maps arbitrary input to a fixed-size digest. Desired properties include preimage resistance, second-preimage resistance, and collision resistance. Collision resistance does not mean collisions are impossible—finite outputs guarantee collisions exist. It means finding one should be computationally infeasible at the intended security level.

Hashes support integrity checks only when the expected digest is itself trusted. An attacker who can replace both a file and an unauthenticated hash can defeat the check.

## 4. MACs

A message authentication code uses a shared secret to authenticate a message. HMAC combines a cryptographic hash with a key in a construction designed to avoid naive `hash(key || message)` pitfalls. MACs provide authenticity/integrity between parties that share the key; they do not provide public verifiability like digital signatures.

## 5. Encryption and AEAD

Encryption transforms plaintext using a key. Modern applications generally need **authenticated encryption**: confidentiality plus integrity/authenticity of ciphertext and selected associated data. Modes that only encrypt but do not authenticate can permit dangerous modification attacks.

Nonce requirements are construction-specific. Reusing a nonce under an AEAD mode that requires uniqueness can catastrophically break security. “Nonce” does not mean “secret”; it means a value with specified uniqueness/randomness requirements.

Never invent a new cipher for production. Teaching constructions in this repository are explicitly toy models.

## 6. Public-key cryptography

Public-key systems separate a public key from a private key. Encryption lets anyone encrypt to a public key while only the private-key holder decrypts, under the scheme's assumptions. Digital signatures let a private-key holder produce a signature that public-key holders can verify. Signatures authenticate a key, not a human identity unless a trusted binding exists.

RSA security is related to the difficulty of factoring large composites, while elliptic-curve systems rely on discrete-logarithm problems in selected groups. Real systems require standardized padding/encoding and side-channel-resistant implementations; textbook formulas alone are insufficient.

## 7. Key exchange and PKI

Key exchange allows parties to derive shared key material over an observable channel. Authentication must be added to resist active man-in-the-middle attacks. Certificates bind names/identities to public keys through a trust infrastructure. Certificate validation includes chain building, validity periods, name matching, algorithm constraints, and revocation/operational policy.

## 8. Passwords and authentication

Passwords should not be stored with fast general-purpose hashes. Password hashing uses slow, salted, memory-hard or work-factor-controlled functions such as Argon2id, scrypt, bcrypt, or PBKDF2 depending platform guidance. Salt is not secret; it prevents identical passwords from sharing the same stored hash and defeats precomputed tables.

Authentication asks “who/what are you under this credential model?” Authorization asks “what may this principal do?” Mixing them causes broken access control.

## 9. Side channels

A mathematically sound algorithm can leak secrets through timing, cache behavior, power, electromagnetic emissions, error messages, memory reuse, or fault behavior. Constant-time coding and hardened libraries matter. Security is an implementation/system property, not only an algorithm property.

## 10. Protocol composition

Secure components can compose insecurely. A protocol must bind context, identities, algorithm choices, message order, freshness, and transcript state. Replay protection needs nonces, counters, timestamps, or state according to the application model.

## 11. Post-quantum reality

Large fault-tolerant quantum computers would threaten widely used public-key schemes based on factoring and discrete logarithms via Shor's algorithm. Symmetric cryptography is affected differently: Grover's algorithm gives a quadratic search speedup in an idealized model, which generally motivates larger symmetric key sizes rather than abandoning symmetric cryptography. Post-quantum cryptography uses classical algorithms designed around problems believed hard for quantum computers; migration is a protocol and inventory problem as much as an algorithm problem.

## 12. What cryptography cannot do

Cryptography cannot make a compromised endpoint trustworthy, prove a sensor measured reality correctly, recover data for which all keys/backups are lost, prevent an authorized user from misusing plaintext they legitimately receive, or guarantee availability against all resource-exhaustion attacks. State those limits explicitly in every design.
