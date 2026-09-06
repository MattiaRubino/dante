"""Purpose-separated protection for short-lived durable Email Platform payloads."""

from __future__ import annotations

import hmac
import json
import secrets
from uuid import UUID

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from dante.platform.email.contracts import (
    ClaimedEmailIntent,
    EmailPayloadError,
    EncryptedEmailPayload,
)

_AAD_PREFIX = b"dante:email:intent:v1\x00"
_FINGERPRINT_PREFIX = b"dante:email:fingerprint:v1\x00"


class EmailPayloadCipher:
    """AES-256-GCM key ring for crash-safe but short-lived delivery material."""

    def __init__(self, *, key_ring: dict[str, bytes], current_key_id: str) -> None:
        if current_key_id not in key_ring:
            raise ValueError("current email payload key is absent from the key ring")
        if any(len(value) != 32 for value in key_ring.values()):
            raise ValueError("email payload keys must be exactly 32 bytes")
        self._key_ring = dict(key_ring)
        self._current_key_id = current_key_id

    def protect(
        self,
        *,
        email_intent_ref: UUID,
        purpose_code: str,
        template_code: str,
        template_revision: str,
        payload: dict[str, str | int],
    ) -> EncryptedEmailPayload | None:
        """Encrypt canonical payload bytes and return a keyed immutable fingerprint."""
        canonical = _canonical_payload(payload)
        fingerprint = self.fingerprint(
            purpose_code=purpose_code,
            template_code=template_code,
            template_revision=template_revision,
            payload=payload,
        )
        if not canonical:
            return None
        nonce = secrets.token_bytes(12)
        ciphertext = AESGCM(self._key_ring[self._current_key_id]).encrypt(
            nonce,
            canonical,
            self._aad(
                email_intent_ref=email_intent_ref,
                purpose_code=purpose_code,
                template_code=template_code,
                template_revision=template_revision,
            ),
        )
        return EncryptedEmailPayload(
            key_id=self._current_key_id,
            nonce=nonce,
            ciphertext=ciphertext,
            fingerprint=fingerprint,
        )

    def fingerprint(
        self,
        *,
        purpose_code: str,
        template_code: str,
        template_revision: str,
        payload: dict[str, str | int],
    ) -> bytes:
        """Derive a keyed fingerprint so low-entropy proofs are not exposed by DB state."""
        return _fingerprint_with_key(
            key=self._key_ring[self._current_key_id],
            purpose_code=purpose_code,
            template_code=template_code,
            template_revision=template_revision,
            payload=payload,
        )

    def matches_fingerprint(
        self,
        expected: bytes,
        *,
        purpose_code: str,
        template_code: str,
        template_revision: str,
        payload: dict[str, str | int],
    ) -> bool:
        """Compare an immutable fingerprint across retained keys during key rotation."""
        matched = False
        for key in self._key_ring.values():
            candidate = _fingerprint_with_key(
                key=key,
                purpose_code=purpose_code,
                template_code=template_code,
                template_revision=template_revision,
                payload=payload,
            )
            matched = hmac.compare_digest(expected, candidate) or matched
        return matched

    def unprotect(self, *, claim: ClaimedEmailIntent) -> dict[str, str | int]:
        """Authenticate and decode the exact claim payload; never guess on corruption."""
        if (
            claim.sensitive_key_id is None
            or claim.sensitive_nonce is None
            or claim.sensitive_ciphertext is None
        ):
            return {}
        key = self._key_ring.get(claim.sensitive_key_id)
        if key is None:
            raise EmailPayloadError("email intent references an unavailable payload key")
        try:
            plaintext = AESGCM(key).decrypt(
                claim.sensitive_nonce,
                claim.sensitive_ciphertext,
                self._aad(
                    email_intent_ref=claim.email_intent_ref,
                    purpose_code=claim.purpose_code,
                    template_code=claim.template_code,
                    template_revision=claim.template_revision,
                ),
            )
        except Exception as exc:
            raise EmailPayloadError("email payload authentication failed") from exc
        try:
            parsed = json.loads(plaintext.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise EmailPayloadError("email payload is not canonical JSON") from exc
        if not isinstance(parsed, dict):
            raise EmailPayloadError("email payload must be a JSON object")
        result: dict[str, str | int] = {}
        for key_name, value in parsed.items():
            if not isinstance(key_name, str) or not isinstance(value, (str, int)):
                raise EmailPayloadError("email payload contains an unsupported value")
            result[key_name] = value
        return result

    @staticmethod
    def _aad(
        *,
        email_intent_ref: UUID,
        purpose_code: str,
        template_code: str,
        template_revision: str,
    ) -> bytes:
        return (
            _AAD_PREFIX
            + email_intent_ref.bytes
            + purpose_code.encode("utf-8")
            + b"\x00"
            + template_code.encode("utf-8")
            + b"\x00"
            + template_revision.encode("utf-8")
        )


def _fingerprint_with_key(
    *,
    key: bytes,
    purpose_code: str,
    template_code: str,
    template_revision: str,
    payload: dict[str, str | int],
) -> bytes:
    canonical = _canonical_payload(payload)
    return hmac.digest(
        key,
        _FINGERPRINT_PREFIX
        + purpose_code.encode("utf-8")
        + b"\x00"
        + template_code.encode("utf-8")
        + b"\x00"
        + template_revision.encode("utf-8")
        + b"\x00"
        + canonical,
        "sha256",
    )


def _canonical_payload(payload: dict[str, str | int]) -> bytes:
    if not payload:
        return b""
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
