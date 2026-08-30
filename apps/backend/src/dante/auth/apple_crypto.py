"""Apple grant token encryption under a rotatable AES-256-GCM key ring."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from uuid import UUID

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import SecretStr

APPLE_GRANT_ISSUER = "https://appleid.apple.com"
_NONCE_BYTES = 12
_MAX_SECRET_BYTES = 131_072
_AAD_PREFIX = b"dante:apple-auth-grant:v1:"


class AppleGrantCryptoError(ValueError):
    """Apple grant secret failed the authenticated-encryption boundary."""


@dataclass(frozen=True, slots=True)
class EncryptedAppleGrant:
    key_id: str
    nonce: bytes
    ciphertext: bytes


def apple_grant_aad(*, grant_ref: UUID, client_id: str) -> bytes:
    if not client_id or client_id.strip() != client_id or any(char in client_id for char in "\r\n"):
        raise AppleGrantCryptoError("Apple client_id must be canonical")
    return (
        _AAD_PREFIX
        + str(grant_ref).encode("ascii")
        + b":"
        + APPLE_GRANT_ISSUER.encode("ascii")
        + b":"
        + client_id.encode("utf-8")
    )


class AppleGrantCipher:
    """Encrypt/decrypt Apple grant material by persisted stable key id."""

    def __init__(self, *, key_ring: dict[str, bytes], current_key_id: str) -> None:
        if current_key_id not in key_ring:
            raise ValueError("current Apple grant key is absent from key ring")
        if not key_ring or any(len(key) != 32 for key in key_ring.values()):
            raise ValueError("Apple grant keys must be exactly 256 bits")
        self._key_ring = dict(key_ring)
        self._current_key_id = current_key_id

    def encrypt(
        self, *, plaintext: SecretStr, grant_ref: UUID, client_id: str
    ) -> EncryptedAppleGrant:
        raw = plaintext.get_secret_value().encode("utf-8")
        if not raw or len(raw) > _MAX_SECRET_BYTES:
            raise AppleGrantCryptoError("Apple grant secret is empty or oversized")
        nonce = secrets.token_bytes(_NONCE_BYTES)
        aad = apple_grant_aad(grant_ref=grant_ref, client_id=client_id)
        ciphertext = AESGCM(self._key_ring[self._current_key_id]).encrypt(nonce, raw, aad)
        return EncryptedAppleGrant(key_id=self._current_key_id, nonce=nonce, ciphertext=ciphertext)

    def decrypt(
        self,
        *,
        key_id: str,
        nonce: bytes,
        ciphertext: bytes,
        grant_ref: UUID,
        client_id: str,
    ) -> SecretStr:
        key = self._key_ring.get(key_id)
        if key is None:
            raise AppleGrantCryptoError("Apple grant references an unknown encryption key")
        if len(nonce) != _NONCE_BYTES or not ciphertext or len(ciphertext) > _MAX_SECRET_BYTES + 32:
            raise AppleGrantCryptoError("Apple grant ciphertext envelope is malformed")
        aad = apple_grant_aad(grant_ref=grant_ref, client_id=client_id)
        try:
            plaintext = AESGCM(key).decrypt(nonce, ciphertext, aad)
            decoded = plaintext.decode("utf-8")
        except (InvalidTag, UnicodeDecodeError) as exc:
            raise AppleGrantCryptoError("Apple grant ciphertext authentication failed") from exc
        if not decoded:
            raise AppleGrantCryptoError("Apple grant plaintext is empty")
        return SecretStr(decoded)
