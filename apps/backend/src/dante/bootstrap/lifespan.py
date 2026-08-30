"""FastAPI lifecycle ownership for process-scoped technical resources."""

from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import cast

from fastapi import FastAPI

from dante.auth.lifecycle_runtime import create_auth_lifecycle_runtime
from dante.auth.provider_flow_runtime import create_provider_flow_runtime
from dante.auth.service import create_auth_runtime
from dante.platform.config.settings import Settings
from dante.platform.database.runtime import create_database_runtime


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create process-scoped DB/Auth resources and dispose them in reverse order."""
    settings = cast(Settings, app.state.settings)

    async with AsyncExitStack() as stack:
        database_runtime = create_database_runtime(settings.database)
        stack.push_async_callback(database_runtime.dispose)
        app.state.database_runtime = database_runtime

        auth_runtime = await create_auth_runtime(
            settings=settings.auth,
            database_runtime=database_runtime,
            release_sha=str(settings.release_sha),
        )
        stack.push_async_callback(auth_runtime.aclose)
        app.state.auth_runtime = auth_runtime

        auth_lifecycle_runtime = await create_auth_lifecycle_runtime(
            settings=settings.auth,
            database_runtime=database_runtime,
            auth_runtime=auth_runtime,
        )
        stack.push_async_callback(auth_lifecycle_runtime.aclose)
        app.state.auth_lifecycle_runtime = auth_lifecycle_runtime

        app.state.provider_flow_runtime = (
            create_provider_flow_runtime(
                settings=settings.auth,
                database_runtime=database_runtime,
                auth_runtime=auth_runtime,
                lifecycle_runtime=auth_lifecycle_runtime,
            )
            if settings.auth.provider.google.enabled
            else None
        )

        yield
