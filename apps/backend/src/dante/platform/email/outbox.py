"""Transactional PostgreSQL outbox for the shared DANTE Email Platform."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID, uuid7

from sqlalchemy import exists, or_, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
    EmailRecipientSuppressionRow,
)
from dante.platform.email.contracts import (
    ClaimedEmailIntent,
    EmailIntentConflictError,
    EmailIntentSpec,
    ProviderOutcome,
    ProviderSendResult,
)
from dante.platform.email.crypto import EmailPayloadCipher


class DurableEmailOutbox:
    """Persist consumer intents, claim with SKIP LOCKED and preserve uncertain outcomes."""

    def __init__(self, *, cipher: EmailPayloadCipher, attempt_limit: int) -> None:
        if attempt_limit <= 0:
            raise ValueError("email attempt limit must be positive")
        self._cipher = cipher
        self._attempt_limit = attempt_limit

    async def stage(
        self,
        database_session: AsyncSession,
        *,
        spec: EmailIntentSpec,
        stream_code: str,
        template_revision: str,
        operation_scope: str,
        idempotency_key: str,
        expires_at: datetime,
        supersession_key: str | None = None,
        locale_code: str = "en",
        eligible_at: datetime | None = None,
    ) -> UUID:
        """Write one immutable provider-neutral intent in the caller-owned transaction."""
        now = datetime.now(UTC)
        if expires_at <= now:
            raise ValueError("email intent expiry must be in the future")
        for name, value in (
            ("stream_code", stream_code),
            ("template_revision", template_revision),
            ("operation_scope", operation_scope),
            ("idempotency_key", idempotency_key),
            ("locale_code", locale_code),
        ):
            if not value or value.strip() != value:
                raise ValueError(f"{name} must be non-blank and trimmed")

        existing = await database_session.scalar(
            select(EmailDeliveryIntentRow).where(
                EmailDeliveryIntentRow.operation_scope == operation_scope,
                EmailDeliveryIntentRow.idempotency_key == idempotency_key,
            )
        )
        if existing is not None:
            if self._cipher.matches_fingerprint(
                existing.payload_fingerprint,
                purpose_code=spec.purpose_code,
                template_code=spec.template_code,
                template_revision=existing.template_revision,
                payload=spec.payload,
            ):
                return existing.email_intent_ref
            raise EmailIntentConflictError(
                "email idempotency identity was reused for different work"
            )

        fingerprint = self._cipher.fingerprint(
            purpose_code=spec.purpose_code,
            template_code=spec.template_code,
            template_revision=template_revision,
            payload=spec.payload,
        )
        email_intent_ref = uuid7()
        protected = self._cipher.protect(
            email_intent_ref=email_intent_ref,
            purpose_code=spec.purpose_code,
            template_code=spec.template_code,
            template_revision=template_revision,
            payload=spec.payload,
        )

        if supersession_key is not None:
            await self._cancel_superseded(
                database_session,
                supersession_key=supersession_key,
                now=now,
            )

        database_session.add(
            EmailDeliveryIntentRow(
                email_intent_ref=email_intent_ref,
                purpose_code=spec.purpose_code,
                stream_code=stream_code,
                recipient_address=spec.recipient_address,
                recipient_comparison_key=spec.recipient_comparison_key,
                template_code=spec.template_code,
                template_revision=template_revision,
                locale_code=locale_code,
                operation_scope=operation_scope,
                idempotency_key=idempotency_key,
                supersession_key=supersession_key,
                payload_fingerprint=fingerprint,
                sensitive_key_id=None if protected is None else protected.key_id,
                sensitive_nonce=None if protected is None else protected.nonce,
                sensitive_ciphertext=None if protected is None else protected.ciphertext,
                created_at=now,
                updated_at=now,
                eligible_at=now if eligible_at is None else eligible_at,
                expires_at=expires_at,
                dispatch_state_code="pending",
                claim_token=None,
                claimed_until=None,
                attempt_count=0,
                attempt_limit=self._attempt_limit,
                next_attempt_at=None,
                last_error_code=None,
                accepted_at=None,
                terminal_at=None,
                sensitive_wiped_at=None,
            )
        )
        return email_intent_ref

    async def claim_batch(
        self,
        database_session: AsyncSession,
        *,
        provider_code: str,
        batch_size: int,
        lease_seconds: float,
        now: datetime | None = None,
    ) -> list[ClaimedEmailIntent]:
        """Claim eligible work and fail closed on expired in-flight leases."""
        if provider_code not in {"smtp", "ses"}:
            raise ValueError("unsupported email provider code")
        if batch_size <= 0 or lease_seconds <= 0:
            raise ValueError("claim batch and lease must be positive")
        effective_now = datetime.now(UTC) if now is None else now

        await self._quarantine_expired_claims(database_session, now=effective_now)
        await self._expire_unsent(database_session, now=effective_now)

        active_suppression = exists(
            select(EmailRecipientSuppressionRow.email_recipient_suppression_ref).where(
                EmailRecipientSuppressionRow.recipient_comparison_key
                == EmailDeliveryIntentRow.recipient_comparison_key,
                EmailRecipientSuppressionRow.cleared_at.is_(None),
            )
        )
        rows = list(
            (
                await database_session.scalars(
                    select(EmailDeliveryIntentRow)
                    .where(
                        EmailDeliveryIntentRow.dispatch_state_code.in_(
                            ("pending", "retryable_failure")
                        ),
                        EmailDeliveryIntentRow.eligible_at <= effective_now,
                        EmailDeliveryIntentRow.expires_at > effective_now,
                        or_(
                            EmailDeliveryIntentRow.next_attempt_at.is_(None),
                            EmailDeliveryIntentRow.next_attempt_at <= effective_now,
                        ),
                        ~active_suppression,
                    )
                    .order_by(
                        EmailDeliveryIntentRow.eligible_at,
                        EmailDeliveryIntentRow.created_at,
                    )
                    .limit(batch_size)
                    .with_for_update(skip_locked=True)
                )
            ).all()
        )

        claims: list[ClaimedEmailIntent] = []
        for row in rows:
            claim_token = uuid7()
            email_attempt_ref = uuid7()
            attempt_number = row.attempt_count + 1
            row.dispatch_state_code = "claimed"
            row.claim_token = claim_token
            row.claimed_until = effective_now + timedelta(seconds=lease_seconds)
            row.attempt_count = attempt_number
            row.next_attempt_at = None
            row.last_error_code = None
            row.updated_at = effective_now

            database_session.add(
                EmailDeliveryAttemptRow(
                    email_attempt_ref=email_attempt_ref,
                    email_intent_ref=row.email_intent_ref,
                    attempt_number=attempt_number,
                    provider_code=provider_code,
                    started_at=effective_now,
                    finished_at=None,
                    result_code="in_progress",
                    provider_message_id=None,
                    error_code=None,
                )
            )
            claims.append(
                ClaimedEmailIntent(
                    email_intent_ref=row.email_intent_ref,
                    email_attempt_ref=email_attempt_ref,
                    claim_token=claim_token,
                    purpose_code=row.purpose_code,
                    stream_code=row.stream_code,
                    template_code=row.template_code,
                    template_revision=row.template_revision,
                    locale_code=row.locale_code,
                    recipient_address=row.recipient_address,
                    recipient_comparison_key=row.recipient_comparison_key,
                    sensitive_key_id=row.sensitive_key_id,
                    sensitive_nonce=row.sensitive_nonce,
                    sensitive_ciphertext=row.sensitive_ciphertext,
                    attempt_number=attempt_number,
                    expires_at=row.expires_at,
                )
            )
        return claims

    async def claim_still_owned(
        self,
        database_session: AsyncSession,
        *,
        claim: ClaimedEmailIntent,
        now: datetime | None = None,
    ) -> bool:
        """Re-check the exact lease immediately before external I/O."""
        effective_now = datetime.now(UTC) if now is None else now
        owned = await database_session.scalar(
            select(EmailDeliveryIntentRow.email_intent_ref).where(
                EmailDeliveryIntentRow.email_intent_ref == claim.email_intent_ref,
                EmailDeliveryIntentRow.dispatch_state_code == "claimed",
                EmailDeliveryIntentRow.claim_token == claim.claim_token,
                EmailDeliveryIntentRow.claimed_until > effective_now,
                EmailDeliveryIntentRow.expires_at > effective_now,
            )
        )
        return owned is not None

    async def finalize(
        self,
        database_session: AsyncSession,
        *,
        claim: ClaimedEmailIntent,
        result: ProviderSendResult,
        now: datetime | None = None,
        retry_delay_seconds: float = 0,
    ) -> bool:
        """Finalize only a still-owned claim; stale workers cannot overwrite newer truth."""
        effective_now = datetime.now(UTC) if now is None else now
        intent = await database_session.scalar(
            select(EmailDeliveryIntentRow)
            .where(
                EmailDeliveryIntentRow.email_intent_ref == claim.email_intent_ref,
                EmailDeliveryIntentRow.dispatch_state_code == "claimed",
                EmailDeliveryIntentRow.claim_token == claim.claim_token,
            )
            .with_for_update()
        )
        attempt = await database_session.scalar(
            select(EmailDeliveryAttemptRow)
            .where(
                EmailDeliveryAttemptRow.email_attempt_ref == claim.email_attempt_ref,
                EmailDeliveryAttemptRow.email_intent_ref == claim.email_intent_ref,
                EmailDeliveryAttemptRow.result_code == "in_progress",
            )
            .with_for_update()
        )
        if intent is None or attempt is None:
            return False

        attempt.finished_at = effective_now
        attempt.result_code = result.outcome.value
        attempt.provider_message_id = result.provider_message_id
        attempt.error_code = _safe_code(result.safe_error_code)

        intent.claim_token = None
        intent.claimed_until = None
        intent.last_error_code = _safe_code(result.safe_error_code)
        intent.updated_at = effective_now

        if result.outcome is ProviderOutcome.ACCEPTED:
            intent.dispatch_state_code = "provider_accepted"
            intent.accepted_at = effective_now
            intent.terminal_at = effective_now
            _wipe_sensitive(intent, effective_now)
            return True

        if result.outcome is ProviderOutcome.AMBIGUOUS:
            intent.dispatch_state_code = "ambiguous"
            intent.terminal_at = effective_now
            _wipe_sensitive(intent, effective_now)
            return True

        if result.outcome is ProviderOutcome.DEFINITIVE_FAILURE:
            intent.dispatch_state_code = "definitive_failure"
            intent.terminal_at = effective_now
            _wipe_sensitive(intent, effective_now)
            return True

        if intent.attempt_count >= intent.attempt_limit or intent.expires_at <= effective_now:
            intent.dispatch_state_code = "definitive_failure"
            intent.terminal_at = effective_now
            _wipe_sensitive(intent, effective_now)
            return True

        intent.dispatch_state_code = "retryable_failure"
        intent.next_attempt_at = effective_now + timedelta(seconds=max(0.0, retry_delay_seconds))
        return True

    async def quarantine_after_restore(
        self,
        database_session: AsyncSession,
        *,
        now: datetime | None = None,
    ) -> int:
        """Quarantine restored non-terminal work before runtime reopen."""
        effective_now = datetime.now(UTC) if now is None else now
        result = await database_session.execute(
            update(EmailDeliveryIntentRow)
            .where(
                EmailDeliveryIntentRow.dispatch_state_code.in_(
                    ("pending", "claimed", "retryable_failure")
                )
            )
            .values(
                dispatch_state_code="recovery_quarantined",
                claim_token=None,
                claimed_until=None,
                next_attempt_at=None,
                last_error_code="post_restore_quarantine",
                terminal_at=effective_now,
                updated_at=effective_now,
                sensitive_key_id=None,
                sensitive_nonce=None,
                sensitive_ciphertext=None,
                sensitive_wiped_at=effective_now,
            )
        )
        return int(cast(CursorResult[Any], result).rowcount or 0)

    async def _quarantine_expired_claims(
        self,
        database_session: AsyncSession,
        *,
        now: datetime,
    ) -> None:
        await database_session.execute(
            update(EmailDeliveryIntentRow)
            .where(
                EmailDeliveryIntentRow.dispatch_state_code == "claimed",
                EmailDeliveryIntentRow.claimed_until <= now,
            )
            .values(
                dispatch_state_code="ambiguous",
                claim_token=None,
                claimed_until=None,
                next_attempt_at=None,
                last_error_code="claim_lease_expired",
                terminal_at=now,
                updated_at=now,
                sensitive_key_id=None,
                sensitive_nonce=None,
                sensitive_ciphertext=None,
                sensitive_wiped_at=now,
            )
        )

    async def _expire_unsent(
        self,
        database_session: AsyncSession,
        *,
        now: datetime,
    ) -> None:
        await database_session.execute(
            update(EmailDeliveryIntentRow)
            .where(
                EmailDeliveryIntentRow.dispatch_state_code.in_(("pending", "retryable_failure")),
                EmailDeliveryIntentRow.expires_at <= now,
            )
            .values(
                dispatch_state_code="expired",
                next_attempt_at=None,
                terminal_at=now,
                updated_at=now,
                sensitive_key_id=None,
                sensitive_nonce=None,
                sensitive_ciphertext=None,
                sensitive_wiped_at=now,
            )
        )

    async def _cancel_superseded(
        self,
        database_session: AsyncSession,
        *,
        supersession_key: str,
        now: datetime,
    ) -> None:
        await database_session.execute(
            update(EmailDeliveryIntentRow)
            .where(
                EmailDeliveryIntentRow.supersession_key == supersession_key,
                EmailDeliveryIntentRow.dispatch_state_code.in_(
                    ("pending", "claimed", "retryable_failure")
                ),
            )
            .values(
                dispatch_state_code="cancelled",
                claim_token=None,
                claimed_until=None,
                next_attempt_at=None,
                last_error_code="superseded",
                terminal_at=now,
                updated_at=now,
                sensitive_key_id=None,
                sensitive_nonce=None,
                sensitive_ciphertext=None,
                sensitive_wiped_at=now,
            )
        )


def _wipe_sensitive(row: EmailDeliveryIntentRow, when: datetime) -> None:
    row.sensitive_key_id = None
    row.sensitive_nonce = None
    row.sensitive_ciphertext = None
    row.sensitive_wiped_at = when


def _safe_code(value: str | None) -> str | None:
    if value is None:
        return None
    candidate = value.strip()
    if not candidate or len(candidate) > 128 or any(ch in candidate for ch in "\r\n"):
        return "provider_error"
    return candidate
