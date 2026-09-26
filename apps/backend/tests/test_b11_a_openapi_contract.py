from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def _schema_ref(response: dict[str, Any], media_type: str) -> str:
    content = cast(dict[str, Any], response["content"])
    media = cast(dict[str, Any], content[media_type])
    schema = cast(dict[str, Any], media["schema"])
    return cast(str, schema["$ref"])


def test_b11_a_advanced_recurrence_operations_are_public_and_semantic() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    expected = {
        ("/api/v1/temporal/routines/{source_ref}/advanced-recurrence", "get"):
            "temporal_get_routine_advanced_recurrence",
        ("/api/v1/temporal/routines/{source_ref}/advanced-recurrence", "put"):
            "temporal_replace_routine_advanced_recurrence",
        ("/api/v1/temporal/routines/{source_ref}/advanced-recurrence/checkpoint", "post"):
            "temporal_checkpoint_routine_advanced_recurrence",
        ("/api/v1/temporal/events/{source_ref}/advanced-recurrence", "get"):
            "temporal_get_event_advanced_recurrence",
        ("/api/v1/temporal/events/{source_ref}/advanced-recurrence", "put"):
            "temporal_replace_event_advanced_recurrence",
        ("/api/v1/temporal/events/{source_ref}/advanced-recurrence/checkpoint", "post"):
            "temporal_checkpoint_event_advanced_recurrence",
    }
    for (path, method), operation_id in expected.items():
        operation = cast(dict[str, Any], cast(dict[str, Any], paths[path])[method])
        assert operation["operationId"] == operation_id


def test_b11_a_write_contract_freezes_creation_replay_and_problem_details() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    cases = (
        (
            "/api/v1/temporal/routines/{source_ref}/advanced-recurrence",
            "put",
            "#/components/schemas/AdvancedRecurrenceResponse",
        ),
        (
            "/api/v1/temporal/events/{source_ref}/advanced-recurrence",
            "put",
            "#/components/schemas/AdvancedRecurrenceResponse",
        ),
        (
            "/api/v1/temporal/routines/{source_ref}/advanced-recurrence/checkpoint",
            "post",
            "#/components/schemas/AdvancedCheckpointResponse",
        ),
        (
            "/api/v1/temporal/events/{source_ref}/advanced-recurrence/checkpoint",
            "post",
            "#/components/schemas/AdvancedCheckpointResponse",
        ),
    )
    for path, method, success_schema in cases:
        operation = cast(dict[str, Any], cast(dict[str, Any], paths[path])[method])
        responses = cast(dict[str, Any], operation["responses"])
        assert set(responses) == {
            "200", "201", "400", "401", "403", "404", "409", "422", "500"
        }
        assert _schema_ref(cast(dict[str, Any], responses["200"]), "application/json") == success_schema
        assert _schema_ref(cast(dict[str, Any], responses["201"]), "application/json") == success_schema
        for status in ("400", "401", "403", "404", "409", "422", "500"):
            assert _schema_ref(
                cast(dict[str, Any], responses[status]), "application/problem+json"
            ) == "#/components/schemas/ProblemDetails"


def test_b11_a_public_schema_keeps_anchor_semantics_typed() -> None:
    document = openapi_document()
    schemas = cast(dict[str, Any], cast(dict[str, Any], document["components"])["schemas"])
    request = cast(dict[str, Any], schemas["AdvancedElapsedRecurrenceRequest"])
    properties = cast(dict[str, Any], request["properties"])

    anchor_mode = cast(dict[str, Any], properties["anchor_mode_code"])
    assert set(cast(list[str], anchor_mode["enum"])) == {
        "previous_completion",
        "anchor_stream",
    }
    assert "anchor_source_family" in properties
    assert "anchor_source_native_ref" in properties
    assert "trigger" not in properties
    assert "condition" not in properties
