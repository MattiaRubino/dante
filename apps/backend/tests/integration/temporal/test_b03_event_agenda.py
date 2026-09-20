"""Real PostgreSQL/API proof for B03-D ordered Event Agenda semantics."""

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
def b03d_hibp_stub_url() -> Generator[str]:
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


def _seed_account(database: Any, auth_settings: AuthSettings, email: str) -> None:
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


def _replace(
    client: TestClient,
    event_ref: UUID,
    csrf: str,
    *,
    operation_id: str,
    expected_revision: int,
    agenda_parts: list[str],
):
    return client.put(
        f"/api/v1/temporal/events/{event_ref}/agenda",
        json={
            "operation_id": operation_id,
            "expected_revision": expected_revision,
            "agenda_parts": agenda_parts,
        },
        headers={**_base_headers(), CSRF_HEADER_NAME: csrf},
    )


@pytest.mark.postgres
def test_event_agenda_create_add_edit_reorder_remove_replay_and_reload(
    migrated_database: Any,
    b03d_hibp_stub_url: str,
) -> None:
    email = "event.agenda@example.com"
    auth_settings = _auth_settings(b03d_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, b03d_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        mutation_headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        created = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:b03-d:create",
                "life_area_ref": api_test_life_area(client, mutation_headers),
                "title": "Riunione B03-D",
                "agenda_parts": ["Apertura", "Decisione"],
            },
            headers=mutation_headers,
        )
        assert created.status_code == 201
        body = created.json()
        event_ref = UUID(body["event_ref"])
        assert body["agenda_revision"] == 0
        assert body["agenda_parts"] == ["Apertura", "Decisione"]

        added = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:add",
            expected_revision=0,
            agenda_parts=["Apertura", "Decisione", "Chiusura"],
        )
        assert added.status_code == 200
        assert added.json() == {
            "event_ref": str(event_ref),
            "agenda_revision": 1,
            "agenda_parts": ["Apertura", "Decisione", "Chiusura"],
            "replayed": False,
        }

        edited = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:edit",
            expected_revision=1,
            agenda_parts=["Apertura aggiornata", "Decisione", "Chiusura"],
        )
        assert edited.status_code == 200
        assert edited.json()["agenda_revision"] == 2

        reordered = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:reorder",
            expected_revision=2,
            agenda_parts=["Chiusura", "Apertura aggiornata", "Decisione"],
        )
        assert reordered.status_code == 200
        assert reordered.json()["agenda_revision"] == 3
        assert reordered.json()["agenda_parts"] == [
            "Chiusura",
            "Apertura aggiornata",
            "Decisione",
        ]

        removed = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:remove",
            expected_revision=3,
            agenda_parts=["Chiusura", "Apertura aggiornata"],
        )
        assert removed.status_code == 200
        assert removed.json()["agenda_revision"] == 4
        assert removed.json()["agenda_parts"] == ["Chiusura", "Apertura aggiornata"]

        replay = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:remove",
            expected_revision=3,
            agenda_parts=["Chiusura", "Apertura aggiornata"],
        )
        assert replay.status_code == 200
        assert replay.json()["agenda_revision"] == 4
        assert replay.json()["replayed"] is True

        reuse_conflict = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:remove",
            expected_revision=3,
            agenda_parts=["Intento diverso"],
        )
        assert reuse_conflict.status_code == 409
        assert reuse_conflict.json()["code"] == "temporal.event.agenda_operation_id_reused"

        stale = _replace(
            client,
            event_ref,
            csrf,
            operation_id="operation:b03-d:stale",
            expected_revision=3,
            agenda_parts=["Stale"],
        )
        assert stale.status_code == 409
        assert stale.json()["code"] == "temporal.event.agenda_revision_conflict"

        detail = client.get(
            f"/api/v1/temporal/events/{event_ref}",
            headers=_base_headers(),
        )
        assert detail.status_code == 200
        assert detail.json()["agenda_revision"] == 4
        assert detail.json()["agenda_parts"] == ["Chiusura", "Apertura aggiornata"]

        create_replay = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:b03-d:create",
                "life_area_ref": api_test_life_area(client, mutation_headers),
                "title": "Riunione B03-D",
                "agenda_parts": ["Apertura", "Decisione"],
            },
            headers=mutation_headers,
        )
        assert create_replay.status_code == 200
        assert create_replay.json()["agenda_revision"] == 0
        assert create_replay.json()["agenda_parts"] == ["Apertura", "Decisione"]
        assert create_replay.json()["replayed"] is True

        detail_after_replay = client.get(
            f"/api/v1/temporal/events/{event_ref}",
            headers=_base_headers(),
        )
        assert detail_after_replay.json()["agenda_revision"] == 4
        assert detail_after_replay.json()["agenda_parts"] == [
            "Chiusura",
            "Apertura aggiornata",
        ]

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        parts = connection.execute(
            "SELECT position,content FROM dante.event_agenda_part "
            "WHERE event_ref=%s ORDER BY position",
            (event_ref,),
        ).fetchall()
        current = connection.execute(
            "SELECT revision FROM dante.event_agenda_current WHERE event_ref=%s",
            (event_ref,),
        ).fetchone()
        receipts = connection.execute(
            "SELECT operation_id,expected_revision,resulting_revision "
            "FROM dante.event_agenda_mutation_operation WHERE event_ref=%s "
            "ORDER BY resulting_revision",
            (event_ref,),
        ).fetchall()

    assert parts == [(1, "Chiusura"), (2, "Apertura aggiornata")]
    assert current == (4,)
    assert [row[1:] for row in receipts] == [(0, 1), (1, 2), (2, 3), (3, 4)]


@pytest.mark.postgres
def test_event_agenda_mutation_is_csrf_and_self_scoped(
    migrated_database: Any,
    b03d_hibp_stub_url: str,
) -> None:
    owner_email = "event.agenda.owner@example.com"
    other_email = "event.agenda.other@example.com"
    auth_settings = _auth_settings(b03d_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, owner_email)
    _seed_account(migrated_database, auth_settings, other_email)
    app = create_app(_settings(migrated_database, b03d_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as owner:
        owner_csrf = _signin(owner, owner_email)
        created = owner.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "operation:b03-d:scope-create",
                "title": "Privato",
                "life_area_ref": api_test_life_area(
                    owner, {**_base_headers(), CSRF_HEADER_NAME: owner_csrf}
                ),
            },
            headers={**_base_headers(), CSRF_HEADER_NAME: owner_csrf},
        )
        assert created.status_code == 201
        event_ref = UUID(created.json()["event_ref"])
        no_csrf = owner.put(
            f"/api/v1/temporal/events/{event_ref}/agenda",
            json={
                "operation_id": "operation:b03-d:no-csrf",
                "expected_revision": 0,
                "agenda_parts": ["Non scrivere"],
            },
            headers=_base_headers(),
        )
        assert no_csrf.status_code == 403
        assert no_csrf.json()["code"] == "security.csrf_failed"

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as other:
        other_csrf = _signin(other, other_email)
        rejected = _replace(
            other,
            event_ref,
            other_csrf,
            operation_id="operation:b03-d:foreign",
            expected_revision=0,
            agenda_parts=["Non autorizzato"],
        )
        assert rejected.status_code == 404
        assert rejected.json()["code"] == "temporal.event.not_found"
