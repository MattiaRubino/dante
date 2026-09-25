"""B10-A public API proof for Event Actual and exact subject-family routing."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app
from tests.integration.temporal.b05_legacy_test_support import api_test_life_area
from tests.integration.temporal.test_b01_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _command(operation_id: str, *, occurred: bool, expected: str | None = None) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "expected_material_state_ref": expected,
        "realization_occurred": occurred,
        "timing": None,
        "session_bases": [],
    }


def test_b10_a_event_actual_public_contract_preserves_unknown_replay_and_family(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "b10a.actual.api@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        mutation_headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        area = api_test_life_area(client, mutation_headers)

        event = client.post(
            "/api/v1/temporal/events",
            json={"operation_id": "b10a:event", "title": "Reality event", "life_area_ref": area},
            headers=mutation_headers,
        )
        activity = client.post(
            "/api/v1/temporal/activities",
            json={"operation_id": "b10a:activity", "title": "Reality activity", "life_area_ref": area},
            headers=mutation_headers,
        )
        assert (event.status_code, activity.status_code) == (201, 201)
        event_ref = event.json()["event_ref"]
        activity_ref = activity.json()["activity_ref"]
        event_actual_path = f"/api/v1/temporal/events/{event_ref}/actual"

        unknown = client.get(event_actual_path, headers=_base_headers())
        assert unknown.status_code == 404
        assert unknown.json()["code"] == "temporal.actual.not_found"

        missing_csrf = client.post(
            event_actual_path,
            json=_command("b10a:event:no-csrf", occurred=True),
            headers=_base_headers(),
        )
        assert missing_csrf.status_code == 403
        assert missing_csrf.json()["code"] == "security.csrf_failed"

        created = client.post(
            event_actual_path,
            json=_command("b10a:event:actual", occurred=True),
            headers=mutation_headers,
        )
        assert created.status_code == 201
        body = created.json()
        assert body["subject_native_ref"] == event_ref
        assert body["realization_occurred"] is True
        assert body["timing"] is None
        assert body["session_bases"] == []
        assert body["replayed"] is False

        current = client.get(event_actual_path, headers=_base_headers())
        assert current.status_code == 200
        assert current.json()["actual_ref"] == body["actual_ref"]
        assert current.json()["material_state_ref"] == body["material_state_ref"]

        replay = client.post(
            event_actual_path,
            json=_command("b10a:event:actual", occurred=True),
            headers=mutation_headers,
        )
        assert replay.status_code == 200
        assert replay.json()["replayed"] is True
        assert replay.json()["material_state_ref"] == body["material_state_ref"]

        reused = client.post(
            event_actual_path,
            json=_command(
                "b10a:event:actual",
                occurred=False,
                expected=body["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert reused.status_code == 409
        assert reused.json()["code"] == "temporal.actual.operation_id_reused"

        wrong_family = client.post(
            f"/api/v1/temporal/events/{activity_ref}/actual",
            json=_command("b10a:event:wrong-family", occurred=True),
            headers=mutation_headers,
        )
        assert wrong_family.status_code == 404
        assert wrong_family.json()["code"] == "temporal.actual.not_found"

        history = client.get(
            f"/api/v1/temporal/actuals/{body['actual_ref']}/history",
            headers=_base_headers(),
        )
        assert history.status_code == 200
        assert len(history.json()) == 1
        assert history.json()[0]["material_state_ref"] == body["material_state_ref"]
        assert history.json()[0]["current_until_at"] is None
