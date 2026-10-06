"""Reality and Objective inbox reviews follow canonical state on Activity/Event."""

from __future__ import annotations

from typing import Any

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
from tests.integration.temporal.test_b03_shared_schedule_event import _post_scheduled_event

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def test_inbox_reviews_shared_reality_and_objectives_without_inventing_actual(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "b14.inbox@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        queue_path = "/api/v1/temporal/resolution-queue"

        created = client.post(
            "/api/v1/temporal/authoring/activities",
            json={
                "operation_id": "inbox:activity:create",
                "title": "Allenamento",
                "session_capture_mode": "record",
            },
            headers=headers,
        )
        assert created.status_code == 201
        activity_ref = created.json()["activity_ref"]
        policy = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/reality-policy",
            json={"operation_id": "inbox:activity:policy", "mode_code": "review_on_end"},
            headers=headers,
        )
        assert policy.status_code == 201
        objective = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/objectives",
            json={
                "operation_id": "inbox:activity:objective",
                "label": "Completare la corsa",
                "result_kind": "boolean",
                "comparator_code": None,
                "target_value": None,
                "target_min": None,
                "target_max": None,
                "unit_code": None,
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert objective.status_code == 201
        assert client.get(queue_path, headers=_base_headers()).json()["count"] == 0

        session = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/sessions/manual",
            json={
                "operation_id": "inbox:activity:session",
                "started_at": "2026-10-04T07:00:00Z",
                "ended_at": "2026-10-04T08:00:00Z",
            },
            headers=headers,
        )
        assert session.status_code == 201
        session_data = session.json()

        event = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="inbox:event:create",
            title="Gara",
            placement={
                "kind": "named_zone_local_interval",
                "starts_local_at": "2026-10-04T10:00:00",
                "ends_local_at": "2026-10-04T11:00:00",
                "zone_id": "Europe/Rome",
            },
        )
        assert event.status_code == 201
        event_ref = event.json()["event_ref"]
        event_policy = client.post(
            f"/api/v1/temporal/events/{event_ref}/reality-policy",
            json={"operation_id": "inbox:event:policy", "mode_code": "review_on_end"},
            headers=headers,
        )
        assert event_policy.status_code == 201
        event_objective = client.post(
            f"/api/v1/temporal/events/{event_ref}/objectives",
            json={
                "operation_id": "inbox:event:objective",
                "label": "Arrivare in tempo",
                "result_kind": "boolean",
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert event_objective.status_code == 201

        all_day = _post_scheduled_event(
            client,
            csrf=csrf,
            operation_id="inbox:all-day:create",
            title="Giornata studio",
            placement={
                "kind": "date_span",
                "start_date": "2026-10-03",
                "end_date_exclusive": "2026-10-04",
            },
        )
        assert all_day.status_code == 201
        all_day_ref = all_day.json()["event_ref"]
        all_day_policy = client.post(
            f"/api/v1/temporal/events/{all_day_ref}/reality-policy",
            json={
                "operation_id": "inbox:all-day:policy",
                "mode_code": "review_on_end",
            },
            headers=headers,
        )
        assert all_day_policy.status_code == 201

        queued = client.get(queue_path, headers=_base_headers())
        assert queued.status_code == 200
        assert queued.json()["count"] == 5
        assert {
            (item["subject_ref"], item["reason_code"])
            for item in queued.json()["items"]
        } == {
            (activity_ref, "realization_review"),
            (activity_ref, "objective_review"),
            (event_ref, "realization_review"),
            (event_ref, "objective_review"),
            (all_day_ref, "realization_review"),
        }

        actual = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/actual",
            json={
                "operation_id": "inbox:activity:actual",
                "expected_material_state_ref": None,
                "realization_occurred": True,
                "session_bases": [{
                    "session_ref": session_data["session_ref"],
                    "session_timing_material_state_ref": session_data["timing_material_state_ref"],
                }],
            },
            headers=headers,
        )
        assert actual.status_code == 201
        assessment = client.post(
            f"/api/v1/temporal/objectives/{objective.json()['objective_ref']}/result",
            json={"operation_id": "inbox:activity:result", "observed_boolean": True},
            headers=headers,
        )
        assert assessment.status_code == 201
        remaining = client.get(queue_path, headers=_base_headers()).json()
        assert remaining["count"] == 3
        assert {item["subject_ref"] for item in remaining["items"]} == {
            event_ref,
            all_day_ref,
        }
