"""B10-B public API proof for canonical Outcome disposition over Actual."""

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


def _actual_command(operation_id: str, *, expected: str | None = None, occurred: bool = True) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "expected_material_state_ref": expected,
        "realization_occurred": occurred,
        "timing": None,
        "session_bases": [],
    }


def _outcome_command(
    operation_id: str,
    *,
    actual_state_ref: str,
    disposition_code: str,
    expected: str | None = None,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "actual_realization_material_state_ref": actual_state_ref,
        "expected_material_state_ref": expected,
        "disposition_code": disposition_code,
    }


def test_b10_b_outcome_is_idempotent_correctable_and_actual_state_scoped(
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
        actual_body = actual.json()
        actual_ref = actual_body["actual_ref"]
        actual_state_ref = actual_body["material_state_ref"]
        path = f"/api/v1/temporal/actuals/{actual_ref}/outcome"

        unknown = client.get(path, headers=_base_headers())
        assert unknown.status_code == 404
        assert unknown.json()["code"] == "temporal.outcome.not_found"

        missing_csrf = client.post(
            path,
            json=_outcome_command(
                "b10b:no-csrf",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.deferred",
            ),
            headers=_base_headers(),
        )
        assert missing_csrf.status_code == 403
        assert missing_csrf.json()["code"] == "security.csrf_failed"

        created = client.post(
            path,
            json=_outcome_command(
                "b10b:create",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.deferred",
            ),
            headers=mutation_headers,
        )
        assert created.status_code == 201
        first = created.json()
        assert first["actual_ref"] == actual_ref
        assert first["actual_realization_material_state_ref"] == actual_state_ref
        assert first["disposition_code"] == "decision.deferred"
        assert first["replayed"] is False

        current = client.get(path, headers=_base_headers())
        assert current.status_code == 200
        assert current.json()["outcome_ref"] == first["outcome_ref"]
        assert current.json()["material_state_ref"] == first["material_state_ref"]

        replay = client.post(
            path,
            json=_outcome_command(
                "b10b:create",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.deferred",
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
                actual_state_ref=actual_state_ref,
                disposition_code="decision.reached",
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
                actual_state_ref=actual_state_ref,
                disposition_code="decision.reached",
                expected=first["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert corrected.status_code == 201
        second = corrected.json()
        assert second["outcome_ref"] == first["outcome_ref"]
        assert second["material_state_ref"] != first["material_state_ref"]
        assert second["disposition_code"] == "decision.reached"

        stale = client.post(
            path,
            json=_outcome_command(
                "b10b:stale",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.deferred",
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
        assert [row["disposition_code"] for row in rows] == [
            "decision.deferred",
            "decision.reached",
        ]
        assert rows[0]["current_until_at"] is not None
        assert rows[1]["current_until_at"] is None

        corrected_actual = client.post(
            f"/api/v1/temporal/events/{event_ref}/actual",
            json=_actual_command(
                "b10b:event:actual:correct",
                expected=actual_state_ref,
                occurred=False,
            ),
            headers=mutation_headers,
        )
        assert corrected_actual.status_code == 201
        new_actual_state_ref = corrected_actual.json()["material_state_ref"]

        old_basis = client.post(
            path,
            json=_outcome_command(
                "b10b:old-basis",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.cancelled",
                expected=second["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert old_basis.status_code == 409
        assert old_basis.json()["code"] == "temporal.outcome.current_conflict"

        rebased = client.post(
            path,
            json=_outcome_command(
                "b10b:new-basis",
                actual_state_ref=new_actual_state_ref,
                disposition_code="decision.cancelled",
                expected=second["material_state_ref"],
            ),
            headers=mutation_headers,
        )
        assert rebased.status_code == 201
        assert rebased.json()["outcome_ref"] == first["outcome_ref"]
        assert rebased.json()["actual_realization_material_state_ref"] == new_actual_state_ref
