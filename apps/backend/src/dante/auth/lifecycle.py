"""M4 signup, verification, recovery, reset and reauthentication application service."""

from __future__ import annotations

import asyncio
import hmac
import logging
import math
import time
from collections import OrderedDict
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import cast
from uuid import UUID, uuid7

from pydantic import SecretStr
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthInputError,
    AuthIntegrityError,
    AuthServiceUnavailableError,
    EmailDeliveryUnavailableError,
    ExistingAccountSignupResult,
    InvalidCredentialsError,
    IssuedSession,
    LifecycleRateLimitedError,
    PasswordCompromisedError,
    Principal,
    ReauthenticationRequiredError,
    RecoveryInvalidOrExpiredError,
    RecoveryValidation,
    SignupCreated,
    SignupResendCooldownError,
    VerificationAttemptsExhaustedError,
    VerificationInvalidOrExpiredError,
)
from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email
from dante.auth.email_contracts import EmailIntentConflictError
from dante.auth.email_delivery import (
    EmailCommand,
    EmailDeliveryPort,
    EmailDispatchCapacityError,
    NoopEmail,
    PasswordRecoveryEmail,
    PasswordResetNotificationEmail,
    SignupVerificationEmail,
)
from dante.auth.email_outbox import DurableEmailOutbox
from dante.auth.passwords import (
    BreachCheckUnavailableError,
    HibpPasswordChecker,
    PasswordInputError,
    PasswordKdf,
    normalize_password_for_authentication,
    validate_new_password,
)
from dante.auth.proofs import (
    SignupOtpCodec,
    issue_recovery_proof,
    recovery_secret_matches,
    recovery_secret_verifier,
)
from dante.auth.sessions import (
    derive_csrf_token,
    generate_session_secret,
    session_secret_verifier,
)
from dante.platform.config.auth import AuthSettings
from dante.platform.database.mappings.auth import (
    AccountRow,
    AuthSessionRow,
    EmailIdentityRow,
    PasswordCredentialRow,
    PasswordRecoveryChallengeRow,
    PasswordSignupChallengeRow,
)

_LOGGER = logging.getLogger(__name__)
_EMAIL_UNIQUENESS_CONSTRAINT = "uq_email_identity_comparison_key"
_SIGNUP_OTP_MAX_ATTEMPTS = 5
_EXPIRED_CLEANUP_BATCH = 128


@dataclass(slots=True)
class _TokenBucket:
    tokens: float
    updated_at: float


class KeyedRateLimiter:
    """Bounded-memory process-local token bucket for one M4 ingress dimension."""

    def __init__(self, *, capacity: int, window_seconds: float, max_keys: int) -> None:
        self._capacity = float(capacity)
        self._refill_rate = float(capacity) / window_seconds
        self._max_keys = max_keys
        self._buckets: OrderedDict[bytes, _TokenBucket] = OrderedDict()
        self._lock = asyncio.Lock()

    async def consume(self, value: str, *, code: str) -> None:
        """Consume one token using only a one-way in-memory key representation."""
        key = sha256(value.encode("utf-8")).digest()
        now = time.monotonic()

        async with self._lock:
            bucket = self._buckets.pop(key, None)
            if bucket is None:
                if len(self._buckets) >= self._max_keys:
                    self._buckets.popitem(last=False)
                bucket = _TokenBucket(tokens=self._capacity, updated_at=now)

            elapsed = max(0.0, now - bucket.updated_at)
            bucket.tokens = min(
                self._capacity,
                bucket.tokens + elapsed * self._refill_rate,
            )
            bucket.updated_at = now

            if bucket.tokens < 1.0:
                self._buckets[key] = bucket
                wait_seconds = (1.0 - bucket.tokens) / self._refill_rate
                raise LifecycleRateLimitedError(
                    code=code,
                    retry_after_seconds=max(1, math.ceil(wait_seconds)),
                )

            bucket.tokens -= 1.0
            self._buckets[key] = bucket


@dataclass(frozen=True, slots=True)
class _EligibleRecoveryIdentity:
    account_ref: UUID
    email_identity_ref: UUID
    email_address: str
    email_comparison_key: str
    password_credential_ref: UUID
    verifier: str
    pepper_key_id: str
    credential_updated_at: datetime


@dataclass(frozen=True, slots=True)
class _RecoverySnapshot:
    password_recovery_ref: UUID
    account_ref: UUID
    email_identity_ref: UUID
    email_address: str
    secret_verifier: bytes
    issued_at: datetime
    expires_at: datetime
    account_status_code: str
    password_credential_ref: UUID
    verifier: str
    pepper_key_id: str
    credential_updated_at: datetime


@dataclass(frozen=True, slots=True)
class _CredentialSnapshot:
    account_ref: UUID
    account_status_code: str
    password_credential_ref: UUID
    verifier: str
    pepper_key_id: str
    credential_updated_at: datetime


@dataclass(frozen=True, slots=True)
class LifecycleLimiters:
    signup_email: KeyedRateLimiter
    signup_source: KeyedRateLimiter
    recovery_email: KeyedRateLimiter
    recovery_source: KeyedRateLimiter
    reauth: KeyedRateLimiter


class AuthLifecycleService:
    """M4 security lifecycle over the canonical M3 Account/AuthSession spine."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings,
        password_kdf: PasswordKdf,
        breach_checker: HibpPasswordChecker,
        otp_codec: SignupOtpCodec,
        email_delivery: EmailDeliveryPort,
        limiters: LifecycleLimiters,
        email_outbox: DurableEmailOutbox | None = None,
        email_wake: Callable[[], None] | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._password_kdf = password_kdf
        self._breach_checker = breach_checker
        self._otp_codec = otp_codec
        self._email_delivery = email_delivery
        self._email_outbox = email_outbox
        self._email_wake = email_wake
        self._limiters = limiters
        self._csrf_key = settings.csrf_key_bytes

    @property
    def session_cookie_max_age_seconds(self) -> int:
        """Return browser cookie lifetime for newly established/rotated sessions."""
        return self._settings.session_max_age_seconds

    async def create_signup(
        self,
        *,
        email: str,
        password: str,
        source_context: str,
    ) -> SignupCreated:
        """Create isolated pending signup proof state without creating an Account."""
        normalized_email = self._normalize_email(email)
        normalized_password = self._normalize_new_password(password, pointer="/password")
        await self._limiters.signup_email.consume(
            normalized_email.comparison_key,
            code="auth.signup_rate_limited",
        )
        await self._limiters.signup_source.consume(
            source_context,
            code="auth.signup_rate_limited",
        )
        await self._require_uncompromised_new_password(normalized_password)
        password_verifier, pepper_key_id = await self._password_kdf.hash_normalized_password(
            normalized_password
        )

        signup_ref = uuid7()
        otp = self._otp_codec.issue(signup_ref)
        now = datetime.now(UTC)
        signup_expires_at = now + timedelta(seconds=self._settings.signup_lifetime_seconds)
        verification_expires_at = min(
            signup_expires_at,
            now + timedelta(seconds=self._settings.signup_otp_lifetime_seconds),
        )
        row = PasswordSignupChallengeRow(
            signup_ref=signup_ref,
            email_address=normalized_email.address,
            email_comparison_key=normalized_email.comparison_key,
            password_verifier=password_verifier,
            password_pepper_key_id=pepper_key_id,
            otp_verifier=otp.verifier,
            otp_key_id=otp.key_id,
            created_at=now,
            updated_at=now,
            signup_expires_at=signup_expires_at,
            verification_issued_at=now,
            verification_expires_at=verification_expires_at,
            failed_verification_attempts=0,
        )

        email_command = SignupVerificationEmail(
            to_address=normalized_email.address,
            code=otp.code,
            expires_minutes=max(1, math.ceil(self._settings.signup_otp_lifetime_seconds / 60)),
        )
        staged = await self._insert_signup_challenge(row, email_command=email_command)
        await self._after_email_commit(email_command, staged=staged)
        return SignupCreated(
            signup_ref=signup_ref,
            signup_expires_at=signup_expires_at,
            verification_expires_at=verification_expires_at,
        )

    async def resend_signup_verification(
        self,
        *,
        signup_ref: UUID,
        source_context: str,
    ) -> SignupCreated:
        """Rotate only the OTP owned by one pending signup challenge."""
        snapshot = await self._read_signup_challenge(signup_ref)
        if snapshot is None:
            raise VerificationInvalidOrExpiredError()

        await self._limiters.signup_email.consume(
            snapshot.email_comparison_key,
            code="auth.signup_rate_limited",
        )
        await self._limiters.signup_source.consume(
            source_context,
            code="auth.signup_rate_limited",
        )

        otp = self._otp_codec.issue(signup_ref)
        now = datetime.now(UTC)
        if snapshot.signup_expires_at <= now:
            await self._delete_signup_ref(signup_ref)
            raise VerificationInvalidOrExpiredError()

        cooldown_until = snapshot.verification_issued_at + timedelta(
            seconds=self._settings.signup_resend_cooldown_seconds
        )
        if cooldown_until > now:
            raise SignupResendCooldownError(
                max(1, math.ceil((cooldown_until - now).total_seconds()))
            )

        verification_expires_at = min(
            snapshot.signup_expires_at,
            now + timedelta(seconds=self._settings.signup_otp_lifetime_seconds),
        )
        email_command = SignupVerificationEmail(
            to_address=snapshot.email_address,
            code=otp.code,
            expires_minutes=max(1, math.ceil(self._settings.signup_otp_lifetime_seconds / 60)),
        )
        staged = False
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                locked = await database_session.scalar(
                    select(PasswordSignupChallengeRow)
                    .where(PasswordSignupChallengeRow.signup_ref == signup_ref)
                    .with_for_update()
                )
                if locked is None or locked.signup_expires_at <= now:
                    raise VerificationInvalidOrExpiredError()

                cooldown_until = locked.verification_issued_at + timedelta(
                    seconds=self._settings.signup_resend_cooldown_seconds
                )
                if cooldown_until > now:
                    raise SignupResendCooldownError(
                        max(1, math.ceil((cooldown_until - now).total_seconds()))
                    )

                locked.otp_verifier = otp.verifier
                locked.otp_key_id = otp.key_id
                locked.updated_at = now
                locked.verification_issued_at = now
                locked.verification_expires_at = verification_expires_at
                locked.failed_verification_attempts = 0
                staged = await self._stage_email_intent(
                    database_session,
                    command=email_command,
                    operation_scope="auth.signup_verification",
                    idempotency_key=f"{signup_ref}:{now.isoformat()}",
                    expires_at=verification_expires_at,
                    supersession_key=f"signup:{signup_ref}",
                )
        except VerificationInvalidOrExpiredError, SignupResendCooldownError:
            raise
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

        await self._after_email_commit(email_command, staged=staged)
        return SignupCreated(
            signup_ref=signup_ref,
            signup_expires_at=snapshot.signup_expires_at,
            verification_expires_at=verification_expires_at,
        )

    async def verify_signup(
        self,
        *,
        signup_ref: UUID,
        code: str,
    ) -> IssuedSession | ExistingAccountSignupResult:
        """Consume one OTP and establish canonical Account state or a safe collision outcome."""
        now = datetime.now(UTC)
        auth_session_ref = uuid7()
        account_ref = uuid7()
        email_identity_ref = uuid7()
        password_credential_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        comparison_key: str | None = None
        email_address: str | None = None
        password_verifier: str | None = None
        password_pepper_key_id: str | None = None
        ambiguous_commit = False

        database_session = self._session_factory()
        try:
            await database_session.begin()
            challenge = await database_session.scalar(
                select(PasswordSignupChallengeRow)
                .where(PasswordSignupChallengeRow.signup_ref == signup_ref)
                .with_for_update()
            )
            if challenge is None or challenge.signup_expires_at <= now:
                await database_session.rollback()
                raise VerificationInvalidOrExpiredError()
            if challenge.failed_verification_attempts >= _SIGNUP_OTP_MAX_ATTEMPTS:
                await database_session.rollback()
                raise VerificationAttemptsExhaustedError()
            if challenge.verification_expires_at <= now:
                await database_session.rollback()
                raise VerificationInvalidOrExpiredError()

            if not self._otp_codec.matches(
                signup_ref=signup_ref,
                submitted_code=code,
                expected_verifier=challenge.otp_verifier,
                key_id=challenge.otp_key_id,
            ):
                challenge.failed_verification_attempts += 1
                challenge.updated_at = now
                exhausted = challenge.failed_verification_attempts >= _SIGNUP_OTP_MAX_ATTEMPTS
                try:
                    await database_session.commit()
                except SQLAlchemyError as exc:
                    raise AuthServiceUnavailableError(retryable=True) from exc
                if exhausted:
                    raise VerificationAttemptsExhaustedError()
                raise VerificationInvalidOrExpiredError()

            comparison_key = challenge.email_comparison_key
            email_address = challenge.email_address
            password_verifier = challenge.password_verifier
            password_pepper_key_id = challenge.password_pepper_key_id
            existing = await database_session.scalar(
                select(EmailIdentityRow.email_identity_ref).where(
                    EmailIdentityRow.comparison_key == comparison_key
                )
            )
            if existing is not None:
                await database_session.execute(
                    delete(PasswordSignupChallengeRow).where(
                        PasswordSignupChallengeRow.email_comparison_key == comparison_key
                    )
                )
                await database_session.commit()
                return ExistingAccountSignupResult()

            database_session.add_all(
                [
                    AccountRow(
                        account_ref=account_ref,
                        status_code="active",
                        created_at=now,
                        disabled_at=None,
                    ),
                    EmailIdentityRow(
                        email_identity_ref=email_identity_ref,
                        account_ref=account_ref,
                        address=email_address,
                        comparison_key=comparison_key,
                        created_at=now,
                        verified_at=now,
                    ),
                    PasswordCredentialRow(
                        password_credential_ref=password_credential_ref,
                        account_ref=account_ref,
                        verifier=password_verifier,
                        pepper_key_id=password_pepper_key_id,
                        created_at=now,
                        updated_at=now,
                    ),
                    AuthSessionRow(
                        auth_session_ref=auth_session_ref,
                        account_ref=account_ref,
                        secret_verifier=secret_verifier,
                        created_at=now,
                        authenticated_at=now,
                        recent_auth_at=now,
                        last_user_activity_at=now,
                        expires_at=expires_at,
                        revoked_at=None,
                        revocation_reason_code=None,
                    ),
                ]
            )
            await database_session.flush()
            await database_session.execute(
                delete(PasswordSignupChallengeRow).where(
                    PasswordSignupChallengeRow.email_comparison_key == comparison_key
                )
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except VerificationAttemptsExhaustedError, VerificationInvalidOrExpiredError:
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if comparison_key is not None and self._is_email_uniqueness_conflict(exc):
                await self._resolve_signup_collision(comparison_key)
                return ExistingAccountSignupResult()
            raise AuthServiceUnavailableError(retryable=False) from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if (
            comparison_key is None
            or email_address is None
            or password_verifier is None
            or password_pepper_key_id is None
        ):
            raise AuthIntegrityError("signup verification completed without frozen challenge state")
        if ambiguous_commit:
            return await self._reconcile_signup_commit(
                signup_ref=signup_ref,
                comparison_key=comparison_key,
                email_address=email_address,
                password_verifier=password_verifier,
                password_pepper_key_id=password_pepper_key_id,
                account_ref=account_ref,
                email_identity_ref=email_identity_ref,
                password_credential_ref=password_credential_ref,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
                created_at=now,
                expires_at=expires_at,
                session_secret=session_secret,
            )

        return self._issued_session(
            account_ref=account_ref,
            auth_session_ref=auth_session_ref,
            authenticated_at=now,
            recent_auth_at=now,
            expires_at=expires_at,
            secret_verifier=secret_verifier,
            session_secret=session_secret,
        )

    async def request_password_recovery(
        self,
        *,
        email: str,
        source_context: str,
    ) -> None:
        """Issue a neutral, single-current recovery proof for eligible password Accounts."""
        started_at = time.monotonic()
        normalized_email = self._normalize_email(email)
        await self._limiters.recovery_email.consume(
            normalized_email.comparison_key,
            code="auth.recovery_rate_limited",
        )
        await self._limiters.recovery_source.consume(
            source_context,
            code="auth.recovery_rate_limited",
        )

        snapshot = await self._read_eligible_recovery_identity(normalized_email.comparison_key)
        if snapshot is None:
            await self._enqueue(NoopEmail())
            await self._pad_recovery_success(started_at)
            return

        recovery_ref = uuid7()
        proof = issue_recovery_proof()
        email_command = PasswordRecoveryEmail(
            to_address=snapshot.email_address,
            password_recovery_ref=recovery_ref,
            secret=proof.secret,
        )
        committed, staged = await self._persist_recovery_challenge(
            snapshot=snapshot,
            password_recovery_ref=recovery_ref,
            secret_verifier=proof.verifier,
            email_command=email_command,
        )
        if not committed:
            await self._enqueue(NoopEmail())
            await self._pad_recovery_success(started_at)
            return

        await self._after_email_commit(email_command, staged=staged)
        await self._pad_recovery_success(started_at)

    async def validate_password_recovery(
        self,
        *,
        password_recovery_ref: UUID,
        secret: str,
    ) -> RecoveryValidation:
        """Validate high-entropy recovery proof without consuming it."""
        verifier = recovery_secret_verifier(secret)
        if verifier is None:
            return RecoveryValidation(valid=False)

        now = datetime.now(UTC)
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = (
                    await database_session.execute(
                        select(
                            PasswordRecoveryChallengeRow,
                            AccountRow,
                            EmailIdentityRow,
                            PasswordCredentialRow,
                        )
                        .join(
                            AccountRow,
                            AccountRow.account_ref == PasswordRecoveryChallengeRow.account_ref,
                        )
                        .join(
                            EmailIdentityRow,
                            (
                                EmailIdentityRow.email_identity_ref
                                == PasswordRecoveryChallengeRow.email_identity_ref
                            )
                            & (
                                EmailIdentityRow.account_ref
                                == PasswordRecoveryChallengeRow.account_ref
                            ),
                        )
                        .join(
                            PasswordCredentialRow,
                            PasswordCredentialRow.account_ref
                            == PasswordRecoveryChallengeRow.account_ref,
                        )
                        .where(
                            PasswordRecoveryChallengeRow.password_recovery_ref
                            == password_recovery_ref
                        )
                    )
                ).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

        if row is None:
            return RecoveryValidation(valid=False)
        challenge, account, email_identity, _credential = row
        return RecoveryValidation(
            valid=(
                account.status_code == "active"
                and email_identity.verified_at is not None
                and challenge.expires_at > now
                and hmac.compare_digest(verifier, challenge.secret_verifier)
            )
        )

    async def reset_password(
        self,
        *,
        password_recovery_ref: UUID,
        secret: str,
        new_password: str,
    ) -> None:
        """Consume recovery proof, replace password and revoke every prior AuthSession."""
        snapshot = await self._read_recovery_snapshot(password_recovery_ref)
        preflight_now = datetime.now(UTC)
        if (
            snapshot is None
            or snapshot.account_status_code != "active"
            or snapshot.expires_at <= preflight_now
            or not recovery_secret_matches(secret, snapshot.secret_verifier)
        ):
            raise RecoveryInvalidOrExpiredError()

        normalized_password = self._normalize_new_password(
            new_password,
            pointer="/new_password",
        )
        await self._require_uncompromised_new_password(normalized_password)
        new_verifier, new_pepper_key_id = await self._password_kdf.hash_normalized_password(
            normalized_password
        )

        ambiguous_commit = False
        mutation_at: datetime | None = None
        notification = PasswordResetNotificationEmail(to_address=snapshot.email_address)
        notification_staged = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(snapshot.account_ref))
            )
            mutation_at = datetime.now(UTC)
            account = await database_session.scalar(
                select(AccountRow).where(AccountRow.account_ref == snapshot.account_ref)
            )
            credential = await database_session.scalar(
                select(PasswordCredentialRow).where(
                    PasswordCredentialRow.account_ref == snapshot.account_ref
                )
            )
            email_identity = await database_session.scalar(
                select(EmailIdentityRow).where(
                    EmailIdentityRow.email_identity_ref == snapshot.email_identity_ref,
                    EmailIdentityRow.account_ref == snapshot.account_ref,
                )
            )
            if (
                account is None
                or account.status_code != "active"
                or credential is None
                or email_identity is None
                or email_identity.verified_at is None
                or credential.password_credential_ref != snapshot.password_credential_ref
                or credential.verifier != snapshot.verifier
                or credential.pepper_key_id != snapshot.pepper_key_id
                or credential.updated_at != snapshot.credential_updated_at
            ):
                await database_session.rollback()
                raise RecoveryInvalidOrExpiredError()

            consumed = await database_session.scalar(
                delete(PasswordRecoveryChallengeRow)
                .where(
                    PasswordRecoveryChallengeRow.password_recovery_ref == password_recovery_ref,
                    PasswordRecoveryChallengeRow.account_ref == snapshot.account_ref,
                    PasswordRecoveryChallengeRow.email_identity_ref == snapshot.email_identity_ref,
                    PasswordRecoveryChallengeRow.secret_verifier == snapshot.secret_verifier,
                    PasswordRecoveryChallengeRow.expires_at > mutation_at,
                )
                .returning(PasswordRecoveryChallengeRow.password_recovery_ref)
            )
            if consumed is None:
                await database_session.rollback()
                raise RecoveryInvalidOrExpiredError()

            credential.verifier = new_verifier
            credential.pepper_key_id = new_pepper_key_id
            credential.updated_at = mutation_at
            await database_session.execute(
                update(AuthSessionRow)
                .where(
                    AuthSessionRow.account_ref == snapshot.account_ref,
                    AuthSessionRow.revoked_at.is_(None),
                )
                .values(
                    revoked_at=mutation_at,
                    revocation_reason_code="password_reset",
                )
            )
            notification_staged = await self._stage_email_intent(
                database_session,
                command=notification,
                operation_scope="auth.password_reset_notification",
                idempotency_key=str(password_recovery_ref),
                expires_at=mutation_at + timedelta(days=1),
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except RecoveryInvalidOrExpiredError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if mutation_at is None:
            raise AuthIntegrityError("password reset completed without mutation timestamp")
        if ambiguous_commit:
            await self._reconcile_reset_commit(
                snapshot=snapshot,
                new_verifier=new_verifier,
                new_pepper_key_id=new_pepper_key_id,
                mutation_at=mutation_at,
            )

        await self._after_email_commit(notification, staged=notification_staged)

    async def reauthenticate(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_verifier: bytes,
        password: str,
        source_context: str,
        request_id: str,
    ) -> IssuedSession:
        """Refresh recent auth on the same session while rotating its exact presented bearer."""
        await self._limiters.reauth.consume(
            f"{admitted.principal.auth_session_ref}:{source_context}",
            code="auth.reauthentication_rate_limited",
        )
        normalized_password = self._normalize_auth_password(password)
        snapshot = await self._read_account_credential(admitted.principal.account_ref)
        if snapshot is None:
            await self._password_kdf.verify_dummy(normalized_password)
            raise InvalidCredentialsError()
        if snapshot.account_status_code != "active":
            raise AccountUnavailableError()

        verification = await self._password_kdf.verify(
            normalized_password=normalized_password,
            verifier=snapshot.verifier,
            pepper_key_id=snapshot.pepper_key_id,
        )
        if not verification.valid:
            raise InvalidCredentialsError()

        try:
            breached = await self._breach_checker.is_breached(normalized_password)
        except BreachCheckUnavailableError:
            _LOGGER.warning("auth.hibp_unavailable request_id=%s", request_id)
            breached = False
        if breached:
            raise PasswordCompromisedError()

        replacement_verifier: tuple[str, str] | None = None
        if verification.needs_rehash:
            replacement_verifier = await self._password_kdf.hash_normalized_password(
                normalized_password
            )

        new_session_secret = generate_session_secret()
        new_secret_verifier = session_secret_verifier(new_session_secret)
        ambiguous_commit = False
        mutation_at: datetime | None = None
        authenticated_at: datetime | None = None
        old_recent_auth_at: datetime | None = None
        old_last_user_activity_at: datetime | None = None
        old_expires_at: datetime | None = None
        expires_at: datetime | None = None

        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(snapshot.account_ref))
            )
            mutation_at = datetime.now(UTC)
            expires_at = mutation_at + timedelta(seconds=self._settings.session_max_age_seconds)

            account = await database_session.scalar(
                select(AccountRow).where(AccountRow.account_ref == snapshot.account_ref)
            )
            credential = await database_session.scalar(
                select(PasswordCredentialRow).where(
                    PasswordCredentialRow.account_ref == snapshot.account_ref
                )
            )
            auth_session = await database_session.scalar(
                select(AuthSessionRow).where(
                    AuthSessionRow.auth_session_ref == admitted.principal.auth_session_ref,
                    AuthSessionRow.account_ref == snapshot.account_ref,
                    AuthSessionRow.secret_verifier == presented_session_verifier,
                    AuthSessionRow.revoked_at.is_(None),
                )
            )
            if auth_session is None:
                await database_session.rollback()
                raise InvalidCredentialsError()

            idle_deadline = auth_session.last_user_activity_at + timedelta(
                seconds=self._settings.session_idle_timeout_seconds
            )
            if (
                account is None
                or account.status_code != "active"
                or credential is None
                or auth_session.expires_at <= mutation_at
                or idle_deadline <= mutation_at
                or credential.password_credential_ref != snapshot.password_credential_ref
                or credential.verifier != snapshot.verifier
                or credential.pepper_key_id != snapshot.pepper_key_id
                or credential.updated_at != snapshot.credential_updated_at
            ):
                await database_session.rollback()
                raise InvalidCredentialsError()

            authenticated_at = auth_session.authenticated_at
            old_recent_auth_at = auth_session.recent_auth_at
            old_last_user_activity_at = auth_session.last_user_activity_at
            old_expires_at = auth_session.expires_at

            if replacement_verifier is not None:
                credential.verifier = replacement_verifier[0]
                credential.pepper_key_id = replacement_verifier[1]
                credential.updated_at = mutation_at

            rotated = await database_session.scalar(
                update(AuthSessionRow)
                .where(
                    AuthSessionRow.auth_session_ref == admitted.principal.auth_session_ref,
                    AuthSessionRow.account_ref == snapshot.account_ref,
                    AuthSessionRow.secret_verifier == presented_session_verifier,
                    AuthSessionRow.revoked_at.is_(None),
                    AuthSessionRow.expires_at > mutation_at,
                    AuthSessionRow.last_user_activity_at
                    > mutation_at - timedelta(seconds=self._settings.session_idle_timeout_seconds),
                )
                .values(
                    secret_verifier=new_secret_verifier,
                    recent_auth_at=mutation_at,
                    last_user_activity_at=mutation_at,
                    expires_at=expires_at,
                )
                .returning(AuthSessionRow.authenticated_at)
            )
            if rotated is None:
                await database_session.rollback()
                raise InvalidCredentialsError()

            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except InvalidCredentialsError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if (
            mutation_at is None
            or authenticated_at is None
            or old_recent_auth_at is None
            or old_last_user_activity_at is None
            or old_expires_at is None
            or expires_at is None
        ):
            raise AuthIntegrityError("reauthentication completed without frozen session state")
        if ambiguous_commit:
            return await self._reconcile_reauth_commit(
                account_ref=snapshot.account_ref,
                auth_session_ref=admitted.principal.auth_session_ref,
                authenticated_at=authenticated_at,
                old_secret_verifier=presented_session_verifier,
                old_recent_auth_at=old_recent_auth_at,
                old_last_user_activity_at=old_last_user_activity_at,
                old_expires_at=old_expires_at,
                recent_auth_at=mutation_at,
                expires_at=expires_at,
                new_secret_verifier=new_secret_verifier,
                new_session_secret=new_session_secret,
            )

        return self._issued_session(
            account_ref=snapshot.account_ref,
            auth_session_ref=admitted.principal.auth_session_ref,
            authenticated_at=authenticated_at,
            recent_auth_at=mutation_at,
            expires_at=expires_at,
            secret_verifier=new_secret_verifier,
            session_secret=new_session_secret,
        )

    def require_recent_auth(self, admitted: AdmittedSession) -> None:
        """Enforce server-authoritative recent-auth freshness for sensitive operations."""
        deadline = admitted.principal.recent_auth_at + timedelta(
            seconds=self._settings.recent_auth_window_seconds
        )
        if deadline <= datetime.now(UTC):
            raise ReauthenticationRequiredError()

    async def _stage_email_intent(
        self,
        database_session: AsyncSession,
        *,
        command: EmailCommand,
        operation_scope: str,
        idempotency_key: str,
        expires_at: datetime,
        supersession_key: str | None = None,
    ) -> bool:
        if self._email_outbox is None or isinstance(command, NoopEmail):
            return False
        try:
            await self._email_outbox.stage(
                database_session,
                command=command,
                operation_scope=operation_scope,
                idempotency_key=idempotency_key,
                expires_at=expires_at,
                supersession_key=supersession_key,
            )
        except EmailIntentConflictError as exc:
            raise AuthIntegrityError("email intent idempotency conflict") from exc
        return True

    async def _after_email_commit(self, command: EmailCommand, *, staged: bool) -> None:
        if staged:
            if self._email_wake is not None:
                self._email_wake()
            return
        if self._email_outbox is not None and isinstance(command, NoopEmail):
            return
        await self._enqueue(command)

    async def _insert_signup_challenge(
        self,
        row: PasswordSignupChallengeRow,
        *,
        email_command: SignupVerificationEmail,
    ) -> bool:
        await self._cleanup_expired_challenges(datetime.now(UTC))
        ambiguous_commit = False
        staged = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            database_session.add(row)
            staged = await self._stage_email_intent(
                database_session,
                command=email_command,
                operation_scope="auth.signup_verification",
                idempotency_key=f"{row.signup_ref}:{row.verification_issued_at.isoformat()}",
                expires_at=row.verification_expires_at,
                supersession_key=f"signup:{row.signup_ref}",
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if not ambiguous_commit:
            return staged

        persisted = await self._read_signup_challenge(row.signup_ref)
        if persisted is None:
            raise AuthServiceUnavailableError(retryable=True)
        if (
            persisted.email_address != row.email_address
            or persisted.email_comparison_key != row.email_comparison_key
            or persisted.password_verifier != row.password_verifier
            or persisted.password_pepper_key_id != row.password_pepper_key_id
            or not hmac.compare_digest(persisted.otp_verifier, row.otp_verifier)
            or persisted.otp_key_id != row.otp_key_id
            or persisted.created_at != row.created_at
            or persisted.updated_at != row.updated_at
            or persisted.signup_expires_at != row.signup_expires_at
            or persisted.verification_issued_at != row.verification_issued_at
            or persisted.verification_expires_at != row.verification_expires_at
            or persisted.failed_verification_attempts != row.failed_verification_attempts
        ):
            raise AuthIntegrityError("ambiguous signup challenge reconciliation mismatched state")
        return staged

    async def _persist_recovery_challenge(
        self,
        *,
        snapshot: _EligibleRecoveryIdentity,
        password_recovery_ref: UUID,
        secret_verifier: bytes,
        email_command: PasswordRecoveryEmail,
    ) -> tuple[bool, bool]:
        await self._cleanup_expired_challenges(datetime.now(UTC))
        ambiguous_commit = False
        issued_at: datetime | None = None
        expires_at: datetime | None = None
        staged = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(snapshot.account_ref))
            )
            current = await self._read_exact_eligible_recovery_identity_in_session(
                database_session,
                snapshot,
            )
            if current is None:
                await database_session.rollback()
                return False, False

            issued_at = datetime.now(UTC)
            expires_at = issued_at + timedelta(seconds=self._settings.recovery_lifetime_seconds)
            await database_session.execute(
                delete(PasswordRecoveryChallengeRow).where(
                    PasswordRecoveryChallengeRow.account_ref == snapshot.account_ref
                )
            )
            database_session.add(
                PasswordRecoveryChallengeRow(
                    password_recovery_ref=password_recovery_ref,
                    account_ref=snapshot.account_ref,
                    email_identity_ref=snapshot.email_identity_ref,
                    secret_verifier=secret_verifier,
                    issued_at=issued_at,
                    expires_at=expires_at,
                )
            )
            staged = await self._stage_email_intent(
                database_session,
                command=email_command,
                operation_scope="auth.password_recovery",
                idempotency_key=str(password_recovery_ref),
                expires_at=expires_at,
                supersession_key=f"password-recovery:{snapshot.account_ref}",
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if issued_at is None or expires_at is None:
            raise AuthIntegrityError("recovery issuance completed without challenge timestamps")
        if not ambiguous_commit:
            return True, staged

        try:
            async with (
                self._session_factory() as reconciliation_session,
                reconciliation_session.begin(),
            ):
                persisted = await reconciliation_session.scalar(
                    select(PasswordRecoveryChallengeRow).where(
                        PasswordRecoveryChallengeRow.password_recovery_ref == password_recovery_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

        if persisted is None:
            raise AuthServiceUnavailableError(retryable=True)
        if (
            persisted.account_ref != snapshot.account_ref
            or persisted.email_identity_ref != snapshot.email_identity_ref
            or not hmac.compare_digest(persisted.secret_verifier, secret_verifier)
            or persisted.issued_at != issued_at
            or persisted.expires_at != expires_at
        ):
            raise AuthIntegrityError("ambiguous recovery issuance reconciliation mismatched state")
        return True, staged

    async def _resolve_signup_collision(self, comparison_key: str) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                existing = await database_session.scalar(
                    select(EmailIdentityRow.email_identity_ref).where(
                        EmailIdentityRow.comparison_key == comparison_key
                    )
                )
                if existing is None:
                    raise AuthServiceUnavailableError(retryable=True)
                await database_session.execute(
                    delete(PasswordSignupChallengeRow).where(
                        PasswordSignupChallengeRow.email_comparison_key == comparison_key
                    )
                )
        except AuthServiceUnavailableError:
            raise
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _reconcile_signup_commit(
        self,
        *,
        signup_ref: UUID,
        comparison_key: str,
        email_address: str,
        password_verifier: str,
        password_pepper_key_id: str,
        account_ref: UUID,
        email_identity_ref: UUID,
        password_credential_ref: UUID,
        auth_session_ref: UUID,
        secret_verifier: bytes,
        created_at: datetime,
        expires_at: datetime,
        session_secret: SecretStr,
    ) -> IssuedSession | ExistingAccountSignupResult:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                account = await database_session.scalar(
                    select(AccountRow).where(AccountRow.account_ref == account_ref)
                )
                email_identity = await database_session.scalar(
                    select(EmailIdentityRow).where(
                        EmailIdentityRow.email_identity_ref == email_identity_ref
                    )
                )
                credential = await database_session.scalar(
                    select(PasswordCredentialRow).where(
                        PasswordCredentialRow.password_credential_ref == password_credential_ref
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref
                    )
                )
                sibling_count = await database_session.scalar(
                    select(func.count())
                    .select_from(PasswordSignupChallengeRow)
                    .where(PasswordSignupChallengeRow.email_comparison_key == comparison_key)
                )
                canonical_email = await database_session.scalar(
                    select(EmailIdentityRow).where(
                        EmailIdentityRow.comparison_key == comparison_key
                    )
                )
                original_challenge = await database_session.scalar(
                    select(PasswordSignupChallengeRow.signup_ref).where(
                        PasswordSignupChallengeRow.signup_ref == signup_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

        exact_new_account = (
            account is not None
            and email_identity is not None
            and credential is not None
            and auth_session is not None
            and canonical_email is not None
            and account.account_ref == account_ref
            and account.status_code == "active"
            and account.created_at == created_at
            and account.disabled_at is None
            and email_identity.email_identity_ref == email_identity_ref
            and email_identity.account_ref == account_ref
            and email_identity.address == email_address
            and email_identity.comparison_key == comparison_key
            and email_identity.created_at == created_at
            and email_identity.verified_at == created_at
            and canonical_email.email_identity_ref == email_identity_ref
            and credential.password_credential_ref == password_credential_ref
            and credential.account_ref == account_ref
            and credential.verifier == password_verifier
            and credential.pepper_key_id == password_pepper_key_id
            and credential.created_at == created_at
            and credential.updated_at == created_at
            and auth_session.account_ref == account_ref
            and hmac.compare_digest(auth_session.secret_verifier, secret_verifier)
            and auth_session.created_at == created_at
            and auth_session.authenticated_at == created_at
            and auth_session.recent_auth_at == created_at
            and auth_session.last_user_activity_at == created_at
            and auth_session.expires_at == expires_at
            and auth_session.revoked_at is None
            and auth_session.revocation_reason_code is None
            and original_challenge is None
            and sibling_count == 0
        )
        if exact_new_account:
            return self._issued_session(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=created_at,
                recent_auth_at=created_at,
                expires_at=expires_at,
                secret_verifier=secret_verifier,
                session_secret=session_secret,
            )
        if account is None and canonical_email is not None:
            await self._resolve_signup_collision(comparison_key)
            return ExistingAccountSignupResult()
        if account is None and canonical_email is None and original_challenge is not None:
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous signup verification reconciliation mismatched state")

    async def _reconcile_reset_commit(
        self,
        *,
        snapshot: _RecoverySnapshot,
        new_verifier: str,
        new_pepper_key_id: str,
        mutation_at: datetime,
    ) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                credential = await database_session.scalar(
                    select(PasswordCredentialRow).where(
                        PasswordCredentialRow.account_ref == snapshot.account_ref
                    )
                )
                challenge = await database_session.scalar(
                    select(PasswordRecoveryChallengeRow.password_recovery_ref).where(
                        PasswordRecoveryChallengeRow.password_recovery_ref
                        == snapshot.password_recovery_ref
                    )
                )
                prior_unrevoked_sessions = await database_session.scalar(
                    select(func.count())
                    .select_from(AuthSessionRow)
                    .where(
                        AuthSessionRow.account_ref == snapshot.account_ref,
                        AuthSessionRow.created_at <= mutation_at,
                        AuthSessionRow.revoked_at.is_(None),
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

        if (
            credential is not None
            and credential.verifier == new_verifier
            and credential.pepper_key_id == new_pepper_key_id
            and credential.updated_at == mutation_at
            and challenge is None
            and prior_unrevoked_sessions == 0
        ):
            return
        if (
            credential is not None
            and credential.verifier == snapshot.verifier
            and credential.pepper_key_id == snapshot.pepper_key_id
            and challenge == snapshot.password_recovery_ref
        ):
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous password reset reconciliation mismatched state")

    async def _reconcile_reauth_commit(
        self,
        *,
        account_ref: UUID,
        auth_session_ref: UUID,
        authenticated_at: datetime,
        old_secret_verifier: bytes,
        old_recent_auth_at: datetime,
        old_last_user_activity_at: datetime,
        old_expires_at: datetime,
        recent_auth_at: datetime,
        expires_at: datetime,
        new_secret_verifier: bytes,
        new_session_secret: SecretStr,
    ) -> IssuedSession:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                persisted = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref,
                        AuthSessionRow.account_ref == account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

        if persisted is None:
            raise InvalidCredentialsError()
        if (
            persisted.revoked_at is None
            and hmac.compare_digest(persisted.secret_verifier, new_secret_verifier)
            and persisted.authenticated_at == authenticated_at
            and persisted.recent_auth_at == recent_auth_at
            and persisted.last_user_activity_at == recent_auth_at
            and persisted.expires_at == expires_at
        ):
            return self._issued_session(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=authenticated_at,
                recent_auth_at=recent_auth_at,
                expires_at=expires_at,
                secret_verifier=new_secret_verifier,
                session_secret=new_session_secret,
            )
        if (
            persisted.revoked_at is None
            and hmac.compare_digest(persisted.secret_verifier, old_secret_verifier)
            and persisted.authenticated_at == authenticated_at
            and persisted.recent_auth_at == old_recent_auth_at
            and persisted.last_user_activity_at == old_last_user_activity_at
            and persisted.expires_at == old_expires_at
        ):
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthServiceUnavailableError(retryable=False)

    async def _read_signup_challenge(
        self,
        signup_ref: UUID,
    ) -> PasswordSignupChallengeRow | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                statement = select(PasswordSignupChallengeRow).where(
                    PasswordSignupChallengeRow.signup_ref == signup_ref
                )
                challenge = await database_session.scalar(statement)
                if challenge is None:
                    return None
                return challenge
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _delete_signup_ref(self, signup_ref: UUID) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                await database_session.execute(
                    delete(PasswordSignupChallengeRow).where(
                        PasswordSignupChallengeRow.signup_ref == signup_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_eligible_recovery_identity(
        self,
        comparison_key: str,
    ) -> _EligibleRecoveryIdentity | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = (
                    await database_session.execute(
                        select(EmailIdentityRow, AccountRow, PasswordCredentialRow)
                        .join(
                            AccountRow,
                            AccountRow.account_ref == EmailIdentityRow.account_ref,
                        )
                        .join(
                            PasswordCredentialRow,
                            PasswordCredentialRow.account_ref == AccountRow.account_ref,
                        )
                        .where(EmailIdentityRow.comparison_key == comparison_key)
                    )
                ).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            return None
        email_identity, account, credential = row
        if email_identity.verified_at is None or account.status_code != "active":
            return None
        return _EligibleRecoveryIdentity(
            account_ref=account.account_ref,
            email_identity_ref=email_identity.email_identity_ref,
            email_address=email_identity.address,
            email_comparison_key=email_identity.comparison_key,
            password_credential_ref=credential.password_credential_ref,
            verifier=credential.verifier,
            pepper_key_id=credential.pepper_key_id,
            credential_updated_at=credential.updated_at,
        )

    async def _read_exact_eligible_recovery_identity_in_session(
        self,
        database_session: AsyncSession,
        expected: _EligibleRecoveryIdentity,
    ) -> _EligibleRecoveryIdentity | None:
        row = (
            await database_session.execute(
                select(EmailIdentityRow, AccountRow, PasswordCredentialRow)
                .join(AccountRow, AccountRow.account_ref == EmailIdentityRow.account_ref)
                .join(
                    PasswordCredentialRow,
                    PasswordCredentialRow.account_ref == AccountRow.account_ref,
                )
                .where(
                    AccountRow.account_ref == expected.account_ref,
                    AccountRow.status_code == "active",
                    EmailIdentityRow.email_identity_ref == expected.email_identity_ref,
                    EmailIdentityRow.comparison_key == expected.email_comparison_key,
                    EmailIdentityRow.verified_at.is_not(None),
                    PasswordCredentialRow.password_credential_ref
                    == expected.password_credential_ref,
                )
            )
        ).one_or_none()
        if row is None:
            return None
        email_identity, account, credential = row
        current = _EligibleRecoveryIdentity(
            account_ref=account.account_ref,
            email_identity_ref=email_identity.email_identity_ref,
            email_address=email_identity.address,
            email_comparison_key=email_identity.comparison_key,
            password_credential_ref=credential.password_credential_ref,
            verifier=credential.verifier,
            pepper_key_id=credential.pepper_key_id,
            credential_updated_at=credential.updated_at,
        )
        return current if current == expected else None

    async def _read_recovery_snapshot(
        self,
        password_recovery_ref: UUID,
    ) -> _RecoverySnapshot | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = (
                    await database_session.execute(
                        select(
                            PasswordRecoveryChallengeRow,
                            AccountRow,
                            PasswordCredentialRow,
                            EmailIdentityRow,
                        )
                        .join(
                            AccountRow,
                            AccountRow.account_ref == PasswordRecoveryChallengeRow.account_ref,
                        )
                        .join(
                            PasswordCredentialRow,
                            PasswordCredentialRow.account_ref
                            == PasswordRecoveryChallengeRow.account_ref,
                        )
                        .join(
                            EmailIdentityRow,
                            (
                                EmailIdentityRow.email_identity_ref
                                == PasswordRecoveryChallengeRow.email_identity_ref
                            )
                            & (
                                EmailIdentityRow.account_ref
                                == PasswordRecoveryChallengeRow.account_ref
                            ),
                        )
                        .where(
                            PasswordRecoveryChallengeRow.password_recovery_ref
                            == password_recovery_ref,
                            EmailIdentityRow.verified_at.is_not(None),
                        )
                    )
                ).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            return None
        challenge, account, credential, email_identity = row
        return _RecoverySnapshot(
            password_recovery_ref=challenge.password_recovery_ref,
            account_ref=challenge.account_ref,
            email_identity_ref=challenge.email_identity_ref,
            email_address=email_identity.address,
            secret_verifier=challenge.secret_verifier,
            issued_at=challenge.issued_at,
            expires_at=challenge.expires_at,
            account_status_code=account.status_code,
            password_credential_ref=credential.password_credential_ref,
            verifier=credential.verifier,
            pepper_key_id=credential.pepper_key_id,
            credential_updated_at=credential.updated_at,
        )

    async def _read_account_credential(self, account_ref: UUID) -> _CredentialSnapshot | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = (
                    await database_session.execute(
                        select(AccountRow, PasswordCredentialRow)
                        .outerjoin(
                            PasswordCredentialRow,
                            PasswordCredentialRow.account_ref == AccountRow.account_ref,
                        )
                        .where(AccountRow.account_ref == account_ref)
                    )
                ).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            return None
        account, credential = row
        credential = cast(PasswordCredentialRow | None, credential)
        if credential is None:
            return None
        return _CredentialSnapshot(
            account_ref=account.account_ref,
            account_status_code=account.status_code,
            password_credential_ref=credential.password_credential_ref,
            verifier=credential.verifier,
            pepper_key_id=credential.pepper_key_id,
            credential_updated_at=credential.updated_at,
        )

    async def _cleanup_expired_challenges(self, now: datetime) -> None:
        """Bound cleanup in its own short transaction, never under an Account security lock."""
        expired_signup_refs = (
            select(PasswordSignupChallengeRow.signup_ref)
            .where(PasswordSignupChallengeRow.signup_expires_at <= now)
            .order_by(PasswordSignupChallengeRow.signup_expires_at)
            .limit(_EXPIRED_CLEANUP_BATCH)
        )
        expired_recovery_refs = (
            select(PasswordRecoveryChallengeRow.password_recovery_ref)
            .where(PasswordRecoveryChallengeRow.expires_at <= now)
            .order_by(PasswordRecoveryChallengeRow.expires_at)
            .limit(_EXPIRED_CLEANUP_BATCH)
        )
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                await database_session.execute(
                    delete(PasswordSignupChallengeRow).where(
                        PasswordSignupChallengeRow.signup_ref.in_(expired_signup_refs)
                    )
                )
                await database_session.execute(
                    delete(PasswordRecoveryChallengeRow).where(
                        PasswordRecoveryChallengeRow.password_recovery_ref.in_(
                            expired_recovery_refs
                        )
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _require_uncompromised_new_password(self, normalized_password: str) -> None:
        try:
            breached = await self._breach_checker.is_breached(normalized_password)
        except BreachCheckUnavailableError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if breached:
            raise PasswordCompromisedError()

    async def _enqueue(self, command: EmailCommand) -> None:
        try:
            await self._email_delivery.enqueue(command)
        except EmailDispatchCapacityError as exc:
            raise EmailDeliveryUnavailableError() from exc

    async def _pad_recovery_success(self, started_at: float) -> None:
        remaining = self._settings.recovery_response_floor_seconds - (time.monotonic() - started_at)
        if remaining > 0:
            await asyncio.sleep(remaining)

    @staticmethod
    def _normalize_email(value: str) -> NormalizedEmail:
        try:
            return normalize_email(value)
        except EmailNormalizationError as exc:
            raise AuthInputError(
                pointer="/email",
                code="invalid_format",
                detail="Enter a valid email address.",
            ) from exc

    @staticmethod
    def _normalize_new_password(value: str, *, pointer: str) -> str:
        try:
            return validate_new_password(value)
        except PasswordInputError as exc:
            raise AuthInputError(
                pointer=pointer,
                code=exc.code,
                detail=exc.detail,
                parameters=exc.parameters,
            ) from exc

    @staticmethod
    def _normalize_auth_password(value: str) -> str:
        try:
            return normalize_password_for_authentication(value)
        except PasswordInputError as exc:
            raise AuthInputError(
                pointer="/password",
                code=exc.code,
                detail=exc.detail,
                parameters=exc.parameters,
            ) from exc

    @staticmethod
    def _is_email_uniqueness_conflict(exc: IntegrityError) -> bool:
        diagnostic = getattr(exc.orig, "diag", None)
        return getattr(diagnostic, "constraint_name", None) == _EMAIL_UNIQUENESS_CONSTRAINT

    def _issued_session(
        self,
        *,
        account_ref: UUID,
        auth_session_ref: UUID,
        authenticated_at: datetime,
        recent_auth_at: datetime,
        expires_at: datetime,
        secret_verifier: bytes,
        session_secret: SecretStr,
    ) -> IssuedSession:
        return IssuedSession(
            principal=Principal(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=authenticated_at,
                recent_auth_at=recent_auth_at,
            ),
            expires_at=expires_at,
            session_secret=session_secret,
            csrf_token=derive_csrf_token(
                csrf_key=self._csrf_key,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
            ),
        )

    @staticmethod
    async def _safe_rollback(database_session: AsyncSession) -> None:
        if not database_session.in_transaction():
            return
        with suppress(SQLAlchemyError):
            await database_session.rollback()
