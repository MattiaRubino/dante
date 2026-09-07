"""Real PostgreSQL + authenticated FastAPI proof for the B00 temporal spine."""

from __future__ import annotations

import asyncio
import threading
from base64 import urlsafe_b64encode
from collections.abc import Generator
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, override
from uuid import UUID, uuid7

import psycopg
import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from dante.auth.email import normalize_email
from dante.auth.passwords import PasswordKdf
from dante.auth.sessions import SESSION_COOKIE_NAME, WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE
from dante.bootstrap.app import create_app
from dante.context.dependencies import DANTE_TIME_ZONE_HEADER_NAME
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.settings import Environment, Settings

_CANONICAL_ORIGIN = "https://dante.test"
_AUTH_TEST_VALUE = "correct horse battery staple"
_EMAIL = "temporal.user@example.com"
_TEST_PEPPER_KEY_ID = "test-password-v1"
_TEST_OTP_KEY_ID = "test-signup-otp-v1"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


_PEPPER = _secret(b"p" * 32)
_CSRF_KEY = _secret(b"c" * 32)
_OTP_KEY = _secret(b"o" * 32)


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
def temporal_hibp_stub_url() -> Generator[str]:
    """Run a local HIBP substitute so the integration proof never needs public Internet."""
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
        signup_otp_current_key_id=_TEST_OTP_KEY_ID,
        signup_otp_keys={_TEST_OTP_KEY_ID: SecretStr(_OTP_KEY)},
        smtp_host="127.0.0.1",
        smtp_port=9,
        smtp_security=SmtpSecurity.PLAIN,
        smtp_from_address="no-reply@dante.test",
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


def _seed_account(database: Any, auth_settings: AuthSettings) -> UUID:
    verifier, pepper_key_id = asyncio.run(_hash_password(auth_settings))
    normalized_email = normalize_email(_EMAIL)
    now = datetime.now(UTC)
    account_ref = uuid7()

    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
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

    return account_ref


def _web_headers() -> dict[str, str]:
    return {
        "Origin": _CANONICAL_ORIGIN,
        "Sec-Fetch-Site": "same-origin",
        WEB_CLIENT_HEADER_NAME: WEB_CLIENT_HEADER_VALUE,
    }


def _context_row(database: Any, account_ref: UUID) -> tuple[UUID, str, str | None] | None:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        row = connection.execute(
            """
            SELECT self_person_ref, timezone_mode, fixed_zone_id
            FROM dante.account_application_context
            WHERE account_ref = %s
            """,
            (account_ref,),
        ).fetchone()

    if row is None:
        return None
    return UUID(str(row[0])), str(row[1]), None if row[2] is None else str(row[2])


def _person_exists(database: Any, person_ref: UUID) -> bool:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        row = connection.execute(
            "SELECT EXISTS(SELECT 1 FROM dante.person WHERE person_ref = %s)",
            (person_ref,),
        ).fetchone()
    assert row is not None
    return bool(row[0])


@pytest.mark.postgres
def test_temporal_window_runs_through_real_auth_context_timezone_and_postgres(
    migrated_database: Any,
    temporal_hibp_stub_url: str,
) -> None:
    auth_settings = _auth_settings(temporal_hibp_stub_url)
    account_ref = _seed_account(migrated_database, auth_settings)
    assert _context_row(migrated_database, account_ref) is None

    app = create_app(_settings(migrated_database, temporal_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        signin = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers=_web_headers(),
        )
        assert signin.status_code == 200
        assert client.cookies.get(SESSION_COOKIE_NAME) is not None

        timeline = client.get(
            "/api/v1/temporal/timeline/window",
            params={
                "start_date": "2026-10-24",
                "end_date_exclusive": "2026-10-27",
            },
            headers={
                **_web_headers(),
                DANTE_TIME_ZONE_HEADER_NAME: "Europe/Rome",
            },
        )

    assert timeline.status_code == 200
    assert timeline.headers["cache-control"] == "no-store"
    assert timeline.json() == {
        "kind": "empty",
        "start_date": "2026-10-24",
        "end_date_exclusive": "2026-10-27",
        "effective_zone_id": "Europe/Rome",
    }
    assert "self_person_ref" not in timeline.text

    context = _context_row(migrated_database, account_ref)
    assert context is not None
    self_person_ref, timezone_mode, fixed_zone_id = context
    assert timezone_mode == "follow_device"
    assert fixed_zone_id is None
    assert _person_exists(migrated_database, self_person_ref)


@pytest.mark.postgres
def test_missing_device_timezone_fails_before_lazy_context_creation(
    migrated_database: Any,
    temporal_hibp_stub_url: str,
) -> None:
    auth_settings = _auth_settings(temporal_hibp_stub_url)
    account_ref = _seed_account(migrated_database, auth_settings)
    app = create_app(_settings(migrated_database, temporal_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        signin = client.post(
            "/api/v1/auth/signin",
            json={"email": _EMAIL, "password": _AUTH_TEST_VALUE},
            headers=_web_headers(),
        )
        assert signin.status_code == 200

        timeline = client.get(
            "/api/v1/temporal/timeline/window",
            params={
                "start_date": "2026-09-07",
                "end_date_exclusive": "2026-09-14",
            },
            headers=_web_headers(),
        )

    assert timeline.status_code == 400
    assert timeline.json()["code"] == "context.device_timezone_required"
    assert _context_row(migrated_database, account_ref) is None
