from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def _schema_ref(response: dict[str, Any], media_type: str) -> str:
    content = cast(dict[str, Any], response["content"])
    media = cast(dict[str, Any], content[media_type])
    schema = cast(dict[str, Any], media["schema"])
    return cast(str, schema["$ref"])


def test_b11_b_conditional_operations_are_public_and_bounded() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    expected = {
        ("/api/v1/temporal/conditions/actual-realization", "post"):
            "temporal_create_actual_realization_condition",
        ("/api/v1/temporal/conditions/actual-realization/{condition_ref}", "get"):
            "temporal_get_actual_realization_condition",
        ("/api/v1/temporal/conditions/actual-realization/{condition_ref}/evaluations", "post"):
            "temporal_evaluate_actual_realization_condition",
    }
    for (path, method), operation_id in expected.items():
        operation = cast(dict[str, Any], cast(dict[str, Any], paths[path])[method])
        assert operation["operationId"] == operation_id


def test_b11_b_write_contract_freezes_creation_replay_and_problem_details() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    cases = (
        (
            "/api/v1/temporal/conditions/actual-realization",
            "post",
            "#/components/schemas/ActualRealizationConditionResponse",
        ),
        (
            "/api/v1/temporal/conditions/actual-realization/{condition_ref}/evaluations",
            "post",
            "#/components/schemas/ConditionalEvaluationResponse",
        ),
    )
    for path, method, success_schema in cases:
        operation = cast(dict[str, Any], cast(dict[str, Any], paths[path])[method])
        responses = cast(dict[str, Any], operation["responses"])
        assert set(responses) == {
            "200", "201", "400", "401", "403", "404", "409", "422", "500"
        }
        assert _schema_ref(
            cast(dict[str, Any], responses["200"]), "application/json"
        ) == success_schema
        assert _schema_ref(
            cast(dict[str, Any], responses["201"]), "application/json"
        ) == success_schema
        for status in ("400", "401", "403", "404", "409", "422", "500"):
            assert _schema_ref(
                cast(dict[str, Any], responses[status]), "application/problem+json"
            ) == "#/components/schemas/ProblemDetails"


def test_b11_b_public_schema_never_accepts_caller_supplied_condition_truth() -> None:
    document = openapi_document()
    schemas = cast(
        dict[str, Any], cast(dict[str, Any], document["components"])["schemas"]
    )

    condition_request = cast(dict[str, Any], schemas["ActualRealizationConditionRequest"])
    condition_properties = cast(dict[str, Any], condition_request["properties"])
    assert set(condition_properties) == {
        "operation_id",
        "subject_kind",
        "subject_native_ref",
    }
    subject_kind = cast(dict[str, Any], condition_properties["subject_kind"])
    assert set(cast(list[str], subject_kind["enum"])) == {
        "activity",
        "event",
        "occurrence",
    }
    assert "result_code" not in condition_properties
    assert "disposition_code" not in condition_properties
    assert "condition_met" not in condition_properties
    assert "allow" not in condition_properties

    evaluation_request = cast(dict[str, Any], schemas["ConditionalEvaluationRequest"])
    evaluation_properties = cast(dict[str, Any], evaluation_request["properties"])
    assert set(evaluation_properties) == {"operation_id"}

    evaluation_response = cast(dict[str, Any], schemas["ConditionalEvaluationResponse"])
    response_properties = cast(dict[str, Any], evaluation_response["properties"])
    assert "result_code" in response_properties
    assert "disposition_code" in response_properties
    assert "actual_ref" in response_properties
    assert "actual_realization_material_state_ref" in response_properties
