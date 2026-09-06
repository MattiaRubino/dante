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
_PROVIDER_ENROLLMENT_OTP_DOMAIN = b"dante:auth:provider-enrollment-otp:v1\x00"
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
    except UnicodeEncodeError, BinasciiError, ValueError:
        return None
    if len(decoded) != _SECRET_BYTES or _encode_urlsafe(decoded) != value:
        return None
    return decoded


@dataclass(frozen=True, slots=True)
class IssuedSignupOtp:
    code: SecretStr
    verifier: bytes
    key_id: str


class _OtpCodec:
    def __init__(
        self,
        *,
        key_ring: dict[str, bytes],
        current_key_id: str,
        domain: bytes,
        purpose_name: str,
    ) -> None:
        if current_key_id not in key_ring:
            raise ValueError(f"current {purpose_name} OTP key is absent from the key ring")
        self._key_ring = dict(key_ring)
        self._current_key_id = current_key_id
        self._domain = domain
        self._purpose_name = purpose_name

    def issue(self, reference: UUID) -> IssuedSignupOtp:
        code = f"{secrets.randbelow(10**_OTP_DIGITS):0{_OTP_DIGITS}d}"
        return IssuedSignupOtp(
            code=SecretStr(code),
            verifier=self._derive(reference, code, self._current_key_id),
            key_id=self._current_key_id,
        )

    def matches(
        self,
        *,
        reference: UUID,
        submitted_code: str,
        expected_verifier: bytes,
        key_id: str,
    ) -> bool:
        if (
            len(submitted_code) != _OTP_DIGITS
            or not submitted_code.isascii()
            or not submitted_code.isdigit()
        ):
            return False
        if key_id not in self._key_ring:
            raise AuthIntegrityError(
                f"stored {self._purpose_name} challenge references unknown OTP key"
            )
        candidate = self._derive(reference, submitted_code, key_id)
        return hmac.compare_digest(candidate, expected_verifier)

    def _derive(self, reference: UUID, code: str, key_id: str) -> bytes:
        return hmac.digest(
            self._key_ring[key_id],
            self._domain + reference.bytes + code.encode("ascii"),
            "sha256",
        )


class SignupOtpCodec:
    """Password-signup OTP codec retaining the stable M4 public call contract."""

    def __init__(self, *, key_ring: dict[str, bytes], current_key_id: str) -> None:
        self._codec = _OtpCodec(
            key_ring=key_ring,
            current_key_id=current_key_id,
            domain=_SIGNUP_OTP_DOMAIN,
            purpose_name="signup",
        )

    def issue(self, signup_ref: UUID) -> IssuedSignupOtp:
        return self._codec.issue(signup_ref)

    def matches(
        self,
        *,
        signup_ref: UUID,
        submitted_code: str,
        expected_verifier: bytes,
        key_id: str,
    ) -> bool:
        return self._codec.matches(
            reference=signup_ref,
            submitted_code=submitted_code,
            expected_verifier=expected_verifier,
            key_id=key_id,
        )


class ProviderEnrollmentOtpCodec:
    """Provider-enrollment OTP codec using a distinct HMAC domain from password signup."""

    def __init__(self, *, key_ring: dict[str, bytes], current_key_id: str) -> None:
        self._codec = _OtpCodec(
            key_ring=key_ring,
            current_key_id=current_key_id,
            domain=_PROVIDER_ENROLLMENT_OTP_DOMAIN,
            purpose_name="provider enrollment",
        )

    def issue(self, external_signup_ref: UUID) -> IssuedSignupOtp:
        return self._codec.issue(external_signup_ref)

    def matches(
        self,
        *,
        external_signup_ref: UUID,
        submitted_code: str,
        expected_verifier: bytes,
        key_id: str,
    ) -> bool:
        return self._codec.matches(
            reference=external_signup_ref,
            submitted_code=submitted_code,
            expected_verifier=expected_verifier,
            key_id=key_id,
        )


@dataclass(frozen=True, slots=True)
class IssuedRecoveryProof:
    secret: SecretStr
    verifier: bytes


def issue_recovery_proof() -> IssuedRecoveryProof:
    raw = secrets.token_bytes(_SECRET_BYTES)
    return IssuedRecoveryProof(
        secret=SecretStr(_encode_urlsafe(raw)), verifier=sha256(_RECOVERY_DOMAIN + raw).digest()
    )


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


def flow_proof_verifier_from_raw(*, purpose: FlowProofPurpose, raw_secret: bytes) -> bytes | None:
    """Derive a purpose-separated verifier from an exact 32-byte raw capability."""
    if len(raw_secret) != _SECRET_BYTES:
        return None
    domain = _M5_DOMAIN_PREFIX + purpose.value.encode("ascii") + _M5_DOMAIN_SUFFIX
    return sha256(domain + raw_secret).digest()


def flow_proof_verifier(*, purpose: FlowProofPurpose, encoded_secret: str) -> bytes | None:
    raw = _decode_secret(encoded_secret)
    if raw is None:
        return None
    return flow_proof_verifier_from_raw(purpose=purpose, raw_secret=raw)


def issue_flow_proof(purpose: FlowProofPurpose) -> IssuedFlowProof:
    raw = secrets.token_bytes(_SECRET_BYTES)
    encoded = _encode_urlsafe(raw)
    verifier = flow_proof_verifier_from_raw(purpose=purpose, raw_secret=raw)
    if verifier is None:  # pragma: no cover - generated exact-width input cannot fail
        raise AssertionError("generated flow proof failed verifier derivation")
    return IssuedFlowProof(secret=SecretStr(encoded), verifier=verifier, purpose=purpose)


def flow_proof_matches(
    *, purpose: FlowProofPurpose, encoded_secret: str, expected_verifier: bytes
) -> bool:
    candidate = flow_proof_verifier(purpose=purpose, encoded_secret=encoded_secret)
    return candidate is not None and hmac.compare_digest(candidate, expected_verifier)
