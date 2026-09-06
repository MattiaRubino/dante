"""Real PostgreSQL proof for M5-C Google Account/session/challenge invariants."""

from __future__ import annotations

import asyncio
from base64 import urlsafe_b64encode
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID, uuid7

import pytest
from pydantic import SecretStr
from sqlalchemy import func, select

from dante.auth.contracts import (
    AdmittedSession,
    Principal,
    ProviderAuthenticated,
    ProviderAuthenticationBegun,
    ProviderAuthenticationResult,
    ProviderEnrollmentRequired,
    ProviderLinkRequired,
    ProviderPurpose,
    ProviderReturnTarget,
    ProviderTransactionInvalidOrExpiredError,
)
from dante.auth.email import normalize_email
from dante.auth.email_delivery import (
    EmailCommand,
    EmailDeliveryPort,
    ProviderEnrollmentVerificationEmail,
)
from dante.auth.google import GoogleIdentityEvidence, GoogleTokenVerifier
from dante.auth.lifecycle import KeyedRateLimiter
from dante.auth.proofs import FlowProofPurpose, ProviderEnrollmentOtpCodec, flow_proof_verifier
from dante.auth.provider_flow import ProviderFlowLimiters, ProviderFlowService
from dante.auth.sessions import generate_session_secret, session_secret_verifier
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.auth_provider import (
    GOOGLE_ISSUER,
    AuthProviderSettings,
    GoogleProviderSettings,
)
from dante.platform.database.mappings.auth import (
    AccountProfileBootstrapRow,
    AccountRow,
    AuthSessionRow,
    EmailIdentityRow,
    ExternalAuthTransactionRow,
    ExternalIdentityRow,
    ExternalLinkChallengeRow,
    ExternalSignupChallengeRow,
)
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime

pytestmark = pytest.mark.postgres

_CLIENT_ID = "dante-google-test.apps.googleusercontent.com"
_KEY_ID = "test-key-v1"


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
            google=GoogleProviderSettings(enabled=True, client_id=_CLIENT_ID),
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


class _FakeGoogleVerifier:
    def __init__(self, evidence: GoogleIdentityEvidence) -> None:
        self.evidence = evidence
        self.calls: list[tuple[str, bytes]] = []

    async def verify(
        self,
        token: str,
        *,
        expected_nonce_verifier: bytes,
    ) -> GoogleIdentityEvidence:
        self.calls.append((token, expected_nonce_verifier))
        return self.evidence


def _evidence(
    *,
    subject: str,
    email: str,
    authoritative: bool,
    display_name: str | None = "Google Person",
) -> GoogleIdentityEvidence:
    normalized = normalize_email(email)
    return GoogleIdentityEvidence(
        issuer=GOOGLE_ISSUER,
        subject=subject,
        email=normalized,
        email_verified=True,
        hosted_domain=(normalized.comparison_key.rsplit("@", 1)[1] if authoritative else None),
        mailbox_authoritative=authoritative,
        display_name=display_name,
        given_name="Google",
        family_name="Person",
        picture_url="https://lh3.googleusercontent.com/test-avatar",
        locale="en-US",
    )


def _limiters(settings: AuthSettings) -> ProviderFlowLimiters:
    max_keys = 128
    return ProviderFlowLimiters(
        begin=KeyedRateLimiter(
            capacity=settings.provider_begin_rate_capacity,
            window_seconds=settings.provider_begin_rate_window_seconds,
            max_keys=max_keys,
        ),
        complete=KeyedRateLimiter(
            capacity=settings.provider_complete_rate_capacity,
            window_seconds=settings.provider_complete_rate_window_seconds,
            max_keys=max_keys,
        ),
        enrollment=KeyedRateLimiter(
            capacity=settings.provider_enrollment_rate_capacity,
            window_seconds=settings.provider_enrollment_rate_window_seconds,
            max_keys=max_keys,
        ),
    )


@asynccontextmanager
async def _provider_service(
    database: Any,
    *,
    evidence: GoogleIdentityEvidence,
) -> AsyncIterator[
    tuple[ProviderFlowService, _FakeGoogleVerifier, _MemoryEmailDelivery, DatabaseRuntime]
]:
    settings = _settings()
    database_runtime = create_database_runtime(database.runtime_settings())
    verifier = _FakeGoogleVerifier(evidence)
    delivery = _MemoryEmailDelivery()
    service = ProviderFlowService(
        session_factory=database_runtime.session_factory,
        settings=settings,
        google_verifier=cast(GoogleTokenVerifier, verifier),
        otp_codec=ProviderEnrollmentOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=cast(EmailDeliveryPort, delivery),
        limiters=_limiters(settings),
    )
    try:
        yield service, verifier, delivery, database_runtime
    finally:
        await database_runtime.dispose()


async def _begin_and_complete(
    service: ProviderFlowService,
    *,
    source: str,
) -> tuple[ProviderAuthenticationBegun, ProviderAuthenticationResult]:
    begun = await service.begin_google(
        purpose=ProviderPurpose.SIGN_IN,
        return_target=ProviderReturnTarget.ACCESS,
        source_context=f"{source}-begin",
    )
    result = await service.complete_google(
        external_auth_transaction_ref=begun.external_auth_transaction_ref,
        state=begun.state.get_secret_value(),
        credential=f"credential-{source}",
        source_context=f"{source}-complete",
    )
    return begun, result


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
async def test_google_begin_persists_only_verifiers_and_complete_claims_once(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="google-claim-once",
        email="claim-once@gmail.com",
        authoritative=True,
    )
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        verifier,
        _delivery,
        runtime,
    ):
        begun = await service.begin_google(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="claim-once-begin",
        )
        state_verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.PROVIDER_STATE,
            encoded_secret=begun.state.get_secret_value(),
        )
        nonce_verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.OIDC_NONCE,
            encoded_secret=begun.nonce.get_secret_value(),
        )
        assert state_verifier is not None
        assert nonce_verifier is not None

        async with runtime.session_factory() as session, session.begin():
            row = await session.scalar(
                select(ExternalAuthTransactionRow).where(
                    ExternalAuthTransactionRow.external_auth_transaction_ref
                    == begun.external_auth_transaction_ref
                )
            )
        assert row is not None
        assert row.state_verifier == state_verifier
        assert row.nonce_verifier == nonce_verifier
        assert row.claimed_at is None

        result = await service.complete_google(
            external_auth_transaction_ref=begun.external_auth_transaction_ref,
            state=begun.state.get_secret_value(),
            credential="credential-claim-once",
            source_context="claim-once-complete",
        )
        assert isinstance(result, ProviderAuthenticated)
        assert verifier.calls == [("credential-claim-once", nonce_verifier)]

        with pytest.raises(ProviderTransactionInvalidOrExpiredError):
            await service.complete_google(
                external_auth_transaction_ref=begun.external_auth_transaction_ref,
                state=begun.state.get_secret_value(),
                credential="credential-replay",
                source_context="claim-once-replay",
            )
        assert len(verifier.calls) == 1


@pytest.mark.asyncio
async def test_authoritative_google_mailbox_creates_passwordless_account_and_reuses_identity(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="google-new-account",
        email="new-account@gmail.com",
        authoritative=True,
    )
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _delivery,
        runtime,
    ):
        _first_begin, first = await _begin_and_complete(service, source="new-account-first")
        assert isinstance(first, ProviderAuthenticated)
        account_ref = first.session.principal.account_ref

        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, EmailIdentityRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AuthSessionRow) == 1
        assert await _count(runtime, AccountProfileBootstrapRow) == 1

        async with runtime.session_factory() as session, session.begin():
            identity = await session.scalar(select(ExternalIdentityRow))
            email = await session.scalar(select(EmailIdentityRow))
        assert identity is not None
        assert identity.account_ref == account_ref
        assert identity.issuer == GOOGLE_ISSUER
        assert identity.subject == "google-new-account"
        assert email is not None
        assert email.account_ref == account_ref
        assert email.verified_at is not None

        _second_begin, second = await _begin_and_complete(service, source="new-account-second")
        assert isinstance(second, ProviderAuthenticated)
        assert second.session.principal.account_ref == account_ref
        assert second.session.principal.auth_session_ref != first.session.principal.auth_session_ref
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AuthSessionRow) == 2


@pytest.mark.asyncio
async def test_google_email_collision_returns_link_required_without_silent_merge(
    migrated_database: Any,
) -> None:
    email = "existing@gmail.com"
    evidence = _evidence(subject="google-collision", email=email, authoritative=True)
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _delivery,
        runtime,
    ):
        account_ref, email_ref = await _seed_account_email(runtime, email=email)

        _begun, result = await _begin_and_complete(service, source="collision")

        assert isinstance(result, ProviderLinkRequired)
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 0
        assert await _count(runtime, AuthSessionRow) == 0
        assert await _count(runtime, ExternalLinkChallengeRow) == 1
        async with runtime.session_factory() as session, session.begin():
            challenge = await session.scalar(select(ExternalLinkChallengeRow))
        assert challenge is not None
        assert challenge.target_account_ref == account_ref
        assert challenge.target_email_identity_ref == email_ref
        assert challenge.subject == "google-collision"


@pytest.mark.asyncio
async def test_third_party_google_mailbox_requires_dante_otp_before_account_creation(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="google-third-party",
        email="person@third-party.example",
        authoritative=False,
    )
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        delivery,
        runtime,
    ):
        _begun, result = await _begin_and_complete(service, source="third-party")
        assert isinstance(result, ProviderEnrollmentRequired)
        assert await _count(runtime, AccountRow) == 0
        assert await _count(runtime, ExternalSignupChallengeRow) == 1

        email_command = delivery.latest_provider_otp()
        completed = await service.verify_provider_enrollment(
            external_signup_ref=result.external_signup_ref,
            continuation_secret=result.continuation_secret.get_secret_value(),
            code=email_command.code.get_secret_value(),
            source_context="third-party-verify",
        )
        assert isinstance(completed, ProviderAuthenticated)
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, EmailIdentityRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AuthSessionRow) == 1
        assert await _count(runtime, ExternalSignupChallengeRow) == 0


@pytest.mark.asyncio
async def test_verified_provider_enrollment_collision_transitions_to_link_required(
    migrated_database: Any,
) -> None:
    email = "enrollment-collision@example.com"
    evidence = _evidence(
        subject="google-enrollment-collision",
        email=email,
        authoritative=False,
    )
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        delivery,
        runtime,
    ):
        _begun, result = await _begin_and_complete(service, source="enrollment-collision")
        assert isinstance(result, ProviderEnrollmentRequired)
        account_ref, _email_ref = await _seed_account_email(runtime, email=email)

        email_command = delivery.latest_provider_otp()
        completed = await service.verify_provider_enrollment(
            external_signup_ref=result.external_signup_ref,
            continuation_secret=result.continuation_secret.get_secret_value(),
            code=email_command.code.get_secret_value(),
            source_context="enrollment-collision-verify",
        )
        assert isinstance(completed, ProviderLinkRequired)
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 0
        assert await _count(runtime, ExternalSignupChallengeRow) == 0
        assert await _count(runtime, ExternalLinkChallengeRow) == 1
        async with runtime.session_factory() as session, session.begin():
            challenge = await session.scalar(select(ExternalLinkChallengeRow))
        assert challenge is not None
        assert challenge.target_account_ref == account_ref


@pytest.mark.asyncio
async def test_concurrent_same_google_identity_converges_on_one_account(
    migrated_database: Any,
) -> None:
    evidence = _evidence(
        subject="google-concurrent",
        email="concurrent@gmail.com",
        authoritative=True,
    )
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        _verifier,
        _delivery,
        runtime,
    ):
        first_begin = await service.begin_google(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="concurrent-begin-1",
        )
        second_begin = await service.begin_google(
            purpose=ProviderPurpose.SIGN_IN,
            return_target=ProviderReturnTarget.ACCESS,
            source_context="concurrent-begin-2",
        )

        first_result, second_result = await asyncio.gather(
            service.complete_google(
                external_auth_transaction_ref=first_begin.external_auth_transaction_ref,
                state=first_begin.state.get_secret_value(),
                credential="credential-concurrent-1",
                source_context="concurrent-complete-1",
            ),
            service.complete_google(
                external_auth_transaction_ref=second_begin.external_auth_transaction_ref,
                state=second_begin.state.get_secret_value(),
                credential="credential-concurrent-2",
                source_context="concurrent-complete-2",
            ),
        )

        assert isinstance(first_result, ProviderAuthenticated)
        assert isinstance(second_result, ProviderAuthenticated)
        assert (
            first_result.session.principal.account_ref
            == second_result.session.principal.account_ref
        )
        assert await _count(runtime, AccountRow) == 1
        assert await _count(runtime, EmailIdentityRow) == 1
        assert await _count(runtime, ExternalIdentityRow) == 1
        assert await _count(runtime, AuthSessionRow) == 2
        assert await _count(runtime, ExternalLinkChallengeRow) == 0


@pytest.mark.asyncio
async def test_authenticated_google_link_and_reauth_rotate_same_session_bearer(
    migrated_database: Any,
) -> None:
    base_email = "linked-account@example.com"
    evidence = _evidence(
        subject="google-direct-link",
        email="linked-google@gmail.com",
        authoritative=True,
    )
    async with _provider_service(migrated_database, evidence=evidence) as (
        service,
        verifier,
        _delivery,
        runtime,
    ):
        account_ref, _email_ref = await _seed_account_email(runtime, email=base_email)
        admitted, original_secret = await _seed_session(runtime, account_ref=account_ref)
        original_session_ref = admitted.principal.auth_session_ref

        link_begin = await service.begin_google(
            purpose=ProviderPurpose.LINK,
            return_target=ProviderReturnTarget.SECURITY,
            source_context="direct-link-begin",
            admitted=admitted,
            presented_session_secret=original_secret.get_secret_value(),
        )
        linked = await service.complete_google(
            external_auth_transaction_ref=link_begin.external_auth_transaction_ref,
            state=link_begin.state.get_secret_value(),
            credential="credential-link",
            source_context="direct-link-complete",
        )
        assert isinstance(linked, ProviderAuthenticated)
        assert linked.session.principal.account_ref == account_ref
        assert linked.session.principal.auth_session_ref == original_session_ref
        assert (
            linked.session.session_secret.get_secret_value() != original_secret.get_secret_value()
        )
        assert await _count(runtime, ExternalIdentityRow) == 1

        verifier.evidence = evidence
        reauth_begin = await service.begin_google(
            purpose=ProviderPurpose.REAUTHENTICATE,
            return_target=ProviderReturnTarget.SECURITY,
            source_context="reauth-begin",
            admitted=AdmittedSession(
                principal=linked.session.principal,
                expires_at=linked.session.expires_at,
                csrf_token=linked.session.csrf_token,
            ),
            presented_session_secret=linked.session.session_secret.get_secret_value(),
        )
        reauthenticated = await service.complete_google(
            external_auth_transaction_ref=reauth_begin.external_auth_transaction_ref,
            state=reauth_begin.state.get_secret_value(),
            credential="credential-reauth",
            source_context="reauth-complete",
        )
        assert isinstance(reauthenticated, ProviderAuthenticated)
        assert reauthenticated.session.principal.auth_session_ref == original_session_ref
        assert (
            reauthenticated.session.session_secret.get_secret_value()
            != linked.session.session_secret.get_secret_value()
        )
        assert (
            reauthenticated.session.principal.recent_auth_at
            >= linked.session.principal.recent_auth_at
        )
        assert await _count(runtime, AuthSessionRow) == 1
