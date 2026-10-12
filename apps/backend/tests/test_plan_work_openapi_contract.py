"""B13-A public contract exposes Plan and internal Steps without Dependency."""

from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def test_b13_a_plan_structure_contract_is_bounded() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    collection = cast(dict[str, Any], paths["/api/v1/temporal/plans"])
    item = cast(dict[str, Any], paths["/api/v1/temporal/plans/{plan_ref}"])
    assert collection["post"]["operationId"] == "temporal_create_self_plan"
    assert collection["get"]["operationId"] == "temporal_list_self_plans"
    assert item["get"]["operationId"] == "temporal_get_self_plan"
    assert item["put"]["operationId"] == "temporal_replace_self_plan_work"
    assert set(collection["post"]["responses"]) == {
        "200",
        "201",
        "400",
        "401",
        "403",
        "409",
        "422",
        "500",
    }
    assert set(item["put"]["responses"]) == {"200", "400", "401", "403", "404", "409", "422", "500"}
    schemas = cast(dict[str, Any], cast(dict[str, Any], document["components"])["schemas"])
    replace = cast(dict[str, Any], schemas["ReplacePlanBody"])
    assert set(replace["properties"]) == {"operation_id", "title", "expected_state_ref", "steps"}
    step = cast(dict[str, Any], schemas["PlanStepBody"])
    assert set(step["properties"]) == {
        "step_ref",
        "title",
        "activity_ref",
        "divisible",
        "max_planned_slices",
        "merge_compatible",
        "execution_strength_code",
    }
    assert "dependency" not in str(step).lower()
    assessment = cast(
        dict[str, Any],
        paths["/api/v1/temporal/plans/{plan_ref}/steps/{step_ref}/execution/assess"],
    )
    assert assessment["post"]["operationId"] == "temporal_assess_plan_step_execution"
    request = cast(dict[str, Any], schemas["AssessExecutionBody"])
    assert set(request["properties"]) == {"expected_state_ref", "slices", "merge_pair"}
    result = cast(dict[str, Any], schemas["ExecutionAssessmentResponse"])
    assert {"basis", "proposed_count", "count_status", "merge_status"} <= set(result["properties"])
