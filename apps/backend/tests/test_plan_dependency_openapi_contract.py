"""B13-B routes expose qualified relation, not a generic graph."""

from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def test_b13_b_plan_dependency_contract_is_typed_and_bounded() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    collection = cast(dict[str, Any], paths["/api/v1/temporal/plans/{plan_ref}/dependencies"])
    item = cast(
        dict[str, Any],
        paths["/api/v1/temporal/plans/{plan_ref}/dependencies/{dependency_ref}"],
    )
    history = cast(
        dict[str, Any],
        paths["/api/v1/temporal/plans/{plan_ref}/dependencies/{dependency_ref}/history"],
    )
    assert collection["post"]["operationId"] == "temporal_create_self_plan_dependency"
    assert collection["get"]["operationId"] == "temporal_list_self_plan_dependencies"
    assert item["get"]["operationId"] == "temporal_get_self_plan_dependency"
    assert item["put"]["operationId"] == "temporal_revise_self_plan_dependency"
    assert history["get"]["operationId"] == "temporal_list_self_plan_dependency_history"
    schemas = cast(dict[str, Any], cast(dict[str, Any], document["components"])["schemas"])
    create = cast(dict[str, Any], schemas["CreatePlanDependencyBody"])
    revise = cast(dict[str, Any], schemas["RevisePlanDependencyBody"])
    response = cast(dict[str, Any], schemas["PlanDependencyResponse"])
    assert set(create["properties"]) == {
        "operation_id",
        "prerequisite_step_ref",
        "dependent_step_ref",
        "qualifier_code",
        "disposition_code",
    }
    assert "expected_state_ref" in revise["properties"]
    assert {
        "dependency_ref",
        "purpose_code",
        "qualifier_code",
        "disposition_code",
        "evaluation_code",
        "cycle",
        "active",
    } <= set(response["properties"])
    assert "blocked" not in response["properties"]
