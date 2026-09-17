"""Real PostgreSQL/API proof for the B03-C Event placement lifecycle."""

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
def b03c_hibp_stub_url() -> Generator[str]:
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


def _mutation_headers(csrf: str) -> dict[str, str]:
    return {**_base_headers(), CSRF_HEADER_NAME: csrf}


def _timeline(client: TestClient, *, start: str, end: str) -> list[dict[str, object]]:
    response = client.get(
        "/api/v1/temporal/timeline/window",
        params={"start_date": start, "end_date_exclusive": end},
        headers=_base_headers(),
    )
    assert response.status_code == 200
    payload = response.json()
    return [] if payload["kind"] == "empty" else payload["items"]


def _schedule_history(database: Any, schedule_ref: UUID) -> tuple[UUID | None, list[tuple[Any, ...]]]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        current_row = connection.execute(
            """
            SELECT current.material_state_ref
              FROM dante.schedule AS schedule
              LEFT JOIN dante.scoped_current_material_state AS current
                ON current.scoped_owner_ref = schedule.schedule_ref
               AND current.facet_code = 'schedule.placement'
             WHERE schedule.schedule_ref = %s
            """,
            (schedule_ref,),
        ).fetchone()
        history = connection.execute(
            """
            SELECT material_state_ref, current_from_at, current_until_at
              FROM dante.schedule_placement_current_history
             WHERE schedule_ref = %s
             ORDER BY current_from_at, material_state_ref
            """,
            (schedule_ref,),
        ).fetchall()
    assert current_row is not None
    current = None if current_row[0] is None else UUID(str(current_row[0]))
    return current, history


@pytest.mark.postgres
def test_b03c_event_reschedule_postpone_and_guarded_undo_preserve_identity_and_history(
    migrated_database: Any,
    b03c_hibp_stub_url: str,
) -> None:
    email = "b03c.lifecycle@example.com"
    auth_settings = _auth_settings(b03c_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, b03c_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = _mutation_headers(csrf)

        created = client.post(
            "/api/v1/temporal/events/scheduled",
            json={
                "operation_id": "operation:b03-c:create",
                "title": "Revisione contratto",
                "placement": {
                    "kind": "floating_local_interval",
                    "starts_local_at": "2026-09-21T09:00:00",
                    "ends_local_at": "2026-09-21T10:00:00",
                },
            },
            headers=headers,
        )
        assert created.status_code == 201
        initial = created.json()
        event_ref = UUID(initial["event_ref"])
        schedule_ref = UUID(initial["schedule_ref"])
        initial_state_ref = UUID(initial["placement_material_state_ref"])

        revised = client.patch(
            f"/api/v1/temporal/schedules/{schedule_ref}/placement",
            json={
                "operation_id": "operation:b03-c:revise",
                "expected_placement_material_state_ref": str(initial_state_ref),
                "placement": {
                    "kind": "floating_local_interval",
                    "starts_local_at": "2026-09-22T14:30:00",
                    "ends_local_at": "2026-09-22T16:00:00",
                },
            },
            headers=headers,
        )
        assert revised.status_code == 200
        revised_body = revised.json()
        revised_state_ref = UUID(revised_body["placement_material_state_ref"])
        assert revised_state_ref != initial_state_ref
        assert UUID(revised_body["previous_placement_material_state_ref"]) == initial_state_ref

        old_window = _timeline(
            client,
            start="2026-09-21",
            end="2026-09-22",
        )
        assert all(item.get("event_ref") != str(event_ref) for item in old_window)

        revised_window = _timeline(
            client,
            start="2026-09-22",
            end="2026-09-23",
        )
        event_item = next(
            item for item in revised_window if item.get("event_ref") == str(event_ref)
        )
        assert event_item["kind"] == "scheduled_event"
        assert event_item["schedule_ref"] == str(schedule_ref)
        assert event_item["placement_material_state_ref"] == str(revised_state_ref)
        assert event_item["starts_local_at"] == "2026-09-22T14:30:00"
        assert event_item["ends_local_at"] == "2026-09-22T16:00:00"

        event_read = client.get(
            f"/api/v1/temporal/events/{event_ref}",
            headers=_base_headers(),
        )
        assert event_read.status_code == 200
        assert event_read.json()["event_ref"] == str(event_ref)
        assert event_read.json()["title"] == "Revisione contratto"

        unscheduled = client.post(
            f"/api/v1/temporal/schedules/{schedule_ref}/unschedule",
            json={
                "operation_id": "operation:b03-c:postpone",
                "expected_placement_material_state_ref": str(revised_state_ref),
            },
            headers=headers,
        )
        assert unscheduled.status_code == 200
        unscheduled_body = unscheduled.json()
        assert UUID(unscheduled_body["previous_placement_material_state_ref"]) == revised_state_ref
        assert unscheduled_body["unschedule_operation_id"] == "operation:b03-c:postpone"

        # Postponed/TBD is not a fabricated placement: the Event remains readable,
        # its Schedule identity/history remain, and Timeline has no current item.
        postponed_read = client.get(
            f"/api/v1/temporal/events/{event_ref}",
            headers=_base_headers(),
        )
        assert postponed_read.status_code == 200
        assert postponed_read.json()["event_ref"] == str(event_ref)
        assert all(
            item.get("event_ref") != str(event_ref)
            for item in _timeline(client, start="2026-09-22", end="2026-09-23")
        )

        current_after_postpone, history_after_postpone = _schedule_history(
            migrated_database,
            schedule_ref,
        )
        assert current_after_postpone is None
        assert [UUID(str(row[0])) for row in history_after_postpone] == [
            initial_state_ref,
            revised_state_ref,
        ]
        assert all(row[2] is not None for row in history_after_postpone)

        stale_revision = client.patch(
            f"/api/v1/temporal/schedules/{schedule_ref}/placement",
            json={
                "operation_id": "operation:b03-c:stale-while-tbd",
                "expected_placement_material_state_ref": str(revised_state_ref),
                "placement": {
                    "kind": "floating_local_interval",
                    "starts_local_at": "2026-09-23T09:00:00",
                    "ends_local_at": "2026-09-23T10:00:00",
                },
            },
            headers=headers,
        )
        assert stale_revision.status_code == 409
        assert stale_revision.json()["code"] == "temporal.schedule.revision_conflict"

        restored = client.post(
            f"/api/v1/temporal/schedules/{schedule_ref}/unschedule/undo",
            json={
                "operation_id": "operation:b03-c:undo-postpone",
                "unschedule_operation_id": unscheduled_body["unschedule_operation_id"],
            },
            headers=headers,
        )
        assert restored.status_code == 200
        restored_body = restored.json()
        restored_state_ref = UUID(restored_body["placement_material_state_ref"])
        assert restored_state_ref not in {initial_state_ref, revised_state_ref}
        assert UUID(restored_body["restored_from_placement_material_state_ref"]) == revised_state_ref
        assert restored_body["starts_local_at"] == "2026-09-22T14:30:00"
        assert restored_body["ends_local_at"] == "2026-09-22T16:00:00"

        restored_window = _timeline(
            client,
            start="2026-09-22",
            end="2026-09-23",
        )
        restored_item = next(
            item for item in restored_window if item.get("event_ref") == str(event_ref)
        )
        assert restored_item["schedule_ref"] == str(schedule_ref)
        assert restored_item["placement_material_state_ref"] == str(restored_state_ref)

        current_after_undo, history_after_undo = _schedule_history(
            migrated_database,
            schedule_ref,
        )
        assert current_after_undo == restored_state_ref
        assert [UUID(str(row[0])) for row in history_after_undo] == [
            initial_state_ref,
            revised_state_ref,
            restored_state_ref,
        ]
        assert history_after_undo[0][2] is not None
        assert history_after_undo[1][2] is not None
        assert history_after_undo[2][2] is None

        undo_replay = client.post(
            f"/api/v1/temporal/schedules/{schedule_ref}/unschedule/undo",
            json={
                "operation_id": "operation:b03-c:undo-postpone",
                "unschedule_operation_id": unscheduled_body["unschedule_operation_id"],
            },
            headers=headers,
        )
        assert undo_replay.status_code == 200
        assert undo_replay.json()["placement_material_state_ref"] == str(restored_state_ref)
        assert undo_replay.json()["replayed"] is True

        stale_after_undo = client.post(
            f"/api/v1/temporal/schedules/{schedule_ref}/unschedule",
            json={
                "operation_id": "operation:b03-c:stale-after-undo",
                "expected_placement_material_state_ref": str(revised_state_ref),
            },
            headers=headers,
        )
        assert stale_after_undo.status_code == 409
        assert stale_after_undo.json()["code"] == "temporal.schedule.unschedule_conflict"

    assert event_ref.version == 7
    assert schedule_ref.version == 7
