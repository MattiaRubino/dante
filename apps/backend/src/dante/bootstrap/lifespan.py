"""FastAPI lifecycle ownership for process-scoped technical resources."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI

from dante.platform.config.settings import Settings
from dante.platform.database.runtime import create_database_runtime


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Create lazy database resources at startup and dispose them at shutdown."""
    settings = cast(Settings, app.state.settings)
    database_runtime = create_database_runtime(settings.database)
    app.state.database_runtime = database_runtime

    try:
        yield
    finally:
        await database_runtime.dispose()
