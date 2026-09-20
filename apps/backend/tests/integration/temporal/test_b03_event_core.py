"""Real PostgreSQL proof for the B03-A Event create/read slice."""

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
from b05_legacy_test_support import api_test_life_area
from fastapi.testclient import TestClient
from pydantic import SecretStr

from dante.auth.email import normalize_email
from dante.auth.passwords import PasswordKdf
from dante.auth.sessions import CSRF_HEADER_NAME, WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE
from dante.bootstrap.app import create_app
from dante.context.dependencies import DANTE_TIME_ZONE_HEADER_NAME
from dante.platform.config.auth import AuthSettings, SmtpSecurity
from dante.platform.config.settings import Environment, Settings

_CANONICAL_ORIGIN = "https://dante.test"
_AUTH_TEST_VALUE = "correct horse battery staple"
_PEPPER_KEY_ID = "test-password-v1"
_OTP_KEY_ID = "test-signup-otp-v1"


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
def event_hibp_stub_url() -> Generator[str]:
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
        password_current_pepper_key_id=_PEPPER_KEY_ID,
        password_peppers={_PEPPER_KEY_ID: SecretStr(_PEPPER)},
        csrf_key=SecretStr(_CSRF_KEY),
        signup_otp_current_key_id=_OTP_KEY_ID,
        signup_otp_keys={_OTP_KEY_ID: SecretStr(_OTP_KEY)},
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


def _seed_account(database: Any, auth_settings: AuthSettings, email: str) -> UUID:
    verifier, pepper_key_id = asyncio.run(_hash_password(auth_settings))
    normalized_email = normalize_email(email)
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
            "INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at) "
            "VALUES (%s,'active',%s,NULL)",
            (account_ref, now),
        )
        connection.execute(
            """
            INSERT INTO dante.email_identity(
                email_identity_ref, account_ref, address, comparison_key,
                created_at, verified_at
            ) VALUES (%s,%s,%s,%s,%s,%s)
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
                password_credential_ref, account_ref, verifier, pepper_key_id,
                created_at, updated_at
            ) VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (uuid7(), account_ref, verifier, pepper_key_id, now, now),
        )
        connection.commit()
    return account_ref


def _base_headers() -> dict[str, str]:
    return {
        "Origin": _CANONICAL_ORIGIN,
        "Sec-Fetch-Site": "same-origin",
        WEB_CLIENT_HEADER_NAME: WEB_CLIENT_HEADER_VALUE,
        DANTE_TIME_ZONE_HEADER_NAME: "Europe/Rome",
    }


def _signin(client: TestClient, email: str) -> str:
    response = client.post(
        "/api/v1/auth/signin",
        json={"email": email, "password": _AUTH_TEST_VALUE},
        headers=_base_headers(),
    )
    assert response.status_code == 200
    token = response.json()["csrf_token"]
    assert isinstance(token, str)
    assert token
    return token


def _event_rows(database: Any) -> list[tuple[object, ...]]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return connection.execute(
            """
            SELECT e.event_ref, e.self_person_ref, e.title,
                   a.owner_family, o.operation_id, o.intent_fingerprint
            FROM dante.event_expectation AS e
            JOIN dante.native_address AS a ON a.native_ref=e.event_ref
            JOIN dante.event_create_operation AS o ON o.event_ref=e.event_ref
            ORDER BY e.created_at, e.event_ref
            """
        ).fetchall()


@pytest.mark.postgres
def test_create_event_is_canonical_idempotent_and_self_scoped(
    migrated_database: Any,
    event_hibp_stub_url: str,
) -> None:
    email = "event.user@example.com"
    auth_settings = _auth_settings(event_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, event_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        mutation_headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}

        created = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:b03-a-create-1",
                "title": "Visita medica",
                "life_area_ref": api_test_life_area(client, mutation_headers),
            },
            headers=mutation_headers,
        )
        assert created.status_code == 201
        assert created.headers["cache-control"] == "no-store"
        body = created.json()
        event_ref = UUID(body["event_ref"])
        assert event_ref.version == 7
        assert body["title"] == "Visita medica"
        assert body["replayed"] is False

        replay = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:b03-a-create-1",
                "title": " Visita medica ",
                "life_area_ref": api_test_life_area(client, mutation_headers),
            },
            headers=mutation_headers,
        )
        assert replay.status_code == 200
        assert replay.json()["event_ref"] == str(event_ref)
        assert replay.json()["replayed"] is True

        conflict = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:b03-a-create-1",
                "title": "Intento diverso",
                "life_area_ref": api_test_life_area(client, mutation_headers),
            },
            headers=mutation_headers,
        )
        assert conflict.status_code == 409
        assert conflict.json()["code"] == "temporal.event.operation_id_reused"

        detail = client.get(
            f"/api/v1/temporal/events/{event_ref}",
            headers=_base_headers(),
        )
        assert detail.status_code == 200
        assert detail.headers["cache-control"] == "no-store"
        assert detail.json()["event_ref"] == str(event_ref)
        assert detail.json()["title"] == "Visita medica"

    rows = _event_rows(migrated_database)
    assert len(rows) == 1
    assert UUID(str(rows[0][0])) == event_ref
    assert rows[0][2] == "Visita medica"
    assert rows[0][3] == "event"
    assert rows[0][4] == "operation:b03-a-create-1"
    assert isinstance(rows[0][5], str)
    assert len(rows[0][5]) == 64


@pytest.mark.postgres
def test_event_requires_csrf_and_other_self_cannot_read_it(
    migrated_database: Any,
    event_hibp_stub_url: str,
) -> None:
    first_email = "event.first@example.com"
    second_email = "event.second@example.com"
    auth_settings = _auth_settings(event_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, first_email)
    _seed_account(migrated_database, auth_settings, second_email)
    app = create_app(_settings(migrated_database, event_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as first_client:
        first_csrf = _signin(first_client, first_email)
        rejected = first_client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:no-csrf",
                "title": "Non creare",
                "life_area_ref": str(uuid7()),
            },
            headers=_base_headers(),
        )
        assert rejected.status_code == 403
        assert rejected.json()["code"] == "security.csrf_failed"

        created = first_client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:first-event",
                "title": "Solo primo utente",
                "life_area_ref": api_test_life_area(
                    first_client, {**_base_headers(), CSRF_HEADER_NAME: first_csrf}
                ),
            },
            headers={**_base_headers(), CSRF_HEADER_NAME: first_csrf},
        )
        assert created.status_code == 201
        event_ref = created.json()["event_ref"]

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as second_client:
        _signin(second_client, second_email)
        other_detail = second_client.get(
            f"/api/v1/temporal/events/{event_ref}",
            headers=_base_headers(),
        )
        assert other_detail.status_code == 404
        assert other_detail.json()["code"] == "temporal.event.not_found"

    rows = _event_rows(migrated_database)
    assert [row[2] for row in rows] == ["Solo primo utente"]
