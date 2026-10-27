# Authentication, authorization, and identity

Authentication establishes a principal under a credential model; authorization decides allowed actions. Sessions, cookies, tokens, API keys, OAuth-like delegation, and MFA solve different problems. Production design must cover issuance, storage, expiration, revocation, rotation, replay, audience/scope, and audit. Build a local API with two roles; write tests proving horizontal and vertical access-control failures are rejected.
