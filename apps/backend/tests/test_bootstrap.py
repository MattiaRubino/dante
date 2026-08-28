"""HTTP/process bootstrap tests for the DANTE FastAPI application factory."""

import importlib
from base64 import urlsafe_b64encode
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from dante.auth.sessions import WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE
from dante.bootstrap.app import create_app
from dante.platform.config.auth import AuthSettings
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

_lifespan_module = importlib.import_module("dante.bootstrap.lifespan")
_auth_service_module = importlib.import_module("dante.auth.service")
_TEST_PEPPER_KEY_ID = "test-v1"
_CANONICAL_ORIGIN = "https://dante.test"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


class _FakeDatabaseRuntime:
    def __init__(self, *, ready: bool) -> None:
        self.ready = ready
        self.disposed = False
        self.session_factory = object()

    async def is_ready(self) -> bool:
        return self.ready

    async def dispose(self) -> None:
        self.disposed = True


class _FakeAuthRuntime:
    def __init__(self) -> None:
        self.closed = False
        self.service = object()

    async def aclose(self) -> None:
        self.closed = True


def _database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        host="127.0.0.1",
        port=5432,
        name="dante",
        user="dante_runtime",
        password=SecretStr("test-runtime-secret"),
    )


def _auth_settings() -> AuthSettings:
    return AuthSettings(
        canonical_web_origin=_CANONICAL_ORIGIN,
        password_current_pepper_key_id=_TEST_PEPPER_KEY_ID,
        password_peppers={_TEST_PEPPER_KEY_ID: SecretStr(_secret(b"p" * 32))},
        csrf_key=SecretStr(_secret(b"c" * 32)),
        kdf_max_concurrency=1,
        kdf_max_queue_depth=1,
        signin_rate_capacity=10,
        signin_rate_window_seconds=60,
    )


def _settings(env: Environment = Environment.LOCAL, *, debug: bool = False) -> Settings:
    local_environment = env is Environment.LOCAL
    return Settings(
        env=env,
        release_sha="local" if local_environment else "abcdef123456",
        build_id="local" if local_environment else "build-42",
        debug=debug,
        database=_database_settings(),
        auth=_auth_settings(),
    )


def _install_fake_runtimes(
    monkeypatch: pytest.MonkeyPatch,
    *,
    ready: bool,
) -> tuple[_FakeDatabaseRuntime, _FakeAuthRuntime]:
    database_runtime = _FakeDatabaseRuntime(ready=ready)
    auth_runtime = _FakeAuthRuntime()

    monkeypatch.setattr(
        _lifespan_module,
        "create_database_runtime",
        lambda _settings: database_runtime,
    )

    async def create_fake_auth_runtime(**_kwargs: object) -> _FakeAuthRuntime:
        return auth_runtime

    monkeypatch.setattr(
        _lifespan_module,
        "create_auth_runtime",
        create_fake_auth_runtime,
    )
    return database_runtime, auth_runtime


def _web_headers() -> dict[str, str]:
    return {
        "Origin": _CANONICAL_ORIGIN,
        "Sec-Fetch-Site": "same-origin",
        WEB_CLIENT_HEADER_NAME: WEB_CLIENT_HEADER_VALUE,
        "Content-Type": "application/json",
    }


def test_application_factory_accepts_explicit_valid_settings() -> None:
    app = create_app(_settings())

    assert app.title == "DANTE Backend"
    assert app.debug is False


def test_liveness_probe_uses_real_http_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)

    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_probe_uses_real_http_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)

    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_reports_dependency_unavailable_without_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=False)

    with TestClient(create_app(_settings())) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}


def test_lifespan_disposes_process_resources(monkeypatch: pytest.MonkeyPatch) -> None:
    database_runtime, auth_runtime = _install_fake_runtimes(monkeypatch, ready=True)

    with TestClient(create_app(_settings())):
        assert database_runtime.disposed is False
        assert auth_runtime.closed is False

    assert auth_runtime.closed is True
    assert database_runtime.disposed is True


@pytest.mark.asyncio
async def test_auth_runtime_partial_startup_closes_already_owned_kdf(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lifecycle = {"started": False, "closed": False}

    class FakePasswordKdf:
        def __init__(self, **_kwargs: object) -> None:
            pass

        async def start(self) -> None:
            lifecycle["started"] = True

        async def aclose(self) -> None:
            lifecycle["closed"] = True

    def fail_http_client(**_kwargs: object) -> object:
        raise RuntimeError("synthetic http client construction failure")

    monkeypatch.setattr(_auth_service_module, "PasswordKdf", FakePasswordKdf)
    monkeypatch.setattr(_auth_service_module.httpx2, "AsyncClient", fail_http_client)

    with pytest.raises(RuntimeError, match="synthetic http client construction failure"):
        await _auth_service_module.create_auth_runtime(
            settings=_auth_settings(),
            database_runtime=cast(Any, _FakeDatabaseRuntime(ready=True)),
            release_sha="test-release",
        )

    assert lifecycle == {"started": True, "closed": True}


@pytest.mark.parametrize("env", [Environment.LOCAL, Environment.DEV, Environment.UAT])
def test_non_production_environments_expose_docs_and_openapi(
    env: Environment,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)

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
    assert schema["paths"]["/api/v1/auth/signin"]["post"]["operationId"] == "auth_sign_in"
    assert schema["paths"]["/api/v1/auth/session"]["get"]["operationId"] == "auth_get_session"
    assert schema["paths"]["/api/v1/auth/session"]["delete"]["operationId"] == "auth_log_out"


def test_production_disables_interactive_docs_and_openapi(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)

    with TestClient(create_app(_settings(Environment.PROD))) as client:
        assert client.get("/docs").status_code == 404
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/redoc").status_code == 404
        assert client.get("/health/live").status_code == 200
        assert client.get("/health/ready").status_code == 200


def test_fastapi_debug_reflects_validated_settings() -> None:
    app = create_app(_settings(debug=True))

    assert app.debug is True


def test_malformed_json_is_400_not_field_validation_422(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)

    with TestClient(create_app(_settings()), base_url=_CANONICAL_ORIGIN) as client:
        response = client.post(
            "/api/v1/auth/signin",
            content=b'{"email":',
            headers=_web_headers(),
        )

    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == "request.malformed"


def test_valid_json_field_failure_is_422(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)

    with TestClient(create_app(_settings()), base_url=_CANONICAL_ORIGIN) as client:
        response = client.post(
            "/api/v1/auth/signin",
            content=b'{"email":"person@example.com"}',
            headers=_web_headers(),
        )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "request.validation_failed"
    assert body["errors"][0]["pointer"] == "/password"


def test_duplicate_origin_fails_closed_before_body_parsing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)
    headers = [
        ("Origin", _CANONICAL_ORIGIN),
        ("Origin", "https://evil.example"),
        ("Sec-Fetch-Site", "same-origin"),
        (WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE),
        ("Content-Type", "application/json"),
    ]

    with TestClient(create_app(_settings()), base_url=_CANONICAL_ORIGIN) as client:
        response = client.post(
            "/api/v1/auth/signin",
            content=b'{"email":',
            headers=headers,
        )

    assert response.status_code == 403
    assert response.json()["code"] == "security.csrf_failed"


def test_duplicate_content_type_is_malformed_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_runtimes(monkeypatch, ready=True)
    headers = [
        ("Origin", _CANONICAL_ORIGIN),
        ("Sec-Fetch-Site", "same-origin"),
        (WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE),
        ("Content-Type", "application/json"),
        ("Content-Type", "text/plain"),
    ]

    with TestClient(create_app(_settings()), base_url=_CANONICAL_ORIGIN) as client:
        response = client.post(
            "/api/v1/auth/signin",
            content=b"{}",
            headers=headers,
        )

    assert response.status_code == 400
    assert response.json()["code"] == "request.malformed"
