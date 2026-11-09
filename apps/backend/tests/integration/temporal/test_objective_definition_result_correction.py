"""M2: same logical Objective, immutable definitions, corrected reality, owner/CAS."""

from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

import psycopg
import pytest
from fastapi.testclient import TestClient
from tests.integration.temporal.test_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)
from tests.integration.temporal.test_shared_schedule_event import _post_scheduled_event

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_activity_core",)


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


def test_recorded_objective_is_immutable_until_its_entire_result_is_deleted(
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
            json={
                "operation_id": "m2:activity",
                "title": "Corsa",
                "session_capture_mode": "record",
            },
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
        removal_url = f"/api/v1/temporal/objectives/{objective_ref}/delete-recording"
        list_url = f"/api/v1/temporal/activities/{activity_ref}/objectives"

        original = client.get(definition_url, headers=_base_headers())
        assert original.status_code == 200
        assert original.json()["definition_revision"] == 0
        # Definition changes are still legal BEFORE a result exists.
        revised = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0),
            headers=headers,
        )
        assert revised.status_code == 200, revised.text
        assert revised.json()["definition_revision"] == 1
        assert revised.json()["evaluation_state_ref"] is None
        replay_before_fact = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0),
            headers=headers,
        )
        assert replay_before_fact.status_code == 200
        assert replay_before_fact.json()["replayed"] is True

        measured = client.post(
            result_url,
            json={"operation_id": "m2:measured", "observed_numeric": 8},
            headers=headers,
        )
        assert measured.status_code == 201, measured.text
        first = measured.json()
        assert first["assessment_code"] == "satisfied"

        # An accepted result makes even a harmless rename illegal until
        # explicit and complete removal of the recorded fact.
        locked = client.put(
            definition_url,
            json=_definition(operation="m2:locked", expected=1, target=9),
            headers=headers,
        )
        assert locked.status_code == 409, locked.text
        locked_replay = client.put(
            definition_url,
            json=_definition(operation="m2:definition", expected=0),
            headers=headers,
        )
        assert locked_replay.status_code == 409

        corrected = client.post(
            correction_url,
            json={
                "operation_id": "m2:correct-result",
                "expected_evaluation_state_ref": first["evaluation_state_ref"],
                "observed_numeric": 6,
            },
            headers=headers,
        )
        assert corrected.status_code == 200, corrected.text
        last = corrected.json()
        assert last["observation_ref"] != first["observation_ref"]
        assert last["assessment_code"] == "not_satisfied"
        replayed = client.post(
            correction_url,
            json={
                "operation_id": "m2:correct-result",
                "expected_evaluation_state_ref": first["evaluation_state_ref"],
                "observed_numeric": 6,
            },
            headers=headers,
        )
        assert replayed.status_code == 200
        assert replayed.json()["replayed"] is True
        obsolete_cas = client.post(
            correction_url,
            json={
                "operation_id": "m2:obsolete",
                "expected_evaluation_state_ref": first["evaluation_state_ref"],
                "observed_numeric": 12,
            },
            headers=headers,
        )
        assert obsolete_cas.status_code == 409
        stale_removal = client.post(
            removal_url,
            json={"expected_evaluation_state_ref": first["evaluation_state_ref"]},
            headers=headers,
        )
        assert stale_removal.status_code == 409
        latest = client.get(list_url, headers=_base_headers())
        assert latest.status_code == 200
        assert latest.json()[0]["observation_ref"] == last["observation_ref"]

        bob_csrf = _signin(client, bob)
        bob_headers = {**_base_headers(), CSRF_HEADER_NAME: bob_csrf}
        assert client.get(definition_url, headers=_base_headers()).status_code == 404
        denied = client.post(
            removal_url,
            json={"expected_evaluation_state_ref": last["evaluation_state_ref"]},
            headers=bob_headers,
        )
        assert denied.status_code == 404
        csrf = _signin(client, alice)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}

        deleted = client.post(
            removal_url,
            json={"expected_evaluation_state_ref": last["evaluation_state_ref"]},
            headers=headers,
        )
        assert deleted.status_code == 200, deleted.text
        assert deleted.json() == {
            "objective_ref": objective_ref,
            "removed_observations": 2,
        }
        assert client.post(
            removal_url,
            json={"expected_evaluation_state_ref": last["evaluation_state_ref"]},
            headers=headers,
        ).status_code == 409

        remaining = client.get(list_url, headers=_base_headers()).json()
        assert len(remaining) == 1
        assert remaining[0]["objective_ref"] == objective_ref
        assert remaining[0]["observation_ref"] is None
        assert remaining[0]["evaluation_state_ref"] is None
        assert remaining[0]["label"] == "Percorrere almeno sette km"

        with (
            psycopg.connect(
                **migrated_database.connection_kwargs(
                    migrated_database.cluster.admin_user,
                    migrated_database.cluster.admin_password,
                )
            ) as conn,
            conn.cursor() as cursor,
        ):
            cursor.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.temporal_objective_definition_revision
                    WHERE objective_ref=%s),
                  (SELECT count(*) FROM dante.temporal_objective_observation
                    WHERE objective_ref=%s),
                  (SELECT count(*) FROM dante.temporal_objective_evaluation_state
                    WHERE objective_ref=%s),
                  (SELECT count(*) FROM dante.temporal_objective_evaluation_current_history
                    WHERE objective_ref=%s),
                  (SELECT count(*) FROM dante.temporal_objective_result_operation
                    WHERE objective_ref=%s),
                  (SELECT count(*) FROM dante.temporal_objective_input_draft
                    WHERE objective_ref=%s),
                  (SELECT count(*) FROM dante.observation
                    WHERE observation_ref IN (%s,%s))
                """,
                (UUID(objective_ref),) * 6
                + (UUID(first["observation_ref"]), UUID(last["observation_ref"])),
            )
            counts = cursor.fetchone()
        assert counts == (1, 0, 0, 0, 0, 0, 0)

        # The original logical definition is preserved and unlocked.
        unlocked = client.put(
            definition_url,
            json=_definition(operation="m2:unlocked", expected=1, target=9),
            headers=headers,
        )
        assert unlocked.status_code == 200, unlocked.text
        assert unlocked.json()["definition_revision"] == 2



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
            client,
            csrf=csrf,
            operation_id="m2:event",
            title="Gara",
            placement={
                "kind": "date_span",
                "start_date": "2026-10-08",
                "end_date_exclusive": "2026-10-09",
            },
        )
        assert event.status_code == 201, event.text
        subject_ref = event.json()["event_ref"]
        response = client.post(
            f"/api/v1/temporal/events/{subject_ref}/objectives",
            json={
                "operation_id": "m2:event:objective",
                "label": "Arrivare puntuali",
                "result_kind": "boolean",
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert response.status_code == 201, response.text
        objective = response.json()["objective_ref"]
        revision = client.put(
            f"/api/v1/temporal/objectives/{objective}/definition",
            json={
                "operation_id": "m2:event:revision",
                "expected_revision": 0,
                "label": "Partenza puntuale",
                "result_kind": "boolean",
                "presentation_order": 0,
            },
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
            json={
                "operation_id": "m2:qual:activity",
                "title": "Esercizio",
                "session_capture_mode": "record",
            },
            headers=headers,
        )
        assert created.status_code == 201, created.text
        subject = created.json()["activity_ref"]
        created_objective = client.post(
            f"/api/v1/temporal/activities/{subject}/objectives",
            json={
                "operation_id": "m2:qual:objective",
                "label": "Qualità",
                "result_kind": "qualitative",
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert created_objective.status_code == 201, created_objective.text
        objective = created_objective.json()["objective_ref"]
        result = client.post(
            f"/api/v1/temporal/objectives/{objective}/result",
            json={
                "operation_id": "m2:qual:result",
                "qualitative_code": "buono",
                "assessment_code": "partial",
            },
            headers=headers,
        )
        assert result.status_code == 201, result.text
        state_ref = result.json()["evaluation_state_ref"]
        renamed = client.put(
            f"/api/v1/temporal/objectives/{objective}/definition",
            json={
                "operation_id": "m2:qual:rename",
                "expected_revision": 0,
                "label": "Qualità corretta",
                "result_kind": "qualitative",
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert renamed.status_code == 409, renamed.text
        assert state_ref == result.json()["evaluation_state_ref"]
        impossible = client.put(
            f"/api/v1/temporal/objectives/{objective}/definition",
            json={
                "operation_id": "m2:qual:kind-switch",
                "expected_revision": 0,
                "label": "Quantità",
                "result_kind": "quantity",
                "comparator_code": "gte",
                "target_value": 2,
                "presentation_order": 0,
            },
            headers=headers,
        )
        assert impossible.status_code == 409, impossible.text
        latest = client.get(
            f"/api/v1/temporal/activities/{subject}/objectives",
            headers=_base_headers(),
        ).json()
        assert latest[0]["objective_ref"] == objective
        assert latest[0]["label"] == "Qualità"
        assert latest[0]["assessment_code"] == "partial"
