"""Coordinated Activity planning must retain explicit dependent intent."""

from datetime import datetime
from types import SimpleNamespace
from uuid import uuid7

import pytest

from dante.modules.temporal.activity_replan_api import (
    ActivityReplanCommand,
    NewPlannedRow,
    ReplanRow,
    _validated_plan,
)
from dante.platform.http.problem import ProblemError


def _time(hour: int) -> datetime:
    return datetime(2026, 10, 9, hour)  # noqa: DTZ001


def _row(role: str, start: int, end: int):
    return SimpleNamespace(
        schedule_ref=uuid7(), placement_material_state_ref=uuid7(),
        role_code=role, temporal_form="named_zone_local", zone_id="Europe/Rome",
        starts_local_at=_time(start), ends_local_at=_time(end),
    )


def _intent(row, start: int, end: int) -> ReplanRow:
    return ReplanRow(
        schedule_ref=row.schedule_ref,
        expected_material_state_ref=row.placement_material_state_ref,
        starts_local_at=_time(start), ends_local_at=_time(end),
    )


def test_replan_previews_every_changed_interval_and_planned_session() -> None:
    envelope, first, second, planned = (
        _row("envelope", 9, 12), _row("interval", 9, 10),
        _row("interval", 11, 12), _row("planned", 11, 12),
    )
    changes, placements = _validated_plan(
        SimpleNamespace(schedules=[envelope, first, second, planned]),
        ActivityReplanCommand(
            operation_id="move-all",
            intervals=[_intent(first, 10, 11), _intent(second, 12, 13)],
            planned_sessions=[_intent(planned, 12, 13)],
        ),
    )
    assert {change.role for change in changes} == {"envelope", "interval", "planned"}
    assert len(changes) == len(placements) == 4
    assert changes[0].proposed_start == _time(10)
    assert changes[0].proposed_end == _time(13)


def test_replan_rejects_omitted_or_overlapping_dependents_and_stale_basis() -> None:
    envelope, first, planned = (
        _row("envelope", 9, 12), _row("interval", 9, 12),
        _row("planned", 10, 11),
    )
    snapshot = SimpleNamespace(schedules=[envelope, first, planned])
    with pytest.raises(ProblemError) as omitted:
        _validated_plan(snapshot, ActivityReplanCommand(
            operation_id="omitted", intervals=[_intent(first, 10, 13)],
        ))
    assert omitted.value.status == 422

    with pytest.raises(ProblemError) as outside:
        _validated_plan(snapshot, ActivityReplanCommand(
            operation_id="outside", intervals=[_intent(first, 10, 13)],
            planned_sessions=[_intent(planned, 9, 10)],
        ))
    assert outside.value.status == 422

    stale = _intent(first, 10, 13).model_copy(
        update={"expected_material_state_ref": uuid7()},
    )
    with pytest.raises(ProblemError) as conflict:
        _validated_plan(snapshot, ActivityReplanCommand(
            operation_id="stale", intervals=[stale],
            planned_sessions=[_intent(planned, 10, 11)],
        ))
    assert conflict.value.status == 409


def test_replan_previews_replacement_and_rejects_ambiguous_planned_rows() -> None:
    envelope, interval, planned = (
        _row("envelope", 9, 12), _row("interval", 9, 12), _row("planned", 9, 10),
    )
    addition = NewPlannedRow(
        client_ref=uuid7(), name="Nuova sessione",
        starts_local_at=_time(10), ends_local_at=_time(11),
    )
    snapshot = SimpleNamespace(schedules=[envelope, interval, planned])
    changes, placements = _validated_plan(snapshot, ActivityReplanCommand(
        operation_id="replace", intervals=[_intent(interval, 9, 12)],
        remove_planned_sessions=[_intent(planned, 9, 10)],
        new_planned_sessions=[addition],
    ))
    assert placements == []
    assert {change.role for change in changes} == {"planned_removed", "planned_added"}
    assert next(change.client_ref for change in changes if change.role == "planned_added") == addition.client_ref
    with pytest.raises(ProblemError) as duplicate:
        _validated_plan(snapshot, ActivityReplanCommand(
            operation_id="duplicate", intervals=[_intent(interval, 9, 12)],
            planned_sessions=[_intent(planned, 9, 10)],
            remove_planned_sessions=[_intent(planned, 9, 10)],
        ))
    assert duplicate.value.status == 422
