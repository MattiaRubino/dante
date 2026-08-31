"""Real PostgreSQL proof for M5-E/G authenticator lifecycle and passwordless recovery."""

from __future__ import annotations

import asyncio
from base64 import urlsafe_b64encode
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID, uuid7

import pytest
from pydantic import SecretStr
from sqlalchemy import func, select

from dante.auth.authenticator_lifecycle import (
    AuthenticatorLifecycleService,
    MultiAuthenticatorLifecycleService,
)
from dante.auth.contracts import (
    AdmittedSession,
    AuthenticatorRemovalBlockedError,
    IssuedSession,
    Principal,
    ProviderLinkAccountMismatchError,
    ProviderReconciliationPendingError,
)
from dante.auth.email import normalize_email
from dante.auth.email_delivery import (
    EmailCommand,
    EmailDeliveryPort,
    PasswordRecoveryEmail,
    PasswordResetNotificationEmail,
)
from dante.auth.lifecycle import KeyedRateLimiter, LifecycleLimiters
from dante.auth.passwords import PasswordKdf, normalize_password_for_authentication
from dante.auth.proofs import FlowProofPurpose, SignupOtpCodec, issue_flow_proof
from dante.auth.sessions import generate_session_secret, session_secret_verifier
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.auth_provider import APPLE_ISSUER, GOOGLE_ISSUER
from dante.platform.database.mappings.auth import (
    AccountRow,
    AppleAuthGrantRow,
    AuthSessionRow,
    EmailIdentityRow,
    ExternalIdentityRow,
    ExternalLinkChallengeRow,
    PasswordCredentialRow,
    PasswordRecoveryChallengeRow,
)
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime

pytestmark = pytest.mark.postgres

_KEY_ID = "test-authenticator-v1"
_VALID_SECRET_PHRASE = "correct horse battery staple"
_REPLACEMENT_SECRET_PHRASE = "replacement horse battery staple"


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
        smtp_host="127.0.0.1",
        smtp_port=9,
        smtp_security=SmtpSecurity.PLAIN,
        smtp_from_address="no-reply@dante.test",
        recovery_response_floor_seconds=0.001,
        kdf_max_concurrency=2,
        kdf_max_queue_depth=2,
        kdf_queue_timeout_seconds=2,
        signin_rate_capacity=100,
        signin_rate_window_seconds=60,
        signup_rate_capacity=100,
        signup_source_rate_capacity=100,
        recovery_rate_capacity=100,
        recovery_source_rate_capacity=100,
        reauth_rate_capacity=100,
    )


class _CleanBreachChecker:
    async def is_breached(self, _normalized_password: str) -> bool:
        return False


class _MemoryEmailDelivery:
    def __init__(self) -> None:
        self.commands: list[EmailCommand] = []

    async def enqueue(self, command: EmailCommand) -> None:
        self.commands.append(command)

    def latest(self, command_type: type[Any]) -> Any:
        for command in reversed(self.commands):
            if isinstance(command, command_type):
                return command
        raise AssertionError(f"No captured command of type {command_type.__name__}")


def _limiters(settings: AuthSettings) -> LifecycleLimiters:
    max_keys = 128
    return LifecycleLimiters(
        signup_email=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=max_keys),
        signup_source=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=max_keys),
        recovery_email=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=max_keys),
        recovery_source=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=max_keys),
        reauth=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=max_keys),
    )


@asynccontextmanager
async def _services(
    database: Any,
    *,
    apple_reconciler: Callable[[], Awaitable[int]] | None = None,
) -> AsyncIterator[
    tuple[
        MultiAuthenticatorLifecycleService,
        AuthenticatorLifecycleService,
        _MemoryEmailDelivery,
        PasswordKdf,
        DatabaseRuntime,
    ]
]:
    settings = _settings()
    runtime = create_database_runtime(database.runtime_settings())
    kdf = PasswordKdf(
        pepper_ring=settings.password_pepper_bytes,
        current_pepper_key_id=settings.password_current_pepper_key_id,
        max_concurrency=2,
        max_queue_depth=2,
        queue_timeout_seconds=2,
    )
    await kdf.start()
    delivery = _MemoryEmailDelivery()
    lifecycle = MultiAuthenticatorLifecycleService(
        session_factory=runtime.session_factory,
        settings=settings,
        password_kdf=kdf,
        breach_checker=cast(Any, _CleanBreachChecker()),
        otp_codec=SignupOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=cast(EmailDeliveryPort, delivery),
        limiters=_limiters(settings),
    )
    authenticators = AuthenticatorLifecycleService(
        session_factory=runtime.session_factory,
        settings=settings,
        apple_reconciler=apple_reconciler,
    )
    try:
        yield lifecycle, authenticators, delivery, kdf, runtime
    finally:
        await kdf.aclose()
        await runtime.dispose()


@dataclass(frozen=True, slots=True)
class _SessionSeed:
    admitted: AdmittedSession
    secret: SecretStr


async def _seed_account(
    runtime: DatabaseRuntime,
    *,
    email: str,
    password_present: bool,
    recovery_restricted: bool = False,
    session_count: int = 1,
) -> tuple[UUID, UUID, list[_SessionSeed]]:
    account_ref = uuid7()
    email_ref = uuid7()
    normalized = normalize_email(email)
    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=1)
    sessions: list[_SessionSeed] = []
    session_rows: list[AuthSessionRow] = []
    for _ in range(session_count):
        secret = generate_session_secret()
        verifier = session_secret_verifier(secret)
        session_ref = uuid7()
        session_rows.append(
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
        sessions.append(
            _SessionSeed(
                admitted=AdmittedSession(
                    principal=Principal(
                        account_ref=account_ref,
                        auth_session_ref=session_ref,
                        authenticated_at=now,
                        recent_auth_at=now,
                    ),
                    expires_at=expires_at,
                    csrf_token=SecretStr("test-csrf"),
                ),
                secret=secret,
            )
        )

    rows: list[Any] = [
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
            recovery_restriction_code=(
                "provider_delivery_disabled" if recovery_restricted else None
            ),
            recovery_restriction_observed_at=(now if recovery_restricted else None),
        ),
        *session_rows,
    ]
    if password_present:
        rows.append(
            PasswordCredentialRow(
                password_credential_ref=uuid7(),
                account_ref=account_ref,
                verifier="$argon2id$v=19$synthetic",
                pepper_key_id=_KEY_ID,
                created_at=now,
                updated_at=now,
            )
        )

    async with runtime.session_factory() as session, session.begin():
        session.add_all(rows)
    return account_ref, email_ref, sessions


async def _seed_provider(
    runtime: DatabaseRuntime,
    *,
    account_ref: UUID,
    email_ref: UUID,
    provider_code: str,
    subject: str,
    status_code: str = "active",
) -> UUID:
    identity_ref = uuid7()
    now = datetime.now(UTC)
    issuer = GOOGLE_ISSUER if provider_code == "google" else APPLE_ISSUER
    async with runtime.session_factory() as session, session.begin():
        session.add(
            ExternalIdentityRow(
                external_identity_ref=identity_ref,
                account_ref=account_ref,
                email_identity_ref=email_ref,
                provider_code=provider_code,
                issuer=issuer,
                subject=subject,
                provider_email_address=f"{provider_code}.{subject}@example.com",
                provider_email_private=False,
                status_code=status_code,
                created_at=now,
                status_changed_at=now,
                last_authenticated_at=now,
                revoked_at=(now if status_code == "revoked" else None),
                revocation_reason_code=("user_unlinked" if status_code == "revoked" else None),
            )
        )
    return identity_ref


async def _seed_active_apple_grant(
    runtime: DatabaseRuntime,
    *,
    external_identity_ref: UUID,
    subject: str,
) -> UUID:
    grant_ref = uuid7()
    now = datetime.now(UTC)
    async with runtime.session_factory() as session, session.begin():
        session.add(
            AppleAuthGrantRow(
                apple_auth_grant_ref=grant_ref,
                external_identity_ref=external_identity_ref,
                issuer=APPLE_ISSUER,
                subject=subject,
                client_id="dante.apple.test",
                refresh_token_ciphertext=b"x" * 32,
                refresh_token_nonce=b"n" * 12,
                encryption_key_id=_KEY_ID,
                status_code="active",
                created_at=now,
                updated_at=now,
                status_changed_at=now,
                pending_expires_at=None,
                revocation_requested_at=None,
                revoked_at=None,
            )
        )
    return grant_ref


async def _seed_link_challenge(
    runtime: DatabaseRuntime,
    *,
    target_account_ref: UUID,
    target_email_ref: UUID,
    subject: str,
) -> tuple[UUID, SecretStr]:
    proof = issue_flow_proof(FlowProofPurpose.PROVIDER_LINK)
    challenge_ref = uuid7()
    now = datetime.now(UTC)
    async with runtime.session_factory() as session, session.begin():
        session.add(
            ExternalLinkChallengeRow(
                external_link_challenge_ref=challenge_ref,
                target_account_ref=target_account_ref,
                target_email_identity_ref=target_email_ref,
                provider_code="google",
                issuer=GOOGLE_ISSUER,
                subject=subject,
                provider_email_address=f"{subject}@example.com",
                provider_email_private=False,
                apple_auth_grant_ref=None,
                continuation_verifier=proof.verifier,
                created_at=now,
                expires_at=now + timedelta(minutes=10),
            )
        )
    return challenge_ref, proof.secret


async def _count(runtime: DatabaseRuntime, model: type[Any]) -> int:
    async with runtime.session_factory() as session, session.begin():
        value = await session.scalar(select(func.count()).select_from(model))
    assert value is not None
    return int(value)


@pytest.mark.asyncio
async def test_remove_password_blocks_last_direct_authenticator(migrated_database: Any) -> None:
    async with _services(migrated_database) as (lifecycle, _authenticators, _delivery, _kdf, runtime):
        _account_ref, _email_ref, sessions = await _seed_account(
            runtime,
            email="password-only@example.com",
            password_present=True,
        )
        current = sessions[0]

        with pytest.raises(AuthenticatorRemovalBlockedError):
            await lifecycle.remove_password(
                admitted=current.admitted,
                presented_session_secret=current.secret.get_secret_value(),
            )

        assert await _count(runtime, PasswordCredentialRow) == 1


@pytest.mark.asyncio
async def test_remove_password_blocks_passwordless_state_without_recovery_email(
    migrated_database: Any,
) -> None:
    async with _services(migrated_database) as (lifecycle, _authenticators, _delivery, _kdf, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="restricted@example.com",
            password_present=True,
            recovery_restricted=True,
        )
        await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="google",
            subject="restricted-provider",
        )

        with pytest.raises(AuthenticatorRemovalBlockedError):
            await lifecycle.remove_password(
                admitted=sessions[0].admitted,
                presented_session_secret=sessions[0].secret.get_secret_value(),
            )

        assert await _count(runtime, PasswordCredentialRow) == 1


@pytest.mark.asyncio
async def test_establish_password_invalidates_recovery_and_rotates_current_bearer(
    migrated_database: Any,
) -> None:
    async with _services(migrated_database) as (lifecycle, _authenticators, delivery, _kdf, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="provider-only@example.com",
            password_present=False,
        )
        await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="google",
            subject="provider-only",
        )
        current = sessions[0]
        await lifecycle.request_password_recovery(
            email="provider-only@example.com",
            source_context="establish-recovery",
        )
        assert isinstance(delivery.latest(PasswordRecoveryEmail), PasswordRecoveryEmail)
        assert await _count(runtime, PasswordRecoveryChallengeRow) == 1

        issued = await lifecycle.establish_password(
            admitted=current.admitted,
            presented_session_secret=current.secret.get_secret_value(),
            new_password=_VALID_SECRET_PHRASE,
        )

        assert await _count(runtime, PasswordCredentialRow) == 1
        assert await _count(runtime, PasswordRecoveryChallengeRow) == 0
        async with runtime.session_factory() as session, session.begin():
            auth_session = await session.scalar(
                select(AuthSessionRow).where(
                    AuthSessionRow.auth_session_ref
                    == current.admitted.principal.auth_session_ref
                )
            )
        assert auth_session is not None
        assert auth_session.secret_verifier == session_secret_verifier(issued.session_secret)
        assert auth_session.secret_verifier != session_secret_verifier(current.secret)


@pytest.mark.asyncio
async def test_passwordless_recovery_creates_first_password_revokes_sessions_and_does_not_login(
    migrated_database: Any,
) -> None:
    async with _services(migrated_database) as (lifecycle, _authenticators, delivery, kdf, runtime):
        account_ref, email_ref, _sessions = await _seed_account(
            runtime,
            email="passwordless-recovery@example.com",
            password_present=False,
            session_count=2,
        )
        await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="google",
            subject="passwordless-recovery",
        )

        await lifecycle.request_password_recovery(
            email="passwordless-recovery@example.com",
            source_context="passwordless-recovery",
        )
        recovery = cast(PasswordRecoveryEmail, delivery.latest(PasswordRecoveryEmail))
        await lifecycle.reset_password(
            password_recovery_ref=recovery.password_recovery_ref,
            secret=recovery.secret.get_secret_value(),
            new_password=_REPLACEMENT_SECRET_PHRASE,
        )

        async with runtime.session_factory() as session, session.begin():
            credential = await session.scalar(
                select(PasswordCredentialRow).where(
                    PasswordCredentialRow.account_ref == account_ref
                )
            )
            unrevoked = await session.scalar(
                select(func.count())
                .select_from(AuthSessionRow)
                .where(
                    AuthSessionRow.account_ref == account_ref,
                    AuthSessionRow.revoked_at.is_(None),
                )
            )
            session_count = await session.scalar(
                select(func.count())
                .select_from(AuthSessionRow)
                .where(AuthSessionRow.account_ref == account_ref)
            )
        assert credential is not None
        verification = await kdf.verify(
            normalized_password=normalize_password_for_authentication(_REPLACEMENT_SECRET_PHRASE),
            verifier=credential.verifier,
            pepper_key_id=credential.pepper_key_id,
        )
        assert verification.valid is True
        assert unrevoked == 0
        assert session_count == 2
        assert await _count(runtime, PasswordRecoveryChallengeRow) == 0
        assert isinstance(delivery.latest(PasswordResetNotificationEmail), PasswordResetNotificationEmail)


@pytest.mark.asyncio
async def test_provider_link_reactivates_same_account_lifetime_identity(migrated_database: Any) -> None:
    async with _services(migrated_database) as (_lifecycle, authenticators, _delivery, _kdf, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="link-reactivation@example.com",
            password_present=True,
        )
        identity_ref = await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="google",
            subject="reactivation-subject",
            status_code="revoked",
        )
        challenge_ref, continuation = await _seed_link_challenge(
            runtime,
            target_account_ref=account_ref,
            target_email_ref=email_ref,
            subject="reactivation-subject",
        )

        issued = await authenticators.confirm_provider_link(
            admitted=sessions[0].admitted,
            presented_session_secret=sessions[0].secret.get_secret_value(),
            external_link_challenge_ref=challenge_ref,
            continuation_secret=continuation.get_secret_value(),
        )

        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.external_identity_ref == identity_ref
                )
            )
            challenge = await session.scalar(
                select(ExternalLinkChallengeRow).where(
                    ExternalLinkChallengeRow.external_link_challenge_ref == challenge_ref
                )
            )
        assert identity is not None
        assert identity.status_code == "active"
        assert identity.email_identity_ref == email_ref
        assert challenge is None
        assert issued.principal.account_ref == account_ref


@pytest.mark.asyncio
async def test_provider_link_rejects_authenticated_account_mismatch(migrated_database: Any) -> None:
    async with _services(migrated_database) as (_lifecycle, authenticators, _delivery, _kdf, runtime):
        target_account, target_email, _target_sessions = await _seed_account(
            runtime,
            email="link-target@example.com",
            password_present=True,
        )
        _other_account, _other_email, other_sessions = await _seed_account(
            runtime,
            email="link-other@example.com",
            password_present=True,
        )
        challenge_ref, continuation = await _seed_link_challenge(
            runtime,
            target_account_ref=target_account,
            target_email_ref=target_email,
            subject="link-mismatch",
        )

        with pytest.raises(ProviderLinkAccountMismatchError):
            await authenticators.confirm_provider_link(
                admitted=other_sessions[0].admitted,
                presented_session_secret=other_sessions[0].secret.get_secret_value(),
                external_link_challenge_ref=challenge_ref,
                continuation_secret=continuation.get_secret_value(),
            )

        assert await _count(runtime, ExternalLinkChallengeRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 0


@pytest.mark.asyncio
async def test_unlink_provider_blocks_last_direct_authenticator(migrated_database: Any) -> None:
    async with _services(migrated_database) as (_lifecycle, authenticators, _delivery, _kdf, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="last-provider@example.com",
            password_present=False,
        )
        identity_ref = await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="google",
            subject="last-provider",
        )

        with pytest.raises(AuthenticatorRemovalBlockedError):
            await authenticators.unlink_provider(
                admitted=sessions[0].admitted,
                presented_session_secret=sessions[0].secret.get_secret_value(),
                external_identity_ref=identity_ref,
            )

        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.external_identity_ref == identity_ref
                )
            )
        assert identity is not None
        assert identity.status_code == "active"


@pytest.mark.asyncio
async def test_apple_unlink_is_locally_durable_when_remote_reconciliation_is_pending(
    migrated_database: Any,
) -> None:
    async def pending_reconciler() -> int:
        raise ProviderReconciliationPendingError()

    async with _services(
        migrated_database,
        apple_reconciler=pending_reconciler,
    ) as (_lifecycle, authenticators, _delivery, _kdf, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="apple-unlink@example.com",
            password_present=True,
        )
        subject = "apple-unlink-subject"
        identity_ref = await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="apple",
            subject=subject,
        )
        grant_ref = await _seed_active_apple_grant(
            runtime,
            external_identity_ref=identity_ref,
            subject=subject,
        )

        issued = await authenticators.unlink_provider(
            admitted=sessions[0].admitted,
            presented_session_secret=sessions[0].secret.get_secret_value(),
            external_identity_ref=identity_ref,
        )

        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.external_identity_ref == identity_ref
                )
            )
            grant = await session.scalar(
                select(AppleAuthGrantRow).where(
                    AppleAuthGrantRow.apple_auth_grant_ref == grant_ref
                )
            )
        assert identity is not None
        assert identity.status_code == "revoked"
        assert identity.revocation_reason_code == "user_unlinked"
        assert grant is not None
        assert grant.status_code == "revocation_pending"
        assert grant.revocation_requested_at is not None
        assert issued.principal.account_ref == account_ref


@pytest.mark.asyncio
async def test_concurrent_password_and_provider_removal_preserves_one_direct_authenticator(
    migrated_database: Any,
) -> None:
    async with _services(migrated_database) as (lifecycle, authenticators, _delivery, _kdf, runtime):
        account_ref, email_ref, sessions = await _seed_account(
            runtime,
            email="removal-race@example.com",
            password_present=True,
            session_count=2,
        )
        identity_ref = await _seed_provider(
            runtime,
            account_ref=account_ref,
            email_ref=email_ref,
            provider_code="google",
            subject="removal-race-provider",
        )

        outcomes = await asyncio.gather(
            lifecycle.remove_password(
                admitted=sessions[0].admitted,
                presented_session_secret=sessions[0].secret.get_secret_value(),
            ),
            authenticators.unlink_provider(
                admitted=sessions[1].admitted,
                presented_session_secret=sessions[1].secret.get_secret_value(),
                external_identity_ref=identity_ref,
            ),
            return_exceptions=True,
        )

        assert sum(isinstance(outcome, IssuedSession) for outcome in outcomes) == 1
        assert sum(isinstance(outcome, AuthenticatorRemovalBlockedError) for outcome in outcomes) == 1
        async with runtime.session_factory() as session, session.begin():
            password_count = await session.scalar(
                select(func.count())
                .select_from(PasswordCredentialRow)
                .where(PasswordCredentialRow.account_ref == account_ref)
            )
            provider_count = await session.scalar(
                select(func.count())
                .select_from(ExternalIdentityRow)
                .where(
                    ExternalIdentityRow.account_ref == account_ref,
                    ExternalIdentityRow.status_code == "active",
                )
            )
        assert int(password_count or 0) + int(provider_count or 0) == 1
