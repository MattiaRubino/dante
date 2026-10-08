"""M2: same logical Objective, immutable definitions, corrected reality, owner/CAS."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
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
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _definition(*, operation: str, expected: int, target: int = 7) -> dict[str, object]:
    return {
        "operation_id": operation,
        "expected_revision": expected,
        "label": "Percorrere almeno sette km",
        "result_kind": "quantity",
        "comparator_code": "gte",
        "target_value": target,
        "presentation_order": 0,
    }


def test_objective_definition_and_result_corrections_are_canonical_without_deletion(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    alice = "b14.m2.alice@example.com"
    bob = "b14.m2.bob@example.com"
    for email in (alice, bob):
        _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, alice)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        created = client.post(
            "/api/v1/temporal/authoring/activities",
            json={"operation_id": "m2:activity", "title": "Corsa",
                  "session_capture_mode": "record"},
            headers=headers,
        )
        assert created.status_code == 201, created.text
        activity_ref = created.json()["activity_ref"]
        created_objective = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/objectives",
            json={
                "operation_id": "m2:create",
                "label": "Percorrere dieci km",
                "result_kind": "quantity",
                "comparator_code": "gte",
                "target_value": 10,
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert created_objective.status_code == 201, created_objective.text
        objective_ref = created_objective.json()["objective_ref"]
        definition_url = f"/api/v1/temporal/objectives/{objective_ref}/definition"
        result_url = f"/api/v1/temporal/objectives/{objective_ref}/result"
        correction_url = f"/api/v1/temporal/objectives/{objective_ref}/correction"

        baseline = client.get(definition_url, headers=_base_headers())
        assert baseline.status_code == 200
        assert baseline.json()["objective_ref"] == objective_ref
        assert baseline.json()["definition_revision"] == 0
        assert baseline.json()["evaluation_state_ref"] is None

        measured = client.post(
            result_url,
            json={"operation_id": "m2:measured", "observed_numeric": 8},
            headers=headers,
        )
        assert measured.status_code == 201, measured.text
        first = measured.json()
        assert first["assessment_code"] == "not_satisfied"

        revised = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0),
            headers=headers,
        )
        assert revised.status_code == 200, revised.text
        changed = revised.json()
        assert changed["objective_ref"] == objective_ref
        assert changed["definition_revision"] == 1
        assert changed["assessment_code"] == "satisfied"
        assert changed["evaluation_state_ref"] != first["evaluation_state_ref"]
        assert revised.json()["replayed"] is False

        current = client.get(definition_url, headers=_base_headers()).json()
        assert current["definition_revision"] == 1
        assert current["label"] == "Percorrere almeno sette km"
        listed = client.get(
            f"/api/v1/temporal/activities/{activity_ref}/objectives",
            headers=_base_headers(),
        )
        assert listed.status_code == 200, listed.text
        assert len(listed.json()) == 1
        assert listed.json()[0]["objective_ref"] == objective_ref
        assert listed.json()[0]["assessment_code"] == "satisfied"

        replay = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0),
            headers=headers,
        )
        assert replay.status_code == 200, replay.text
        assert replay.json()["replayed"] is True
        assert replay.json()["definition_revision"] == 1
        stale = client.put(
            definition_url,
            json=_definition(operation="m2:stale", expected=0, target=9),
            headers=headers,
        )
        assert stale.status_code == 409
        reuse = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0, target=9),
            headers=headers,
        )
        assert reuse.status_code == 409

        corrected = client.post(
            correction_url,
            json={
                "operation_id": "m2:correct-result",
                "expected_evaluation_state_ref": changed["evaluation_state_ref"],
                "observed_numeric": 6,
            },
            headers=headers,
        )
        assert corrected.status_code == 200, corrected.text
        last = corrected.json()
        assert last["objective_ref"] == objective_ref
        assert last["observation_ref"] != first["observation_ref"]
        assert last["assessment_code"] == "not_satisfied"
        replayed = client.post(
            correction_url,
            json={
                "operation_id": "m2:correct-result",
                "expected_evaluation_state_ref": changed["evaluation_state_ref"],
                "observed_numeric": 6,
            },
            headers=headers,
        )
        assert replayed.status_code == 200
        assert replayed.json()["replayed"] is True
        assert replayed.json()["observation_ref"] == last["observation_ref"]

        obsolete_cas = client.post(
            correction_url,
            json={
                "operation_id": "m2:obsolete-result",
                "expected_evaluation_state_ref": changed["evaluation_state_ref"],
                "observed_numeric": 9,
            },
            headers=headers,
        )
        assert obsolete_cas.status_code == 409
        latest = client.get(
            f"/api/v1/temporal/activities/{activity_ref}/objectives",
            headers=_base_headers(),
        ).json()
        assert latest[0]["assessment_code"] == "not_satisfied"
        assert latest[0]["observed_numeric"] == 6

        # Internal audit is append-only; neither the original observation,
        # original evaluation nor the objective identity was replaced.
        async def count_audit() -> tuple[int, int, int]:
            runtime = create_database_runtime(migrated_database.runtime_settings())
            try:
                async with runtime.session_factory() as session, session.begin():
                    values = (
                        await session.execute(
                            text("""
                                SELECT
                                    (SELECT count(*) FROM dante.temporal_objective_definition_revision
                                      WHERE objective_ref=:objective),
                                    (SELECT count(*) FROM dante.temporal_objective_observation
                                      WHERE objective_ref=:objective),
                                    (SELECT count(*) FROM dante.temporal_objective_evaluation_state
                                      WHERE objective_ref=:objective)
                            """),
                            {"objective": objective_ref},
                        )
                    ).one()
                    return (int(values[0]), int(values[1]), int(values[2])
            finally:
                await runtime.dispose()

        assert asyncio.run(count_audit()) == (1, 2, 3)

        bob_csrf = _signin(client, bob)
        bob_headers = {**_base_headers(), CSRF_HEADER_NAME: bob_csrf}
        assert client.get(definition_url, headers=_base_headers()).status_code == 404
        denied = client.put(
            definition_url,
            json=_definition(operation="m2:cross-owner", expected=1),
            headers=bob_headers,
        )
        assert denied.status_code == 404
        refused = client.post(
            correction_url,
            json={"operation_id": "m2:cross-owner-correction",
                  "expected_evaluation_state_ref": last["evaluation_state_ref"],
                  "observed_numeric": 3},
            headers=bob_headers,
        )
        assert refused.status_code == 404


def test_event_objective_same_identity_definition_revision(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "b14.m2.event@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        event = _post_scheduled_event(
            client, csrf=csrf, operation_id="m2:event",
            title="Gara", placement={
                "kind": "date_span",
                "start_date": "2026-10-08",
                "end_date_exclusive": "2026-10-09",
            },
        )
        assert event.status_code == 201, event.text
        subject_ref = event.json()["event_ref"]
        response = client.post(
            f"/api/v1/temporal/events/{subject_ref}/objectives",
            json={"operation_id": "m2:event:objective",
                  "label": "Arrivare puntuali", "result_kind": "boolean",
                  "presentation_order": 0},
            headers=headers,
        )
        assert response.status_code == 201, response.text
        objective = response.json()["objective_ref"]
        revision = client.put(
            f"/api/v1/temporal/objectives/{objective}/definition",
            json={"operation_id": "m2:event:revision", "expected_revision": 0,
                  "label": "Partenza puntuale", "result_kind": "boolean",
                  "presentation_order": 0},
            headers=headers,
        )
        assert revision.status_code == 200, revision.text
        result = client.get(
            f"/api/v1/temporal/events/{subject_ref}/objectives",
            headers=_base_headers(),
        )
        assert result.status_code == 200
        assert result.json()[0]["objective_ref"] == objective
        assert result.json()[0]["label"] == "Partenza puntuale"
