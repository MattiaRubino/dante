"""PostgreSQL replay checks for the shared Email Platform."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from dante.platform.database.runtime import create_database_runtime
from dante.platform.email.contracts import EmailIntentConflictError, EmailIntentSpec
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.outbox import DurableEmailOutbox

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_replay_requires_same_recipient_and_stream(migrated_database: Any) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    outbox = DurableEmailOutbox(
        cipher=EmailPayloadCipher(key_ring={"k1": b"x" * 32}, current_key_id="k1"),
        attempt_limit=3,
    )
    expires_at = datetime.now(UTC) + timedelta(minutes=10)
    original = EmailIntentSpec(
        purpose_code="signup_verification",
        template_code="auth.signup_verification",
        payload={"code": "123456", "expires_minutes": 10},
        recipient_address="one@example.com",
        recipient_comparison_key="one@example.com",
    )

    try:
        async with runtime.session_factory() as session, session.begin():
            original_ref = await outbox.stage(
                session,
                spec=original,
                stream_code="auth_security",
                template_revision="2",
                operation_scope="test.replay",
                idempotency_key="replay-1",
                expires_at=expires_at,
            )

        async with runtime.session_factory() as session, session.begin():
            replay_ref = await outbox.stage(
                session,
                spec=original,
                stream_code="auth_security",
                template_revision="2",
                operation_scope="test.replay",
                idempotency_key="replay-1",
                expires_at=expires_at + timedelta(minutes=1),
            )
        assert replay_ref == original_ref

        changed_recipient = EmailIntentSpec(
            purpose_code=original.purpose_code,
            template_code=original.template_code,
            payload=original.payload,
            recipient_address="two@example.com",
            recipient_comparison_key="two@example.com",
        )
        with pytest.raises(EmailIntentConflictError):
            async with runtime.session_factory() as session, session.begin():
                await outbox.stage(
                    session,
                    spec=changed_recipient,
                    stream_code="auth_security",
                    template_revision="2",
                    operation_scope="test.replay",
                    idempotency_key="replay-1",
                    expires_at=expires_at,
                )

        with pytest.raises(EmailIntentConflictError):
            async with runtime.session_factory() as session, session.begin():
                await outbox.stage(
                    session,
                    spec=original,
                    stream_code="other_stream",
                    template_revision="2",
                    operation_scope="test.replay",
                    idempotency_key="replay-1",
                    expires_at=expires_at,
                )
    finally:
        await runtime.dispose()
