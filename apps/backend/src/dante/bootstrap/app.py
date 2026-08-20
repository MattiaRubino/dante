"""FastAPI application factory for the DANTE backend process."""

from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from dante.bootstrap.lifespan import lifespan
from dante.platform.config.settings import Environment, Settings
from dante.platform.database.runtime import DatabaseRuntime


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a fully validated DANTE FastAPI application instance."""
    effective_settings = settings if settings is not None else Settings()
    expose_openapi = effective_settings.env is not Environment.PROD

    app = FastAPI(
        title="DANTE Backend",
        version="0.1.0",
        debug=effective_settings.debug,
        docs_url="/docs" if expose_openapi else None,
        redoc_url=None,
        openapi_url="/openapi.json" if expose_openapi else None,
        lifespan=lifespan,
    )
    app.state.settings = effective_settings

    @app.get("/health/live", include_in_schema=False)
    def health_live() -> dict[str, str]:
        """Report process liveness without depending on external services."""
        return {"status": "ok"}

    @app.get("/health/ready", include_in_schema=False)
    async def health_ready(request: Request) -> dict[str, str] | JSONResponse:
        """Report readiness only when the runtime PostgreSQL boundary is reachable."""
        database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
        if await database_runtime.is_ready():
            return {"status": "ready"}
        return JSONResponse(status_code=503, content={"status": "not_ready"})

    return app
