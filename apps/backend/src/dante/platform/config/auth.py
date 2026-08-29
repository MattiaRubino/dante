"""Validated process configuration for the DANTE Access/Auth runtime."""

from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from enum import StrEnum
from typing import Annotated, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator

PositiveInt = Annotated[int, Field(gt=0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
PositiveFloat = Annotated[float, Field(gt=0)]

_SECRET_BYTES = 32


class SmtpSecurity(StrEnum):
    """Supported SMTP transport-security modes."""

    PLAIN = "plain"
    STARTTLS = "starttls"
    TLS = "tls"


def _encode_urlsafe(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _decode_canonical_secret(value: str, *, name: str) -> bytes:
    try:
        raw_ascii = value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{name} must use canonical Base64URL ASCII") from exc

    padding = b"=" * (-len(raw_ascii) % 4)
    try:
        decoded = b64decode(raw_ascii + padding, altchars=b"-_", validate=True)
    except (BinasciiError, ValueError) as exc:
        raise ValueError(f"{name} must use canonical unpadded Base64URL") from exc

    if len(decoded) != _SECRET_BYTES:
        raise ValueError(f"{name} must decode to exactly {_SECRET_BYTES} bytes")
    if _encode_urlsafe(decoded) != value:
        raise ValueError(f"{name} must use canonical unpadded Base64URL")
    return decoded


def _normalize_base_url(value: str, *, name: str) -> str:
    candidate = value.strip()
    parts = urlsplit(candidate)
    scheme = parts.scheme.lower()
    hostname = parts.hostname

    if scheme not in {"http", "https"}:
        raise ValueError(f"{name} must use http or https")
    if hostname is None or parts.username is not None or parts.password is not None:
        raise ValueError(f"{name} must be an origin/base URL without userinfo")
    if parts.query or parts.fragment or parts.path not in {"", "/"}:
        raise ValueError(f"{name} must not contain path, query or fragment")

    try:
        canonical_host = hostname.encode("ascii").decode("ascii").lower()
    except UnicodeEncodeError as exc:
        raise ValueError(f"{name} host must use canonical ASCII/IDNA form") from exc

    try:
        port = parts.port
    except ValueError as exc:
        raise ValueError(f"{name} contains an invalid port") from exc

    default_port = 443 if scheme == "https" else 80
    host_for_authority = f"[{canonical_host}]" if ":" in canonical_host else canonical_host
    authority = (
        host_for_authority
        if port is None or port == default_port
        else f"{host_for_authority}:{port}"
    )
    return f"{scheme}://{authority}"


def _trimmed_identity(value: str, *, name: str) -> str:
    if not value or value.strip() != value or any(character in value for character in "\r\n"):
        raise ValueError(f"{name} must be non-blank, trimmed and single-line")
    return value


def _smtp_host(value: str) -> str:
    value = _trimmed_identity(value, name="smtp_host")
    if "://" in value or any(character.isspace() for character in value):
        raise ValueError("smtp_host must be a bare host name/address")
    return value


def _smtp_mailbox(value: str) -> str:
    value = _trimmed_identity(value, name="smtp_from_address")
    if any(character.isspace() for character in value) or value.count("@") != 1:
        raise ValueError("smtp_from_address must be one bare mailbox address")
    local_part, domain = value.rsplit("@", 1)
    if not local_part or not domain:
        raise ValueError("smtp_from_address must be one bare mailbox address")
    return value


class AuthSettings(BaseModel):
    """Immutable Auth runtime policy/configuration constructed at process bootstrap."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    canonical_web_origin: str
    password_current_pepper_key_id: str
    password_peppers: dict[str, SecretStr]
    csrf_key: SecretStr

    signup_otp_current_key_id: str
    signup_otp_keys: dict[str, SecretStr]

    smtp_host: str
    smtp_port: PositiveInt = 587
    smtp_security: SmtpSecurity = SmtpSecurity.STARTTLS
    smtp_username: str | None = None
    smtp_password: SecretStr | None = None
    smtp_from_address: str
    smtp_timeout_seconds: PositiveFloat = 5.0
    email_queue_capacity: PositiveInt = 256
    email_worker_count: PositiveInt = 2
    email_shutdown_drain_seconds: PositiveFloat = 10.0

    session_max_age_seconds: PositiveInt = 2_592_000
    session_idle_timeout_seconds: PositiveInt = 2_592_000
    recent_auth_window_seconds: PositiveInt = 600

    signup_lifetime_seconds: PositiveInt = 86_400
    signup_otp_lifetime_seconds: PositiveInt = 900
    signup_resend_cooldown_seconds: PositiveInt = 60
    recovery_lifetime_seconds: PositiveInt = 1_800
    recovery_response_floor_seconds: PositiveFloat = 0.25

    kdf_max_concurrency: PositiveInt
    kdf_max_queue_depth: NonNegativeInt = 4
    kdf_queue_timeout_seconds: PositiveFloat = 1.0

    signin_rate_capacity: PositiveInt
    signin_rate_window_seconds: PositiveFloat
    signin_rate_max_keys: PositiveInt = 10_000

    signup_rate_capacity: PositiveInt = 5
    signup_rate_window_seconds: PositiveFloat = 3_600
    signup_source_rate_capacity: PositiveInt = 30
    signup_source_rate_window_seconds: PositiveFloat = 3_600
    recovery_rate_capacity: PositiveInt = 5
    recovery_rate_window_seconds: PositiveFloat = 3_600
    recovery_source_rate_capacity: PositiveInt = 30
    recovery_source_rate_window_seconds: PositiveFloat = 3_600
    reauth_rate_capacity: PositiveInt = 10
    reauth_rate_window_seconds: PositiveFloat = 300
    lifecycle_rate_max_keys: PositiveInt = 20_000

    hibp_base_url: str = "https://api.pwnedpasswords.com"
    hibp_timeout_seconds: PositiveFloat = 2.0
    hibp_max_response_bytes: PositiveInt = 131_072
    hibp_max_connections: PositiveInt = 8

    @field_validator("canonical_web_origin")
    @classmethod
    def validate_canonical_web_origin(cls, value: str) -> str:
        """Canonicalize the exact browser origin used by Origin checks."""
        return _normalize_base_url(value, name="canonical_web_origin")

    @field_validator("hibp_base_url")
    @classmethod
    def validate_hibp_base_url(cls, value: str) -> str:
        """Canonicalize the Pwned Passwords API base URL."""
        return _normalize_base_url(value, name="hibp_base_url")

    @field_validator("password_current_pepper_key_id", "signup_otp_current_key_id")
    @classmethod
    def validate_current_key_id(cls, value: str) -> str:
        """Reject blank or whitespace-mutated security-key identifiers."""
        return _trimmed_identity(value, name="security key id")

    @field_validator("smtp_host")
    @classmethod
    def validate_smtp_host(cls, value: str) -> str:
        """Reject URL/userinfo/whitespace SMTP host configuration."""
        return _smtp_host(value)

    @field_validator("smtp_from_address")
    @classmethod
    def validate_smtp_from_address(cls, value: str) -> str:
        """Keep the configured envelope/header sender injection-safe."""
        return _smtp_mailbox(value)

    @field_validator("smtp_username")
    @classmethod
    def validate_smtp_username(cls, value: str | None) -> str | None:
        """Reject ambiguous SMTP usernames while allowing no-auth transports."""
        if value is None:
            return None
        return _trimmed_identity(value, name="smtp_username")

    @model_validator(mode="after")
    def validate_secret_rings_and_transport(self) -> Self:
        """Validate exact key encoding/routing, purpose separation and SMTP auth pairing."""
        if not self.password_peppers:
            raise ValueError("password_peppers must contain at least one key")
        if self.password_current_pepper_key_id not in self.password_peppers:
            raise ValueError("password_current_pepper_key_id is absent from password_peppers")
        if not self.signup_otp_keys:
            raise ValueError("signup_otp_keys must contain at least one key")
        if self.signup_otp_current_key_id not in self.signup_otp_keys:
            raise ValueError("signup_otp_current_key_id is absent from signup_otp_keys")

        pepper_bytes = self._decode_ring(self.password_peppers, name="password_peppers")
        otp_bytes = self._decode_ring(self.signup_otp_keys, name="signup_otp_keys")
        csrf_bytes = _decode_canonical_secret(
            self.csrf_key.get_secret_value(),
            name="csrf_key",
        )

        if len(set(pepper_bytes.values())) != len(pepper_bytes):
            raise ValueError("password_peppers must not alias secret material across key ids")
        if len(set(otp_bytes.values())) != len(otp_bytes):
            raise ValueError("signup_otp_keys must not alias secret material across key ids")

        all_peppers = set(pepper_bytes.values())
        all_otp_keys = set(otp_bytes.values())
        if csrf_bytes in all_peppers or csrf_bytes in all_otp_keys or all_peppers & all_otp_keys:
            raise ValueError("Auth security keys must be distinct across cryptographic purposes")

        if (self.smtp_username is None) != (self.smtp_password is None):
            raise ValueError("smtp_username and smtp_password must be configured together")

        if self.signup_otp_lifetime_seconds > self.signup_lifetime_seconds:
            raise ValueError("signup OTP lifetime cannot exceed pending signup lifetime")
        if self.signup_resend_cooldown_seconds >= self.signup_lifetime_seconds:
            raise ValueError("signup resend cooldown must be shorter than signup lifetime")

        return self

    @staticmethod
    def _decode_ring(values: dict[str, SecretStr], *, name: str) -> dict[str, bytes]:
        decoded: dict[str, bytes] = {}
        for key_id, secret in values.items():
            if not key_id or key_id.strip() != key_id or any(
                character in key_id for character in "\r\n"
            ):
                raise ValueError(f"{name} keys must be non-blank, trimmed and single-line")
            decoded[key_id] = _decode_canonical_secret(
                secret.get_secret_value(),
                name=f"{name}[{key_id!r}]",
            )
        return decoded

    @property
    def password_pepper_bytes(self) -> dict[str, bytes]:
        """Return validated decoded pepper bytes keyed by stable non-secret ID."""
        return self._decode_ring(self.password_peppers, name="password_peppers")

    @property
    def signup_otp_key_bytes(self) -> dict[str, bytes]:
        """Return validated decoded signup-OTP HMAC keys by stable non-secret ID."""
        return self._decode_ring(self.signup_otp_keys, name="signup_otp_keys")

    @property
    def csrf_key_bytes(self) -> bytes:
        """Return the validated decoded CSRF derivation key."""
        return _decode_canonical_secret(self.csrf_key.get_secret_value(), name="csrf_key")
