"""B12-B candidate search is a self-scoped, read-only typed endpoint."""

from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def test_b12_b_candidate_contract() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    endpoint = cast(dict[str, Any], paths["/api/v1/temporal/plans/{plan_ref}/steps/{step_ref}/candidates"])
    assert set(endpoint) == {"get"}
    get = cast(dict[str, Any], endpoint["get"])
    assert get["operationId"] == "temporal_search_self_plan_step_candidates"
    assert {item["name"] for item in get["parameters"]} == {
        "plan_ref", "step_ref", "expected_state_ref",
    }
    schemas = cast(dict[str, Any], cast(dict[str, Any], document["components"])["schemas"])
    result = cast(dict[str, Any], schemas["PlanCandidateResponse"])
    assert {"placement", "dependencies", "constraint_states", "candidates",
            "solver_status", "basis_status", "capacity_evaluated",
            "movement_policy_material_state_ref"} <= set(result["properties"])
