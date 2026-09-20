"""Real PostgreSQL/API proof for B03-B shared Schedule + Event Timeline."""

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
def b03b_hibp_stub_url() -> Generator[str]:
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


def _post_scheduled_event(
    client: TestClient,
    *,
    csrf: str,
    operation_id: str,
    title: str,
    placement: dict[str, object],
):
    return client.post(
        "/api/v1/temporal/events/scheduled",
        json={
            "operation_id": operation_id,
            "life_area_ref": api_test_life_area(
                client, {**_base_headers(), CSRF_HEADER_NAME: csrf}
            ),
            "title": title,
            "placement": placement,
        },
        headers={**_base_headers(), CSRF_HEADER_NAME: csrf},
    )


@pytest.mark.postgres
def test_b03b_event_forms_share_schedule_and_project_with_activity(
    migrated_database: Any,
    b03b_hibp_stub_url: str,
) -> None:
    email = "b03b.timeline@example.com"
    auth_settings = _auth_settings(b03b_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, b03b_hibp_stub_url))

    event_refs: list[UUID] = []
    schedule_refs: list[UUID] = []

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        mutation_headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}

        activity = client.post(
            "/api/v1/temporal/activities/scheduled",
            json={
                "operation_id": "operation:b03-b:activity-witness",
                "life_area_ref": api_test_life_area(client, mutation_headers),
                "title": "Activity witness",
                "placement": {
                    "kind": "floating_local_interval",
                    "starts_local_at": "2026-09-17T17:00:00",
                    "ends_local_at": "2026-09-17T18:00:00",
                },
            },
            headers=mutation_headers,
        )
        assert activity.status_code == 201

        floating_payload = {
            "kind": "floating_local_interval",
            "starts_local_at": "2026-09-17T18:30:00",
            "ends_local_at": "2026-09-17T20:00:00",
        }
        floating = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:floating",
            title="Evento serale",
            placement=floating_payload,
        )
        assert floating.status_code == 201
        floating_body = floating.json()
        assert floating_body["temporal_form"] == "floating_local"
        assert floating_body["replayed"] is False
        event_refs.append(UUID(floating_body["event_ref"]))
        schedule_refs.append(UUID(floating_body["schedule_ref"]))

        replay = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:floating",
            title=" Evento serale ",
            placement=floating_payload,
        )
        assert replay.status_code == 200
        assert replay.json()["event_ref"] == floating_body["event_ref"]
        assert replay.json()["schedule_ref"] == floating_body["schedule_ref"]
        assert (
            replay.json()["placement_material_state_ref"]
            == (floating_body["placement_material_state_ref"])
        )
        assert replay.json()["replayed"] is True

        single_day = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:single-day",
            title="Giornata intera",
            placement={
                "kind": "date_span",
                "start_date": "2026-09-18",
                "end_date_exclusive": "2026-09-19",
            },
        )
        assert single_day.status_code == 201
        assert single_day.json()["temporal_form"] == "date_span"
        event_refs.append(UUID(single_day.json()["event_ref"]))
        schedule_refs.append(UUID(single_day.json()["schedule_ref"]))

        multi_day = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:multi-day",
            title="Conferenza",
            placement={
                "kind": "date_span",
                "start_date": "2026-09-19",
                "end_date_exclusive": "2026-09-22",
            },
        )
        assert multi_day.status_code == 201
        assert multi_day.json()["start_date"] == "2026-09-19"
        assert multi_day.json()["end_date_exclusive"] == "2026-09-22"
        event_refs.append(UUID(multi_day.json()["event_ref"]))
        schedule_refs.append(UUID(multi_day.json()["schedule_ref"]))

        named = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:named-zone",
            title="Cambio ora",
            placement={
                "kind": "named_zone_local_interval",
                "starts_local_at": "2026-10-25T02:10:00",
                "ends_local_at": "2026-10-25T02:40:00",
                "zone_id": "Europe/Rome",
                "disambiguation": "later",
            },
        )
        assert named.status_code == 201
        named_body = named.json()
        assert named_body["temporal_form"] == "named_zone_local"
        assert named_body["zone_id"] == "Europe/Rome"
        assert datetime.fromisoformat(named_body["resolved_start_at"]) == datetime(
            2026, 10, 25, 1, 10, tzinfo=UTC
        )
        assert datetime.fromisoformat(named_body["resolved_end_at"]) == datetime(
            2026, 10, 25, 1, 40, tzinfo=UTC
        )
        event_refs.append(UUID(named_body["event_ref"]))
        schedule_refs.append(UUID(named_body["schedule_ref"]))

        september = client.get(
            "/api/v1/temporal/timeline/window",
            params={
                "start_date": "2026-09-17",
                "end_date_exclusive": "2026-09-22",
            },
            headers=_base_headers(),
        )
        assert september.status_code == 200
        september_body = september.json()
        assert september_body["kind"] == "window"
        by_title = {item["title"]: item for item in september_body["items"]}
        assert set(by_title) == {
            "Activity witness",
            "Evento serale",
            "Giornata intera",
            "Conferenza",
        }
        assert by_title["Activity witness"]["kind"] == "scheduled_activity"
        assert "activity_ref" in by_title["Activity witness"]
        assert "event_ref" not in by_title["Activity witness"]
        for title in ("Evento serale", "Giornata intera", "Conferenza"):
            assert by_title[title]["kind"] == "scheduled_event"
            assert "event_ref" in by_title[title]
            assert "activity_ref" not in by_title[title]
        assert by_title["Giornata intera"]["temporal_form"] == "date_span"
        assert by_title["Conferenza"]["start_date"] == "2026-09-19"
        assert by_title["Conferenza"]["end_date_exclusive"] == "2026-09-22"

        october = client.get(
            "/api/v1/temporal/timeline/window",
            params={
                "start_date": "2026-10-25",
                "end_date_exclusive": "2026-10-26",
            },
            headers=_base_headers(),
        )
        assert october.status_code == 200
        october_items = october.json()["items"]
        assert len(october_items) == 1
        assert october_items[0]["kind"] == "scheduled_event"
        assert october_items[0]["event_ref"] == named_body["event_ref"]
        assert october_items[0]["temporal_form"] == "named_zone_local"
        assert october_items[0]["zone_id"] == "Europe/Rome"

    assert all(ref.version == 7 for ref in event_refs)
    assert all(ref.version == 7 for ref in schedule_refs)
    assert len(set(event_refs)) == 4
    assert len(set(schedule_refs)) == 4

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        rows = connection.execute(
            """
            SELECT schedule.schedule_ref,
                   schedule.subject_native_ref,
                   address.owner_family,
                   current.material_state_ref,
                   count(history.*) FILTER (WHERE history.schedule_ref IS NOT NULL)
              FROM dante.schedule AS schedule
              JOIN dante.native_address AS address
                ON address.native_ref = schedule.subject_native_ref
              JOIN dante.scoped_current_material_state AS current
                ON current.scoped_owner_ref = schedule.schedule_ref
               AND current.facet_code = 'schedule.placement'
              LEFT JOIN dante.schedule_placement_current_history AS history
                ON history.schedule_ref = schedule.schedule_ref
             WHERE schedule.schedule_ref = ANY(%s)
             GROUP BY schedule.schedule_ref, schedule.subject_native_ref,
                      address.owner_family, current.material_state_ref
             ORDER BY schedule.schedule_ref
            """,
            (schedule_refs,),
        ).fetchall()
        separate_engine = connection.execute(
            "SELECT to_regclass('dante.event_schedule')"
        ).fetchone()

    assert len(rows) == 4
    assert {UUID(str(row[1])) for row in rows} == set(event_refs)
    assert all(row[2] == "event" for row in rows)
    assert all(row[3] is not None for row in rows)
    assert all(row[4] == 1 for row in rows)
    assert separate_engine == (None,)


@pytest.mark.postgres
def test_b03b_event_authoring_fails_closed_without_partial_event(
    migrated_database: Any,
    b03b_hibp_stub_url: str,
) -> None:
    email = "b03b.failclosed@example.com"
    auth_settings = _auth_settings(b03b_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, b03b_hibp_stub_url))

    def event_count() -> int:
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator",
                migrated_database.cluster.migrator_password,
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            row = connection.execute("SELECT count(*) FROM dante.event_expectation").fetchone()
        assert row is not None
        return int(row[0])

    before = event_count()
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)

        invalid_span = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:invalid-span",
            title="Invalid span",
            placement={
                "kind": "date_span",
                "start_date": "2026-09-20",
                "end_date_exclusive": "2026-09-20",
            },
        )
        assert invalid_span.status_code == 422
        assert invalid_span.json()["code"] == "temporal.event.invalid_schedule_create"

        coarse = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="operation:b03-b:coarse-rejected",
            title="Coarse Event",
            placement={
                "kind": "coarse_local_period",
                "local_date": "2026-09-20",
                "period": "morning",
            },
        )
        assert coarse.status_code == 422

    assert event_count() == before
