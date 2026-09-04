"""FastAPI application factory for the DANTE backend process."""

from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from dante.auth.api import router as auth_router
from dante.auth.dependencies import AuthRequestBodyLimitMiddleware, BrowserAuthSecurityMiddleware
from dante.auth.m5_api import router as auth_m5_router
from dante.auth.m5_passkey_api import router as auth_m5_passkey_router
from dante.auth.m5_provider_api import router as auth_m5_provider_router
from dante.bootstrap.lifespan import lifespan
from dante.platform.config.settings import Environment, Settings
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import RequestContextMiddleware, install_problem_handlers


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

    # Starlette executes the last registered middleware first. Keep request context
    # outermost, reject invalid first-party browser mutations before reading bodies,
    # then bound accepted Auth payloads before framework parsing/application allocation.
    app.add_middleware(AuthRequestBodyLimitMiddleware)
    app.add_middleware(
        BrowserAuthSecurityMiddleware,
        canonical_web_origin=effective_settings.auth.canonical_web_origin,
    )
    app.add_middleware(RequestContextMiddleware)

    install_problem_handlers(app)
    app.include_router(auth_router)
    app.include_router(auth_m5_router)
    app.include_router(auth_m5_provider_router)
    app.include_router(auth_m5_passkey_router)

    @app.get("/health/live", include_in_schema=False)
    def health_live() -> dict[str, str]:
        """Report process liveness without depending on external services."""
        return {"status": "ok"}

    @app.get("/health/ready", include_in_schema=False, response_model=None)
    async def health_ready(request: Request) -> dict[str, str] | JSONResponse:
        """Report readiness only when the runtime PostgreSQL boundary is reachable."""
        database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
        if await database_runtime.is_ready():
            return {"status": "ready"}
        return JSONResponse(status_code=503, content={"status": "not_ready"})

    return app
