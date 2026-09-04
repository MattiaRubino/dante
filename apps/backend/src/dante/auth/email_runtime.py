"""Access/Auth integration wiring for the shared DANTE Email Platform."""

from __future__ import annotations

from dataclasses import dataclass

from dante.auth.email_feedback import AuthEmailSuppressionProjection
from dante.auth.email_outbox import DurableEmailOutbox
from dante.auth.email_render import AuthSecurityEmailRenderer
from dante.platform.config.auth import AuthSettings
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.email.crypto import EmailPayloadCipher
from dante.platform.email.feedback import EmailFeedbackStore
from dante.platform.email.observability import EmailObservabilityProbe, EmailOperationalSnapshot
from dante.platform.email.outbox import DurableEmailOutbox as SharedDurableEmailOutbox
from dante.platform.email.provider import SesEmailProvider, SmtpEmailProvider
from dante.platform.email.worker import EmailDeliveryWorkerPool


@dataclass(slots=True)
class EmailPlatformRuntime:
    """Auth integration handle over one process-scoped shared Email Platform runtime."""

    outbox: DurableEmailOutbox
    worker_pool: EmailDeliveryWorkerPool
    feedback_store: EmailFeedbackStore
    observability: EmailObservabilityProbe

    def wake(self) -> None:
        """Nudge shared workers after an Auth transaction commits staged email work."""
        self.worker_pool.wake()

    async def operational_snapshot(self, *, window_seconds: int = 900) -> EmailOperationalSnapshot:
        """Expose privacy-minimized durable Email Platform metrics."""
        return await self.observability.snapshot(window_seconds=window_seconds)

    async def aclose(self) -> None:
        """Stop shared workers and finish bounded provider calls."""
        await self.worker_pool.aclose()


async def create_email_platform_runtime(
    *,
    settings: AuthSettings,
    database_runtime: DatabaseRuntime,
) -> EmailPlatformRuntime:
    """Compose Auth rendering/projection into shared delivery mechanics."""
    current_key_id = settings.email_payload_current_key_id
    if current_key_id is None:
        raise RuntimeError("enabled Email Platform lost validated payload-key identity")

    cipher = EmailPayloadCipher(
        key_ring=settings.email_payload_key_bytes,
        current_key_id=current_key_id,
    )
    core_outbox = SharedDurableEmailOutbox(
        cipher=cipher,
        attempt_limit=settings.email_attempt_limit,
    )
    auth_outbox = DurableEmailOutbox.from_shared(core_outbox)

    transport = settings.email_transport.value
    if transport == "ses":
        provider = SesEmailProvider(settings=settings)
    elif transport == "smtp":
        provider = SmtpEmailProvider(settings=settings)
    else:
        raise RuntimeError(f"unsupported Email Platform transport: {transport}")

    worker_pool = EmailDeliveryWorkerPool(
        session_factory=database_runtime.session_factory,
        outbox=core_outbox,
        cipher=cipher,
        provider=provider,
        renderer=AuthSecurityEmailRenderer(
            canonical_web_origin=settings.canonical_web_origin,
        ),
        settings=settings,
    )
    runtime = EmailPlatformRuntime(
        outbox=auth_outbox,
        worker_pool=worker_pool,
        feedback_store=EmailFeedbackStore(
            suppression_projection=AuthEmailSuppressionProjection(),
        ),
        observability=EmailObservabilityProbe(session_factory=database_runtime.session_factory),
    )
    await worker_pool.start()
    return runtime
