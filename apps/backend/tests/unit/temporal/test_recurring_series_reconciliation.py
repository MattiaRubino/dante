"""Clean future plans can change cadence without erasing local history."""

from dataclasses import replace
from datetime import UTC, date, datetime, time
from uuid import UUID

import pytest

from dante.modules.temporal.occurrence import CalendarCoordinate, OccurrenceView
from dante.modules.temporal.occurrence_edit_inventory import OccurrenceEditInventory
from dante.modules.temporal.occurrence_edit_scope import (
    RecurrenceEditCandidate,
    select_recurrence_edit_scope,
)
from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_structure_preview import (
    StructuralSeriesPreviewConflict,
    structural_scope,
)
from dante.modules.temporal.recurring_series_reconciliation import (
    MaterializedSeriesInstance,
    SeriesReconciliationError,
    SeriesReconciliationWindow,
    preview_calendar_series_reconciliation,
    reconcile_materialized_series,
)

SOURCE, FIRST, LOCAL, CLEAN = (UUID(int=n) for n in (1, 11, 12, 13))
WINDOW = SeriesReconciliationWindow(date(2026, 10, 19), date(2026, 10, 29))


def _coordinate(day: int) -> CalendarCoordinate:
    return CalendarCoordinate(
        family_code="calendar_wall_clock",
        generated_date=date(2026, 10, day),
        generated_wall_time=time(10),
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        resolved_at=datetime(2026, 10, day, 8, tzinfo=UTC),
    )


def _scope(*, recorded: bool = False):
    return select_recurrence_edit_scope(
        selected_occurrence_ref=FIRST,
        scope="from_next" if recorded else "this_and_following",
        candidates=tuple(
            RecurrenceEditCandidate(
                occurrence_ref=ref,
                source_native_ref=SOURCE,
                expected_at=datetime(2026, 10, day, 8, tzinfo=UTC),
                origin_code="recurrence_generated",
                has_recorded_facts=recorded and ref == FIRST,
                has_override=ref == LOCAL,
            )
            for ref, day in ((FIRST, 20), (LOCAL, 21), (CLEAN, 22))
        ),
        captured_at=datetime(2026, 10, 19, 8, tzinfo=UTC),
        authoritative_inventory=True,
    )


def _materialized() -> tuple[MaterializedSeriesInstance, ...]:
    return tuple(
        MaterializedSeriesInstance(ref, _coordinate(day))
        for ref, day in ((FIRST, 20), (LOCAL, 21), (CLEAN, 22))
    )


def test_revising_cadence_preserves_local_exception_and_replaces_clean_instance() -> None:
    result = reconcile_materialized_series(
        scope=_scope(),
        materialized=_materialized(),
        regenerated=(_coordinate(20), _coordinate(27)),
        window=WINDOW,
        effective_zone_id="Europe/Rome",
        authoritative_inventory=True,
    )
    assert result.retained_occurrence_refs == (FIRST,)
    assert result.superseded_occurrence_refs == (CLEAN,)
    assert result.protected_occurrence_refs == (LOCAL,)
    assert result.new_coordinates == (_coordinate(27),)


def test_recorded_selected_instance_is_not_replaced() -> None:
    result = reconcile_materialized_series(
        scope=_scope(recorded=True),
        materialized=_materialized(),
        regenerated=(_coordinate(27),),
        window=WINDOW,
        effective_zone_id="Europe/Rome",
        authoritative_inventory=True,
    )
    assert result.superseded_occurrence_refs == (CLEAN,)
    assert result.protected_occurrence_refs == (LOCAL,)


def test_protected_coordinate_is_consumed_without_replacing_its_instance() -> None:
    result = reconcile_materialized_series(
        scope=_scope(),
        materialized=_materialized(),
        regenerated=(_coordinate(20), _coordinate(21), _coordinate(27)),
        window=WINDOW,
        effective_zone_id="Europe/Rome",
        authoritative_inventory=True,
    )
    assert result.retained_occurrence_refs == (FIRST,)
    assert result.superseded_occurrence_refs == (CLEAN,)
    assert result.protected_occurrence_refs == (LOCAL,)
    assert result.new_coordinates == (_coordinate(27),)


def test_incomplete_or_duplicate_inventory_is_rejected() -> None:
    with pytest.raises(SeriesReconciliationError, match="complete source inventory"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=False,
        )
    with pytest.raises(SeriesReconciliationError, match="disagree"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized()[:2],
            regenerated=(),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )
    with pytest.raises(SeriesReconciliationError, match="duplicate coordinate"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(_coordinate(20), _coordinate(20)),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_dst_overlap_resolution_changes_occurrence_identity() -> None:
    earlier = CalendarCoordinate(
        family_code="calendar_wall_clock",
        generated_date=date(2026, 10, 25),
        generated_wall_time=time(2, 30),
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        resolved_at=datetime(2026, 10, 25, 0, 30, tzinfo=UTC),
    )
    later = replace(earlier, resolved_at=datetime(2026, 10, 25, 1, 30, tzinfo=UTC))
    scope = select_recurrence_edit_scope(
        selected_occurrence_ref=FIRST,
        scope="this_and_following",
        candidates=(
            RecurrenceEditCandidate(
                occurrence_ref=FIRST,
                source_native_ref=SOURCE,
                expected_at=earlier.resolved_at,
                origin_code="recurrence_generated",
            ),
        ),
        captured_at=datetime(2026, 10, 24, tzinfo=UTC),
        authoritative_inventory=True,
    )
    result = reconcile_materialized_series(
        scope=scope,
        materialized=(MaterializedSeriesInstance(FIRST, earlier),),
        regenerated=(later,),
        window=SeriesReconciliationWindow(date(2026, 10, 25), date(2026, 10, 26)),
        effective_zone_id="Europe/Rome",
        authoritative_inventory=True,
    )
    assert result.retained_occurrence_refs == ()
    assert result.superseded_occurrence_refs == (FIRST,)
    assert result.new_coordinates == (later,)


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (date(2026, 10, 20), date(2026, 10, 20)),
        (date(2026, 10, 21), date(2026, 10, 20)),
    ],
)
def test_reconciliation_rejects_empty_or_backward_window(start: date, end: date) -> None:
    with pytest.raises(SeriesReconciliationError, match="horizon"):
        SeriesReconciliationWindow(start, end)


def test_reconciliation_rejects_materialized_occurrence_outside_complete_horizon() -> None:
    with pytest.raises(SeriesReconciliationError, match="Source inventory escapes"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(_coordinate(27),),
            window=SeriesReconciliationWindow(date(2026, 10, 20), date(2026, 10, 22)),
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_reconciliation_rejects_new_candidate_outside_horizon() -> None:
    with pytest.raises(SeriesReconciliationError, match="Regenerated cadence escapes"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(_coordinate(30),),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_reconciliation_fails_closed_when_materialized_inventory_exceeds_limit() -> None:
    with pytest.raises(SeriesReconciliationError, match="bounded instance limit"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized() * 3334,
            regenerated=(),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_reconciliation_fails_closed_when_proposed_cadence_exceeds_limit() -> None:
    with pytest.raises(SeriesReconciliationError, match="bounded instance limit"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(_coordinate(27),) * 10001,
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def _weekly_tuesday() -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 10, 20),
        effective_until=None,
        pattern_code="weekly_weekdays",
        interval_count=1,
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        pattern_anchor_date=None,
        wall_times=(time(10),),
        weekdays=(2,),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy="skip_civil_candidate",
        ambiguous_local_time_policy="earlier",
    )


def test_calendar_preview_reconciles_weekly_cadence_without_touching_local_edit() -> None:
    result = preview_calendar_series_reconciliation(
        scope=_scope(),
        materialized=_materialized(),
        proposed_recurrence=_weekly_tuesday(),
        window=WINDOW,
        effective_zone_id="Europe/Rome",
        authoritative_inventory=True,
    )
    assert result.retained_occurrence_refs == (FIRST,)
    assert result.superseded_occurrence_refs == (CLEAN,)
    assert result.protected_occurrence_refs == (LOCAL,)
    assert [value.generated_date for value in result.new_coordinates] == [date(2026, 10, 27)]
    assert [value.resolved_at for value in result.new_coordinates] == [
        datetime(2026, 10, 27, 9, tzinfo=UTC)
    ]


def test_calendar_preview_starts_after_recorded_selected_instance() -> None:
    result = preview_calendar_series_reconciliation(
        scope=_scope(recorded=True),
        materialized=_materialized(),
        proposed_recurrence=_weekly_tuesday(),
        window=WINDOW,
        effective_zone_id="Europe/Rome",
        authoritative_inventory=True,
    )
    assert FIRST not in result.superseded_occurrence_refs
    assert result.protected_occurrence_refs == (LOCAL,)
    assert result.superseded_occurrence_refs == (CLEAN,)
    assert len(result.new_coordinates) == 1


def test_calendar_preview_cannot_rewrite_a_past_selected_anchor() -> None:
    with pytest.raises(SeriesReconciliationError, match="past anchor"):
        preview_calendar_series_reconciliation(
            scope=replace(_scope(), captured_at=datetime(2026, 10, 22, 8, tzinfo=UTC)),
            materialized=_materialized(),
            proposed_recurrence=_weekly_tuesday(),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_calendar_preview_does_not_grant_write_with_partial_inventory() -> None:
    with pytest.raises(SeriesReconciliationError, match="complete source inventory"):
        preview_calendar_series_reconciliation(
            scope=_scope(),
            materialized=_materialized(),
            proposed_recurrence=_weekly_tuesday(),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=False,
        )


def test_calendar_preview_rejects_incomplete_scope_before_generation() -> None:
    with pytest.raises(SeriesReconciliationError, match="complete source inventory"):
        preview_calendar_series_reconciliation(
            scope=_scope(),
            materialized=_materialized(),
            proposed_recurrence=_weekly_tuesday(),
            window=WINDOW,
            effective_zone_id="Invalid/Zone",
            authoritative_inventory=False,
        )


def test_calendar_preview_never_allows_local_only_scope_to_revise_source() -> None:
    local = replace(_scope(), scope="only_this", update_future_source_template=False)
    with pytest.raises(SeriesReconciliationError, match="following scope"):
        preview_calendar_series_reconciliation(
            scope=local,
            materialized=_materialized(),
            proposed_recurrence=_weekly_tuesday(),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_calendar_preview_refuses_generator_truncation_before_cutover() -> None:
    selected = CalendarCoordinate(
        family_code="calendar_wall_clock",
        generated_date=date(2024, 1, 1),
        generated_wall_time=time(10),
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        resolved_at=datetime(2024, 1, 1, 9, tzinfo=UTC),
    )
    scope = select_recurrence_edit_scope(
        selected_occurrence_ref=FIRST,
        scope="this_and_following",
        candidates=(
            RecurrenceEditCandidate(
                occurrence_ref=FIRST,
                source_native_ref=SOURCE,
                expected_at=selected.resolved_at,
                origin_code="recurrence_generated",
            ),
        ),
        captured_at=datetime(2023, 12, 31, tzinfo=UTC),
        authoritative_inventory=True,
    )
    recurrence = replace(
        _weekly_tuesday(),
        effective_from=date(2020, 1, 1),
        pattern_code="daily",
        weekdays=(),
        wall_times=tuple(time(hour, minute) for hour in range(8) for minute in (0, 30)),
    )
    with pytest.raises(SeriesReconciliationError, match="bounded instance limit"):
        preview_calendar_series_reconciliation(
            scope=scope,
            materialized=(MaterializedSeriesInstance(FIRST, selected),),
            proposed_recurrence=recurrence,
            window=SeriesReconciliationWindow(date(2020, 1, 1), date(2025, 1, 1)),
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_cadence_reconciliation_refuses_new_expected_instance_before_selected_boundary() -> None:
    with pytest.raises(SeriesReconciliationError, match="edit boundary"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(_coordinate(19),),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def test_cadence_reconciliation_refuses_post_preview_cutover_backfill() -> None:
    scope = replace(
        _scope(recorded=True),
        captured_at=datetime(2026, 10, 23, 8, tzinfo=UTC),
    )
    with pytest.raises(SeriesReconciliationError, match="edit boundary"):
        reconcile_materialized_series(
            scope=scope,
            materialized=_materialized(),
            regenerated=(_coordinate(19),),
            window=WINDOW,
            effective_zone_id="Europe/Rome",
            authoritative_inventory=True,
        )


def _structural_inventory() -> OccurrenceEditInventory:
    return OccurrenceEditInventory(
        selected_occurrence_ref=FIRST,
        source_native_ref=SOURCE,
        captured_at=datetime(2026, 10, 19, 8, tzinfo=UTC),
        occurrences=tuple(
            OccurrenceView(
                occurrence_ref=ref,
                source_native_ref=SOURCE,
                governing_recurrence_state_ref=None,
                origin_code="recurrence_generated",
                coordinate=_coordinate(day),
                skipped=False,
                skip_reason=None,
                skipped_at=None,
            )
            for ref, day in ((FIRST, 20), (LOCAL, 21), (CLEAN, 22))
        ),
    )


def test_structural_preview_classifies_canonical_local_exceptions() -> None:
    scope, generated = structural_scope(
        inventory=_structural_inventory(),
        protections={FIRST: None, LOCAL: "legacy_unknown", CLEAN: None},
        scope_code="this_and_following",
        effective_zone_id="Europe/Rome",
    )
    assert len(generated) == 3
    assert scope.target_occurrence_refs == (FIRST, CLEAN)
    assert scope.protected_future_occurrence_refs == (LOCAL,)
    assert scope.protected_future_reasons == ((LOCAL, "local_change"),)


def test_structural_preview_refuses_incomplete_protection_snapshot() -> None:
    with pytest.raises(StructuralSeriesPreviewConflict, match="incomplete"):
        structural_scope(
            inventory=_structural_inventory(),
            protections={FIRST: None, CLEAN: None},
            scope_code="this_and_following",
            effective_zone_id="Europe/Rome",
        )


def test_structural_preview_from_next_preserves_recorded_selected() -> None:
    scope, _ = structural_scope(
        inventory=_structural_inventory(),
        protections={FIRST: "registration", LOCAL: "local_change", CLEAN: None},
        scope_code="from_next",
        effective_zone_id="Europe/Rome",
    )
    assert scope.target_occurrence_refs == (CLEAN,)
    assert scope.protected_future_occurrence_refs == (LOCAL,)
