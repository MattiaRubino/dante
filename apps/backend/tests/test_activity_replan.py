"""Activity interval edits never turn named Sessions into calendar placements."""

from datetime import datetime
from typing import Literal
from uuid import uuid7

import pytest
from pydantic import ValidationError

from dante.modules.temporal.activity_edit_snapshot_api import (
    ActivityEditSnapshot,
    EditExecutionPolicy,
)
from dante.modules.temporal.activity_replan_api import (
    ActivityReplanCommand,
    DeletePlannedRow,
    NewPlannedRow,
    ReplanRow,
    RetainedPlannedRow,
    _validated_plan,
)
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.reality_objective_api import RealityPolicyResponse
from dante.platform.http.problem import ProblemError


def _time(hour: int) -> datetime:
    return datetime(2026, 10, 9, hour)  # noqa: DTZ001


def _row(
    role: Literal["envelope", "interval", "planned"], start: int, end: int
) -> ActivityScheduleResponse:
    return ActivityScheduleResponse(
        schedule_ref=uuid7(),
        placement_material_state_ref=uuid7(),
        role_code=role,
        temporal_form="named_zone_local",
        zone_id="Europe/Rome",
        starts_local_at=_time(start),
        ends_local_at=_time(end),
        presentation_order=None,
        display_name=None,
        start_date=None,
        end_date_exclusive=None,
        resolved_start_at=None,
        resolved_end_at=None,
        starts_at=None,
        ends_at=None,
        local_date=None,
        period_code=None,
    )


def _snapshot(*rows: ActivityScheduleResponse) -> ActivityEditSnapshot:
    activity_ref = uuid7()
    return ActivityEditSnapshot(
        activity_ref=activity_ref,
        execution_policy=EditExecutionPolicy(
            activity_ref=activity_ref, mode_code="disabled", state_ref=None
        ),
        reality_policy=RealityPolicyResponse(
            subject_kind="activity",
            subject_native_ref=activity_ref,
            state_ref=None,
            mode_code="manual",
        ),
        child_guard_mode="none",
        life_area_ref=None,
        schedules=list(rows),
        objectives=[],
        placement_lock=None,
        reminder=None,
    )


def _interval(row: ActivityScheduleResponse, start: int, end: int) -> ReplanRow:
    assert row.placement_material_state_ref is not None
    return ReplanRow(
        schedule_ref=row.schedule_ref,
        expected_material_state_ref=row.placement_material_state_ref,
        starts_local_at=_time(start),
        ends_local_at=_time(end),
    )


def _session(row: ActivityScheduleResponse) -> RetainedPlannedRow:
    return RetainedPlannedRow(
        schedule_ref=row.schedule_ref, expected_material_state_ref=row.placement_material_state_ref
    )


def test_replan_moves_activity_intervals_without_retiming_named_sessions() -> None:
    envelope, first, second, named = (
        _row("envelope", 9, 12),
        _row("interval", 9, 10),
        _row("interval", 11, 12),
        _row("planned", 11, 12),
    )
    changes, placements = _validated_plan(
        _snapshot(envelope, first, second, named),
        ActivityReplanCommand(
            operation_id="move",
            intervals=[_interval(first, 10, 11), _interval(second, 12, 13)],
            planned_sessions=[_session(named)],
        ),
    )
    assert {change.role for change in changes} == {"envelope", "interval"}
    assert len(placements) == 3
    assert all(change.schedule_ref != named.schedule_ref for change in changes)


def test_replan_requires_each_named_session_to_be_kept_or_deleted() -> None:
    envelope, interval, named = (
        _row("envelope", 9, 12),
        _row("interval", 9, 12),
        _row("planned", 10, 11),
    )
    with pytest.raises(ProblemError) as omitted:
        _validated_plan(
            _snapshot(envelope, interval, named),
            ActivityReplanCommand(operation_id="omitted", intervals=[_interval(interval, 9, 12)]),
        )
    assert omitted.value.status == 422

    changes, placements = _validated_plan(
        _snapshot(envelope, interval, named),
        ActivityReplanCommand(
            operation_id="delete",
            intervals=[_interval(interval, 9, 12)],
            delete_planned_sessions=[
                DeletePlannedRow(
                    schedule_ref=named.schedule_ref,
                    expected_material_state_ref=named.placement_material_state_ref,
                )
            ],
        ),
    )
    assert placements == []
    assert [(change.role, change.schedule_ref) for change in changes] == [
        ("planned_deleted", named.schedule_ref)
    ]


def test_replan_adds_an_untimed_named_session() -> None:
    envelope, interval = _row("envelope", 9, 12), _row("interval", 9, 12)
    added = NewPlannedRow(client_ref=uuid7(), name="Ripasso")
    changes, placements = _validated_plan(
        _snapshot(envelope, interval),
        ActivityReplanCommand(
            operation_id="add", intervals=[_interval(interval, 9, 12)], new_planned_sessions=[added]
        ),
    )
    assert placements == []
    assert [(change.role, change.client_ref) for change in changes] == [
        ("planned_added", added.client_ref)
    ]


def test_replan_rejects_overlapping_activity_intervals_even_with_named_sessions() -> None:
    envelope, first, second, named = (
        _row("envelope", 9, 12),
        _row("interval", 9, 10),
        _row("interval", 11, 12),
        _row("planned", 9, 12),
    )
    with pytest.raises(ProblemError) as invalid:
        _validated_plan(
            _snapshot(envelope, first, second, named),
            ActivityReplanCommand(
                operation_id="overlap",
                intervals=[_interval(first, 9, 11), _interval(second, 10, 12)],
                planned_sessions=[_session(named)],
            ),
        )
    assert invalid.value.status == 422


def test_named_session_identity_rejects_stale_placement_and_old_timed_payload() -> None:
    envelope, interval, named = (
        _row("envelope", 9, 12),
        _row("interval", 9, 12),
        _row("planned", 10, 11),
    )
    with pytest.raises(ProblemError) as stale:
        _validated_plan(
            _snapshot(envelope, interval, named),
            ActivityReplanCommand(
                operation_id="stale",
                intervals=[_interval(interval, 9, 12)],
                planned_sessions=[
                    RetainedPlannedRow(
                        schedule_ref=named.schedule_ref, expected_material_state_ref=uuid7()
                    )
                ],
            ),
        )
    assert stale.value.status == 409
    with pytest.raises(ValidationError):
        NewPlannedRow.model_validate(
            {"client_ref": uuid7(), "name": "Ripasso", "starts_local_at": _time(10)}
        )
