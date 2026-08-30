"""Google OIDC trust-boundary validation for DANTE Access/Auth."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urlsplit

from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email
from dante.auth.jose import JoseBoundaryError, parse_compact_header, verify_compact_jwt
from dante.auth.proofs import FlowProofPurpose, flow_proof_matches
from dante.auth.provider_runtime import ProviderRuntime, ProviderRuntimeError
from dante.platform.config.auth_provider import GOOGLE_ISSUER, AuthProviderSettings

_GOOGLE_ISSUER_ALIASES = frozenset({"accounts.google.com", GOOGLE_ISSUER})
_MAX_AUDIENCES = 8
_MAX_HOSTED_DOMAIN_LENGTH = 253
_MAX_PROFILE_NAME_LENGTH = 256
_MAX_PROFILE_PART_LENGTH = 128
_MAX_LOCALE_LENGTH = 64
_MAX_PICTURE_URL_LENGTH = 2048
_MAX_IAT_FUTURE_SKEW_SECONDS = 60


class GoogleProofError(ValueError):
    """Google credential failed protocol/claim validation."""


class GoogleProviderUnavailableError(RuntimeError):
    """Google trust material could not be obtained safely."""


@dataclass(frozen=True, slots=True)
class GoogleIdentityEvidence:
    """Verified Google identity/security evidence plus bounded bootstrap metadata."""

    issuer: str
    subject: str
    email: NormalizedEmail | None
    email_verified: bool
    hosted_domain: str | None
    mailbox_authoritative: bool
    display_name: str | None
    given_name: str | None
    family_name: str | None
    picture_url: str | None
    locale: str | None


class GoogleTokenVerifier:
    """Verify Google compact ID tokens using only the trusted M5-B runtime."""

    def __init__(
        self,
        *,
        settings: AuthProviderSettings,
        provider_runtime: ProviderRuntime,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._settings = settings
        self._provider_runtime = provider_runtime
        self._now = now or (lambda: datetime.now(UTC))

    async def verify(
        self,
        token: str,
        *,
        expected_nonce_verifier: bytes,
    ) -> GoogleIdentityEvidence:
        """Verify signature, provider claims and DANTE nonce binding."""
        google = self._settings.google
        client_id = google.client_id
        if not google.enabled or client_id is None:
            raise GoogleProviderUnavailableError("Google authentication is not enabled")

        network = self._settings.network
        try:
            header = parse_compact_header(
                token,
                allowed_algorithms=google.allowed_algorithms,
                max_token_bytes=network.max_compact_token_bytes,
                max_header_bytes=network.max_protected_header_bytes,
            )
        except JoseBoundaryError as exc:
            raise GoogleProofError("Google ID token failed JOSE admission") from exc

        try:
            jwk = await self._provider_runtime.jwk_for_kid(provider="google", kid=header.kid)
        except ProviderRuntimeError as exc:
            raise GoogleProviderUnavailableError("Google JWK resolution failed") from exc

        try:
            verified = verify_compact_jwt(
                token,
                trusted_jwks={"keys": [jwk]},
                allowed_algorithms=google.allowed_algorithms,
                max_token_bytes=network.max_compact_token_bytes,
                max_header_bytes=network.max_protected_header_bytes,
            )
        except JoseBoundaryError as exc:
            raise GoogleProofError("Google ID token signature verification failed") from exc

        return self._validate_claims(
            verified.claims,
            client_id=client_id,
            expected_nonce_verifier=expected_nonce_verifier,
        )

    def _validate_claims(
        self,
        claims: dict[str, object],
        *,
        client_id: str,
        expected_nonce_verifier: bytes,
    ) -> GoogleIdentityEvidence:
        issuer = claims.get("iss")
        if not isinstance(issuer, str) or issuer not in _GOOGLE_ISSUER_ALIASES:
            raise GoogleProofError("Google issuer is invalid")

        subject = self._required_string(claims, "sub", maximum=255)
        audiences = self._audiences(claims.get("aud"))
        if client_id not in audiences:
            raise GoogleProofError("Google audience is invalid")

        azp = claims.get("azp")
        if len(audiences) > 1:
            if azp != client_id:
                raise GoogleProofError("Google authorized party is required for multiple audiences")
        elif azp is not None and azp != client_id:
            raise GoogleProofError("Google authorized party is invalid")

        now_timestamp = self._now().timestamp()
        expires_at = self._numeric_date(claims.get("exp"), name="exp")
        if expires_at <= now_timestamp:
            raise GoogleProofError("Google ID token is expired")

        issued_at_claim = claims.get("iat")
        if issued_at_claim is not None:
            issued_at = self._numeric_date(issued_at_claim, name="iat")
            if issued_at > now_timestamp + _MAX_IAT_FUTURE_SKEW_SECONDS:
                raise GoogleProofError("Google ID token issue time is in the future")

        nonce = self._required_string(claims, "nonce", maximum=512)
        if not flow_proof_matches(
            purpose=FlowProofPurpose.OIDC_NONCE,
            encoded_secret=nonce,
            expected_verifier=expected_nonce_verifier,
        ):
            raise GoogleProofError("Google nonce does not match the DANTE transaction")

        email = self._validated_email(claims.get("email"))
        email_verified_claim = claims.get("email_verified")
        if email_verified_claim is None:
            email_verified = False
        elif isinstance(email_verified_claim, bool):
            email_verified = email_verified_claim
        else:
            raise GoogleProofError("Google email_verified claim is invalid")

        hosted_domain = self._hosted_domain(claims.get("hd"))
        mailbox_authoritative = False
        if email is not None and email_verified:
            domain = email.comparison_key.rsplit("@", 1)[1]
            mailbox_authoritative = domain == "gmail.com" or hosted_domain is not None

        return GoogleIdentityEvidence(
            issuer=GOOGLE_ISSUER,
            subject=subject,
            email=email,
            email_verified=email_verified,
            hosted_domain=hosted_domain,
            mailbox_authoritative=mailbox_authoritative,
            display_name=self._profile_text(claims.get("name"), maximum=_MAX_PROFILE_NAME_LENGTH),
            given_name=self._profile_text(
                claims.get("given_name"), maximum=_MAX_PROFILE_PART_LENGTH
            ),
            family_name=self._profile_text(
                claims.get("family_name"), maximum=_MAX_PROFILE_PART_LENGTH
            ),
            picture_url=self._picture_url(claims.get("picture")),
            locale=self._profile_text(claims.get("locale"), maximum=_MAX_LOCALE_LENGTH),
        )

    @staticmethod
    def _required_string(
        claims: dict[str, object],
        name: str,
        *,
        maximum: int,
    ) -> str:
        value = claims.get(name)
        if (
            not isinstance(value, str)
            or not value
            or value.strip() != value
            or len(value) > maximum
            or any(character in value for character in "\r\n")
        ):
            raise GoogleProofError(f"Google {name} claim is invalid")
        return value

    @staticmethod
    def _numeric_date(value: object, *, name: str) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise GoogleProofError(f"Google {name} claim is invalid")
        converted = float(value)
        if not math.isfinite(converted) or converted < 0:
            raise GoogleProofError(f"Google {name} claim is invalid")
        return converted

    @staticmethod
    def _audiences(value: object) -> tuple[str, ...]:
        if isinstance(value, str):
            values = (value,)
        elif (
            isinstance(value, list)
            and 1 <= len(value) <= _MAX_AUDIENCES
            and all(isinstance(item, str) for item in value)
        ):
            values = tuple(value)
        else:
            raise GoogleProofError("Google aud claim is invalid")

        if (
            any(not item or item.strip() != item or len(item) > 512 for item in values)
            or len(set(values)) != len(values)
        ):
            raise GoogleProofError("Google aud claim is invalid")
        return values

    @staticmethod
    def _validated_email(value: object) -> NormalizedEmail | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise GoogleProofError("Google email claim is invalid")
        try:
            return normalize_email(value)
        except EmailNormalizationError as exc:
            raise GoogleProofError("Google email claim is invalid") from exc

    @staticmethod
    def _hosted_domain(value: object) -> str | None:
        if value is None:
            return None
        if (
            not isinstance(value, str)
            or not value
            or value.strip() != value
            or len(value) > _MAX_HOSTED_DOMAIN_LENGTH
            or any(character in value for character in "\r\n")
        ):
            raise GoogleProofError("Google hd claim is invalid")
        return value.casefold()

    @staticmethod
    def _profile_text(value: object, *, maximum: int) -> str | None:
        if not isinstance(value, str):
            return None
        candidate = value.strip()
        if not candidate or len(candidate) > maximum or any(char in candidate for char in "\r\n"):
            return None
        return candidate

    @staticmethod
    def _picture_url(value: object) -> str | None:
        if not isinstance(value, str):
            return None
        candidate = value.strip()
        if not candidate or len(candidate) > _MAX_PICTURE_URL_LENGTH:
            return None
        parts = urlsplit(candidate)
        if (
            parts.scheme != "https"
            or parts.hostname is None
            or parts.username is not None
            or parts.password is not None
        ):
            return None
        return candidate
