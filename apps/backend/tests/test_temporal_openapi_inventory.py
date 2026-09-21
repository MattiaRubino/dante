from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document

_HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "options", "head", "trace"})

# Accepted pre-B04 Temporal v1 compatibility baseline.
#
# These operationIds were originally FastAPI-generated. They are intentionally
# frozen rather than cosmetically renamed because Orval export names are already
# a published repository contract. They are the only legacy exception to the
# semantic operationId rule below.
_PRE_B04_TEMPORAL_OPERATIONS = {
    ("/api/v1/temporal/timeline/window", "get"): (
        "get_timeline_window_api_v1_temporal_timeline_window_get"
    ),
    ("/api/v1/temporal/activities", "post"): ("create_activity_api_v1_temporal_activities_post"),
    ("/api/v1/temporal/activities/scheduled", "post"): (
        "create_scheduled_activity_api_v1_temporal_activities_scheduled_post"
    ),
    ("/api/v1/temporal/activities/{activity_ref}/schedule", "post"): (
        "establish_activity_schedule_api_v1_temporal_activities__activity_ref__schedule_post"
    ),
    ("/api/v1/temporal/schedules/{schedule_ref}/placement", "patch"): (
        "revise_schedule_placement_api_v1_temporal_schedules__schedule_ref__placement_patch"
    ),
    ("/api/v1/temporal/schedules/{schedule_ref}/unschedule", "post"): (
        "unschedule_schedule_api_v1_temporal_schedules__schedule_ref__unschedule_post"
    ),
    ("/api/v1/temporal/schedules/{schedule_ref}/unschedule/undo", "post"): (
        "undo_schedule_unschedule_api_v1_temporal_schedules__schedule_ref__unschedule_undo_post"
    ),
    ("/api/v1/temporal/activities/unplaced", "get"): (
        "list_unplaced_activities_api_v1_temporal_activities_unplaced_get"
    ),
    ("/api/v1/temporal/activities/{activity_ref}", "get"): (
        "get_activity_api_v1_temporal_activities__activity_ref__get"
    ),
    ("/api/v1/temporal/events", "post"): ("create_event_api_v1_temporal_events_post"),
    ("/api/v1/temporal/events/scheduled", "post"): (
        "create_scheduled_event_api_v1_temporal_events_scheduled_post"
    ),
    ("/api/v1/temporal/events/{event_ref}/agenda", "put"): (
        "replace_event_agenda_api_v1_temporal_events__event_ref__agenda_put"
    ),
    ("/api/v1/temporal/events/{event_ref}", "get"): (
        "get_event_api_v1_temporal_events__event_ref__get"
    ),
}

# Current accepted public Temporal inventory. B04+ endpoint additions belong
# here, while _PRE_B04_TEMPORAL_OPERATIONS remains immutable compatibility
# history so new operations cannot inherit the legacy implicit-ID exception.
_EXPECTED_TEMPORAL_OPERATIONS = {
    **_PRE_B04_TEMPORAL_OPERATIONS,
    ("/api/v1/temporal/events/postponed", "get"): "temporal_list_postponed_events",
    ("/api/v1/temporal/events/{event_ref}/schedules/{schedule_ref}/replan", "put"): "temporal_replan_postponed_event",
    ("/api/v1/temporal/life-areas", "post"): "temporal_create_life_area",
    ("/api/v1/temporal/life-areas", "get"): "temporal_list_life_areas",
    ("/api/v1/temporal/life-areas/order", "put"): "temporal_reorder_life_areas",
    ("/api/v1/temporal/life-areas/{life_area_ref}/name", "patch"): "temporal_rename_life_area",
    ("/api/v1/temporal/life-areas/{life_area_ref}/archive", "post"): "temporal_archive_life_area",
    (
        "/api/v1/temporal/life-areas/{life_area_ref}/visibility",
        "put",
    ): "temporal_set_life_area_visibility",
    (
        "/api/v1/temporal/life-areas/{life_area_ref}/appearance",
        "put",
    ): "temporal_set_life_area_appearance",
    ("/api/v1/temporal/life-area-assignments", "get"): "temporal_list_life_area_assignments",
    ("/api/v1/temporal/tags", "post"): "temporal_create_product_tag",
    ("/api/v1/temporal/tags", "get"): "temporal_list_product_tags",
    ("/api/v1/temporal/tags/{tag_ref}/name", "put"): "temporal_rename_product_tag",
    ("/api/v1/temporal/tags/{tag_ref}/archive", "post"): "temporal_archive_product_tag",
    ("/api/v1/temporal/tags/assignments", "get"): "temporal_list_item_tags",
    (
        "/api/v1/temporal/activities/{activity_ref}/tags/{tag_ref}/attach",
        "post",
    ): "temporal_attach_activity_tag",
    (
        "/api/v1/temporal/activities/{activity_ref}/tags/{tag_ref}/detach",
        "post",
    ): "temporal_detach_activity_tag",
    (
        "/api/v1/temporal/events/{event_ref}/tags/{tag_ref}/attach",
        "post",
    ): "temporal_attach_event_tag",
    (
        "/api/v1/temporal/events/{event_ref}/tags/{tag_ref}/detach",
        "post",
    ): "temporal_detach_event_tag",
    (
        "/api/v1/temporal/life-area-assignments/unassigned",
        "get",
    ): "temporal_list_unassigned_life_area_items",
    (
        "/api/v1/temporal/life-area-assignments/activities/{activity_ref}",
        "put",
    ): "temporal_assign_activity_life_area",
    (
        "/api/v1/temporal/life-area-assignments/events/{event_ref}",
        "put",
    ): "temporal_assign_event_life_area",
    ("/api/v1/temporal/constraints", "post"): "temporal_create_constraint",
    ("/api/v1/temporal/constraints", "get"): ("temporal_list_constraints_by_subject"),
    ("/api/v1/temporal/constraints/evaluate", "post"): ("temporal_evaluate_constraints"),
    ("/api/v1/temporal/constraints/{constraint_ref}", "get"): ("temporal_get_constraint"),
    ("/api/v1/temporal/constraints/{constraint_ref}/rule", "patch"): (
        "temporal_revise_constraint_rule"
    ),
    ("/api/v1/temporal/constraints/{constraint_ref}/retire", "post"): (
        "temporal_retire_constraint"
    ),
    ("/api/v1/temporal/activities/constrained", "post"): ("temporal_create_constrained_activity"),
}


def _temporal_operations(document: dict[str, Any]) -> dict[tuple[str, str], str]:
    paths = cast(dict[str, Any], document["paths"])
    inventory: dict[tuple[str, str], str] = {}

    for path, raw_path_item in paths.items():
        if not path.startswith("/api/v1/temporal/"):
            continue
        path_item = cast(dict[str, Any], raw_path_item)
        for method, raw_operation in path_item.items():
            if method not in _HTTP_METHODS:
                continue
            operation = cast(dict[str, Any], raw_operation)
            operation_id = cast(str, operation["operationId"])
            inventory[(path, method)] = operation_id

    return inventory


def test_complete_temporal_operation_inventory_and_operation_ids_are_frozen() -> None:
    """No Temporal endpoint may be lost, duplicated or silently renamed."""
    actual = _temporal_operations(openapi_document())

    assert actual == _EXPECTED_TEMPORAL_OPERATIONS
    assert len(set(actual.values())) == len(actual)


def test_post_b03_temporal_operations_use_explicit_semantic_operation_ids() -> None:
    """Only the frozen pre-B04 surface may retain implicit FastAPI operationIds."""
    actual = _temporal_operations(openapi_document())

    for key, operation_id in actual.items():
        if key in _PRE_B04_TEMPORAL_OPERATIONS:
            assert operation_id == _PRE_B04_TEMPORAL_OPERATIONS[key]
            continue
        assert operation_id.startswith("temporal_"), (
            f"new Temporal operation {key!r} must define an explicit stable semantic "
            f"operationId starting with 'temporal_'; got {operation_id!r}"
        )


def test_temporal_inventory_is_only_v1_temporal_surface() -> None:
    """Keep the inventory boundary exact instead of accidentally governing other APIs."""
    assert all(path.startswith("/api/v1/temporal/") for path, _ in _EXPECTED_TEMPORAL_OPERATIONS)
