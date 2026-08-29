"""FastAPI lifecycle ownership for process-scoped technical resources."""

from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import cast

from fastapi import FastAPI

from dante.auth.service import create_auth_runtime
from dante.platform.config.settings import Settings
from dante.platform.database.runtime import create_database_runtime
from dante.platform.observability.runtime import ObservabilityRuntime


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create process-scoped DB/Auth resources and dispose them in reverse order."""
    settings = cast(Settings, app.state.settings)
    observability_runtime = cast(ObservabilityRuntime, app.state.observability_runtime)

    async with AsyncExitStack() as stack:
        stack.push_async_callback(observability_runtime.aclose)

        database_runtime = create_database_runtime(
            settings.database,
            telemetry=observability_runtime.database,
        )
        stack.push_async_callback(database_runtime.dispose)
        app.state.database_runtime = database_runtime

        auth_runtime = await create_auth_runtime(
            settings=settings.auth,
            database_runtime=database_runtime,
            release_sha=str(settings.release_sha),
            telemetry=observability_runtime.auth,
        )
        stack.push_async_callback(auth_runtime.aclose)
        app.state.auth_runtime = auth_runtime

        yield
