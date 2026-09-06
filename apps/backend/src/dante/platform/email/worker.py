"""Process-scoped durable workers for the shared DANTE Email Platform."""

from __future__ import annotations

import asyncio
import logging
import time
from contextlib import suppress
from datetime import UTC, datetime
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.email.contracts import (
    ClaimedEmailIntent,
    EmailPayloadError,
    EmailProviderPort,
    ProviderMessage,
    ProviderOutcome,
    ProviderSendResult,
)
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.outbox import DurableEmailOutbox
from dante.platform.email.settings import EmailPlatformSettings

_LOGGER = logging.getLogger(__name__)


class EmailRendererPort(Protocol):
    """Consumer-owned renderer for one claimed durable intent."""

    def render(
        self,
        *,
        claim: ClaimedEmailIntent,
        cipher: EmailPayloadCipher,
        from_address: str,
    ) -> ProviderMessage:
        """Render one claimed consumer intent into provider-neutral content."""
        ...


class EmailDeliveryWorkerPool:
    """Fixed bounded workers; PostgreSQL, not process memory, owns admitted work."""

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        outbox: DurableEmailOutbox,
        cipher: EmailPayloadCipher,
        provider: EmailProviderPort,
        renderer: EmailRendererPort,
        settings: EmailPlatformSettings,
    ) -> None:
        self._session_factory = session_factory
        self._outbox = outbox
        self._cipher = cipher
        self._provider = provider
        self._renderer = renderer
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
                _LOGGER.exception("email_platform.worker_batch_failed worker=%d", worker_index)
                processed = 0

            if processed > 0:
                continue
            self._wake.clear()
            with suppress(TimeoutError):
                await asyncio.wait_for(
                    self._wake.wait(),
                    timeout=self._settings.email_poll_interval_seconds,
                )

    async def _run_batch(self) -> int:
        claims = await self._claim_batch()
        for claim in claims:
            if self._stop.is_set():
                break
            result: ProviderSendResult
            provider_elapsed_ms: float | None = None
            try:
                still_owned = await self._claim_still_owned(claim)
                if not still_owned:
                    continue
                message = self._renderer.render(
                    claim=claim,
                    cipher=self._cipher,
                    from_address=self._settings.email_sender_address,
                )
            except EmailPayloadError:
                _LOGGER.exception(
                    "email_platform.payload_invalid intent_ref=%s",
                    claim.email_intent_ref,
                )
                result = ProviderSendResult(
                    outcome=ProviderOutcome.DEFINITIVE_FAILURE,
                    safe_error_code="invalid_protected_payload",
                )
            else:
                # External provider I/O is intentionally outside every PostgreSQL transaction.
                started = time.perf_counter()
                result = await self._provider.send(message)
                provider_elapsed_ms = max(0.0, (time.perf_counter() - started) * 1000.0)

            finalized = await self._finalize(claim=claim, result=result)
            if finalized:
                _LOGGER.info(
                    "email_platform.delivery_result provider=%s outcome=%s attempt=%d "
                    "provider_elapsed_ms=%s intent_ref=%s",
                    self._provider.provider_code,
                    result.outcome.value,
                    claim.attempt_number,
                    provider_elapsed_ms,
                    claim.email_intent_ref,
                )
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
    ) -> bool:
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
                "email_platform.stale_worker_result intent_ref=%s attempt=%d",
                claim.email_intent_ref,
                claim.attempt_number,
            )
        return finalized

    def _retry_delay_seconds(self, attempt_number: int) -> float:
        base = float(self._settings.email_retry_base_seconds)
        cap = float(self._settings.email_retry_max_seconds)
        exponent = max(0, attempt_number - 1)
        delay = base * float(2**exponent)
        return cap if delay > cap else delay
