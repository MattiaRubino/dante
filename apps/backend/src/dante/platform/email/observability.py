"""Privacy-minimized operational metrics derived from canonical Email Platform state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
    EmailRecipientSuppressionRow,
)

_BACKLOG_STATES = ("pending", "claimed", "retryable_failure")


@dataclass(frozen=True, slots=True)
class EmailOperationalSnapshot:
    """Low-cardinality Email Platform metrics with no recipient or secret dimensions."""

    captured_at: datetime
    window_seconds: int
    backlog_count: int
    oldest_backlog_age_seconds: float | None
    provider_accepted_count: int
    ambiguous_count: int
    retryable_failure_count: int
    definitive_failure_count: int
    accepted_send_latency_avg_seconds: float | None
    accepted_send_latency_max_seconds: float | None
    active_hard_bounce_suppressions: int
    active_complaint_suppressions: int


class EmailObservabilityProbe:
    """Pull operational metrics from durable PostgreSQL truth, never process-local counters."""

    def __init__(self, *, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def snapshot(
        self,
        *,
        window_seconds: int = 900,
        now: datetime | None = None,
    ) -> EmailOperationalSnapshot:
        """Return one bounded operational snapshot suitable for metrics/export adapters."""
        if window_seconds <= 0:
            raise ValueError("email observability window must be positive")
        captured_at = datetime.now(UTC) if now is None else now.astimezone(UTC)
        window_start = captured_at - timedelta(seconds=window_seconds)

        async with self._session_factory() as session, session.begin():
            backlog_row = (
                await session.execute(
                    select(
                        func.count(EmailDeliveryIntentRow.email_intent_ref),
                        func.min(EmailDeliveryIntentRow.created_at),
                    ).where(EmailDeliveryIntentRow.dispatch_state_code.in_(_BACKLOG_STATES))
                )
            ).one()

            outcome_rows = (
                await session.execute(
                    select(
                        EmailDeliveryAttemptRow.result_code,
                        func.count(EmailDeliveryAttemptRow.email_attempt_ref),
                    )
                    .where(
                        EmailDeliveryAttemptRow.finished_at.is_not(None),
                        EmailDeliveryAttemptRow.finished_at >= window_start,
                    )
                    .group_by(EmailDeliveryAttemptRow.result_code)
                )
            ).all()

            latency_row = (
                await session.execute(
                    select(
                        func.avg(
                            func.extract(
                                "epoch",
                                EmailDeliveryAttemptRow.finished_at
                                - EmailDeliveryAttemptRow.started_at,
                            )
                        ),
                        func.max(
                            func.extract(
                                "epoch",
                                EmailDeliveryAttemptRow.finished_at
                                - EmailDeliveryAttemptRow.started_at,
                            )
                        ),
                    ).where(
                        EmailDeliveryAttemptRow.result_code == "provider_accepted",
                        EmailDeliveryAttemptRow.finished_at.is_not(None),
                        EmailDeliveryAttemptRow.finished_at >= window_start,
                    )
                )
            ).one()

            suppression_rows = (
                await session.execute(
                    select(
                        EmailRecipientSuppressionRow.reason_code,
                        func.count(EmailRecipientSuppressionRow.email_recipient_suppression_ref),
                    )
                    .where(EmailRecipientSuppressionRow.cleared_at.is_(None))
                    .group_by(EmailRecipientSuppressionRow.reason_code)
                )
            ).all()

        backlog_count = int(backlog_row[0])
        oldest_created_at = backlog_row[1]
        oldest_age = (
            None
            if oldest_created_at is None
            else max(0.0, (captured_at - oldest_created_at).total_seconds())
        )
        outcomes = {str(code): int(count) for code, count in outcome_rows}
        suppressions = {str(code): int(count) for code, count in suppression_rows}
        latency_avg = None if latency_row[0] is None else float(latency_row[0])
        latency_max = None if latency_row[1] is None else float(latency_row[1])

        return EmailOperationalSnapshot(
            captured_at=captured_at,
            window_seconds=window_seconds,
            backlog_count=backlog_count,
            oldest_backlog_age_seconds=oldest_age,
            provider_accepted_count=outcomes.get("provider_accepted", 0),
            ambiguous_count=outcomes.get("ambiguous", 0),
            retryable_failure_count=outcomes.get("retryable_failure", 0),
            definitive_failure_count=outcomes.get("definitive_failure", 0),
            accepted_send_latency_avg_seconds=latency_avg,
            accepted_send_latency_max_seconds=latency_max,
            active_hard_bounce_suppressions=suppressions.get("hard_bounce", 0),
            active_complaint_suppressions=suppressions.get("complaint", 0),
        )
