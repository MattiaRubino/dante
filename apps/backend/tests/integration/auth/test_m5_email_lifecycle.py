"""Real PostgreSQL proof that Auth mutations and durable EmailIntents share one transaction."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, cast, override
from uuid import UUID, uuid7

import psycopg
import pytest
from pydantic import SecretStr
from sqlalchemy import select

from dante.auth.contracts import AuthIntegrityError, IssuedSession
from dante.auth.email_contracts import ClaimedEmailIntent, EmailIntentConflictError
from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_delivery import EmailCommand, EmailDeliveryPort
from dante.auth.email_outbox import DurableEmailOutbox
from dante.auth.lifecycle import AuthLifecycleService, KeyedRateLimiter, LifecycleLimiters
from dante.auth.passwords import PasswordKdf
from dante.auth.proofs import SignupOtpCodec
from dante.platform.config.auth import AuthSettings, EmailTransport, SmtpSecurity
from dante.platform.database.mappings.email_delivery import EmailDeliveryIntentRow
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime

pytestmark = pytest.mark.postgres

_EMAIL = "m5.email.lifecycle@example.com"
_TEST_CREDENTIAL = "correct horse battery staple"
_REPLACEMENT_TEST_CREDENTIAL = "replacement horse battery staple"
_CREDENTIAL_KEY_ID = "test-password-v1"
_OTP_KEY_ID = "test-signup-otp-v1"
_EMAIL_KEY_ID = "test-email-v1"
_CREDENTIAL_KEY = b"p" * 32
_OTP_KEY = b"o" * 32
_EMAIL_KEY = b"e" * 32
_CSRF_KEY = b"c" * 32
_COUNT_QUERIES = {
    "password_signup_challenge": "SELECT count(*) FROM dante.password_signup_challenge",
    "password_recovery_challenge": "SELECT count(*) FROM dante.password_recovery_challenge",
    "email_delivery_intent": "SELECT count(*) FROM dante.email_delivery_intent",
    "account": "SELECT count(*) FROM dante.account",
    "auth_session": "SELECT count(*) FROM dante.auth_session",
}


def _encoded(raw: bytes) -> str:
    from base64 import urlsafe_b64encode

    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


class _CleanBreachChecker:
    async def is_breached(self, _normalized_password: str) -> bool:
        return False


class _MemoryEmailDelivery(EmailDeliveryPort):
    def __init__(self) -> None:
        self.commands: list[EmailCommand] = []

    @override
    async def enqueue(self, command: EmailCommand) -> None:
        self.commands.append(command)


@dataclass(slots=True)
class _WakeCounter:
    count: int = 0

    def wake(self) -> None:
        self.count += 1


class _ConflictingOutbox:
    async def stage(self, *_args: Any, **_kwargs: Any) -> UUID | None:
        raise EmailIntentConflictError("injected conflict")


def _settings() -> AuthSettings:
    return AuthSettings(
        canonical_web_origin="https://dante.test",
        password_current_pepper_key_id=_CREDENTIAL_KEY_ID,
        password_peppers={_CREDENTIAL_KEY_ID: SecretStr(_encoded(_CREDENTIAL_KEY))},
        csrf_key=SecretStr(_encoded(_CSRF_KEY)),
        signup_otp_current_key_id=_OTP_KEY_ID,
        signup_otp_keys={_OTP_KEY_ID: SecretStr(_encoded(_OTP_KEY))},
        smtp_host="127.0.0.1",
        smtp_port=9,
        smtp_security=SmtpSecurity.PLAIN,
        smtp_from_address="no-reply@dante.test",
        email_platform_enabled=True,
        email_transport=EmailTransport.SMTP,
        email_payload_current_key_id=_EMAIL_KEY_ID,
        email_payload_keys={_EMAIL_KEY_ID: SecretStr(_encoded(_EMAIL_KEY))},
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


def _limiters() -> LifecycleLimiters:
    return LifecycleLimiters(
        signup_email=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        signup_source=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        recovery_email=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        recovery_source=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
        reauth=KeyedRateLimiter(capacity=100, window_seconds=60, max_keys=128),
    )


@dataclass(slots=True)
class _LifecycleHarness:
    service: AuthLifecycleService
    outbox: DurableEmailOutbox
    cipher: EmailPayloadCipher
    fallback: _MemoryEmailDelivery
    wake: _WakeCounter
    password_kdf: PasswordKdf
    database_runtime: DatabaseRuntime


@asynccontextmanager
async def _lifecycle(database: Any) -> AsyncIterator[_LifecycleHarness]:
    settings = _settings()
    database_runtime = create_database_runtime(database.runtime_settings())
    password_kdf = PasswordKdf(
        pepper_ring=settings.password_pepper_bytes,
        current_pepper_key_id=settings.password_current_pepper_key_id,
        max_concurrency=2,
        max_queue_depth=2,
        queue_timeout_seconds=2,
    )
    await password_kdf.start()
    cipher = EmailPayloadCipher(
        key_ring=settings.email_payload_key_bytes,
        current_key_id=_EMAIL_KEY_ID,
    )
    outbox = DurableEmailOutbox(cipher=cipher, attempt_limit=3)
    fallback = _MemoryEmailDelivery()
    wake = _WakeCounter()
    service = AuthLifecycleService(
        session_factory=database_runtime.session_factory,
        settings=settings,
        password_kdf=password_kdf,
        breach_checker=cast(Any, _CleanBreachChecker()),
        otp_codec=SignupOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=fallback,
        email_outbox=outbox,
        email_wake=wake.wake,
        limiters=_limiters(),
    )
    try:
        yield _LifecycleHarness(
            service=service,
            outbox=outbox,
            cipher=cipher,
            fallback=fallback,
            wake=wake,
            password_kdf=password_kdf,
            database_runtime=database_runtime,
        )
    finally:
        await password_kdf.aclose()
        await database_runtime.dispose()


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs(
            database.cluster.admin_user,
            database.cluster.admin_password,
        )
    )


def _count(database: Any, table_name: str) -> int:
    query = _COUNT_QUERIES.get(table_name)
    if query is None:
        raise AssertionError("test requested an unapproved table")
    with _admin(database) as connection:
        row = connection.execute(query).fetchone()
    assert row is not None
    return int(row[0])


async def _latest_intent_payload(
    harness: _LifecycleHarness,
    *,
    operation_scope: str,
) -> tuple[EmailDeliveryIntentRow, dict[str, str | int]]:
    async with harness.database_runtime.session_factory() as session, session.begin():
        row = await session.scalar(
            select(EmailDeliveryIntentRow)
            .where(EmailDeliveryIntentRow.operation_scope == operation_scope)
            .order_by(EmailDeliveryIntentRow.created_at.desc())
            .limit(1)
        )
        assert row is not None
        claim = ClaimedEmailIntent(
            email_intent_ref=row.email_intent_ref,
            email_attempt_ref=uuid7(),
            claim_token=uuid7(),
            purpose_code=row.purpose_code,
            template_code=row.template_code,
            template_revision=row.template_revision,
            locale_code=row.locale_code,
            recipient_address=row.recipient_address,
            recipient_comparison_key=row.recipient_comparison_key,
            sensitive_key_id=row.sensitive_key_id,
            sensitive_nonce=row.sensitive_nonce,
            sensitive_ciphertext=row.sensitive_ciphertext,
            attempt_number=max(1, row.attempt_count),
            expires_at=row.expires_at,
        )
        payload = harness.cipher.unprotect(claim=claim)
        return row, payload


@pytest.mark.asyncio
async def test_signup_challenge_and_email_intent_commit_together(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as harness:
        created = await harness.service.create_signup(
            email=_EMAIL,
            password=_TEST_CREDENTIAL,
            source_context="email-lifecycle-signup",
        )

        assert _count(migrated_database, "password_signup_challenge") == 1
        assert _count(migrated_database, "email_delivery_intent") == 1
        assert harness.fallback.commands == []
        assert harness.wake.count == 1

        intent, payload = await _latest_intent_payload(
            harness,
            operation_scope="auth.signup_verification",
        )
        assert intent.idempotency_key.startswith(f"{created.signup_ref}:")
        assert intent.supersession_key == f"signup:{created.signup_ref}"
        assert intent.template_revision == "2"
        assert intent.dispatch_state_code == "pending"
        assert isinstance(payload["code"], str)
        assert payload["expires_minutes"] == 15


@pytest.mark.asyncio
async def test_email_stage_conflict_rolls_back_signup_challenge(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as harness:
        settings = _settings()
        failing_service = AuthLifecycleService(
            session_factory=harness.database_runtime.session_factory,
            settings=settings,
            password_kdf=harness.password_kdf,
            breach_checker=cast(Any, _CleanBreachChecker()),
            otp_codec=SignupOtpCodec(
                key_ring=settings.signup_otp_key_bytes,
                current_key_id=_OTP_KEY_ID,
            ),
            email_delivery=harness.fallback,
            email_outbox=cast(DurableEmailOutbox, cast(Any, _ConflictingOutbox())),
            email_wake=harness.wake.wake,
            limiters=_limiters(),
        )

        with pytest.raises(AuthIntegrityError, match="email intent idempotency conflict"):
            await failing_service.create_signup(
                email="rollback@example.com",
                password=_TEST_CREDENTIAL,
                source_context="email-lifecycle-rollback",
            )

        assert _count(migrated_database, "password_signup_challenge") == 0
        assert _count(migrated_database, "email_delivery_intent") == 0
        assert harness.fallback.commands == []
        assert harness.wake.count == 0


@pytest.mark.asyncio
async def test_recovery_and_reset_security_intents_follow_canonical_auth_mutations(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as harness:
        created = await harness.service.create_signup(
            email=_EMAIL,
            password=_TEST_CREDENTIAL,
            source_context="email-lifecycle-account",
        )
        _signup_intent, signup_payload = await _latest_intent_payload(
            harness,
            operation_scope="auth.signup_verification",
        )
        issued = await harness.service.verify_signup(
            signup_ref=created.signup_ref,
            code=cast(str, signup_payload["code"]),
        )
        assert isinstance(issued, IssuedSession)
        assert _count(migrated_database, "account") == 1

        await harness.service.request_password_recovery(
            email=_EMAIL,
            source_context="email-lifecycle-recovery",
        )
        recovery_intent, recovery_payload = await _latest_intent_payload(
            harness,
            operation_scope="auth.password_recovery",
        )
        recovery_ref = UUID(cast(str, recovery_payload["password_recovery_ref"]))
        recovery_secret = cast(str, recovery_payload["secret"])

        assert _count(migrated_database, "password_recovery_challenge") == 1
        assert recovery_intent.idempotency_key == str(recovery_ref)
        assert (
            recovery_intent.supersession_key == f"password-recovery:{issued.principal.account_ref}"
        )

        await harness.service.reset_password(
            password_recovery_ref=recovery_ref,
            secret=recovery_secret,
            new_password=_REPLACEMENT_TEST_CREDENTIAL,
        )

        assert _count(migrated_database, "password_recovery_challenge") == 0
        assert _count(migrated_database, "auth_session") == 1
        notification, notification_payload = await _latest_intent_payload(
            harness,
            operation_scope="auth.password_reset_notification",
        )
        assert notification.idempotency_key == str(recovery_ref)
        assert notification_payload == {}
        assert harness.fallback.commands == []
        assert harness.wake.count == 3

        with _admin(migrated_database) as connection:
            revoked = connection.execute(
                "SELECT revoked_at, revocation_reason_code FROM dante.auth_session"
            ).fetchone()
        assert revoked is not None
        assert revoked[0] is not None
        assert revoked[1] == "password_reset"
