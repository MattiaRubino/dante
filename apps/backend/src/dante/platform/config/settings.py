"""Typed, immutable bootstrap configuration for the DANTE backend."""

from enum import StrEnum
from typing import Annotated, Self
from urllib.parse import urlsplit

from pydantic import StringConstraints, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.auth_provider import (
    APPLE_AUTHORIZE_URL,
    APPLE_ISSUER,
    APPLE_JWKS_URL,
    APPLE_REVOKE_URL,
    APPLE_TOKEN_URL,
    GOOGLE_ISSUER,
    GOOGLE_JWKS_URL,
)
from dante.platform.config.database import DatabaseSettings

IdentityValue = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Environment(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    UAT = "uat"
    PROD = "prod"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DANTE_",
        env_nested_delimiter="__",
        extra="forbid",
        frozen=True,
    )

    env: Environment
    release_sha: IdentityValue
    build_id: IdentityValue
    debug: bool = False
    database: DatabaseSettings
    auth: AuthSettings

    @model_validator(mode="after")
    def validate_environment_safety(self) -> Self:
        if self.env is Environment.PROD and self.debug:
            raise ValueError("DANTE_DEBUG must be false when DANTE_ENV=prod")
        if self.env is not Environment.LOCAL:
            if self.release_sha.casefold() == "local":
                raise ValueError("DANTE_RELEASE_SHA=local is allowed only when DANTE_ENV=local")
            if self.build_id.casefold() == "local":
                raise ValueError("DANTE_BUILD_ID=local is allowed only when DANTE_ENV=local")
            if urlsplit(self.auth.canonical_web_origin).scheme != "https":
                raise ValueError("non-local canonical Web origin must use HTTPS")
            if urlsplit(self.auth.hibp_base_url).scheme != "https":
                raise ValueError("non-local HIBP base URL must use HTTPS")
            if self.auth.smtp_security is SmtpSecurity.PLAIN:
                raise ValueError("non-local SMTP transport must use STARTTLS or implicit TLS")

            google = self.auth.provider.google
            if google.enabled and (google.issuer != GOOGLE_ISSUER or google.jwks_url != GOOGLE_JWKS_URL):
                raise ValueError("non-local Google authority endpoints are frozen to canonical values")

            apple = self.auth.provider.apple
            if apple.enabled and (
                apple.issuer != APPLE_ISSUER
                or apple.jwks_url != APPLE_JWKS_URL
                or apple.authorize_url != APPLE_AUTHORIZE_URL
                or apple.token_url != APPLE_TOKEN_URL
                or apple.revoke_url != APPLE_REVOKE_URL
            ):
                raise ValueError("non-local Apple authority endpoints are frozen to canonical values")

            webauthn = self.auth.provider.webauthn
            if webauthn.enabled:
                if webauthn.rp_id == "localhost":
                    raise ValueError("non-local WebAuthn RP ID cannot be localhost")
                if self.auth.canonical_web_origin not in webauthn.expected_origins:
                    raise ValueError("canonical Web origin must be an allowed WebAuthn origin")
                if any(urlsplit(origin).scheme != "https" for origin in webauthn.expected_origins):
                    raise ValueError("non-local WebAuthn origins must use HTTPS")
        return self
