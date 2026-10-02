"""U6 explicit Activity Session policy read, correction and self-scope proof."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest
from fastapi.testclient import TestClient
from tests.integration.temporal.test_b01_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def test_activity_execution_policy_is_explicit_current_and_self_scoped(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    alice = "u6.policy.alice@example.com"
    bob = "u6.policy.bob@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, alice)
    _seed_account(migrated_database, auth_settings, bob)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, alice)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        created = client.post(
            "/api/v1/temporal/authoring/activities",
            json={"operation_id": "u6:policy:create", "title": "Write DANTE"},
            headers=headers,
        )
        assert created.status_code == 201
        activity_ref = created.json()["activity_ref"]
        path = f"/api/v1/temporal/activities/{activity_ref}/execution-policy"
        initial = client.get(path, headers=_base_headers())
        assert initial.status_code == 200
        assert initial.json() == {
            "activity_ref": activity_ref, "state_ref": None,
            "mode_code": "disabled", "replayed": False,
        }

        request = {
            "operation_id": "u6:policy:live", "mode_code": "live",
            "expected_state_ref": None,
        }
        first = client.post(path, json=request, headers=headers)
        assert first.status_code == 201
        assert first.json()["mode_code"] == "live"
        state_ref = first.json()["state_ref"]
        assert state_ref is not None
        assert client.post(path, json=request, headers=headers).json() == {
            **first.json(), "replayed": True,
        }
        assert client.get(path, headers=_base_headers()).json()["state_ref"] == state_ref

        started = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/sessions",
            json={"operation_id": "u6:policy:start"}, headers=headers,
        )
        assert started.status_code == 201
        assert started.json()["subject_native_ref"] == activity_ref

        stale = client.post(
            path,
            json={"operation_id": "u6:policy:stale", "mode_code": "disabled",
                  "expected_state_ref": None},
            headers=headers,
        )
        assert stale.status_code == 409
        invalid = client.post(
            path,
            json={"operation_id": "u6:policy:invalid", "mode_code": "future"},
            headers=headers,
        )
        assert invalid.status_code == 422

        disabled = client.post(
            path,
            json={"operation_id": "u6:policy:disable", "mode_code": "disabled",
                  "expected_state_ref": state_ref},
            headers=headers,
        )
        assert disabled.status_code == 201
        assert disabled.json()["state_ref"] != state_ref
        assert client.get(path, headers=_base_headers()).json()["mode_code"] == "disabled"
        blocked = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/sessions",
            json={"operation_id": "u6:policy:blocked"}, headers=headers,
        )
        assert blocked.status_code == 409
        assert blocked.json()["code"] == "temporal.session.capture_disabled"
        replay_started = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/sessions",
            json={"operation_id": "u6:policy:start"}, headers=headers,
        )
        assert replay_started.status_code == 200
        assert replay_started.json()["session_ref"] == started.json()["session_ref"]

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as other:
        _signin(other, bob)
        assert other.get(path, headers=_base_headers()).status_code == 404

    with psycopg.connect(**migrated_database.connection_kwargs(
        "dante_runtime", migrated_database.cluster.runtime_password,
    )) as connection, pytest.raises(psycopg.errors.InsufficientPrivilege):
        connection.execute("SELECT * FROM dante.activity_execution_policy LIMIT 1")


def test_activity_create_commits_policy_atomically_and_replays(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "u6.policy.create@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        command = {
            "operation_id": "u6:policy:atomic", "title": "Read DANTE",
            "session_capture_mode": "live",
        }
        first = client.post("/api/v1/temporal/authoring/activities", json=command, headers=headers)
        assert first.status_code == 201
        assert first.json()["session_capture_mode"] == "live"
        activity_ref = first.json()["activity_ref"]
        policy_path = f"/api/v1/temporal/activities/{activity_ref}/execution-policy"
        assert client.get(policy_path, headers=_base_headers()).json()["mode_code"] == "live"

        replay = client.post("/api/v1/temporal/authoring/activities", json=command, headers=headers)
        assert replay.status_code == 200
        assert replay.json()["activity_ref"] == activity_ref
        assert replay.json()["replayed"] is True

        reuse = client.post(
            "/api/v1/temporal/authoring/activities",
            json={**command, "session_capture_mode": "record"}, headers=headers,
        )
        assert reuse.status_code == 409
        assert client.get(policy_path, headers=_base_headers()).json()["mode_code"] == "live"
