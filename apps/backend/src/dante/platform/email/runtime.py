"""Process-scoped runtime ownership for the shared DANTE Email Platform."""

from __future__ import annotations

from dataclasses import dataclass

from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.feedback import EmailFeedbackStore, EmailSuppressionProjectionPort
from dante.platform.email.observability import EmailObservabilityProbe, EmailOperationalSnapshot
from dante.platform.email.outbox import DurableEmailOutbox
from dante.platform.email.provider import SesEmailProvider, SmtpEmailProvider
from dante.platform.email.settings import EmailPlatformSettings
from dante.platform.email.worker import EmailDeliveryWorkerPool, EmailRendererPort


@dataclass(slots=True)
class EmailPlatformRuntime:
    """One shared outbox, provider client and bounded worker pool per backend process."""

    outbox: DurableEmailOutbox
    worker_pool: EmailDeliveryWorkerPool
    feedback_store: EmailFeedbackStore
    observability: EmailObservabilityProbe

    def wake(self) -> None:
        """Nudge workers after a caller has committed newly staged intent."""
        self.worker_pool.wake()

    async def operational_snapshot(self, *, window_seconds: int = 900) -> EmailOperationalSnapshot:
        """Expose privacy-minimized durable delivery metrics to observability adapters."""
        return await self.observability.snapshot(window_seconds=window_seconds)

    async def aclose(self) -> None:
        """Stop claiming new work and finish bounded provider calls."""
        await self.worker_pool.aclose()


async def create_email_platform_runtime(
    *,
    settings: EmailPlatformSettings,
    database_runtime: DatabaseRuntime,
    renderer: EmailRendererPort,
    suppression_projection: EmailSuppressionProjectionPort | None = None,
) -> EmailPlatformRuntime:
    """Construct shared delivery resources without performing provider network I/O."""
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
    transport = _enum_value(settings.email_transport)
    if transport == "ses":
        provider = SesEmailProvider(settings=settings)
    elif transport == "smtp":
        provider = SmtpEmailProvider(settings=settings)
    else:
        raise RuntimeError(f"unsupported Email Platform transport: {transport}")
    worker_pool = EmailDeliveryWorkerPool(
        session_factory=database_runtime.session_factory,
        outbox=outbox,
        cipher=cipher,
        provider=provider,
        renderer=renderer,
        settings=settings,
    )
    runtime = EmailPlatformRuntime(
        outbox=outbox,
        worker_pool=worker_pool,
        feedback_store=EmailFeedbackStore(suppression_projection=suppression_projection),
        observability=EmailObservabilityProbe(session_factory=database_runtime.session_factory),
    )
    await worker_pool.start()
    return runtime


def _enum_value(value: object) -> str:
    candidate = getattr(value, "value", value)
    return str(candidate)
