"""M5-F WebAuthn/passkey application and persistence state machine."""

from __future__ import annotations

import hmac
import secrets
from collections.abc import Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

from pydantic import SecretStr
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.authenticator_lifecycle import (
    AuthenticatorState,
    _issued_session,
    _lock_current_session,
    _presented_session_verifier,
    _read_authenticator_state,
    _rotate_locked_session,
    require_viable_authenticator_state,
)
from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthenticatorRemovalBlockedError,
    AuthInputError,
    AuthIntegrityError,
    AuthServiceUnavailableError,
    AuthStateChangedError,
    IssuedSession,
    PasskeyAlreadyRegisteredError,
    PasskeyCeremonyBegun,
    PasskeyChallengeInvalidOrExpiredError,
    PasskeyMethod,
    PasskeyNotFoundError,
    PasskeyVerificationFailedError,
    Principal,
    ReauthenticationRequiredError,
)
from dante.auth.lifecycle import KeyedRateLimiter
from dante.auth.proofs import FlowProofPurpose, flow_proof_verifier_from_raw
from dante.auth.sessions import (
    derive_csrf_token,
    generate_session_secret,
    session_secret_verifier,
)
from dante.auth.webauthn import (
    ParsedWebAuthnResponse,
    WebAuthnAssertionEvidence,
    WebAuthnPolicy,
    WebAuthnRegistrationEvidence,
)
from dante.platform.config.auth import AuthSettings
from dante.platform.database.mappings.auth import (
    AccountRow,
    AuthSessionRow,
    EmailIdentityRow,
    PasskeyCredentialRow,
    WebAuthnAccountRow,
    WebAuthnChallengeRow,
)

_CHALLENGE_BYTES = 32
_EXPIRED_CLEANUP_BATCH = 128
_MAX_TRANSPORTS = 8
_MAX_TRANSPORT_LENGTH = 32
_MAX_LABEL_LENGTH = 100


@dataclass(frozen=True, slots=True)
class PasskeyFlowLimiters:
    """Bounded process-local ingress guards; PostgreSQL remains replay/race authority."""

    begin: KeyedRateLimiter
    complete: KeyedRateLimiter


@dataclass(frozen=True, slots=True)
class _ChallengeSnapshot:
    webauthn_challenge_ref: UUID
    ceremony_code: str
    challenge_verifier: bytes
    account_ref: UUID | None
    auth_session_ref: UUID | None
    auth_session_secret_verifier: bytes | None
    user_handle: bytes | None
    rp_id: str
    expected_origin: str
    created_at: datetime
    expires_at: datetime
    claimed_at: datetime


@dataclass(frozen=True, slots=True)
class _CredentialSnapshot:
    passkey_credential_ref: UUID
    account_ref: UUID
    user_handle: bytes
    credential_id: bytes
    public_key_cose: bytes
    cose_algorithm: int
    backup_eligible: bool


class PasskeyFlowService:
    """Canonical WebAuthn ceremony, credential and AuthSession authority."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings,
        policy: WebAuthnPolicy,
        limiters: PasskeyFlowLimiters,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._webauthn = settings.provider.webauthn
        self._policy = policy
        self._limiters = limiters

    async def begin_registration(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        expected_origin: str,
    ) -> PasskeyCeremonyBegun:
        """Begin one recent-authenticated resident passkey registration."""
        self._require_origin(expected_origin)
        await self._limiters.begin.consume(
            str(admitted.principal.account_ref),
            code="auth.passkey_rate_limited",
        )
        await self._cleanup_expired_challenges()
        presented_verifier = _presented_session_verifier(presented_session_secret)
        challenge = secrets.token_bytes(_CHALLENGE_BYTES)
        challenge_verifier = self._challenge_verifier(challenge)
        challenge_ref = uuid7()

        user_handle: bytes | None = None
        display_name: str | None = None
        existing_credential_ids: tuple[bytes, ...] = ()
        created_at: datetime | None = None
        expires_at: datetime | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            created_at = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=created_at,
                require_recent=True,
            )
            webauthn_account = await database_session.scalar(
                select(WebAuthnAccountRow).where(
                    WebAuthnAccountRow.account_ref == locked.account_ref
                )
            )
            if webauthn_account is None:
                user_handle = secrets.token_bytes(_CHALLENGE_BYTES)
                webauthn_account = WebAuthnAccountRow(
                    account_ref=locked.account_ref,
                    user_handle=user_handle,
                    created_at=created_at,
                )
                database_session.add(webauthn_account)
                await database_session.flush()
            else:
                user_handle = webauthn_account.user_handle

            display_name = await database_session.scalar(
                select(EmailIdentityRow.address)
                .where(
                    EmailIdentityRow.account_ref == locked.account_ref,
                    EmailIdentityRow.verified_at.is_not(None),
                )
                .order_by(EmailIdentityRow.created_at, EmailIdentityRow.email_identity_ref)
                .limit(1)
            )
            if display_name is None:
                raise AuthIntegrityError("passkey registration Account has no verified EmailIdentity")

            existing_credential_ids = tuple(
                (
                    await database_session.scalars(
                        select(PasskeyCredentialRow.credential_id)
                        .where(PasskeyCredentialRow.account_ref == locked.account_ref)
                        .order_by(PasskeyCredentialRow.passkey_credential_ref)
                    )
                ).all()
            )
            expires_at = created_at + timedelta(
                seconds=self._webauthn.challenge_lifetime_seconds
            )
            database_session.add(
                WebAuthnChallengeRow(
                    webauthn_challenge_ref=challenge_ref,
                    ceremony_code="registration",
                    challenge_verifier=challenge_verifier,
                    account_ref=locked.account_ref,
                    auth_session_ref=locked.auth_session_ref,
                    auth_session_secret_verifier=locked.old_secret_verifier,
                    user_handle=user_handle,
                    rp_id=self._policy.rp_id,
                    expected_origin=expected_origin,
                    created_at=created_at,
                    expires_at=expires_at,
                    claimed_at=None,
                )
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            AccountUnavailableError,
            AuthIntegrityError,
            AuthStateChangedError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if user_handle is None or display_name is None or created_at is None or expires_at is None:
            raise AuthIntegrityError("passkey registration begin lost frozen state")
        if ambiguous_commit:
            await self._reconcile_challenge_insert(
                challenge_ref=challenge_ref,
                ceremony_code="registration",
                challenge_verifier=challenge_verifier,
                account_ref=admitted.principal.account_ref,
                auth_session_ref=admitted.principal.auth_session_ref,
                auth_session_secret_verifier=presented_verifier,
                user_handle=user_handle,
                expected_origin=expected_origin,
                created_at=created_at,
                expires_at=expires_at,
            )
        options = self._policy.registration_options(
            user_handle=user_handle,
            display_name=display_name,
            challenge=challenge,
            existing_credential_ids=existing_credential_ids,
        )
        return PasskeyCeremonyBegun(
            webauthn_challenge_ref=challenge_ref,
            options=options,
            expires_at=expires_at,
        )

    async def complete_registration(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        webauthn_challenge_ref: UUID,
        response: Mapping[str, Any],
        label: str,
        transports: Sequence[str] = (),
    ) -> IssuedSession:
        """Verify and lifetime-bind one new passkey, then rotate the same AuthSession bearer."""
        normalized_label = self._normalize_label(label)
        normalized_transports = self._normalize_transports(transports)
        parsed = self._parse_registration(response)
        await self._limiters.complete.consume(
            str(admitted.principal.account_ref),
            code="auth.passkey_rate_limited",
        )
        snapshot = await self._claim_challenge(
            webauthn_challenge_ref=webauthn_challenge_ref,
            ceremony_code="registration",
            parsed=parsed,
        )
        if (
            snapshot.account_ref is None
            or snapshot.auth_session_ref is None
            or snapshot.auth_session_secret_verifier is None
            or snapshot.user_handle is None
            or snapshot.account_ref != admitted.principal.account_ref
            or snapshot.auth_session_ref != admitted.principal.auth_session_ref
        ):
            await self._delete_challenge(snapshot)
            raise PasskeyChallengeInvalidOrExpiredError()

        try:
            evidence = self._policy.verify_registration(
                response=response,
                expected_challenge=parsed.challenge,
            )
        except (TypeError, ValueError) as exc:
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError() from exc
        if evidence.credential_id != parsed.credential_id:
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError()

        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_secret = generate_session_secret()
        new_secret_verifier = session_secret_verifier(new_secret)
        credential_ref = uuid7()
        mutation_at: datetime | None = None
        locked = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(snapshot.account_ref))
            )
            mutation_at = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=mutation_at,
                require_recent=True,
            )
            if not hmac.compare_digest(
                locked.old_secret_verifier,
                snapshot.auth_session_secret_verifier,
            ):
                raise AuthStateChangedError()
            webauthn_account = await database_session.scalar(
                select(WebAuthnAccountRow).where(
                    WebAuthnAccountRow.account_ref == locked.account_ref,
                    WebAuthnAccountRow.user_handle == snapshot.user_handle,
                )
            )
            if webauthn_account is None:
                raise AuthStateChangedError()
            existing = await database_session.scalar(
                select(PasskeyCredentialRow.passkey_credential_ref).where(
                    PasskeyCredentialRow.credential_id == evidence.credential_id
                )
            )
            if existing is not None:
                raise PasskeyAlreadyRegisteredError()

            database_session.add(
                PasskeyCredentialRow(
                    passkey_credential_ref=credential_ref,
                    account_ref=locked.account_ref,
                    credential_id=evidence.credential_id,
                    credential_public_key=evidence.public_key_cose,
                    cose_algorithm=evidence.cose_algorithm,
                    sign_count=evidence.sign_count,
                    backup_eligible=evidence.backup_eligible,
                    backup_state=evidence.backup_state,
                    transports=list(normalized_transports),
                    label=normalized_label,
                    status_code="active",
                    created_at=mutation_at,
                    updated_at=mutation_at,
                    last_used_at=None,
                    revoked_at=None,
                    revocation_reason_code=None,
                )
            )
            await database_session.flush()
            await self._consume_claimed_challenge(database_session, snapshot=snapshot)
            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_secret_verifier,
                now=mutation_at,
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
            PasskeyAlreadyRegisteredError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if await self._credential_id_exists(evidence.credential_id):
                raise PasskeyAlreadyRegisteredError() from exc
            raise AuthServiceUnavailableError(retryable=True) from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if locked is None or mutation_at is None:
            raise AuthIntegrityError("passkey registration completion lost locked state")
        if ambiguous_commit:
            await self._reconcile_registration(
                snapshot=snapshot,
                credential_ref=credential_ref,
                account_ref=locked.account_ref,
                evidence=evidence,
                mutation_at=mutation_at,
                new_session_verifier=new_secret_verifier,
            )
        return _issued_session(
            settings=self._settings,
            locked=locked,
            new_secret=new_secret,
            new_secret_verifier=new_secret_verifier,
        )

    async def begin_authentication(
        self,
        *,
        expected_origin: str,
        source_context: str,
    ) -> PasskeyCeremonyBegun:
        """Begin discoverable username-less passkey authentication."""
        self._require_origin(expected_origin)
        await self._limiters.begin.consume(
            source_context,
            code="auth.passkey_rate_limited",
        )
        await self._cleanup_expired_challenges()
        challenge = secrets.token_bytes(_CHALLENGE_BYTES)
        verifier = self._challenge_verifier(challenge)
        challenge_ref = uuid7()
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._webauthn.challenge_lifetime_seconds)
        row = WebAuthnChallengeRow(
            webauthn_challenge_ref=challenge_ref,
            ceremony_code="authentication",
            challenge_verifier=verifier,
            account_ref=None,
            auth_session_ref=None,
            auth_session_secret_verifier=None,
            user_handle=None,
            rp_id=self._policy.rp_id,
            expected_origin=expected_origin,
            created_at=now,
            expires_at=expires_at,
            claimed_at=None,
        )
        ambiguous_commit = await self._insert_challenge(row)
        if ambiguous_commit:
            await self._reconcile_challenge_insert(
                challenge_ref=challenge_ref,
                ceremony_code="authentication",
                challenge_verifier=verifier,
                account_ref=None,
                auth_session_ref=None,
                auth_session_secret_verifier=None,
                user_handle=None,
                expected_origin=expected_origin,
                created_at=now,
                expires_at=expires_at,
            )
        return PasskeyCeremonyBegun(
            webauthn_challenge_ref=challenge_ref,
            options=self._policy.authentication_options(
                challenge=challenge,
                credential_ids=None,
            ),
            expires_at=expires_at,
        )

    async def complete_authentication(
        self,
        *,
        webauthn_challenge_ref: UUID,
        response: Mapping[str, Any],
        source_context: str,
    ) -> IssuedSession:
        """Verify one discoverable assertion and create a fresh canonical AuthSession."""
        parsed = self._parse_authentication(response)
        await self._limiters.complete.consume(
            source_context,
            code="auth.passkey_rate_limited",
        )
        snapshot = await self._claim_challenge(
            webauthn_challenge_ref=webauthn_challenge_ref,
            ceremony_code="authentication",
            parsed=parsed,
        )
        if any(
            value is not None
            for value in (
                snapshot.account_ref,
                snapshot.auth_session_ref,
                snapshot.auth_session_secret_verifier,
                snapshot.user_handle,
            )
        ):
            await self._delete_challenge(snapshot)
            raise PasskeyChallengeInvalidOrExpiredError()
        if parsed.user_handle is None or len(parsed.user_handle) != _CHALLENGE_BYTES:
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError()

        credential_snapshot = await self._read_credential_snapshot(
            credential_id=parsed.credential_id,
            account_ref=None,
        )
        if credential_snapshot is None or not hmac.compare_digest(
            credential_snapshot.user_handle,
            parsed.user_handle,
        ):
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError()
        evidence = await self._verify_assertion(
            snapshot=snapshot,
            parsed=parsed,
            response=response,
            credential=credential_snapshot,
        )

        auth_session_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        mutation_at = datetime.now(UTC)
        expires_at = mutation_at + timedelta(seconds=self._settings.session_max_age_seconds)
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(credential_snapshot.account_ref))
            )
            account = await database_session.scalar(
                select(AccountRow).where(
                    AccountRow.account_ref == credential_snapshot.account_ref
                )
            )
            if account is None or account.status_code != "active":
                raise AccountUnavailableError()
            credential = await self._lock_exact_credential(
                database_session,
                snapshot=credential_snapshot,
            )
            self._apply_assertion_state(
                credential,
                evidence=evidence,
                mutation_at=mutation_at,
            )
            await self._consume_claimed_challenge(database_session, snapshot=snapshot)
            database_session.add(
                AuthSessionRow(
                    auth_session_ref=auth_session_ref,
                    account_ref=credential_snapshot.account_ref,
                    secret_verifier=secret_verifier,
                    created_at=mutation_at,
                    authenticated_at=mutation_at,
                    recent_auth_at=mutation_at,
                    last_user_activity_at=mutation_at,
                    expires_at=expires_at,
                    revoked_at=None,
                    revocation_reason_code=None,
                )
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (AccountUnavailableError, AuthStateChangedError, PasskeyVerificationFailedError):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            await self._reconcile_authentication(
                snapshot=snapshot,
                credential=credential_snapshot,
                evidence=evidence,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
                mutation_at=mutation_at,
                expires_at=expires_at,
            )
        return IssuedSession(
            principal=Principal(
                account_ref=credential_snapshot.account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=mutation_at,
                recent_auth_at=mutation_at,
            ),
            expires_at=expires_at,
            session_secret=session_secret,
            csrf_token=derive_csrf_token(
                csrf_key=self._settings.csrf_key_bytes,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
            ),
        )

    async def begin_reauthentication(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        expected_origin: str,
    ) -> PasskeyCeremonyBegun:
        """Begin passkey reauthentication without requiring already-recent evidence."""
        self._require_origin(expected_origin)
        await self._limiters.begin.consume(
            str(admitted.principal.account_ref),
            code="auth.passkey_rate_limited",
        )
        await self._cleanup_expired_challenges()
        presented_verifier = _presented_session_verifier(presented_session_secret)
        challenge = secrets.token_bytes(_CHALLENGE_BYTES)
        verifier = self._challenge_verifier(challenge)
        challenge_ref = uuid7()

        user_handle: bytes | None = None
        credential_ids: tuple[bytes, ...] = ()
        created_at: datetime | None = None
        expires_at: datetime | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            created_at = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=created_at,
                require_recent=False,
            )
            user_handle = await database_session.scalar(
                select(WebAuthnAccountRow.user_handle).where(
                    WebAuthnAccountRow.account_ref == locked.account_ref
                )
            )
            credential_ids = tuple(
                (
                    await database_session.scalars(
                        select(PasskeyCredentialRow.credential_id)
                        .where(
                            PasskeyCredentialRow.account_ref == locked.account_ref,
                            PasskeyCredentialRow.status_code == "active",
                        )
                        .order_by(PasskeyCredentialRow.passkey_credential_ref)
                    )
                ).all()
            )
            if user_handle is None or not credential_ids:
                raise PasskeyNotFoundError()
            expires_at = created_at + timedelta(
                seconds=self._webauthn.challenge_lifetime_seconds
            )
            database_session.add(
                WebAuthnChallengeRow(
                    webauthn_challenge_ref=challenge_ref,
                    ceremony_code="reauthentication",
                    challenge_verifier=verifier,
                    account_ref=locked.account_ref,
                    auth_session_ref=locked.auth_session_ref,
                    auth_session_secret_verifier=locked.old_secret_verifier,
                    user_handle=user_handle,
                    rp_id=self._policy.rp_id,
                    expected_origin=expected_origin,
                    created_at=created_at,
                    expires_at=expires_at,
                    claimed_at=None,
                )
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
            PasskeyNotFoundError,
        ):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if user_handle is None or created_at is None or expires_at is None:
            raise AuthIntegrityError("passkey reauthentication begin lost frozen state")
        if ambiguous_commit:
            await self._reconcile_challenge_insert(
                challenge_ref=challenge_ref,
                ceremony_code="reauthentication",
                challenge_verifier=verifier,
                account_ref=admitted.principal.account_ref,
                auth_session_ref=admitted.principal.auth_session_ref,
                auth_session_secret_verifier=presented_verifier,
                user_handle=user_handle,
                expected_origin=expected_origin,
                created_at=created_at,
                expires_at=expires_at,
            )
        return PasskeyCeremonyBegun(
            webauthn_challenge_ref=challenge_ref,
            options=self._policy.authentication_options(
                challenge=challenge,
                credential_ids=credential_ids,
            ),
            expires_at=expires_at,
        )

    async def complete_reauthentication(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        webauthn_challenge_ref: UUID,
        response: Mapping[str, Any],
    ) -> IssuedSession:
        """Refresh recent authentication and rotate the exact same AuthSession bearer."""
        parsed = self._parse_authentication(response)
        await self._limiters.complete.consume(
            str(admitted.principal.account_ref),
            code="auth.passkey_rate_limited",
        )
        snapshot = await self._claim_challenge(
            webauthn_challenge_ref=webauthn_challenge_ref,
            ceremony_code="reauthentication",
            parsed=parsed,
        )
        if (
            snapshot.account_ref is None
            or snapshot.auth_session_ref is None
            or snapshot.auth_session_secret_verifier is None
            or snapshot.user_handle is None
            or snapshot.account_ref != admitted.principal.account_ref
            or snapshot.auth_session_ref != admitted.principal.auth_session_ref
            or (
                parsed.user_handle is not None
                and not hmac.compare_digest(parsed.user_handle, snapshot.user_handle)
            )
        ):
            await self._delete_challenge(snapshot)
            raise PasskeyChallengeInvalidOrExpiredError()
        credential_snapshot = await self._read_credential_snapshot(
            credential_id=parsed.credential_id,
            account_ref=snapshot.account_ref,
        )
        if credential_snapshot is None or not hmac.compare_digest(
            credential_snapshot.user_handle,
            snapshot.user_handle,
        ):
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError()
        evidence = await self._verify_assertion(
            snapshot=snapshot,
            parsed=parsed,
            response=response,
            credential=credential_snapshot,
        )

        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_secret = generate_session_secret()
        new_secret_verifier = session_secret_verifier(new_secret)
        mutation_at: datetime | None = None
        locked = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(snapshot.account_ref))
            )
            mutation_at = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=mutation_at,
                require_recent=False,
            )
            if not hmac.compare_digest(
                locked.old_secret_verifier,
                snapshot.auth_session_secret_verifier,
            ):
                raise AuthStateChangedError()
            credential = await self._lock_exact_credential(
                database_session,
                snapshot=credential_snapshot,
            )
            self._apply_assertion_state(
                credential,
                evidence=evidence,
                mutation_at=mutation_at,
            )
            await self._consume_claimed_challenge(database_session, snapshot=snapshot)
            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_secret_verifier,
                now=mutation_at,
            )
            refreshed = await database_session.scalar(
                update(AuthSessionRow)
                .where(
                    AuthSessionRow.auth_session_ref == locked.auth_session_ref,
                    AuthSessionRow.account_ref == locked.account_ref,
                    AuthSessionRow.secret_verifier == new_secret_verifier,
                    AuthSessionRow.revoked_at.is_(None),
                )
                .values(recent_auth_at=mutation_at)
                .returning(AuthSessionRow.auth_session_ref)
            )
            if refreshed is None:
                raise AuthStateChangedError()
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            AccountUnavailableError,
            AuthStateChangedError,
            PasskeyVerificationFailedError,
        ):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if locked is None or mutation_at is None:
            raise AuthIntegrityError("passkey reauthentication completion lost locked state")
        if ambiguous_commit:
            await self._reconcile_reauthentication(
                snapshot=snapshot,
                credential=credential_snapshot,
                evidence=evidence,
                auth_session_ref=locked.auth_session_ref,
                new_session_verifier=new_secret_verifier,
                recent_auth_at=mutation_at,
            )
        return IssuedSession(
            principal=Principal(
                account_ref=locked.account_ref,
                auth_session_ref=locked.auth_session_ref,
                authenticated_at=locked.authenticated_at,
                recent_auth_at=mutation_at,
            ),
            expires_at=locked.expires_at,
            session_secret=new_secret,
            csrf_token=derive_csrf_token(
                csrf_key=self._settings.csrf_key_bytes,
                auth_session_ref=locked.auth_session_ref,
                secret_verifier=new_secret_verifier,
            ),
        )

    async def list_passkeys(
        self,
        *,
        admitted: AdmittedSession,
    ) -> tuple[PasskeyMethod, ...]:
        """Return safe active-passkey management metadata without credential secrets."""
        try:
            async with self._session_factory() as database_session, database_session.begin():
                account = await database_session.scalar(
                    select(AccountRow).where(
                        AccountRow.account_ref == admitted.principal.account_ref
                    )
                )
                if account is None or account.status_code != "active":
                    raise AccountUnavailableError()
                rows = tuple(
                    (
                        await database_session.scalars(
                            select(PasskeyCredentialRow)
                            .where(
                                PasskeyCredentialRow.account_ref == account.account_ref,
                                PasskeyCredentialRow.status_code == "active",
                            )
                            .order_by(
                                PasskeyCredentialRow.created_at,
                                PasskeyCredentialRow.passkey_credential_ref,
                            )
                        )
                    ).all()
                )
        except AccountUnavailableError:
            raise
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        return tuple(
            PasskeyMethod(
                passkey_credential_ref=row.passkey_credential_ref,
                label=row.label,
                transports=tuple(row.transports),
                backup_eligible=row.backup_eligible,
                backup_state=row.backup_state,
                created_at=row.created_at,
                last_used_at=row.last_used_at,
            )
            for row in rows
        )

    async def update_label(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        passkey_credential_ref: UUID,
        label: str,
    ) -> None:
        """Update only user-facing passkey label; no security evidence changes."""
        normalized_label = self._normalize_label(label)
        presented_verifier = _presented_session_verifier(presented_session_secret)
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
                require_recent=False,
            )
            credential = await database_session.scalar(
                select(PasskeyCredentialRow)
                .where(
                    PasskeyCredentialRow.passkey_credential_ref == passkey_credential_ref,
                    PasskeyCredentialRow.account_ref == locked.account_ref,
                    PasskeyCredentialRow.status_code == "active",
                )
                .with_for_update()
            )
            if credential is None:
                raise PasskeyNotFoundError()
            credential.label = normalized_label
            credential.updated_at = now
            await database_session.commit()
        except (AccountUnavailableError, AuthStateChangedError, PasskeyNotFoundError):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

    async def remove_passkey(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        passkey_credential_ref: UUID,
    ) -> IssuedSession:
        """Logically revoke one passkey only when Account-wide anti-lockout remains viable."""
        presented_verifier = _presented_session_verifier(presented_session_secret)
        new_secret = generate_session_secret()
        new_secret_verifier = session_secret_verifier(new_secret)
        locked = None
        mutation_at: datetime | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(admitted.principal.account_ref))
            )
            mutation_at = datetime.now(UTC)
            locked = await _lock_current_session(
                database_session,
                settings=self._settings,
                admitted=admitted,
                presented_session_verifier=presented_verifier,
                now=mutation_at,
                require_recent=True,
            )
            credential = await database_session.scalar(
                select(PasskeyCredentialRow)
                .where(
                    PasskeyCredentialRow.passkey_credential_ref == passkey_credential_ref,
                    PasskeyCredentialRow.account_ref == locked.account_ref,
                )
                .with_for_update()
            )
            if credential is None or credential.status_code != "active":
                raise PasskeyNotFoundError()
            state = await _read_authenticator_state(
                database_session,
                account_ref=locked.account_ref,
            )
            resulting = AuthenticatorState(
                password_present=state.password_present,
                active_provider_count=state.active_provider_count,
                active_passkey_count=max(0, state.active_passkey_count - 1),
                recovery_eligible_email_count=state.recovery_eligible_email_count,
            )
            require_viable_authenticator_state(resulting)
            credential.status_code = "revoked"
            credential.updated_at = mutation_at
            credential.revoked_at = mutation_at
            credential.revocation_reason_code = "user_removed"
            await _rotate_locked_session(
                database_session,
                locked=locked,
                new_secret_verifier=new_secret_verifier,
                now=mutation_at,
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
            PasskeyNotFoundError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if locked is None or mutation_at is None:
            raise AuthIntegrityError("passkey removal lost locked state")
        if ambiguous_commit:
            await self._reconcile_removal(
                account_ref=locked.account_ref,
                passkey_credential_ref=passkey_credential_ref,
                revoked_at=mutation_at,
                auth_session_ref=locked.auth_session_ref,
                new_session_verifier=new_secret_verifier,
            )
        return _issued_session(
            settings=self._settings,
            locked=locked,
            new_secret=new_secret,
            new_secret_verifier=new_secret_verifier,
        )

    async def _claim_challenge(
        self,
        *,
        webauthn_challenge_ref: UUID,
        ceremony_code: str,
        parsed: ParsedWebAuthnResponse,
    ) -> _ChallengeSnapshot:
        verifier = flow_proof_verifier_from_raw(
            purpose=FlowProofPurpose.WEBAUTHN_CHALLENGE,
            raw_secret=parsed.challenge,
        )
        if verifier is None or not self._policy.origin_allowed(parsed.origin):
            raise PasskeyChallengeInvalidOrExpiredError()
        claimed_at = datetime.now(UTC)
        ambiguous_commit = False
        challenge: WebAuthnChallengeRow | None = None
        database_session = self._session_factory()
        try:
            await database_session.begin()
            claimed_ref = await database_session.scalar(
                update(WebAuthnChallengeRow)
                .where(
                    WebAuthnChallengeRow.webauthn_challenge_ref == webauthn_challenge_ref,
                    WebAuthnChallengeRow.ceremony_code == ceremony_code,
                    WebAuthnChallengeRow.challenge_verifier == verifier,
                    WebAuthnChallengeRow.rp_id == self._policy.rp_id,
                    WebAuthnChallengeRow.expected_origin == parsed.origin,
                    WebAuthnChallengeRow.claimed_at.is_(None),
                    WebAuthnChallengeRow.expires_at > claimed_at,
                )
                .values(claimed_at=claimed_at)
                .returning(WebAuthnChallengeRow.webauthn_challenge_ref)
            )
            if claimed_ref is None:
                raise PasskeyChallengeInvalidOrExpiredError()
            challenge = await database_session.scalar(
                select(WebAuthnChallengeRow).where(
                    WebAuthnChallengeRow.webauthn_challenge_ref == webauthn_challenge_ref
                )
            )
            if challenge is None:
                raise AuthIntegrityError("claimed WebAuthn challenge disappeared before commit")
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except PasskeyChallengeInvalidOrExpiredError:
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            challenge = await self._reconcile_challenge_claim(
                challenge_ref=webauthn_challenge_ref,
                ceremony_code=ceremony_code,
                challenge_verifier=verifier,
                claimed_at=claimed_at,
            )
        if challenge is None:
            raise AuthIntegrityError("WebAuthn challenge claim lost canonical row")
        return self._snapshot(challenge, claimed_at=claimed_at)

    async def _verify_assertion(
        self,
        *,
        snapshot: _ChallengeSnapshot,
        parsed: ParsedWebAuthnResponse,
        response: Mapping[str, Any],
        credential: _CredentialSnapshot,
    ) -> WebAuthnAssertionEvidence:
        try:
            evidence = self._policy.verify_authentication(
                response=response,
                expected_challenge=parsed.challenge,
                credential_id=credential.credential_id,
                public_key_cose=credential.public_key_cose,
                cose_algorithm=credential.cose_algorithm,
            )
        except (TypeError, ValueError) as exc:
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError() from exc
        if evidence.credential_id != credential.credential_id:
            await self._delete_challenge(snapshot)
            raise PasskeyVerificationFailedError()
        return evidence

    async def _read_credential_snapshot(
        self,
        *,
        credential_id: bytes,
        account_ref: UUID | None,
    ) -> _CredentialSnapshot | None:
        statement = (
            select(PasskeyCredentialRow, WebAuthnAccountRow, AccountRow)
            .join(
                WebAuthnAccountRow,
                WebAuthnAccountRow.account_ref == PasskeyCredentialRow.account_ref,
            )
            .join(AccountRow, AccountRow.account_ref == PasskeyCredentialRow.account_ref)
            .where(
                PasskeyCredentialRow.credential_id == credential_id,
                PasskeyCredentialRow.status_code == "active",
                AccountRow.status_code == "active",
            )
        )
        if account_ref is not None:
            statement = statement.where(PasskeyCredentialRow.account_ref == account_ref)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = (await database_session.execute(statement)).one_or_none()
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc
        if row is None:
            return None
        credential, webauthn_account, _account = row
        return _CredentialSnapshot(
            passkey_credential_ref=credential.passkey_credential_ref,
            account_ref=credential.account_ref,
            user_handle=webauthn_account.user_handle,
            credential_id=credential.credential_id,
            public_key_cose=credential.credential_public_key,
            cose_algorithm=credential.cose_algorithm,
            backup_eligible=credential.backup_eligible,
        )

    async def _lock_exact_credential(
        self,
        database_session: AsyncSession,
        *,
        snapshot: _CredentialSnapshot,
    ) -> PasskeyCredentialRow:
        credential = await database_session.scalar(
            select(PasskeyCredentialRow)
            .where(
                PasskeyCredentialRow.passkey_credential_ref == snapshot.passkey_credential_ref,
                PasskeyCredentialRow.account_ref == snapshot.account_ref,
                PasskeyCredentialRow.credential_id == snapshot.credential_id,
            )
            .with_for_update()
        )
        webauthn_account = await database_session.scalar(
            select(WebAuthnAccountRow).where(
                WebAuthnAccountRow.account_ref == snapshot.account_ref,
                WebAuthnAccountRow.user_handle == snapshot.user_handle,
            )
        )
        if (
            credential is None
            or credential.status_code != "active"
            or webauthn_account is None
            or credential.credential_public_key != snapshot.public_key_cose
            or credential.cose_algorithm != snapshot.cose_algorithm
            or credential.backup_eligible != snapshot.backup_eligible
        ):
            raise AuthStateChangedError()
        return credential

    @staticmethod
    def _apply_assertion_state(
        credential: PasskeyCredentialRow,
        *,
        evidence: WebAuthnAssertionEvidence,
        mutation_at: datetime,
    ) -> None:
        if evidence.backup_eligible != credential.backup_eligible:
            raise PasskeyVerificationFailedError()
        credential.sign_count = max(credential.sign_count, evidence.sign_count)
        credential.backup_state = evidence.backup_state
        credential.last_used_at = mutation_at
        credential.updated_at = mutation_at

    async def _consume_claimed_challenge(
        self,
        database_session: AsyncSession,
        *,
        snapshot: _ChallengeSnapshot,
    ) -> None:
        consumed = await database_session.scalar(
            delete(WebAuthnChallengeRow)
            .where(
                WebAuthnChallengeRow.webauthn_challenge_ref == snapshot.webauthn_challenge_ref,
                WebAuthnChallengeRow.ceremony_code == snapshot.ceremony_code,
                WebAuthnChallengeRow.challenge_verifier == snapshot.challenge_verifier,
                WebAuthnChallengeRow.claimed_at == snapshot.claimed_at,
            )
            .returning(WebAuthnChallengeRow.webauthn_challenge_ref)
        )
        if consumed is None:
            raise PasskeyChallengeInvalidOrExpiredError()

    async def _insert_challenge(self, row: WebAuthnChallengeRow) -> bool:
        database_session = self._session_factory()
        try:
            await database_session.begin()
            database_session.add(row)
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                return True
            return False
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

    async def _delete_challenge(self, snapshot: _ChallengeSnapshot) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                await database_session.execute(
                    delete(WebAuthnChallengeRow).where(
                        WebAuthnChallengeRow.webauthn_challenge_ref
                        == snapshot.webauthn_challenge_ref,
                        WebAuthnChallengeRow.challenge_verifier == snapshot.challenge_verifier,
                        WebAuthnChallengeRow.claimed_at == snapshot.claimed_at,
                    )
                )
        except SQLAlchemyError:
            return

    async def _cleanup_expired_challenges(self) -> None:
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                refs = tuple(
                    (
                        await database_session.scalars(
                            select(WebAuthnChallengeRow.webauthn_challenge_ref)
                            .where(WebAuthnChallengeRow.expires_at <= now)
                            .order_by(WebAuthnChallengeRow.expires_at)
                            .limit(_EXPIRED_CLEANUP_BATCH)
                        )
                    ).all()
                )
                if refs:
                    await database_session.execute(
                        delete(WebAuthnChallengeRow).where(
                            WebAuthnChallengeRow.webauthn_challenge_ref.in_(refs)
                        )
                    )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _reconcile_challenge_insert(
        self,
        *,
        challenge_ref: UUID,
        ceremony_code: str,
        challenge_verifier: bytes,
        account_ref: UUID | None,
        auth_session_ref: UUID | None,
        auth_session_secret_verifier: bytes | None,
        user_handle: bytes | None,
        expected_origin: str,
        created_at: datetime,
        expires_at: datetime,
    ) -> None:
        row = await self._read_challenge(challenge_ref)
        if row is None:
            raise AuthServiceUnavailableError(retryable=True)
        if (
            row.ceremony_code == ceremony_code
            and hmac.compare_digest(row.challenge_verifier, challenge_verifier)
            and row.account_ref == account_ref
            and row.auth_session_ref == auth_session_ref
            and self._optional_bytes_equal(
                row.auth_session_secret_verifier,
                auth_session_secret_verifier,
            )
            and self._optional_bytes_equal(row.user_handle, user_handle)
            and row.rp_id == self._policy.rp_id
            and row.expected_origin == expected_origin
            and row.created_at == created_at
            and row.expires_at == expires_at
            and row.claimed_at is None
        ):
            return
        raise AuthIntegrityError("ambiguous WebAuthn challenge insertion mismatched state")

    async def _reconcile_challenge_claim(
        self,
        *,
        challenge_ref: UUID,
        ceremony_code: str,
        challenge_verifier: bytes,
        claimed_at: datetime,
    ) -> WebAuthnChallengeRow:
        row = await self._read_challenge(challenge_ref)
        if row is None:
            raise AuthServiceUnavailableError(retryable=False)
        if (
            row.ceremony_code == ceremony_code
            and hmac.compare_digest(row.challenge_verifier, challenge_verifier)
            and row.claimed_at == claimed_at
        ):
            return row
        if row.claimed_at is None:
            raise AuthServiceUnavailableError(retryable=True)
        raise PasskeyChallengeInvalidOrExpiredError()

    async def _reconcile_registration(
        self,
        *,
        snapshot: _ChallengeSnapshot,
        credential_ref: UUID,
        account_ref: UUID,
        evidence: WebAuthnRegistrationEvidence,
        mutation_at: datetime,
        new_session_verifier: bytes,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                credential = await database_session.scalar(
                    select(PasskeyCredentialRow).where(
                        PasskeyCredentialRow.passkey_credential_ref == credential_ref
                    )
                )
                challenge = await database_session.scalar(
                    select(WebAuthnChallengeRow.webauthn_challenge_ref).where(
                        WebAuthnChallengeRow.webauthn_challenge_ref
                        == snapshot.webauthn_challenge_ref
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == snapshot.auth_session_ref,
                        AuthSessionRow.account_ref == account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            credential is not None
            and credential.account_ref == account_ref
            and credential.credential_id == evidence.credential_id
            and credential.credential_public_key == evidence.public_key_cose
            and credential.cose_algorithm == evidence.cose_algorithm
            and credential.created_at == mutation_at
            and challenge is None
            and self._session_has_verifier(auth_session, new_session_verifier)
        ):
            return
        if challenge == snapshot.webauthn_challenge_ref:
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous passkey registration reconciliation mismatched state")

    async def _reconcile_authentication(
        self,
        *,
        snapshot: _ChallengeSnapshot,
        credential: _CredentialSnapshot,
        evidence: WebAuthnAssertionEvidence,
        auth_session_ref: UUID,
        secret_verifier: bytes,
        mutation_at: datetime,
        expires_at: datetime,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                persisted_credential = await database_session.scalar(
                    select(PasskeyCredentialRow).where(
                        PasskeyCredentialRow.passkey_credential_ref
                        == credential.passkey_credential_ref
                    )
                )
                challenge = await database_session.scalar(
                    select(WebAuthnChallengeRow.webauthn_challenge_ref).where(
                        WebAuthnChallengeRow.webauthn_challenge_ref
                        == snapshot.webauthn_challenge_ref
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref,
                        AuthSessionRow.account_ref == credential.account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            persisted_credential is not None
            and persisted_credential.status_code == "active"
            and persisted_credential.sign_count >= evidence.sign_count
            and persisted_credential.backup_state == evidence.backup_state
            and persisted_credential.last_used_at == mutation_at
            and challenge is None
            and auth_session is not None
            and auth_session.secret_verifier == secret_verifier
            and auth_session.authenticated_at == mutation_at
            and auth_session.recent_auth_at == mutation_at
            and auth_session.expires_at == expires_at
            and auth_session.revoked_at is None
        ):
            return
        if challenge == snapshot.webauthn_challenge_ref and auth_session is None:
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous passkey authentication reconciliation mismatched state")

    async def _reconcile_reauthentication(
        self,
        *,
        snapshot: _ChallengeSnapshot,
        credential: _CredentialSnapshot,
        evidence: WebAuthnAssertionEvidence,
        auth_session_ref: UUID,
        new_session_verifier: bytes,
        recent_auth_at: datetime,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                persisted_credential = await database_session.scalar(
                    select(PasskeyCredentialRow).where(
                        PasskeyCredentialRow.passkey_credential_ref
                        == credential.passkey_credential_ref
                    )
                )
                challenge = await database_session.scalar(
                    select(WebAuthnChallengeRow.webauthn_challenge_ref).where(
                        WebAuthnChallengeRow.webauthn_challenge_ref
                        == snapshot.webauthn_challenge_ref
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref,
                        AuthSessionRow.account_ref == credential.account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            persisted_credential is not None
            and persisted_credential.status_code == "active"
            and persisted_credential.sign_count >= evidence.sign_count
            and persisted_credential.backup_state == evidence.backup_state
            and persisted_credential.last_used_at == recent_auth_at
            and challenge is None
            and self._session_has_verifier(auth_session, new_session_verifier)
            and auth_session is not None
            and auth_session.recent_auth_at == recent_auth_at
        ):
            return
        if challenge == snapshot.webauthn_challenge_ref:
            raise AuthServiceUnavailableError(retryable=True)
        raise AuthIntegrityError("ambiguous passkey reauthentication reconciliation mismatched state")

    async def _reconcile_removal(
        self,
        *,
        account_ref: UUID,
        passkey_credential_ref: UUID,
        revoked_at: datetime,
        auth_session_ref: UUID,
        new_session_verifier: bytes,
    ) -> None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                credential = await database_session.scalar(
                    select(PasskeyCredentialRow).where(
                        PasskeyCredentialRow.passkey_credential_ref == passkey_credential_ref,
                        PasskeyCredentialRow.account_ref == account_ref,
                    )
                )
                auth_session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref,
                        AuthSessionRow.account_ref == account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            credential is not None
            and credential.status_code == "revoked"
            and credential.revoked_at == revoked_at
            and credential.revocation_reason_code == "user_removed"
            and self._session_has_verifier(auth_session, new_session_verifier)
        ):
            return
        raise AuthIntegrityError("ambiguous passkey removal reconciliation mismatched state")

    async def _read_challenge(self, challenge_ref: UUID) -> WebAuthnChallengeRow | None:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row: WebAuthnChallengeRow | None = await database_session.scalar(
                    select(WebAuthnChallengeRow).where(
                        WebAuthnChallengeRow.webauthn_challenge_ref == challenge_ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

    async def _credential_id_exists(self, credential_id: bytes) -> bool:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                value = await database_session.scalar(
                    select(PasskeyCredentialRow.passkey_credential_ref).where(
                        PasskeyCredentialRow.credential_id == credential_id
                    )
                )
                return value is not None
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

    def _parse_registration(self, response: Mapping[str, Any]) -> ParsedWebAuthnResponse:
        try:
            return self._policy.parse_registration(response)
        except (TypeError, ValueError, KeyError) as exc:
            raise PasskeyVerificationFailedError() from exc

    def _parse_authentication(self, response: Mapping[str, Any]) -> ParsedWebAuthnResponse:
        try:
            return self._policy.parse_authentication(response)
        except (TypeError, ValueError, KeyError) as exc:
            raise PasskeyVerificationFailedError() from exc

    def _require_origin(self, origin: str) -> None:
        if not self._policy.origin_allowed(origin):
            raise AuthInputError(
                pointer="/origin",
                code="invalid_origin",
                detail="WebAuthn origin is not configured for this relying party.",
            )

    @staticmethod
    def _challenge_verifier(challenge: bytes) -> bytes:
        verifier = flow_proof_verifier_from_raw(
            purpose=FlowProofPurpose.WEBAUTHN_CHALLENGE,
            raw_secret=challenge,
        )
        if verifier is None:
            raise AuthIntegrityError("generated WebAuthn challenge has invalid width")
        return verifier

    @staticmethod
    def _normalize_label(value: str) -> str:
        if (
            not value
            or value.strip() != value
            or len(value) > _MAX_LABEL_LENGTH
            or any(character in value for character in "\r\n")
        ):
            raise AuthInputError(
                pointer="/label",
                code="invalid_format",
                detail="Passkey label must be trimmed, single-line and at most 100 characters.",
            )
        return value

    @staticmethod
    def _normalize_transports(values: Sequence[str]) -> tuple[str, ...]:
        if len(values) > _MAX_TRANSPORTS:
            raise AuthInputError(
                pointer="/transports",
                code="too_many_items",
                detail="Passkey transports exceed the supported bound.",
            )
        result: list[str] = []
        for value in values:
            if (
                not value
                or value.strip() != value
                or len(value) > _MAX_TRANSPORT_LENGTH
                or any(character in value for character in "\r\n")
            ):
                raise AuthInputError(
                    pointer="/transports",
                    code="invalid_format",
                    detail="Passkey transport hint is invalid.",
                )
            if value not in result:
                result.append(value)
        return tuple(result)

    @staticmethod
    def _snapshot(row: WebAuthnChallengeRow, *, claimed_at: datetime) -> _ChallengeSnapshot:
        if row.claimed_at != claimed_at:
            raise AuthIntegrityError("WebAuthn claimed timestamp changed unexpectedly")
        return _ChallengeSnapshot(
            webauthn_challenge_ref=row.webauthn_challenge_ref,
            ceremony_code=row.ceremony_code,
            challenge_verifier=row.challenge_verifier,
            account_ref=row.account_ref,
            auth_session_ref=row.auth_session_ref,
            auth_session_secret_verifier=row.auth_session_secret_verifier,
            user_handle=row.user_handle,
            rp_id=row.rp_id,
            expected_origin=row.expected_origin,
            created_at=row.created_at,
            expires_at=row.expires_at,
            claimed_at=claimed_at,
        )

    @staticmethod
    def _optional_bytes_equal(left: bytes | None, right: bytes | None) -> bool:
        if left is None or right is None:
            return left is right
        return hmac.compare_digest(left, right)

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
