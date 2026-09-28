"""Defensive cryptography learning helpers. Not a production protocol."""
from __future__ import annotations
import hashlib, hmac, secrets


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def make_hmac(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()


def verify_hmac(key: bytes, message: bytes, tag: bytes) -> bool:
    return hmac.compare_digest(make_hmac(key, message), tag)


def derive_password_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    if iterations < 1:
        raise ValueError("iterations must be positive")
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=32)


def new_salt(n: int = 16) -> bytes:
    return secrets.token_bytes(n)
