"""Amazon SES feedback normalization and idempotent DANTE persistence."""

from __future__ import annotations

import json
import logging
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any
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

_LOGGER = logging.getLogger(__name__)
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
class NormalizedSesFeedback:
    """Safe normalized provider observation without raw message content or headers."""

    provider_event_ref: UUID
    provider_event_id: str
    provider_message_id: str
    event_type_code: str
    provider_occurred_at: datetime
    payload_digest: bytes
    safe_subtype_code: str | None
    hard_failure: bool


def normalize_ses_feedback(payload: bytes | str | Mapping[str, Any]) -> NormalizedSesFeedback:
    """Normalize one bounded SES event envelope and reject malformed/unsupported input."""
    if isinstance(payload, Mapping):
        raw: Mapping[str, Any] = payload
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    else:
        encoded = payload.encode("utf-8") if isinstance(payload, str) else payload
        if len(encoded) > _MAX_EVENT_BYTES:
            raise SesFeedbackError("SES feedback exceeds admission bound")
        try:
            parsed = json.loads(encoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SesFeedbackError("SES feedback is not valid JSON") from exc
        if not isinstance(parsed, Mapping):
            raise SesFeedbackError("SES feedback root must be an object")
        raw = parsed

    if len(encoded) > _MAX_EVENT_BYTES:
        raise SesFeedbackError("SES feedback exceeds admission bound")

    event_type = raw.get("eventType")
    if not isinstance(event_type, str) or event_type not in _SUPPORTED_EVENTS:
        raise SesFeedbackError("SES feedback event type is unsupported")
    event_type_code = _SUPPORTED_EVENTS[event_type]

    mail = raw.get("mail")
    if not isinstance(mail, Mapping):
        raise SesFeedbackError("SES feedback mail envelope is missing")
    message_id = mail.get("messageId")
    if not isinstance(message_id, str) or not message_id.strip():
        raise SesFeedbackError("SES feedback messageId is missing")

    timestamp_value = mail.get("timestamp")
    if not isinstance(timestamp_value, str):
        raise SesFeedbackError("SES feedback mail timestamp is missing")
    try:
        occurred_at = datetime.fromisoformat(timestamp_value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SesFeedbackError("SES feedback timestamp is invalid") from exc
    if occurred_at.tzinfo is None:
        raise SesFeedbackError("SES feedback timestamp must be timezone-aware")
    occurred_at = occurred_at.astimezone(UTC)

    return NormalizedSesFeedback(
        provider_event_ref=uuid7(),
        provider_event_id=_provider_event_id(raw, encoded),
        provider_message_id=message_id,
        event_type_code=event_type_code,
        provider_occurred_at=occurred_at,
        payload_digest=sha256(encoded).digest(),
        safe_subtype_code=_safe_subtype(raw, event_type),
        hard_failure=_is_hard_failure(raw, event_type),
    )


class EmailFeedbackStore:
    """Idempotently persist SES observations and current delivery suppression projection."""

    async def record(
        self,
        database_session: AsyncSession,
        *,
        feedback: NormalizedSesFeedback,
    ) -> bool:
        """Record one SES observation; return False only when correlation is not yet known."""
        attempt = await database_session.scalar(
            select(EmailDeliveryAttemptRow).where(
                EmailDeliveryAttemptRow.provider_message_id == feedback.provider_message_id
            )
        )
        if attempt is None or attempt.provider_code != "ses":
            _LOGGER.warning(
                "auth.email_feedback_uncorrelated provider=ses event_type=%s",
                feedback.event_type_code,
            )
            return False

        insert_stmt = (
            pg_insert(EmailProviderEventRow)
            .values(
                email_provider_event_ref=feedback.provider_event_ref,
                provider_code="ses",
                provider_event_id=feedback.provider_event_id,
                provider_message_id=feedback.provider_message_id,
                email_intent_ref=attempt.email_intent_ref,
                event_type_code=feedback.event_type_code,
                observed_at=feedback.provider_occurred_at,
                received_at=datetime.now(UTC),
                payload_digest=feedback.payload_digest,
                safe_detail_code=feedback.safe_subtype_code,
            )
            .on_conflict_do_nothing(
                index_elements=[
                    EmailProviderEventRow.provider_code,
                    EmailProviderEventRow.provider_event_id,
                ]
            )
            .returning(EmailProviderEventRow.email_provider_event_ref)
        )
        inserted_event_ref = await database_session.scalar(insert_stmt)
        if inserted_event_ref is None:
            return True

        if feedback.event_type_code in {"bounced", "complained"}:
            await self._apply_suppression(
                database_session,
                attempt=attempt,
                feedback=feedback,
                source_provider_event_ref=inserted_event_ref,
            )

        _LOGGER.info(
            "auth.email_feedback_recorded provider=ses event_type=%s hard_failure=%s intent_ref=%s",
            feedback.event_type_code,
            feedback.hard_failure,
            attempt.email_intent_ref,
        )
        return True

    async def _apply_suppression(
        self,
        database_session: AsyncSession,
        *,
        attempt: EmailDeliveryAttemptRow,
        feedback: NormalizedSesFeedback,
        source_provider_event_ref: UUID,
    ) -> None:
        intent = await database_session.scalar(
            select(EmailDeliveryIntentRow).where(
                EmailDeliveryIntentRow.email_intent_ref == attempt.email_intent_ref
            )
        )
        if intent is None:
            return

        if feedback.event_type_code == "complained":
            reason_code = "complaint"
        elif feedback.hard_failure:
            reason_code = "hard_bounce"
        else:
            return

        now = datetime.now(UTC)
        suppression_stmt = (
            pg_insert(EmailRecipientSuppressionRow)
            .values(
                email_recipient_suppression_ref=uuid7(),
                recipient_comparison_key=intent.recipient_comparison_key,
                reason_code=reason_code,
                source_provider_event_ref=source_provider_event_ref,
                suppressed_at=feedback.provider_occurred_at,
                updated_at=now,
                cleared_at=None,
            )
            .on_conflict_do_update(
                index_elements=[EmailRecipientSuppressionRow.recipient_comparison_key],
                set_={
                    "reason_code": reason_code,
                    "source_provider_event_ref": source_provider_event_ref,
                    "suppressed_at": feedback.provider_occurred_at,
                    "updated_at": now,
                    "cleared_at": None,
                },
            )
        )
        await database_session.execute(suppression_stmt)
        await database_session.execute(
            update(EmailIdentityRow)
            .where(EmailIdentityRow.comparison_key == intent.recipient_comparison_key)
            .values(
                recovery_restriction_code="provider_delivery_disabled",
                recovery_restriction_observed_at=feedback.provider_occurred_at,
            )
        )


def _provider_event_id(raw: Mapping[str, Any], encoded: bytes) -> str:
    for key in ("eventId", "id"):
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return sha256(encoded).hexdigest()


def _safe_subtype(raw: Mapping[str, Any], event_type: str) -> str | None:
    key = {
        "Bounce": "bounce",
        "Complaint": "complaint",
        "DeliveryDelay": "deliveryDelay",
        "Reject": "reject",
    }.get(event_type)
    section = raw.get(key) if key is not None else None
    if not isinstance(section, Mapping):
        return None
    for candidate in (
        "bounceType",
        "bounceSubType",
        "complaintFeedbackType",
        "delayType",
        "reason",
    ):
        value = section.get(candidate)
        if isinstance(value, str) and value.strip():
            return value[:128]
    return None


def _is_hard_failure(raw: Mapping[str, Any], event_type: str) -> bool:
    if event_type == "Complaint":
        return True
    if event_type != "Bounce":
        return False
    bounce = raw.get("bounce")
    return isinstance(bounce, Mapping) and bounce.get("bounceType") == "Permanent"
