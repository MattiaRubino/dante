"""Process-scoped durable email workers over PostgreSQL outbox state."""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.email_contracts import (
    ClaimedEmailIntent,
    EmailPayloadError,
    EmailProviderPort,
    ProviderOutcome,
    ProviderSendResult,
)
from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_outbox import DurableEmailOutbox
from dante.auth.email_render import render_claim
from dante.platform.config.auth import AuthSettings

_LOGGER = logging.getLogger(__name__)


class EmailDeliveryWorkerPool:
    """Fixed bounded workers; PostgreSQL, not process memory, owns admitted work."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        outbox: DurableEmailOutbox,
        cipher: EmailPayloadCipher,
        provider: EmailProviderPort,
        settings: AuthSettings,
    ) -> None:
        self._session_factory = session_factory
        self._outbox = outbox
        self._cipher = cipher
        self._provider = provider
        self._settings = settings
        self._stop = asyncio.Event()
        self._wake = asyncio.Event()
        self._workers: list[asyncio.Task[None]] = []
        self._started = False
        self._closed = False

    async def start(self) -> None:
        """Start the configured fixed worker set once."""
        if self._started:
            return
        if self._closed:
            raise RuntimeError("email worker pool is already closed")
        self._started = True
        self._workers = [
            asyncio.create_task(self._worker_loop(index), name=f"dante-email-{index}")
            for index in range(self._settings.email_worker_count)
        ]

    def wake(self) -> None:
        """Reduce commit-to-send latency; polling remains the durable fallback."""
        if self._started and not self._closed:
            self._wake.set()

    async def aclose(self) -> None:
        """Stop claiming new work and let bounded provider calls finish."""
        if self._closed:
            return
        self._closed = True
        self._stop.set()
        self._wake.set()
        if not self._started:
            return
        await asyncio.gather(*self._workers, return_exceptions=False)
        self._workers.clear()

    async def _worker_loop(self, worker_index: int) -> None:
        while not self._stop.is_set():
            try:
                processed = await self._run_batch()
            except asyncio.CancelledError:
                raise
            except Exception:
                _LOGGER.exception("auth.email_worker_batch_failed worker=%d", worker_index)
                processed = 0

            if processed > 0:
                continue
            self._wake.clear()
            try:
                await asyncio.wait_for(
                    self._wake.wait(),
                    timeout=self._settings.email_poll_interval_seconds,
                )
            except TimeoutError:
                pass

    async def _run_batch(self) -> int:
        claims = await self._claim_batch()
        for claim in claims:
            if self._stop.is_set():
                # The exact claim remains durable. On an actual process exit, lease recovery
                # keeps its outcome conservative rather than fabricating a safe retry.
                break
            result: ProviderSendResult
            try:
                still_owned = await self._claim_still_owned(claim)
                if not still_owned:
                    continue
                message = render_claim(
                    claim=claim,
                    cipher=self._cipher,
                    from_address=self._settings.email_from_address,
                    canonical_web_origin=self._settings.canonical_web_origin,
                )
            except EmailPayloadError:
                _LOGGER.exception(
                    "auth.email_payload_invalid intent_ref=%s",
                    claim.email_intent_ref,
                )
                result = ProviderSendResult(
                    outcome=ProviderOutcome.DEFINITIVE_FAILURE,
                    safe_error_code="invalid_protected_payload",
                )
            else:
                # This is intentionally outside every PostgreSQL transaction.
                result = await self._provider.send(message)

            await self._finalize(claim=claim, result=result)
        return len(claims)

    async def _claim_batch(self) -> list[ClaimedEmailIntent]:
        async with self._session_factory() as database_session, database_session.begin():
            return await self._outbox.claim_batch(
                database_session,
                provider_code=self._provider.provider_code,
                batch_size=self._settings.email_claim_batch_size,
                lease_seconds=self._settings.email_claim_lease_seconds,
            )

    async def _claim_still_owned(self, claim: ClaimedEmailIntent) -> bool:
        async with self._session_factory() as database_session, database_session.begin():
            return await self._outbox.claim_still_owned(database_session, claim=claim)

    async def _finalize(
        self,
        *,
        claim: ClaimedEmailIntent,
        result: ProviderSendResult,
    ) -> None:
        retry_delay = self._retry_delay_seconds(claim.attempt_number)
        async with self._session_factory() as database_session, database_session.begin():
            finalized = await self._outbox.finalize(
                database_session,
                claim=claim,
                result=result,
                now=datetime.now(UTC),
                retry_delay_seconds=retry_delay,
            )
        if not finalized:
            _LOGGER.warning(
                "auth.email_stale_worker_result intent_ref=%s attempt=%d",
                claim.email_intent_ref,
                claim.attempt_number,
            )

    def _retry_delay_seconds(self, attempt_number: int) -> float:
        base = self._settings.email_retry_base_seconds
        cap = self._settings.email_retry_max_seconds
        exponent = max(0, attempt_number - 1)
        return min(cap, base * (2**exponent))
