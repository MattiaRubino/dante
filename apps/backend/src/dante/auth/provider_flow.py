"""M5 provider application flow over canonical DANTE persistence/session authority."""

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
    ProviderAuthenticationBegun,
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
from dante.auth.google import (
    GoogleIdentityEvidence,
    GoogleProofError,
    GoogleProviderUnavailableError,
    GoogleTokenVerifier,
)
from dante.auth.lifecycle import KeyedRateLimiter
from dante.auth.proofs import (
    FlowProofPurpose,
    ProviderEnrollmentOtpCodec,
    flow_proof_matches,
    flow_proof_verifier,
    issue_flow_proof,
)
from dante.auth.sessions import (
    decode_session_secret,
    derive_csrf_token,
    generate_session_secret,
    session_secret_verifier,
    session_secret_verifier_from_raw,
)
from dante.platform.config.auth import AuthSettings
from dante.platform.config.auth_provider import GOOGLE_ISSUER
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

_PROVIDER_TRANSACTION_TTL = timedelta(minutes=15)
_PROVIDER_LINK_TTL = timedelta(minutes=15)
_PROVIDER_ENROLLMENT_TTL = timedelta(minutes=30)
_PROFILE_BOOTSTRAP_TTL = timedelta(days=30)
_PROVIDER_ENROLLMENT_OTP_MAX_ATTEMPTS = 5
_PROVIDER_ENROLLMENT_OTP_MAX_TTL = timedelta(minutes=15)
_EXPIRED_CLEANUP_BATCH = 128
_EMAIL_UNIQUENESS_CONSTRAINT = "uq_email_identity_comparison_key"
_EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT = "uq_external_identity_issuer_subject"


@dataclass(frozen=True, slots=True)
class ProviderFlowLimiters:
    """Bounded process-local ingress limits ahead of provider/database work."""

    begin: KeyedRateLimiter
    complete: KeyedRateLimiter
    enrollment: KeyedRateLimiter


@dataclass(frozen=True, slots=True)
class _ClaimedTransaction:
    ref: UUID
    purpose: ProviderPurpose
    expected_issuer: str
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
    provider_code: str
    issuer: str
    subject: str
    provider_email_address: str | None
    provider_email_private: bool | None
    continuation_verifier: bytes
    email_address: str
    email_comparison_key: str
    bootstrap_display_name: str | None
    bootstrap_given_name: str | None
    bootstrap_family_name: str | None
    bootstrap_picture_url: str | None
    bootstrap_locale: str | None


class ProviderFlowService:
    """Google provider state machine converging on DANTE Account/AuthSession truth."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings,
        google_verifier: GoogleTokenVerifier,
        otp_codec: ProviderEnrollmentOtpCodec,
        email_delivery: EmailDeliveryPort,
        limiters: ProviderFlowLimiters,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._google_verifier = google_verifier
        self._otp_codec = otp_codec
        self._email_delivery = email_delivery
        self._limiters = limiters
        self._csrf_key = settings.csrf_key_bytes

    async def begin_google(
        self,
        *,
        purpose: ProviderPurpose,
        return_target: ProviderReturnTarget,
        source_context: str,
        admitted: AdmittedSession | None = None,
        presented_session_secret: str | None = None,
    ) -> ProviderAuthenticationBegun:
        """Persist one short-lived Google transaction and return only transient capabilities."""
        if not self._settings.provider.google.enabled:
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
        transaction_ref = uuid7()
        now = datetime.now(UTC)
        expires_at = now + _PROVIDER_TRANSACTION_TTL
        row = ExternalAuthTransactionRow(
            external_auth_transaction_ref=transaction_ref,
            provider_code="google",
            expected_issuer=GOOGLE_ISSUER,
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
        await self._persist_provider_transaction(row)
        return ProviderAuthenticationBegun(
            external_auth_transaction_ref=transaction_ref,
            state=state.secret,
            nonce=nonce.secret,
            expires_at=expires_at,
        )

    async def complete_google(
        self,
        *,
        external_auth_transaction_ref: UUID,
        state: str,
        credential: str,
        source_context: str,
    ) -> ProviderAuthenticationResult:
        """Claim once, verify Google outside DB transaction, then resolve DANTE state."""
        await self._limiters.complete.consume(source_context, code="auth.provider_rate_limited")
        transaction = await self._claim_provider_transaction(
            external_auth_transaction_ref=external_auth_transaction_ref,
            state=state,
        )
        if transaction.expected_issuer != GOOGLE_ISSUER:
            raise ProviderTransactionInvalidOrExpiredError()

        try:
            evidence = await self._google_verifier.verify(
                credential,
                expected_nonce_verifier=transaction.nonce_verifier,
            )
        except GoogleProofError as exc:
            raise ProviderProofInvalidError() from exc
        except GoogleProviderUnavailableError as exc:
            raise ProviderUnavailableError(retryable=True) from exc

        if transaction.purpose is ProviderPurpose.SIGN_IN:
            return await self._complete_google_sign_in(evidence)
        if transaction.purpose is ProviderPurpose.LINK:
            session = await self._complete_google_link(transaction=transaction, evidence=evidence)
            return ProviderAuthenticated(session=session)
        if transaction.purpose is ProviderPurpose.REAUTHENTICATE:
            session = await self._complete_google_reauthentication(
                transaction=transaction,
                evidence=evidence,
            )
            return ProviderAuthenticated(session=session)
        raise AuthIntegrityError("stored provider transaction has unknown purpose")

    async def inspect_provider_enrollment(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
    ) -> ProviderEnrollmentRequired:
        """Resolve one provider enrollment without exposing provider identity internals."""
        now = datetime.now(UTC)
        challenge = self._require_enrollment_challenge(
            await self._read_provider_enrollment(external_signup_ref),
            continuation_secret=continuation_secret,
            now=now,
        )
        return ProviderEnrollmentRequired(
            external_signup_ref=challenge.external_signup_ref,
            continuation_secret=SecretStr(continuation_secret),
            expires_at=challenge.expires_at,
            email_address=challenge.email_address,
            verification_expires_at=challenge.verification_expires_at,
        )

    async def set_provider_enrollment_email(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
        email: str,
        source_context: str,
    ) -> ProviderEnrollmentRequired:
        """Set/replace the mailbox proof on one still-live provider enrollment."""
        await self._limiters.enrollment.consume(source_context, code="auth.provider_rate_limited")
        normalized = self._normalize_enrollment_email(email)
        await self._limiters.enrollment.consume(
            normalized.comparison_key,
            code="auth.provider_rate_limited",
        )
        otp = self._otp_codec.issue(external_signup_ref)
        now = datetime.now(UTC)
        expires_at: datetime | None = None
        verification_expires_at: datetime | None = None

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
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if expires_at is None or verification_expires_at is None:
            raise AuthIntegrityError("provider enrollment email update lost challenge timestamps")
        await self._enqueue_provider_otp(
            email_address=normalized.address,
            code=otp.code,
            expires_at=verification_expires_at,
            now=now,
        )
        return ProviderEnrollmentRequired(
            external_signup_ref=external_signup_ref,
            continuation_secret=SecretStr(continuation_secret),
            expires_at=expires_at,
            email_address=normalized.address,
            verification_expires_at=verification_expires_at,
        )

    async def resend_provider_enrollment_verification(
        self,
        *,
        external_signup_ref: UUID,
        continuation_secret: str,
        source_context: str,
    ) -> ProviderEnrollmentRequired:
        """Rotate provider-enrollment OTP after the governed resend cooldown."""
        await self._limiters.enrollment.consume(source_context, code="auth.provider_rate_limited")
        now = datetime.now(UTC)
        challenge = self._require_enrollment_challenge(
            await self._read_provider_enrollment(external_signup_ref),
            continuation_secret=continuation_secret,
            now=now,
        )
        if challenge.email_comparison_key is None:
            raise ProviderEnrollmentInvalidOrExpiredError()
        await self._limiters.enrollment.consume(
            challenge.email_comparison_key,
            code="auth.provider_rate_limited",
        )

        otp = self._otp_codec.issue(external_signup_ref)
        email_address: str | None = None
        expires_at: datetime | None = None
        verification_expires_at: datetime | None = None
        database_session = self._session_factory()
        try:
            await database_session.begin()
            locked = self._require_enrollment_challenge(
                await database_session.scalar(
                    select(ExternalSignupChallengeRow)
                    .where(ExternalSignupChallengeRow.external_signup_ref == external_signup_ref)
                    .with_for_update()
                ),
                continuation_secret=continuation_secret,
                now=now,
            )
            if locked.email_address is None or locked.verification_issued_at is None:
                await database_session.rollback()
                raise ProviderEnrollmentInvalidOrExpiredError()

            cooldown_until = locked.verification_issued_at + timedelta(
                seconds=self._settings.signup_resend_cooldown_seconds
            )
            if cooldown_until > now:
                await database_session.rollback()
                raise SignupResendCooldownError(
                    max(1, math.ceil((cooldown_until - now).total_seconds()))
                )

            email_address = locked.email_address
            expires_at = locked.expires_at
            verification_expires_at = min(expires_at, now + self._provider_otp_ttl())
            locked.otp_verifier = otp.verifier
            locked.otp_key_id = otp.key_id
            locked.verification_issued_at = now
            locked.verification_expires_at = verification_expires_at
            locked.failed_verification_attempts = 0
            locked.updated_at = now
            await database_session.commit()
        except ProviderEnrollmentInvalidOrExpiredError, SignupResendCooldownError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if email_address is None or expires_at is None or verification_expires_at is None:
            raise AuthIntegrityError("provider enrollment resend lost challenge state")
        await self._enqueue_provider_otp(
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
        """Consume mailbox proof and atomically create Account or typed link collision."""
        await self._limiters.enrollment.consume(source_context, code="auth.provider_rate_limited")
        now = datetime.now(UTC)
        account_ref = uuid7()
        email_identity_ref = uuid7()
        external_identity_ref = uuid7()
        auth_session_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
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
                challenge.email_address is None
                or challenge.email_comparison_key is None
                or challenge.otp_verifier is None
                or challenge.otp_key_id is None
                or challenge.verification_expires_at is None
                or challenge.verification_expires_at <= now
            ):
                await database_session.rollback()
                raise ProviderEnrollmentVerificationInvalidOrExpiredError()
            if challenge.failed_verification_attempts >= _PROVIDER_ENROLLMENT_OTP_MAX_ATTEMPTS:
                await database_session.rollback()
                raise ProviderEnrollmentAttemptsExhaustedError()

            if not self._otp_codec.matches(
                external_signup_ref=external_signup_ref,
                submitted_code=code,
                expected_verifier=challenge.otp_verifier,
                key_id=challenge.otp_key_id,
            ):
                challenge.failed_verification_attempts += 1
                challenge.updated_at = now
                exhausted = (
                    challenge.failed_verification_attempts
                    >= _PROVIDER_ENROLLMENT_OTP_MAX_ATTEMPTS
                )
                await database_session.commit()
                if exhausted:
                    raise ProviderEnrollmentAttemptsExhaustedError()
                raise ProviderEnrollmentVerificationInvalidOrExpiredError()

            snapshot = self._enrollment_snapshot(challenge)
            await self._delete_stale_link_challenge(
                database_session,
                issuer=snapshot.issuer,
                subject=snapshot.subject,
            )
            existing_email = await database_session.scalar(
                select(EmailIdentityRow).where(
                    EmailIdentityRow.comparison_key == snapshot.email_comparison_key
                )
            )
            if existing_email is not None:
                link_result = self._stage_link_from_enrollment(
                    database_session,
                    snapshot=snapshot,
                    target_email=existing_email,
                    now=now,
                )
            else:
                await self._stage_account_from_enrollment(
                    database_session,
                    snapshot=snapshot,
                    account_ref=account_ref,
                    email_identity_ref=email_identity_ref,
                    external_identity_ref=external_identity_ref,
                    auth_session_ref=auth_session_ref,
                    secret_verifier=secret_verifier,
                    now=now,
                    expires_at=expires_at,
                )
            await database_session.delete(challenge)

            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            ProviderEnrollmentAttemptsExhaustedError,
            ProviderEnrollmentInvalidOrExpiredError,
            ProviderEnrollmentVerificationInvalidOrExpiredError,
        ):
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if snapshot is None:
                raise AuthServiceUnavailableError(retryable=False) from exc
            return await self._resolve_enrollment_integrity_race(
                snapshot=snapshot,
                constraint_name=self._constraint_name(exc),
            )
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if snapshot is None:
            raise AuthIntegrityError("provider enrollment completed without frozen challenge state")
        if link_result is not None:
            if ambiguous_commit:
                await self._reconcile_link_commit(
                    result=link_result,
                    consumed_signup_ref=external_signup_ref,
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
                expires_at=expires_at,
                consumed_signup_ref=external_signup_ref,
            )
        return ProviderAuthenticated(
            session=self._issued_session(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=now,
                recent_auth_at=now,
                expires_at=expires_at,
                secret_verifier=secret_verifier,
                session_secret=session_secret,
            )
        )

    async def _complete_google_sign_in(
        self,
        evidence: GoogleIdentityEvidence,
    ) -> ProviderAuthenticationResult:
        existing = await self._read_external_identity(evidence.issuer, evidence.subject)
        if existing is not None:
            if existing.status_code == "active":
                session = await self._sign_in_existing_identity(existing.account_ref, evidence)
                return ProviderAuthenticated(session=session)
            return await self._link_required_for_bound_identity(existing, evidence)

        if evidence.email is None or not evidence.mailbox_authoritative:
            return await self._create_provider_enrollment(evidence)

        collision = await self._read_email_identity(evidence.email.comparison_key)
        if collision is not None:
            return await self._create_link_required(evidence=evidence, target_email=collision)
        return await self._create_google_account(evidence)

    async def _complete_google_link(
        self,
        *,
        transaction: _ClaimedTransaction,
        evidence: GoogleIdentityEvidence,
    ) -> IssuedSession:
        new_secret = generate_session_secret()
        new_verifier = session_secret_verifier(new_secret)
        now = datetime.now(UTC)
        bound: _BoundSession | None = None
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
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.issuer == evidence.issuer,
                    ExternalIdentityRow.subject == evidence.subject,
                )
            )
            if identity is not None and identity.account_ref != bound.account_ref:
                await database_session.rollback()
                raise ProviderIdentityConflictError()

            email_identity_ref = await self._same_account_email_ref(
                database_session,
                account_ref=bound.account_ref,
                evidence=evidence,
            )
            if identity is None:
                database_session.add(
                    ExternalIdentityRow(
                        external_identity_ref=uuid7(),
                        account_ref=bound.account_ref,
                        email_identity_ref=email_identity_ref,
                        provider_code="google",
                        issuer=evidence.issuer,
                        subject=evidence.subject,
                        provider_email_address=(
                            evidence.email.address if evidence.email is not None else None
                        ),
                        provider_email_private=(False if evidence.email is not None else None),
                        status_code="active",
                        created_at=now,
                        status_changed_at=now,
                        last_authenticated_at=now,
                        revoked_at=None,
                        revocation_reason_code=None,
                    )
                )
            else:
                self._activate_google_identity(
                    identity,
                    evidence=evidence,
                    email_identity_ref=email_identity_ref,
                    now=now,
                )

            await self._delete_stale_provider_challenges(
                database_session,
                issuer=evidence.issuer,
                subject=evidence.subject,
            )
            await self._rotate_bound_session(
                database_session,
                bound=bound,
                new_secret_verifier=new_verifier,
                recent_auth_at=bound.recent_auth_at,
                expires_at=bound.expires_at,
                now=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except (
            ProviderIdentityConflictError,
            ProviderTransactionInvalidOrExpiredError,
            ReauthenticationRequiredError,
        ):
            raise
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            if (
                bound is not None
                and self._constraint_name(exc) == _EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT
            ):
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
            return await self._complete_google_link(transaction=transaction, evidence=evidence)
        if bound is None:
            raise AuthIntegrityError("Google link completed without bound AuthSession")
        if ambiguous_commit:
            await self._reconcile_rotated_session(
                bound=bound,
                new_secret_verifier=new_verifier,
                recent_auth_at=bound.recent_auth_at,
                expires_at=bound.expires_at,
                evidence=evidence,
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

    async def _complete_google_reauthentication(
        self,
        *,
        transaction: _ClaimedTransaction,
        evidence: GoogleIdentityEvidence,
    ) -> IssuedSession:
        new_secret = generate_session_secret()
        new_verifier = session_secret_verifier(new_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        bound: _BoundSession | None = None
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
                )
            )
            if (
                identity is None
                or identity.account_ref != bound.account_ref
                or identity.status_code != "active"
            ):
                await database_session.rollback()
                raise ProviderProofInvalidError()

            self._refresh_google_identity_metadata(identity, evidence=evidence, now=now)
            await self._delete_stale_provider_challenges(
                database_session,
                issuer=evidence.issuer,
                subject=evidence.subject,
            )
            await self._rotate_bound_session(
                database_session,
                bound=bound,
                new_secret_verifier=new_verifier,
                recent_auth_at=now,
                expires_at=expires_at,
                now=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except ProviderProofInvalidError, ProviderTransactionInvalidOrExpiredError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if bound is None:
            raise AuthIntegrityError("Google reauthentication completed without bound AuthSession")
        if ambiguous_commit:
            await self._reconcile_rotated_session(
                bound=bound,
                new_secret_verifier=new_verifier,
                recent_auth_at=now,
                expires_at=expires_at,
                evidence=evidence,
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

    async def _sign_in_existing_identity(
        self,
        account_ref: UUID,
        evidence: GoogleIdentityEvidence,
    ) -> IssuedSession:
        auth_session_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await database_session.execute(
                select(func.dante.acquire_account_security_lock(account_ref))
            )
            account = await database_session.scalar(
                select(AccountRow).where(AccountRow.account_ref == account_ref)
            )
            identity = await database_session.scalar(
                select(ExternalIdentityRow).where(
                    ExternalIdentityRow.issuer == evidence.issuer,
                    ExternalIdentityRow.subject == evidence.subject,
                    ExternalIdentityRow.account_ref == account_ref,
                )
            )
            if account is None or account.status_code != "active":
                await database_session.rollback()
                raise AccountUnavailableError()
            if identity is None or identity.status_code != "active":
                await database_session.rollback()
                raise ProviderProofInvalidError()

            self._refresh_google_identity_metadata(identity, evidence=evidence, now=now)
            await self._delete_stale_provider_challenges(
                database_session,
                issuer=evidence.issuer,
                subject=evidence.subject,
            )
            database_session.add(
                self._new_session_row(
                    auth_session_ref=auth_session_ref,
                    account_ref=account_ref,
                    secret_verifier=secret_verifier,
                    now=now,
                    expires_at=expires_at,
                )
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except AccountUnavailableError, ProviderProofInvalidError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            await self._reconcile_session_commit(
                auth_session_ref=auth_session_ref,
                account_ref=account_ref,
                secret_verifier=secret_verifier,
                created_at=now,
                expires_at=expires_at,
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

    async def _create_google_account(
        self,
        evidence: GoogleIdentityEvidence,
    ) -> ProviderAuthenticationResult:
        if evidence.email is None or not evidence.mailbox_authoritative:
            raise AuthIntegrityError(
                "Google Account creation requires authoritative mailbox evidence"
            )

        account_ref = uuid7()
        email_identity_ref = uuid7()
        external_identity_ref = uuid7()
        auth_session_ref = uuid7()
        session_secret = generate_session_secret()
        secret_verifier = session_secret_verifier(session_secret)
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._settings.session_max_age_seconds)
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await self._delete_stale_provider_challenges(
                database_session,
                issuer=evidence.issuer,
                subject=evidence.subject,
            )
            await self._stage_google_account(
                database_session,
                evidence=evidence,
                account_ref=account_ref,
                email_identity_ref=email_identity_ref,
                external_identity_ref=external_identity_ref,
                auth_session_ref=auth_session_ref,
                secret_verifier=secret_verifier,
                now=now,
                expires_at=expires_at,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except IntegrityError as exc:
            await self._safe_rollback(database_session)
            return await self._resolve_google_account_integrity_race(
                evidence=evidence,
                constraint_name=self._constraint_name(exc),
            )
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if ambiguous_commit:
            await self._reconcile_new_account_commit(
                account_ref=account_ref,
                email_identity_ref=email_identity_ref,
                external_identity_ref=external_identity_ref,
                auth_session_ref=auth_session_ref,
                issuer=evidence.issuer,
                subject=evidence.subject,
                email_comparison_key=evidence.email.comparison_key,
                secret_verifier=secret_verifier,
                created_at=now,
                expires_at=expires_at,
                consumed_signup_ref=None,
            )
        return ProviderAuthenticated(
            session=self._issued_session(
                account_ref=account_ref,
                auth_session_ref=auth_session_ref,
                authenticated_at=now,
                recent_auth_at=now,
                expires_at=expires_at,
                secret_verifier=secret_verifier,
                session_secret=session_secret,
            )
        )

    async def _resolve_google_account_integrity_race(
        self,
        *,
        evidence: GoogleIdentityEvidence,
        constraint_name: str | None,
    ) -> ProviderAuthenticationResult:
        if evidence.email is None:
            raise AuthServiceUnavailableError(retryable=False)

        identity = await self._read_external_identity(evidence.issuer, evidence.subject)
        if constraint_name == _EMAIL_UNIQUENESS_CONSTRAINT:
            collision = await self._read_email_identity(evidence.email.comparison_key)
            if collision is None:
                raise AuthServiceUnavailableError(retryable=True)
            if identity is None:
                return await self._create_link_required(evidence=evidence, target_email=collision)
            if identity.account_ref != collision.account_ref:
                raise ProviderIdentityConflictError()
            if identity.status_code == "active":
                session = await self._sign_in_existing_identity(identity.account_ref, evidence)
                return ProviderAuthenticated(session=session)
            return await self._link_required_for_bound_identity(identity, evidence)

        if constraint_name == _EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT:
            if identity is None:
                raise AuthServiceUnavailableError(retryable=True)
            if identity.status_code == "active":
                session = await self._sign_in_existing_identity(identity.account_ref, evidence)
                return ProviderAuthenticated(session=session)
            return await self._link_required_for_bound_identity(identity, evidence)

        raise AuthServiceUnavailableError(retryable=False)

    async def _create_provider_enrollment(
        self,
        evidence: GoogleIdentityEvidence,
    ) -> ProviderEnrollmentRequired:
        continuation = issue_flow_proof(FlowProofPurpose.PROVIDER_ENROLLMENT)
        external_signup_ref = uuid7()
        now = datetime.now(UTC)
        expires_at = now + _PROVIDER_ENROLLMENT_TTL
        otp = self._otp_codec.issue(external_signup_ref) if evidence.email is not None else None
        verification_expires_at = (
            min(expires_at, now + self._provider_otp_ttl()) if otp is not None else None
        )
        row = ExternalSignupChallengeRow(
            external_signup_ref=external_signup_ref,
            provider_code="google",
            issuer=evidence.issuer,
            subject=evidence.subject,
            provider_email_address=(evidence.email.address if evidence.email is not None else None),
            provider_email_private=(False if evidence.email is not None else None),
            apple_auth_grant_ref=None,
            continuation_verifier=continuation.verifier,
            email_address=(evidence.email.address if evidence.email is not None else None),
            email_comparison_key=(
                evidence.email.comparison_key if evidence.email is not None else None
            ),
            otp_verifier=(otp.verifier if otp is not None else None),
            otp_key_id=(otp.key_id if otp is not None else None),
            verification_issued_at=(now if otp is not None else None),
            verification_expires_at=verification_expires_at,
            failed_verification_attempts=0,
            bootstrap_display_name=evidence.display_name,
            bootstrap_given_name=evidence.given_name,
            bootstrap_family_name=evidence.family_name,
            bootstrap_picture_url=evidence.picture_url,
            bootstrap_locale=evidence.locale,
            created_at=now,
            updated_at=now,
            expires_at=expires_at,
        )
        await self._persist_provider_enrollment(row)
        if otp is not None and evidence.email is not None and verification_expires_at is not None:
            await self._enqueue_provider_otp(
                email_address=evidence.email.address,
                code=otp.code,
                expires_at=verification_expires_at,
                now=now,
            )
        return ProviderEnrollmentRequired(
            external_signup_ref=external_signup_ref,
            continuation_secret=continuation.secret,
            expires_at=expires_at,
            email_address=(evidence.email.address if evidence.email is not None else None),
            verification_expires_at=verification_expires_at,
        )

    async def _create_link_required(
        self,
        *,
        evidence: GoogleIdentityEvidence,
        target_email: EmailIdentityRow,
    ) -> ProviderLinkRequired:
        continuation = issue_flow_proof(FlowProofPurpose.PROVIDER_LINK)
        link_ref = uuid7()
        now = datetime.now(UTC)
        expires_at = now + _PROVIDER_LINK_TTL
        row = ExternalLinkChallengeRow(
            external_link_challenge_ref=link_ref,
            target_account_ref=target_email.account_ref,
            target_email_identity_ref=target_email.email_identity_ref,
            provider_code="google",
            issuer=evidence.issuer,
            subject=evidence.subject,
            provider_email_address=(evidence.email.address if evidence.email is not None else None),
            provider_email_private=(False if evidence.email is not None else None),
            apple_auth_grant_ref=None,
            continuation_verifier=continuation.verifier,
            created_at=now,
            expires_at=expires_at,
        )
        await self._persist_link_challenge(row)
        return ProviderLinkRequired(
            external_link_challenge_ref=link_ref,
            continuation_secret=continuation.secret,
            expires_at=expires_at,
        )

    async def _link_required_for_bound_identity(
        self,
        identity: ExternalIdentityRow,
        evidence: GoogleIdentityEvidence,
    ) -> ProviderLinkRequired:
        target_email: EmailIdentityRow | None = None
        if identity.email_identity_ref is not None:
            target_email = await self._read_email_identity_by_ref(
                identity.email_identity_ref,
                identity.account_ref,
            )
        if target_email is None and evidence.email is not None:
            candidate = await self._read_email_identity(evidence.email.comparison_key)
            if candidate is not None and candidate.account_ref == identity.account_ref:
                target_email = candidate
        if target_email is None:
            raise ProviderIdentityConflictError()
        return await self._create_link_required(evidence=evidence, target_email=target_email)

    async def _persist_provider_transaction(self, row: ExternalAuthTransactionRow) -> None:
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await self._cleanup_expired(database_session, now=row.created_at)
            database_session.add(row)
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
            return
        persisted = await self._read_provider_transaction(row.external_auth_transaction_ref)
        if persisted is None or not self._same_provider_transaction(persisted, row):
            raise AuthServiceUnavailableError(retryable=False)

    async def _claim_provider_transaction(
        self,
        *,
        external_auth_transaction_ref: UUID,
        state: str,
    ) -> _ClaimedTransaction:
        state_verifier = flow_proof_verifier(
            purpose=FlowProofPurpose.PROVIDER_STATE,
            encoded_secret=state,
        )
        if state_verifier is None:
            raise ProviderTransactionInvalidOrExpiredError()

        now = datetime.now(UTC)
        claimed: _ClaimedTransaction | None = None
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            row = await database_session.scalar(
                select(ExternalAuthTransactionRow)
                .where(
                    ExternalAuthTransactionRow.external_auth_transaction_ref
                    == external_auth_transaction_ref
                )
                .with_for_update()
            )
            if (
                row is None
                or row.provider_code != "google"
                or row.claimed_at is not None
                or row.expires_at <= now
                or not hmac.compare_digest(row.state_verifier, state_verifier)
            ):
                await database_session.rollback()
                raise ProviderTransactionInvalidOrExpiredError()
            try:
                purpose = ProviderPurpose(row.purpose_code)
                return_target = ProviderReturnTarget(row.return_target_code)
            except ValueError as exc:
                await database_session.rollback()
                raise AuthIntegrityError(
                    "stored provider transaction vocabulary is invalid"
                ) from exc

            row.claimed_at = now
            claimed = _ClaimedTransaction(
                ref=row.external_auth_transaction_ref,
                purpose=purpose,
                expected_issuer=row.expected_issuer,
                nonce_verifier=row.nonce_verifier,
                auth_session_ref=row.auth_session_ref,
                auth_session_secret_verifier=row.auth_session_secret_verifier,
                return_target=return_target,
                claimed_at=now,
            )
            try:
                await database_session.commit()
            except DBAPIError as exc:
                if not exc.connection_invalidated:
                    raise
                ambiguous_commit = True
        except ProviderTransactionInvalidOrExpiredError, AuthIntegrityError:
            raise
        except SQLAlchemyError as exc:
            await self._safe_rollback(database_session)
            raise AuthServiceUnavailableError(retryable=True) from exc
        finally:
            await database_session.close()

        if claimed is None:
            raise AuthIntegrityError("provider transaction claim lost frozen state")
        if ambiguous_commit:
            await self._reconcile_provider_claim(
                claimed=claimed,
                state_verifier=state_verifier,
            )
        return claimed

    async def _reconcile_provider_claim(
        self,
        *,
        claimed: _ClaimedTransaction,
        state_verifier: bytes,
    ) -> None:
        persisted = await self._read_provider_transaction(claimed.ref)
        if (
            persisted is None
            or persisted.provider_code != "google"
            or persisted.claimed_at != claimed.claimed_at
            or not hmac.compare_digest(persisted.state_verifier, state_verifier)
            or not hmac.compare_digest(persisted.nonce_verifier, claimed.nonce_verifier)
            or persisted.expected_issuer != claimed.expected_issuer
            or persisted.purpose_code != claimed.purpose.value
            or persisted.auth_session_ref != claimed.auth_session_ref
            or persisted.auth_session_secret_verifier != claimed.auth_session_secret_verifier
            or persisted.return_target_code != claimed.return_target.value
        ):
            raise AuthServiceUnavailableError(retryable=False)

    async def _persist_provider_enrollment(self, row: ExternalSignupChallengeRow) -> None:
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await self._cleanup_expired(database_session, now=row.created_at)
            await database_session.execute(
                delete(ExternalSignupChallengeRow).where(
                    ExternalSignupChallengeRow.issuer == row.issuer,
                    ExternalSignupChallengeRow.subject == row.subject,
                )
            )
            database_session.add(row)
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
            return
        persisted = await self._read_provider_enrollment(row.external_signup_ref)
        if (
            persisted is None
            or persisted.issuer != row.issuer
            or persisted.subject != row.subject
            or not hmac.compare_digest(
                persisted.continuation_verifier,
                row.continuation_verifier,
            )
        ):
            raise AuthServiceUnavailableError(retryable=False)

    async def _persist_link_challenge(self, row: ExternalLinkChallengeRow) -> None:
        ambiguous_commit = False
        database_session = self._session_factory()
        try:
            await database_session.begin()
            await self._cleanup_expired(database_session, now=row.created_at)
            await database_session.execute(
                delete(ExternalLinkChallengeRow).where(
                    ExternalLinkChallengeRow.issuer == row.issuer,
                    ExternalLinkChallengeRow.subject == row.subject,
                )
            )
            database_session.add(row)
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

        if ambiguous_commit:
            await self._reconcile_link_row(row)

    async def _verify_begin_session(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_verifier: bytes,
    ) -> None:
        now = datetime.now(UTC)
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
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
        transaction: _ClaimedTransaction,
        now: datetime,
        require_recent: bool,
    ) -> _BoundSession:
        auth_session_ref = transaction.auth_session_ref
        old_secret_verifier = transaction.auth_session_secret_verifier
        if auth_session_ref is None or old_secret_verifier is None:
            raise ProviderTransactionInvalidOrExpiredError()

        initial = await database_session.scalar(
            select(AuthSessionRow).where(AuthSessionRow.auth_session_ref == auth_session_ref)
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
                AuthSessionRow.auth_session_ref == auth_session_ref,
                AuthSessionRow.account_ref == initial.account_ref,
                AuthSessionRow.secret_verifier == old_secret_verifier,
                AuthSessionRow.revoked_at.is_(None),
            )
        )
        if account is None or account.status_code != "active" or current is None:
            raise ProviderTransactionInvalidOrExpiredError()
        if current.expires_at <= now or current.last_user_activity_at <= now - timedelta(
            seconds=self._settings.session_idle_timeout_seconds
        ):
            raise ProviderTransactionInvalidOrExpiredError()
        if require_recent and (
            current.recent_auth_at + timedelta(seconds=self._settings.recent_auth_window_seconds)
            <= now
        ):
            raise ReauthenticationRequiredError()
        return _BoundSession(
            account_ref=current.account_ref,
            auth_session_ref=current.auth_session_ref,
            authenticated_at=current.authenticated_at,
            recent_auth_at=current.recent_auth_at,
            expires_at=current.expires_at,
            old_secret_verifier=old_secret_verifier,
        )

    async def _rotate_bound_session(
        self,
        database_session: AsyncSession,
        *,
        bound: _BoundSession,
        new_secret_verifier: bytes,
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
                secret_verifier=new_secret_verifier,
                recent_auth_at=recent_auth_at,
                last_user_activity_at=now,
                expires_at=expires_at,
            )
            .returning(AuthSessionRow.auth_session_ref)
        )
        if rotated is None:
            raise ProviderTransactionInvalidOrExpiredError()

    async def _same_account_email_ref(
        self,
        database_session: AsyncSession,
        *,
        account_ref: UUID,
        evidence: GoogleIdentityEvidence,
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
    def _activate_google_identity(
        identity: ExternalIdentityRow,
        *,
        evidence: GoogleIdentityEvidence,
        email_identity_ref: UUID | None,
        now: datetime,
    ) -> None:
        if identity.status_code != "active":
            identity.status_code = "active"
            identity.status_changed_at = now
            identity.revoked_at = None
            identity.revocation_reason_code = None
        if identity.email_identity_ref is None and email_identity_ref is not None:
            identity.email_identity_ref = email_identity_ref
        ProviderFlowService._refresh_google_identity_metadata(identity, evidence=evidence, now=now)

    async def _stage_google_account(
        self,
        database_session: AsyncSession,
        *,
        evidence: GoogleIdentityEvidence,
        account_ref: UUID,
        email_identity_ref: UUID,
        external_identity_ref: UUID,
        auth_session_ref: UUID,
        secret_verifier: bytes,
        now: datetime,
        expires_at: datetime,
    ) -> None:
        if evidence.email is None:
            raise AuthIntegrityError("Google Account staging requires email evidence")
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
                    address=evidence.email.address,
                    comparison_key=evidence.email.comparison_key,
                    created_at=now,
                    verified_at=now,
                    recovery_restriction_code=None,
                    recovery_restriction_observed_at=None,
                ),
                ExternalIdentityRow(
                    external_identity_ref=external_identity_ref,
                    account_ref=account_ref,
                    email_identity_ref=email_identity_ref,
                    provider_code="google",
                    issuer=evidence.issuer,
                    subject=evidence.subject,
                    provider_email_address=evidence.email.address,
                    provider_email_private=False,
                    status_code="active",
                    created_at=now,
                    status_changed_at=now,
                    last_authenticated_at=now,
                    revoked_at=None,
                    revocation_reason_code=None,
                ),
                self._new_session_row(
                    auth_session_ref=auth_session_ref,
                    account_ref=account_ref,
                    secret_verifier=secret_verifier,
                    now=now,
                    expires_at=expires_at,
                ),
            ]
        )
        await database_session.flush()
        bootstrap = self._profile_bootstrap_row(account_ref=account_ref, evidence=evidence, now=now)
        if bootstrap is not None:
            database_session.add(bootstrap)

    async def _stage_account_from_enrollment(
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
                    provider_code=snapshot.provider_code,
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
                    auth_session_ref=auth_session_ref,
                    account_ref=account_ref,
                    secret_verifier=secret_verifier,
                    now=now,
                    expires_at=expires_at,
                ),
            ]
        )
        await database_session.flush()
        bootstrap = self._profile_bootstrap_from_snapshot(
            account_ref=account_ref,
            snapshot=snapshot,
            now=now,
        )
        if bootstrap is not None:
            database_session.add(bootstrap)

    def _stage_link_from_enrollment(
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
                provider_code=snapshot.provider_code,
                issuer=snapshot.issuer,
                subject=snapshot.subject,
                provider_email_address=snapshot.provider_email_address,
                provider_email_private=snapshot.provider_email_private,
                apple_auth_grant_ref=None,
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

    async def _resolve_enrollment_integrity_race(
        self,
        *,
        snapshot: _EnrollmentSnapshot,
        constraint_name: str | None,
    ) -> ProviderEnrollmentResult:
        evidence = self._evidence_from_snapshot(snapshot)
        identity = await self._read_external_identity(snapshot.issuer, snapshot.subject)

        if constraint_name == _EMAIL_UNIQUENESS_CONSTRAINT:
            collision = await self._read_email_identity(snapshot.email_comparison_key)
            if collision is None:
                raise AuthServiceUnavailableError(retryable=True)
            if identity is None:
                result: ProviderEnrollmentResult = await self._create_link_required(
                    evidence=evidence,
                    target_email=collision,
                )
            elif identity.account_ref != collision.account_ref:
                raise ProviderIdentityConflictError()
            elif identity.status_code == "active":
                result = ProviderAuthenticated(
                    session=await self._sign_in_existing_identity(identity.account_ref, evidence)
                )
            else:
                result = await self._link_required_for_bound_identity(identity, evidence)
            await self._delete_provider_enrollment_if_present(snapshot.external_signup_ref)
            return result

        if constraint_name == _EXTERNAL_IDENTITY_UNIQUENESS_CONSTRAINT:
            if identity is None:
                raise AuthServiceUnavailableError(retryable=True)
            if identity.status_code == "active":
                result = ProviderAuthenticated(
                    session=await self._sign_in_existing_identity(identity.account_ref, evidence)
                )
            else:
                result = await self._link_required_for_bound_identity(identity, evidence)
            await self._delete_provider_enrollment_if_present(snapshot.external_signup_ref)
            return result

        raise AuthServiceUnavailableError(retryable=False)

    async def _read_external_identity(
        self,
        issuer: str,
        subject: str,
    ) -> ExternalIdentityRow | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row: ExternalIdentityRow | None = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.issuer == issuer,
                        ExternalIdentityRow.subject == subject,
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_email_identity(self, comparison_key: str) -> EmailIdentityRow | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row: EmailIdentityRow | None = await database_session.scalar(
                    select(EmailIdentityRow).where(
                        EmailIdentityRow.comparison_key == comparison_key
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_email_identity_by_ref(
        self,
        email_identity_ref: UUID,
        account_ref: UUID,
    ) -> EmailIdentityRow | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row: EmailIdentityRow | None = await database_session.scalar(
                    select(EmailIdentityRow).where(
                        EmailIdentityRow.email_identity_ref == email_identity_ref,
                        EmailIdentityRow.account_ref == account_ref,
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _read_provider_transaction(
        self,
        transaction_ref: UUID,
    ) -> ExternalAuthTransactionRow | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row: ExternalAuthTransactionRow | None = await database_session.scalar(
                    select(ExternalAuthTransactionRow).where(
                        ExternalAuthTransactionRow.external_auth_transaction_ref == transaction_ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

    async def _read_provider_enrollment(
        self,
        external_signup_ref: UUID,
    ) -> ExternalSignupChallengeRow | None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row: ExternalSignupChallengeRow | None = await database_session.scalar(
                    select(ExternalSignupChallengeRow).where(
                        ExternalSignupChallengeRow.external_signup_ref == external_signup_ref
                    )
                )
                return row
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=True) from exc

    async def _delete_provider_enrollment_if_present(self, external_signup_ref: UUID) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                await database_session.execute(
                    delete(ExternalSignupChallengeRow).where(
                        ExternalSignupChallengeRow.external_signup_ref == external_signup_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc

    async def _delete_stale_provider_challenges(
        self,
        database_session: AsyncSession,
        *,
        issuer: str,
        subject: str,
    ) -> None:
        await database_session.execute(
            delete(ExternalSignupChallengeRow).where(
                ExternalSignupChallengeRow.issuer == issuer,
                ExternalSignupChallengeRow.subject == subject,
            )
        )
        await self._delete_stale_link_challenge(
            database_session,
            issuer=issuer,
            subject=subject,
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

    async def _cleanup_expired(self, database_session: AsyncSession, *, now: datetime) -> None:
        transaction_refs = list(
            await database_session.scalars(
                select(ExternalAuthTransactionRow.external_auth_transaction_ref)
                .where(ExternalAuthTransactionRow.expires_at <= now)
                .order_by(ExternalAuthTransactionRow.expires_at)
                .limit(_EXPIRED_CLEANUP_BATCH)
            )
        )
        if transaction_refs:
            await database_session.execute(
                delete(ExternalAuthTransactionRow).where(
                    ExternalAuthTransactionRow.external_auth_transaction_ref.in_(transaction_refs)
                )
            )

        signup_refs = list(
            await database_session.scalars(
                select(ExternalSignupChallengeRow.external_signup_ref)
                .where(ExternalSignupChallengeRow.expires_at <= now)
                .order_by(ExternalSignupChallengeRow.expires_at)
                .limit(_EXPIRED_CLEANUP_BATCH)
            )
        )
        if signup_refs:
            await database_session.execute(
                delete(ExternalSignupChallengeRow).where(
                    ExternalSignupChallengeRow.external_signup_ref.in_(signup_refs)
                )
            )

        link_refs = list(
            await database_session.scalars(
                select(ExternalLinkChallengeRow.external_link_challenge_ref)
                .where(ExternalLinkChallengeRow.expires_at <= now)
                .order_by(ExternalLinkChallengeRow.expires_at)
                .limit(_EXPIRED_CLEANUP_BATCH)
            )
        )
        if link_refs:
            await database_session.execute(
                delete(ExternalLinkChallengeRow).where(
                    ExternalLinkChallengeRow.external_link_challenge_ref.in_(link_refs)
                )
            )

    async def _reconcile_session_commit(
        self,
        *,
        auth_session_ref: UUID,
        account_ref: UUID,
        secret_verifier: bytes,
        created_at: datetime,
        expires_at: datetime,
    ) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                persisted = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == auth_session_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            persisted is None
            or persisted.account_ref != account_ref
            or not hmac.compare_digest(persisted.secret_verifier, secret_verifier)
            or persisted.created_at != created_at
            or persisted.authenticated_at != created_at
            or persisted.recent_auth_at != created_at
            or persisted.expires_at != expires_at
            or persisted.revoked_at is not None
        ):
            raise AuthServiceUnavailableError(retryable=False)

    async def _reconcile_rotated_session(
        self,
        *,
        bound: _BoundSession,
        new_secret_verifier: bytes,
        recent_auth_at: datetime,
        expires_at: datetime,
        evidence: GoogleIdentityEvidence,
    ) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                session = await database_session.scalar(
                    select(AuthSessionRow).where(
                        AuthSessionRow.auth_session_ref == bound.auth_session_ref,
                        AuthSessionRow.account_ref == bound.account_ref,
                    )
                )
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.issuer == evidence.issuer,
                        ExternalIdentityRow.subject == evidence.subject,
                        ExternalIdentityRow.account_ref == bound.account_ref,
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            session is None
            or identity is None
            or identity.status_code != "active"
            or not hmac.compare_digest(session.secret_verifier, new_secret_verifier)
            or session.recent_auth_at != recent_auth_at
            or session.expires_at != expires_at
            or session.revoked_at is not None
        ):
            raise AuthServiceUnavailableError(retryable=False)

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
        consumed_signup_ref: UUID | None,
    ) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                account = await database_session.scalar(
                    select(AccountRow).where(AccountRow.account_ref == account_ref)
                )
                email = await database_session.scalar(
                    select(EmailIdentityRow).where(
                        EmailIdentityRow.email_identity_ref == email_identity_ref,
                        EmailIdentityRow.account_ref == account_ref,
                    )
                )
                identity = await database_session.scalar(
                    select(ExternalIdentityRow).where(
                        ExternalIdentityRow.external_identity_ref == external_identity_ref,
                        ExternalIdentityRow.account_ref == account_ref,
                    )
                )
                pending = (
                    await database_session.scalar(
                        select(ExternalSignupChallengeRow.external_signup_ref).where(
                            ExternalSignupChallengeRow.external_signup_ref == consumed_signup_ref
                        )
                    )
                    if consumed_signup_ref is not None
                    else None
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            account is None
            or account.status_code != "active"
            or email is None
            or email.comparison_key != email_comparison_key
            or email.verified_at != created_at
            or identity is None
            or identity.issuer != issuer
            or identity.subject != subject
            or identity.status_code != "active"
            or pending is not None
        ):
            raise AuthServiceUnavailableError(retryable=False)
        await self._reconcile_session_commit(
            auth_session_ref=auth_session_ref,
            account_ref=account_ref,
            secret_verifier=secret_verifier,
            created_at=created_at,
            expires_at=expires_at,
        )

    async def _reconcile_link_commit(
        self,
        *,
        result: ProviderLinkRequired,
        consumed_signup_ref: UUID,
    ) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = await database_session.scalar(
                    select(ExternalLinkChallengeRow).where(
                        ExternalLinkChallengeRow.external_link_challenge_ref
                        == result.external_link_challenge_ref
                    )
                )
                pending = await database_session.scalar(
                    select(ExternalSignupChallengeRow.external_signup_ref).where(
                        ExternalSignupChallengeRow.external_signup_ref == consumed_signup_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            row is None
            or pending is not None
            or not flow_proof_matches(
                purpose=FlowProofPurpose.PROVIDER_LINK,
                encoded_secret=result.continuation_secret.get_secret_value(),
                expected_verifier=row.continuation_verifier,
            )
        ):
            raise AuthServiceUnavailableError(retryable=False)

    async def _reconcile_link_row(self, expected: ExternalLinkChallengeRow) -> None:
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = await database_session.scalar(
                    select(ExternalLinkChallengeRow).where(
                        ExternalLinkChallengeRow.external_link_challenge_ref
                        == expected.external_link_challenge_ref
                    )
                )
        except SQLAlchemyError as exc:
            raise AuthServiceUnavailableError(retryable=False) from exc
        if (
            row is None
            or row.target_account_ref != expected.target_account_ref
            or row.target_email_identity_ref != expected.target_email_identity_ref
            or row.issuer != expected.issuer
            or row.subject != expected.subject
            or not hmac.compare_digest(
                row.continuation_verifier,
                expected.continuation_verifier,
            )
            or row.expires_at != expected.expires_at
        ):
            raise AuthServiceUnavailableError(retryable=False)

    async def _enqueue_provider_otp(
        self,
        *,
        email_address: str,
        code: SecretStr,
        expires_at: datetime,
        now: datetime,
    ) -> None:
        try:
            await self._email_delivery.enqueue(
                ProviderEnrollmentVerificationEmail(
                    to_address=email_address,
                    code=code,
                    expires_minutes=max(1, math.ceil((expires_at - now).total_seconds() / 60)),
                )
            )
        except EmailDispatchCapacityError as exc:
            raise EmailDeliveryUnavailableError() from exc

    def _require_enrollment_challenge(
        self,
        challenge: ExternalSignupChallengeRow | None,
        *,
        continuation_secret: str,
        now: datetime,
    ) -> ExternalSignupChallengeRow:
        if (
            challenge is None
            or challenge.expires_at <= now
            or not flow_proof_matches(
                purpose=FlowProofPurpose.PROVIDER_ENROLLMENT,
                encoded_secret=continuation_secret,
                expected_verifier=challenge.continuation_verifier,
            )
        ):
            raise ProviderEnrollmentInvalidOrExpiredError()
        return challenge

    def _require_recent_auth(self, admitted: AdmittedSession) -> None:
        deadline = admitted.principal.recent_auth_at + timedelta(
            seconds=self._settings.recent_auth_window_seconds
        )
        if deadline <= datetime.now(UTC):
            raise ReauthenticationRequiredError()

    def _provider_otp_ttl(self) -> timedelta:
        return min(
            timedelta(seconds=self._settings.signup_otp_lifetime_seconds),
            _PROVIDER_ENROLLMENT_OTP_MAX_TTL,
        )

    @staticmethod
    def _normalize_enrollment_email(value: str) -> NormalizedEmail:
        try:
            return normalize_email(value)
        except EmailNormalizationError as exc:
            raise AuthInputError(
                pointer="/email",
                code="invalid_format",
                detail="Enter a valid email address.",
            ) from exc

    @staticmethod
    def _refresh_google_identity_metadata(
        identity: ExternalIdentityRow,
        *,
        evidence: GoogleIdentityEvidence,
        now: datetime,
    ) -> None:
        if evidence.email is not None:
            identity.provider_email_address = evidence.email.address
            identity.provider_email_private = False
        identity.last_authenticated_at = now

    @staticmethod
    def _new_session_row(
        *,
        auth_session_ref: UUID,
        account_ref: UUID,
        secret_verifier: bytes,
        now: datetime,
        expires_at: datetime,
    ) -> AuthSessionRow:
        return AuthSessionRow(
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
    def _profile_bootstrap_row(
        *,
        account_ref: UUID,
        evidence: GoogleIdentityEvidence,
        now: datetime,
    ) -> AccountProfileBootstrapRow | None:
        values = (
            evidence.display_name,
            evidence.given_name,
            evidence.family_name,
            evidence.picture_url,
            evidence.locale,
        )
        if not any(value is not None for value in values):
            return None
        return AccountProfileBootstrapRow(
            account_ref=account_ref,
            source_provider_code="google",
            source_issuer=evidence.issuer,
            display_name=evidence.display_name,
            given_name=evidence.given_name,
            family_name=evidence.family_name,
            picture_url=evidence.picture_url,
            locale=evidence.locale,
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
        values = (
            snapshot.bootstrap_display_name,
            snapshot.bootstrap_given_name,
            snapshot.bootstrap_family_name,
            snapshot.bootstrap_picture_url,
            snapshot.bootstrap_locale,
        )
        if not any(value is not None for value in values):
            return None
        return AccountProfileBootstrapRow(
            account_ref=account_ref,
            source_provider_code=snapshot.provider_code,
            source_issuer=snapshot.issuer,
            display_name=snapshot.bootstrap_display_name,
            given_name=snapshot.bootstrap_given_name,
            family_name=snapshot.bootstrap_family_name,
            picture_url=snapshot.bootstrap_picture_url,
            locale=snapshot.bootstrap_locale,
            created_at=now,
            expires_at=now + _PROFILE_BOOTSTRAP_TTL,
        )

    @staticmethod
    def _enrollment_snapshot(challenge: ExternalSignupChallengeRow) -> _EnrollmentSnapshot:
        if challenge.email_address is None or challenge.email_comparison_key is None:
            raise AuthIntegrityError("verified provider enrollment has no mailbox")
        return _EnrollmentSnapshot(
            external_signup_ref=challenge.external_signup_ref,
            provider_code=challenge.provider_code,
            issuer=challenge.issuer,
            subject=challenge.subject,
            provider_email_address=challenge.provider_email_address,
            provider_email_private=challenge.provider_email_private,
            continuation_verifier=challenge.continuation_verifier,
            email_address=challenge.email_address,
            email_comparison_key=challenge.email_comparison_key,
            bootstrap_display_name=challenge.bootstrap_display_name,
            bootstrap_given_name=challenge.bootstrap_given_name,
            bootstrap_family_name=challenge.bootstrap_family_name,
            bootstrap_picture_url=challenge.bootstrap_picture_url,
            bootstrap_locale=challenge.bootstrap_locale,
        )

    @staticmethod
    def _evidence_from_snapshot(snapshot: _EnrollmentSnapshot) -> GoogleIdentityEvidence:
        provider_email = None
        if snapshot.provider_email_address is not None:
            try:
                provider_email = normalize_email(snapshot.provider_email_address)
            except EmailNormalizationError as exc:
                raise AuthIntegrityError("stored Google provider email is invalid") from exc
        return GoogleIdentityEvidence(
            issuer=snapshot.issuer,
            subject=snapshot.subject,
            email=provider_email,
            email_verified=False,
            hosted_domain=None,
            mailbox_authoritative=False,
            display_name=snapshot.bootstrap_display_name,
            given_name=snapshot.bootstrap_given_name,
            family_name=snapshot.bootstrap_family_name,
            picture_url=snapshot.bootstrap_picture_url,
            locale=snapshot.bootstrap_locale,
        )

    @staticmethod
    def _same_provider_transaction(
        persisted: ExternalAuthTransactionRow,
        expected: ExternalAuthTransactionRow,
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
            and persisted.claimed_at is None
        )

    @staticmethod
    def _constraint_name(exc: IntegrityError) -> str | None:
        diagnostic = getattr(exc.orig, "diag", None)
        value = getattr(diagnostic, "constraint_name", None)
        return value if isinstance(value, str) else None

    @staticmethod
    async def _safe_rollback(database_session: AsyncSession) -> None:
        if not database_session.in_transaction():
            return
        with suppress(SQLAlchemyError):
            await database_session.rollback()
