# Security/cryptography project ladder

## S-1 Tamper-evident log
Build an append-only local log that chains records with hashes/HMACs. Test deletion, reordering, modification, truncation, key loss, and key compromise. Explain what the log can prove and what it cannot prove about real-world events.

## S-2 Authenticated message service
Implement framed local messages with HMAC, sender IDs, counters, replay rejection, and key rotation simulation. Fuzz malformed frames and record rejected states.

## S-3 Password-auth service model
Build a local account store using a standard password-KDF API, salts, rate limiting, session tokens, authorization checks, and audit logging. Threat-model database theft, credential stuffing, session theft, and administrator misuse.

## S-4 Secure file envelope
Using a reputable installed crypto library only, design AEAD file encryption with versioned metadata and key identifiers. Never implement your own production cipher. Test wrong key, modified ciphertext, truncated data, duplicate nonce prevention, and migration/version handling.

## S-5 PKI/TLS inspection lab
On a local service you control, inspect certificate fields, chain, hostname validation, protocol version/cipher negotiation, and failure when trust/name/time assumptions break. Do not disable verification as a “fix.”

## S-6 Secure data pipeline capstone
Ingest authenticated records, validate schema, record provenance, authorize access, encrypt sensitive storage using supported platform tools, audit reads/writes, test recovery, rotate keys, and run incident scenarios. Include a statement of residual risk.
