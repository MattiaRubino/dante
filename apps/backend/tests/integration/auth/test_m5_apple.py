"""Real PostgreSQL proof for M5-D Apple Account/grant/session/challenge invariants."""

from __future__ import annotations

import asyncio
import json
from base64 import urlsafe_b64encode
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from urllib.parse import parse_qs, urlsplit
from uuid import UUID, uuid7

import pytest
from pydantic import SecretStr
from sqlalchemy import func, select

from dante.auth.apple import (
    AppleIdentityEvidence,
    AppleNotificationEvent,
    AppleNotificationVerifier,
    AppleProtocolClient,
    AppleProviderUnavailableError,
    AppleTokenResponse,
    AppleTokenVerifier,
)
from dante.auth.apple_crypto import AppleGrantCipher
from dante.auth.apple_flow import AppleFlowService
from dante.auth.contracts import (
    AdmittedSession,
    Principal,
    ProviderAuthenticated,
    ProviderAuthenticationResult,
    ProviderEnrollmentRequired,
    ProviderLinkRequired,
    ProviderPurpose,
    ProviderReconciliationPendingError,
    ProviderReturnTarget,
    ProviderTransactionInvalidOrExpiredError,
)
from dante.auth.email import normalize_email
from dante.auth.email_delivery import (
    EmailCommand,
    EmailDeliveryPort,
    ProviderEnrollmentVerificationEmail,
)
from dante.auth.lifecycle import KeyedRateLimiter
from dante.auth.proofs import FlowProofPurpose, ProviderEnrollmentOtpCodec, flow_proof_verifier
from dante.auth.provider_flow import ProviderFlowLimiters
from dante.auth.sessions import generate_session_secret, session_secret_verifier
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.auth_provider import APPLE_ISSUER, AppleProviderSettings, AuthProviderSettings
from dante.platform.database.mappings.auth import (
    AccountProfileBootstrapRow,
    AccountRow,
    AppleAuthGrantRow,
    AuthSessionRow,
    EmailIdentityRow,
    ExternalAuthTransactionRow,
    ExternalIdentityRow,
    ExternalLinkChallengeRow,
    ExternalSignupChallengeRow,
)
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime

pytestmark = pytest.mark.postgres

_CLIENT_ID = "com.dante.test.web"
_KEY_ID = "test-key-v1"
_GRANT_KEY_ID = "apple-grant-v1"


def _encoded(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _settings() -> AuthSettings:
    return AuthSettings(
        canonical_web_origin="https://dante.test",
        password_current_pepper_key_id=_KEY_ID,
        password_peppers={_KEY_ID: SecretStr(_encoded(b"p" * 32))},
        csrf_key=SecretStr(_encoded(b"c" * 32)),
        signup_otp_current_key_id=_KEY_ID,
        signup_otp_keys={_KEY_ID: SecretStr(_encoded(b"o" * 32))},
        provider=AuthProviderSettings(
            apple=AppleProviderSettings(
                enabled=True,
                client_id=_CLIENT_ID,
                team_id="ABCDE12345",
                key_id="APPLEKEY01",
                client_private_key_pem=SecretStr("test-p8-material"),
                redirect_uri="https://auth.dante.test/api/v1/auth/apple/callback",
                grant_encryption_current_key_id=_GRANT_KEY_ID,
                grant_encryption_keys={
                    _GRANT_KEY_ID: SecretStr(_encoded(b"g" * 32)),
                },
            )
        ),
        smtp_host="127.0.0.1",
        smtp_port=9,
        smtp_security=SmtpSecurity.PLAIN,
        smtp_from_address="no-reply@dante.test",
        kdf_max_concurrency=1,
        signin_rate_capacity=100,
        signin_rate_window_seconds=60,
        provider_begin_rate_capacity=100,
        provider_complete_rate_capacity=100,
        provider_enrollment_rate_capacity=100,
    )


class _MemoryEmailDelivery:
    def __init__(self) -> None:
        self.commands: list[EmailCommand] = []

    async def enqueue(self, command: EmailCommand) -> None:
        self.commands.append(command)

    def latest_provider_otp(self) -> ProviderEnrollmentVerificationEmail:
        for command in reversed(self.commands):
            if isinstance(command, ProviderEnrollmentVerificationEmail):
                return command
        raise AssertionError("provider enrollment OTP was not queued")


class _FakeAppleVerifier:
    def __init__(self, evidence: AppleIdentityEvidence) -> None:
        self.evidence = evidence
        self.calls: list[tuple[str, bytes, str | None]] = []

    async def verify(
        self,
        token: str,
        *,
        expected_nonce_verifier: bytes,
        expected_code: str | None = None,
    ) -> AppleIdentityEvidence:
        self.calls.append((token, expected_nonce_verifier, expected_code))
        return self.evidence


class _FakeAppleProtocolClient:
    def __init__(self) -> None:
        self.exchange_codes: list[str] = []
        self.revoke_attempts: list[str] = []
        self.revoked_tokens: list[str] = []
        self.revoke_failures_remaining = 0

    async def exchange_code(self, code: str) -> AppleTokenResponse:
        self.exchange_codes.append(code)
        return AppleTokenResponse(
            id_token=f"exchanged-id-token:{code}",
            refresh_token=SecretStr(f"refresh-token:{code}"),
        )

    async def revoke_refresh_token(self, refresh_token: SecretStr) -> None:
        token = refresh_token.get_secret_value()
        self.revoke_attempts.append(token)
        if self.revoke_failures_remaining > 0:
            self.revoke_failures_remaining -= 1
            raise AppleProviderUnavailableError("simulated Apple revoke outage")
        self.revoked_tokens.append(token)


class _FakeNotificationVerifier:
    def __init__(self) -> None:
        self.events: dict[str, AppleNotificationEvent] = {}

    async def verify_notification(self, token: str) -> AppleNotificationEvent:
        return self.events[token]


def _evidence(
    *,
    subject: str,
    email: str | None,
    authoritative: bool,
    private: bool | None = None,
) -> AppleIdentityEvidence:
    normalized = normalize_email(email) if email is not None else None
    return AppleIdentityEvidence(
        issuer=APPLE_ISSUER,
        subject=subject,
        email=normalized,
        email_verified=authoritative and normalized is not None,
        email_private=(private if normalized is not None else None),
        mailbox_authoritative=authoritative and normalized is not None,
    )


def _limiters(settings: AuthSettings) -> ProviderFlowLimiters:
    return ProviderFlowLimiters(
        begin=KeyedRateLimiter(
            capacity=settings.provider_begin_rate_capacity,
            window_seconds=settings.provider_begin_rate_window_seconds,
            max_keys=128,
        ),
        complete=KeyedRateLimiter(
            capacity=settings.provider_complete_rate_capacity,
            window_seconds=settings.provider_complete_rate_window_seconds,
            max_keys=128,
        ),
        enrollment=KeyedRateLimiter(
            capacity=settings.provider_enrollment_rate_capacity,
            window_seconds=settings.provider_enrollment_rate_window_seconds,
            max_keys=128,
        ),
    )


@asynccontextmanager
async def _apple_service(
    database: Any,
    *,
    evidence: AppleIdentityEvidence,
) -> AsyncIterator[
    tuple[
        AppleFlowService,
        _FakeAppleVerifier,
        _FakeAppleProtocolClient,
        _FakeNotificationVerifier,
        _MemoryEmailDelivery,
        DatabaseRuntime,
    ]
]:
    settings = _settings()
    runtime = create_database_runtime(database.runtime_settings())
    verifier = _FakeAppleVerifier(evidence)
    protocol = _FakeAppleProtocolClient()
    notifications = _FakeNotificationVerifier()
    delivery = _MemoryEmailDelivery()
    service = AppleFlowService(
        session_factory=runtime.session_factory,
        settings=settings,
        token_verifier=cast(AppleTokenVerifier, verifier),
        notification_verifier=cast(AppleNotificationVerifier, notifications),
        protocol_client=cast(AppleProtocolClient, protocol),
        grant_cipher=AppleGrantCipher(
            key_ring=settings.provider.apple.grant_encryption_key_bytes,
            current_key_id=_GRANT_KEY_ID,
        ),
        otp_codec=ProviderEnrollmentOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=cast(EmailDeliveryPort, delivery),
        limiters=_limiters(settings),
    )
    try:
        yield service, verifier, protocol, notifications, delivery, runtime
    finally:
        await runtime.dispose()


def _state_from_url(url: str) -> str:
    values = parse_qs(urlsplit(url).query, strict_parsing=True)
    return values["state"][0]


def _nonce_from_url(url: str) -> str:
    values = parse_qs(urlsplit(url).query, strict_parsing=True)
    return values["nonce"][0]


async def _begin_and_complete(
    service: AppleFlowService,
    *,
    source: str,
    user: str | None = None,
) -> ProviderAuthenticationResult:
    begun = await service.begin_apple(
        purpose=ProviderPurpose.SIGN_IN,
        return_target=ProviderReturnTarget.ACCESS,
        source_context=f"{source}-begin",
    )
    return await service.complete_apple(
        state=_state_from_url(begun.authorization_url),
        code=f"code-{source}",
        id_token=f"front-id-token-{source}",
        user=user,
        error=None,
        source_context=f"{source}-complete",
    )


async def _count(runtime: DatabaseRuntime, model: type[Any]) -> int:
    async with runtime.session_factory() as session, session.begin():
        value = await session.scalar(select(func.count()).select_from(model))
    assert value is not None
    return int(value)


async def _seed_account_email(
    runtime: DatabaseRuntime,
    *,
    email: str,
) -> tuple[UUID, UUID]:
    account_ref = uuid7()
    email_ref = uuid7()
    normalized = normalize_email(email)
    now = datetime.now(UTC)
    async with runtime.session_factory() as session, session.begin():
        session.add_all(
            [
                AccountRow(
                    account_ref=account_ref,
                    status_code="active",
                    created_at=now,
                    disabled_at=None,
                ),
                EmailIdentityRow(
                    email_identity_ref=email_ref,
                    account_ref=account_ref,
                    address=normalized.address,
                    comparison_key=normalized.comparison_key,
                    created_at=now,
                    verified_at=now,
                    recovery_restriction_code=None,
                    recovery_restriction_observed_at=None,
                ),
            ]
        )
    return account_ref, email_ref


async def _seed_session(
    runtime: DatabaseRuntime,
    *,
    account_ref: UUID,
) -> tuple[AdmittedSession, SecretStr]:
    secret = generate_session_secret()
    verifier = session_secret_verifier(secret)
    session_ref = uuid7()
    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=1)
    async with runtime.session_factory() as session, session.begin():
        session.add(
            AuthSessionRow(
                auth_session_ref=session_ref,
                account_ref=account_ref,
                secret_verifier=verifier,
                created_at=now,
                authenticated_at=now,
                recent_auth_at=now,
                last_user_activity_at=now,
                expires_at=expires_at,
                revoked_at=None,
                revocation_reason_code=None,
            )
        )
    return (
        AdmittedSession(
            principal=Principal(
                account_ref=account_ref,
                auth_session_ref=session_ref,
                authenticated_at=now,
                recent_auth_at=now,
            ),
            expires_at=expires_at,
            csrf_token=SecretStr("not-used-here"),
        ),
        secret,
    )


@pytest.mark.asyncio
async def test_apple_transaction_persists_only_verifiers_and_claims_before_single_exchange(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="apple-claim-once",
        email="claim-once@example.com",
        authoritative=True,
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        verifier,
        protocol,
        _notifications,
        _delivery,
        runtime,
    ):
        begun = await service.begin_apple(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="claim-once-begin",
        )
        state = _state_from_url(begun.authorization_url)
        nonce = _nonce_from_url(begun.authorization_url)
        state_verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.PROVIDER_STATE,
            encoded_secret=state,
        )
        nonce_verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.OIDC_NONCE,
            encoded_secret=nonce,
        )
        assert state_verifier is not None
        assert nonce_verifier is not None

        async with runtime.session_factory() as session, session.begin():
            row = await session.scalar(
                select(ExternalAuthTransactionRow).where(
                    ExternalAuthTransactionRow.provider_code == "apple",
                    ExternalAuthTransactionRow.state_verifier == state_verifier,
                )
            )
        assert row is not None
        assert row.nonce_verifier == nonce_verifier
        assert row.claimed_at is None

        result = await service.complete_apple(
            state=state,
            code="single-use-code",
            id_token="front-id-token",
            user=None,
            error=None,
            source_context="claim-once-complete",
        )
        assert isinstance(result, ProviderAuthenticated)
        assert protocol.exchange_codes == ["single-use-code"]
        assert len(verifier.calls) == 2

        with pytest.raises(ProviderTransactionInvalidOrExpiredError):
            await service.complete_apple(
                state=state,
                code="single-use-code",
                id_token="front-id-token",
                user=None,
                error=None,
                source_context="claim-once-replay",
            )
        assert protocol.exchange_codes == ["single-use-code"]
        assert len(verifier.calls) == 2


@pytest.mark.asyncio
async def test_authoritative_private_relay_creates_passwordless_account_active_grant_and_bootstrap(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="apple-new-account",
        email="opaque@private.icloud.com",
        authoritative=True,
        private=True,
    )
    user = json.dumps(
        {
            "name": {"firstName": "Ada", "lastName": "Lovelace"},
            "email": "opaque@private.icloud.com",
        }
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        _notifications,
        _delivery,
        runtime,
    ):
        first = await _begin_and_complete(service, source="new-account-first", user=user)
        assert isinstance(first, ProviderAuthenticated)
        account_ref = first.session.principal.account_ref

        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, EmailIdentityRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AppleAuthGrantRow) == 1
        assert await _count(runtime, AuthSessionRow) == 1
        assert await _count(runtime, AccountProfileBootstrapRow) == 1

        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(select(ExternalIdentityRow))
            grant = await session.scalar(select(AppleAuthGrantRow))
        assert identity is not None
        assert identity.account_ref == account_ref
        assert identity.provider_email_private is True
        assert grant is not None
        assert grant.status_code == "active"
        assert grant.external_identity_ref == identity.external_identity_ref
        assert grant.refresh_token_ciphertext is not None
        assert b"refresh-token" not in grant.refresh_token_ciphertext

        second = await _begin_and_complete(service, source="new-account-second")
        assert isinstance(second, ProviderAuthenticated)
        assert second.session.principal.account_ref == account_ref
        assert second.session.principal.auth_session_ref != first.session.principal.auth_session_ref
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AppleAuthGrantRow) == 1
        assert await _count(runtime, AuthSessionRow) == 2


@pytest.mark.asyncio
async def test_apple_email_collision_returns_link_required_with_pending_revocable_grant(
    migrated_database: Any,
) -> None:
    email = "existing@example.com"
    evidence = _evidence(subject="apple-collision", email=email, authoritative=True)
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        _notifications,
        _delivery,
        runtime,
    ):
        account_ref, email_ref = await _seed_account_email(runtime, email=email)
        result = await _begin_and_complete(service, source="collision")

        assert isinstance(result, ProviderLinkRequired)
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 0
        assert await _count(runtime, AuthSessionRow) == 0
        assert await _count(runtime, AppleAuthGrantRow) == 1
        assert await _count(runtime, ExternalLinkChallengeRow) == 1
        async with runtime.session_factory() as session, session.begin():
            challenge = await session.scalar(select(ExternalLinkChallengeRow))
            grant = await session.scalar(select(AppleAuthGrantRow))
        assert challenge is not None
        assert grant is not None
        assert challenge.target_account_ref == account_ref
        assert challenge.target_email_identity_ref == email_ref
        assert challenge.apple_auth_grant_ref == grant.apple_auth_grant_ref
        assert grant.status_code == "pending"
        assert grant.external_identity_ref is None


@pytest.mark.asyncio
async def test_one_shot_email_without_signed_mailbox_authority_requires_dante_otp(
    migrated_database: Any,
) -> None:
    evidence = _evidence(subject="apple-enrollment", email=None, authoritative=False)
    user = json.dumps(
        {
            "name": {"firstName": "Grace", "lastName": "Hopper"},
            "email": "grace@example.com",
        }
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        _notifications,
        delivery,
        runtime,
    ):
        result = await _begin_and_complete(service, source="enrollment", user=user)
        assert isinstance(result, ProviderEnrollmentRequired)
        assert await _count(runtime, AccountRow) == 0
        assert await _count(runtime, AppleAuthGrantRow) == 1
        assert await _count(runtime, ExternalSignupChallengeRow) == 1

        otp = delivery.latest_provider_otp()
        completed = await service.verify_provider_enrollment(
            external_signup_ref=result.external_signup_ref,
            continuation_secret=result.continuation_secret.get_secret_value(),
            code=otp.code.get_secret_value(),
            source_context="enrollment-verify",
        )
        assert isinstance(completed, ProviderAuthenticated)
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, EmailIdentityRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AuthSessionRow) == 1
        assert await _count(runtime, ExternalSignupChallengeRow) == 0
        assert await _count(runtime, AccountProfileBootstrapRow) == 1
        async with runtime.session_factory() as session, session.begin():
            grant = await session.scalar(select(AppleAuthGrantRow))
        assert grant is not None
        assert grant.status_code == "active"
        assert grant.external_identity_ref is not None


@pytest.mark.asyncio
async def test_enrollment_race_to_existing_email_preserves_same_pending_grant_for_link(
    migrated_database: Any,
) -> None:
    evidence = _evidence(subject="apple-enrollment-collision", email=None, authoritative=False)
    user = json.dumps({"email": "race@example.com"})
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        _notifications,
        delivery,
        runtime,
    ):
        result = await _begin_and_complete(service, source="enrollment-collision", user=user)
        assert isinstance(result, ProviderEnrollmentRequired)
        await _seed_account_email(runtime, email="race@example.com")
        otp = delivery.latest_provider_otp()

        completed = await service.verify_provider_enrollment(
            external_signup_ref=result.external_signup_ref,
            continuation_secret=result.continuation_secret.get_secret_value(),
            code=otp.code.get_secret_value(),
            source_context="enrollment-collision-verify",
        )
        assert isinstance(completed, ProviderLinkRequired)
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 0
        assert await _count(runtime, ExternalSignupChallengeRow) == 0
        assert await _count(runtime, ExternalLinkChallengeRow) == 1
        async with runtime.session_factory() as session, session.begin():
            grant = await session.scalar(select(AppleAuthGrantRow))
            challenge = await session.scalar(select(ExternalLinkChallengeRow))
        assert grant is not None
        assert challenge is not None
        assert grant.status_code == "pending"
        assert challenge.apple_auth_grant_ref == grant.apple_auth_grant_ref


@pytest.mark.asyncio
async def test_authenticated_link_then_apple_reauthentication_rotate_exact_same_session(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="apple-settings-link",
        email="settings-link@example.com",
        authoritative=True,
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        _notifications,
        _delivery,
        runtime,
    ):
        account_ref, _email_ref = await _seed_account_email(runtime, email="owner@example.com")
        admitted, original_secret = await _seed_session(runtime, account_ref=account_ref)
        begun = await service.begin_apple(
            purpose=ProviderPurpose.LINK,
            return_target=ProviderReturnTarget.SECURITY,
            source_context="settings-link-begin",
            admitted=admitted,
            presented_session_secret=original_secret.get_secret_value(),
        )
        linked = await service.complete_apple(
            state=_state_from_url(begun.authorization_url),
            code="settings-link-code",
            id_token="front-link-token",
            user=None,
            error=None,
            source_context="settings-link-complete",
        )
        assert isinstance(linked, ProviderAuthenticated)
        assert linked.session.principal.account_ref == account_ref
        assert linked.session.principal.auth_session_ref == admitted.principal.auth_session_ref
        assert linked.session.session_secret.get_secret_value() != original_secret.get_secret_value()
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AppleAuthGrantRow) == 1

        reauth_admitted = AdmittedSession(
            principal=linked.session.principal,
            expires_at=linked.session.expires_at,
            csrf_token=linked.session.csrf_token,
        )
        reauth_begin = await service.begin_apple(
            purpose=ProviderPurpose.REAUTHENTICATE,
            return_target=ProviderReturnTarget.SECURITY,
            source_context="apple-reauth-begin",
            admitted=reauth_admitted,
            presented_session_secret=linked.session.session_secret.get_secret_value(),
        )
        reauthenticated = await service.complete_apple(
            state=_state_from_url(reauth_begin.authorization_url),
            code="reauth-code",
            id_token="front-reauth-token",
            user=None,
            error=None,
            source_context="apple-reauth-complete",
        )
        assert isinstance(reauthenticated, ProviderAuthenticated)
        assert reauthenticated.session.principal.auth_session_ref == admitted.principal.auth_session_ref
        assert (
            reauthenticated.session.session_secret.get_secret_value()
            != linked.session.session_secret.get_secret_value()
        )


@pytest.mark.asyncio
async def test_signed_email_events_are_monotonic_and_revocation_clears_grant_secret(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="apple-notifications",
        email="relay@privaterelay.appleid.com",
        authoritative=True,
        private=True,
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        notifications,
        _delivery,
        runtime,
    ):
        result = await _begin_and_complete(service, source="notifications")
        assert isinstance(result, ProviderAuthenticated)
        base = datetime.now(UTC)
        normalized = normalize_email("relay@privaterelay.appleid.com")
        notifications.events["disabled"] = AppleNotificationEvent(
            event_type="email-disabled",
            subject=evidence.subject,
            event_time=base,
            email=normalized,
            email_private=True,
            jti="disabled-1",
        )
        notifications.events["enabled"] = AppleNotificationEvent(
            event_type="email-enabled",
            subject=evidence.subject,
            event_time=base + timedelta(seconds=2),
            email=normalized,
            email_private=True,
            jti="enabled-1",
        )
        notifications.events["old-disabled"] = AppleNotificationEvent(
            event_type="email-disabled",
            subject=evidence.subject,
            event_time=base + timedelta(seconds=1),
            email=normalized,
            email_private=True,
            jti="disabled-old",
        )
        notifications.events["revoked"] = AppleNotificationEvent(
            event_type="consent-revoked",
            subject=evidence.subject,
            event_time=base + timedelta(seconds=3),
            email=None,
            email_private=None,
            jti="revoked-1",
        )

        assert await service.process_notification("disabled") is True
        assert await service.process_notification("enabled") is True
        assert await service.process_notification("old-disabled") is True
        async with runtime.session_factory() as session, session.begin():
            email = await session.scalar(select(EmailIdentityRow))
        assert email is not None
        assert email.recovery_restriction_code is None
        assert email.recovery_restriction_observed_at == base + timedelta(seconds=2)

        assert await service.process_notification("revoked") is True
        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(select(ExternalIdentityRow))
            grant = await session.scalar(select(AppleAuthGrantRow))
        assert identity is not None
        assert identity.status_code == "revoked"
        assert identity.revocation_reason_code == "provider_revoked"
        assert grant is not None
        assert grant.status_code == "revoked"
        assert grant.refresh_token_ciphertext is None
        assert grant.refresh_token_nonce is None
        assert grant.encryption_key_id is None


@pytest.mark.asyncio
async def test_concurrent_first_apple_callbacks_converge_on_one_account_identity_and_active_grant(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="apple-concurrent-subject",
        email="concurrent@example.com",
        authoritative=True,
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _protocol,
        _notifications,
        _delivery,
        runtime,
    ):
        first_begin = await service.begin_apple(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="concurrent-begin-1",
        )
        second_begin = await service.begin_apple(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="concurrent-begin-2",
        )

        first, second = await asyncio.gather(
            service.complete_apple(
                state=_state_from_url(first_begin.authorization_url),
                code="concurrent-code-1",
                id_token="front-concurrent-1",
                user=None,
                error=None,
                source_context="concurrent-complete-1",
            ),
            service.complete_apple(
                state=_state_from_url(second_begin.authorization_url),
                code="concurrent-code-2",
                id_token="front-concurrent-2",
                user=None,
                error=None,
                source_context="concurrent-complete-2",
            ),
        )
        assert isinstance(first, ProviderAuthenticated)
        assert isinstance(second, ProviderAuthenticated)
        assert first.session.principal.account_ref == second.session.principal.account_ref
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AppleAuthGrantRow) == 1
        assert await _count(runtime, AuthSessionRow) == 2

        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(select(ExternalIdentityRow))
            grant = await session.scalar(select(AppleAuthGrantRow))
        assert identity is not None
        assert grant is not None
        assert grant.status_code == "active"
        assert grant.external_identity_ref == identity.external_identity_ref
        assert grant.pending_expires_at is None
        assert grant.revocation_requested_at is None


@pytest.mark.asyncio
async def test_local_revoke_survives_provider_outage_and_reconciles_pending_grant(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="apple-revoke-reconcile",
        email="revoke@example.com",
        authoritative=True,
    )
    async with _apple_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        protocol,
        _notifications,
        _delivery,
        runtime,
    ):
        result = await _begin_and_complete(service, source="revoke-reconcile")
        assert isinstance(result, ProviderAuthenticated)
        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(select(ExternalIdentityRow))
            grant = await session.scalar(select(AppleAuthGrantRow))
        assert identity is not None
        assert grant is not None
        assert grant.status_code == "active"
        original_ciphertext = grant.refresh_token_ciphertext
        assert original_ciphertext is not None

        protocol.revoke_failures_remaining = 1
        with pytest.raises(ProviderReconciliationPendingError):
            await service.revoke_identity_and_grant(
                external_identity_ref=identity.external_identity_ref,
            )

        async with runtime.session_factory() as session, session.begin():
            revoked_identity = await session.scalar(select(ExternalIdentityRow))
            pending_grant = await session.scalar(select(AppleAuthGrantRow))
        assert revoked_identity is not None
        assert revoked_identity.status_code == "revoked"
        assert revoked_identity.revocation_reason_code == "user_unlinked"
        assert pending_grant is not None
        assert pending_grant.status_code == "revocation_pending"
        assert pending_grant.refresh_token_ciphertext == original_ciphertext
        assert pending_grant.refresh_token_nonce is not None
        assert pending_grant.encryption_key_id is not None
        assert pending_grant.revocation_requested_at is not None
        assert protocol.revoked_tokens == []
        assert len(protocol.revoke_attempts) == 1

        assert await service.reconcile_expired_pending_grants() == 1

        async with runtime.session_factory() as session, session.begin():
            final_grant = await session.scalar(select(AppleAuthGrantRow))
        assert final_grant is not None
        assert final_grant.status_code == "revoked"
        assert final_grant.refresh_token_ciphertext is None
        assert final_grant.refresh_token_nonce is None
        assert final_grant.encryption_key_id is None
        assert final_grant.revoked_at is not None
        assert len(protocol.revoke_attempts) == 2
        assert len(protocol.revoked_tokens) == 1
