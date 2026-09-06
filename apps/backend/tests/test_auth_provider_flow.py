"""Fast M5-C provider-flow ingress and policy tests."""

from __future__ import annotations

from base64 import urlsafe_b64encode
from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import uuid7

import pytest
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.contracts import (
    AdmittedSession,
    AuthInputError,
    Principal,
    ProviderPurpose,
    ProviderReturnTarget,
    ProviderTransactionInvalidOrExpiredError,
    ProviderUnavailableError,
    ReauthenticationRequiredError,
)
from dante.auth.email_delivery import EmailCommand, EmailDeliveryPort
from dante.auth.google import GoogleTokenVerifier
from dante.auth.lifecycle import KeyedRateLimiter
from dante.auth.proofs import ProviderEnrollmentOtpCodec
from dante.auth.provider_flow import ProviderFlowLimiters, ProviderFlowService
from dante.platform.config.auth import AuthSettings
from dante.platform.config.auth_provider import AuthProviderSettings, GoogleProviderSettings

_KEY_ID = "test-key"


def _encoded(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _malformed_session_bearer() -> str:
    return "not-a-session-secret"


class _NoDatabase:
    def __call__(self) -> AsyncSession:
        raise AssertionError("database must not be touched by this preflight failure")


class _NoopDelivery:
    async def enqueue(self, _command: EmailCommand) -> None:
        return None


def _settings(*, google_enabled: bool) -> AuthSettings:
    return AuthSettings(
        canonical_web_origin="https://dante.test",
        password_current_pepper_key_id=_KEY_ID,
        password_peppers={_KEY_ID: SecretStr(_encoded(b"p" * 32))},
        csrf_key=SecretStr(_encoded(b"c" * 32)),
        signup_otp_current_key_id=_KEY_ID,
        signup_otp_keys={_KEY_ID: SecretStr(_encoded(b"o" * 32))},
        provider=AuthProviderSettings(
            google=GoogleProviderSettings(
                enabled=google_enabled,
                client_id="dante-client.apps.googleusercontent.com" if google_enabled else None,
            )
        ),
        smtp_host="smtp.dante.test",
        smtp_from_address="no-reply@dante.test",
        kdf_max_concurrency=1,
        signin_rate_capacity=10,
        signin_rate_window_seconds=60,
    )


def _limiter() -> KeyedRateLimiter:
    return KeyedRateLimiter(capacity=20, window_seconds=60, max_keys=16)


def _service(*, google_enabled: bool = True) -> ProviderFlowService:
    settings = _settings(google_enabled=google_enabled)
    return ProviderFlowService(
        session_factory=cast(async_sessionmaker[AsyncSession], _NoDatabase()),
        settings=settings,
        google_verifier=cast(GoogleTokenVerifier, object()),
        otp_codec=ProviderEnrollmentOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=cast(EmailDeliveryPort, _NoopDelivery()),
        limiters=ProviderFlowLimiters(
            begin=_limiter(),
            complete=_limiter(),
            enrollment=_limiter(),
        ),
    )


def _admitted(*, recent_auth_at: datetime) -> AdmittedSession:
    now = datetime.now(UTC)
    return AdmittedSession(
        principal=Principal(
            account_ref=uuid7(),
            auth_session_ref=uuid7(),
            authenticated_at=now - timedelta(minutes=30),
            recent_auth_at=recent_auth_at,
        ),
        expires_at=now + timedelta(hours=1),
        csrf_token=SecretStr("not-used-at-application-layer"),
    )


@pytest.mark.asyncio
async def test_disabled_google_fails_before_database_or_network() -> None:
    service = _service(google_enabled=False)

    with pytest.raises(ProviderUnavailableError) as raised:
        await service.begin_google(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="test-source",
        )

    assert raised.value.retryable is False


@pytest.mark.asyncio
async def test_sign_in_begin_rejects_authenticated_session_binding() -> None:
    service = _service()

    with pytest.raises(ProviderTransactionInvalidOrExpiredError):
        await service.begin_google(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="test-source",
            admitted=_admitted(recent_auth_at=datetime.now(UTC)),
            presented_session_secret=_malformed_session_bearer(),
        )


@pytest.mark.asyncio
async def test_link_begin_requires_recent_auth_before_database_access() -> None:
    service = _service()
    stale = datetime.now(UTC) - timedelta(hours=1)

    with pytest.raises(ReauthenticationRequiredError):
        await service.begin_google(
            purpose=ProviderPurpose.LINK,
            return_target=ProviderReturnTarget.SECURITY,
            source_context="test-source",
            admitted=_admitted(recent_auth_at=stale),
            presented_session_secret=_encoded(b"s" * 32),
        )


@pytest.mark.asyncio
async def test_link_and_reauth_require_exact_session_bearer_shape() -> None:
    service = _service()
    admitted = _admitted(recent_auth_at=datetime.now(UTC))

    for purpose in (ProviderPurpose.LINK, ProviderPurpose.REAUTHENTICATE):
        with pytest.raises(ProviderTransactionInvalidOrExpiredError):
            await service.begin_google(
                purpose=purpose,
                return_target=ProviderReturnTarget.SECURITY,
                source_context=f"test-source-{purpose.value}",
                admitted=admitted,
                presented_session_secret=_malformed_session_bearer(),
            )


@pytest.mark.asyncio
async def test_provider_enrollment_email_uses_canonical_dante_validation_before_database() -> None:
    service = _service()

    with pytest.raises(AuthInputError) as raised:
        await service.set_provider_enrollment_email(
            external_signup_ref=uuid7(),
            continuation_secret=_encoded(b"e" * 32),
            email="not an email",
            source_context="test-source",
        )

    assert raised.value.pointer == "/email"
    assert raised.value.code == "invalid_format"
