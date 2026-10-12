"""M5 Objective editor: atomic one-save batch, history-safe retirement and replay."""

from __future__ import annotations

from typing import Any
from uuid import UUID

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


def _create_activity(client: TestClient, headers: dict[str, str], key: str) -> str:
    response = client.post(
        "/api/v1/temporal/authoring/activities",
        json={"operation_id": f"m5:{key}:activity", "title": "Studio"},
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return str(response.json()["activity_ref"])


def _objective(
    client: TestClient, headers: dict[str, str], activity: str, key: str,
) -> str:
    response = client.post(
        f"/api/v1/temporal/activities/{activity}/objectives",
        json={
            "operation_id": f"m5:{key}:create", "label": key,
            "result_kind": "quantity", "comparator_code": "gte",
            "target_value": 10, "unit_code": "km",
            "presentation_order": 0 if key in {"First", "Unrecorded"} else 1,
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return str(response.json()["objective_ref"])


def _revise(objective: str, key: str, expected: int) -> dict[str, object]:
    return {
        "objective_ref": objective,
        "change": {
            "operation_id": f"m5:{key}:revise", "expected_revision": expected,
            "label": "Correre 12 km", "result_kind": "quantity",
            "comparator_code": "gte", "target_value": 12,
            "unit_code": "km", "presentation_order": 0,
        },
    }


def test_m5_objective_edits_one_transaction_and_retirement_replay(
    migrated_database: Any, activity_hibp_stub_url: str,
) -> None:
    email = "b14.m5.objective@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        headers = {**_base_headers(), CSRF_HEADER_NAME: _signin(client, email)}
        activity = _create_activity(client, headers, "batch")
        changed = _objective(client, headers, activity, "First")
        removed = _objective(client, headers, activity, "Second")
        endpoint = f"/api/v1/temporal/activities/{activity}/objective-edits"
        command = {
            "add": [{
                "operation_id": "m5:batch:add", "label": "Allenarsi",
                "result_kind": "boolean", "presentation_order": 2,
            }],
            "revise": [_revise(changed, "batch", 0)],
            "retire": [{
                "objective_ref": removed, "operation_id": "m5:batch:retire",
                "expected_revision": 0,
            }],
        }
        applied = client.put(endpoint, json=command, headers=headers)
        assert applied.status_code == 200, applied.text
        assert {item["label"] for item in applied.json()} == {"Correre 12 km", "Allenarsi"}
        assert len(applied.json()) == 2
        replay = client.put(endpoint, json=command, headers=headers)
        assert replay.status_code == 200, replay.text
        assert {row["objective_ref"] for row in replay.json()} == {
            row["objective_ref"] for row in applied.json()
        }
        assert client.get(
            f"/api/v1/temporal/objectives/{removed}/definition",
            headers=_base_headers(),
        ).status_code == 404
        with psycopg.connect(
            host=migrated_database.cluster.host,
            port=migrated_database.cluster.port,
            dbname=migrated_database.name,
            user=migrated_database.cluster.admin_user,
            password=migrated_database.cluster.admin_password,
        ) as connection:
            tombstone = connection.execute(
                "SELECT retired_at,retirement_operation_id FROM dante.temporal_objective "
                "WHERE objective_ref=%s", (UUID(removed),),
            ).fetchone()
            assert tombstone is not None
            assert tombstone[0] is not None
            assert tombstone[1] == "m5:batch:retire"
        other = _create_activity(client, headers, "other")
        unrelated = client.put(
            f"/api/v1/temporal/activities/{other}/objective-edits",
            json={"revise": [_revise(changed, "other", 1)]},
            headers=headers,
        )
        assert unrelated.status_code == 409


def test_m5_recorded_result_retirement_veto_rolls_back_other_objective_edits(
    migrated_database: Any, activity_hibp_stub_url: str,
) -> None:
    email = "b14.m5.protect@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        headers = {**_base_headers(), CSRF_HEADER_NAME: _signin(client, email)}
        activity = _create_activity(client, headers, "protect")
        changed = _objective(client, headers, activity, "Unrecorded")
        protected = _objective(client, headers, activity, "Recorded")
        result = client.post(
            f"/api/v1/temporal/objectives/{protected}/result",
            json={
                "operation_id": "m5:observed:result",
                "observed_numeric": 8,
            },
            headers=headers,
        )
        assert result.status_code == 201, result.text
        endpoint = f"/api/v1/temporal/activities/{activity}/objective-edits"
        rejected = client.put(endpoint, json={
            "add": [{
                "operation_id": "m5:rollback:add", "label": "Third",
                "result_kind": "boolean", "presentation_order": 3,
            }],
            "revise": [_revise(changed, "rollback", 0)],
            "retire": [{
                "objective_ref": protected,
                "operation_id": "m5:rollback:retire", "expected_revision": 0,
            }],
        }, headers=headers)
        assert rejected.status_code == 409, rejected.text
        assert "risultati registrati" in rejected.json()["detail"]
        latest = client.get(
            f"/api/v1/temporal/activities/{activity}/objectives",
            headers=_base_headers(),
        )
        assert latest.status_code == 200, latest.text
        assert {row["label"] for row in latest.json()} == {"Unrecorded", "Recorded"}
        assert client.get(
            f"/api/v1/temporal/objectives/{changed}/definition",
            headers=_base_headers(),
        ).json()["definition_revision"] == 0
