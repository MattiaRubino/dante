"""Real PostgreSQL proof for M4 signup, recovery/reset and reauthentication invariants."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, cast

import psycopg
import pytest
from pydantic import SecretStr

from dante.auth.contracts import (
    AdmittedSession,
    ExistingAccountSignupResult,
    InvalidCredentialsError,
    IssuedSession,
    RecoveryInvalidOrExpiredError,
)
from dante.auth.email_delivery import (
    EmailCommand,
    PasswordRecoveryEmail,
    PasswordResetNotificationEmail,
    SignupVerificationEmail,
)
from dante.auth.lifecycle import AuthLifecycleService, KeyedRateLimiter, LifecycleLimiters
from dante.auth.passwords import PasswordKdf, normalize_password_for_authentication
from dante.auth.proofs import SignupOtpCodec
from dante.auth.sessions import session_secret_verifier
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.database.runtime import DatabaseRuntime, create_database_runtime

pytestmark = pytest.mark.postgres

_EMAIL = "m4.lifecycle@example.com"
_PASSWORD = "correct horse battery staple"
_NEW_PASSWORD = "replacement horse battery staple"
_PEPPER_KEY_ID = "test-password-v1"
_OTP_KEY_ID = "test-signup-otp-v1"
_PEPPER = b"p" * 32
_OTP_KEY = b"o" * 32
_CSRF_KEY = b"c" * 32


def _encoded(raw: bytes) -> str:
    from base64 import urlsafe_b64encode

    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


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


def _auth_settings() -> AuthSettings:
    return AuthSettings(
        canonical_web_origin="https://dante.test",
        password_current_pepper_key_id=_PEPPER_KEY_ID,
        password_peppers={_PEPPER_KEY_ID: SecretStr(_encoded(_PEPPER))},
        csrf_key=SecretStr(_encoded(_CSRF_KEY)),
        signup_otp_current_key_id=_OTP_KEY_ID,
        signup_otp_keys={_OTP_KEY_ID: SecretStr(_encoded(_OTP_KEY))},
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
async def _lifecycle(
    database: Any,
) -> AsyncIterator[tuple[AuthLifecycleService, _MemoryEmailDelivery, PasswordKdf, DatabaseRuntime]]:
    settings = _auth_settings()
    database_runtime = create_database_runtime(database.runtime_settings())
    password_kdf = PasswordKdf(
        pepper_ring=settings.password_pepper_bytes,
        current_pepper_key_id=settings.password_current_pepper_key_id,
        max_concurrency=2,
        max_queue_depth=2,
        queue_timeout_seconds=2,
    )
    await password_kdf.start()
    email_delivery = _MemoryEmailDelivery()
    service = AuthLifecycleService(
        session_factory=database_runtime.session_factory,
        settings=settings,
        password_kdf=password_kdf,
        breach_checker=cast(Any, _CleanBreachChecker()),
        otp_codec=SignupOtpCodec(
            key_ring=settings.signup_otp_key_bytes,
            current_key_id=settings.signup_otp_current_key_id,
        ),
        email_delivery=email_delivery,
        limiters=_limiters(settings),
    )
    try:
        yield service, email_delivery, password_kdf, database_runtime
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


def _count(database: Any, sql: str, params: tuple[object, ...] = ()) -> int:
    with _admin(database) as connection:
        row = connection.execute(sql, params).fetchone()
    assert row is not None
    return int(row[0])


async def _establish_account(
    service: AuthLifecycleService,
    email_delivery: _MemoryEmailDelivery,
    *,
    email: str = _EMAIL,
    password: str = _PASSWORD,
    source: str = "integration-source",
) -> IssuedSession:
    created = await service.create_signup(
        email=email,
        password=password,
        source_context=source,
    )
    verification = cast(
        SignupVerificationEmail,
        email_delivery.latest(SignupVerificationEmail),
    )
    result = await service.verify_signup(
        signup_ref=created.signup_ref,
        code=verification.code.get_secret_value(),
    )
    assert isinstance(result, IssuedSession)
    return result


@pytest.mark.asyncio
async def test_signup_creates_no_canonical_account_until_valid_mailbox_proof(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as (service, email_delivery, _kdf, _runtime):
        created = await service.create_signup(
            email=_EMAIL,
            password=_PASSWORD,
            source_context="signup-source",
        )

        assert _count(migrated_database, "SELECT count(*) FROM dante.account") == 0
        assert _count(migrated_database, "SELECT count(*) FROM dante.email_identity") == 0
        assert _count(migrated_database, "SELECT count(*) FROM dante.password_credential") == 0
        assert _count(migrated_database, "SELECT count(*) FROM dante.auth_session") == 0
        assert _count(
            migrated_database,
            "SELECT count(*) FROM dante.password_signup_challenge WHERE signup_ref = %s",
            (created.signup_ref,),
        ) == 1

        verification = cast(
            SignupVerificationEmail,
            email_delivery.latest(SignupVerificationEmail),
        )
        issued = await service.verify_signup(
            signup_ref=created.signup_ref,
            code=verification.code.get_secret_value(),
        )
        assert isinstance(issued, IssuedSession)

        assert _count(migrated_database, "SELECT count(*) FROM dante.account") == 1
        assert _count(migrated_database, "SELECT count(*) FROM dante.email_identity") == 1
        assert _count(migrated_database, "SELECT count(*) FROM dante.password_credential") == 1
        assert _count(migrated_database, "SELECT count(*) FROM dante.auth_session") == 1
        assert _count(migrated_database, "SELECT count(*) FROM dante.password_signup_challenge") == 0


@pytest.mark.asyncio
async def test_verified_existing_email_never_overwrites_existing_password_or_creates_session(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as (service, email_delivery, _kdf, _runtime):
        first = await _establish_account(service, email_delivery)
        with _admin(migrated_database) as connection:
            before = connection.execute(
                "SELECT verifier, pepper_key_id, updated_at FROM dante.password_credential"
            ).fetchone()
        assert before is not None

        created = await service.create_signup(
            email=_EMAIL,
            password="attacker-chosen replacement password",
            source_context="second-signup-source",
        )
        verification = cast(
            SignupVerificationEmail,
            email_delivery.latest(SignupVerificationEmail),
        )
        result = await service.verify_signup(
            signup_ref=created.signup_ref,
            code=verification.code.get_secret_value(),
        )

        assert isinstance(result, ExistingAccountSignupResult)
        with _admin(migrated_database) as connection:
            after = connection.execute(
                "SELECT verifier, pepper_key_id, updated_at FROM dante.password_credential"
            ).fetchone()
        assert after == before
        assert _count(migrated_database, "SELECT count(*) FROM dante.account") == 1
        assert _count(migrated_database, "SELECT count(*) FROM dante.auth_session") == 1
        assert _count(migrated_database, "SELECT count(*) FROM dante.password_signup_challenge") == 0
        assert first.principal.account_ref is not None


@pytest.mark.asyncio
async def test_recovery_supersedes_prior_proof_and_reset_consumes_once_revoking_all_sessions(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as (service, email_delivery, password_kdf, _runtime):
        issued = await _establish_account(service, email_delivery)
        email_delivery.commands.clear()

        await service.request_password_recovery(
            email=_EMAIL,
            source_context="recovery-source-1",
        )
        first_mail = cast(
            PasswordRecoveryEmail,
            email_delivery.latest(PasswordRecoveryEmail),
        )
        assert (
            await service.validate_password_recovery(
                password_recovery_ref=first_mail.password_recovery_ref,
                secret=first_mail.secret.get_secret_value(),
            )
        ).valid

        await service.request_password_recovery(
            email=_EMAIL,
            source_context="recovery-source-2",
        )
        second_mail = cast(
            PasswordRecoveryEmail,
            email_delivery.latest(PasswordRecoveryEmail),
        )
        assert second_mail.password_recovery_ref != first_mail.password_recovery_ref
        assert not (
            await service.validate_password_recovery(
                password_recovery_ref=first_mail.password_recovery_ref,
                secret=first_mail.secret.get_secret_value(),
            )
        ).valid
        assert (
            await service.validate_password_recovery(
                password_recovery_ref=second_mail.password_recovery_ref,
                secret=second_mail.secret.get_secret_value(),
            )
        ).valid

        await service.reset_password(
            password_recovery_ref=second_mail.password_recovery_ref,
            secret=second_mail.secret.get_secret_value(),
            new_password=_NEW_PASSWORD,
        )

        with pytest.raises(RecoveryInvalidOrExpiredError):
            await service.reset_password(
                password_recovery_ref=second_mail.password_recovery_ref,
                secret=second_mail.secret.get_secret_value(),
                new_password=_NEW_PASSWORD,
            )

        assert _count(migrated_database, "SELECT count(*) FROM dante.password_recovery_challenge") == 0
        assert _count(
            migrated_database,
            "SELECT count(*) FROM dante.auth_session WHERE revoked_at IS NULL",
        ) == 0
        assert _count(
            migrated_database,
            "SELECT count(*) FROM dante.auth_session WHERE revocation_reason_code = 'password_reset'",
        ) == 1
        assert isinstance(
            email_delivery.latest(PasswordResetNotificationEmail),
            PasswordResetNotificationEmail,
        )

        with _admin(migrated_database) as connection:
            credential = connection.execute(
                "SELECT verifier, pepper_key_id FROM dante.password_credential "
                "WHERE account_ref = %s",
                (issued.principal.account_ref,),
            ).fetchone()
        assert credential is not None
        verification = await password_kdf.verify(
            normalized_password=normalize_password_for_authentication(_NEW_PASSWORD),
            verifier=str(credential[0]),
            pepper_key_id=str(credential[1]),
        )
        assert verification.valid


@pytest.mark.asyncio
async def test_reauthentication_rotates_exact_presented_bearer_on_same_session(
    migrated_database: Any,
) -> None:
    async with _lifecycle(migrated_database) as (service, email_delivery, _kdf, _runtime):
        issued = await _establish_account(service, email_delivery)
        admitted = AdmittedSession(
            principal=issued.principal,
            expires_at=issued.expires_at,
            csrf_token=issued.csrf_token,
        )
        old_secret = issued.session_secret.get_secret_value()
        old_verifier = session_secret_verifier(issued.session_secret)

        rotated = await service.reauthenticate(
            admitted=admitted,
            presented_session_verifier=old_verifier,
            password=_PASSWORD,
            source_context="reauth-source",
            request_id="integration-request",
        )

        assert rotated.principal.auth_session_ref == issued.principal.auth_session_ref
        assert rotated.principal.account_ref == issued.principal.account_ref
        assert rotated.session_secret.get_secret_value() != old_secret
        assert rotated.principal.recent_auth_at >= issued.principal.recent_auth_at

        with pytest.raises(InvalidCredentialsError):
            await service.reauthenticate(
                admitted=admitted,
                presented_session_verifier=old_verifier,
                password=_PASSWORD,
                source_context="stale-reauth-source",
                request_id="stale-integration-request",
            )

        with _admin(migrated_database) as connection:
            row = connection.execute(
                "SELECT secret_verifier, auth_session_ref FROM dante.auth_session"
            ).fetchone()
        assert row is not None
        assert bytes(row[0]) == session_secret_verifier(rotated.session_secret)
        assert row[1] == issued.principal.auth_session_ref
