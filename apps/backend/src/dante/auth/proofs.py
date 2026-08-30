"""Purpose-separated Auth proof and capability primitives."""

from __future__ import annotations

import hmac
import secrets
from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from uuid import UUID

from pydantic import SecretStr

from dante.auth.contracts import AuthIntegrityError

_OTP_DIGITS = 6
_SECRET_BYTES = 32
_SIGNUP_OTP_DOMAIN = b"dante:auth:signup-otp:v1\x00"
_RECOVERY_DOMAIN = b"dante:auth:password-recovery:v1\x00"
_M5_DOMAIN_PREFIX = b"dante:auth:m5:"
_M5_DOMAIN_SUFFIX = b":v1\x00"


class FlowProofPurpose(StrEnum):
    PROVIDER_STATE = "provider-state"
    OIDC_NONCE = "oidc-nonce"
    PROVIDER_LINK = "provider-link"
    PROVIDER_ENROLLMENT = "provider-enrollment"
    WEBAUTHN_CHALLENGE = "webauthn-challenge"


def _encode_urlsafe(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _decode_secret(value: str) -> bytes | None:
    try:
        raw_ascii = value.encode("ascii")
        decoded = b64decode(raw_ascii + b"=" * (-len(raw_ascii) % 4), altchars=b"-_", validate=True)
    except (UnicodeEncodeError, BinasciiError, ValueError):
        return None
    if len(decoded) != _SECRET_BYTES or _encode_urlsafe(decoded) != value:
        return None
    return decoded


@dataclass(frozen=True, slots=True)
class IssuedSignupOtp:
    code: SecretStr
    verifier: bytes
    key_id: str


class SignupOtpCodec:
    def __init__(self, *, key_ring: dict[str, bytes], current_key_id: str) -> None:
        if current_key_id not in key_ring:
            raise ValueError("current signup OTP key is absent from the key ring")
        self._key_ring = dict(key_ring)
        self._current_key_id = current_key_id

    def issue(self, signup_ref: UUID) -> IssuedSignupOtp:
        code = f"{secrets.randbelow(10**_OTP_DIGITS):0{_OTP_DIGITS}d}"
        return IssuedSignupOtp(code=SecretStr(code), verifier=self._derive(signup_ref, code, self._current_key_id), key_id=self._current_key_id)

    def matches(self, *, signup_ref: UUID, submitted_code: str, expected_verifier: bytes, key_id: str) -> bool:
        if len(submitted_code) != _OTP_DIGITS or not submitted_code.isascii() or not submitted_code.isdigit():
            return False
        if key_id not in self._key_ring:
            raise AuthIntegrityError("stored signup challenge references unknown OTP key")
        candidate = self._derive(signup_ref, submitted_code, key_id)
        return hmac.compare_digest(candidate, expected_verifier)

    def _derive(self, signup_ref: UUID, code: str, key_id: str) -> bytes:
        return hmac.digest(self._key_ring[key_id], _SIGNUP_OTP_DOMAIN + signup_ref.bytes + code.encode("ascii"), "sha256")


@dataclass(frozen=True, slots=True)
class IssuedRecoveryProof:
    secret: SecretStr
    verifier: bytes


def issue_recovery_proof() -> IssuedRecoveryProof:
    raw = secrets.token_bytes(_SECRET_BYTES)
    return IssuedRecoveryProof(secret=SecretStr(_encode_urlsafe(raw)), verifier=sha256(_RECOVERY_DOMAIN + raw).digest())


def recovery_secret_verifier(encoded_secret: str) -> bytes | None:
    raw = _decode_secret(encoded_secret)
    return None if raw is None else sha256(_RECOVERY_DOMAIN + raw).digest()


def recovery_secret_matches(encoded_secret: str, expected_verifier: bytes) -> bool:
    candidate = recovery_secret_verifier(encoded_secret)
    return candidate is not None and hmac.compare_digest(candidate, expected_verifier)


@dataclass(frozen=True, slots=True)
class IssuedFlowProof:
    secret: SecretStr
    verifier: bytes
    purpose: FlowProofPurpose


def flow_proof_verifier(*, purpose: FlowProofPurpose, encoded_secret: str) -> bytes | None:
    raw = _decode_secret(encoded_secret)
    if raw is None:
        return None
    domain = _M5_DOMAIN_PREFIX + purpose.value.encode("ascii") + _M5_DOMAIN_SUFFIX
    return sha256(domain + raw).digest()


def issue_flow_proof(purpose: FlowProofPurpose) -> IssuedFlowProof:
    raw = secrets.token_bytes(_SECRET_BYTES)
    encoded = _encode_urlsafe(raw)
    verifier = flow_proof_verifier(purpose=purpose, encoded_secret=encoded)
    if verifier is None:  # pragma: no cover - generated canonical input cannot fail decoding
        raise AssertionError("generated flow proof failed canonical decoding")
    return IssuedFlowProof(secret=SecretStr(encoded), verifier=verifier, purpose=purpose)


def flow_proof_matches(*, purpose: FlowProofPurpose, encoded_secret: str, expected_verifier: bytes) -> bool:
    candidate = flow_proof_verifier(purpose=purpose, encoded_secret=encoded_secret)
    return candidate is not None and hmac.compare_digest(candidate, expected_verifier)
