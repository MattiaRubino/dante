from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def _response_schema_ref(response: dict[str, Any]) -> str:
    content = cast(dict[str, Any], response["content"])
    application_json = cast(dict[str, Any], content["application/json"])
    schema = cast(dict[str, Any], application_json["schema"])
    return cast(str, schema["$ref"])


def test_b10_c_confirmation_write_openapi_matches_runtime_http_contract() -> None:
    """Creation, replay and expected failure statuses must remain public contract truth."""
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    path = cast(
        dict[str, Any],
        paths["/api/v1/temporal/outcomes/{outcome_ref}/confirmations"],
    )
    operation = cast(dict[str, Any], path["post"])
    responses = cast(dict[str, Any], operation["responses"])

    assert set(responses) == {
        "200",
        "201",
        "400",
        "401",
        "403",
        "404",
        "409",
        "422",
        "500",
    }
    assert _response_schema_ref(cast(dict[str, Any], responses["200"])) == (
        "#/components/schemas/ConfirmationResponse"
    )
    assert _response_schema_ref(cast(dict[str, Any], responses["201"])) == (
        "#/components/schemas/ConfirmationResponse"
    )
    for status in ("400", "401", "403", "404", "409", "422", "500"):
        assert _response_schema_ref(cast(dict[str, Any], responses[status])) == (
            "#/components/schemas/ProblemDetails"
        )
