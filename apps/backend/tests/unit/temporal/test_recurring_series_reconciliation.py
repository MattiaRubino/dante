"""Clean future plans can change cadence without erasing local history."""

from dataclasses import replace
from datetime import UTC, date, datetime, time
from uuid import UUID

import pytest

from dante.modules.temporal.occurrence import CalendarCoordinate
from dante.modules.temporal.occurrence_edit_scope import (
    RecurrenceEditCandidate,
    select_recurrence_edit_scope,
)
from dante.modules.temporal.recurring_series_reconciliation import (
    MaterializedSeriesInstance,
    SeriesReconciliationError,
    reconcile_materialized_series,
)

SOURCE, FIRST, LOCAL, CLEAN = (UUID(int=n) for n in (1, 11, 12, 13))


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
        authoritative_inventory=True,
    )
    assert result.superseded_occurrence_refs == (CLEAN,)
    assert result.protected_occurrence_refs == (LOCAL,)


@pytest.mark.parametrize(("recorded", "day"), [(False, 21), (True, 20)])
def test_new_cadence_cannot_merge_into_unchanged_instance(recorded: bool, day: int) -> None:
    with pytest.raises(SeriesReconciliationError, match="unchanged instance"):
        reconcile_materialized_series(
            scope=_scope(recorded=recorded),
            materialized=_materialized(),
            regenerated=(_coordinate(day),),
            authoritative_inventory=True,
        )


def test_incomplete_or_duplicate_inventory_is_rejected() -> None:
    with pytest.raises(SeriesReconciliationError, match="complete source inventory"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(),
            authoritative_inventory=False,
        )
    with pytest.raises(SeriesReconciliationError, match="disagree"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized()[:2],
            regenerated=(),
            authoritative_inventory=True,
        )
    with pytest.raises(SeriesReconciliationError, match="duplicate coordinate"):
        reconcile_materialized_series(
            scope=_scope(),
            materialized=_materialized(),
            regenerated=(_coordinate(20), _coordinate(20)),
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
        authoritative_inventory=True,
    )
    assert result.retained_occurrence_refs == ()
    assert result.superseded_occurrence_refs == (FIRST,)
    assert result.new_coordinates == (later,)
