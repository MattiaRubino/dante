"""Sign in with Apple protocol/trust boundary for DANTE Access/Auth."""

from __future__ import annotations

import hmac
import json
import math
from base64 import urlsafe_b64encode
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from urllib.parse import urlencode, urlsplit

from joserfc import jwt
from joserfc.jwk import ECKey
from pydantic import SecretStr

from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email
from dante.auth.jose import JoseBoundaryError, parse_compact_header, verify_compact_jwt
from dante.auth.proofs import FlowProofPurpose, flow_proof_matches
from dante.auth.provider_runtime import (
    ProviderMutationAmbiguousError,
    ProviderRuntime,
    ProviderRuntimeError,
)
from dante.platform.config.auth_provider import APPLE_ISSUER, AuthProviderSettings

_PRIVATE_EMAIL_DOMAINS = frozenset({"privaterelay.appleid.com", "private.icloud.com"})
_MAX_CLOCK_SKEW_SECONDS = 60
_MAX_CODE_BYTES = 4096
_MAX_PROFILE_JSON_BYTES = 8192
_MAX_PROFILE_PART_LENGTH = 128
_MAX_NOTIFICATION_EVENTS_BYTES = 8192
_MAX_NOTIFICATION_JTI_LENGTH = 512
_CLIENT_SECRET_TTL = timedelta(minutes=5)
_CLIENT_SECRET_MAX_TTL = timedelta(seconds=15_777_000)
_KNOWN_NOTIFICATION_TYPES = frozenset(
    {"email-disabled", "email-enabled", "consent-revoked", "account-deleted"}
)


class AppleProofError(ValueError):
    """Apple-signed evidence failed DANTE protocol/claim validation."""


class AppleProtocolError(ValueError):
    """Apple returned a conclusive OAuth/protocol failure."""

    def __init__(self, code: str) -> None:
        super().__init__("Apple protocol request failed")
        self.code = code


class AppleProviderUnavailableError(RuntimeError):
    """Apple trust material or provider transport is unavailable."""


class AppleExchangeAmbiguousError(RuntimeError):
    """The single-use Apple authorization-code exchange lost a conclusive result."""


@dataclass(frozen=True, slots=True)
class AppleIdentityEvidence:
    """Verified Apple identity evidence plus signed mailbox semantics."""

    issuer: str
    subject: str
    email: NormalizedEmail | None
    email_verified: bool
    email_private: bool | None
    mailbox_authoritative: bool

    def __post_init__(self) -> None:
        if self.email is None:
            if self.email_verified or self.email_private is not None or self.mailbox_authoritative:
                raise AppleProofError("Apple email metadata requires an email claim")
            return
        if self.email_private is None:
            object.__setattr__(self, "email_private", False)
        if self.mailbox_authoritative and not self.email_verified:
            raise AppleProofError("Apple mailbox authority requires verified email evidence")


@dataclass(frozen=True, slots=True)
class AppleAuthorizationProfile:
    """One-shot, unsigned-but-provider-delivered profile bootstrap candidate."""

    given_name: str | None
    family_name: str | None
    email: NormalizedEmail | None

    @property
    def display_name(self) -> str | None:
        parts = [part for part in (self.given_name, self.family_name) if part]
        return " ".join(parts) or None


@dataclass(frozen=True, slots=True)
class AppleTokenResponse:
    """Successful Apple code exchange with only the material DANTE consumes."""

    id_token: str
    refresh_token: SecretStr


@dataclass(frozen=True, slots=True)
class AppleNotificationEvent:
    """One verified Sign in with Apple server-to-server lifecycle event."""

    event_type: str
    subject: str
    event_time: datetime
    email: NormalizedEmail | None
    email_private: bool | None
    jti: str

    @property
    def known(self) -> bool:
        return self.event_type in _KNOWN_NOTIFICATION_TYPES


@dataclass(frozen=True, slots=True)
class AppleAuthenticationBegun:
    """Persisted Apple transaction represented by one exact provider authorization URL."""

    authorization_url: str
    expires_at: datetime


class AppleClientSecretSigner:
    """Issue short-lived ES256 client assertions from the configured Apple .p8 key."""

    def __init__(
        self,
        *,
        team_id: str,
        key_id: str,
        client_id: str,
        private_key_pem: SecretStr,
        now: Callable[[], datetime] | None = None,
        ttl: timedelta = _CLIENT_SECRET_TTL,
    ) -> None:
        if ttl <= timedelta(0) or ttl > _CLIENT_SECRET_MAX_TTL:
            raise ValueError("Apple client-secret lifetime is outside Apple's admitted bound")
        self._team_id = team_id
        self._key_id = key_id
        self._client_id = client_id
        self._now = now or (lambda: datetime.now(UTC))
        self._ttl = ttl
        try:
            self._key = ECKey.import_key(private_key_pem.get_secret_value())
        except Exception as exc:
            raise ValueError("Apple client private key is not a valid EC private key") from exc

    def issue(self) -> SecretStr:
        now = self._now()
        claims = {
            "iss": self._team_id,
            "iat": int(now.timestamp()),
            "exp": int((now + self._ttl).timestamp()),
            "aud": APPLE_ISSUER,
            "sub": self._client_id,
        }
        try:
            encoded = jwt.encode(
                {"alg": "ES256", "kid": self._key_id},
                claims,
                self._key,
                algorithms=["ES256"],
            )
        except Exception as exc:
            raise AppleProviderUnavailableError("Apple client-secret signing failed") from exc
        return SecretStr(encoded)


class AppleProtocolClient:
    """Single-attempt Apple token/revoke protocol over the shared bounded ProviderRuntime."""

    def __init__(
        self,
        *,
        settings: AuthProviderSettings,
        provider_runtime: ProviderRuntime,
        signer: AppleClientSecretSigner,
    ) -> None:
        self._settings = settings
        self._runtime = provider_runtime
        self._signer = signer

    async def exchange_code(self, code: str) -> AppleTokenResponse:
        apple = self._settings.apple
        client_id = apple.client_id
        redirect_uri = apple.redirect_uri
        if not apple.enabled or client_id is None or redirect_uri is None:
            raise AppleProviderUnavailableError("Apple authentication is not enabled")
        if not _canonical_secret(code, maximum=_MAX_CODE_BYTES):
            raise AppleProtocolError("invalid_grant")

        form = {
            "client_id": client_id,
            "client_secret": self._signer.issue().get_secret_value(),
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        try:
            response = await self._runtime.apple_token_exchange(form)
        except ProviderMutationAmbiguousError as exc:
            raise AppleExchangeAmbiguousError("Apple authorization-code exchange is ambiguous") from exc
        except ProviderRuntimeError as exc:
            raise AppleProviderUnavailableError("Apple token endpoint failed safely") from exc

        body = response.body or {}
        if response.status_code != 200:
            raise AppleProtocolError(_protocol_error_code(body))
        id_token = _required_response_string(body, "id_token", maximum=16_384)
        refresh_token = _required_response_string(body, "refresh_token", maximum=16_384)
        return AppleTokenResponse(id_token=id_token, refresh_token=SecretStr(refresh_token))

    async def revoke_refresh_token(self, refresh_token: SecretStr) -> None:
        apple = self._settings.apple
        client_id = apple.client_id
        if not apple.enabled or client_id is None:
            raise AppleProviderUnavailableError("Apple authentication is not enabled")
        token = refresh_token.get_secret_value()
        if not _canonical_secret(token, maximum=16_384):
            raise AppleProtocolError("invalid_token")
        form = {
            "client_id": client_id,
            "client_secret": self._signer.issue().get_secret_value(),
            "token": token,
            "token_type_hint": "refresh_token",
        }
        try:
            response = await self._runtime.apple_revoke(form)
        except ProviderMutationAmbiguousError as exc:
            raise AppleProviderUnavailableError("Apple revoke result is ambiguous") from exc
        except ProviderRuntimeError as exc:
            raise AppleProviderUnavailableError("Apple revoke endpoint failed safely") from exc
        if response.status_code != 200:
            raise AppleProtocolError(_protocol_error_code(response.body or {}))


class AppleTokenVerifier:
    """Verify Apple ID tokens using only trusted Apple JWKS from M5-B."""

    def __init__(
        self,
        *,
        settings: AuthProviderSettings,
        provider_runtime: ProviderRuntime,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._settings = settings
        self._runtime = provider_runtime
        self._now = now or (lambda: datetime.now(UTC))

    async def verify(
        self,
        token: str,
        *,
        expected_nonce_verifier: bytes,
        expected_code: str | None = None,
    ) -> AppleIdentityEvidence:
        apple = self._settings.apple
        client_id = apple.client_id
        if not apple.enabled or client_id is None:
            raise AppleProviderUnavailableError("Apple authentication is not enabled")
        claims = await self._verified_claims(token)
        return self._validate_identity_claims(
            claims,
            client_id=client_id,
            expected_nonce_verifier=expected_nonce_verifier,
            expected_code=expected_code,
        )

    async def _verified_claims(self, token: str) -> dict[str, object]:
        apple = self._settings.apple
        network = self._settings.network
        try:
            header = parse_compact_header(
                token,
                allowed_algorithms=apple.allowed_algorithms,
                max_token_bytes=network.max_compact_token_bytes,
                max_header_bytes=network.max_protected_header_bytes,
            )
        except JoseBoundaryError as exc:
            raise AppleProofError("Apple token failed JOSE admission") from exc
        try:
            jwk = await self._runtime.jwk_for_kid(provider="apple", kid=header.kid)
        except ProviderRuntimeError as exc:
            raise AppleProviderUnavailableError("Apple JWK resolution failed") from exc
        try:
            verified = verify_compact_jwt(
                token,
                trusted_jwks={"keys": [jwk]},
                allowed_algorithms=apple.allowed_algorithms,
                max_token_bytes=network.max_compact_token_bytes,
                max_header_bytes=network.max_protected_header_bytes,
            )
        except JoseBoundaryError as exc:
            raise AppleProofError("Apple token signature verification failed") from exc
        return {str(key): value for key, value in verified.claims.items()}

    def _validate_identity_claims(
        self,
        claims: dict[str, object],
        *,
        client_id: str,
        expected_nonce_verifier: bytes,
        expected_code: str | None,
    ) -> AppleIdentityEvidence:
        if claims.get("iss") != APPLE_ISSUER:
            raise AppleProofError("Apple issuer is invalid")
        if claims.get("aud") != client_id:
            raise AppleProofError("Apple audience is invalid")
        subject = _required_claim_string(claims, "sub", maximum=255)
        now_timestamp = self._now().timestamp()
        expires_at = _numeric_date(claims.get("exp"), name="exp")
        if expires_at <= now_timestamp:
            raise AppleProofError("Apple ID token is expired")
        issued_at = _numeric_date(claims.get("iat"), name="iat")
        if issued_at > now_timestamp + _MAX_CLOCK_SKEW_SECONDS:
            raise AppleProofError("Apple ID token issue time is in the future")

        nonce = _required_claim_string(claims, "nonce", maximum=512)
        if not flow_proof_matches(
            purpose=FlowProofPurpose.OIDC_NONCE,
            encoded_secret=nonce,
            expected_verifier=expected_nonce_verifier,
        ):
            raise AppleProofError("Apple nonce does not match the DANTE transaction")

        if expected_code is not None:
            c_hash = _required_claim_string(claims, "c_hash", maximum=128)
            if not hmac.compare_digest(c_hash, apple_code_hash(expected_code)):
                raise AppleProofError("Apple c_hash does not bind the authorization code")

        email = _validated_email(claims.get("email"))
        email_verified = _optional_apple_bool(claims.get("email_verified"), name="email_verified")
        private_claim = _optional_apple_bool(claims.get("is_private_email"), name="is_private_email")
        email_private: bool | None = None
        if email is not None:
            domain = email.comparison_key.rsplit("@", 1)[1]
            email_private = bool(private_claim) or domain in _PRIVATE_EMAIL_DOMAINS
        elif private_claim is not None:
            raise AppleProofError("Apple private-email claim requires an email claim")

        return AppleIdentityEvidence(
            issuer=APPLE_ISSUER,
            subject=subject,
            email=email,
            email_verified=email_verified is True,
            email_private=email_private,
            mailbox_authoritative=email is not None and email_verified is True,
        )


class AppleNotificationVerifier(AppleTokenVerifier):
    """Verify and normalize one Apple server-to-server lifecycle notification."""

    async def verify_notification(self, token: str) -> AppleNotificationEvent:
        apple = self._settings.apple
        client_id = apple.client_id
        if not apple.enabled or client_id is None:
            raise AppleProviderUnavailableError("Apple authentication is not enabled")
        claims = await self._verified_claims(token)
        if claims.get("iss") != APPLE_ISSUER or claims.get("aud") != client_id:
            raise AppleProofError("Apple notification authority is invalid")
        now_timestamp = self._now().timestamp()
        issued_at = _numeric_date(claims.get("iat"), name="iat")
        if issued_at > now_timestamp + _MAX_CLOCK_SKEW_SECONDS:
            raise AppleProofError("Apple notification issue time is in the future")
        jti = _required_claim_string(claims, "jti", maximum=_MAX_NOTIFICATION_JTI_LENGTH)
        event = _notification_event_object(claims.get("events"))
        event_type = _required_object_string(event, "type", maximum=128)
        subject = _required_object_string(event, "sub", maximum=255)
        event_time = datetime.fromtimestamp(
            _numeric_date(event.get("event_time"), name="event_time"),
            tz=UTC,
        )
        if event_time.timestamp() > now_timestamp + _MAX_CLOCK_SKEW_SECONDS:
            raise AppleProofError("Apple notification event time is in the future")
        email = _validated_email(event.get("email"))
        private_claim = _optional_apple_bool(event.get("is_private_email"), name="is_private_email")
        email_private: bool | None = None
        if email is not None:
            domain = email.comparison_key.rsplit("@", 1)[1]
            email_private = bool(private_claim) or domain in _PRIVATE_EMAIL_DOMAINS
        elif private_claim is not None:
            raise AppleProofError("Apple notification private-email flag requires email")
        return AppleNotificationEvent(
            event_type=event_type,
            subject=subject,
            event_time=event_time,
            email=email,
            email_private=email_private,
            jti=jti,
        )


def build_apple_authorization_url(
    *,
    settings: AuthProviderSettings,
    state: str,
    nonce: str,
) -> str:
    """Build the exact Apple Web authorization request for DANTE Auth."""
    apple = settings.apple
    if not apple.enabled or apple.client_id is None or apple.redirect_uri is None:
        raise AppleProviderUnavailableError("Apple authentication is not enabled")
    if not _canonical_secret(state, maximum=512) or not _canonical_secret(nonce, maximum=512):
        raise AppleProofError("Apple transaction capability is malformed")
    query = urlencode(
        {
            "client_id": apple.client_id,
            "redirect_uri": apple.redirect_uri,
            "response_type": "code id_token",
            "response_mode": "form_post",
            "scope": "name email",
            "state": state,
            "nonce": nonce,
        }
    )
    return f"{apple.authorize_url}?{query}"


def parse_apple_authorization_profile(raw_user: str | None) -> AppleAuthorizationProfile | None:
    """Sanitize Apple's first-authorization user JSON without treating it as signed evidence."""
    if raw_user is None:
        return None
    try:
        encoded = raw_user.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise AppleProofError("Apple user profile is invalid") from exc
    if not encoded or len(encoded) > _MAX_PROFILE_JSON_BYTES:
        raise AppleProofError("Apple user profile is empty or oversized")
    try:
        payload = json.loads(raw_user)
    except json.JSONDecodeError as exc:
        raise AppleProofError("Apple user profile is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise AppleProofError("Apple user profile must be a JSON object")
    unknown = set(payload) - {"name", "email"}
    if unknown:
        raise AppleProofError("Apple user profile contains unexpected members")

    name = payload.get("name")
    given_name: str | None = None
    family_name: str | None = None
    if name is not None:
        if not isinstance(name, dict) or set(name) - {"firstName", "lastName"}:
            raise AppleProofError("Apple user name is malformed")
        given_name = _profile_part(name.get("firstName"))
        family_name = _profile_part(name.get("lastName"))

    email = _validated_email(payload.get("email"))
    return AppleAuthorizationProfile(given_name=given_name, family_name=family_name, email=email)


def reconcile_apple_profile_email(
    *,
    evidence: AppleIdentityEvidence,
    profile: AppleAuthorizationProfile | None,
) -> None:
    """Reject contradictory one-shot profile email when signed email evidence is present."""
    if profile is None or profile.email is None or evidence.email is None:
        return
    if profile.email.comparison_key != evidence.email.comparison_key:
        raise AppleProofError("Apple one-shot email contradicts the signed ID-token email")


def apple_code_hash(code: str) -> str:
    """Return OIDC c_hash for an RS256-signed Apple ID token."""
    if not _canonical_secret(code, maximum=_MAX_CODE_BYTES):
        raise AppleProofError("Apple authorization code is malformed")
    digest = sha256(code.encode("ascii")).digest()[:16]
    return urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def is_apple_private_email(email: NormalizedEmail) -> bool:
    """Recognize both current and legacy Sign in with Apple relay domains."""
    return email.comparison_key.rsplit("@", 1)[1] in _PRIVATE_EMAIL_DOMAINS


def _notification_event_object(value: object) -> dict[str, object]:
    if isinstance(value, str):
        if not value or len(value.encode("utf-8")) > _MAX_NOTIFICATION_EVENTS_BYTES:
            raise AppleProofError("Apple notification events claim is invalid")
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise AppleProofError("Apple notification events claim is invalid") from exc
    if isinstance(value, list):
        if len(value) != 1:
            raise AppleProofError("Apple notification must contain exactly one event")
        value = value[0]
    if not isinstance(value, dict):
        raise AppleProofError("Apple notification events claim must contain one object")
    return {str(key): item for key, item in value.items()}


def _required_claim_string(claims: dict[str, object], name: str, *, maximum: int) -> str:
    value = claims.get(name)
    if not isinstance(value, str) or not _canonical_text(value, maximum=maximum):
        raise AppleProofError(f"Apple {name} claim is invalid")
    return value


def _required_object_string(value: dict[str, object], name: str, *, maximum: int) -> str:
    candidate = value.get(name)
    if not isinstance(candidate, str) or not _canonical_text(candidate, maximum=maximum):
        raise AppleProofError(f"Apple event {name} is invalid")
    return candidate


def _canonical_text(value: object, *, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and value.strip() == value
        and len(value) <= maximum
        and not any(char in value for char in "\r\n\x00")
    )


def _canonical_secret(value: str, *, maximum: int) -> bool:
    if not _canonical_text(value, maximum=maximum):
        return False
    try:
        value.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def _numeric_date(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise AppleProofError(f"Apple {name} claim is invalid")
    converted = float(value)
    if not math.isfinite(converted) or converted < 0:
        raise AppleProofError(f"Apple {name} claim is invalid")
    return converted


def _optional_apple_bool(value: object, *, name: str) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value in {"true", "false"}:
        return value == "true"
    raise AppleProofError(f"Apple {name} claim is invalid")


def _validated_email(value: object) -> NormalizedEmail | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise AppleProofError("Apple email is invalid")
    try:
        return normalize_email(value)
    except EmailNormalizationError as exc:
        raise AppleProofError("Apple email is invalid") from exc


def _profile_part(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise AppleProofError("Apple profile name is invalid")
    candidate = " ".join(value.split())
    if not candidate:
        return None
    if len(candidate) > _MAX_PROFILE_PART_LENGTH or any(char in candidate for char in "\r\n\x00"):
        raise AppleProofError("Apple profile name is invalid")
    return candidate


def _required_response_string(body: dict[str, object], name: str, *, maximum: int) -> str:
    value = body.get(name)
    if not isinstance(value, str) or not _canonical_text(value, maximum=maximum):
        raise AppleProviderUnavailableError(f"Apple token response omitted valid {name}")
    return value


def _protocol_error_code(body: dict[str, object]) -> str:
    value = body.get("error")
    if not isinstance(value, str) or not _canonical_text(value, maximum=128):
        return "provider_error"
    return value
