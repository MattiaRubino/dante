"""U6 Activity Reality policy: real review queue and B10 auto-confirm proof."""

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

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _policy(
    client: TestClient,
    headers: dict[str, str],
    activity_ref: str,
    mode: str,
    operation_id: str,
) -> None:
    response = client.post(
        f"/api/v1/temporal/activities/{activity_ref}/outcome-review-policy",
        json={
            "operation_id": operation_id,
            "mode_code": mode,
            "expected_state_ref": None,
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["mode_code"] == mode


def test_review_on_end_uses_real_session_basis_and_disappears_after_actual(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "u6.reality.review@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        created = client.post(
            "/api/v1/temporal/authoring/activities",
            json={
                "operation_id": "u6:reality:review:create",
                "title": "Review after work",
                "session_capture_mode": "record",
            },
            headers=headers,
        )
        assert created.status_code == 201
        activity_ref = created.json()["activity_ref"]
        _policy(
            client,
            headers,
            activity_ref,
            "review_on_end",
            "u6:reality:review:policy",
        )

        assert client.get("/api/v1/temporal/resolution-queue", headers=_base_headers()).json() == {
            "items": [],
            "count": 0,
        }

        recorded = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/sessions/manual",
            json={
                "operation_id": "u6:reality:review:session",
                "started_at": "2026-10-04T07:00:00Z",
                "ended_at": "2026-10-04T08:00:00Z",
            },
            headers=headers,
        )
        assert recorded.status_code == 201
        session = recorded.json()

        queued = client.get("/api/v1/temporal/resolution-queue", headers=_base_headers())
        assert queued.status_code == 200
        assert queued.json()["count"] == 1
        item = queued.json()["items"][0]
        assert item["reason_code"] == "realization_review"
        assert item["subject_kind"] == "activity"
        assert item["subject_ref"] == activity_ref
        assert item["session_ref"] == session["session_ref"]
        assert item["session_timing_material_state_ref"] == session["timing_material_state_ref"]
        assert item["reconciliation_ref"] is None
        assert item["outcome_ref"] is None
        assert item["actions"] == ["record_realization"]

        actual = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/actual",
            json={
                "operation_id": "u6:reality:review:actual",
                "expected_material_state_ref": None,
                "realization_occurred": True,
                "session_bases": [
                    {
                        "session_ref": session["session_ref"],
                        "session_timing_material_state_ref": session[
                            "timing_material_state_ref"
                        ],
                    }
                ],
            },
            headers=headers,
        )
        assert actual.status_code == 201
        assert actual.json()["session_bases"] == [
            {
                "session_ref": session["session_ref"],
                "session_timing_material_state_ref": session[
                    "timing_material_state_ref"
                ],
            }
        ]
        assert client.get(
            "/api/v1/temporal/resolution-queue", headers=_base_headers()
        ).json() == {"items": [], "count": 0}


def test_auto_confirm_only_attests_an_existing_activity_outcome(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "u6.reality.auto@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        created = client.post(
            "/api/v1/temporal/authoring/activities",
            json={"operation_id": "u6:reality:auto:create", "title": "Auto attest"},
            headers=headers,
        )
        assert created.status_code == 201
        activity_ref = created.json()["activity_ref"]
        _policy(
            client,
            headers,
            activity_ref,
            "auto_confirm_outcome",
            "u6:reality:auto:policy",
        )

        # Policy alone invents no B10 truth.
        missing_actual = client.get(
            f"/api/v1/temporal/activities/{activity_ref}/actual",
            headers=_base_headers(),
        )
        assert missing_actual.status_code == 404

        actual = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/actual",
            json={
                "operation_id": "u6:reality:auto:actual",
                "expected_material_state_ref": None,
                "realization_occurred": True,
            },
            headers=headers,
        )
        assert actual.status_code == 201
        actual_body = actual.json()

        outcome = client.post(
            f"/api/v1/temporal/actuals/{actual_body['actual_ref']}/outcome",
            json={
                "operation_id": "u6:reality:auto:outcome",
                "actual_realization_material_state_ref": actual_body["material_state_ref"],
                "expected_material_state_ref": None,
                "disposition_code": "completed",
            },
            headers=headers,
        )
        assert outcome.status_code == 201
        outcome_body = outcome.json()

        confirmations = client.get(
            f"/api/v1/temporal/outcomes/{outcome_body['outcome_ref']}/confirmations",
            headers=_base_headers(),
        )
        assert confirmations.status_code == 200
        body = confirmations.json()
        assert len(body) == 1
        assert body[0]["outcome_ref"] == outcome_body["outcome_ref"]
        assert body[0]["outcome_disposition_material_state_ref"] == outcome_body[
            "material_state_ref"
        ]
        assert body[0]["purpose_code"] == "activity.policy.auto"
        assert body[0]["stance_code"] == "attested"
        assert body[0]["confirmer_is_self"] is True

        # Outcome replay also replays the derived Confirmation; no duplicate is created.
        replay = client.post(
            f"/api/v1/temporal/actuals/{actual_body['actual_ref']}/outcome",
            json={
                "operation_id": "u6:reality:auto:outcome",
                "actual_realization_material_state_ref": actual_body["material_state_ref"],
                "expected_material_state_ref": None,
                "disposition_code": "completed",
            },
            headers=headers,
        )
        assert replay.status_code == 200
        assert replay.json()["outcome_ref"] == outcome_body["outcome_ref"]
        assert len(
            client.get(
                f"/api/v1/temporal/outcomes/{outcome_body['outcome_ref']}/confirmations",
                headers=_base_headers(),
            ).json()
        ) == 1
