"""Access/Auth integration wiring for the shared DANTE Email Platform."""

from __future__ import annotations

from dataclasses import dataclass

from dante.auth.email_feedback import AuthEmailSuppressionProjection
from dante.auth.email_outbox import DurableEmailOutbox
from dante.auth.email_render import AuthSecurityEmailRenderer
from dante.platform.config.auth import AuthSettings
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.email.feedback import EmailFeedbackStore
from dante.platform.email.observability import EmailObservabilityProbe, EmailOperationalSnapshot
from dante.platform.email.runtime import create_email_platform_runtime as create_shared_runtime
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
    """Inject Auth rendering/projection into the shared runtime composer."""
    shared = await create_shared_runtime(
        settings=settings,
        database_runtime=database_runtime,
        renderer=AuthSecurityEmailRenderer(
            canonical_web_origin=settings.canonical_web_origin,
        ),
        suppression_projection=AuthEmailSuppressionProjection(),
    )
    return EmailPlatformRuntime(
        outbox=DurableEmailOutbox.from_shared(shared.outbox),
        worker_pool=shared.worker_pool,
        feedback_store=shared.feedback_store,
        observability=shared.observability,
    )
