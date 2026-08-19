"""HTTP/process bootstrap tests for the DANTE FastAPI application factory."""

import pytest
from fastapi.testclient import TestClient

from dante.bootstrap.app import create_app
from dante.platform.config.settings import Environment, Settings


def _settings(env: Environment = Environment.LOCAL, *, debug: bool = False) -> Settings:
    local_environment = env is Environment.LOCAL
    return Settings(
        env=env,
        release_sha="local" if local_environment else "abcdef123456",
        build_id="local" if local_environment else "build-42",
        debug=debug,
    )


def test_application_factory_accepts_explicit_valid_settings() -> None:
    app = create_app(_settings())

    assert app.title == "DANTE Backend"
    assert app.debug is False


def test_liveness_probe_uses_real_http_transport() -> None:
    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_probe_uses_real_http_transport() -> None:
    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.parametrize("env", [Environment.LOCAL, Environment.DEV, Environment.UAT])
def test_non_production_environments_expose_docs_and_openapi(env: Environment) -> None:
    with TestClient(create_app(_settings(env))) as client:
        docs_response = client.get("/docs")
        openapi_response = client.get("/openapi.json")
        redoc_response = client.get("/redoc")

    assert docs_response.status_code == 200
    assert openapi_response.status_code == 200
    assert redoc_response.status_code == 404

    schema = openapi_response.json()
    assert "/health/live" not in schema["paths"]
    assert "/health/ready" not in schema["paths"]


def test_production_disables_interactive_docs_and_openapi() -> None:
    with TestClient(create_app(_settings(Environment.PROD))) as client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/redoc").status_code == 404
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200


def test_fastapi_debug_reflects_validated_settings() -> None:
    app = create_app(_settings(debug=True))

    assert app.debug is True
