"""FastAPI application factory for the DANTE backend process."""

from fastapi import FastAPI

from dante.platform.config.settings import Environment, Settings


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
    )

    @app.get("/health/live", include_in_schema=False)
    def health_live() -> dict[str, str]:
        """Report process liveness without depending on external services."""
        return {"status": "ok"}

    @app.get("/health/ready", include_in_schema=False)
    def health_ready() -> dict[str, str]:
        """Report CP1 readiness after successful bootstrap/configuration."""
        return {"status": "ready"}

    return app
