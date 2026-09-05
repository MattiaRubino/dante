"""Post-restore reconciliation for durable Email Platform work.

This module owns the provider-free database transition required before Email
workers may resume after a restore/PITR.  It deliberately performs no provider
I/O and does not construct a worker pool.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
)

_RESTORED_SENDABLE_STATES = ("pending", "claimed", "retryable_failure")
_POST_RESTORE_ERROR_CODE = "post_restore_quarantine"


@dataclass(frozen=True, slots=True)
class EmailPostRestoreQuarantineResult:
    """Committed-transition counts produced by one post-restore transaction."""

    quarantined_intent_count: int
    ambiguous_attempt_count: int


async def quarantine_restored_email_delivery(
    database_session: AsyncSession,
    *,
    now: datetime | None = None,
) -> EmailPostRestoreQuarantineResult:
    """Make restored non-terminal email work permanently non-sendable.

    A restored ``claimed`` intent can also carry an ``in_progress`` provider
    attempt.  That attempt is uncertain after PITR and must become ``ambiguous``
    before the intent is quarantined.  Pending and retryable intents are then
    terminalized and all short-lived sensitive delivery material is wiped.

    The caller owns the surrounding transaction.  No provider/network I/O is
    permitted in this function.
    """

    effective_now = datetime.now(UTC) if now is None else now
    target_intents = select(EmailDeliveryIntentRow.email_intent_ref).where(
        EmailDeliveryIntentRow.dispatch_state_code.in_(_RESTORED_SENDABLE_STATES)
    )

    attempt_result = await database_session.execute(
        update(EmailDeliveryAttemptRow)
        .where(
            EmailDeliveryAttemptRow.email_intent_ref.in_(target_intents),
            EmailDeliveryAttemptRow.result_code == "in_progress",
        )
        .values(
            finished_at=effective_now,
            result_code="ambiguous",
            error_code=_POST_RESTORE_ERROR_CODE,
        )
    )

    intent_result = await database_session.execute(
        update(EmailDeliveryIntentRow)
        .where(EmailDeliveryIntentRow.dispatch_state_code.in_(_RESTORED_SENDABLE_STATES))
        .values(
            dispatch_state_code="recovery_quarantined",
            claim_token=None,
            claimed_until=None,
            next_attempt_at=None,
            last_error_code=_POST_RESTORE_ERROR_CODE,
            terminal_at=effective_now,
            updated_at=effective_now,
            sensitive_key_id=None,
            sensitive_nonce=None,
            sensitive_ciphertext=None,
            sensitive_wiped_at=effective_now,
        )
    )

    return EmailPostRestoreQuarantineResult(
        quarantined_intent_count=int(cast(CursorResult[Any], intent_result).rowcount or 0),
        ambiguous_attempt_count=int(cast(CursorResult[Any], attempt_result).rowcount or 0),
    )


__all__ = [
    "EmailPostRestoreQuarantineResult",
    "quarantine_restored_email_delivery",
]
