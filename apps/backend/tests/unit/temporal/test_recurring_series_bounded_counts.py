"""Finite calendar series must retain the original end under partial edits."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, time

import pytest

from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_series_edit import (
    SeriesReconciliationError,
    _remaining_expected_calendar_counts,
)


def _weekly() -> CalendarRecurrence:
    first = date(2026, 11, 15)
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="expected_count",
        expected_occurrence_count=5,
        effective_from=first,
        effective_until=None,
        pattern_code="weekly_weekdays",
        interval_count=2,
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        pattern_anchor_date=first,
        wall_times=(time(9, 20),),
        weekdays=(7,),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy="skip_civil_candidate",
        ambiguous_local_time_policy="earlier",
        step_unit_code=None,
    )


@pytest.mark.parametrize(
    ("selected", "including", "after"),
    [
        (date(2026, 11, 15), 5, 4),
        (date(2026, 11, 29), 4, 3),
        (date(2026, 12, 13), 3, 2),
        (date(2026, 12, 27), 2, 1),
        (date(2027, 1, 10), 1, 0),
    ],
)
def test_biweekly_finite_series_preserves_last_day(
    selected: date, including: int, after: int
) -> None:
    assert _remaining_expected_calendar_counts(_weekly(), selected) == (
        including,
        after,
    )


def test_multiple_wall_times_on_selected_day_are_excluded_together() -> None:
    recurrence = replace(
        _weekly(),
        pattern_code="daily",
        interval_count=1,
        pattern_anchor_date=None,
        weekdays=(),
        expected_occurrence_count=6,
        wall_times=(time(9), time(17)),
    )
    assert _remaining_expected_calendar_counts(
        recurrence, date(2026, 11, 16)
    ) == (4, 2)


def test_monthly_ordinal_uses_canonical_calendar_phase() -> None:
    recurrence = replace(
        _weekly(),
        pattern_code="monthly_ordinal_weekdays",
        interval_count=1,
        pattern_anchor_date=None,
        weekdays=(),
        ordinal_weekdays=((7, 3),),
    )
    assert _remaining_expected_calendar_counts(
        recurrence, date(2027, 1, 17)
    ) == (3, 2)


def test_open_series_has_no_bounded_count() -> None:
    assert _remaining_expected_calendar_counts(
        replace(_weekly(), range_kind="open", expected_occurrence_count=None),
        date(2026, 11, 29),
    ) == (None, None)


@pytest.mark.parametrize("selected", [date(2026, 11, 14), date(2026, 11, 16)])
def test_out_of_series_boundary_is_rejected(selected: date) -> None:
    with pytest.raises(SeriesReconciliationError):
        _remaining_expected_calendar_counts(_weekly(), selected)
