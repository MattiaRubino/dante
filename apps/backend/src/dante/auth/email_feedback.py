"""Amazon SES feedback normalization and idempotent DANTE persistence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any, Mapping
from uuid import UUID, uuid7

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from dante.platform.database.mappings.auth import EmailIdentityRow
from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
    EmailProviderEventRow,
    EmailRecipientSuppressionRow,
)

_MAX_EVENT_BYTES = 262_144
_SUPPORTED_EVENTS = {
    "Delivery": "delivered",
    "DeliveryDelay": "delivery_delayed",
    "Bounce": "bounced",
    "Complaint": "complained",
    "Reject": "rejected",
}


class SesFeedbackError(ValueError):
    """SES feedback envelope is unsupported, malformed or exceeds admission bounds."""


@dataclass(frozen=True, slots=True)
class SesFeedbackEvent:
    """Privacy-minimized normalized provider evidence."""

    provider_event_id: str
    provider_message_id: str
    email_intent_ref: UUID
    event_type_code: str
    observed_at: datetime
    payload_digest: bytes
    safe_detail_code: str | None
    permanent_suppression_reason: str | None


def parse_ses_feedback(raw_body: bytes) -> SesFeedbackEvent | None:
    """Normalize one EventBridge/SES JSON event; tracking-only events are ignored."""
    if not raw_body or len(raw_body) > _MAX_EVENT_BYTES:
        raise SesFeedbackError("SES event body violates size bounds")
    digest = sha256(raw_body).digest()
    try:
        envelope = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise SesFeedbackError("SES event body is not JSON") from exc
    if not isinstance(envelope, dict):
        raise SesFeedbackError("SES event envelope must be an object")

    detail_obj = envelope.get("detail", envelope)
    if not isinstance(detail_obj, dict):
        raise SesFeedbackError("SES event detail must be an object")
    detail = _mapping(detail_obj)

    raw_type = detail.get("eventType") or detail.get("event_type")
    if raw_type in {"Open", "Click", "Subscription"}:
        return None
    if not isinstance(raw_type, str) or raw_type not in _SUPPORTED_EVENTS:
        raise SesFeedbackError("SES event type is unsupported")

    mail = _mapping(detail.get("mail"))
    message_id = mail.get("messageId")
    if not isinstance(message_id, str) or not message_id.strip():
        raise SesFeedbackError("SES event has no provider message id")

    intent_ref = _intent_ref_from_tags(_mapping(mail.get("tags")))
    if intent_ref is None:
        raise SesFeedbackError("SES event has no DANTE intent correlation tag")

    event_id = envelope.get("id")
    if not isinstance(event_id, str) or not event_id.strip():
        event_id = digest.hex()

    observed_at = _event_timestamp(detail=detail, mail=mail)
    safe_detail: str | None = None
    suppression_reason: str | None = None
    if raw_type == "Bounce":
        bounce = _mapping(detail.get("bounce"))
        bounce_type = bounce.get("bounceType")
        if isinstance(bounce_type, str):
            safe_detail = bounce_type[:64]
            if bounce_type == "Permanent":
                suppression_reason = "hard_bounce"
    elif raw_type == "Complaint":
        complaint = _mapping(detail.get("complaint"))
        feedback = complaint.get("complaintFeedbackType")
        safe_detail = feedback[:64] if isinstance(feedback, str) else None
        suppression_reason = "complaint"
    elif raw_type == "DeliveryDelay":
        delay = _mapping(detail.get("deliveryDelay"))
        delay_type = delay.get("delayType")
        safe_detail = delay_type[:64] if isinstance(delay_type, str) else None
    elif raw_type == "Reject":
        reject = _mapping(detail.get("reject"))
        reason = reject.get("reason")
        safe_detail = reason[:64] if isinstance(reason, str) else None

    return SesFeedbackEvent(
        provider_event_id=event_id,
        provider_message_id=message_id,
        email_intent_ref=intent_ref,
        event_type_code=_SUPPORTED_EVENTS[raw_type],
        observed_at=observed_at,
        payload_digest=digest,
        safe_detail_code=safe_detail,
        permanent_suppression_reason=suppression_reason,
    )


class SesFeedbackStore:
    """Persist normalized SES evidence idempotently and project durable suppression."""

    async def ingest(
        self,
        database_session: AsyncSession,
        *,
        event: SesFeedbackEvent,
        received_at: datetime | None = None,
    ) -> bool:
        """Accept one correlated event; duplicates become safe no-ops."""
        now = datetime.now(UTC) if received_at is None else received_at
        intent = await database_session.scalar(
            select(EmailDeliveryIntentRow).where(
                EmailDeliveryIntentRow.email_intent_ref == event.email_intent_ref
            )
        )
        if intent is None:
            raise SesFeedbackError("SES event references an unknown DANTE email intent")
        attempt = await database_session.scalar(
            select(EmailDeliveryAttemptRow.email_attempt_ref).where(
                EmailDeliveryAttemptRow.email_intent_ref == event.email_intent_ref,
                EmailDeliveryAttemptRow.provider_code == "ses",
                EmailDeliveryAttemptRow.provider_message_id == event.provider_message_id,
            )
        )
        if attempt is None:
            raise SesFeedbackError("SES event message id does not match the DANTE intent")

        event_ref = uuid7()
        inserted = await database_session.scalar(
            pg_insert(EmailProviderEventRow)
            .values(
                email_provider_event_ref=event_ref,
                provider_code="ses",
                provider_event_id=event.provider_event_id,
                provider_message_id=event.provider_message_id,
                email_intent_ref=event.email_intent_ref,
                event_type_code=event.event_type_code,
                observed_at=event.observed_at,
                received_at=now,
                payload_digest=event.payload_digest,
                safe_detail_code=event.safe_detail_code,
            )
            .on_conflict_do_nothing(
                index_elements=[
                    EmailProviderEventRow.provider_code,
                    EmailProviderEventRow.provider_event_id,
                ]
            )
            .returning(EmailProviderEventRow.email_provider_event_ref)
        )
        if inserted is None:
            return False

        if event.permanent_suppression_reason is not None:
            await self._apply_suppression(
                database_session,
                intent=intent,
                source_event_ref=event_ref,
                reason_code=event.permanent_suppression_reason,
                observed_at=event.observed_at,
            )
        return True

    async def _apply_suppression(
        self,
        database_session: AsyncSession,
        *,
        intent: EmailDeliveryIntentRow,
        source_event_ref: UUID,
        reason_code: str,
        observed_at: datetime,
    ) -> None:
        await database_session.execute(
            pg_insert(EmailRecipientSuppressionRow)
            .values(
                email_recipient_suppression_ref=uuid7(),
                recipient_comparison_key=intent.recipient_comparison_key,
                reason_code=reason_code,
                source_provider_event_ref=source_event_ref,
                suppressed_at=observed_at,
                updated_at=observed_at,
                cleared_at=None,
            )
            .on_conflict_do_update(
                index_elements=[EmailRecipientSuppressionRow.recipient_comparison_key],
                set_={
                    "reason_code": reason_code,
                    "source_provider_event_ref": source_event_ref,
                    "updated_at": observed_at,
                    "cleared_at": None,
                },
                where=EmailRecipientSuppressionRow.updated_at <= observed_at,
            )
        )
        await database_session.execute(
            update(EmailIdentityRow)
            .where(
                EmailIdentityRow.comparison_key == intent.recipient_comparison_key,
                (
                    EmailIdentityRow.recovery_restriction_observed_at.is_(None)
                    | (EmailIdentityRow.recovery_restriction_observed_at <= observed_at)
                ),
            )
            .values(
                recovery_restriction_code="provider_delivery_disabled",
                recovery_restriction_observed_at=observed_at,
            )
        )


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, dict) else {}


def _intent_ref_from_tags(tags: Mapping[str, Any]) -> UUID | None:
    value = tags.get("dante_intent")
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    if not isinstance(value, str):
        return None
    try:
        return UUID(value)
    except ValueError:
        return None


def _event_timestamp(*, detail: Mapping[str, Any], mail: Mapping[str, Any]) -> datetime:
    candidates: list[object] = [
        detail.get("timestamp"),
        mail.get("timestamp"),
    ]
    for value in candidates:
        if not isinstance(value, str):
            continue
        candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(candidate)
        except ValueError:
            continue
        if parsed.tzinfo is not None:
            return parsed.astimezone(UTC)
    raise SesFeedbackError("SES event has no valid timezone-aware timestamp")
