"""Process-scoped runtime ownership for the DANTE durable Email Platform."""

from __future__ import annotations

from dataclasses import dataclass

from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_feedback import SesFeedbackStore
from dante.auth.email_outbox import DurableEmailOutbox
from dante.auth.email_provider import SesEmailProvider, SmtpEmailProvider
from dante.auth.email_worker import EmailDeliveryWorkerPool
from dante.platform.config.auth import AuthSettings, EmailTransport
from dante.platform.database.runtime import DatabaseRuntime


@dataclass(slots=True)
class EmailPlatformRuntime:
    """One shared outbox, provider client and bounded worker pool per backend process."""

    outbox: DurableEmailOutbox
    worker_pool: EmailDeliveryWorkerPool
    feedback_store: SesFeedbackStore

    def wake(self) -> None:
        """Nudge workers after a caller has committed newly staged intent."""
        self.worker_pool.wake()

    async def aclose(self) -> None:
        """Stop claiming new work and finish bounded provider calls."""
        await self.worker_pool.aclose()


async def create_email_platform_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
) -> EmailPlatformRuntime:
    """Construct the durable email platform without performing provider network I/O."""
    current_key_id = settings.email_payload_current_key_id
    if current_key_id is None:
        raise RuntimeError("enabled Email Platform lost validated payload-key identity")
    cipher = EmailPayloadCipher(
        key_ring=settings.email_payload_key_bytes,
        current_key_id=current_key_id,
    )
    outbox = DurableEmailOutbox(
        cipher=cipher,
        attempt_limit=settings.email_attempt_limit,
    )
    provider = (
        SesEmailProvider(settings=settings)
        if settings.email_transport is EmailTransport.SES
        else SmtpEmailProvider(settings=settings)
    )
    worker_pool = EmailDeliveryWorkerPool(
        session_factory=database_runtime.session_factory,
        outbox=outbox,
        cipher=cipher,
        provider=provider,
        settings=settings,
    )
    runtime = EmailPlatformRuntime(
        outbox=outbox,
        worker_pool=worker_pool,
        feedback_store=SesFeedbackStore(),
    )
    await worker_pool.start()
    return runtime
