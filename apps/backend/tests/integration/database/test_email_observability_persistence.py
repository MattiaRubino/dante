"""Real PostgreSQL proof for privacy-minimized durable Email Platform observability."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from pydantic import SecretStr

from dante.auth.email_contracts import ProviderOutcome, ProviderSendResult
from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_delivery import SignupVerificationEmail
from dante.auth.email_feedback import EmailFeedbackStore, normalize_ses_feedback
from dante.auth.email_observability import EmailObservabilityProbe
from dante.auth.email_outbox import DurableEmailOutbox
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres

_KEY_ID = "email-observability-v1"
_KEY = b"m" * 32


def _outbox() -> DurableEmailOutbox:
    return DurableEmailOutbox(
        cipher=EmailPayloadCipher(key_ring={_KEY_ID: _KEY}, current_key_id=_KEY_ID),
        attempt_limit=3,
    )


async def _stage_signup(
    runtime: Any,
    outbox: DurableEmailOutbox,
    *,
    idempotency_key: str,
) -> Any:
    async with runtime.session_factory() as session, session.begin():
        intent_ref = await outbox.stage(
            session,
            command=SignupVerificationEmail(
                to_address=f"{idempotency_key}@example.com",
                code=SecretStr("482913"),
                expires_minutes=10,
            ),
            operation_scope="observability-signup",
            idempotency_key=idempotency_key,
            expires_at=datetime.now(UTC) + timedelta(minutes=10),
        )
    assert intent_ref is not None
    return intent_ref


@pytest.mark.asyncio
async def test_email_operational_snapshot_uses_durable_truth_without_pii_dimensions(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()
    feedback_store = EmailFeedbackStore()

    try:
        accepted_ref = await _stage_signup(runtime, outbox, idempotency_key="accepted")
        async with runtime.session_factory() as session, session.begin():
            accepted_claim = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=30,
                )
            )[0]
        assert accepted_claim.email_intent_ref == accepted_ref
        async with runtime.session_factory() as session, session.begin():
            assert await outbox.finalize(
                session,
                claim=accepted_claim,
                result=ProviderSendResult(
                    outcome=ProviderOutcome.ACCEPTED,
                    provider_message_id="observability-accepted-message",
                ),
            )

        ambiguous_ref = await _stage_signup(runtime, outbox, idempotency_key="ambiguous")
        async with runtime.session_factory() as session, session.begin():
            ambiguous_claim = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=30,
                )
            )[0]
        assert ambiguous_claim.email_intent_ref == ambiguous_ref
        async with runtime.session_factory() as session, session.begin():
            assert await outbox.finalize(
                session,
                claim=ambiguous_claim,
                result=ProviderSendResult(
                    outcome=ProviderOutcome.AMBIGUOUS,
                    safe_error_code="ReadTimeoutError",
                ),
            )

        observed_at = datetime.now(UTC)
        feedback = normalize_ses_feedback(
            {
                "eventType": "Bounce",
                "eventId": "observability-hard-bounce",
                "mail": {
                    "messageId": "observability-accepted-message",
                    "timestamp": observed_at.isoformat().replace("+00:00", "Z"),
                },
                "bounce": {"bounceType": "Permanent", "bounceSubType": "General"},
            }
        )
        async with runtime.session_factory() as session, session.begin():
            assert await feedback_store.record(session, feedback=feedback)

        await _stage_signup(runtime, outbox, idempotency_key="pending")

        probe = EmailObservabilityProbe(session_factory=runtime.session_factory)
        snapshot = await probe.snapshot(window_seconds=3600)

        assert snapshot.backlog_count == 1
        assert snapshot.oldest_backlog_age_seconds is not None
        assert snapshot.oldest_backlog_age_seconds >= 0
        assert snapshot.provider_accepted_count == 1
        assert snapshot.ambiguous_count == 1
        assert snapshot.retryable_failure_count == 0
        assert snapshot.definitive_failure_count == 0
        assert snapshot.accepted_send_latency_avg_seconds is not None
        assert snapshot.accepted_send_latency_avg_seconds >= 0
        assert snapshot.accepted_send_latency_max_seconds is not None
        assert snapshot.accepted_send_latency_max_seconds >= 0
        assert snapshot.active_hard_bounce_suppressions == 1
        assert snapshot.active_complaint_suppressions == 0

        metric_names = set(asdict(snapshot))
        forbidden_fragments = {"recipient", "address", "email", "secret", "payload", "message"}
        assert not any(
            fragment in metric_name
            for metric_name in metric_names
            for fragment in forbidden_fragments
        )
    finally:
        await runtime.dispose()
