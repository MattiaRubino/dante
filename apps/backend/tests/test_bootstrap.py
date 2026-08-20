"""HTTP/process bootstrap tests for the DANTE FastAPI application factory."""

import importlib

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from dante.bootstrap.app import create_app
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

_lifespan_module = importlib.import_module("dante.bootstrap.lifespan")


class _FakeDatabaseRuntime:
    def __init__(self, *, ready: bool) -> None:
        self.ready = ready
        self.disposed = False

    async def is_ready(self) -> bool:
        return self.ready

    async def dispose(self) -> None:
        self.disposed = True


def _database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        host="127.0.0.1",
        port=5432,
        name="dante",
        user="dante_runtime",
        password=SecretStr("test-runtime-secret"),
    )


def _settings(env: Environment = Environment.LOCAL, *, debug: bool = False) -> Settings:
    local_environment = env is Environment.LOCAL
    return Settings(
        env=env,
        release_sha="local" if local_environment else "abcdef123456",
        build_id="local" if local_environment else "build-42",
        debug=debug,
        database=_database_settings(),
    )


def _install_fake_database_runtime(
    monkeypatch: pytest.MonkeyPatch,
    *,
    ready: bool,
) -> _FakeDatabaseRuntime:
    runtime = _FakeDatabaseRuntime(ready=ready)
    monkeypatch.setattr(
        _lifespan_module,
        "create_database_runtime",
        lambda _settings: runtime,
    )
    return runtime


def test_application_factory_accepts_explicit_valid_settings() -> None:
    app = create_app(_settings())

    assert app.title == "DANTE Backend"
    assert app.debug is False


def test_liveness_probe_uses_real_http_transport() -> None:
    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_probe_uses_real_http_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_database_runtime(monkeypatch, ready=True)

    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_reports_dependency_unavailable_without_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_database_runtime(monkeypatch, ready=False)

    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}


def test_lifespan_disposes_process_database_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime = _install_fake_database_runtime(monkeypatch, ready=True)

    with TestClient(create_app(_settings())):
        assert runtime.disposed is False

    assert runtime.disposed is True


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


def test_production_disables_interactive_docs_and_openapi(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_database_runtime(monkeypatch, ready=True)

    with TestClient(create_app(_settings(Environment.PROD))) as client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/redoc").status_code == 404
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200


def test_fastapi_debug_reflects_validated_settings() -> None:
    app = create_app(_settings(debug=True))

    assert app.debug is True
