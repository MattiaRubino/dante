"""B12-A diagnosis remains an authenticated read-only public contract."""

from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def test_b12_a_conflict_diagnosis_contract() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    endpoint = cast(dict[str, Any], paths["/api/v1/temporal/plans/{plan_ref}/conflicts"])
    assert set(endpoint) == {"get"}
    get = cast(dict[str, Any], endpoint["get"])
    assert get["operationId"] == "temporal_diagnose_self_plan_conflicts"
    assert set(get["responses"]) == {"200", "401", "403", "404", "409", "422", "500"}
    assert {item["name"] for item in get["parameters"]} == {
        "plan_ref", "expected_state_ref",
    }
    schemas = cast(dict[str, Any], cast(dict[str, Any], document["components"])["schemas"])
    result = cast(dict[str, Any], schemas["PlanDiagnosisResponse"])
    assert {"plan_state_ref", "capacity_evaluated", "steps"} <= set(result["properties"])
    step = cast(dict[str, Any], schemas["StepDiagnosisResponse"])
    assert {"placements", "constraints", "constraint_status", "hard_set_status",
            "dependencies", "diagnostics"} <= set(step["properties"])
