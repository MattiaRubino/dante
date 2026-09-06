"""Real PostgreSQL proof for Email post-restore quarantine and reopen safety."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from sqlalchemy import select

from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
)
from dante.platform.database.runtime import create_database_runtime
from dante.platform.email.contracts import EmailIntentSpec, ProviderOutcome, ProviderSendResult
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.outbox import DurableEmailOutbox
from dante.platform.recovery.email_post_restore import reconcile_restored_email_delivery

pytestmark = pytest.mark.postgres

_KEY_ID = "recovery-email-test-v1"
_KEY = bytes(range(32))


def _outbox() -> DurableEmailOutbox:
    return DurableEmailOutbox(
        cipher=EmailPayloadCipher(key_ring={_KEY_ID: _KEY}, current_key_id=_KEY_ID),
        attempt_limit=3,
    )


def _spec(name: str) -> EmailIntentSpec:
    address = f"recovery-{name}@example.com"
    return EmailIntentSpec(
        purpose_code="recovery_probe",
        template_code="recovery_probe",
        payload={"fixture": name, "secret": f"secret-{name}"},
        recipient_address=address,
        recipient_comparison_key=address,
    )


@pytest.mark.asyncio
async def test_post_restore_reconciliation_quarantines_every_sendable_state_and_attempt(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()

    try:
        async with runtime.session_factory() as session, session.begin():
            claimed_ref = await outbox.stage(
                session,
                spec=_spec("claimed"),
                stream_code="security",
                template_revision="1",
                operation_scope="recovery-probe",
                idempotency_key="claimed",
                expires_at=datetime.now(UTC) + timedelta(hours=1),
            )

        async with runtime.session_factory() as session, session.begin():
            claimed = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=300,
                )
            )[0]
        assert claimed.email_intent_ref == claimed_ref

        async with runtime.session_factory() as session, session.begin():
            retryable_ref = await outbox.stage(
                session,
                spec=_spec("retryable"),
                stream_code="security",
                template_revision="1",
                operation_scope="recovery-probe",
                idempotency_key="retryable",
                expires_at=datetime.now(UTC) + timedelta(hours=1),
            )

        async with runtime.session_factory() as session, session.begin():
            retryable_claim = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=300,
                )
            )[0]
        assert retryable_claim.email_intent_ref == retryable_ref

        async with runtime.session_factory() as session, session.begin():
            assert await outbox.finalize(
                session,
                claim=retryable_claim,
                result=ProviderSendResult(
                    outcome=ProviderOutcome.RETRYABLE_FAILURE,
                    safe_error_code="temporary_provider_failure",
                ),
                retry_delay_seconds=3600,
            )

        async with runtime.session_factory() as session, session.begin():
            pending_ref = await outbox.stage(
                session,
                spec=_spec("pending"),
                stream_code="security",
                template_revision="1",
                operation_scope="recovery-probe",
                idempotency_key="pending",
                expires_at=datetime.now(UTC) + timedelta(hours=1),
                eligible_at=datetime.now(UTC) + timedelta(minutes=30),
            )

        async with runtime.session_factory() as session, session.begin():
            before = {
                row.email_intent_ref: row.dispatch_state_code
                for row in (
                    await session.scalars(
                        select(EmailDeliveryIntentRow).where(
                            EmailDeliveryIntentRow.email_intent_ref.in_(
                                (pending_ref, claimed_ref, retryable_ref)
                            )
                        )
                    )
                ).all()
            }
        assert before == {
            pending_ref: "pending",
            claimed_ref: "claimed",
            retryable_ref: "retryable_failure",
        }

        result = await reconcile_restored_email_delivery(runtime)
        assert result.quarantined_intent_count == 3
        assert result.ambiguous_attempt_count == 1
        assert result.remaining_sendable_intent_count == 0
        assert result.unsafe_quarantined_intent_count == 0
        assert result.in_progress_quarantined_attempt_count == 0

        async with runtime.session_factory() as session, session.begin():
            rows = (
                await session.scalars(
                    select(EmailDeliveryIntentRow).where(
                        EmailDeliveryIntentRow.email_intent_ref.in_(
                            (pending_ref, claimed_ref, retryable_ref)
                        )
                    )
                )
            ).all()
            assert len(rows) == 3
            for row in rows:
                assert row.dispatch_state_code == "recovery_quarantined"
                assert row.claim_token is None
                assert row.claimed_until is None
                assert row.next_attempt_at is None
                assert row.last_error_code == "post_restore_quarantine"
                assert row.terminal_at is not None
                assert row.sensitive_key_id is None
                assert row.sensitive_nonce is None
                assert row.sensitive_ciphertext is None
                assert row.sensitive_wiped_at is not None

            claimed_attempt = await session.get(
                EmailDeliveryAttemptRow,
                claimed.email_attempt_ref,
            )
            retryable_attempt = await session.get(
                EmailDeliveryAttemptRow,
                retryable_claim.email_attempt_ref,
            )
            assert claimed_attempt is not None
            assert claimed_attempt.result_code == "ambiguous"
            assert claimed_attempt.finished_at is not None
            assert claimed_attempt.error_code == "post_restore_quarantine"

            assert retryable_attempt is not None
            assert retryable_attempt.result_code == "retryable_failure"
            assert retryable_attempt.finished_at is not None
            assert retryable_attempt.error_code == "temporary_provider_failure"

        async with runtime.session_factory() as session, session.begin():
            assert (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=10,
                    lease_seconds=30,
                )
                == []
            )
    finally:
        await runtime.dispose()
