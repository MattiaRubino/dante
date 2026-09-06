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
from dante.platform.email.contracts import ClaimedEmailIntent, ProviderSendResult
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.outbox import DurableEmailOutbox as SharedDurableEmailOutbox


class DurableEmailOutbox:
    """Auth consumer adapter around the shared durable outbox.

    The wrapped platform object owns every delivery lifecycle mechanic. This adapter owns only
    Auth command-to-intent conversion and preserves the historical Auth-facing API while the
    shared platform remains import-independent from ``dante.auth``.
    """

    def __init__(self, *, cipher: EmailPayloadCipher, attempt_limit: int) -> None:
        self._core = SharedDurableEmailOutbox(cipher=cipher, attempt_limit=attempt_limit)

    @classmethod
    def from_shared(cls, core: SharedDurableEmailOutbox) -> DurableEmailOutbox:
        """Bind Auth staging to an already constructed shared outbox instance."""
        instance = cls.__new__(cls)
        instance._core = core
        return instance

    @property
    def core(self) -> SharedDurableEmailOutbox:
        """Expose the shared worker/recovery mechanic without transferring ownership to Auth."""
        return self._core

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
        return await self._core.stage(
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

    async def claim_batch(
        self,
        database_session: AsyncSession,
        *,
        provider_code: str,
        batch_size: int,
        lease_seconds: float,
        now: datetime | None = None,
    ) -> list[ClaimedEmailIntent]:
        """Compatibility delegation to shared claim mechanics."""
        return await self._core.claim_batch(
            database_session,
            provider_code=provider_code,
            batch_size=batch_size,
            lease_seconds=lease_seconds,
            now=now,
        )

    async def claim_still_owned(
        self,
        database_session: AsyncSession,
        *,
        claim: ClaimedEmailIntent,
        now: datetime | None = None,
    ) -> bool:
        """Compatibility delegation to shared lease ownership verification."""
        return await self._core.claim_still_owned(database_session, claim=claim, now=now)

    async def finalize(
        self,
        database_session: AsyncSession,
        *,
        claim: ClaimedEmailIntent,
        result: ProviderSendResult,
        now: datetime | None = None,
        retry_delay_seconds: float = 0,
    ) -> bool:
        """Compatibility delegation to shared provider-outcome finalization."""
        return await self._core.finalize(
            database_session,
            claim=claim,
            result=result,
            now=now,
            retry_delay_seconds=retry_delay_seconds,
        )

    async def quarantine_after_restore(
        self,
        database_session: AsyncSession,
        *,
        now: datetime | None = None,
    ) -> int:
        """Compatibility delegation to shared post-restore quarantine."""
        return await self._core.quarantine_after_restore(database_session, now=now)


__all__ = ["DurableEmailOutbox", "EmailPayloadCipher"]
