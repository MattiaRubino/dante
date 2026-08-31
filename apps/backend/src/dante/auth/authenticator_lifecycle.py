"""M5-E/G Account-wide authenticator and password/passwordless lifecycle."""

from __future__ import annotations

import hmac
import logging
import time
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import override
from uuid import UUID, uuid7

from pydantic import SecretStr
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthenticationMethods,
    AuthenticationProviderMethod,
    AuthenticatorRemovalBlockedError,
    AuthIntegrityError,
    AuthServiceUnavailableError,
    AuthStateChangedError,
    IssuedSession,
    PasswordAlreadyEstablishedError,
    Principal,
    ProviderIdentityConflictError,
    ProviderLinkAccountMismatchError,
    ProviderLinkInvalidOrExpiredError,
    ProviderLinkState,
    ProviderReconciliationPendingError,
    ProviderUnavailableError,
    ReauthenticationRequiredError,
    RecoveryInvalidOrExpiredError,
    RecoveryValidation,
)
from dante.auth.email_delivery import (
    EmailDeliveryPort,
    EmailDispatchCapacityError,
    NoopEmail,
    PasswordRecoveryEmail,
    PasswordResetNotificationEmail,
)
from dante.auth.lifecycle import AuthLifecycleService, LifecycleLimiters
from dante.auth.passwords import HibpPasswordChecker, PasswordKdf
from dante.auth.proofs import (
    FlowProofPurpose,
    SignupOtpCodec,
    flow_proof_matches,
    issue_recovery_proof,
    recovery_secret_matches,
    recovery_secret_verifier,
)
from dante.auth.sessions import (
    decode_session_secret,
    derive_csrf_token,
    generate_session_secret,
    session_secret_verifier,
    session_secret_verifier_from_raw,
)
from dante.platform.config.auth import AuthSettings
from dante.platform.database.mappings.auth import (
    AccountRow,
    AppleAuthGrantRow,
    AuthSessionRow,
    EmailIdentityRow,
    ExternalIdentityRow,
    ExternalLinkChallengeRow,
    PasskeyCredentialRow,
    PasswordCredentialRow,
    PasswordRecoveryChallengeRow,
)

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class AuthenticatorState:
    """Durable Account-wide facts used by the pure anti-lockout decision."""

    password_present: bool
    active_provider_count: int
    active_passkey_count: int
    recovery_eligible_email_count: int

    @property
    def direct_authenticator_count(self) -> int:
        """Return the number of direct authenticators represented by this state."""
        return (
            int(self.password_present)
            + self.active_provider_count
            + self.active_passkey_count
        )


def require_viable_authenticator_state(state: AuthenticatorState) -> None:
    """Reject states that would lock an Account out after a normal removal."""
    if state.direct_authenticator_count < 1:
        raise AuthenticatorRemovalBlockedError()
    if not state.password_present and state.recovery_eligible_email_count < 1:
        raise AuthenticatorRemovalBlockedError()


@dataclass(frozen=True, slots=True)
class _LockedSession:
    account_ref: UUID
    auth_session_ref: UUID
    authenticated_at: datetime
    recent_auth_at: datetime
    expires_at: datetime
    old_secret_verifier: bytes


@dataclass(frozen=True, slots=True)
class _RecoveryChannel:
    account_ref: UUID
    email_identity_ref: UUID
    email_address: str
    email_comparison_key: str


@dataclass(frozen=True, slots=True)
class _RecoveryProofSnapshot:
    password_recovery_ref: UUID
    account_ref: UUID
    email_identity_ref: UUID
    email_address: str
    secret_verifier: bytes
    issued_at: datetime
    expires_at: datetime


async def _lock_current_session(
    database_session: AsyncSession,
    *,
    settings: AuthSettings,
    admitted: AdmittedSession,
    presented_session_verifier: bytes,
    now: datetime,
    require_recent: bool,
) -> _LockedSession:
    """Re-read the exact current bearer under the already-held Account security lock."""
    account = await database_session.scalar(
        select(AccountRow).where(AccountRow.account_ref == admitted.principal.account_ref)
    )
    if account is None or account.status_code != "active":
        raise AccountUnavailableError()

    auth_session = await database_session.scalar(
        select(AuthSessionRow)
        .where(
            AuthSessionRow.auth_session_ref == admitted.principal.auth_session_ref,
            AuthSessionRow.account_ref == admitted.principal.account_ref,
        )
        .with_for_update()
    )
    idle_deadline = (
        auth_session.last_user_activity_at
        + timedelta(seconds=settings.session_idle_timeout_seconds)
        if auth_session is not None
        else now
    )
    if (
        auth_session is None
        or auth_session.revoked_at is not None
        or auth_session.expires_at <= now
        or idle_deadline <= now
        or not hmac.compare_digest(
            auth_session.secret_verifier,
            presented_session_verifier,
        )
    ):
        raise AuthStateChangedError()
    if require_recent and (
        auth_session.recent_auth_at
        + timedelta(seconds=settings.recent_auth_window_seconds)
        <= now
    ):
        raise ReauthenticationRequiredError()

    return _LockedSession(
        account_ref=auth_session.account_ref,
        auth_session_ref=auth_session.auth_session_ref,
        authenticated_at=auth_session.authenticated_at,
        recent_auth_at=auth_session.recent_auth_at,
        expires_at=auth_session.expires_at,
        old_secret_verifier=auth_session.secret_verifier,
    )


async def _rotate_locked_session(
    database_session: AsyncSession,
    *,
    locked: _LockedSession,
    new_secret_verifier: bytes,
    now: datetime,
) -> None:
    rotated = await database_session.scalar(
        update(AuthSessionRow)
        .where(
            AuthSessionRow.auth_session_ref == locked.auth_session_ref,
            AuthSessionRow.account_ref == locked.account_ref,
            AuthSessionRow.secret_verifier == locked.old_secret_verifier,
            AuthSessionRow.revoked_at.is_(None),
        )
        .values(
            secret_verifier=new_secret_verifier,
            last_user_activity_at=now,
        )
        .returning(AuthSessionRow.auth_session_ref)
    )
    if rotated is None:
        raise AuthStateChangedError()


async def _read_authenticator_state(
    database_session: AsyncSession,
    *,
    account_ref: UUID,
) -> AuthenticatorState:
    password_ref = await database_session.scalar(
        select(PasswordCredentialRow.password_credential_ref).where(
            PasswordCredentialRow.account_ref == account_ref
        )
    )
    provider_count = await database_session.scalar(
        select(func.count())
        .select_from(ExternalIdentityRow)
        .where(
            ExternalIdentityRow.account_ref == account_ref,
            ExternalIdentityRow.status_code == "active",
        )
    )
    passkey_count = await database_session.scalar(
        select(func.count())
        .select_from(PasskeyCredentialRow)
        .where(
            PasskeyCredentialRow.account_ref == account_ref,
            PasskeyCredentialRow.status_code == "active",
        )
    )
    recovery_count = await database_session.scalar(
        select(func.count())
        .select_from(EmailIdentityRow)
        .where(
            EmailIdentityRow.account_ref == account_ref,
            EmailIdentityRow.verified_at.is_not(None),
            EmailIdentityRow.recovery_restriction_code.is_(None),
        )
    )
    return AuthenticatorState(
        password_present=password_ref is not None,
        active_provider_count=int(provider_count or 0),
        active_passkey_count=int(passkey_count or 0),
        recovery_eligible_email_count=int(recovery_count or 0),
    )


def _presented_session_verifier(value: str) -> bytes:
    raw = decode_session_secret(value)
    if raw is None:
        raise AuthStateChangedError()
    return session_secret_verifier_from_raw(raw)


def _issued_session(
    *,
    settings: AuthSettings,
    locked: _LockedSession,
    new_secret: SecretStr,
    new_secret_verifier: bytes,
) -> IssuedSession:
    return IssuedSession(
        principal=Principal(
            account_ref=locked.account_ref,
            auth_session_ref=locked.auth_session_ref,
            authenticated_at=locked.authenticated_at,
            recent_auth_at=locked.recent_auth_at,
        ),
        expires_at=locked.expires_at,
        session_secret=new_secret,
        csrf_token=derive_csrf_token(
            csrf_key=settings.csrf_key_bytes,
            auth_session_ref=locked.auth_session_ref,
            secret_verifier=new_secret_verifier,
        ),
    )


class MultiAuthenticatorLifecycleService(AuthLifecycleService):
    """M4 lifecycle plus M5 password establishment/removal and passwordless recovery."""

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
    ) -> None:
        super().__init__(
            session_factory=session_factory,
            settings=settings,
            password_kdf=password_kdf,
            breach_checker=breach_checker,
            otp_codec=otp_codec,
            email_delivery=email_delivery,
            limiters=limiters,
        )

    async def establish_password(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        new_password: str,
    ) -> IssuedSession:
        """Establish the first password under Account lock and rotate the same session bearer."""
        normalized = self._normalize_new_password(new_password, pointer="/new_password")
        await self._require_uncompromised_new_password(normalized)
        verifier, pepper_key_id = await self._password_kdf.hash_normalized_password(normalized)
        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_session_secret = generate_session_secret()
        new_session_verifier = session_secret_verifier(new_session_secret)

        now: datetime | None = None
        locked: _LockedSession | None = None
        ambiguous_commit = False
        credential_ref = uuid7()
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            now = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=now,
                require_recent=True,
            )
            existing = await database_session.scalar(
                select(PasswordCredentialRow.password_credential_ref).where(
                    PasswordCredentialRow.account_ref == locked.account_ref
                )
            )
            if existing is not None:
                raise PasswordAlreadyEstablishedError()

            await database_session.execute(
                delete(PasswordRecoveryChallengeRow).where(
                    PasswordRecoveryChallengeRow.account_ref == locked.account_ref
                )
            )
            database_session.add(
                PasswordCredentialRow(
                    password_credential_ref=credential_ref,
                    account_ref=locked.account_ref,
                    verifier=verifier,
                    pepper_key_id=pepper_key_id,
                    created_at=now,
                    updated_at=now,
                )
            )
            await database_session.flush()
            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_session_verifier,
                now=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            AccountUnavailableError,
            AuthStateChangedError,
            PasswordAlreadyEstablishedError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            raise PasswordAlreadyEstablishedError() from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if locked is None or now is None:
            raise AuthIntegrityError("password establishment lost locked session state")
        if ambiguous_commit:
            await self._reconcile_password_establishment(
                locked=locked,
                credential_ref=credential_ref,
                password_verifier=verifier,
                pepper_key_id=pepper_key_id,
                mutation_at=now,
                new_session_verifier=new_session_verifier,
            )
        return _issued_session(
            settings=self._settings,
            locked=locked,
            new_secret=new_session_secret,
            new_secret_verifier=new_session_verifier,
        )

    async def remove_password(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
    ) -> IssuedSession:
        """Remove the current password only when Account-wide anti-lockout remains satisfied."""
        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_session_secret = generate_session_secret()
        new_session_verifier = session_secret_verifier(new_session_secret)

        now: datetime | None = None
        locked: _LockedSession | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            now = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=now,
                require_recent=True,
            )
            credential = await database_session.scalar(
                select(PasswordCredentialRow)
                .where(PasswordCredentialRow.account_ref == locked.account_ref)
                .with_for_update()
            )
            if credential is None:
                raise AuthStateChangedError()

            state = await _read_authenticator_state(
                database_session,
                account_ref=locked.account_ref,
            )
            resulting = AuthenticatorState(
                password_present=False,
                active_provider_count=state.active_provider_count,
                active_passkey_count=state.active_passkey_count,
                recovery_eligible_email_count=state.recovery_eligible_email_count,
            )
            require_viable_authenticator_state(resulting)

            await database_session.execute(
                delete(PasswordRecoveryChallengeRow).where(
                    PasswordRecoveryChallengeRow.account_ref == locked.account_ref
                )
            )
            await database_session.delete(credential)
            await database_session.flush()
            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_session_verifier,
                now=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            AccountUnavailableError,
            AuthenticatorRemovalBlockedError,
            AuthStateChangedError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if locked is None or now is None:
            raise AuthIntegrityError("password removal lost locked session state")
        if ambiguous_commit:
            await self._reconcile_password_removal(
                locked=locked,
                new_session_verifier=new_session_verifier,
            )
        return _issued_session(
            settings=self._settings,
            locked=locked,
            new_secret=new_session_secret,
            new_secret_verifier=new_session_verifier,
        )

    @override
    async def request_password_recovery(
        self,
        *,
        email: str,
        source_context: str,
    ) -> None:
        """Issue a neutral recovery proof for any active Account with an eligible mailbox."""
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

        channel = await self._read_recovery_channel(normalized_email.comparison_key)
        if channel is None:
            await self._enqueue(NoopEmail())
            await self._pad_recovery_success(started_at)
            return

        recovery_ref = uuid7()
        proof = issue_recovery_proof()
        committed = await self._persist_passwordless_recovery_challenge(
            channel=channel,
            password_recovery_ref=recovery_ref,
            secret_verifier=proof.verifier,
        )
        if not committed:
            await self._enqueue(NoopEmail())
            await self._pad_recovery_success(started_at)
            return

        await self._enqueue(
            PasswordRecoveryEmail(
                to_address=channel.email_address,
                password_recovery_ref=recovery_ref,
                secret=proof.secret,
            )
        )
        await self._pad_recovery_success(started_at)

    @override
    async def validate_password_recovery(
        self,
        *,
        password_recovery_ref: UUID,
        secret: str,
    ) -> RecoveryValidation:
        """Validate an Account+EmailIdentity recovery proof without requiring a password."""
        verifier = recovery_secret_verifier(secret)
        if verifier is None:
            return RecoveryValidation(valid=False)
        snapshot = await self._read_passwordless_recovery_snapshot(password_recovery_ref)
        now = datetime.now(UTC)
        return RecoveryValidation(
            valid=(
                snapshot is not None
                and snapshot.expires_at > now
                and hmac.compare_digest(verifier, snapshot.secret_verifier)
            )
        )

    @override
    async def reset_password(
        self,
        *,
        password_recovery_ref: UUID,
        secret: str,
        new_password: str,
    ) -> None:
        """Consume recovery proof, create-or-replace password, and revoke every AuthSession."""
        snapshot = await self._read_passwordless_recovery_snapshot(password_recovery_ref)
        preflight_now = datetime.now(UTC)
        if (
            snapshot is None
            or snapshot.expires_at <= preflight_now
            or not recovery_secret_matches(secret, snapshot.secret_verifier)
        ):
            raise RecoveryInvalidOrExpiredError()

        normalized = self._normalize_new_password(new_password, pointer="/new_password")
        await self._require_uncompromised_new_password(normalized)
        verifier, pepper_key_id = await self._password_kdf.hash_normalized_password(normalized)

        mutation_at: datetime | None = None
        ambiguous_commit = False
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
            email_identity = await database_session.scalar(
                select(EmailIdentityRow).where(
                    EmailIdentityRow.email_identity_ref == snapshot.email_identity_ref,
                    EmailIdentityRow.account_ref == snapshot.account_ref,
                )
            )
            if (
                account is None
                or account.status_code != "active"
                or email_identity is None
                or email_identity.verified_at is None
                or email_identity.recovery_restriction_code is not None
            ):
                raise RecoveryInvalidOrExpiredError()

            consumed = await database_session.scalar(
                delete(PasswordRecoveryChallengeRow)
                .where(
                    PasswordRecoveryChallengeRow.password_recovery_ref
                    == snapshot.password_recovery_ref,
                    PasswordRecoveryChallengeRow.account_ref == snapshot.account_ref,
                    PasswordRecoveryChallengeRow.email_identity_ref
                    == snapshot.email_identity_ref,
                    PasswordRecoveryChallengeRow.secret_verifier == snapshot.secret_verifier,
                    PasswordRecoveryChallengeRow.expires_at > mutation_at,
                )
                .returning(PasswordRecoveryChallengeRow.password_recovery_ref)
            )
            if consumed is None:
                raise RecoveryInvalidOrExpiredError()

            credential = await database_session.scalar(
                select(PasswordCredentialRow)
                .where(PasswordCredentialRow.account_ref == snapshot.account_ref)
                .with_for_update()
            )
            if credential is None:
                database_session.add(
                    PasswordCredentialRow(
                        password_credential_ref=uuid7(),
                        account_ref=snapshot.account_ref,
                        verifier=verifier,
                        pepper_key_id=pepper_key_id,
                        created_at=mutation_at,
                        updated_at=mutation_at,
                    )
                )
            else:
                credential.verifier = verifier
                credential.pepper_key_id = pepper_key_id
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
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except RecoveryInvalidOrExpiredError:
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if mutation_at is None:
            raise AuthIntegrityError("passwordless reset lost mutation timestamp")
        if ambiguous_commit:
            await self._reconcile_passwordless_reset(
                snapshot=snapshot,
                password_verifier=verifier,
                pepper_key_id=pepper_key_id,
                mutation_at=mutation_at,
            )

        try:
            await self._email_delivery.enqueue(
                PasswordResetNotificationEmail(to_address=snapshot.email_address)
            )
        except EmailDispatchCapacityError:
            _LOGGER.warning("auth.password_reset_notification_queue_unavailable")

    async def _read_recovery_channel(self, comparison_key: str) -> _RecoveryChannel | None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = (
                    await database_session.execute(
                        select(EmailIdentityRow, AccountRow)
                        .join(AccountRow, AccountRow.account_ref == EmailIdentityRow.account_ref)
                        .where(EmailIdentityRow.comparison_key == comparison_key)
                    )
                ).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            return None
        email_identity, account = row
        if (
            account.status_code != "active"
            or email_identity.verified_at is None
            or email_identity.recovery_restriction_code is not None
        ):
            return None
        return _RecoveryChannel(
            account_ref=account.account_ref,
            email_identity_ref=email_identity.email_identity_ref,
            email_address=email_identity.address,
            email_comparison_key=email_identity.comparison_key,
        )

    async def _persist_passwordless_recovery_challenge(
        self,
        *,
        channel: _RecoveryChannel,
        password_recovery_ref: UUID,
        secret_verifier: bytes,
    ) -> bool:
        await self._cleanup_expired_challenges(datetime.now(UTC))
        issued_at: datetime | None = None
        expires_at: datetime | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(channel.account_ref))
            )
            current = await database_session.scalar(
                select(EmailIdentityRow)
                .join(AccountRow, AccountRow.account_ref == EmailIdentityRow.account_ref)
                .where(
                    EmailIdentityRow.email_identity_ref == channel.email_identity_ref,
                    EmailIdentityRow.account_ref == channel.account_ref,
                    EmailIdentityRow.comparison_key == channel.email_comparison_key,
                    EmailIdentityRow.verified_at.is_not(None),
                    EmailIdentityRow.recovery_restriction_code.is_(None),
                    AccountRow.status_code == "active",
                )
            )
            if current is None or current.address != channel.email_address:
                await database_session.rollback()
                return False

            issued_at = datetime.now(UTC)
            expires_at = issued_at + timedelta(seconds=self._settings.recovery_lifetime_seconds)
            await database_session.execute(
                delete(PasswordRecoveryChallengeRow).where(
                    PasswordRecoveryChallengeRow.account_ref == channel.account_ref
                )
            )
            database_session.add(
                PasswordRecoveryChallengeRow(
                    password_recovery_ref=password_recovery_ref,
                    account_ref=channel.account_ref,
                    email_identity_ref=channel.email_identity_ref,
                    secret_verifier=secret_verifier,
                    issued_at=issued_at,
                    expires_at=expires_at,
                )
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
            raise AuthIntegrityError("passwordless recovery issuance lost timestamps")
        if not ambiguous_commit:
            return True
        try:
            async with self._session_factory() as database_session, database_session.begin():
                persisted = await database_session.scalar(
                    select(PasswordRecoveryChallengeRow).where(
                        PasswordRecoveryChallengeRow.password_recovery_ref
                        == password_recovery_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            persisted is not None
            and persisted.account_ref == channel.account_ref
            and persisted.email_identity_ref == channel.email_identity_ref
            and hmac.compare_digest(persisted.secret_verifier, secret_verifier)
            and persisted.issued_at == issued_at
            and persisted.expires_at == expires_at
        ):
            return True
        if persisted is None:
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous passwordless recovery issuance mismatched state")

    async def _read_passwordless_recovery_snapshot(
        self,
        password_recovery_ref: UUID,
    ) -> _RecoveryProofSnapshot | None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = (
                    await database_session.execute(
                        select(
                            PasswordRecoveryChallengeRow,
                            AccountRow,
                            EmailIdentityRow,
                        )
                        .join(
                            AccountRow,
                            AccountRow.account_ref
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
                            AccountRow.status_code == "active",
                            EmailIdentityRow.verified_at.is_not(None),
                            EmailIdentityRow.recovery_restriction_code.is_(None),
                        )
                    )
                ).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            return None
        challenge, _account, email_identity = row
        return _RecoveryProofSnapshot(
            password_recovery_ref=challenge.password_recovery_ref,
            account_ref=challenge.account_ref,
            email_identity_ref=challenge.email_identity_ref,
            email_address=email_identity.address,
            secret_verifier=challenge.secret_verifier,
            issued_at=challenge.issued_at,
            expires_at=challenge.expires_at,
        )

    async def _reconcile_password_establishment(
        self,
        *,
        locked: _LockedSession,
        credential_ref: UUID,
        password_verifier: str,
        pepper_key_id: str,
        mutation_at: datetime,
        new_session_verifier: bytes,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                credential = await database_session.scalar(
                    select(PasswordCredentialRow).where(
                        PasswordCredentialRow.account_ref == locked.account_ref
                    )
                )
                challenge_count = await database_session.scalar(
                    select(func.count())
                    .select_from(PasswordRecoveryChallengeRow)
                    .where(PasswordRecoveryChallengeRow.account_ref == locked.account_ref)
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == locked.auth_session_ref,
                        AuthSessionRow.account_ref == locked.account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            credential is not None
            and credential.password_credential_ref == credential_ref
            and credential.verifier == password_verifier
            and credential.pepper_key_id == pepper_key_id
            and credential.created_at == mutation_at
            and credential.updated_at == mutation_at
            and challenge_count == 0
            and self._session_has_verifier(auth_session, new_session_verifier)
        ):
            return
        if (
            credential is None
            and self._session_has_verifier(auth_session, locked.old_secret_verifier)
        ):
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous password establishment reconciliation mismatched state")

    async def _reconcile_password_removal(
        self,
        *,
        locked: _LockedSession,
        new_session_verifier: bytes,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                credential = await database_session.scalar(
                    select(PasswordCredentialRow.password_credential_ref).where(
                        PasswordCredentialRow.account_ref == locked.account_ref
                    )
                )
                challenge_count = await database_session.scalar(
                    select(func.count())
                    .select_from(PasswordRecoveryChallengeRow)
                    .where(PasswordRecoveryChallengeRow.account_ref == locked.account_ref)
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == locked.auth_session_ref,
                        AuthSessionRow.account_ref == locked.account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            credential is None
            and challenge_count == 0
            and self._session_has_verifier(auth_session, new_session_verifier)
        ):
            return
        if credential is not None and self._session_has_verifier(
            auth_session,
            locked.old_secret_verifier,
        ):
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous password removal reconciliation mismatched state")

    async def _reconcile_passwordless_reset(
        self,
        *,
        snapshot: _RecoveryProofSnapshot,
        password_verifier: str,
        pepper_key_id: str,
        mutation_at: datetime,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
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
                unrevoked = await database_session.scalar(
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
            and credential.verifier == password_verifier
            and credential.pepper_key_id == pepper_key_id
            and credential.updated_at == mutation_at
            and challenge is None
            and unrevoked == 0
        ):
            return
        if challenge == snapshot.password_recovery_ref:
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous passwordless reset reconciliation mismatched state")

    @staticmethod
    def _session_has_verifier(auth_session: AuthSessionRow | None, verifier: bytes) -> bool:
        return (
            auth_session is not None
            and auth_session.revoked_at is None
            and hmac.compare_digest(auth_session.secret_verifier, verifier)
        )


class AuthenticatorLifecycleService:
    """Provider-link, provider-unlink and Account-wide method inventory authority."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings,
        apple_reconciler: Callable[[], Awaitable[int]] | None,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._apple_reconciler = apple_reconciler

    async def authentication_methods(self, *, admitted: AdmittedSession) -> AuthenticationMethods:
        """Return current active methods without exposing provider identity subjects or secrets."""
        try:
            async with self._session_factory() as database_session, database_session.begin():
                account = await database_session.scalar(
                    select(AccountRow).where(
                        AccountRow.account_ref == admitted.principal.account_ref
                    )
                )
                if account is None or account.status_code != "active":
                    raise AccountUnavailableError()
                state = await _read_authenticator_state(
                    database_session,
                    account_ref=account.account_ref,
                )
                providers = tuple(
                    AuthenticationProviderMethod(
                        external_identity_ref=row.external_identity_ref,
                        provider_code=row.provider_code,
                        provider_email_address=row.provider_email_address,
                        provider_email_private=row.provider_email_private,
                    )
                    for row in (
                        await database_session.scalars(
                            select(ExternalIdentityRow)
                            .where(
                                ExternalIdentityRow.account_ref == account.account_ref,
                                ExternalIdentityRow.status_code == "active",
                            )
                            .order_by(
                                ExternalIdentityRow.provider_code,
                                ExternalIdentityRow.external_identity_ref,
                            )
                        )
                    ).all()
                )
        except AccountUnavailableError:
            raise
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        return AuthenticationMethods(
            password_established=state.password_present,
            providers=providers,
            active_passkey_count=state.active_passkey_count,
            recovery_eligible_email_count=state.recovery_eligible_email_count,
        )

    async def inspect_provider_link(
        self,
        *,
        external_link_challenge_ref: UUID,
        continuation_secret: str,
    ) -> ProviderLinkState:
        """Validate one provider-first continuation capability without exposing its Account target."""
        try:
            async with self._session_factory() as database_session, database_session.begin():
                challenge = await database_session.scalar(
                    select(ExternalLinkChallengeRow).where(
                        ExternalLinkChallengeRow.external_link_challenge_ref
                        == external_link_challenge_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        self._require_link_challenge(
            challenge,
            continuation_secret=continuation_secret,
            now=datetime.now(UTC),
        )
        if challenge is None:
            raise ProviderLinkInvalidOrExpiredError()
        return ProviderLinkState(
            external_link_challenge_ref=challenge.external_link_challenge_ref,
            provider_code=challenge.provider_code,
            expires_at=challenge.expires_at,
        )

    async def confirm_provider_link(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        external_link_challenge_ref: UUID,
        continuation_secret: str,
    ) -> IssuedSession:
        """Bind verified provider-first evidence to the exact authenticated target Account."""
        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_session_secret = generate_session_secret()
        new_session_verifier = session_secret_verifier(new_session_secret)

        now: datetime | None = None
        locked: _LockedSession | None = None
        identity_ref: UUID | None = None
        provider_code: str | None = None
        issuer: str | None = None
        subject: str | None = None
        apple_grant_ref: UUID | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            now = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=now,
                require_recent=True,
            )
            challenge = await database_session.scalar(
                select(ExternalLinkChallengeRow).where(
                    ExternalLinkChallengeRow.external_link_challenge_ref
                    == external_link_challenge_ref
                )
            )
            self._require_link_challenge(
                challenge,
                continuation_secret=continuation_secret,
                now=now,
            )
            if challenge is None:
                raise ProviderLinkInvalidOrExpiredError()
            if challenge.target_account_ref != locked.account_ref:
                raise ProviderLinkAccountMismatchError()
            target_email = await database_session.scalar(
                select(EmailIdentityRow).where(
                    EmailIdentityRow.email_identity_ref
                    == challenge.target_email_identity_ref,
                    EmailIdentityRow.account_ref == locked.account_ref,
                )
            )
            if target_email is None:
                raise AuthStateChangedError()

            provider_code = challenge.provider_code
            issuer = challenge.issuer
            subject = challenge.subject
            apple_grant_ref = challenge.apple_auth_grant_ref
            identity = await database_session.scalar(
                select(ExternalIdentityRow)
                .where(
                    ExternalIdentityRow.issuer == challenge.issuer,
                    ExternalIdentityRow.subject == challenge.subject,
                )
                .with_for_update()
            )
            if identity is not None and identity.account_ref != locked.account_ref:
                raise ProviderIdentityConflictError()
            if identity is None:
                identity_ref = uuid7()
                identity = ExternalIdentityRow(
                    external_identity_ref=identity_ref,
                    account_ref=locked.account_ref,
                    email_identity_ref=challenge.target_email_identity_ref,
                    provider_code=challenge.provider_code,
                    issuer=challenge.issuer,
                    subject=challenge.subject,
                    provider_email_address=challenge.provider_email_address,
                    provider_email_private=challenge.provider_email_private,
                    status_code="active",
                    created_at=now,
                    status_changed_at=now,
                    last_authenticated_at=challenge.created_at,
                    revoked_at=None,
                    revocation_reason_code=None,
                )
                database_session.add(identity)
                await database_session.flush()
            else:
                identity_ref = identity.external_identity_ref
                identity.provider_email_address = challenge.provider_email_address,
                identity.provider_email_private = challenge.provider_email_private
                identity.status_code = "active"
                identity.status_changed_at = now
                identity.last_authenticated_at = max(
                    identity.last_authenticated_at,
                    challenge.created_at,
                )
                identity.revoked_at = None
                identity.revocation_reason_code = None

            if challenge.provider_code == "apple":
                await self._activate_apple_grant_for_link(
                    database_session,
                    challenge=challenge,
                    external_identity_ref=identity_ref,
                    now=now,
                )
            elif challenge.apple_auth_grant_ref is not None:
                raise AuthIntegrityError("non-Apple link challenge unexpectedly owns Apple grant")

            consumed_link_ref = await database_session.scalar(
                delete(ExternalLinkChallengeRow)
                .where(
                    ExternalLinkChallengeRow.external_link_challenge_ref
                    == external_link_challenge_ref,
                    ExternalLinkChallengeRow.target_account_ref == locked.account_ref,
                    ExternalLinkChallengeRow.target_email_identity_ref
                    == challenge.target_email_identity_ref,
                    ExternalLinkChallengeRow.provider_code == challenge.provider_code,
                    ExternalLinkChallengeRow.issuer == challenge.issuer,
                    ExternalLinkChallengeRow.subject == challenge.subject,
                    ExternalLinkChallengeRow.apple_auth_grant_ref
                    == challenge.apple_auth_grant_ref,
                    ExternalLinkChallengeRow.continuation_verifier
                    == challenge.continuation_verifier,
                    ExternalLinkChallengeRow.expires_at == challenge.expires_at,
                    ExternalLinkChallengeRow.expires_at > now,
                )
                .returning(ExternalLinkChallengeRow.external_link_challenge_ref)
            )
            if consumed_link_ref is None:
                raise ProviderLinkInvalidOrExpiredError()

            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_session_verifier,
                now=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            AccountUnavailableError,
            AuthStateChangedError,
            ProviderIdentityConflictError,
            ProviderLinkAccountMismatchError,
            ProviderLinkInvalidOrExpiredError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if issuer is not None and subject is not None and locked is not None:
                current = await self._read_external_identity(issuer=issuer, subject=subject)
                if current is not None and current.account_ref != locked.account_ref:
                    raise ProviderIdentityConflictError() from exc
            raise AuthServiceUnavailableError(retryable=True) from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if (
            locked is None
            or now is None
            or identity_ref is None
            or provider_code is None
            or issuer is None
            or subject is None
        ):
            raise AuthIntegrityError("provider link confirmation lost frozen state")
        if ambiguous_commit:
            await self._reconcile_provider_link(
                locked=locked,
                challenge_ref=external_link_challenge_ref,
                external_identity_ref=identity_ref,
                issuer=issuer,
                subject=subject,
                apple_grant_ref=apple_grant_ref,
                new_session_verifier=new_session_verifier,
            )
        return _issued_session(
            settings=self._settings,
            locked=locked,
            new_secret=new_session_secret,
            new_secret_verifier=new_session_verifier,
        )

    async def unlink_provider(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        external_identity_ref: UUID,
    ) -> IssuedSession:
        """Revoke one provider identity locally while preserving Account anti-lockout."""
        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_session_secret = generate_session_secret()
        new_session_verifier = session_secret_verifier(new_session_secret)

        now: datetime | None = None
        locked: _LockedSession | None = None
        provider_code: str | None = None
        apple_grant_ref: UUID | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            now = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=now,
                require_recent=True,
            )
            identity = await database_session.scalar(
                select(ExternalIdentityRow)
                .where(
                    ExternalIdentityRow.external_identity_ref == external_identity_ref,
                    ExternalIdentityRow.account_ref == locked.account_ref,
                )
                .with_for_update()
            )
            if identity is None or identity.status_code != "active":
                raise AuthStateChangedError()

            state = await _read_authenticator_state(
                database_session,
                account_ref=locked.account_ref,
            )
            resulting = AuthenticatorState(
                password_present=state.password_present,
                active_provider_count=max(0, state.active_provider_count - 1),
                active_passkey_count=state.active_passkey_count,
                recovery_eligible_email_count=state.recovery_eligible_email_count,
            )
            require_viable_authenticator_state(resulting)

            provider_code = identity.provider_code
            identity.status_code = "revoked"
            identity.status_changed_at = now
            identity.revoked_at = now
            identity.revocation_reason_code = "user_unlinked"
            if identity.provider_code == "apple":
                grant = await database_session.scalar(
                    select(AppleAuthGrantRow)
                    .where(
                        AppleAuthGrantRow.external_identity_ref == external_identity_ref,
                        AppleAuthGrantRow.issuer == identity.issuer,
                        AppleAuthGrantRow.subject == identity.subject,
                    )
                    .with_for_update()
                )
                if grant is None or grant.status_code != "active":
                    raise AuthIntegrityError("active Apple identity lost its active durable grant")
                grant.status_code = "revocation_pending"
                grant.updated_at = now
                grant.status_changed_at = now
                grant.pending_expires_at = None
                grant.revocation_requested_at = now
                grant.revoked_at = None
                apple_grant_ref = grant.apple_auth_grant_ref

            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_session_verifier,
                now=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            AccountUnavailableError,
            AuthenticatorRemovalBlockedError,
            AuthStateChangedError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if locked is None or now is None or provider_code is None:
            raise AuthIntegrityError("provider unlink lost frozen state")
        if ambiguous_commit:
            await self._reconcile_provider_unlink(
                locked=locked,
                external_identity_ref=external_identity_ref,
                apple_grant_ref=apple_grant_ref,
                new_session_verifier=new_session_verifier,
            )

        if provider_code == "apple" and apple_grant_ref is not None:
            await self._best_effort_apple_reconcile()
        return _issued_session(
            settings=self._settings,
            locked=locked,
            new_secret=new_session_secret,
            new_secret_verifier=new_session_verifier,
        )

    async def _activate_apple_grant_for_link(
        self,
        database_session: AsyncSession,
        *,
        challenge: ExternalLinkChallengeRow,
        external_identity_ref: UUID,
        now: datetime,
    ) -> None:
        grant_ref = challenge.apple_auth_grant_ref
        if grant_ref is None:
            raise AuthIntegrityError("Apple link challenge lost its required grant")
        grant = await database_session.scalar(
            select(AppleAuthGrantRow)
            .where(
                AppleAuthGrantRow.apple_auth_grant_ref == grant_ref,
                AppleAuthGrantRow.issuer == challenge.issuer,
                AppleAuthGrantRow.subject == challenge.subject,
            )
            .with_for_update()
        )
        if (
            grant is None
            or grant.status_code != "pending"
            or grant.external_identity_ref is not None
            or grant.pending_expires_at is None
            or grant.pending_expires_at <= now
        ):
            raise ProviderLinkInvalidOrExpiredError()
        grant.external_identity_ref = external_identity_ref
        grant.status_code = "active"
        grant.updated_at = now
        grant.status_changed_at = now
        grant.pending_expires_at = None
        grant.revocation_requested_at = None
        grant.revoked_at = None

    async def _reconcile_provider_link(
        self,
        *,
        locked: _LockedSession,
        challenge_ref: UUID,
        external_identity_ref: UUID,
        issuer: str,
        subject: str,
        apple_grant_ref: UUID | None,
        new_session_verifier: bytes,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                challenge = await database_session.scalar(
                    select(ExternalLinkChallengeRow.external_link_challenge_ref).where(
                        ExternalLinkChallengeRow.external_link_challenge_ref == challenge_ref
                    )
                )
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.issuer == issuer,
                        ExternalIdentityRow.subject == subject,
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == locked.auth_session_ref,
                        AuthSessionRow.account_ref == locked.account_ref,
                    )
                )
                grant = (
                    await database_session.scalar(
                        select(AppleAuthGrantRow).where(
                            AppleAuthGrantRow.apple_auth_grant_ref == apple_grant_ref
                        )
                    )
                    if apple_grant_ref is not None
                    else None
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        exact_grant = apple_grant_ref is None or (
            grant is not None
            and grant.status_code == "active"
            and grant.external_identity_ref == external_identity_ref
        )
        if (
            challenge is None
            and identity is not None
            and identity.account_ref == locked.account_ref
            and identity.status_code == "active"
            and exact_grant
            and self._session_has_verifier(auth_session, new_session_verifier)
        ):
            return
        if challenge == challenge_ref and self._session_has_verifier(
            auth_session,
            locked.old_secret_verifier,
        ):
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous provider link reconciliation mismatched state")

    async def _reconcile_provider_unlink(
        self,
        *,
        locked: _LockedSession,
        external_identity_ref: UUID,
        apple_grant_ref: UUID | None,
        new_session_verifier: bytes,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.account_ref == locked.account_ref,
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == locked.auth_session_ref,
                        AuthSessionRow.account_ref == locked.account_ref,
                    )
                )
                grant = (
                    await database_session.scalar(
                        select(AppleAuthGrantRow).where(
                            AppleAuthGrantRow.apple_auth_grant_ref == apple_grant_ref
                        )
                    )
                    if apple_grant_ref is not None
                    else None
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        exact_grant = apple_grant_ref is None or (
            grant is not None
            and grant.status_code == "revocation_pending"
            and grant.external_identity_ref == external_identity_ref
        )
        if (
            identity is not None
            and identity.status_code == "revoked"
            and identity.revocation_reason_code == "user_unlinked"
            and exact_grant
            and self._session_has_verifier(auth_session, new_session_verifier)
        ):
            return
        if (
            identity is not None
            and identity.status_code == "active"
            and self._session_has_verifier(auth_session, locked.old_secret_verifier)
        ):
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous provider unlink reconciliation mismatched state")

    async def _read_external_identity(
        self,
        *,
        issuer: str,
        subject: str,
    ) -> ExternalIdentityRow | None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                identity: ExternalIdentityRow | None = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.issuer == issuer,
                        ExternalIdentityRow.subject == subject,
                    )
                )
                return identity
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _best_effort_apple_reconcile(self) -> None:
        reconciler = self._apple_reconciler
        if reconciler is None:
            _LOGGER.warning("auth.apple_unlink_remote_reconciliation_unavailable")
            return
        try:
            await reconciler()
        except (
            AuthServiceUnavailableError,
            ProviderReconciliationPendingError,
            ProviderUnavailableError,
        ):
            _LOGGER.warning("auth.apple_unlink_remote_reconciliation_pending")

    @staticmethod
    def _require_link_challenge(
        challenge: ExternalLinkChallengeRow | None,
        *,
        continuation_secret: str,
        now: datetime,
    ) -> None:
        if (
            challenge is None
            or challenge.expires_at <= now
            or not flow_proof_matches(
                purpose=FlowProofPurpose.PROVIDER_LINK,
                encoded_secret=continuation_secret,
                expected_verifier=challenge.continuation_verifier,
            )
        ):
            raise ProviderLinkInvalidOrExpiredError()

    @staticmethod
    def _session_has_verifier(auth_session: AuthSessionRow | None, verifier: bytes) -> bool:
        return (
            auth_session is not None
            and auth_session.revoked_at is None
            and hmac.compare_digest(auth_session.secret_verifier, verifier)
        )

    @staticmethod
    async def _safe_rollback(database_session: AsyncSession) -> None:
        if not database_session.in_transaction():
            return
        with suppress(SQLAlchemyError):
            await database_session.rollback()
