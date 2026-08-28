"""Real PostgreSQL 18.6 + FastAPI proof for the first M3 authenticated spine."""

from __future__ import annotations

import asyncio
import threading
from base64 import urlsafe_b64encode
from collections.abc import Generator
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, override
from uuid import uuid7

import psycopg
import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from dante.auth.email import normalize_email
from dante.auth.passwords import PasswordKdf
from dante.auth.sessions import (
    CSRF_HEADER_NAME,
    SESSION_COOKIE_NAME,
    WEB_CLIENT_HEADER_NAME,
    WEB_CLIENT_HEADER_VALUE,
)
from dante.bootstrap.app import create_app
from dante.platform.config.auth import AuthSettings
from dante.platform.config.settings import Environment, Settings

_CANONICAL_ORIGIN = "https://dante.test"
_AUTH_TEST_VALUE = "correct horse battery staple"
_EMAIL = "synthetic.user@example.com"
_TEST_PEPPER_KEY_ID = "test-v1"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


_PEPPER = _secret(b"p" * 32)
_CSRF_KEY = _secret(b"c" * 32)


class _HibpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if not self.path.startswith("/range/"):
            self.send_response(404)
            self.end_headers()
            return

        payload = f"{'0' * 35}:0\r\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    @override
    def log_message(self, _format: str, *args: object) -> None:
        _ = args


@pytest.fixture
def hibp_stub_url() -> Generator[str]:
    """Run a local HIBP range substitute; public Internet is never required."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _HibpHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = int(server.server_address[1])

    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def _auth_settings(hibp_stub_url: str) -> AuthSettings:
    return AuthSettings(
        canonical_web_origin=_CANONICAL_ORIGIN,
        password_current_pepper_key_id=_TEST_PEPPER_KEY_ID,
        password_peppers={_TEST_PEPPER_KEY_ID: SecretStr(_PEPPER)},
        csrf_key=SecretStr(_CSRF_KEY),
        session_max_age_seconds=3_600,
        session_idle_timeout_seconds=60,
        kdf_max_concurrency=2,
        kdf_max_queue_depth=4,
        kdf_queue_timeout_seconds=2,
        signin_rate_capacity=100,
        signin_rate_window_seconds=60,
        hibp_base_url=hibp_stub_url,
        hibp_timeout_seconds=1,
        hibp_max_connections=4,
    )


def _settings(database: Any, hibp_stub_url: str) -> Settings:
    return Settings(
        env=Environment.LOCAL,
        release_sha="local",
        build_id="local",
        debug=False,
        database=database.runtime_settings(),
        auth=_auth_settings(hibp_stub_url),
    )


async def _hash_password(auth_settings: AuthSettings) -> tuple[str, str]:
    kdf = PasswordKdf(
        pepper_ring=auth_settings.password_pepper_bytes,
        current_pepper_key_id=auth_settings.password_current_pepper_key_id,
        max_concurrency=1,
        max_queue_depth=0,
        queue_timeout_seconds=2,
    )
    await kdf.start()
    try:
        return await kdf.hash_new_password(_AUTH_TEST_VALUE)
    finally:
        await kdf.aclose()


def _seed_account(database: Any, auth_settings: AuthSettings) -> None:
    verifier, pepper_key_id = asyncio.run(_hash_password(auth_settings))
    normalized_email = normalize_email(_EMAIL)
    now = datetime.now(UTC)

    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")

        account_ref = uuid7()
        connection.execute(
            """
            INSERT INTO dante.account(
                account_ref, status_code, created_at, disabled_at
            )
            VALUES (%s, 'active', %s, NULL)
            """,
            (account_ref, now),
        )
        connection.execute(
            """
            INSERT INTO dante.email_identity(
                email_identity_ref,
                account_ref,
                address,
                comparison_key,
                created_at,
                verified_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                uuid7(),
                account_ref,
                normalized_email.address,
                normalized_email.comparison_key,
                now,
                now,
            ),
        )
        connection.execute(
            """
            INSERT INTO dante.password_credential(
                password_credential_ref,
                account_ref,
                verifier,
                pepper_key_id,
                created_at,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (uuid7(), account_ref, verifier, pepper_key_id, now, now),
        )
        connection.commit()


def _web_headers() -> dict[str, str]:
    return {
        "Origin": _CANONICAL_ORIGIN,
        "Sec-Fetch-Site": "same-origin",
        WEB_CLIENT_HEADER_NAME: WEB_CLIENT_HEADER_VALUE,
    }


def _auth_session_count(database: Any) -> int:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        row = connection.execute("SELECT count(*) FROM dante.auth_session").fetchone()
    assert row is not None
    return int(row[0])


@pytest.mark.postgres
def test_real_signin_bootstrap_logout_and_second_session_survival(
    migrated_database: Any,
    hibp_stub_url: str,
) -> None:
    auth_settings = _auth_settings(hibp_stub_url)
    _seed_account(migrated_database, auth_settings)
    app = create_app(_settings(migrated_database, hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        signin_a = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers=_web_headers(),
        )
        assert signin_a.status_code == 200
        assert signin_a.headers["cache-control"] == "no-store"
        assert signin_a.headers["x-request-id"]

        cookie_header = signin_a.headers["set-cookie"]
        assert f"{SESSION_COOKIE_NAME}=" in cookie_header
        assert "Max-Age=3600" in cookie_header
        assert "Secure" in cookie_header
        assert "HttpOnly" in cookie_header
        assert "Path=/" in cookie_header
        assert "SameSite=lax" in cookie_header
        assert "Domain=" not in cookie_header

        session_a = client.cookies.get(SESSION_COOKIE_NAME)
        assert session_a is not None
        csrf_a = str(signin_a.json()["csrf_token"])

        client.cookies.clear()
        signin_b = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers=_web_headers(),
        )
        assert signin_b.status_code == 200
        session_b = client.cookies.get(SESSION_COOKIE_NAME)
        assert session_b is not None
        assert session_b != session_a
        assert _auth_session_count(migrated_database) == 2

        client.cookies.clear()
        bootstrap_b = client.get(
            "/api/v1/auth/session",
            headers={"Cookie": f"{SESSION_COOKIE_NAME}={session_b}"},
        )
        assert bootstrap_b.status_code == 200
        assert bootstrap_b.json()["authenticated"] is True
        assert bootstrap_b.headers["cache-control"] == "no-store"

        logout_a = client.delete(
            "/api/v1/auth/session",
            headers={
                **_web_headers(),
                "Cookie": f"{SESSION_COOKIE_NAME}={session_a}",
                CSRF_HEADER_NAME: csrf_a,
            },
        )
        assert logout_a.status_code == 204
        assert logout_a.headers["cache-control"] == "no-store"

        session_a_after = client.get(
            "/api/v1/auth/session",
            headers={"Cookie": f"{SESSION_COOKIE_NAME}={session_a}"},
        )
        assert session_a_after.status_code == 200
        assert session_a_after.json() == {"authenticated": False}

        session_b_after = client.get(
            "/api/v1/auth/session",
            headers={"Cookie": f"{SESSION_COOKIE_NAME}={session_b}"},
        )
        assert session_b_after.status_code == 200
        assert session_b_after.json()["authenticated"] is True

        repeat_logout_without_cookie = client.delete(
            "/api/v1/auth/session",
            headers=_web_headers(),
        )
        assert repeat_logout_without_cookie.status_code == 204


@pytest.mark.postgres
def test_wrong_password_and_unknown_email_are_publicly_equivalent(
    migrated_database: Any,
    hibp_stub_url: str,
) -> None:
    auth_settings = _auth_settings(hibp_stub_url)
    _seed_account(migrated_database, auth_settings)
    app = create_app(_settings(migrated_database, hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        wrong = client.post(
            "/api/v1/auth/signin",
            json={
                "email": _EMAIL,
                "password": "definitely wrong credential value",
            },
            headers=_web_headers(),
        )
        unknown = client.post(
            "/api/v1/auth/signin",
            json={
                "email": "unknown.user@example.com",
                "password": _AUTH_TEST_VALUE,
            },
            headers=_web_headers(),
        )

    assert wrong.status_code == unknown.status_code == 401

    wrong_body = wrong.json()
    unknown_body = unknown.json()
    for response, body in ((wrong, wrong_body), (unknown, unknown_body)):
        assert response.headers["content-type"].startswith("application/problem+json")
        assert response.headers["cache-control"] == "no-store"
        assert response.headers["x-request-id"] == body["request_id"]
        assert body["code"] == "auth.invalid_credentials"
        assert body["category"] == "authentication"
        assert body["retryable"] is False
        assert body["status"] == 401

    wrong_body.pop("request_id")
    unknown_body.pop("request_id")
    assert wrong_body == unknown_body


@pytest.mark.postgres
def test_web_security_rejects_invalid_origin_content_type_and_missing_csrf(
    migrated_database: Any,
    hibp_stub_url: str,
) -> None:
    auth_settings = _auth_settings(hibp_stub_url)
    _seed_account(migrated_database, auth_settings)
    app = create_app(_settings(migrated_database, hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        wrong_origin = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers={
                **_web_headers(),
                "Origin": "https://evil.example",
            },
        )
        assert wrong_origin.status_code == 403
        assert wrong_origin.json()["code"] == "security.csrf_failed"
        assert wrong_origin.headers["x-request-id"] == wrong_origin.json()["request_id"]

        wrong_content_type = client.post(
            "/api/v1/auth/signin",
            content=b"{}",
            headers={
                **_web_headers(),
                "Content-Type": "text/plain",
            },
        )
        assert wrong_content_type.status_code == 400
        assert wrong_content_type.json()["code"] == "request.malformed"

        signin = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers=_web_headers(),
        )
        assert signin.status_code == 200

        logout = client.delete(
            "/api/v1/auth/session",
            headers=_web_headers(),
        )

    assert logout.status_code == 403
    assert logout.json()["code"] == "security.csrf_failed"


@pytest.mark.postgres
def test_duplicate_session_cookie_fails_closed(
    migrated_database: Any,
    hibp_stub_url: str,
) -> None:
    auth_settings = _auth_settings(hibp_stub_url)
    _seed_account(migrated_database, auth_settings)
    app = create_app(_settings(migrated_database, hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        signin = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers=_web_headers(),
        )
        assert signin.status_code == 200
        session_secret = client.cookies.get(SESSION_COOKIE_NAME)
        assert session_secret is not None
        client.cookies.clear()

        duplicate_cookie = f"{SESSION_COOKIE_NAME}={session_secret}; {SESSION_COOKIE_NAME}=different-value"
        bootstrap = client.get(
            "/api/v1/auth/session",
            headers={"Cookie": duplicate_cookie},
        )
        assert bootstrap.status_code == 200
        assert bootstrap.json() == {"authenticated": False}
        assert f'{SESSION_COOKIE_NAME}=""' in bootstrap.headers["set-cookie"]

        logout = client.delete(
            "/api/v1/auth/session",
            headers={**_web_headers(), "Cookie": duplicate_cookie},
        )
        assert logout.status_code == 403
        assert logout.json()["code"] == "security.csrf_failed"
