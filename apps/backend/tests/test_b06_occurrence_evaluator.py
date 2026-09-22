"""B06-C deterministic bounded Occurrence evaluator proof."""

from datetime import UTC, date, datetime, time
from decimal import Decimal
from uuid import UUID

import pytest

from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    CyclicCoordinate,
    ElapsedCoordinate,
    OccurrenceCheckpointLimitError,
    OccurrenceInputError,
    QuotaCoordinate,
    RecurrenceHistoryEntry,
    _normalize_exclusion_coordinate,
    evaluate_recurrence_history,
)
from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    CyclicRecurrence,
    ElapsedRecurrence,
    QuotaRecurrence,
)

_OLD = UUID("0199f100-0000-7000-8000-000000000001")
_NEW = UUID("0199f100-0000-7000-8000-000000000002")


def _history(state_ref: UUID, recurrence: object, accepted: int) -> RecurrenceHistoryEntry:
    return RecurrenceHistoryEntry(
        material_state_ref=state_ref,
        current_from_at=datetime(2026, 1, accepted, tzinfo=UTC),
        current_until_at=None,
        recurrence=recurrence,  # type: ignore[arg-type]
    )


def _daily(*, effective_from: date, wall_time: time | None = None) -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=effective_from,
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="floating_local",
        zone_id=None,
        pattern_anchor_date=None,
        wall_times=(() if wall_time is None else (wall_time,)),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy=None,
        ambiguous_local_time_policy=None,
    )


def test_future_revision_supersedes_virtual_old_state_at_effective_boundary() -> None:
    result = evaluate_recurrence_history(
        (
            _history(_OLD, _daily(effective_from=date(2026, 1, 1)), 1),
            _history(_NEW, _daily(effective_from=date(2026, 1, 5)), 2),
        ),
        start_date=date(2026, 1, 1),
        end_date_exclusive=date(2026, 1, 8),
        effective_zone_id="Europe/Rome",
    )

    assert [item.governing_recurrence_state_ref for item in result] == [
        _OLD,
        _OLD,
        _OLD,
        _OLD,
        _NEW,
        _NEW,
        _NEW,
    ]


def test_revision_boundary_uses_checkpoint_zone_for_named_calendar_candidate() -> None:
    old = CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 1, 2),
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        pattern_anchor_date=None,
        wall_times=(time(0, 30),),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy="skip_civil_candidate",
        ambiguous_local_time_policy="earlier",
    )
    new = _daily(effective_from=date(2026, 1, 2), wall_time=time(9))

    result = evaluate_recurrence_history(
        (
            _history(_OLD, old, 1),
            _history(_NEW, new, 2),
        ),
        start_date=date(2026, 1, 1),
        end_date_exclusive=date(2026, 1, 3),
        effective_zone_id="America/New_York",
    )

    assert [item.governing_recurrence_state_ref for item in result] == [_OLD, _NEW]


def test_named_zone_gap_skips_candidate_and_overlap_selects_exactly_one_instant() -> None:
    def named(day: date, policy: str) -> CalendarRecurrence:
        return CalendarRecurrence(
            family_code="calendar_wall_clock",
            range_kind="expected_count",
            expected_occurrence_count=1,
            effective_from=day,
            effective_until=None,
            pattern_code="daily",
            interval_count=1,
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            pattern_anchor_date=None,
            wall_times=(time(2, 30),),
            weekdays=(),
            month_days=(),
            ordinal_weekdays=(),
            year_month_days=(),
            nonexistent_local_time_policy="skip_civil_candidate",
            ambiguous_local_time_policy=policy,  # type: ignore[arg-type]
        )

    gap = evaluate_recurrence_history(
        (_history(_OLD, named(date(2026, 3, 29), "earlier"), 1),),
        start_date=date(2026, 3, 29),
        end_date_exclusive=date(2026, 3, 30),
        effective_zone_id="Europe/Rome",
    )
    earlier = evaluate_recurrence_history(
        (_history(_OLD, named(date(2026, 10, 25), "earlier"), 1),),
        start_date=date(2026, 10, 25),
        end_date_exclusive=date(2026, 10, 26),
        effective_zone_id="Europe/Rome",
    )
    later = evaluate_recurrence_history(
        (_history(_NEW, named(date(2026, 10, 25), "later"), 1),),
        start_date=date(2026, 10, 25),
        end_date_exclusive=date(2026, 10, 26),
        effective_zone_id="Europe/Rome",
    )

    assert gap == ()
    assert len(earlier) == len(later) == 1
    earlier_coordinate = earlier[0].coordinate
    later_coordinate = later[0].coordinate
    assert isinstance(earlier_coordinate, CalendarCoordinate)
    assert isinstance(later_coordinate, CalendarCoordinate)
    assert earlier_coordinate.resolved_at == datetime(2026, 10, 25, 0, 30, tzinfo=UTC)
    assert later_coordinate.resolved_at == datetime(2026, 10, 25, 1, 30, tzinfo=UTC)


def test_quota_emits_flexible_period_identity_without_invented_slot_time() -> None:
    recurrence = QuotaRecurrence(
        family_code="quota_per_period",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 9, 21),
        effective_until=None,
        quota_count=3,
        period_unit_code="week",
        period_span=1,
        frame_code="floating_local",
        zone_id=None,
        week_start=1,
        pattern_anchor_date=None,
    )
    result = evaluate_recurrence_history(
        (_history(_OLD, recurrence, 1),),
        start_date=date(2026, 9, 21),
        end_date_exclusive=date(2026, 9, 28),
        effective_zone_id="Europe/Rome",
    )

    assert len(result) == 3
    assert all(isinstance(item.coordinate, QuotaCoordinate) for item in result)
    assert {
        item.coordinate.period_start_date
        for item in result
        if isinstance(item.coordinate, QuotaCoordinate)
    } == {date(2026, 9, 21)}


def test_dense_elapsed_checkpoint_fails_atomically_before_persistence() -> None:
    recurrence = ElapsedRecurrence(
        family_code="elapsed_interval",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=datetime(2026, 9, 22, tzinfo=UTC),
        effective_until=None,
        elapsed_seconds=Decimal("0.001"),
        anchor_mode_code="fixed_anchor",
        anchor_at=datetime(2026, 9, 22, tzinfo=UTC),
    )
    with pytest.raises(OccurrenceCheckpointLimitError, match="10,000"):
        evaluate_recurrence_history(
            (_history(_OLD, recurrence, 1),),
            start_date=date(2026, 9, 22),
            end_date_exclusive=date(2026, 9, 23),
            effective_zone_id="UTC",
        )


def test_checkpoint_range_is_half_open_and_capped_at_62_days() -> None:
    result = evaluate_recurrence_history(
        (_history(_OLD, _daily(effective_from=date(2026, 1, 1)), 1),),
        start_date=date(2026, 1, 1),
        end_date_exclusive=date(2026, 1, 3),
        effective_zone_id="UTC",
    )
    assert [
        item.coordinate.generated_date
        for item in result
        if isinstance(item.coordinate, CalendarCoordinate)
    ] == [date(2026, 1, 1), date(2026, 1, 2)]

    with pytest.raises(OccurrenceInputError, match="1 to 62"):
        evaluate_recurrence_history(
            (_history(_OLD, _daily(effective_from=date(2026, 1, 1)), 1),),
            start_date=date(2026, 1, 1),
            end_date_exclusive=date(2026, 3, 5),
            effective_zone_id="UTC",
        )


def test_elapsed_coordinate_starts_after_anchor_and_is_absolute_not_wall_clock() -> None:
    recurrence = ElapsedRecurrence(
        family_code="elapsed_interval",
        range_kind="expected_count",
        expected_occurrence_count=2,
        effective_from=datetime(2026, 10, 25, 0, 30, tzinfo=UTC),
        effective_until=None,
        elapsed_seconds=Decimal("3600"),
        anchor_mode_code="fixed_anchor",
        anchor_at=datetime(2026, 10, 25, 0, 30, tzinfo=UTC),
    )
    result = evaluate_recurrence_history(
        (_history(_OLD, recurrence, 1),),
        start_date=date(2026, 10, 25),
        end_date_exclusive=date(2026, 10, 26),
        effective_zone_id="Europe/Rome",
    )
    instants = [
        item.coordinate.expected_at
        for item in result
        if isinstance(item.coordinate, ElapsedCoordinate)
    ]
    assert instants == [
        datetime(2026, 10, 25, 1, 30, tzinfo=UTC),
        datetime(2026, 10, 25, 2, 30, tzinfo=UTC),
    ]


def test_absolute_calendar_coordinate_is_filtered_in_effective_timezone() -> None:
    recurrence = CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 10, 25),
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="absolute_utc",
        zone_id=None,
        pattern_anchor_date=None,
        wall_times=(time(23, 30),),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy=None,
        ambiguous_local_time_policy=None,
    )
    history = (_history(_OLD, recurrence, 1),)

    assert (
        evaluate_recurrence_history(
            history,
            start_date=date(2026, 10, 25),
            end_date_exclusive=date(2026, 10, 26),
            effective_zone_id="Europe/Rome",
        )
        == ()
    )
    next_day = evaluate_recurrence_history(
        history,
        start_date=date(2026, 10, 26),
        end_date_exclusive=date(2026, 10, 27),
        effective_zone_id="Europe/Rome",
    )
    assert [
        item.coordinate.generated_date
        for item in next_day
        if isinstance(item.coordinate, CalendarCoordinate)
    ] == [date(2026, 10, 25)]


def test_cyclic_expected_count_preserves_position_and_half_open_window() -> None:
    recurrence = CyclicRecurrence(
        family_code="cyclic_positional",
        range_kind="expected_count",
        expected_occurrence_count=3,
        effective_from=date(2026, 11, 2),
        effective_until=None,
        cycle_length=3,
        position_unit_code="day",
        pattern_anchor_date=date(2026, 11, 1),
        generates_expected=(True, False, True),
    )

    result = evaluate_recurrence_history(
        (_history(_OLD, recurrence, 1),),
        start_date=date(2026, 11, 2),
        end_date_exclusive=date(2026, 11, 8),
        effective_zone_id="UTC",
    )

    coordinates = [
        item.coordinate for item in result if isinstance(item.coordinate, CyclicCoordinate)
    ]
    assert [(item.generated_date, item.position_index) for item in coordinates] == [
        (date(2026, 11, 3), 2),
        (date(2026, 11, 4), 0),
        (date(2026, 11, 6), 2),
    ]


def test_structural_exclusion_requires_absolute_elapsed_coordinate() -> None:
    with pytest.raises(OccurrenceInputError, match="absolute instant"):
        _normalize_exclusion_coordinate(
            ElapsedCoordinate(
                family_code="elapsed_interval",
                expected_at=datetime(2026, 11, 2, 9),
            )
        )


@pytest.mark.parametrize(
    "coordinate",
    [
        CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=date(2026, 10, 25),
            generated_wall_time=time(2, 30),
            clock_basis_code="named_zone",
            zone_id=None,
            resolved_at=None,
        ),
        CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=date(2026, 10, 25),
            generated_wall_time=time(2, 30),
            clock_basis_code="floating_local",
            zone_id="Europe/Rome",
            resolved_at=None,
        ),
        CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=date(2026, 10, 25),
            generated_wall_time=time(2, 30),
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            resolved_at=datetime(2026, 10, 25, 2, 30),
        ),
        CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=date(2026, 10, 25),
            generated_wall_time=time(2, 30),
            clock_basis_code="named_zone",
            zone_id="Europe/Rome",
            resolved_at=datetime(2026, 10, 25, 3, 30, tzinfo=UTC),
        ),
    ],
)
def test_structural_exclusion_rejects_incoherent_calendar_coordinate(
    coordinate: CalendarCoordinate,
) -> None:
    with pytest.raises(OccurrenceInputError):
        _normalize_exclusion_coordinate(coordinate)


def test_structural_exclusion_normalizes_valid_overlap_to_civil_identity() -> None:
    coordinate = CalendarCoordinate(
        family_code="calendar_wall_clock",
        generated_date=date(2026, 10, 25),
        generated_wall_time=time(2, 30),
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        resolved_at=datetime(2026, 10, 25, 0, 30, tzinfo=UTC),
    )

    normalized = _normalize_exclusion_coordinate(coordinate)

    assert isinstance(normalized, CalendarCoordinate)
    assert normalized.resolved_at is None


def test_structural_exclusion_rejects_negative_cycle_position() -> None:
    with pytest.raises(OccurrenceInputError, match="zero or greater"):
        _normalize_exclusion_coordinate(
            CyclicCoordinate(
                family_code="cyclic_positional",
                generated_date=date(2026, 11, 2),
                position_index=-1,
            )
        )
