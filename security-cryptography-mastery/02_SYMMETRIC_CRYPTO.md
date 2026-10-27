# Symmetric cryptography

Block ciphers are keyed permutations over fixed-size blocks; modes or AEAD constructions turn them into message encryption. Stream-cipher style constructions generate a keystream combined with plaintext. Never reuse a nonce where a construction requires uniqueness. Authenticated encryption protects confidentiality and detects modification under its security model. Experiment with a toy XOR stream to see why keystream reuse leaks `P1 xor P2`; then use a standard library AEAD and show tampering causes verification failure.
