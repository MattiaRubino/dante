"""M2: same logical Objective, immutable definitions, corrected reality, owner/CAS."""

from __future__ import annotations

from decimal import Decimal
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
from tests.integration.temporal.test_b03_shared_schedule_event import _post_scheduled_event

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

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
        # Only the internal materializer can mint generated template lineage.
        forged = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/objectives",
            json={
                "operation_id": f"b14:objective:activity:{activity_ref}:0",
                "label": "Origine falsa",
                "result_kind": "boolean",
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert forged.status_code == 422
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
        # A definition replay must retain its original accepted evaluation,
        # not silently return this later corrected Observation's assessment.
        definition_replay = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0),
            headers=headers,
        )
        assert definition_replay.status_code == 200
        assert definition_replay.json()["replayed"] is True
        assert definition_replay.json()["evaluation_state_ref"] == changed["evaluation_state_ref"]
        assert definition_replay.json()["assessment_code"] == "satisfied"
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
        assert Decimal(str(latest[0]["observed_numeric"])) == Decimal("6")

        # Internal audit is append-only; neither the original observation,
        # original evaluation nor the objective identity was replaced.
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                migrated_database.cluster.admin_user,
                migrated_database.cluster.admin_password,
            )
        ) as conn, conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    (SELECT count(*) FROM dante.temporal_objective_definition_revision
                     WHERE objective_ref=%s),
                    (SELECT count(*) FROM dante.temporal_objective_observation
                     WHERE objective_ref=%s),
                    (SELECT count(*) FROM dante.temporal_objective_evaluation_state
                     WHERE objective_ref=%s)
                """,
                (UUID(objective_ref),) * 3,
            )
            counts = cursor.fetchone()
        assert counts == (1, 2, 3)
        # Test-admin audit is deliberately separate from application runtime:
        # dante_runtime must NOT receive table SELECT permissions.

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



def test_qualitative_objective_never_synthesizes_manual_assessment(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "b14.m2.qualitative@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        created = client.post(
            "/api/v1/temporal/authoring/activities",
            json={"operation_id": "m2:qual:activity", "title": "Esercizio",
                  "session_capture_mode": "record"},
            headers=headers,
        )
        assert created.status_code == 201, created.text
        subject = created.json()["activity_ref"]
        created_objective = client.post(
            f"/api/v1/temporal/activities/{subject}/objectives",
            json={"operation_id": "m2:qual:objective", "label": "Qualità",
                  "result_kind": "qualitative", "presentation_order": 0},
            headers=headers,
        )
        assert created_objective.status_code == 201, created_objective.text
        objective = created_objective.json()["objective_ref"]
        result = client.post(
            f"/api/v1/temporal/objectives/{objective}/result",
            json={"operation_id": "m2:qual:result",
                  "qualitative_code": "buono", "assessment_code": "partial"},
            headers=headers,
        )
        assert result.status_code == 201, result.text
        state_ref = result.json()["evaluation_state_ref"]
        renamed = client.put(
            f"/api/v1/temporal/objectives/{objective}/definition",
            json={"operation_id": "m2:qual:rename",
                  "expected_revision": 0,
                  "label": "Qualità corretta",
                  "result_kind": "qualitative",
                  "presentation_order": 0},
            headers=headers,
        )
        assert renamed.status_code == 200, renamed.text
        assert renamed.json()["assessment_code"] == "partial"
        assert renamed.json()["evaluation_state_ref"] == state_ref
        impossible = client.put(
            f"/api/v1/temporal/objectives/{objective}/definition",
            json={"operation_id": "m2:qual:kind-switch",
                  "expected_revision": 1,
                  "label": "Quantità", "result_kind": "quantity",
                  "comparator_code": "gte", "target_value": 2,
                  "presentation_order": 0},
            headers=headers,
        )
        assert impossible.status_code == 409, impossible.text
        latest = client.get(
            f"/api/v1/temporal/activities/{subject}/objectives",
            headers=_base_headers(),
        ).json()
        assert latest[0]["objective_ref"] == objective
        assert latest[0]["label"] == "Qualità corretta"
        assert latest[0]["assessment_code"] == "partial"
