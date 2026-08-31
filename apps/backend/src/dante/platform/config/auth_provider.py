"""Frozen M5 provider, network and WebAuthn configuration."""

from __future__ import annotations

from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from ipaddress import ip_address
from typing import Annotated, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator

PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0)]

GOOGLE_ISSUER = "https://accounts.google.com"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
APPLE_ISSUER = "https://appleid.apple.com"
APPLE_JWKS_URL = "https://appleid.apple.com/auth/keys"
APPLE_AUTHORIZE_URL = "https://appleid.apple.com/auth/authorize"
# Public OAuth endpoint; Ruff's password-name heuristic is a false positive here.
APPLE_TOKEN_URL = "https://appleid.apple.com/auth/token"  # noqa: S105
APPLE_REVOKE_URL = "https://appleid.apple.com/auth/revoke"
_ALLOWED_PROVIDER_ALGORITHMS = ("RS256",)
_SECRET_BYTES = 32


def _trimmed(value: str, *, name: str) -> str:
    if not value or value.strip() != value or any(char in value for char in "\r\n"):
        raise ValueError(f"{name} must be non-blank, trimmed and single-line")
    return value


def _canonical_url(value: str, *, name: str, origin_only: bool = False) -> str:
    candidate = value.strip()
    parts = urlsplit(candidate)
    if parts.scheme not in {"http", "https"} or parts.hostname is None:
        raise ValueError(f"{name} must be an absolute HTTP(S) URL")
    if parts.username is not None or parts.password is not None or parts.fragment:
        raise ValueError(f"{name} must not contain userinfo or fragment")
    if origin_only and (parts.path not in {"", "/"} or parts.query):
        raise ValueError(f"{name} must be an origin")
    return candidate.rstrip("/") if origin_only else candidate


def _apple_redirect_uri(value: str) -> str:
    candidate = _canonical_url(value, name="Apple redirect URI")
    parts = urlsplit(candidate)
    if parts.scheme != "https" or parts.hostname is None or parts.query:
        raise ValueError("Apple redirect URI must be an exact HTTPS URL without query")
    if parts.hostname == "localhost":
        raise ValueError("Apple redirect URI cannot use localhost")
    try:
        ip_address(parts.hostname)
    except ValueError:
        pass
    else:
        raise ValueError("Apple redirect URI must use a registered domain, not an IP address")
    return candidate


def _decode_key(value: str, *, name: str) -> bytes:
    try:
        encoded = value.encode("ascii")
        decoded = b64decode(encoded + b"=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
    except (UnicodeEncodeError, BinasciiError, ValueError) as exc:
        raise ValueError(f"{name} must use canonical unpadded Base64URL") from exc
    canonical = urlsafe_b64encode(decoded).rstrip(b"=").decode("ascii")
    if len(decoded) != _SECRET_BYTES or canonical != value:
        raise ValueError(f"{name} must be canonical Base64URL for exactly 32 bytes")
    return decoded


class ProviderNetworkSettings(BaseModel):
    """Bounded provider HTTP/JWK cache policy."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    connect_timeout_seconds: PositiveFloat = 2.0
    read_timeout_seconds: PositiveFloat = 3.0
    write_timeout_seconds: PositiveFloat = 3.0
    pool_timeout_seconds: PositiveFloat = 1.0
    max_connections: PositiveInt = 8
    max_keepalive_connections: PositiveInt = 4
    max_jwks_response_bytes: PositiveInt = 262_144
    max_jwk_count: PositiveInt = 32
    default_jwk_ttl_seconds: PositiveInt = 300
    max_jwk_ttl_seconds: PositiveInt = 86_400
    unknown_kid_refresh_cooldown_seconds: PositiveFloat = 5.0
    max_compact_token_bytes: PositiveInt = 16_384
    max_protected_header_bytes: PositiveInt = 4_096

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        if self.max_keepalive_connections > self.max_connections:
            raise ValueError("provider keepalive connections cannot exceed max connections")
        if self.default_jwk_ttl_seconds > self.max_jwk_ttl_seconds:
            raise ValueError("default JWK TTL cannot exceed maximum JWK TTL")
        if self.max_protected_header_bytes >= self.max_compact_token_bytes:
            raise ValueError("protected-header bound must be smaller than compact-token bound")
        return self


class GoogleProviderSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    client_id: str | None = None
    issuer: str = GOOGLE_ISSUER
    jwks_url: str = GOOGLE_JWKS_URL
    allowed_algorithms: tuple[str, ...] = _ALLOWED_PROVIDER_ALGORITHMS

    @field_validator("issuer", "jwks_url")
    @classmethod
    def validate_urls(cls, value: str) -> str:
        return _canonical_url(value, name="Google authority URL")

    @model_validator(mode="after")
    def validate_enabled(self) -> Self:
        if self.allowed_algorithms != _ALLOWED_PROVIDER_ALGORITHMS:
            raise ValueError("Google allowed_algorithms is frozen to RS256")
        if self.enabled and self.client_id is None:
            raise ValueError("enabled Google authentication requires client_id")
        if self.client_id is not None:
            _trimmed(self.client_id, name="Google client_id")
        return self


class AppleProviderSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    client_id: str | None = None
    team_id: str | None = None
    key_id: str | None = None
    client_private_key_pem: SecretStr | None = None
    redirect_uri: str | None = None
    issuer: str = APPLE_ISSUER
    jwks_url: str = APPLE_JWKS_URL
    authorize_url: str = APPLE_AUTHORIZE_URL
    token_url: str = APPLE_TOKEN_URL
    revoke_url: str = APPLE_REVOKE_URL
    allowed_algorithms: tuple[str, ...] = _ALLOWED_PROVIDER_ALGORITHMS
    grant_encryption_current_key_id: str | None = None
    grant_encryption_keys: dict[str, SecretStr] = Field(default_factory=dict)

    @field_validator("issuer", "jwks_url", "authorize_url", "token_url", "revoke_url")
    @classmethod
    def validate_urls(cls, value: str) -> str:
        return _canonical_url(value, name="Apple authority URL")

    @field_validator("redirect_uri")
    @classmethod
    def validate_redirect_uri(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _apple_redirect_uri(value)

    @field_validator("client_id", "team_id", "key_id")
    @classmethod
    def validate_optional_identity(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _trimmed(value, name="Apple provider identity")

    @model_validator(mode="after")
    def validate_configuration(self) -> Self:
        if self.allowed_algorithms != _ALLOWED_PROVIDER_ALGORITHMS:
            raise ValueError("Apple allowed_algorithms is frozen to RS256")

        if self.client_private_key_pem is not None:
            private_key = self.client_private_key_pem.get_secret_value()
            if not private_key.strip() or "\x00" in private_key:
                raise ValueError("Apple client private key must be non-blank PEM material")

        decoded: dict[str, bytes] = {}
        for key_id, value in self.grant_encryption_keys.items():
            _trimmed(key_id, name="Apple grant key id")
            decoded[key_id] = _decode_key(
                value.get_secret_value(), name=f"Apple grant key {key_id}"
            )
        if len(set(decoded.values())) != len(decoded):
            raise ValueError("Apple grant key ids must not alias key material")
        if self.grant_encryption_current_key_id is not None:
            _trimmed(self.grant_encryption_current_key_id, name="Apple current grant key id")
            if self.grant_encryption_current_key_id not in decoded:
                raise ValueError("Apple current grant key id is absent from key ring")
        if self.enabled:
            required = (
                self.client_id,
                self.team_id,
                self.key_id,
                self.client_private_key_pem,
                self.redirect_uri,
            )
            if any(value is None for value in required):
                raise ValueError(
                    "enabled Apple authentication requires client/team/key/private-key/redirect config"
                )
            if self.grant_encryption_current_key_id is None:
                raise ValueError(
                    "enabled Apple authentication requires a current grant encryption key"
                )
        return self

    @property
    def grant_encryption_key_bytes(self) -> dict[str, bytes]:
        return {
            key_id: _decode_key(secret.get_secret_value(), name=f"Apple grant key {key_id}")
            for key_id, secret in self.grant_encryption_keys.items()
        }


class WebAuthnSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    enabled: bool = False
    rp_id: str = "localhost"
    rp_name: str = "DANTE"
    expected_origins: tuple[str, ...] = ("https://localhost:5173",)

    @field_validator("rp_id", "rp_name")
    @classmethod
    def validate_identity(cls, value: str) -> str:
        return _trimmed(value, name="WebAuthn RP identity")

    @field_validator("expected_origins")
    @classmethod
    def validate_origins(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if not values:
            raise ValueError("WebAuthn expected_origins must not be empty")
        canonical = tuple(
            _canonical_url(value, name="WebAuthn origin", origin_only=True) for value in values
        )
        if len(set(canonical)) != len(canonical):
            raise ValueError("WebAuthn expected_origins must be unique")
        return canonical


class AuthProviderSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    network: ProviderNetworkSettings = Field(default_factory=ProviderNetworkSettings)
    google: GoogleProviderSettings = Field(default_factory=GoogleProviderSettings)
    apple: AppleProviderSettings = Field(default_factory=AppleProviderSettings)
    webauthn: WebAuthnSettings = Field(default_factory=WebAuthnSettings)
