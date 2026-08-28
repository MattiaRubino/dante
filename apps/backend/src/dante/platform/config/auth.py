"""Validated process configuration for the DANTE Access/Auth runtime."""

from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from typing import Annotated, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator

PositiveInt = Annotated[int, Field(gt=0)]
NonNegativeInt = Annotated[int, Field(ge=0)]
PositiveFloat = Annotated[float, Field(gt=0)]

_SECRET_BYTES = 32


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


class AuthSettings(BaseModel):
    """Immutable Auth runtime policy/configuration constructed at process bootstrap."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    canonical_web_origin: str
    password_current_pepper_key_id: str
    password_peppers: dict[str, SecretStr]
    csrf_key: SecretStr

    session_max_age_seconds: PositiveInt = 2_592_000
    session_idle_timeout_seconds: PositiveInt = 2_592_000

    kdf_max_concurrency: PositiveInt
    kdf_max_queue_depth: NonNegativeInt = 4
    kdf_queue_timeout_seconds: PositiveFloat = 1.0

    signin_rate_capacity: PositiveInt
    signin_rate_window_seconds: PositiveFloat
    signin_rate_max_keys: PositiveInt = 10_000

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

    @field_validator("password_current_pepper_key_id")
    @classmethod
    def validate_current_pepper_key_id(cls, value: str) -> str:
        """Reject blank or whitespace-mutated pepper identifiers."""
        stripped = value.strip()
        if not stripped or stripped != value:
            raise ValueError("password_current_pepper_key_id must be non-blank and trimmed")
        return value

    @model_validator(mode="after")
    def validate_secret_ring(self) -> Self:
        """Validate exact key encoding, routing and purpose separation."""
        if not self.password_peppers:
            raise ValueError("password_peppers must contain at least one key")
        if self.password_current_pepper_key_id not in self.password_peppers:
            raise ValueError("password_current_pepper_key_id is absent from password_peppers")

        pepper_bytes: list[bytes] = []
        for key_id, secret in self.password_peppers.items():
            if not key_id or key_id.strip() != key_id:
                raise ValueError("password_peppers keys must be non-blank and trimmed")
            pepper_bytes.append(
                _decode_canonical_secret(
                    secret.get_secret_value(),
                    name=f"password_peppers[{key_id!r}]",
                )
            )

        csrf_bytes = _decode_canonical_secret(
            self.csrf_key.get_secret_value(),
            name="csrf_key",
        )
        if any(csrf_bytes == pepper for pepper in pepper_bytes):
            raise ValueError("csrf_key must be distinct from every password pepper")

        return self

    @property
    def password_pepper_bytes(self) -> dict[str, bytes]:
        """Return validated decoded pepper bytes keyed by stable non-secret ID."""
        return {
            key_id: _decode_canonical_secret(
                secret.get_secret_value(),
                name=f"password_peppers[{key_id!r}]",
            )
            for key_id, secret in self.password_peppers.items()
        }

    @property
    def csrf_key_bytes(self) -> bytes:
        """Return the validated decoded CSRF derivation key."""
        return _decode_canonical_secret(self.csrf_key.get_secret_value(), name="csrf_key")
