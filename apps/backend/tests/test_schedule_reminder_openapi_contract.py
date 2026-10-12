"""B11-C public contract keeps Reminder configuration separate from delivery."""

from __future__ import annotations

from typing import Any, cast

from dante.bootstrap.openapi_export import openapi_document


def test_b11_c_reminder_operations_and_payload_are_bounded() -> None:
    document = openapi_document()
    paths = cast(dict[str, Any], document["paths"])
    operations = cast(dict[str, Any], paths["/api/v1/temporal/schedules/{schedule_ref}/reminder"])
    assert operations["get"]["operationId"] == "temporal_get_schedule_reminder"
    assert operations["put"]["operationId"] == "temporal_configure_schedule_reminder"
    assert set(operations["put"]["responses"]) == {
        "200", "201", "400", "401", "403", "404", "409", "422", "500"
    }

    schemas = cast(dict[str, Any], cast(dict[str, Any], document["components"])["schemas"])
    request = cast(dict[str, Any], schemas["ScheduleReminderRequest"])
    request_properties = cast(dict[str, Any], request["properties"])
    assert set(request_properties) == {
        "operation_id", "expected_material_state_ref", "enabled", "lead_minutes"
    }
    assert request_properties["lead_minutes"]["minimum"] == 0
    assert request_properties["lead_minutes"]["maximum"] == 10080
    response = cast(dict[str, Any], schemas["ScheduleReminderResponse"])
    properties = cast(dict[str, Any], response["properties"])
    assert set(properties) == {
        "reminder_ref", "schedule_ref", "material_state_ref", "enabled",
        "lead_minutes", "schedule_starts_at", "due_at", "disposition_code", "replayed"
    }
    assert set(properties["disposition_code"]["enum"]) == {
        "pending", "due", "unavailable"
    }
