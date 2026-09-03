"""Real PostgreSQL acceptance proof for the bounded M5 Email Platform."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from pydantic import SecretStr
from sqlalchemy import func, select

from dante.auth.email_contracts import (
    EmailIntentConflictError,
    ProviderOutcome,
    ProviderSendResult,
)
from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_delivery import PasswordRecoveryEmail, SignupVerificationEmail
from dante.auth.email_feedback import EmailFeedbackStore, normalize_ses_feedback
from dante.auth.email_outbox import DurableEmailOutbox
from dante.platform.database.mappings.auth import AccountRow, EmailIdentityRow
from dante.platform.database.mappings.email_delivery import (
    EmailDeliveryAttemptRow,
    EmailDeliveryIntentRow,
    EmailProviderEventRow,
    EmailRecipientSuppressionRow,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres

_KEY_ID = "email-test-v1"
_KEY = bytes(range(32))


def _outbox() -> DurableEmailOutbox:
    return DurableEmailOutbox(
        cipher=EmailPayloadCipher(key_ring={_KEY_ID: _KEY}, current_key_id=_KEY_ID),
        attempt_limit=3,
    )


def _cipher() -> EmailPayloadCipher:
    return EmailPayloadCipher(key_ring={_KEY_ID: _KEY}, current_key_id=_KEY_ID)


def test_email_runtime_acl_is_least_privilege(migrated_database: Any) -> None:
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            migrated_database.cluster.admin_user,
            migrated_database.cluster.admin_password,
        )
    ) as connection:
        table_acl = connection.execute(
            """
            SELECT
              has_table_privilege('dante_runtime','dante.email_delivery_intent','SELECT'),
              has_table_privilege('dante_runtime','dante.email_delivery_intent','INSERT'),
              has_table_privilege('dante_runtime','dante.email_delivery_intent','UPDATE'),
              has_table_privilege('dante_runtime','dante.email_delivery_intent','DELETE'),
              has_table_privilege('dante_runtime','dante.email_delivery_attempt','SELECT'),
              has_table_privilege('dante_runtime','dante.email_delivery_attempt','INSERT'),
              has_table_privilege('dante_runtime','dante.email_delivery_attempt','UPDATE'),
              has_table_privilege('dante_runtime','dante.email_delivery_attempt','DELETE'),
              has_table_privilege('dante_runtime','dante.email_provider_event','SELECT'),
              has_table_privilege('dante_runtime','dante.email_provider_event','INSERT'),
              has_table_privilege('dante_runtime','dante.email_provider_event','UPDATE'),
              has_table_privilege('dante_runtime','dante.email_provider_event','DELETE'),
              has_table_privilege('dante_runtime','dante.email_recipient_suppression','SELECT'),
              has_table_privilege('dante_runtime','dante.email_recipient_suppression','INSERT'),
              has_table_privilege('dante_runtime','dante.email_recipient_suppression','UPDATE'),
              has_table_privilege('dante_runtime','dante.email_recipient_suppression','DELETE')
            """
        ).fetchone()
        column_acl = connection.execute(
            """
            SELECT
              has_column_privilege('dante_runtime','dante.email_delivery_intent','dispatch_state_code','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_delivery_intent','sensitive_ciphertext','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_delivery_intent','recipient_address','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_delivery_intent','idempotency_key','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_delivery_attempt','result_code','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_delivery_attempt','provider_message_id','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_delivery_attempt','email_intent_ref','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_recipient_suppression','reason_code','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_recipient_suppression','cleared_at','UPDATE'),
              has_column_privilege('dante_runtime','dante.email_recipient_suppression','recipient_comparison_key','UPDATE')
            """
        ).fetchone()

    assert table_acl == (
        True,
        True,
        False,
        False,
        True,
        True,
        False,
        False,
        True,
        True,
        False,
        False,
        True,
        True,
        False,
        False,
    )
    assert column_acl == (True, True, False, False, True, True, False, True, True, False)


@pytest.mark.asyncio
async def test_outbox_idempotency_acceptance_and_sensitive_wipe(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()
    command = SignupVerificationEmail(
        to_address="Email.Platform@example.com",
        code=SecretStr("482913"),
        expires_minutes=10,
    )
    expires_at = datetime.now(UTC) + timedelta(minutes=10)

    try:
        async with runtime.session_factory() as session, session.begin():
            first_ref = await outbox.stage(
                session,
                command=command,
                operation_scope="signup-verification",
                idempotency_key="signup-1:revision-1",
                expires_at=expires_at,
                supersession_key="signup-1",
            )
        assert first_ref is not None

        async with runtime.session_factory() as session, session.begin():
            replay_ref = await outbox.stage(
                session,
                command=command,
                operation_scope="signup-verification",
                idempotency_key="signup-1:revision-1",
                expires_at=expires_at,
                supersession_key="signup-1",
            )
        assert replay_ref == first_ref

        changed = SignupVerificationEmail(
            to_address="Email.Platform@example.com",
            code=SecretStr("111111"),
            expires_minutes=10,
        )
        with pytest.raises(EmailIntentConflictError):
            async with runtime.session_factory() as session, session.begin():
                await outbox.stage(
                    session,
                    command=changed,
                    operation_scope="signup-verification",
                    idempotency_key="signup-1:revision-1",
                    expires_at=expires_at,
                    supersession_key="signup-1",
                )

        async with runtime.session_factory() as session, session.begin():
            row = await session.get(EmailDeliveryIntentRow, first_ref)
            assert row is not None
            assert row.sensitive_ciphertext is not None
            assert b"482913" not in row.sensitive_ciphertext
            assert row.dispatch_state_code == "pending"

        async with runtime.session_factory() as session, session.begin():
            claims = await outbox.claim_batch(
                session,
                provider_code="ses",
                batch_size=10,
                lease_seconds=30,
            )
        assert len(claims) == 1
        claim = claims[0]
        assert claim.email_intent_ref == first_ref

        async with runtime.session_factory() as session, session.begin():
            finalized = await outbox.finalize(
                session,
                claim=claim,
                result=ProviderSendResult(
                    outcome=ProviderOutcome.ACCEPTED,
                    provider_message_id="ses-message-accepted-1",
                ),
            )
        assert finalized is True

        async with runtime.session_factory() as session, session.begin():
            row = await session.get(EmailDeliveryIntentRow, first_ref)
            attempt = await session.get(EmailDeliveryAttemptRow, claim.email_attempt_ref)
            assert row is not None
            assert attempt is not None
            assert row.dispatch_state_code == "provider_accepted"
            assert row.accepted_at is not None
            assert row.terminal_at is not None
            assert row.sensitive_key_id is None
            assert row.sensitive_nonce is None
            assert row.sensitive_ciphertext is None
            assert row.sensitive_wiped_at is not None
            assert attempt.result_code == "provider_accepted"
            assert attempt.provider_message_id == "ses-message-accepted-1"

            no_replay = await outbox.claim_batch(
                session,
                provider_code="ses",
                batch_size=10,
                lease_seconds=30,
            )
            assert no_replay == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_ambiguous_result_and_expired_lease_never_blind_retry(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()
    now = datetime.now(UTC)

    try:
        async with runtime.session_factory() as session, session.begin():
            ambiguous_ref = await outbox.stage(
                session,
                command=PasswordRecoveryEmail(
                    to_address="ambiguous@example.com",
                    password_recovery_ref=uuid7(),
                    secret=SecretStr("recovery-secret-ambiguous"),
                ),
                operation_scope="password-recovery",
                idempotency_key="recovery-ambiguous",
                expires_at=now + timedelta(minutes=20),
            )
        assert ambiguous_ref is not None

        async with runtime.session_factory() as session, session.begin():
            claim = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=30,
                    now=now + timedelta(seconds=1),
                )
            )[0]
        async with runtime.session_factory() as session, session.begin():
            assert await outbox.finalize(
                session,
                claim=claim,
                result=ProviderSendResult(
                    outcome=ProviderOutcome.AMBIGUOUS,
                    safe_error_code="ReadTimeoutError",
                ),
                now=now + timedelta(seconds=2),
            )

        async with runtime.session_factory() as session, session.begin():
            ambiguous = await session.get(EmailDeliveryIntentRow, ambiguous_ref)
            assert ambiguous is not None
            assert ambiguous.dispatch_state_code == "ambiguous"
            assert ambiguous.next_attempt_at is None
            assert ambiguous.sensitive_ciphertext is None

            assert (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=10,
                    lease_seconds=30,
                    now=now + timedelta(seconds=3),
                )
                == []
            )

        async with runtime.session_factory() as session, session.begin():
            lease_ref = await outbox.stage(
                session,
                command=SignupVerificationEmail(
                    to_address="lease@example.com",
                    code=SecretStr("731842"),
                    expires_minutes=10,
                ),
                operation_scope="signup-verification",
                idempotency_key="lease-expiry",
                expires_at=datetime.now(UTC) + timedelta(minutes=10),
            )
        assert lease_ref is not None

        claim_time = datetime.now(UTC)
        async with runtime.session_factory() as session, session.begin():
            lease_claim = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=1,
                    now=claim_time,
                )
            )[0]
            assert lease_claim.email_intent_ref == lease_ref

        async with runtime.session_factory() as session, session.begin():
            assert (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=10,
                    lease_seconds=30,
                    now=claim_time + timedelta(seconds=2),
                )
                == []
            )
            lease_row = await session.get(EmailDeliveryIntentRow, lease_ref)
            assert lease_row is not None
            assert lease_row.dispatch_state_code == "ambiguous"
            assert lease_row.last_error_code == "claim_lease_expired"
            assert lease_row.sensitive_ciphertext is None
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_skip_locked_claiming_has_one_owner(migrated_database: Any) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()

    try:
        async with runtime.session_factory() as session, session.begin():
            intent_ref = await outbox.stage(
                session,
                command=SignupVerificationEmail(
                    to_address="claim@example.com",
                    code=SecretStr("284615"),
                    expires_minutes=10,
                ),
                operation_scope="signup-verification",
                idempotency_key="claim-race",
                expires_at=datetime.now(UTC) + timedelta(minutes=10),
            )
        assert intent_ref is not None

        async def claim_once() -> list[Any]:
            async with runtime.session_factory() as session, session.begin():
                return await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=30,
                )

        left, right = await asyncio.gather(claim_once(), claim_once())
        claims = [*left, *right]
        assert len(claims) == 1
        assert claims[0].email_intent_ref == intent_ref
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_feedback_is_idempotent_and_suppresses_future_claims(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()
    feedback_store = EmailFeedbackStore()
    created_at = datetime.now(UTC) - timedelta(seconds=1)
    account_ref = uuid7()
    email_identity_ref = uuid7()
    address = "suppressed@example.com"

    try:
        async with runtime.session_factory() as session, session.begin():
            session.add(
                AccountRow(
                    account_ref=account_ref,
                    status_code="active",
                    created_at=created_at,
                    disabled_at=None,
                )
            )
            session.add(
                EmailIdentityRow(
                    email_identity_ref=email_identity_ref,
                    account_ref=account_ref,
                    address=address,
                    comparison_key=address,
                    created_at=created_at,
                    verified_at=created_at,
                    recovery_restriction_code=None,
                    recovery_restriction_observed_at=None,
                )
            )
            intent_ref = await outbox.stage(
                session,
                command=PasswordRecoveryEmail(
                    to_address=address,
                    password_recovery_ref=uuid7(),
                    secret=SecretStr("recovery-secret-before-bounce"),
                ),
                operation_scope="password-recovery",
                idempotency_key="bounce-source",
                expires_at=datetime.now(UTC) + timedelta(minutes=20),
            )
        assert intent_ref is not None

        async with runtime.session_factory() as session, session.begin():
            claim = (
                await outbox.claim_batch(
                    session,
                    provider_code="ses",
                    batch_size=1,
                    lease_seconds=30,
                )
            )[0]
        async with runtime.session_factory() as session, session.begin():
            assert await outbox.finalize(
                session,
                claim=claim,
                result=ProviderSendResult(
                    outcome=ProviderOutcome.ACCEPTED,
                    provider_message_id="ses-bounce-message-1",
                ),
            )

        observed_at = datetime.now(UTC)
        normalized = normalize_ses_feedback(
            {
                "eventType": "Bounce",
                "eventId": "ses-event-hard-bounce-1",
                "mail": {
                    "messageId": "ses-bounce-message-1",
                    "timestamp": observed_at.isoformat().replace("+00:00", "Z"),
                },
                "bounce": {
                    "bounceType": "Permanent",
                    "bounceSubType": "General",
                },
            }
        )
        async with runtime.session_factory() as session, session.begin():
            assert await feedback_store.record(session, feedback=normalized)
        async with runtime.session_factory() as session, session.begin():
            assert await feedback_store.record(session, feedback=normalized)

        async with runtime.session_factory() as session, session.begin():
            event_count = await session.scalar(select(func.count()).select_from(EmailProviderEventRow))
            suppression = await session.scalar(
                select(EmailRecipientSuppressionRow).where(
                    EmailRecipientSuppressionRow.recipient_comparison_key == address
                )
            )
            identity = await session.get(EmailIdentityRow, email_identity_ref)
            assert event_count == 1
            assert suppression is not None
            assert suppression.reason_code == "hard_bounce"
            assert suppression.cleared_at is None
            assert identity is not None
            assert identity.recovery_restriction_code == "provider_delivery_disabled"
            assert identity.recovery_restriction_observed_at == observed_at

            blocked_ref = await outbox.stage(
                session,
                command=PasswordRecoveryEmail(
                    to_address=address,
                    password_recovery_ref=uuid7(),
                    secret=SecretStr("recovery-secret-after-bounce"),
                ),
                operation_scope="password-recovery",
                idempotency_key="blocked-by-suppression",
                expires_at=datetime.now(UTC) + timedelta(minutes=20),
            )
            assert blocked_ref is not None

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


@pytest.mark.asyncio
async def test_post_restore_quarantine_wipes_pending_sensitive_material(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = _outbox()

    try:
        async with runtime.session_factory() as session, session.begin():
            intent_ref = await outbox.stage(
                session,
                command=SignupVerificationEmail(
                    to_address="restore@example.com",
                    code=SecretStr("934271"),
                    expires_minutes=10,
                ),
                operation_scope="signup-verification",
                idempotency_key="restore-quarantine",
                expires_at=datetime.now(UTC) + timedelta(minutes=10),
            )
        assert intent_ref is not None

        async with runtime.session_factory() as session, session.begin():
            assert await outbox.quarantine_after_restore(session) == 1

        async with runtime.session_factory() as session, session.begin():
            row = await session.get(EmailDeliveryIntentRow, intent_ref)
            assert row is not None
            assert row.dispatch_state_code == "recovery_quarantined"
            assert row.last_error_code == "post_restore_quarantine"
            assert row.sensitive_key_id is None
            assert row.sensitive_nonce is None
            assert row.sensitive_ciphertext is None
            assert row.sensitive_wiped_at is not None
    finally:
        await runtime.dispose()
