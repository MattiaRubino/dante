"""Purpose-separated M4 signup OTP and password-recovery proof primitives."""

from __future__ import annotations

import hmac
import secrets
from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from dataclasses import dataclass
from hashlib import sha256
from uuid import UUID

from pydantic import SecretStr

from dante.auth.contracts import AuthIntegrityError

_OTP_DIGITS = 6
_RECOVERY_SECRET_BYTES = 32
_SIGNUP_OTP_DOMAIN = b"dante:auth:signup-otp:v1\x00"
_RECOVERY_DOMAIN = b"dante:auth:password-recovery:v1\x00"


def _encode_urlsafe(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _decode_recovery_secret(value: str) -> bytes | None:
    try:
        raw_ascii = value.encode("ascii")
    except UnicodeEncodeError:
        return None

    padding = b"=" * (-len(raw_ascii) % 4)
    try:
        decoded = b64decode(raw_ascii + padding, altchars=b"-_", validate=True)
    except (BinasciiError, ValueError):
        return None

    if len(decoded) != _RECOVERY_SECRET_BYTES or _encode_urlsafe(decoded) != value:
        return None
    return decoded


@dataclass(frozen=True, slots=True)
class IssuedSignupOtp:
    """Transient raw signup OTP plus persistence-safe verifier metadata."""

    code: SecretStr
    verifier: bytes
    key_id: str


class SignupOtpCodec:
    """Issue and verify six-digit OTPs under a dedicated rotatable HMAC key ring."""

    def __init__(self, *, key_ring: dict[str, bytes], current_key_id: str) -> None:
        if current_key_id not in key_ring:
            raise ValueError("current signup OTP key is absent from the key ring")
        self._key_ring = dict(key_ring)
        self._current_key_id = current_key_id

    def issue(self, signup_ref: UUID) -> IssuedSignupOtp:
        """Generate one uniform six-digit code and its challenge-bound HMAC verifier."""
        code = f"{secrets.randbelow(10**_OTP_DIGITS):0{_OTP_DIGITS}d}"
        return IssuedSignupOtp(
            code=SecretStr(code),
            verifier=self._derive(signup_ref, code, self._current_key_id),
            key_id=self._current_key_id,
        )

    def matches(
        self,
        *,
        signup_ref: UUID,
        submitted_code: str,
        expected_verifier: bytes,
        key_id: str,
    ) -> bool:
        """Constant-time compare a bounded code against the stored challenge verifier."""
        if len(submitted_code) != _OTP_DIGITS or not submitted_code.isascii():
            return False
        if not submitted_code.isdigit():
            return False
        if key_id not in self._key_ring:
            raise AuthIntegrityError("stored signup challenge references unknown OTP key")
        candidate = self._derive(signup_ref, submitted_code, key_id)
        return hmac.compare_digest(candidate, expected_verifier)

    def _derive(self, signup_ref: UUID, code: str, key_id: str) -> bytes:
        payload = _SIGNUP_OTP_DOMAIN + signup_ref.bytes + code.encode("ascii")
        return hmac.digest(self._key_ring[key_id], payload, "sha256")


@dataclass(frozen=True, slots=True)
class IssuedRecoveryProof:
    """Transient high-entropy recovery bearer plus persistence-safe verifier."""

    secret: SecretStr
    verifier: bytes


def issue_recovery_proof() -> IssuedRecoveryProof:
    """Generate one 256-bit canonical Base64URL recovery bearer."""
    raw = secrets.token_bytes(_RECOVERY_SECRET_BYTES)
    return IssuedRecoveryProof(
        secret=SecretStr(_encode_urlsafe(raw)),
        verifier=sha256(_RECOVERY_DOMAIN + raw).digest(),
    )


def recovery_secret_verifier(encoded_secret: str) -> bytes | None:
    """Decode a canonical 256-bit bearer and derive its domain-separated verifier."""
    raw = _decode_recovery_secret(encoded_secret)
    if raw is None:
        return None
    return sha256(_RECOVERY_DOMAIN + raw).digest()


def recovery_secret_matches(encoded_secret: str, expected_verifier: bytes) -> bool:
    """Constant-time validate one canonical recovery bearer."""
    candidate = recovery_secret_verifier(encoded_secret)
    return candidate is not None and hmac.compare_digest(candidate, expected_verifier)
