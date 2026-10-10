"""Deterministic projection tests: clock passage is never execution."""

from datetime import UTC, datetime
from uuid import uuid7


from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.session_panel_api import build_panel


def schedule(role="planned", start=None, end=None, form="absolute", **extra):
    value = dict.fromkeys(ActivityScheduleResponse.model_fields)
    value.update(
        schedule_ref=str(uuid7()),
        role_code=role,
        presentation_order=1,
        display_name="Ripasso",
        temporal_form=form if start else None,
    )
    if form == "absolute":
        value.update(starts_at=start, ends_at=end)
    elif form == "floating_local":
        value.update(starts_local_at=start, ends_local_at=end)
    elif form == "named_zone_local":
        value.update(resolved_start_at=start, resolved_end_at=end, zone_id="Europe/Rome")
    value.update(extra)
    return value


def owner(*schedules, mode="live", executions=()):
    return {
        "activity_ref": uuid7(),
        "title": "Studio",
        "mode_code": mode,
        "schedules": list(schedules),
        "executions": list(executions),
    }


def at(hour, minute=0):
    return datetime(2026, 10, 9, hour, minute, tzinfo=UTC)


def names(panel):
    return [row.name for group in panel.groups for row in group.rows]


def execution(ref=None, **extra):
    return dict(
        session_ref=str(uuid7()),
        timing_material_state_ref=str(uuid7()),
        planned_schedule_ref=ref,
        paused=False,
        **extra,
    )


def test_exact_start_and_end_and_next_boundary():
    record = owner(schedule("envelope", at(9), at(12)), schedule(start=at(10), end=at(11)))
    early = build_panel([record], at(9), "UTC")
    assert names(early) == ["Sessione attività"]
    assert early.next_change_at == at(9, 55)
    assert names(build_panel([record], at(9, 55), "UTC")) == [
        "Sessione attività", "Ripasso"
    ]
    assert names(build_panel([record], at(10), "UTC")) == [
        "Sessione attività", "Ripasso"
    ]
    assert names(build_panel([record], at(11), "UTC")) == ["Sessione attività"]
    assert build_panel([record], at(12), "UTC").groups == []


def test_untimed_uses_intervals_not_envelope_gaps():
    record = owner(
        schedule("envelope", at(9), at(12)),
        schedule("interval", at(9), at(10)),
        schedule("interval", at(11), at(12)),
        schedule(),
    )
    assert "Ripasso" in names(build_panel([record], at(9), "UTC"))
    assert build_panel([record], at(10), "UTC").groups == []
    assert "Ripasso" in names(build_panel([record], at(11), "UTC"))


def test_independent_groups_and_unique_activity_with_multiple_intervals():
    first = owner(
        schedule("interval", at(9), at(12)), schedule(), schedule(display_name="Esercizi")
    )
    second = owner(schedule("envelope", at(9), at(12)), schedule())
    panel = build_panel([first, second], at(10), "UTC")
    assert len(panel.groups) == 2
    assert len(panel.groups[0].rows) == 3  # generic main plus two planned internals


def test_open_executions_survive_end_and_disabled_capture_without_collapsing_attempts():
    planned = schedule(start=at(9), end=at(10))
    record = owner(
        planned,
        mode="disabled",
        executions=[
            execution(planned["schedule_ref"]),
            execution(planned["schedule_ref"]),
            execution(),
        ],
    )
    panel = build_panel([record], at(23), "UTC")
    assert len(panel.groups[0].rows) == 3
    assert len({r.execution.session_ref for r in panel.groups[0].rows}) == 3


def test_independent_planned_slice_is_ready_without_main_capture():
    record = owner(schedule("envelope", at(9), at(12)), schedule(), mode="internal_only")
    assert names(build_panel([record], at(10), "UTC")) == ["Ripasso"]
    assert names(build_panel([record], at(13), "UTC")) == []


def test_disabled_capture_without_planned_slices_never_offers_main():
    record = owner(schedule("envelope", at(9), at(12)), mode="disabled")
    assert build_panel([record], at(10), "UTC").groups == []


def test_floating_time_uses_effective_zone_not_server_zone():
    record = owner(
        schedule("envelope", "2026-10-09T09:00:00", "2026-10-09T10:00:00", "floating_local"),
        schedule(),
    )
    assert "Ripasso" in names(build_panel([record], at(7), "Europe/Rome"))
    assert build_panel([record], at(8), "Europe/Rome").groups == []


def test_named_zone_uses_resolved_instant_in_dst_overlap():
    record = owner(
        schedule(start="2026-10-25T01:30:00Z", end="2026-10-25T02:30:00Z", form="named_zone_local")
    )
    assert (
        build_panel([record], datetime(2026, 10, 25, 0, 30, tzinfo=UTC), "Europe/Rome").groups == []
    )
    assert names(
        build_panel([record], datetime(2026, 10, 25, 1, 30, tzinfo=UTC), "Europe/Rome")
    ) == ["Ripasso"]


def test_date_span_and_coarse_precision_do_not_invent_hourly_boundaries():
    for row in [
        schedule(
            "envelope",
            temporal_form="date_span",
            start_date="2026-10-09",
            end_date_exclusive="2026-10-10",
        ),
        schedule(
            "envelope",
            temporal_form="coarse_local_period",
            local_date="2026-10-09",
            period_code="evening",
        ),
    ]:
        record = owner(row, schedule())
        assert "Ripasso" in names(build_panel([record], at(0), "Europe/Rome"))
        assert build_panel([record], at(22), "Europe/Rome").groups == []


def test_no_placement_does_not_invent_activity_start_but_open_work_survives():
    assert build_panel([owner(schedule())], at(10), "UTC").groups == []
    record = owner(executions=[execution(str(uuid7()))])
    assert names(build_panel([record], at(10), "UTC")) == ["Sessione in corso"]


def test_preview_is_not_an_execution_and_exact_start_is_preserved():
    planned = schedule(start=at(10), end=at(11))
    record = owner(schedule("envelope", at(9), at(12)), planned)
    early = build_panel([record], at(9, 54), "UTC")
    assert names(early) == ["Sessione attività"]
    assert early.next_change_at == at(9, 55)
    preview = build_panel([record], at(9, 55), "UTC")
    assert names(preview) == ["Sessione attività", "Ripasso"]
    child = preview.groups[0].rows[1]
    assert child.starts_at == at(10)
    assert child.execution is None
    assert preview.next_change_at == at(10)


def test_main_preview_does_not_fill_interval_gaps():
    record = owner(
        schedule("interval", at(9), at(10)),
        schedule("interval", at(11), at(12)),
        schedule(),
    )
    assert build_panel([record], at(10, 30), "UTC").groups == []
    assert names(build_panel([record], at(10, 55), "UTC")) == [
        "Sessione attività"
    ]
    assert names(build_panel([record], at(11), "UTC")) == [
        "Sessione attività", "Ripasso"
    ]


def test_completed_main_exits_desk_and_hides_untouched_internal_rows():
    envelope = schedule("envelope", at(18), at(19))
    internal = schedule(start=at(18), end=at(19))
    activity = owner(envelope, internal)
    stopped = [{
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": None,
        "started_at": at(18, 10),
        "ended_at": at(18, 12),
    }]
    assert names(build_panel([activity], at(18, 10), "UTC")) == [
        "Sessione attività", "Ripasso",
    ]
    assert build_panel([activity], at(18, 12), "UTC", stopped).groups == []
    assert build_panel([activity], at(18, 30), "UTC", stopped).groups == []
    assert build_panel([activity], at(19), "UTC", stopped).groups == []


def test_completed_internal_exits_desk_while_main_stays_available():
    envelope = schedule("envelope", at(18), at(19))
    internal = schedule(start=at(18), end=at(19))
    activity = owner(envelope, internal)
    stopped = [{
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": internal["schedule_ref"],
        "started_at": at(18, 10),
        "ended_at": at(18, 12),
    }]
    assert names(build_panel([activity], at(18, 12), "UTC", stopped)) == [
        "Sessione attività",
    ]


def test_old_stopped_execution_does_not_hide_new_unrelated_interval():
    first = schedule("interval", at(9), at(10))
    second = schedule("interval", at(18), at(19))
    activity = owner(first, second)
    stopped = [{
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": None,
        "started_at": at(9, 10),
        "ended_at": at(9, 30),
    }]
    assert names(build_panel([activity], at(9, 30), "UTC", stopped)) == []
    assert names(build_panel([activity], at(18), "UTC", stopped)) == [
        "Sessione attività",
    ]
