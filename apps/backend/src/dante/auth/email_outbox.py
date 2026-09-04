"""Access/Auth adapter over the shared DANTE Email Platform outbox."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from dante.auth.email_delivery import DeliverableEmail, NoopEmail
from dante.auth.email_render import (
    AUTH_EMAIL_STREAM,
    AUTH_EMAIL_TEMPLATE_REVISION,
    email_intent_spec,
)
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.outbox import DurableEmailOutbox as SharedDurableEmailOutbox


class DurableEmailOutbox(SharedDurableEmailOutbox):
    """Compatibility adapter that stages typed Auth commands into the shared outbox.

    Delivery lifecycle, claims, provider outcomes, recovery quarantine and persistence mechanics
    are owned by ``dante.platform.email``. This class owns only the conversion from one
    Access/Auth command to its consumer-specific immutable intent semantics.
    """

    async def stage(
        self,
        database_session: AsyncSession,
        *,
        command: DeliverableEmail | NoopEmail,
        operation_scope: str,
        idempotency_key: str,
        expires_at: datetime,
        supersession_key: str | None = None,
        locale_code: str = "en",
        eligible_at: datetime | None = None,
    ) -> UUID | None:
        """Stage one Auth/security command without performing provider network I/O."""
        if isinstance(command, NoopEmail):
            return None
        return await super().stage(
            database_session,
            spec=email_intent_spec(command),
            stream_code=AUTH_EMAIL_STREAM,
            template_revision=AUTH_EMAIL_TEMPLATE_REVISION,
            operation_scope=operation_scope,
            idempotency_key=idempotency_key,
            expires_at=expires_at,
            supersession_key=supersession_key,
            locale_code=locale_code,
            eligible_at=eligible_at,
        )


__all__ = ["DurableEmailOutbox", "EmailPayloadCipher"]
