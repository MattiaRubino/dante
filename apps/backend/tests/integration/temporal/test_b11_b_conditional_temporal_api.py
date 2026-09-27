"""B11-B public API proof for bounded Actual-realization conditions."""

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
from tests.integration.temporal.test_b10_c_confirmation_api import _actual_command

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _condition_command(
    operation_id: str,
    *,
    subject_kind: str,
    subject_native_ref: str,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "subject_kind": subject_kind,
        "subject_native_ref": subject_native_ref,
    }


def test_b11_b_conditional_api_derives_truth_and_pins_actual_state(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "b11b.api@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        area = api_test_life_area(client, headers)
        event = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "b11b-api:event",
                "title": "Conditional source",
                "life_area_ref": area,
            },
            headers=headers,
        )
        assert event.status_code == 201
        event_ref = event.json()["event_ref"]

        condition_path = "/api/v1/temporal/conditions/actual-realization"
        condition_payload = _condition_command(
            "b11b-api:condition",
            subject_kind="event",
            subject_native_ref=event_ref,
        )

        missing_csrf = client.post(
            condition_path,
            json=condition_payload,
            headers=_base_headers(),
        )
        assert missing_csrf.status_code == 403
        assert missing_csrf.headers["content-type"].startswith("application/problem+json")
        assert missing_csrf.json()["code"] == "security.csrf_failed"

        created = client.post(condition_path, json=condition_payload, headers=headers)
        assert created.status_code == 201
        first_condition = created.json()
        condition_ref = first_condition["condition_ref"]
        assert first_condition["subject_kind"] == "event"
        assert first_condition["subject_native_ref"] == event_ref
        assert first_condition["family_code"] == "actual_realization"
        assert first_condition["replayed"] is False
        assert "result_code" not in first_condition
        assert "disposition_code" not in first_condition

        replay = client.post(condition_path, json=condition_payload, headers=headers)
        assert replay.status_code == 200
        assert replay.json()["condition_ref"] == condition_ref
        assert replay.json()["replayed"] is True

        fetched = client.get(
            f"{condition_path}/{condition_ref}",
            headers=_base_headers(),
        )
        assert fetched.status_code == 200
        assert fetched.json()["condition_ref"] == condition_ref
        assert fetched.json()["replayed"] is False

        evaluation_path = f"{condition_path}/{condition_ref}/evaluations"
        unknown = client.post(
            evaluation_path,
            json={"operation_id": "b11b-api:evaluate:unknown"},
            headers=headers,
        )
        assert unknown.status_code == 201
        unknown_body = unknown.json()
        assert unknown_body["result_code"] == "indeterminate"
        assert unknown_body["disposition_code"] == "withhold"
        assert unknown_body["actual_ref"] is None
        assert unknown_body["actual_realization_material_state_ref"] is None
        assert unknown_body["replayed"] is False

        # A caller cannot inject condition truth. Extra fields are rejected before
        # the runtime reaches PostgreSQL because the evaluation request is operation-id only.
        injected = client.post(
            evaluation_path,
            json={
                "operation_id": "b11b-api:evaluate:injected",
                "result_code": "satisfied",
                "disposition_code": "allow",
            },
            headers=headers,
        )
        assert injected.status_code == 422
        assert injected.headers["content-type"].startswith("application/problem+json")
        assert injected.json()["code"] == "request.validation_failed"

        actual = client.post(
            f"/api/v1/temporal/events/{event_ref}/actual",
            json=_actual_command("b11b-api:actual:true"),
            headers=headers,
        )
        assert actual.status_code == 201
        actual_body = actual.json()

        satisfied = client.post(
            evaluation_path,
            json={"operation_id": "b11b-api:evaluate:satisfied"},
            headers=headers,
        )
        assert satisfied.status_code == 201
        satisfied_body = satisfied.json()
        assert satisfied_body["result_code"] == "satisfied"
        assert satisfied_body["disposition_code"] == "allow"
        assert satisfied_body["actual_ref"] == actual_body["actual_ref"]
        assert (
            satisfied_body["actual_realization_material_state_ref"]
            == actual_body["material_state_ref"]
        )
        assert satisfied_body["replayed"] is False

        satisfied_replay = client.post(
            evaluation_path,
            json={"operation_id": "b11b-api:evaluate:satisfied"},
            headers=headers,
        )
        assert satisfied_replay.status_code == 200
        assert satisfied_replay.json()["evaluation_ref"] == satisfied_body["evaluation_ref"]
        assert satisfied_replay.json()["replayed"] is True

        corrected = client.post(
            f"/api/v1/temporal/events/{event_ref}/actual",
            json=_actual_command(
                "b11b-api:actual:false",
                expected=actual_body["material_state_ref"],
                occurred=False,
            ),
            headers=headers,
        )
        assert corrected.status_code == 201
        corrected_body = corrected.json()
        assert corrected_body["material_state_ref"] != actual_body["material_state_ref"]

        not_satisfied = client.post(
            evaluation_path,
            json={"operation_id": "b11b-api:evaluate:not-satisfied"},
            headers=headers,
        )
        assert not_satisfied.status_code == 201
        not_satisfied_body = not_satisfied.json()
        assert not_satisfied_body["result_code"] == "not_satisfied"
        assert not_satisfied_body["disposition_code"] == "withhold"
        assert not_satisfied_body["actual_ref"] == actual_body["actual_ref"]
        assert (
            not_satisfied_body["actual_realization_material_state_ref"]
            == corrected_body["material_state_ref"]
        )
        assert (
            satisfied_body["actual_realization_material_state_ref"]
            == actual_body["material_state_ref"]
        )

        operation_reuse = client.post(
            condition_path,
            json=_condition_command(
                "b11b-api:evaluate:satisfied",
                subject_kind="event",
                subject_native_ref=event_ref,
            ),
            headers=headers,
        )
        assert operation_reuse.status_code == 409
        assert operation_reuse.headers["content-type"].startswith("application/problem+json")
        assert operation_reuse.json()["code"] == "temporal.conditional.operation_id_reused"

        openapi = client.get("/openapi.json").json()
        create_operation = openapi["paths"][condition_path]["post"]
        evaluation_operation = openapi["paths"][
            "/api/v1/temporal/conditions/actual-realization/{condition_ref}/evaluations"
        ]["post"]
        assert create_operation["operationId"] == "temporal_create_actual_realization_condition"
        assert evaluation_operation["operationId"] == "temporal_evaluate_actual_realization_condition"
        assert "200" in create_operation["responses"]
        assert "201" in create_operation["responses"]
        assert "200" in evaluation_operation["responses"]
        assert "201" in evaluation_operation["responses"]

        components = openapi["components"]["schemas"]
        condition_input = components["ActualRealizationConditionRequest"]["properties"]
        evaluation_input = components["ConditionalEvaluationRequest"]["properties"]
        assert set(condition_input) == {
            "operation_id",
            "subject_kind",
            "subject_native_ref",
        }
        assert set(evaluation_input) == {"operation_id"}
        assert "result_code" not in condition_input
        assert "disposition_code" not in condition_input
        assert "result_code" not in evaluation_input
        assert "disposition_code" not in evaluation_input
