# Security: Inter-Node Authentication and Replay Protection

## Threat Model
In an unauthenticated distributed cluster, an attacker with network vantage could:
1. Inject fraudulent `APPEND_ENTRIES` RPCs to overwrite state machine values.
2. Replay captured election votes to prematurely advance terms or cause flapping.
3. Forge `REQUEST_VOTE` messages to force denial-of-service leader step-downs.

## Mitigations Implemented
1. **HMAC Message Tokens:** Every message carries an HMAC-SHA256 signature calculated over `(src, dst, msg_type, term, nonce, payload)` using a pre-shared cluster secret.
2. **Monotonic Nonce Sequence:** Each node attaches a strictly increasing `nonce` to outgoing messages. The receiving node records `last_seen_nonce[src]` and drops any message where `nonce <= last_seen_nonce[src]`.
3. **Audit Counters:** Tampered tokens and replayed nonces increment `security_violations` and `tampered_rejected` counters for anomaly alerting.
