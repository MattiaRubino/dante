"""M5-D Apple application flow over canonical DANTE Account/AuthSession persistence."""

from __future__ import annotations

import hmac
import math
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid7

from pydantic import SecretStr
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.apple import (
    AppleAuthenticationBegun,
    AppleAuthorizationProfile,
    AppleExchangeAmbiguousError,
    AppleIdentityEvidence,
    AppleNotificationEvent,
    AppleNotificationVerifier,
    AppleProofError,
    AppleProtocolClient,
    AppleProtocolError,
    AppleProviderUnavailableError,
    AppleTokenVerifier,
    build_apple_authorization_url,
    is_apple_private_email,
    parse_apple_authorization_profile,
    reconcile_apple_profile_email,
)
from dante.auth.apple_crypto import AppleGrantCipher, AppleGrantCryptoError, EncryptedAppleGrant
from dante.auth.contracts import (
    AccountUnavailableError,
    AdmittedSession,
    AuthInputError,
    AuthIntegrityError,
    AuthServiceUnavailableError,
    EmailDeliveryUnavailableError,
    IssuedSession,
    Principal,
    ProviderAuthenticated,
    ProviderAuthenticationResult,
    ProviderEnrollmentAttemptsExhaustedError,
    ProviderEnrollmentInvalidOrExpiredError,
    ProviderEnrollmentRequired,
    ProviderEnrollmentResult,
    ProviderEnrollmentVerificationInvalidOrExpiredError,
    ProviderIdentityConflictError,
    ProviderLinkRequired,
    ProviderProofInvalidError,
    ProviderPurpose,
    ProviderReconciliationPendingError,
    ProviderReturnTarget,
    ProviderTransactionInvalidOrExpiredError,
    ProviderUnavailableError,
    ReauthenticationRequiredError,
    SignupResendCooldownError,
)
from dante.auth.email import EmailNormalizationError, NormalizedEmail, normalize_email
from dante.auth.email_delivery import (
    EmailDeliveryPort,
    EmailDispatchCapacityError,
    ProviderEnrollmentVerificationEmail,
)
from dante.auth.proofs import (
    FlowProofPurpose,
    ProviderEnrollmentOtpCodec,
    flow_proof_matches,
    flow_proof_verifier,
    issue_flow_proof,
)
from dante.auth.provider_flow import ProviderFlowLimiters
from dante.auth.sessions import (
    decode_session_secret,
    derive_csrf_token,
    generate_session_secret,
    session_secret_verifier,
    session_secret_verifier_from_raw,
)
from dante.platform.config.auth import AuthSettings
from dante.platform.config.auth_provider import APPLE_ISSUER
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

_PROVIDER_TRANSACTION_TTL = timedelta(minutes=15)
_PROVIDER_LINK_TTL = timedelta(minutes=15)
_PROVIDER_ENROLLMENT_TTL = timedelta(minutes=30)
_PROVIDER_ENROLLMENT_OTP_MAX_ATTEMPTS = 5
_PROVIDER_ENROLLMENT_OTP_MAX_TTL = timedelta(minutes=15)
_PROFILE_BOOTSTRAP_TTL = timedelta(days=30)
_PENDING_GRANT_TTL = timedelta(minutes=30)
_RECONCILE_BATCH = 32
_EMAIL_UNIQUENESS_CONSTRAINT = "uq_email_identity_comparison_key"
_EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT = "uq_external_identity_issuer_subject"
_APPLE_GRANT_UNIQUENESS_CONSTRAINT = "uq_apple_auth_grant_issuer_subject"


class AppleAuthorizationCancelledError(Exception):
    """The user cancelled the Apple authorization interaction."""


@dataclass(frozen=True, slots=True)
class _ClaimedAppleTransaction:
    ref: UUID
    expected_issuer: str
    purpose: ProviderPurpose
    nonce_verifier: bytes
    auth_session_ref: UUID | None
    auth_session_secret_verifier: bytes | None
    return_target: ProviderReturnTarget
    claimed_at: datetime


@dataclass(frozen=True, slots=True)
class _BoundSession:
    account_ref: UUID
    auth_session_ref: UUID
    authenticated_at: datetime
    recent_auth_at: datetime
    expires_at: datetime
    old_secret_verifier: bytes


@dataclass(frozen=True, slots=True)
class _EnrollmentSnapshot:
    external_signup_ref: UUID
    issuer: str
    subject: str
    provider_email_address: str | None
    provider_email_private: bool | None
    apple_auth_grant_ref: UUID
    email_address: str
    email_comparison_key: str
    bootstrap_display_name: str | None
    bootstrap_given_name: str | None
    bootstrap_family_name: str | None


@dataclass(frozen=True, slots=True)
class _PreparedGrant:
    grant_ref: UUID
    status_code: str
    external_identity_ref: UUID | None


class AppleFlowService:
    """Apple authentication, grant and notification state machine for canonical DANTE Auth."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings,
        token_verifier: AppleTokenVerifier,
        notification_verifier: AppleNotificationVerifier,
        protocol_client: AppleProtocolClient,
        grant_cipher: AppleGrantCipher,
        otp_codec: ProviderEnrollmentOtpCodec,
        email_delivery: EmailDeliveryPort,
        limiters: ProviderFlowLimiters,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._token_verifier = token_verifier
        self._notification_verifier = notification_verifier
        self._protocol_client = protocol_client
        self._grant_cipher = grant_cipher
        self._otp_codec = otp_codec
        self._email_delivery = email_delivery
        self._limiters = limiters
        self._csrf_key = settings.csrf_key_bytes

    async def begin_apple(
        self,
        *,
        purpose: ProviderPurpose,
        return_target: ProviderReturnTarget,
        source_context: str,
        admitted: AdmittedSession | None = None,
        presented_session_secret: str | None = None,
    ) -> AppleAuthenticationBegun:
        """Persist one exact Apple transaction before exposing provider capabilities."""
        if not self._settings.provider.apple.enabled:
            raise ProviderUnavailableError(retryable=False)
        await self._limiters.begin.consume(source_context, code="auth.provider_rate_limited")

        auth_session_ref: UUID | None = None
        auth_session_secret_verifier: bytes | None = None
        if purpose is ProviderPurpose.SIGN_IN:
            if admitted is not None or presented_session_secret is not None:
                raise ProviderTransactionInvalidOrExpiredError()
        else:
            if admitted is None or presented_session_secret is None:
                raise ProviderTransactionInvalidOrExpiredError()
            raw_secret = decode_session_secret(presented_session_secret)
            if raw_secret is None:
                raise ProviderTransactionInvalidOrExpiredError()
            auth_session_ref = admitted.principal.auth_session_ref
            auth_session_secret_verifier = session_secret_verifier_from_raw(raw_secret)
            if purpose is ProviderPurpose.LINK:
                self._require_recent_auth(admitted)
            await self._verify_begin_session(
                admitted=admitted,
                presented_session_verifier=auth_session_secret_verifier,
            )

        state = issue_flow_proof(FlowProofPurpose.PROVIDER_STATE)
        nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
        now = datetime.now(UTC)
        expires_at = now + _PROVIDER_TRANSACTION_TTL
        row = ExternalAuthTransactionRow(
            external_auth_transaction_ref=uuid7(),
            provider_code="apple",
            expected_issuer=APPLE_ISSUER,
            purpose_code=purpose.value,
            state_verifier=state.verifier,
            nonce_verifier=nonce.verifier,
            auth_session_ref=auth_session_ref,
            auth_session_secret_verifier=auth_session_secret_verifier,
            return_target_code=return_target.value,
            created_at=now,
            expires_at=expires_at,
            claimed_at=None,
        )
        await self._persist_transaction(row)
        try:
            authorization_url = build_apple_authorization_url(
                settings=self._settings.provider,
                state=state.secret.get_secret_value(),
                nonce=nonce.secret.get_secret_value(),
            )
        except (AppleProofError, AppleProviderUnavailableError) as exc:
            raise ProviderUnavailableError(retryable=False) from exc
        return AppleAuthenticationBegun(authorization_url=authorization_url, expires_at=expires_at)

    async def complete_apple(
        self,
        *,
        state: str,
        code: str | None,
        id_token: str | None,
        user: str | None,
        error: str | None,
        source_context: str,
    ) -> ProviderAuthenticationResult:
        """Claim state before the single-use exchange and converge on DANTE session truth."""
        await self._limiters.complete.consume(source_context, code="auth.provider_rate_limited")
        transaction = await self._claim_transaction(state)

        if error is not None:
            if error == "user_cancelled_authorize":
                raise AppleAuthorizationCancelledError()
            raise ProviderProofInvalidError()
        if code is None or id_token is None:
            raise ProviderProofInvalidError()

        try:
            front_evidence = await self._token_verifier.verify(
                id_token,
                expected_nonce_verifier=transaction.nonce_verifier,
                expected_code=code,
            )
            profile = parse_apple_authorization_profile(user)
            reconcile_apple_profile_email(evidence=front_evidence, profile=profile)
            tokens = await self._protocol_client.exchange_code(code)
            evidence = await self._token_verifier.verify(
                tokens.id_token,
                expected_nonce_verifier=transaction.nonce_verifier,
            )
            self._require_same_identity(front_evidence, evidence)
            reconcile_apple_profile_email(evidence=evidence, profile=profile)
        except AppleExchangeAmbiguousError as exc:
            raise ProviderReconciliationPendingError() from exc
        except (AppleProtocolError, AppleProofError) as exc:
            raise ProviderProofInvalidError() from exc
        except AppleProviderUnavailableError as exc:
            raise ProviderUnavailableError(retryable=True) from exc

        if transaction.expected_issuer != evidence.issuer:
            raise ProviderProofInvalidError()

        if transaction.purpose is ProviderPurpose.SIGN_IN:
            return await self._complete_sign_in(
                evidence=evidence,
                profile=profile,
                refresh_token=tokens.refresh_token,
            )
        if transaction.purpose is ProviderPurpose.LINK:
            return ProviderAuthenticated(
                session=await self._complete_authenticated_link(
                    transaction=transaction,
                    evidence=evidence,
                    refresh_token=tokens.refresh_token,
                )
            )
        if transaction.purpose is ProviderPurpose.REAUTHENTICATE:
            return ProviderAuthenticated(
                session=await self._complete_reauthentication(
                    transaction=transaction,
                    evidence=evidence,
                    refresh_token=tokens.refresh_token,
                )
            )
        raise AuthIntegrityError("stored Apple transaction has unknown purpose")

    async def inspect_provider_enrollment(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
    ) -> ProviderEnrollmentRequired:
        challenge = self._require_enrollment_challenge(
            await self._read_enrollment(external_signup_ref),
            continuation_secret=continuation_secret,
            now=datetime.now(UTC),
        )
        return self._enrollment_result(challenge, continuation_secret)

    async def set_provider_enrollment_email(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
        email: str,
        source_context: str,
    ) -> ProviderEnrollmentRequired:
        await self._limiters.enrollment.consume(source_context, code="auth.provider_rate_limited")
        normalized = self._normalize_enrollment_email(email)
        await self._limiters.enrollment.consume(
            normalized.comparison_key,
            code="auth.provider_rate_limited",
        )
        now = datetime.now(UTC)
        otp = self._otp_codec.issue(external_signup_ref)
        email_address: str | None = None
        verification_expires_at: datetime | None = None
        expires_at: datetime | None = None
        database_session = self._session_factory()
        try:
            await database_session.begin()
            challenge = self._require_enrollment_challenge(
                await database_session.scalar(
                    select(ExternalSignupChallengeRow)
                    .where(ExternalSignupChallengeRow.external_signup_ref == external_signup_ref)
                    .with_for_update()
                ),
                continuation_secret=continuation_secret,
                now=now,
            )
            if challenge.apple_auth_grant_ref is None:
                raise ProviderEnrollmentInvalidOrExpiredError()
            email_address = normalized.address
            expires_at = challenge.expires_at
            verification_expires_at = min(expires_at, now + self._provider_otp_ttl())
            challenge.email_address = normalized.address
            challenge.email_comparison_key = normalized.comparison_key
            challenge.otp_verifier = otp.verifier
            challenge.otp_key_id = otp.key_id
            challenge.verification_issued_at = now
            challenge.verification_expires_at = verification_expires_at
            challenge.failed_verification_attempts = 0
            challenge.updated_at = now
            await database_session.commit()
        except ProviderEnrollmentInvalidOrExpiredError:
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if email_address is None or expires_at is None or verification_expires_at is None:
            raise AuthIntegrityError("Apple enrollment email update lost challenge state")
        await self._enqueue_otp(
            email_address=email_address,
            code=otp.code,
            expires_at=verification_expires_at,
            now=now,
        )
        return ProviderEnrollmentRequired(
            external_signup_ref=external_signup_ref,
            continuation_secret=SecretStr(continuation_secret),
            expires_at=expires_at,
            email_address=email_address,
            verification_expires_at=verification_expires_at,
        )

    async def resend_provider_enrollment_verification(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
        source_context: str,
    ) -> ProviderEnrollmentRequired:
        await self._limiters.enrollment.consume(source_context, code="auth.provider_rate_limited")
        now = datetime.now(UTC)
        current = self._require_enrollment_challenge(
            await self._read_enrollment(external_signup_ref),
            continuation_secret=continuation_secret,
            now=now,
        )
        if current.email_comparison_key is None:
            raise ProviderEnrollmentInvalidOrExpiredError()
        await self._limiters.enrollment.consume(
            current.email_comparison_key,
            code="auth.provider_rate_limited",
        )

        otp = self._otp_codec.issue(external_signup_ref)
        email_address: str | None = None
        verification_expires_at: datetime | None = None
        expires_at: datetime | None = None
        database_session = self._session_factory()
        try:
            await database_session.begin()
            challenge = self._require_enrollment_challenge(
                await database_session.scalar(
                    select(ExternalSignupChallengeRow)
                    .where(ExternalSignupChallengeRow.external_signup_ref == external_signup_ref)
                    .with_for_update()
                ),
                continuation_secret=continuation_secret,
                now=now,
            )
            if challenge.email_address is None or challenge.verification_issued_at is None:
                raise ProviderEnrollmentInvalidOrExpiredError()
            cooldown_until = challenge.verification_issued_at + timedelta(
                seconds=self._settings.signup_resend_cooldown_seconds
            )
            if cooldown_until > now:
                raise SignupResendCooldownError(
                    max(1, math.ceil((cooldown_until - now).total_seconds()))
                )
            email_address = challenge.email_address
            expires_at = challenge.expires_at
            verification_expires_at = min(expires_at, now + self._provider_otp_ttl())
            challenge.otp_verifier = otp.verifier
            challenge.otp_key_id = otp.key_id
            challenge.verification_issued_at = now
            challenge.verification_expires_at = verification_expires_at
            challenge.failed_verification_attempts = 0
            challenge.updated_at = now
            await database_session.commit()
        except (ProviderEnrollmentInvalidOrExpiredError, SignupResendCooldownError):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if email_address is None or expires_at is None or verification_expires_at is None:
            raise AuthIntegrityError("Apple enrollment resend lost challenge state")
        await self._enqueue_otp(
            email_address=email_address,
            code=otp.code,
            expires_at=verification_expires_at,
            now=now,
        )
        return ProviderEnrollmentRequired(
            external_signup_ref=external_signup_ref,
            continuation_secret=SecretStr(continuation_secret),
            expires_at=expires_at,
            email_address=email_address,
            verification_expires_at=verification_expires_at,
        )

    async def verify_provider_enrollment(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
        code: str,
        source_context: str,
    ) -> ProviderEnrollmentResult:
        """Consume mailbox proof and atomically create Account or explicit link state."""
        await self._limiters.enrollment.consume(source_context, code="auth.provider_rate_limited")
        now = datetime.now(UTC)
        account_ref = uuid7()
        email_identity_ref = uuid7()
        external_identity_ref = uuid7()
        auth_session_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        session_expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        snapshot: _EnrollmentSnapshot | None = None
        link_result: ProviderLinkRequired | None = None
        ambiguous_commit = False

        database_session = self._session_factory()
        try:
            await database_session.begin()
            challenge = self._require_enrollment_challenge(
                await database_session.scalar(
                    select(ExternalSignupChallengeRow)
                    .where(ExternalSignupChallengeRow.external_signup_ref == external_signup_ref)
                    .with_for_update()
                ),
                continuation_secret=continuation_secret,
                now=now,
            )
            if (
                challenge.apple_auth_grant_ref is None
                or challenge.email_address is None
                or challenge.email_comparison_key is None
                or challenge.otp_verifier is None
                or challenge.otp_key_id is None
                or challenge.verification_expires_at is None
            ):
                raise ProviderEnrollmentInvalidOrExpiredError()
            if challenge.failed_verification_attempts >= _PROVIDER_ENROLLMENT_OTP_MAX_ATTEMPTS:
                raise ProviderEnrollmentAttemptsExhaustedError()
            if challenge.verification_expires_at <= now:
                raise ProviderEnrollmentVerificationInvalidOrExpiredError()
            if not self._otp_codec.matches(
                external_signup_ref=external_signup_ref,
                submitted_code=code,
                expected_verifier=challenge.otp_verifier,
                key_id=challenge.otp_key_id,
            ):
                challenge.failed_verification_attempts += 1
                challenge.updated_at = now
                exhausted = (
                    challenge.failed_verification_attempts >= _PROVIDER_ENROLLMENT_OTP_MAX_ATTEMPTS
                )
                await database_session.commit()
                if exhausted:
                    raise ProviderEnrollmentAttemptsExhaustedError()
                raise ProviderEnrollmentVerificationInvalidOrExpiredError()

            snapshot = self._snapshot(challenge)
            grant = await self._lock_pending_grant(
                database_session,
                grant_ref=snapshot.apple_auth_grant_ref,
                issuer=snapshot.issuer,
                subject=snapshot.subject,
                now=now,
            )
            collision = await database_session.scalar(
                select(EmailIdentityRow).where(
                    EmailIdentityRow.comparison_key == snapshot.email_comparison_key
                )
            )
            await self._delete_stale_link_challenge(
                database_session,
                issuer=snapshot.issuer,
                subject=snapshot.subject,
            )
            if collision is not None:
                link_result = self._stage_link_challenge(
                    database_session,
                    snapshot=snapshot,
                    target_email=collision,
                    now=now,
                )
            else:
                self._stage_account_core_from_enrollment(
                    database_session,
                    snapshot=snapshot,
                    account_ref=account_ref,
                    email_identity_ref=email_identity_ref,
                    external_identity_ref=external_identity_ref,
                    auth_session_ref=auth_session_ref,
                    secret_verifier=secret_verifier,
                    now=now,
                    expires_at=session_expires_at,
                )
                await database_session.flush()
                bootstrap = self._profile_bootstrap_from_snapshot(
                    account_ref=account_ref,
                    snapshot=snapshot,
                    now=now,
                )
                if bootstrap is not None:
                    database_session.add(bootstrap)
                self._activate_grant(grant, external_identity_ref=external_identity_ref, now=now)
            await database_session.delete(challenge)
            ambiguous_commit = await self._commit(database_session)
        except (
            ProviderEnrollmentInvalidOrExpiredError,
            ProviderEnrollmentAttemptsExhaustedError,
            ProviderEnrollmentVerificationInvalidOrExpiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if snapshot is None:
                raise AuthServiceUnavailableError(retryable=False) from exc
            return await self._resolve_enrollment_race(
                snapshot=snapshot,
                constraint=self._constraint_name(exc),
            )
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if snapshot is None:
            raise AuthIntegrityError("Apple enrollment completed without frozen state")
        if link_result is not None:
            if ambiguous_commit:
                await self._reconcile_link_commit(
                    result=link_result,
                    consumed_signup_ref=external_signup_ref,
                    grant_ref=snapshot.apple_auth_grant_ref,
                )
            return link_result
        if ambiguous_commit:
            await self._reconcile_new_account_commit(
                account_ref=account_ref,
                email_identity_ref=email_identity_ref,
                external_identity_ref=external_identity_ref,
                auth_session_ref=auth_session_ref,
                issuer=snapshot.issuer,
                subject=snapshot.subject,
                email_comparison_key=snapshot.email_comparison_key,
                secret_verifier=secret_verifier,
                created_at=now,
                expires_at=session_expires_at,
                grant_ref=snapshot.apple_auth_grant_ref,
                consumed_signup_ref=external_signup_ref,
            )
        return ProviderAuthenticated(
            session=self._issued_session(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=now,
                recent_auth_at=now,
                expires_at=session_expires_at,
                secret_verifier=secret_verifier,
                session_secret=session_secret,
            )
        )

    async def process_notification(self, token: str) -> bool:
        """Apply one verified Apple lifecycle notification idempotently."""
        try:
            event = await self._notification_verifier.verify_notification(token)
        except AppleProofError as exc:
            raise ProviderProofInvalidError() from exc
        except AppleProviderUnavailableError as exc:
            raise ProviderUnavailableError(retryable=True) from exc
        if not event.known:
            return False
        if event.event_type in {"email-disabled", "email-enabled"}:
            return await self._apply_email_event(event)
        return await self._apply_revocation_event(event)

    async def revoke_identity_and_grant(
        self,
        *,
        external_identity_ref: UUID,
        reason: str = "user_unlinked",
    ) -> None:
        """Disable locally first; remote revoke is reconciled only after durable proof."""
        if reason not in {"user_unlinked", "provider_revoked", "provider_account_deleted"}:
            raise ValueError("unsupported Apple revocation reason")
        grant_ref: UUID | None = None
        account_ref: UUID | None = None
        ambiguous_commit = False
        now = datetime.now(UTC)
        database_session = self._session_factory()
        try:
            await database_session.begin()
            identity = await database_session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.external_identity_ref == external_identity_ref,
                    ExternalIdentityRow.provider_code == "apple",
                )
            )
            if identity is None:
                raise ProviderProofInvalidError()
            account_ref = identity.account_ref
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(identity.account_ref))
            )
            identity = await database_session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.external_identity_ref == external_identity_ref,
                    ExternalIdentityRow.account_ref == account_ref,
                )
            )
            if identity is None:
                raise ProviderProofInvalidError()
            if identity.status_code != "revoked":
                identity.status_code = "revoked"
                identity.status_changed_at = now
                identity.revoked_at = now
                identity.revocation_reason_code = reason

            grant = await database_session.scalar(
                select(AppleAuthGrantRow)
                .where(AppleAuthGrantRow.external_identity_ref == external_identity_ref)
                .with_for_update()
            )
            if grant is not None and grant.status_code != "revoked":
                if grant.status_code != "revocation_pending":
                    grant.status_code = "revocation_pending"
                    grant.updated_at = now
                    grant.status_changed_at = now
                    grant.pending_expires_at = None
                    grant.revocation_requested_at = now
                grant_ref = grant.apple_auth_grant_ref
            ambiguous_commit = await self._commit(database_session)
        except ProviderProofInvalidError:
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if account_ref is None:
            raise AuthIntegrityError("Apple revoke lost Account binding")
        if ambiguous_commit:
            await self._reconcile_local_revocation(
                external_identity_ref=external_identity_ref,
                account_ref=account_ref,
                grant_ref=grant_ref,
            )
        if grant_ref is not None:
            await self._revoke_grant_remote(grant_ref)

    async def reconcile_expired_pending_grants(self) -> int:
        """Revoke expired pending grants and retry durable revocation_pending work."""
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                expired_refs = list(
                    (
                        await database_session.scalars(
                            select(AppleAuthGrantRow.apple_auth_grant_ref)
                            .where(
                                AppleAuthGrantRow.status_code == "pending",
                                AppleAuthGrantRow.pending_expires_at <= now,
                            )
                            .order_by(AppleAuthGrantRow.pending_expires_at)
                            .limit(_RECONCILE_BATCH)
                        )
                    ).all()
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

        for grant_ref in expired_refs:
            await self._mark_pending_grant_for_revoke(grant_ref)

        try:
            async with self._session_factory() as database_session, database_session.begin():
                revocation_refs = list(
                    (
                        await database_session.scalars(
                            select(AppleAuthGrantRow.apple_auth_grant_ref)
                            .where(AppleAuthGrantRow.status_code == "revocation_pending")
                            .order_by(
                                AppleAuthGrantRow.revocation_requested_at,
                                AppleAuthGrantRow.updated_at,
                            )
                            .limit(_RECONCILE_BATCH)
                        )
                    ).all()
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

        completed = 0
        for grant_ref in revocation_refs:
            try:
                await self._revoke_grant_remote(grant_ref)
            except ProviderReconciliationPendingError:
                continue
            completed += 1
        return completed

    async def _complete_sign_in(
        self,
        *,
        evidence: AppleIdentityEvidence,
        profile: AppleAuthorizationProfile | None,
        refresh_token: SecretStr,
    ) -> ProviderAuthenticationResult:
        existing = await self._read_external_identity(evidence.issuer, evidence.subject)
        if existing is not None:
            if existing.status_code == "active":
                return ProviderAuthenticated(
                    session=await self._sign_in_existing_identity(
                        identity=existing,
                        evidence=evidence,
                        refresh_token=refresh_token,
                    )
                )
            await self._stage_unaccepted_grant_for_revoke(
                identity=existing,
                evidence=evidence,
                refresh_token=refresh_token,
            )
            raise ProviderIdentityConflictError()

        prepared = await self._persist_signin_grant(
            evidence=evidence,
            refresh_token=refresh_token,
            allow_insert_race_retry=True,
        )
        if prepared.status_code == "active":
            identity = await self._read_external_identity_by_ref(prepared.external_identity_ref)
            if identity is None or identity.status_code != "active":
                raise ProviderReconciliationPendingError()
            return ProviderAuthenticated(
                session=await self._sign_in_existing_identity(
                    identity=identity,
                    evidence=evidence,
                    refresh_token=refresh_token,
                )
            )

        existing = await self._read_external_identity(evidence.issuer, evidence.subject)
        if existing is not None:
            if existing.status_code != "active":
                raise ProviderIdentityConflictError()
            return ProviderAuthenticated(
                session=await self._sign_in_existing_identity(
                    identity=existing,
                    evidence=evidence,
                    refresh_token=refresh_token,
                )
            )
        return await self._complete_new_identity_sign_in(
            evidence=evidence,
            profile=profile,
            grant_ref=prepared.grant_ref,
        )

    async def _complete_new_identity_sign_in(
        self,
        *,
        evidence: AppleIdentityEvidence,
        profile: AppleAuthorizationProfile | None,
        grant_ref: UUID,
    ) -> ProviderAuthenticationResult:
        effective_email = evidence.email or (profile.email if profile is not None else None)
        if evidence.mailbox_authoritative and evidence.email is not None:
            collision = await self._read_email_identity(evidence.email.comparison_key)
            if collision is not None:
                return await self._create_link_required(
                    evidence=evidence,
                    grant_ref=grant_ref,
                    target_email=collision,
                )
            return await self._create_account(
                evidence=evidence,
                profile=profile,
                grant_ref=grant_ref,
            )
        return await self._create_enrollment(
            evidence=evidence,
            profile=profile,
            grant_ref=grant_ref,
            email=effective_email,
        )

    async def _create_account(
        self,
        *,
        evidence: AppleIdentityEvidence,
        profile: AppleAuthorizationProfile | None,
        grant_ref: UUID,
    ) -> ProviderAuthenticationResult:
        if evidence.email is None or not evidence.mailbox_authoritative:
            raise AuthIntegrityError("Apple Account creation requires signed mailbox authority")
        account_ref = uuid7()
        email_ref = uuid7()
        identity_ref = uuid7()
        session_ref = uuid7()
        session_secret = generate_session_secret()
        verifier = session_secret_verifier(session_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            grant = await self._lock_pending_grant(
                database_session,
                grant_ref=grant_ref,
                issuer=evidence.issuer,
                subject=evidence.subject,
                now=now,
            )
            await self._delete_stale_challenges(database_session, evidence=evidence)
            database_session.add_all(
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
                        address=evidence.email.address,
                        comparison_key=evidence.email.comparison_key,
                        created_at=now,
                        verified_at=now,
                        recovery_restriction_code=None,
                        recovery_restriction_observed_at=None,
                    ),
                    self._new_identity_row(
                        identity_ref=identity_ref,
                        account_ref=account_ref,
                        email_ref=email_ref,
                        evidence=evidence,
                        now=now,
                    ),
                    self._new_session_row(
                        session_ref=session_ref,
                        account_ref=account_ref,
                        verifier=verifier,
                        now=now,
                        expires_at=expires_at,
                    ),
                ]
            )
            await database_session.flush()
            bootstrap = self._profile_bootstrap(account_ref=account_ref, profile=profile, now=now)
            if bootstrap is not None:
                database_session.add(bootstrap)
            self._activate_grant(grant, external_identity_ref=identity_ref, now=now)
            ambiguous_commit = await self._commit(database_session)
        except ProviderProofInvalidError:
            await self._safe_rollback(database_session)
            return await self._converge_active_grant(evidence=evidence, grant_ref=grant_ref)
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            return await self._resolve_account_race(
                evidence=evidence,
                grant_ref=grant_ref,
                constraint=self._constraint_name(exc),
            )
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            await self._reconcile_new_account_commit(
                account_ref=account_ref,
                email_identity_ref=email_ref,
                external_identity_ref=identity_ref,
                auth_session_ref=session_ref,
                issuer=evidence.issuer,
                subject=evidence.subject,
                email_comparison_key=evidence.email.comparison_key,
                secret_verifier=verifier,
                created_at=now,
                expires_at=expires_at,
                grant_ref=grant_ref,
                consumed_signup_ref=None,
            )
        return ProviderAuthenticated(
            session=self._issued_session(
                account_ref=account_ref,
                auth_session_ref=session_ref,
                authenticated_at=now,
                recent_auth_at=now,
                expires_at=expires_at,
                secret_verifier=verifier,
                session_secret=session_secret,
            )
        )

    async def _converge_active_grant(
        self,
        *,
        evidence: AppleIdentityEvidence,
        grant_ref: UUID,
    ) -> ProviderAuthenticationResult:
        grant = await self._read_grant_by_ref(grant_ref)
        identity = await self._read_external_identity(evidence.issuer, evidence.subject)
        if (
            grant is None
            or grant.status_code != "active"
            or grant.external_identity_ref is None
            or identity is None
            or identity.status_code != "active"
            or identity.external_identity_ref != grant.external_identity_ref
        ):
            raise ProviderReconciliationPendingError()
        return ProviderAuthenticated(
            session=await self._sign_in_existing_identity(
                identity=identity,
                evidence=evidence,
                refresh_token=self._decrypt_grant(grant),
            )
        )

    async def _sign_in_existing_identity(
        self,
        *,
        identity: ExternalIdentityRow,
        evidence: AppleIdentityEvidence,
        refresh_token: SecretStr,
    ) -> IssuedSession:
        session_ref = uuid7()
        session_secret = generate_session_secret()
        verifier = session_secret_verifier(session_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(identity.account_ref))
            )
            account = await database_session.scalar(
                select(AccountRow).where(AccountRow.account_ref == identity.account_ref)
            )
            current = await database_session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.external_identity_ref == identity.external_identity_ref,
                    ExternalIdentityRow.account_ref == identity.account_ref,
                    ExternalIdentityRow.issuer == evidence.issuer,
                    ExternalIdentityRow.subject == evidence.subject,
                )
            )
            if account is None or account.status_code != "active":
                raise AccountUnavailableError()
            if current is None or current.status_code != "active":
                raise ProviderProofInvalidError()
            self._refresh_identity(current, evidence=evidence, now=now)
            await self._upsert_active_grant(
                database_session,
                evidence=evidence,
                external_identity_ref=current.external_identity_ref,
                refresh_token=refresh_token,
                now=now,
            )
            await self._delete_stale_challenges(database_session, evidence=evidence)
            database_session.add(
                self._new_session_row(
                    session_ref=session_ref,
                    account_ref=current.account_ref,
                    verifier=verifier,
                    now=now,
                    expires_at=expires_at,
                )
            )
            ambiguous_commit = await self._commit(database_session)
        except (AccountUnavailableError, ProviderProofInvalidError, ProviderReconciliationPendingError):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            await self._reconcile_session_grant_commit(
                auth_session_ref=session_ref,
                account_ref=identity.account_ref,
                secret_verifier=verifier,
                created_at=now,
                expires_at=expires_at,
                issuer=evidence.issuer,
                subject=evidence.subject,
                external_identity_ref=identity.external_identity_ref,
            )
        return self._issued_session(
            account_ref=identity.account_ref,
            auth_session_ref=session_ref,
            authenticated_at=now,
            recent_auth_at=now,
            expires_at=expires_at,
            secret_verifier=verifier,
            session_secret=session_secret,
        )

    async def _complete_authenticated_link(
        self,
        *,
        transaction: _ClaimedAppleTransaction,
        evidence: AppleIdentityEvidence,
        refresh_token: SecretStr,
    ) -> IssuedSession:
        new_secret = generate_session_secret()
        new_verifier = session_secret_verifier(new_secret)
        now = datetime.now(UTC)
        bound: _BoundSession | None = None
        identity_ref: UUID | None = None
        ambiguous_commit = False
        same_account_identity_race = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            bound = await self._lock_bound_session(
                database_session,
                transaction=transaction,
                now=now,
                require_recent=True,
            )
            identity = await database_session.scalar(
                select(ExternalIdentityRow)
                .where(
                    ExternalIdentityRow.issuer == evidence.issuer,
                    ExternalIdentityRow.subject == evidence.subject,
                )
                .with_for_update()
            )
            if identity is not None and identity.account_ref != bound.account_ref:
                raise ProviderIdentityConflictError()
            email_ref = await self._same_account_email_ref(
                database_session,
                account_ref=bound.account_ref,
                evidence=evidence,
            )
            if identity is None:
                identity = self._new_identity_row(
                    identity_ref=uuid7(),
                    account_ref=bound.account_ref,
                    email_ref=email_ref,
                    evidence=evidence,
                    now=now,
                )
                database_session.add(identity)
                await database_session.flush()
            else:
                self._activate_identity(identity, evidence=evidence, email_ref=email_ref, now=now)
            identity_ref = identity.external_identity_ref
            await self._upsert_active_grant(
                database_session,
                evidence=evidence,
                external_identity_ref=identity.external_identity_ref,
                refresh_token=refresh_token,
                now=now,
            )
            await self._delete_stale_challenges(database_session, evidence=evidence)
            await self._rotate_bound_session(
                database_session,
                bound=bound,
                new_verifier=new_verifier,
                recent_auth_at=bound.recent_auth_at,
                expires_at=bound.expires_at,
                now=now,
            )
            ambiguous_commit = await self._commit(database_session)
        except (
            ProviderIdentityConflictError,
            ProviderTransactionInvalidOrExpiredError,
            ProviderReconciliationPendingError,
            ReauthenticationRequiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if bound is not None and self._constraint_name(exc) == _EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT:
                current = await self._read_external_identity(evidence.issuer, evidence.subject)
                if current is not None and current.account_ref == bound.account_ref:
                    same_account_identity_race = True
                else:
                    raise ProviderIdentityConflictError() from exc
            else:
                raise AuthServiceUnavailableError(retryable=False) from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if same_account_identity_race:
            return await self._complete_authenticated_link(
                transaction=transaction,
                evidence=evidence,
                refresh_token=refresh_token,
            )
        if bound is None or identity_ref is None:
            raise AuthIntegrityError("Apple link completed without bound durable state")
        if ambiguous_commit:
            await self._reconcile_rotated_session_grant(
                bound=bound,
                new_secret_verifier=new_verifier,
                recent_auth_at=bound.recent_auth_at,
                expires_at=bound.expires_at,
                issuer=evidence.issuer,
                subject=evidence.subject,
                external_identity_ref=identity_ref,
            )
        return self._issued_session(
            account_ref=bound.account_ref,
            auth_session_ref=bound.auth_session_ref,
            authenticated_at=bound.authenticated_at,
            recent_auth_at=bound.recent_auth_at,
            expires_at=bound.expires_at,
            secret_verifier=new_verifier,
            session_secret=new_secret,
        )

    async def _complete_reauthentication(
        self,
        *,
        transaction: _ClaimedAppleTransaction,
        evidence: AppleIdentityEvidence,
        refresh_token: SecretStr,
    ) -> IssuedSession:
        new_secret = generate_session_secret()
        new_verifier = session_secret_verifier(new_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        bound: _BoundSession | None = None
        identity_ref: UUID | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            bound = await self._lock_bound_session(
                database_session,
                transaction=transaction,
                now=now,
                require_recent=False,
            )
            identity = await database_session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.issuer == evidence.issuer,
                    ExternalIdentityRow.subject == evidence.subject,
                    ExternalIdentityRow.account_ref == bound.account_ref,
                    ExternalIdentityRow.status_code == "active",
                )
            )
            if identity is None:
                raise ProviderProofInvalidError()
            identity_ref = identity.external_identity_ref
            self._refresh_identity(identity, evidence=evidence, now=now)
            await self._upsert_active_grant(
                database_session,
                evidence=evidence,
                external_identity_ref=identity.external_identity_ref,
                refresh_token=refresh_token,
                now=now,
            )
            await self._delete_stale_challenges(database_session, evidence=evidence)
            await self._rotate_bound_session(
                database_session,
                bound=bound,
                new_verifier=new_verifier,
                recent_auth_at=now,
                expires_at=expires_at,
                now=now,
            )
            ambiguous_commit = await self._commit(database_session)
        except (
            ProviderProofInvalidError,
            ProviderReconciliationPendingError,
            ProviderTransactionInvalidOrExpiredError,
        ):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if bound is None or identity_ref is None:
            raise AuthIntegrityError("Apple reauthentication completed without bound durable state")
        if ambiguous_commit:
            await self._reconcile_rotated_session_grant(
                bound=bound,
                new_secret_verifier=new_verifier,
                recent_auth_at=now,
                expires_at=expires_at,
                issuer=evidence.issuer,
                subject=evidence.subject,
                external_identity_ref=identity_ref,
            )
        return self._issued_session(
            account_ref=bound.account_ref,
            auth_session_ref=bound.auth_session_ref,
            authenticated_at=bound.authenticated_at,
            recent_auth_at=now,
            expires_at=expires_at,
            secret_verifier=new_verifier,
            session_secret=new_secret,
        )

    async def _create_enrollment(
        self,
        *,
        evidence: AppleIdentityEvidence,
        profile: AppleAuthorizationProfile | None,
        grant_ref: UUID,
        email: NormalizedEmail | None,
    ) -> ProviderEnrollmentRequired:
        continuation = issue_flow_proof(FlowProofPurpose.PROVIDER_ENROLLMENT)
        signup_ref = uuid7()
        now = datetime.now(UTC)
        expires_at = now + _PROVIDER_ENROLLMENT_TTL
        otp = self._otp_codec.issue(signup_ref) if email is not None else None
        verification_expires_at = (
            min(expires_at, now + self._provider_otp_ttl()) if otp is not None else None
        )
        private = is_apple_private_email(email) if email is not None else None
        row = ExternalSignupChallengeRow(
            external_signup_ref=signup_ref,
            provider_code="apple",
            issuer=evidence.issuer,
            subject=evidence.subject,
            provider_email_address=(email.address if email is not None else None),
            provider_email_private=private,
            apple_auth_grant_ref=grant_ref,
            continuation_verifier=continuation.verifier,
            email_address=(email.address if email is not None else None),
            email_comparison_key=(email.comparison_key if email is not None else None),
            otp_verifier=(otp.verifier if otp is not None else None),
            otp_key_id=(otp.key_id if otp is not None else None),
            verification_issued_at=(now if otp is not None else None),
            verification_expires_at=verification_expires_at,
            failed_verification_attempts=0,
            bootstrap_display_name=(profile.display_name if profile is not None else None),
            bootstrap_given_name=(profile.given_name if profile is not None else None),
            bootstrap_family_name=(profile.family_name if profile is not None else None),
            bootstrap_picture_url=None,
            bootstrap_locale=None,
            created_at=now,
            updated_at=now,
            expires_at=expires_at,
        )
        await self._persist_enrollment(row)
        if otp is not None and email is not None and verification_expires_at is not None:
            await self._enqueue_otp(
                email_address=email.address,
                code=otp.code,
                expires_at=verification_expires_at,
                now=now,
            )
        return ProviderEnrollmentRequired(
            external_signup_ref=signup_ref,
            continuation_secret=continuation.secret,
            expires_at=expires_at,
            email_address=(email.address if email is not None else None),
            verification_expires_at=verification_expires_at,
        )

    async def _create_link_required(
        self,
        *,
        evidence: AppleIdentityEvidence,
        grant_ref: UUID,
        target_email: EmailIdentityRow,
    ) -> ProviderLinkRequired:
        continuation = issue_flow_proof(FlowProofPurpose.PROVIDER_LINK)
        now = datetime.now(UTC)
        expires_at = now + _PROVIDER_LINK_TTL
        row = ExternalLinkChallengeRow(
            external_link_challenge_ref=uuid7(),
            target_account_ref=target_email.account_ref,
            target_email_identity_ref=target_email.email_identity_ref,
            provider_code="apple",
            issuer=evidence.issuer,
            subject=evidence.subject,
            provider_email_address=(evidence.email.address if evidence.email is not None else None),
            provider_email_private=evidence.email_private,
            apple_auth_grant_ref=grant_ref,
            continuation_verifier=continuation.verifier,
            created_at=now,
            expires_at=expires_at,
        )
        await self._persist_link(row)
        return ProviderLinkRequired(
            external_link_challenge_ref=row.external_link_challenge_ref,
            continuation_secret=continuation.secret,
            expires_at=expires_at,
        )

    async def _persist_signin_grant(
        self,
        *,
        evidence: AppleIdentityEvidence,
        refresh_token: SecretStr,
        allow_insert_race_retry: bool,
    ) -> _PreparedGrant:
        now = datetime.now(UTC)
        ambiguous_commit = False
        intended_status: str | None = None
        intended_identity_ref: UUID | None = None
        encrypted: EncryptedAppleGrant | None = None
        grant_ref: UUID | None = None
        pending_expires_at: datetime | None = None
        database_session = self._session_factory()
        try:
            await database_session.begin()
            grant = await database_session.scalar(
                select(AppleAuthGrantRow)
                .where(
                    AppleAuthGrantRow.issuer == evidence.issuer,
                    AppleAuthGrantRow.subject == evidence.subject,
                )
                .with_for_update()
            )
            grant_ref = grant.apple_auth_grant_ref if grant is not None else uuid7()
            encrypted = self._encrypt_grant(
                refresh_token=refresh_token,
                grant_ref=grant_ref,
                subject=evidence.subject,
            )
            if grant is None:
                pending_expires_at = now + _PENDING_GRANT_TTL
                intended_status = "pending"
                database_session.add(
                    AppleAuthGrantRow(
                        apple_auth_grant_ref=grant_ref,
                        external_identity_ref=None,
                        issuer=evidence.issuer,
                        subject=evidence.subject,
                        client_id=self._apple_client_id(),
                        refresh_token_ciphertext=encrypted.ciphertext,
                        refresh_token_nonce=encrypted.nonce,
                        encryption_key_id=encrypted.key_id,
                        status_code="pending",
                        created_at=now,
                        updated_at=now,
                        status_changed_at=now,
                        pending_expires_at=pending_expires_at,
                        revocation_requested_at=None,
                        revoked_at=None,
                    )
                )
            elif grant.status_code == "pending":
                if grant.pending_expires_at is None or grant.pending_expires_at <= now:
                    raise ProviderReconciliationPendingError()
                intended_status = "pending"
                pending_expires_at = grant.pending_expires_at
                grant.client_id = self._apple_client_id()
                grant.refresh_token_ciphertext = encrypted.ciphertext
                grant.refresh_token_nonce = encrypted.nonce
                grant.encryption_key_id = encrypted.key_id
                grant.updated_at = now
            elif grant.status_code == "active":
                if grant.external_identity_ref is None:
                    raise AuthIntegrityError("active Apple grant lost ExternalIdentity binding")
                intended_status = "active"
                intended_identity_ref = grant.external_identity_ref
                grant.client_id = self._apple_client_id()
                grant.refresh_token_ciphertext = encrypted.ciphertext
                grant.refresh_token_nonce = encrypted.nonce
                grant.encryption_key_id = encrypted.key_id
                grant.updated_at = now
            elif grant.status_code in {"revocation_pending", "revoked"}:
                raise ProviderReconciliationPendingError()
            else:
                raise AuthIntegrityError("Apple grant has unknown status")
            ambiguous_commit = await self._commit(database_session)
        except ProviderReconciliationPendingError:
            await self._safe_rollback(database_session)
            raise
        except AppleGrantCryptoError as exc:
            await self._safe_rollback(database_session)
            raise AuthIntegrityError("Apple grant encryption failed") from exc
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if allow_insert_race_retry and self._constraint_name(exc) == _APPLE_GRANT_UNIQUENESS_CONSTRAINT:
                return await self._persist_signin_grant(
                    evidence=evidence,
                    refresh_token=refresh_token,
                    allow_insert_race_retry=False,
                )
            raise AuthServiceUnavailableError(retryable=False) from exc
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if grant_ref is None or intended_status is None or encrypted is None:
            raise AuthIntegrityError("Apple grant preparation lost frozen state")
        if ambiguous_commit:
            return await self._reconcile_grant_write(
                grant_ref=grant_ref,
                issuer=evidence.issuer,
                subject=evidence.subject,
                status_code=intended_status,
                external_identity_ref=intended_identity_ref,
                encrypted=encrypted,
                pending_expires_at=pending_expires_at,
            )
        return _PreparedGrant(
            grant_ref=grant_ref,
            status_code=intended_status,
            external_identity_ref=intended_identity_ref,
        )

    async def _stage_unaccepted_grant_for_revoke(
        self,
        *,
        identity: ExternalIdentityRow,
        evidence: AppleIdentityEvidence,
        refresh_token: SecretStr,
    ) -> None:
        now = datetime.now(UTC)
        grant_ref: UUID | None = None
        ambiguous = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            grant = await database_session.scalar(
                select(AppleAuthGrantRow)
                .where(
                    AppleAuthGrantRow.issuer == evidence.issuer,
                    AppleAuthGrantRow.subject == evidence.subject,
                )
                .with_for_update()
            )
            if grant is None:
                grant_ref = uuid7()
                encrypted = self._encrypt_grant(
                    refresh_token=refresh_token,
                    grant_ref=grant_ref,
                    subject=evidence.subject,
                )
                database_session.add(
                    AppleAuthGrantRow(
                        apple_auth_grant_ref=grant_ref,
                        external_identity_ref=identity.external_identity_ref,
                        issuer=evidence.issuer,
                        subject=evidence.subject,
                        client_id=self._apple_client_id(),
                        refresh_token_ciphertext=encrypted.ciphertext,
                        refresh_token_nonce=encrypted.nonce,
                        encryption_key_id=encrypted.key_id,
                        status_code="revocation_pending",
                        created_at=now,
                        updated_at=now,
                        status_changed_at=now,
                        pending_expires_at=None,
                        revocation_requested_at=now,
                        revoked_at=None,
                    )
                )
            elif grant.status_code == "active":
                raise AuthIntegrityError("revoked Apple identity unexpectedly owns active grant")
            else:
                grant_ref = grant.apple_auth_grant_ref
                encrypted = self._encrypt_grant(
                    refresh_token=refresh_token,
                    grant_ref=grant_ref,
                    subject=evidence.subject,
                )
                grant.external_identity_ref = identity.external_identity_ref
                grant.client_id = self._apple_client_id()
                grant.refresh_token_ciphertext = encrypted.ciphertext
                grant.refresh_token_nonce = encrypted.nonce
                grant.encryption_key_id = encrypted.key_id
                grant.status_code = "revocation_pending"
                grant.updated_at = now
                grant.status_changed_at = now
                grant.pending_expires_at = None
                grant.revocation_requested_at = now
                grant.revoked_at = None
            ambiguous = await self._commit(database_session)
        except AuthIntegrityError:
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if grant_ref is None:
            raise AuthIntegrityError("Apple rejected grant lost durable ref")
        if ambiguous:
            current = await self._read_grant_by_ref(grant_ref)
            if (
                current is None
                or current.status_code != "revocation_pending"
                or current.external_identity_ref != identity.external_identity_ref
            ):
                raise ProviderReconciliationPendingError()
        try:
            await self._revoke_grant_remote(grant_ref)
        except ProviderReconciliationPendingError:
            return

    async def _upsert_active_grant(
        self,
        database_session: AsyncSession,
        *,
        evidence: AppleIdentityEvidence,
        external_identity_ref: UUID,
        refresh_token: SecretStr,
        now: datetime,
    ) -> None:
        grant = await database_session.scalar(
            select(AppleAuthGrantRow)
            .where(
                AppleAuthGrantRow.issuer == evidence.issuer,
                AppleAuthGrantRow.subject == evidence.subject,
            )
            .with_for_update()
        )
        grant_ref = grant.apple_auth_grant_ref if grant is not None else uuid7()
        encrypted = self._encrypt_grant(
            refresh_token=refresh_token,
            grant_ref=grant_ref,
            subject=evidence.subject,
        )
        if grant is None:
            database_session.add(
                AppleAuthGrantRow(
                    apple_auth_grant_ref=grant_ref,
                    external_identity_ref=external_identity_ref,
                    issuer=evidence.issuer,
                    subject=evidence.subject,
                    client_id=self._apple_client_id(),
                    refresh_token_ciphertext=encrypted.ciphertext,
                    refresh_token_nonce=encrypted.nonce,
                    encryption_key_id=encrypted.key_id,
                    status_code="active",
                    created_at=now,
                    updated_at=now,
                    status_changed_at=now,
                    pending_expires_at=None,
                    revocation_requested_at=None,
                    revoked_at=None,
                )
            )
            return
        if grant.status_code == "revocation_pending":
            raise ProviderReconciliationPendingError()
        grant.external_identity_ref = external_identity_ref
        grant.client_id = self._apple_client_id()
        grant.refresh_token_ciphertext = encrypted.ciphertext
        grant.refresh_token_nonce = encrypted.nonce
        grant.encryption_key_id = encrypted.key_id
        if grant.status_code != "active":
            grant.status_code = "active"
            grant.status_changed_at = now
        grant.updated_at = now
        grant.pending_expires_at = None
        grant.revocation_requested_at = None
        grant.revoked_at = None

    async def _persist_transaction(self, row: ExternalAuthTransactionRow) -> None:
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            database_session.add(row)
            ambiguous_commit = await self._commit(database_session)
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()
        if ambiguous_commit:
            await self._reconcile_transaction_insert(row)

    async def _claim_transaction(self, state: str) -> _ClaimedAppleTransaction:
        verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.PROVIDER_STATE,
            encoded_secret=state,
        )
        if verifier is None:
            raise ProviderTransactionInvalidOrExpiredError()
        now = datetime.now(UTC)
        claimed: _ClaimedAppleTransaction | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            row = await database_session.scalar(
                select(ExternalAuthTransactionRow)
                .where(
                    ExternalAuthTransactionRow.provider_code == "apple",
                    ExternalAuthTransactionRow.state_verifier == verifier,
                )
                .with_for_update()
            )
            if (
                row is None
                or row.expected_issuer != APPLE_ISSUER
                or row.claimed_at is not None
                or row.expires_at <= now
            ):
                raise ProviderTransactionInvalidOrExpiredError()
            try:
                purpose = ProviderPurpose(row.purpose_code)
                return_target = ProviderReturnTarget(row.return_target_code)
            except ValueError as exc:
                raise AuthIntegrityError("stored Apple transaction vocabulary is invalid") from exc
            row.claimed_at = now
            claimed = _ClaimedAppleTransaction(
                ref=row.external_auth_transaction_ref,
                expected_issuer=row.expected_issuer,
                purpose=purpose,
                nonce_verifier=row.nonce_verifier,
                auth_session_ref=row.auth_session_ref,
                auth_session_secret_verifier=row.auth_session_secret_verifier,
                return_target=return_target,
                claimed_at=now,
            )
            ambiguous_commit = await self._commit(database_session)
        except (ProviderTransactionInvalidOrExpiredError, AuthIntegrityError):
            await self._safe_rollback(database_session)
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=False) from exc
        finally:
            await database_session.close()

        if claimed is None:
            raise AuthIntegrityError("Apple transaction claim lost frozen state")
        if ambiguous_commit:
            await self._reconcile_claim(claimed=claimed, state_verifier=verifier)
        return claimed

    async def _persist_enrollment(self, row: ExternalSignupChallengeRow) -> None:
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                delete(ExternalSignupChallengeRow).where(
                    ExternalSignupChallengeRow.issuer == row.issuer,
                    ExternalSignupChallengeRow.subject == row.subject,
                )
            )
            database_session.add(row)
            ambiguous_commit = await self._commit(database_session)
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()
        if ambiguous_commit:
            persisted = await self._read_enrollment(row.external_signup_ref)
            if not self._same_enrollment(persisted, row):
                raise ProviderReconciliationPendingError()

    async def _persist_link(self, row: ExternalLinkChallengeRow) -> None:
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                delete(ExternalLinkChallengeRow).where(
                    ExternalLinkChallengeRow.issuer == row.issuer,
                    ExternalLinkChallengeRow.subject == row.subject,
                )
            )
            database_session.add(row)
            ambiguous_commit = await self._commit(database_session)
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()
        if ambiguous_commit:
            await self._reconcile_link_row(row)

    async def _apply_email_event(self, event: AppleNotificationEvent) -> bool:
        if event.email is None:
            return False
        try:
            async with self._session_factory() as database_session, database_session.begin():
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.issuer == APPLE_ISSUER,
                        ExternalIdentityRow.subject == event.subject,
                    )
                )
                if identity is None or identity.email_identity_ref is None:
                    return False
                email = await database_session.scalar(
                    select(EmailIdentityRow)
                    .where(
                        EmailIdentityRow.email_identity_ref == identity.email_identity_ref,
                        EmailIdentityRow.account_ref == identity.account_ref,
                    )
                    .with_for_update()
                )
                if email is None or email.comparison_key != event.email.comparison_key:
                    return False
                observed = email.recovery_restriction_observed_at
                if observed is not None and observed >= event.event_time:
                    return True
                email.recovery_restriction_observed_at = event.event_time
                email.recovery_restriction_code = (
                    "provider_delivery_disabled" if event.event_type == "email-disabled" else None
                )
                return True
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _apply_revocation_event(self, event: AppleNotificationEvent) -> bool:
        reason = "provider_account_deleted" if event.event_type == "account-deleted" else "provider_revoked"
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.issuer == APPLE_ISSUER,
                        ExternalIdentityRow.subject == event.subject,
                    )
                )
                if identity is None:
                    return False
                await database_session.execute(
                    select(func.dante.acquire_account_security_lock(identity.account_ref))
                )
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == identity.external_identity_ref
                    )
                )
                if identity is None:
                    return False
                identity.status_code = "revoked"
                identity.status_changed_at = now
                identity.revoked_at = now
                identity.revocation_reason_code = reason
                grant = await database_session.scalar(
                    select(AppleAuthGrantRow)
                    .where(
                        AppleAuthGrantRow.issuer == APPLE_ISSUER,
                        AppleAuthGrantRow.subject == event.subject,
                    )
                    .with_for_update()
                )
                if grant is not None:
                    self._mark_grant_revoked(grant, now=now)
                return True
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _revoke_grant_remote(self, grant_ref: UUID) -> None:
        grant = await self._read_grant_by_ref(grant_ref)
        if grant is None or grant.status_code != "revocation_pending":
            return
        token = self._decrypt_grant(grant)
        try:
            await self._protocol_client.revoke_refresh_token(token)
        except (AppleProviderUnavailableError, AppleProtocolError) as exc:
            raise ProviderReconciliationPendingError() from exc

        now = datetime.now(UTC)
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            current = await database_session.scalar(
                select(AppleAuthGrantRow)
                .where(
                    AppleAuthGrantRow.apple_auth_grant_ref == grant_ref,
                    AppleAuthGrantRow.status_code == "revocation_pending",
                )
                .with_for_update()
            )
            if current is None:
                await database_session.rollback()
                return
            self._mark_grant_revoked(current, now=now)
            ambiguous_commit = await self._commit(database_session)
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise ProviderReconciliationPendingError() from exc
        finally:
            await database_session.close()
        if ambiguous_commit:
            persisted = await self._read_grant_by_ref(grant_ref)
            if not self._grant_is_revoked(persisted):
                raise ProviderReconciliationPendingError()

    async def _mark_pending_grant_for_revoke(self, grant_ref: UUID) -> bool:
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                grant = await database_session.scalar(
                    select(AppleAuthGrantRow)
                    .where(
                        AppleAuthGrantRow.apple_auth_grant_ref == grant_ref,
                        AppleAuthGrantRow.status_code == "pending",
                        AppleAuthGrantRow.pending_expires_at <= now,
                    )
                    .with_for_update()
                )
                if grant is None:
                    return False
                grant.status_code = "revocation_pending"
                grant.updated_at = now
                grant.status_changed_at = now
                grant.pending_expires_at = None
                grant.revocation_requested_at = now
                return True
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _resolve_account_race(
        self,
        *,
        evidence: AppleIdentityEvidence,
        grant_ref: UUID,
        constraint: str | None,
    ) -> ProviderAuthenticationResult:
        identity = await self._read_external_identity(evidence.issuer, evidence.subject)
        if constraint == _EMAIL_UNIQUENESS_CONSTRAINT and evidence.email is not None:
            collision = await self._read_email_identity(evidence.email.comparison_key)
            if collision is None:
                raise AuthServiceUnavailableError(retryable=True)
            if identity is None:
                return await self._create_link_required(
                    evidence=evidence,
                    grant_ref=grant_ref,
                    target_email=collision,
                )
            if identity.account_ref != collision.account_ref:
                raise ProviderIdentityConflictError()
            if identity.status_code == "active":
                grant = await self._read_grant_by_ref(grant_ref)
                if grant is None:
                    raise AuthServiceUnavailableError(retryable=True)
                return ProviderAuthenticated(
                    session=await self._sign_in_existing_identity(
                        identity=identity,
                        evidence=evidence,
                        refresh_token=self._decrypt_grant(grant),
                    )
                )
            raise ProviderIdentityConflictError()
        if constraint == _EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT and identity is not None:
            if identity.status_code == "active":
                grant = await self._read_grant_by_ref(grant_ref)
                if grant is None:
                    raise AuthServiceUnavailableError(retryable=True)
                return ProviderAuthenticated(
                    session=await self._sign_in_existing_identity(
                        identity=identity,
                        evidence=evidence,
                        refresh_token=self._decrypt_grant(grant),
                    )
                )
            raise ProviderIdentityConflictError()
        raise AuthServiceUnavailableError(retryable=False)

    async def _resolve_enrollment_race(
        self,
        *,
        snapshot: _EnrollmentSnapshot,
        constraint: str | None,
    ) -> ProviderEnrollmentResult:
        if constraint != _EMAIL_UNIQUENESS_CONSTRAINT:
            raise AuthServiceUnavailableError(retryable=False)
        collision = await self._read_email_identity(snapshot.email_comparison_key)
        if collision is None:
            raise AuthServiceUnavailableError(retryable=True)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                challenge = await database_session.scalar(
                    select(ExternalSignupChallengeRow)
                    .where(ExternalSignupChallengeRow.external_signup_ref == snapshot.external_signup_ref)
                    .with_for_update()
                )
                if challenge is None:
                    raise AuthServiceUnavailableError(retryable=True)
                await self._delete_stale_link_challenge(
                    database_session,
                    issuer=snapshot.issuer,
                    subject=snapshot.subject,
                )
                result = self._stage_link_challenge(
                    database_session,
                    snapshot=snapshot,
                    target_email=collision,
                    now=datetime.now(UTC),
                )
                await database_session.delete(challenge)
                return result
        except AuthServiceUnavailableError:
            raise
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    def _stage_account_core_from_enrollment(
        self,
        database_session: AsyncSession,
        *,
        snapshot: _EnrollmentSnapshot,
        account_ref: UUID,
        email_identity_ref: UUID,
        external_identity_ref: UUID,
        auth_session_ref: UUID,
        secret_verifier: bytes,
        now: datetime,
        expires_at: datetime,
    ) -> None:
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
                    address=snapshot.email_address,
                    comparison_key=snapshot.email_comparison_key,
                    created_at=now,
                    verified_at=now,
                    recovery_restriction_code=None,
                    recovery_restriction_observed_at=None,
                ),
                ExternalIdentityRow(
                    external_identity_ref=external_identity_ref,
                    account_ref=account_ref,
                    email_identity_ref=email_identity_ref,
                    provider_code="apple",
                    issuer=snapshot.issuer,
                    subject=snapshot.subject,
                    provider_email_address=snapshot.provider_email_address,
                    provider_email_private=snapshot.provider_email_private,
                    status_code="active",
                    created_at=now,
                    status_changed_at=now,
                    last_authenticated_at=now,
                    revoked_at=None,
                    revocation_reason_code=None,
                ),
                self._new_session_row(
                    session_ref=auth_session_ref,
                    account_ref=account_ref,
                    verifier=secret_verifier,
                    now=now,
                    expires_at=expires_at,
                ),
            ]
        )

    def _stage_link_challenge(
        self,
        database_session: AsyncSession,
        *,
        snapshot: _EnrollmentSnapshot,
        target_email: EmailIdentityRow,
        now: datetime,
    ) -> ProviderLinkRequired:
        continuation = issue_flow_proof(FlowProofPurpose.PROVIDER_LINK)
        link_ref = uuid7()
        expires_at = now + _PROVIDER_LINK_TTL
        database_session.add(
            ExternalLinkChallengeRow(
                external_link_challenge_ref=link_ref,
                target_account_ref=target_email.account_ref,
                target_email_identity_ref=target_email.email_identity_ref,
                provider_code="apple",
                issuer=snapshot.issuer,
                subject=snapshot.subject,
                provider_email_address=snapshot.provider_email_address,
                provider_email_private=snapshot.provider_email_private,
                apple_auth_grant_ref=snapshot.apple_auth_grant_ref,
                continuation_verifier=continuation.verifier,
                created_at=now,
                expires_at=expires_at,
            )
        )
        return ProviderLinkRequired(
            external_link_challenge_ref=link_ref,
            continuation_secret=continuation.secret,
            expires_at=expires_at,
        )

    async def _verify_begin_session(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_verifier: bytes,
    ) -> None:
        now = datetime.now(UTC)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == admitted.principal.auth_session_ref,
                        AuthSessionRow.account_ref == admitted.principal.account_ref,
                        AuthSessionRow.secret_verifier == presented_session_verifier,
                        AuthSessionRow.revoked_at.is_(None),
                        AuthSessionRow.expires_at > now,
                        AuthSessionRow.last_user_activity_at
                        > now - timedelta(seconds=self._settings.session_idle_timeout_seconds),
                    )
                )
                if row is None:
                    raise ProviderTransactionInvalidOrExpiredError()
        except ProviderTransactionInvalidOrExpiredError:
            raise
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _lock_bound_session(
        self,
        database_session: AsyncSession,
        *,
        transaction: _ClaimedAppleTransaction,
        now: datetime,
        require_recent: bool,
    ) -> _BoundSession:
        session_ref = transaction.auth_session_ref
        old_verifier = transaction.auth_session_secret_verifier
        if session_ref is None or old_verifier is None:
            raise ProviderTransactionInvalidOrExpiredError()
        initial = await database_session.scalar(
            select(AuthSessionRow).where(AuthSessionRow.auth_session_ref == session_ref)
        )
        if initial is None:
            raise ProviderTransactionInvalidOrExpiredError()
        await database_session.execute(
            select(func.dante.acquire_account_security_lock(initial.account_ref))
        )
        account = await database_session.scalar(
            select(AccountRow).where(AccountRow.account_ref == initial.account_ref)
        )
        current = await database_session.scalar(
            select(AuthSessionRow).where(
                AuthSessionRow.auth_session_ref == session_ref,
                AuthSessionRow.account_ref == initial.account_ref,
                AuthSessionRow.secret_verifier == old_verifier,
                AuthSessionRow.revoked_at.is_(None),
            )
        )
        if account is None or account.status_code != "active" or current is None:
            raise ProviderTransactionInvalidOrExpiredError()
        if current.expires_at <= now or current.last_user_activity_at <= now - timedelta(
            seconds=self._settings.session_idle_timeout_seconds
        ):
            raise ProviderTransactionInvalidOrExpiredError()
        if require_recent and current.recent_auth_at + timedelta(
            seconds=self._settings.recent_auth_window_seconds
        ) <= now:
            raise ReauthenticationRequiredError()
        return _BoundSession(
            account_ref=current.account_ref,
            auth_session_ref=current.auth_session_ref,
            authenticated_at=current.authenticated_at,
            recent_auth_at=current.recent_auth_at,
            expires_at=current.expires_at,
            old_secret_verifier=old_verifier,
        )

    async def _rotate_bound_session(
        self,
        database_session: AsyncSession,
        *,
        bound: _BoundSession,
        new_verifier: bytes,
        recent_auth_at: datetime,
        expires_at: datetime,
        now: datetime,
    ) -> None:
        rotated = await database_session.scalar(
            update(AuthSessionRow)
            .where(
                AuthSessionRow.auth_session_ref == bound.auth_session_ref,
                AuthSessionRow.account_ref == bound.account_ref,
                AuthSessionRow.secret_verifier == bound.old_secret_verifier,
                AuthSessionRow.revoked_at.is_(None),
                AuthSessionRow.expires_at > now,
            )
            .values(
                secret_verifier=new_verifier,
                recent_auth_at=recent_auth_at,
                last_user_activity_at=now,
                expires_at=expires_at,
            )
            .returning(AuthSessionRow.auth_session_ref)
        )
        if rotated is None:
            raise ProviderTransactionInvalidOrExpiredError()

    async def _lock_pending_grant(
        self,
        database_session: AsyncSession,
        *,
        grant_ref: UUID,
        issuer: str,
        subject: str,
        now: datetime,
    ) -> AppleAuthGrantRow:
        grant = await database_session.scalar(
            select(AppleAuthGrantRow)
            .where(
                AppleAuthGrantRow.apple_auth_grant_ref == grant_ref,
                AppleAuthGrantRow.issuer == issuer,
                AppleAuthGrantRow.subject == subject,
            )
            .with_for_update()
        )
        if (
            grant is None
            or grant.status_code != "pending"
            or grant.pending_expires_at is None
            or grant.pending_expires_at <= now
        ):
            raise ProviderProofInvalidError()
        return grant

    async def _delete_stale_challenges(
        self,
        database_session: AsyncSession,
        *,
        evidence: AppleIdentityEvidence,
    ) -> None:
        await self._delete_stale_link_challenge(
            database_session,
            issuer=evidence.issuer,
            subject=evidence.subject,
        )
        await database_session.execute(
            delete(ExternalSignupChallengeRow).where(
                ExternalSignupChallengeRow.issuer == evidence.issuer,
                ExternalSignupChallengeRow.subject == evidence.subject,
            )
        )

    @staticmethod
    async def _delete_stale_link_challenge(
        database_session: AsyncSession,
        *,
        issuer: str,
        subject: str,
    ) -> None:
        await database_session.execute(
            delete(ExternalLinkChallengeRow).where(
                ExternalLinkChallengeRow.issuer == issuer,
                ExternalLinkChallengeRow.subject == subject,
            )
        )

    async def _same_account_email_ref(
        self,
        database_session: AsyncSession,
        *,
        account_ref: UUID,
        evidence: AppleIdentityEvidence,
    ) -> UUID | None:
        if evidence.email is None:
            return None
        row = await database_session.scalar(
            select(EmailIdentityRow).where(
                EmailIdentityRow.account_ref == account_ref,
                EmailIdentityRow.comparison_key == evidence.email.comparison_key,
            )
        )
        return row.email_identity_ref if row is not None else None

    @staticmethod
    def _activate_grant(grant: AppleAuthGrantRow, *, external_identity_ref: UUID, now: datetime) -> None:
        grant.external_identity_ref = external_identity_ref
        grant.status_code = "active"
        grant.updated_at = now
        grant.status_changed_at = now
        grant.pending_expires_at = None
        grant.revocation_requested_at = None
        grant.revoked_at = None

    @staticmethod
    def _mark_grant_revoked(grant: AppleAuthGrantRow, *, now: datetime) -> None:
        grant.status_code = "revoked"
        grant.updated_at = now
        grant.status_changed_at = now
        grant.pending_expires_at = None
        grant.revocation_requested_at = grant.revocation_requested_at or now
        grant.revoked_at = now
        grant.refresh_token_ciphertext = None
        grant.refresh_token_nonce = None
        grant.encryption_key_id = None

    @staticmethod
    def _grant_is_revoked(grant: AppleAuthGrantRow | None) -> bool:
        return bool(
            grant is not None
            and grant.status_code == "revoked"
            and grant.revoked_at is not None
            and grant.refresh_token_ciphertext is None
            and grant.refresh_token_nonce is None
            and grant.encryption_key_id is None
        )

    @staticmethod
    def _new_identity_row(
        *,
        identity_ref: UUID,
        account_ref: UUID,
        email_ref: UUID | None,
        evidence: AppleIdentityEvidence,
        now: datetime,
    ) -> ExternalIdentityRow:
        return ExternalIdentityRow(
            external_identity_ref=identity_ref,
            account_ref=account_ref,
            email_identity_ref=email_ref,
            provider_code="apple",
            issuer=evidence.issuer,
            subject=evidence.subject,
            provider_email_address=(evidence.email.address if evidence.email is not None else None),
            provider_email_private=evidence.email_private,
            status_code="active",
            created_at=now,
            status_changed_at=now,
            last_authenticated_at=now,
            revoked_at=None,
            revocation_reason_code=None,
        )

    @staticmethod
    def _activate_identity(
        identity: ExternalIdentityRow,
        *,
        evidence: AppleIdentityEvidence,
        email_ref: UUID | None,
        now: datetime,
    ) -> None:
        identity.status_code = "active"
        identity.status_changed_at = now
        identity.revoked_at = None
        identity.revocation_reason_code = None
        if identity.email_identity_ref is None and email_ref is not None:
            identity.email_identity_ref = email_ref
        AppleFlowService._refresh_identity(identity, evidence=evidence, now=now)

    @staticmethod
    def _refresh_identity(
        identity: ExternalIdentityRow,
        *,
        evidence: AppleIdentityEvidence,
        now: datetime,
    ) -> None:
        if evidence.email is not None:
            identity.provider_email_address = evidence.email.address
            identity.provider_email_private = evidence.email_private
        identity.last_authenticated_at = now

    @staticmethod
    def _new_session_row(
        *,
        session_ref: UUID,
        account_ref: UUID,
        verifier: bytes,
        now: datetime,
        expires_at: datetime,
    ) -> AuthSessionRow:
        return AuthSessionRow(
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
    def _require_same_identity(
        front: AppleIdentityEvidence,
        exchanged: AppleIdentityEvidence,
    ) -> None:
        if front.issuer != exchanged.issuer or front.subject != exchanged.subject:
            raise AppleProofError("Apple front/back ID token identity mismatch")
        if (
            front.email is not None
            and exchanged.email is not None
            and front.email.comparison_key != exchanged.email.comparison_key
        ):
            raise AppleProofError("Apple front/back ID token email mismatch")

    @staticmethod
    def _snapshot(challenge: ExternalSignupChallengeRow) -> _EnrollmentSnapshot:
        if (
            challenge.apple_auth_grant_ref is None
            or challenge.email_address is None
            or challenge.email_comparison_key is None
        ):
            raise ProviderEnrollmentInvalidOrExpiredError()
        return _EnrollmentSnapshot(
            external_signup_ref=challenge.external_signup_ref,
            issuer=challenge.issuer,
            subject=challenge.subject,
            provider_email_address=challenge.provider_email_address,
            provider_email_private=challenge.provider_email_private,
            apple_auth_grant_ref=challenge.apple_auth_grant_ref,
            email_address=challenge.email_address,
            email_comparison_key=challenge.email_comparison_key,
            bootstrap_display_name=challenge.bootstrap_display_name,
            bootstrap_given_name=challenge.bootstrap_given_name,
            bootstrap_family_name=challenge.bootstrap_family_name,
        )

    @staticmethod
    def _profile_bootstrap(
        *,
        account_ref: UUID,
        profile: AppleAuthorizationProfile | None,
        now: datetime,
    ) -> AccountProfileBootstrapRow | None:
        if profile is None or not any((profile.display_name, profile.given_name, profile.family_name)):
            return None
        return AccountProfileBootstrapRow(
            account_ref=account_ref,
            source_provider_code="apple",
            source_issuer=APPLE_ISSUER,
            display_name=profile.display_name,
            given_name=profile.given_name,
            family_name=profile.family_name,
            picture_url=None,
            locale=None,
            created_at=now,
            expires_at=now + _PROFILE_BOOTSTRAP_TTL,
        )

    @staticmethod
    def _profile_bootstrap_from_snapshot(
        *,
        account_ref: UUID,
        snapshot: _EnrollmentSnapshot,
        now: datetime,
    ) -> AccountProfileBootstrapRow | None:
        if not any(
            (
                snapshot.bootstrap_display_name,
                snapshot.bootstrap_given_name,
                snapshot.bootstrap_family_name,
            )
        ):
            return None
        return AccountProfileBootstrapRow(
            account_ref=account_ref,
            source_provider_code="apple",
            source_issuer=APPLE_ISSUER,
            display_name=snapshot.bootstrap_display_name,
            given_name=snapshot.bootstrap_given_name,
            family_name=snapshot.bootstrap_family_name,
            picture_url=None,
            locale=None,
            created_at=now,
            expires_at=now + _PROFILE_BOOTSTRAP_TTL,
        )

    def _require_enrollment_challenge(
        self,
        challenge: ExternalSignupChallengeRow | None,
        *,
        continuation_secret: str,
        now: datetime,
    ) -> ExternalSignupChallengeRow:
        if (
            challenge is None
            or challenge.provider_code != "apple"
            or challenge.expires_at <= now
            or not flow_proof_matches(
                purpose=FlowProofPurpose.PROVIDER_ENROLLMENT,
                encoded_secret=continuation_secret,
                expected_verifier=challenge.continuation_verifier,
            )
        ):
            raise ProviderEnrollmentInvalidOrExpiredError()
        return challenge

    @staticmethod
    def _enrollment_result(
        challenge: ExternalSignupChallengeRow,
        continuation_secret: str,
    ) -> ProviderEnrollmentRequired:
        return ProviderEnrollmentRequired(
            external_signup_ref=challenge.external_signup_ref,
            continuation_secret=SecretStr(continuation_secret),
            expires_at=challenge.expires_at,
            email_address=challenge.email_address,
            verification_expires_at=challenge.verification_expires_at,
        )

    @staticmethod
    def _normalize_enrollment_email(email: str) -> NormalizedEmail:
        try:
            return normalize_email(email)
        except EmailNormalizationError as exc:
            raise AuthInputError(
                pointer="/email",
                code="invalid_format",
                detail="Enter a valid email address.",
            ) from exc

    async def _enqueue_otp(
        self,
        *,
        email_address: str,
        code: SecretStr,
        expires_at: datetime,
        now: datetime,
    ) -> None:
        remaining = max(1, math.ceil((expires_at - now).total_seconds() / 60))
        try:
            await self._email_delivery.enqueue(
                ProviderEnrollmentVerificationEmail(
                    to_address=email_address,
                    code=code,
                    expires_minutes=remaining,
                )
            )
        except EmailDispatchCapacityError as exc:
            raise EmailDeliveryUnavailableError() from exc

    def _provider_otp_ttl(self) -> timedelta:
        return min(
            timedelta(seconds=self._settings.signup_otp_lifetime_seconds),
            _PROVIDER_ENROLLMENT_OTP_MAX_TTL,
        )

    def _require_recent_auth(self, admitted: AdmittedSession) -> None:
        if admitted.principal.recent_auth_at + timedelta(
            seconds=self._settings.recent_auth_window_seconds
        ) <= datetime.now(UTC):
            raise ReauthenticationRequiredError()

    def _apple_client_id(self) -> str:
        client_id = self._settings.provider.apple.client_id
        if client_id is None:
            raise AuthIntegrityError("enabled Apple flow lost client_id")
        return client_id

    def _encrypt_grant(
        self,
        *,
        refresh_token: SecretStr,
        grant_ref: UUID,
        subject: str,
    ) -> EncryptedAppleGrant:
        try:
            return self._grant_cipher.encrypt(
                plaintext=refresh_token,
                grant_ref=grant_ref,
                subject=subject,
                client_id=self._apple_client_id(),
            )
        except AppleGrantCryptoError as exc:
            raise AuthIntegrityError("Apple grant encryption failed") from exc

    def _decrypt_grant(self, grant: AppleAuthGrantRow) -> SecretStr:
        if (
            grant.refresh_token_ciphertext is None
            or grant.refresh_token_nonce is None
            or grant.encryption_key_id is None
        ):
            raise AuthIntegrityError("Apple grant secret envelope is incomplete")
        try:
            return self._grant_cipher.decrypt(
                key_id=grant.encryption_key_id,
                nonce=grant.refresh_token_nonce,
                ciphertext=grant.refresh_token_ciphertext,
                grant_ref=grant.apple_auth_grant_ref,
                subject=grant.subject,
                client_id=grant.client_id,
            )
        except AppleGrantCryptoError as exc:
            raise AuthIntegrityError("Apple grant decryption failed") from exc

    async def _read_transaction(self, ref: UUID) -> ExternalAuthTransactionRow | None:
        try:
            async with self._session_factory() as session, session.begin():
                row: ExternalAuthTransactionRow | None = await session.scalar(
                    select(ExternalAuthTransactionRow).where(
                        ExternalAuthTransactionRow.external_auth_transaction_ref == ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

    async def _read_external_identity(self, issuer: str, subject: str) -> ExternalIdentityRow | None:
        try:
            async with self._session_factory() as session, session.begin():
                row: ExternalIdentityRow | None = await session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.issuer == issuer,
                        ExternalIdentityRow.subject == subject,
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_external_identity_by_ref(self, ref: UUID | None) -> ExternalIdentityRow | None:
        if ref is None:
            return None
        try:
            async with self._session_factory() as session, session.begin():
                row: ExternalIdentityRow | None = await session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_email_identity(self, comparison_key: str) -> EmailIdentityRow | None:
        try:
            async with self._session_factory() as session, session.begin():
                row: EmailIdentityRow | None = await session.scalar(
                    select(EmailIdentityRow).where(EmailIdentityRow.comparison_key == comparison_key)
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_enrollment(self, signup_ref: UUID) -> ExternalSignupChallengeRow | None:
        try:
            async with self._session_factory() as session, session.begin():
                row: ExternalSignupChallengeRow | None = await session.scalar(
                    select(ExternalSignupChallengeRow).where(
                        ExternalSignupChallengeRow.external_signup_ref == signup_ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_grant_by_ref(self, grant_ref: UUID) -> AppleAuthGrantRow | None:
        try:
            async with self._session_factory() as session, session.begin():
                row: AppleAuthGrantRow | None = await session.scalar(
                    select(AppleAuthGrantRow).where(
                        AppleAuthGrantRow.apple_auth_grant_ref == grant_ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _reconcile_transaction_insert(self, expected: ExternalAuthTransactionRow) -> None:
        persisted = await self._read_transaction(expected.external_auth_transaction_ref)
        if persisted is None or not self._same_transaction(persisted, expected, require_unclaimed=True):
            raise AuthServiceUnavailableError(retryable=False)

    async def _reconcile_claim(
        self,
        *,
        claimed: _ClaimedAppleTransaction,
        state_verifier: bytes,
    ) -> None:
        persisted = await self._read_transaction(claimed.ref)
        if (
            persisted is None
            or persisted.provider_code != "apple"
            or persisted.expected_issuer != claimed.expected_issuer
            or persisted.purpose_code != claimed.purpose.value
            or persisted.return_target_code != claimed.return_target.value
            or persisted.auth_session_ref != claimed.auth_session_ref
            or persisted.auth_session_secret_verifier != claimed.auth_session_secret_verifier
            or persisted.claimed_at != claimed.claimed_at
            or not hmac.compare_digest(persisted.state_verifier, state_verifier)
            or not hmac.compare_digest(persisted.nonce_verifier, claimed.nonce_verifier)
        ):
            raise AuthServiceUnavailableError(retryable=False)

    async def _reconcile_grant_write(
        self,
        *,
        grant_ref: UUID,
        issuer: str,
        subject: str,
        status_code: str,
        external_identity_ref: UUID | None,
        encrypted: EncryptedAppleGrant,
        pending_expires_at: datetime | None,
    ) -> _PreparedGrant:
        grant = await self._read_grant_by_ref(grant_ref)
        if grant is None or grant.issuer != issuer or grant.subject != subject:
            raise ProviderReconciliationPendingError()
        if grant.status_code == "active" and grant.external_identity_ref is not None:
            return _PreparedGrant(
                grant_ref=grant_ref,
                status_code="active",
                external_identity_ref=grant.external_identity_ref,
            )
        if (
            grant.status_code != status_code
            or grant.external_identity_ref != external_identity_ref
            or grant.client_id != self._apple_client_id()
            or grant.refresh_token_ciphertext != encrypted.ciphertext
            or grant.refresh_token_nonce != encrypted.nonce
            or grant.encryption_key_id != encrypted.key_id
            or grant.pending_expires_at != pending_expires_at
        ):
            raise ProviderReconciliationPendingError()
        return _PreparedGrant(
            grant_ref=grant_ref,
            status_code=status_code,
            external_identity_ref=external_identity_ref,
        )

    async def _reconcile_session_grant_commit(
        self,
        *,
        auth_session_ref: UUID,
        account_ref: UUID,
        secret_verifier: bytes,
        created_at: datetime,
        expires_at: datetime,
        issuer: str,
        subject: str,
        external_identity_ref: UUID,
    ) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                auth_session = await session.scalar(
                    select(AuthSessionRow).where(AuthSessionRow.auth_session_ref == auth_session_ref)
                )
                identity = await session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.account_ref == account_ref,
                        ExternalIdentityRow.issuer == issuer,
                        ExternalIdentityRow.subject == subject,
                    )
                )
                grant = await session.scalar(
                    select(AppleAuthGrantRow).where(
                        AppleAuthGrantRow.issuer == issuer,
                        AppleAuthGrantRow.subject == subject,
                    )
                )
        except SQLAlchemyError as exc:
            raise ProviderReconciliationPendingError() from exc
        if (
            auth_session is None
            or identity is None
            or identity.status_code != "active"
            or grant is None
            or grant.status_code != "active"
            or grant.external_identity_ref != external_identity_ref
            or auth_session.account_ref != account_ref
            or not hmac.compare_digest(auth_session.secret_verifier, secret_verifier)
            or auth_session.created_at != created_at
            or auth_session.expires_at != expires_at
            or auth_session.revoked_at is not None
        ):
            raise ProviderReconciliationPendingError()

    async def _reconcile_rotated_session_grant(
        self,
        *,
        bound: _BoundSession,
        new_secret_verifier: bytes,
        recent_auth_at: datetime,
        expires_at: datetime,
        issuer: str,
        subject: str,
        external_identity_ref: UUID,
    ) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                auth_session = await session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == bound.auth_session_ref,
                        AuthSessionRow.account_ref == bound.account_ref,
                    )
                )
                identity = await session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.account_ref == bound.account_ref,
                        ExternalIdentityRow.issuer == issuer,
                        ExternalIdentityRow.subject == subject,
                    )
                )
                grant = await session.scalar(
                    select(AppleAuthGrantRow).where(
                        AppleAuthGrantRow.issuer == issuer,
                        AppleAuthGrantRow.subject == subject,
                    )
                )
        except SQLAlchemyError as exc:
            raise ProviderReconciliationPendingError() from exc
        if (
            auth_session is None
            or identity is None
            or identity.status_code != "active"
            or grant is None
            or grant.status_code != "active"
            or grant.external_identity_ref != external_identity_ref
            or not hmac.compare_digest(auth_session.secret_verifier, new_secret_verifier)
            or auth_session.recent_auth_at != recent_auth_at
            or auth_session.expires_at != expires_at
            or auth_session.revoked_at is not None
        ):
            raise ProviderReconciliationPendingError()

    async def _reconcile_new_account_commit(
        self,
        *,
        account_ref: UUID,
        email_identity_ref: UUID,
        external_identity_ref: UUID,
        auth_session_ref: UUID,
        issuer: str,
        subject: str,
        email_comparison_key: str,
        secret_verifier: bytes,
        created_at: datetime,
        expires_at: datetime,
        grant_ref: UUID,
        consumed_signup_ref: UUID | None,
    ) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                account = await session.scalar(select(AccountRow).where(AccountRow.account_ref == account_ref))
                email = await session.scalar(
                    select(EmailIdentityRow).where(
                        EmailIdentityRow.email_identity_ref == email_identity_ref,
                        EmailIdentityRow.account_ref == account_ref,
                    )
                )
                identity = await session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.account_ref == account_ref,
                    )
                )
                auth_session = await session.scalar(
                    select(AuthSessionRow).where(AuthSessionRow.auth_session_ref == auth_session_ref)
                )
                grant = await session.scalar(
                    select(AppleAuthGrantRow).where(AppleAuthGrantRow.apple_auth_grant_ref == grant_ref)
                )
                pending = (
                    await session.scalar(
                        select(ExternalSignupChallengeRow.external_signup_ref).where(
                            ExternalSignupChallengeRow.external_signup_ref == consumed_signup_ref
                        )
                    )
                    if consumed_signup_ref is not None
                    else None
                )
        except SQLAlchemyError as exc:
            raise ProviderReconciliationPendingError() from exc
        if (
            account is None
            or account.status_code != "active"
            or email is None
            or email.comparison_key != email_comparison_key
            or identity is None
            or identity.issuer != issuer
            or identity.subject != subject
            or identity.status_code != "active"
            or auth_session is None
            or not hmac.compare_digest(auth_session.secret_verifier, secret_verifier)
            or auth_session.created_at != created_at
            or auth_session.expires_at != expires_at
            or grant is None
            or grant.status_code != "active"
            or grant.external_identity_ref != external_identity_ref
            or pending is not None
        ):
            raise ProviderReconciliationPendingError()

    async def _reconcile_link_commit(
        self,
        *,
        result: ProviderLinkRequired,
        consumed_signup_ref: UUID,
        grant_ref: UUID,
    ) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                link = await session.scalar(
                    select(ExternalLinkChallengeRow).where(
                        ExternalLinkChallengeRow.external_link_challenge_ref
                        == result.external_link_challenge_ref
                    )
                )
                pending = await session.scalar(
                    select(ExternalSignupChallengeRow.external_signup_ref).where(
                        ExternalSignupChallengeRow.external_signup_ref == consumed_signup_ref
                    )
                )
                grant = await session.scalar(
                    select(AppleAuthGrantRow).where(AppleAuthGrantRow.apple_auth_grant_ref == grant_ref)
                )
        except SQLAlchemyError as exc:
            raise ProviderReconciliationPendingError() from exc
        if (
            link is None
            or pending is not None
            or grant is None
            or grant.status_code != "pending"
            or link.apple_auth_grant_ref != grant_ref
            or not flow_proof_matches(
                purpose=FlowProofPurpose.PROVIDER_LINK,
                encoded_secret=result.continuation_secret.get_secret_value(),
                expected_verifier=link.continuation_verifier,
            )
        ):
            raise ProviderReconciliationPendingError()

    async def _reconcile_link_row(self, expected: ExternalLinkChallengeRow) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                row = await session.scalar(
                    select(ExternalLinkChallengeRow).where(
                        ExternalLinkChallengeRow.external_link_challenge_ref
                        == expected.external_link_challenge_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise ProviderReconciliationPendingError() from exc
        if (
            row is None
            or row.target_account_ref != expected.target_account_ref
            or row.target_email_identity_ref != expected.target_email_identity_ref
            or row.issuer != expected.issuer
            or row.subject != expected.subject
            or row.apple_auth_grant_ref != expected.apple_auth_grant_ref
            or row.expires_at != expected.expires_at
            or not hmac.compare_digest(row.continuation_verifier, expected.continuation_verifier)
        ):
            raise ProviderReconciliationPendingError()

    async def _reconcile_local_revocation(
        self,
        *,
        external_identity_ref: UUID,
        account_ref: UUID,
        grant_ref: UUID | None,
    ) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                identity = await session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.account_ref == account_ref,
                    )
                )
                grant = (
                    await session.scalar(
                        select(AppleAuthGrantRow).where(
                            AppleAuthGrantRow.apple_auth_grant_ref == grant_ref
                        )
                    )
                    if grant_ref is not None
                    else None
                )
        except SQLAlchemyError as exc:
            raise ProviderReconciliationPendingError() from exc
        if identity is None or identity.status_code != "revoked":
            raise ProviderReconciliationPendingError()
        if grant_ref is not None and (grant is None or grant.status_code != "revocation_pending"):
            raise ProviderReconciliationPendingError()

    @staticmethod
    def _same_transaction(
        persisted: ExternalAuthTransactionRow,
        expected: ExternalAuthTransactionRow,
        *,
        require_unclaimed: bool,
    ) -> bool:
        return (
            persisted.provider_code == expected.provider_code
            and persisted.expected_issuer == expected.expected_issuer
            and persisted.purpose_code == expected.purpose_code
            and hmac.compare_digest(persisted.state_verifier, expected.state_verifier)
            and hmac.compare_digest(persisted.nonce_verifier, expected.nonce_verifier)
            and persisted.auth_session_ref == expected.auth_session_ref
            and persisted.auth_session_secret_verifier == expected.auth_session_secret_verifier
            and persisted.return_target_code == expected.return_target_code
            and persisted.created_at == expected.created_at
            and persisted.expires_at == expected.expires_at
            and (not require_unclaimed or persisted.claimed_at is None)
        )

    @staticmethod
    def _same_enrollment(
        persisted: ExternalSignupChallengeRow | None,
        expected: ExternalSignupChallengeRow,
    ) -> bool:
        return bool(
            persisted is not None
            and persisted.provider_code == "apple"
            and persisted.issuer == expected.issuer
            and persisted.subject == expected.subject
            and persisted.apple_auth_grant_ref == expected.apple_auth_grant_ref
            and persisted.expires_at == expected.expires_at
            and hmac.compare_digest(
                persisted.continuation_verifier,
                expected.continuation_verifier,
            )
        )

    @staticmethod
    async def _commit(database_session: AsyncSession) -> bool:
        try:
            await database_session.commit()
            return False
        except DBAPIError as exc:
            if not exc.connection_invalidated:
                raise
            return True

    @staticmethod
    def _constraint_name(exc: IntegrityError) -> str | None:
        diagnostic = getattr(getattr(exc, "orig", None), "diag", None)
        value = getattr(diagnostic, "constraint_name", None)
        return value if isinstance(value, str) else None

    @staticmethod
    async def _safe_rollback(database_session: AsyncSession) -> None:
        if database_session.in_transaction():
            with suppress(SQLAlchemyError):
                await database_session.rollback()
