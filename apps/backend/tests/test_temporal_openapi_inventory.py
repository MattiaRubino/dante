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
    ("/api/v1/temporal/activities", "post"): (
        "create_activity_api_v1_temporal_activities_post"
    ),
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
    ("/api/v1/temporal/events", "post"): (
        "create_event_api_v1_temporal_events_post"
    ),
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
