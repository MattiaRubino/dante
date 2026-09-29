"""B12-C reviewed candidate admission exposes two explicit authenticated writes."""

from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def test_b12_c_reviewed_move_contract() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    base = "/api/v1/temporal/plans/{plan_ref}/steps/{step_ref}/candidate-moves"
    for path, operation_id in (
        (base, "temporal_request_reviewed_plan_candidate_move"),
        (base + "/{proposal_ref}/confirm", "temporal_confirm_reviewed_plan_candidate_move"),
    ):
        assert set(paths[path]) == {"post"}
        operation = cast(dict[str, Any], paths[path]["post"])
        assert operation["operationId"] == operation_id
        assert {"200", "401", "403", "404", "409", "422", "500"} == set(
            operation["responses"]
        )
        body = operation["requestBody"]["content"]["application/json"]["schema"]
        assert body["$ref"] == "#/components/schemas/ReviewedMoveBody"
        result = operation["responses"]["200"]["content"]["application/json"]["schema"]
        assert result["$ref"] == "#/components/schemas/PlanAdmissionResponse"
    schemas = document["components"]["schemas"]
    required = set(schemas["ReviewedMoveBody"]["required"])
    assert {"operation_id", "expected_plan_state_ref", "expected_schedule_state_ref",
            "expected_policy_state_ref", "basis_fingerprint", "starts_at", "ends_at"} <= required
