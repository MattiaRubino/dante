"""B10-B public API proof for contextual Outcome over canonical Actual."""

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


def _actual_command(operation_id: str) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "expected_material_state_ref": None,
        "realization_occurred": True,
        "timing": None,
        "session_bases": [],
    }


def _outcome_command(
    operation_id: str,
    *,
    result_code: str,
    expected: str | None = None,
    note: str | None = None,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "expected_material_state_ref": expected,
        "result_code": result_code,
        "note": note,
    }


def test_b10_b_outcome_is_contextual_idempotent_correctable_and_actual_scoped(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "b10b.outcome.api@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        mutation_headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        area = api_test_life_area(client, mutation_headers)
        event = client.post(
            "/api/v1/temporal/events",
            json={"operation_id": "b10b:event", "title": "Decision meeting", "life_area_ref": area},
            headers=mutation_headers,
        )
        assert event.status_code == 201
        event_ref = event.json()["event_ref"]
        actual = client.post(
            f"/api/v1/temporal/events/{event_ref}/actual",
            json=_actual_command("b10b:event:actual"),
            headers=mutation_headers,
        )
        assert actual.status_code == 201
        actual_ref = actual.json()["actual_ref"]
        path = f"/api/v1/temporal/actuals/{actual_ref}/outcomes/meeting.decision"

        unknown = client.get(path, headers=_base_headers())
        assert unknown.status_code == 404
        assert unknown.json()["code"] == "temporal.outcome.not_found"

        missing_csrf = client.post(
            path,
            json=_outcome_command("b10b:no-csrf", result_code="decision.deferred"),
            headers=_base_headers(),
        )
        assert missing_csrf.status_code == 403
        assert missing_csrf.json()["code"] == "security.csrf_failed"

        created = client.post(
            path,
            json=_outcome_command(
                "b10b:create",
                result_code="decision.deferred",
                note="Awaiting external input",
            ),
            headers=mutation_headers,
        )
        assert created.status_code == 201
        first = created.json()
        assert first["actual_ref"] == actual_ref
        assert first["vocabulary_code"] == "meeting.decision"
        assert first["result_code"] == "decision.deferred"
        assert first["note"] == "Awaiting external input"
        assert first["replayed"] is False

        current = client.get(path, headers=_base_headers())
        assert current.status_code == 200
        assert current.json()["outcome_ref"] == first["outcome_ref"]
        assert current.json()["material_state_ref"] == first["material_state_ref"]

        replay = client.post(
            path,
            json=_outcome_command(
                "b10b:create",
                result_code="decision.deferred",
                note="Awaiting external input",
            ),
            headers=mutation_headers,
        )
        assert replay.status_code == 200
        assert replay.json()["replayed"] is True
        assert replay.json()["material_state_ref"] == first["material_state_ref"]

        reused = client.post(
            path,
            json=_outcome_command(
                "b10b:create",
                result_code="decision.reached",
                expected=first["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert reused.status_code == 409
        assert reused.json()["code"] == "temporal.outcome.operation_id_reused"

        corrected = client.post(
            path,
            json=_outcome_command(
                "b10b:correct",
                result_code="decision.reached",
                expected=first["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert corrected.status_code == 201
        second = corrected.json()
        assert second["outcome_ref"] == first["outcome_ref"]
        assert second["material_state_ref"] != first["material_state_ref"]
        assert second["result_code"] == "decision.reached"

        stale = client.post(
            path,
            json=_outcome_command(
                "b10b:stale",
                result_code="decision.deferred",
                expected=first["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert stale.status_code == 409
        assert stale.json()["code"] == "temporal.outcome.current_conflict"

        history = client.get(
            f"/api/v1/temporal/outcomes/{first['outcome_ref']}/history",
            headers=_base_headers(),
        )
        assert history.status_code == 200
        rows = history.json()
        assert [row["result_code"] for row in rows] == [
            "decision.deferred",
            "decision.reached",
        ]
        assert rows[0]["current_until_at"] is not None
        assert rows[1]["current_until_at"] is None

        final = client.get(path, headers=_base_headers())
        assert final.status_code == 200
        assert final.json()["material_state_ref"] == second["material_state_ref"]
        assert final.json()["result_code"] == "decision.reached"
