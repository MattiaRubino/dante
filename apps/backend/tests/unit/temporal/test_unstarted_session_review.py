"""Current-plan projection of never-started Activity Session review rows."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.resolution_queue_api import _unstarted_session_items


def _schedule(role: str, start: datetime | None, end: datetime | None) -> dict[str, Any]:
    row: dict[str, Any] = dict.fromkeys(ActivityScheduleResponse.model_fields)
    row.update(
        schedule_ref=uuid7(),
        role_code=role,
        presentation_order=1,
        display_name="Ripasso" if role == "planned" else None,
        temporal_form="absolute" if start is not None else None,
        starts_at=start,
        ends_at=end,
    )
    return row


def _owner(
    end: datetime,
    *,
    mode: str = "live",
    attempts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "activity_ref": uuid7(),
        "title": "Studio",
        "mode_code": mode,
        "schedules": [
            _schedule("envelope", datetime(2026, 10, 9, 9, tzinfo=UTC), end),
            _schedule("planned", None, None),
        ],
        "historical_attempts": attempts or [],
    }


def test_unstarted_rows_follow_the_current_plan_across_past_and_future() -> None:
    now = datetime(2026, 10, 10, 12, tzinfo=UTC)
    record = _owner(datetime(2026, 10, 9, 10, tzinfo=UTC))
    previous = _unstarted_session_items([record], now, "Europe/Rome")
    assert len(previous) == 2
    assert {row.planned_schedule_ref for row in previous} == {
        None,
        record["schedules"][1]["schedule_ref"],
    }
    assert all(row.actions == [] and row.session_ref is None for row in previous)

    record["schedules"][0]["ends_at"] = datetime(2026, 10, 11, 10, tzinfo=UTC)
    assert _unstarted_session_items([record], now, "Europe/Rome") == []
    assert (
        len(
            _unstarted_session_items(
                [record], datetime(2026, 10, 11, 10, tzinfo=UTC), "Europe/Rome"
            )
        )
        == 2
    )


def test_only_unattempted_enabled_parts_are_reviewed() -> None:
    now = datetime(2026, 10, 10, 12, tzinfo=UTC)
    record = _owner(datetime(2026, 10, 9, 10, tzinfo=UTC), mode="internal_only")
    assert len(_unstarted_session_items([record], now, "UTC")) == 1
    record["historical_attempts"] = [
        {"planned_schedule_ref": record["schedules"][1]["schedule_ref"]}
    ]
    assert _unstarted_session_items([record], now, "UTC") == []

    record["mode_code"] = "record"
    record["historical_attempts"] = []
    record_only = _unstarted_session_items([record], now, "UTC")
    assert len(record_only) == 1
    assert record_only[0].planned_schedule_ref is not None

    record["mode_code"] = "live"
    record["historical_attempts"] = [
        {"planned_schedule_ref": record["schedules"][1]["schedule_ref"]}
    ]
    pending = _unstarted_session_items([record], now, "UTC")
    assert len(pending) == 1
    assert pending[0].planned_schedule_ref is None
    record["historical_attempts"].append({"planned_schedule_ref": None})
    assert _unstarted_session_items([record], now, "UTC") == []


def test_every_current_interval_must_have_ended() -> None:
    now = datetime(2026, 10, 10, 12, tzinfo=UTC)
    record = _owner(datetime(2026, 10, 9, 10, tzinfo=UTC))
    record["schedules"].extend(
        [
            _schedule(
                "interval",
                datetime(2026, 10, 9, 9, tzinfo=UTC),
                datetime(2026, 10, 9, 10, tzinfo=UTC),
            ),
            _schedule(
                "interval",
                datetime(2026, 10, 11, 9, tzinfo=UTC),
                datetime(2026, 10, 11, 10, tzinfo=UTC),
            ),
        ]
    )
    assert _unstarted_session_items([record], now, "UTC") == []
