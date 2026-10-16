"""Deterministic projection tests: clock passage is never execution."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.session_panel_api import SessionPanelResponse, build_panel


def schedule(
    role: str = "planned",
    start: datetime | str | None = None,
    end: datetime | str | None = None,
    form: str = "absolute",
    **extra: Any,
) -> dict[str, Any]:
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


def owner(
    *schedules: dict[str, Any],
    mode: str = "live",
    executions: tuple[dict[str, Any], ...] | list[dict[str, Any]] = (),
) -> dict[str, Any]:
    return {
        "activity_ref": uuid7(),
        "title": "Studio",
        "mode_code": mode,
        "schedules": list(schedules),
        "executions": list(executions),
    }


def at(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 10, 9, hour, minute, tzinfo=UTC)


def names(panel: SessionPanelResponse) -> list[str]:
    return [row.name for group in panel.groups for row in group.rows]


def execution(ref: str | None = None, **extra: Any) -> dict[str, Any]:
    return dict(
        session_ref=str(uuid7()),
        timing_material_state_ref=str(uuid7()),
        planned_schedule_ref=ref,
        paused=False,
        **extra,
    )


def test_exact_start_and_end_and_next_boundary() -> None:
    record = owner(schedule("envelope", at(9), at(12)), schedule(start=at(10), end=at(11)))
    early = build_panel([record], at(9), "UTC")
    assert names(early) == ["Sessione attività", "Ripasso"]
    assert early.next_change_at == at(12)
    assert names(build_panel([record], at(9, 55), "UTC")) == ["Sessione attività", "Ripasso"]
    assert names(build_panel([record], at(10), "UTC")) == ["Sessione attività", "Ripasso"]
    assert names(build_panel([record], at(11), "UTC")) == ["Sessione attività", "Ripasso"]
    assert build_panel([record], at(12), "UTC").groups == []


def test_untimed_uses_intervals_not_envelope_gaps() -> None:
    record = owner(
        schedule("envelope", at(9), at(12)),
        schedule("interval", at(9), at(10)),
        schedule("interval", at(11), at(12)),
        schedule(),
    )
    assert "Ripasso" in names(build_panel([record], at(9), "UTC"))
    assert build_panel([record], at(10), "UTC").groups == []
    assert "Ripasso" in names(build_panel([record], at(11), "UTC"))


def test_independent_groups_and_unique_activity_with_multiple_intervals() -> None:
    first = owner(
        schedule("interval", at(9), at(12)), schedule(), schedule(display_name="Esercizi")
    )
    second = owner(schedule("envelope", at(9), at(12)), schedule())
    panel = build_panel([first, second], at(10), "UTC")
    assert len(panel.groups) == 2
    assert len(panel.groups[0].rows) == 3  # generic main plus two planned internals


def test_main_started_hours_early_exposes_all_unstarted_internal_sessions() -> None:
    record = owner(
        schedule("interval", at(23, 30), at(23, 59)),
        schedule(display_name="Ripasso"),
        schedule(display_name="Esercizi"),
        executions=[execution()],
    )
    # This is not an Activity preview at 20:47; only explicit main Play
    # makes the named Sessions visible before the planned 23:30 start.
    before = {**record, "executions": []}
    assert build_panel([before], at(20, 47), "UTC").groups == []

    panel = build_panel([record], at(20, 47), "UTC")
    assert names(panel) == ["Sessione attività", "Ripasso", "Esercizi"]
    assert panel.next_change_at == at(23, 25)
    main, *internals = panel.groups[0].rows
    assert main.execution is not None
    assert main.execution.paused is False
    assert all(row.execution is None for row in internals)
    assert all(row.starts_at is None for row in internals)
    assert len({row.planned_schedule_ref for row in internals}) == 2


def test_paused_main_keeps_early_internal_rows_visible_without_auto_start() -> None:
    record = owner(
        schedule("interval", at(23, 30), at(23, 59)),
        schedule(display_name="Ripasso"),
        schedule(display_name="Esercizi"),
        executions=[{**execution(), "paused": True}],
    )
    panel = build_panel([record], at(20, 47), "UTC")
    assert names(panel) == ["Sessione attività", "Ripasso", "Esercizi"]
    assert panel.groups[0].rows[0].execution is not None
    assert panel.groups[0].rows[0].execution.paused is True
    assert all(row.execution is None for row in panel.groups[0].rows[1:])
    # Stopping the main execution removes the early access: it must not
    # leave orphaned ready children before the scheduled preview.
    stopped = {**record, "executions": []}
    assert build_panel([stopped], at(20, 47), "UTC").groups == []


def test_open_main_keeps_configured_internal_sessions_visible_after_plan_ends() -> None:
    record = owner(
        schedule("interval", at(18), at(19)),
        schedule(display_name="Ripasso"),
        executions=[execution()],
    )
    assert names(build_panel([record], at(20), "UTC")) == [
        "Sessione attività",
        "Ripasso",
    ]
    assert build_panel([{**record, "executions": []}], at(20), "UTC").groups == []


def test_early_child_stop_stays_retired_during_current_main_attempt() -> None:
    named = schedule(display_name="Ripasso")
    activity = owner(
        schedule("interval", at(23, 30), at(23, 59)),
        named,
        executions=[execution()],
    )
    visuals = [
        {
            "activity_ref": activity["activity_ref"],
            "planned_schedule_ref": None,
            "started_at": at(20, 46),
            "ended_at": None,
        },
        {
            "activity_ref": activity["activity_ref"],
            "planned_schedule_ref": named["schedule_ref"],
            "started_at": at(20, 47),
            "ended_at": at(20, 48),
        },
    ]
    panel = build_panel([activity], at(20, 50), "UTC", visuals)
    assert names(panel) == ["Sessione attività"]


def test_new_main_attempt_re_admits_children_stopped_in_previous_attempt() -> None:
    named = schedule(display_name="Ripasso")
    activity = owner(
        schedule("interval", at(23, 30), at(23, 59)),
        named,
        executions=[execution()],
    )
    stopped_main = {
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": None,
        "started_at": at(23, 30),
        "ended_at": at(23, 31),
    }
    stopped_child = {
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": named["schedule_ref"],
        "started_at": at(23, 30),
        "ended_at": at(23, 31),
    }
    new_main = {
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": None,
        "started_at": at(23, 32),
        "ended_at": None,
    }
    # A previously stopped main within the same plan interval must not
    # suppress child readiness after an explicit new main Play.
    previous = [stopped_main, stopped_child, new_main]
    assert names(build_panel([activity], at(23, 35), "UTC", previous)) == [
        "Sessione attività",
        "Ripasso",
    ]
    new_child_stop = {
        "activity_ref": activity["activity_ref"],
        "planned_schedule_ref": named["schedule_ref"],
        "started_at": at(23, 33),
        "ended_at": at(23, 34),
    }
    after_child_stop = build_panel(
        [activity], at(23, 35), "UTC", [*previous, new_child_stop]
    )
    assert names(after_child_stop) == ["Sessione attività"]


def test_open_executions_survive_end_and_disabled_capture_without_collapsing_attempts() -> None:
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
    executions = [row.execution for row in panel.groups[0].rows]
    assert all(item is not None for item in executions)
    assert len({item.session_ref for item in executions if item is not None}) == 3


def test_independent_planned_slice_is_ready_without_main_capture() -> None:
    record = owner(schedule("envelope", at(9), at(12)), schedule(), mode="internal_only")
    assert names(build_panel([record], at(10), "UTC")) == ["Ripasso"]
    assert names(build_panel([record], at(13), "UTC")) == []


def test_disabled_capture_without_planned_slices_never_offers_main() -> None:
    record = owner(schedule("envelope", at(9), at(12)), mode="disabled")
    assert build_panel([record], at(10), "UTC").groups == []


def test_floating_time_uses_effective_zone_not_server_zone() -> None:
    record = owner(
        schedule("envelope", "2026-10-09T09:00:00", "2026-10-09T10:00:00", "floating_local"),
        schedule(),
    )
    assert "Ripasso" in names(build_panel([record], at(7), "Europe/Rome"))
    assert build_panel([record], at(8), "Europe/Rome").groups == []


def test_named_zone_uses_resolved_instant_in_dst_overlap() -> None:
    record = owner(
        schedule(
            "envelope",
            start="2026-10-25T01:30:00Z",
            end="2026-10-25T02:30:00Z",
            form="named_zone_local",
        ),
        schedule(start="2026-10-25T01:30:00Z", end="2026-10-25T02:30:00Z", form="named_zone_local"),
    )
    assert (
        build_panel([record], datetime(2026, 10, 25, 0, 30, tzinfo=UTC), "Europe/Rome").groups == []
    )
    assert names(
        build_panel([record], datetime(2026, 10, 25, 1, 30, tzinfo=UTC), "Europe/Rome")
    ) == ["Sessione attività", "Ripasso"]


def test_date_span_and_coarse_precision_do_not_invent_hourly_boundaries() -> None:
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


def test_no_placement_does_not_invent_activity_start_but_open_work_survives() -> None:
    assert build_panel([owner(schedule())], at(10), "UTC").groups == []
    record = owner(executions=[execution(str(uuid7()))])
    assert names(build_panel([record], at(10), "UTC")) == ["Sessione in corso"]


def test_named_session_uses_activity_preview_and_has_no_own_planned_time() -> None:
    # The legacy named schedule carries old timestamps, but panel availability
    # follows the enclosing Activity interval and exposes no child clock.
    planned = schedule(start=at(10), end=at(11))
    record = owner(schedule("envelope", at(9), at(12)), planned)
    assert names(build_panel([record], at(8, 54), "UTC")) == []
    preview = build_panel([record], at(8, 55), "UTC")
    child = preview.groups[0].rows[1]
    assert child.name == "Ripasso"
    assert child.starts_at is None
    assert child.execution is None
    assert preview.next_change_at == at(9)


def test_main_preview_does_not_fill_interval_gaps() -> None:
    record = owner(
        schedule("interval", at(9), at(10)),
        schedule("interval", at(11), at(12)),
        schedule(),
    )
    assert build_panel([record], at(10, 30), "UTC").groups == []
    assert names(build_panel([record], at(10, 55), "UTC")) == ["Sessione attività", "Ripasso"]
    assert names(build_panel([record], at(11), "UTC")) == ["Sessione attività", "Ripasso"]


def test_completed_main_exits_desk_and_hides_untouched_internal_rows() -> None:
    envelope = schedule("envelope", at(18), at(19))
    internal = schedule(start=at(18), end=at(19))
    activity = owner(envelope, internal)
    stopped = [
        {
            "activity_ref": activity["activity_ref"],
            "planned_schedule_ref": None,
            "started_at": at(18, 10),
            "ended_at": at(18, 12),
        }
    ]
    assert names(build_panel([activity], at(18, 10), "UTC")) == [
        "Sessione attività",
        "Ripasso",
    ]
    assert build_panel([activity], at(18, 12), "UTC", stopped).groups == []
    assert build_panel([activity], at(18, 30), "UTC", stopped).groups == []
    assert build_panel([activity], at(19), "UTC", stopped).groups == []


def test_completed_internal_exits_desk_while_main_stays_available() -> None:
    envelope = schedule("envelope", at(18), at(19))
    internal = schedule(start=at(18), end=at(19))
    activity = owner(envelope, internal)
    stopped = [
        {
            "activity_ref": activity["activity_ref"],
            "planned_schedule_ref": internal["schedule_ref"],
            "started_at": at(18, 10),
            "ended_at": at(18, 12),
        }
    ]
    assert names(build_panel([activity], at(18, 12), "UTC", stopped)) == [
        "Sessione attività",
    ]


def test_old_stopped_execution_does_not_hide_new_unrelated_interval() -> None:
    first = schedule("interval", at(9), at(10))
    second = schedule("interval", at(18), at(19))
    named = schedule()
    activity = owner(first, second, named)
    stopped = [
        {
            "activity_ref": activity["activity_ref"],
            "planned_schedule_ref": None,
            "started_at": at(9, 10),
            "ended_at": at(9, 30),
        }
    ]
    assert names(build_panel([activity], at(9, 30), "UTC", stopped)) == []
    assert names(build_panel([activity], at(18), "UTC", stopped)) == [
        "Sessione attività",
        "Ripasso",
    ]

    stopped_named = [{**stopped[0], "planned_schedule_ref": named["schedule_ref"]}]
    assert names(build_panel([activity], at(9, 30), "UTC", stopped_named)) == ["Sessione attività"]
    assert names(build_panel([activity], at(18), "UTC", stopped_named)) == [
        "Sessione attività",
        "Ripasso",
    ]


def test_early_stopped_attempt_does_not_reappear_at_planned_start() -> None:
    interval = schedule("interval", at(10), at(10, 30))
    internal = schedule(start=at(10), end=at(10, 30))
    activity = owner(interval, internal)
    early = [
        {
            "activity_ref": activity["activity_ref"],
            "planned_schedule_ref": ref,
            "started_at": at(9, 49),
            "ended_at": at(9, 51),
        }
        for ref in (None, internal["schedule_ref"])
    ]
    assert build_panel([activity], at(10), "UTC", early).groups == []
