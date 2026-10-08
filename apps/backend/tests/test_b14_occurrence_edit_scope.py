"""B14 M1-A selected anchor and protected future recurrence edit targeting."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from dante.modules.temporal.occurrence_edit_scope import (
    EditScopeInputError,
    RecurrenceEditCandidate,
    select_recurrence_edit_scope,
)

SOURCE = UUID("0199a101-0000-7000-8000-000000000001")
OTHER_SOURCE = UUID("0199a101-0000-7000-8000-000000000002")
NOW = datetime(2026, 10, 8, 12, 0, tzinfo=UTC)


def _ref(n: int) -> UUID:
    return UUID(f"0199a101-0000-7000-8000-{n:012d}")


def _occurrence(n: int, *, source: UUID = SOURCE, **kwargs: object) -> RecurrenceEditCandidate:
    dates = {
        1: NOW - timedelta(days=3),
        2: NOW - timedelta(days=2),
        3: NOW - timedelta(days=1),
        4: NOW + timedelta(days=1),
        5: NOW + timedelta(days=2),
        6: NOW + timedelta(days=3),
    }
    return RecurrenceEditCandidate(
        occurrence_ref=_ref(n),
        source_native_ref=source,
        expected_at=dates[n],
        origin_code="recurrence_generated",
        **kwargs,
    )


@pytest.fixture
def timeline() -> tuple[RecurrenceEditCandidate, ...]:
    return tuple(_occurrence(n) for n in range(1, 7))


@pytest.mark.parametrize(
    ("selected", "scope", "expected"),
    [
        (1, "only_this", (1,)),
        (1, "this_and_following", (1, 4, 5, 6)),
        (2, "this_and_following", (2, 4, 5, 6)),
        (4, "only_this", (4,)),
        (4, "this_and_following", (4, 5, 6)),
        (5, "this_and_following", (5, 6)),
        (6, "this_and_following", (6,)),
    ],
)
def test_selected_instance_always_included_without_touching_other_past(
    timeline: tuple[RecurrenceEditCandidate, ...],
    selected: int,
    scope: str,
    expected: tuple[int, ...],
) -> None:
    plan = select_recurrence_edit_scope(
        selected_occurrence_ref=_ref(selected),
        scope=scope,  # type: ignore[arg-type]
        candidates=timeline,
        captured_at=NOW,
        authoritative_inventory=True,
    )
    assert plan.target_occurrence_refs == tuple(_ref(n) for n in expected)
    assert plan.update_future_source_template is (scope == "this_and_following")
    assert plan.can_apply
    if scope == "this_and_following":
        assert _ref(3) not in plan.target_occurrence_refs
    else:
        assert plan.untouched_past_occurrence_refs == ()


def test_past_selection_marks_other_past_as_untouched(
    timeline: tuple[RecurrenceEditCandidate, ...],
) -> None:
    result = select_recurrence_edit_scope(
        selected_occurrence_ref=_ref(1),
        scope="this_and_following",
        candidates=timeline,
        captured_at=NOW,
        authoritative_inventory=True,
    )
    assert result.untouched_past_occurrence_refs == (_ref(2), _ref(3))
    assert result.target_occurrence_refs[0] == _ref(1)


def test_overrides_skip_and_recorded_future_facts_block_propagation() -> None:
    rows = (
        _occurrence(1),
        _occurrence(4, has_override=True),
        _occurrence(5, skipped=True),
        _occurrence(6, has_recorded_facts=True),
    )
    result = select_recurrence_edit_scope(
        selected_occurrence_ref=_ref(1),
        scope="this_and_following",
        candidates=rows,
        captured_at=NOW,
        authoritative_inventory=True,
    )
    assert result.target_occurrence_refs == (_ref(1),)
    assert result.blocked_future_occurrence_refs == (_ref(4), _ref(5), _ref(6))
    assert not result.can_apply


def test_explicit_extra_is_not_a_recurring_successor() -> None:
    extra = RecurrenceEditCandidate(
        occurrence_ref=_ref(5),
        source_native_ref=SOURCE,
        expected_at=None,
        origin_code="explicit_extra",
    )
    rows = (_occurrence(1), _occurrence(4), extra, _occurrence(6))
    result = select_recurrence_edit_scope(
        selected_occurrence_ref=_ref(1),
        scope="this_and_following",
        candidates=rows,
        captured_at=NOW,
        authoritative_inventory=True,
    )
    assert result.target_occurrence_refs == (_ref(1), _ref(4), _ref(6))
    with pytest.raises(EditScopeInputError, match="recurrence-generated anchor"):
        select_recurrence_edit_scope(
            selected_occurrence_ref=_ref(5),
            scope="this_and_following",
            candidates=rows,
            captured_at=NOW,
            authoritative_inventory=True,
        )
    single = select_recurrence_edit_scope(
        selected_occurrence_ref=_ref(5),
        scope="only_this",
        candidates=rows,
        captured_at=NOW,
        authoritative_inventory=False,
    )
    assert single.target_occurrence_refs == (_ref(5),)


@pytest.mark.parametrize("fault", ["missing", "duplicate", "mixed_source", "incomplete"])
def test_fail_closed_on_incomplete_or_cross_source_snapshots(
    timeline: tuple[RecurrenceEditCandidate, ...],
    fault: str,
) -> None:
    cases = {
        "missing": timeline[1:],
        "duplicate": (*timeline, timeline[0]),
        "mixed_source": (*timeline, RecurrenceEditCandidate(
            occurrence_ref=UUID(int=42),
            source_native_ref=OTHER_SOURCE,
            expected_at=NOW + timedelta(days=4),
            origin_code="recurrence_generated",
        )),
        "incomplete": timeline,
    }
    with pytest.raises(EditScopeInputError):
        select_recurrence_edit_scope(
            selected_occurrence_ref=_ref(1),
            scope="this_and_following",
            candidates=cases[fault],
            captured_at=NOW,
            authoritative_inventory=fault != "incomplete",
        )


def test_no_coercion_of_naive_or_ambiguous_wall_clock_times() -> None:
    with pytest.raises(EditScopeInputError, match="resolved aware instant"):
        select_recurrence_edit_scope(
            selected_occurrence_ref=_ref(1),
            scope="this_and_following",
            candidates=(_occurrence(1), _occurrence(4)),
            captured_at=NOW.replace(tzinfo=None),
            authoritative_inventory=True,
        )
    with pytest.raises(EditScopeInputError, match="resolved aware instant"):
        select_recurrence_edit_scope(
            selected_occurrence_ref=_ref(1),
            scope="this_and_following",
            candidates=(
                _occurrence(1),
                RecurrenceEditCandidate(
                    occurrence_ref=_ref(4),
                    source_native_ref=SOURCE,
                    expected_at=NOW.replace(tzinfo=None),
                    origin_code="recurrence_generated",
                ),
            ),
            captured_at=NOW,
            authoritative_inventory=True,
        )


def test_equal_time_anchor_requires_unambiguous_sequence() -> None:
    tied = RecurrenceEditCandidate(
        occurrence_ref=_ref(2),
        source_native_ref=SOURCE,
        expected_at=NOW - timedelta(days=3),
        origin_code="recurrence_generated",
    )
    with pytest.raises(EditScopeInputError, match="Equal-time"):
        select_recurrence_edit_scope(
            selected_occurrence_ref=_ref(1),
            scope="this_and_following",
            candidates=(_occurrence(1), tied, _occurrence(4)),
            captured_at=NOW,
            authoritative_inventory=True,
        )


def test_selected_item_can_be_corrected_despite_its_existing_history() -> None:
    result = select_recurrence_edit_scope(
        selected_occurrence_ref=_ref(1),
        scope="only_this",
        candidates=(_occurrence(1, has_recorded_facts=True, has_override=True),),
        captured_at=NOW,
        authoritative_inventory=False,
    )
    assert result.target_occurrence_refs == (_ref(1),)
    assert not result.update_future_source_template


def test_reject_more_than_10000_candidates() -> None:
    selected = _occurrence(1)
    many = (
        selected,
        *(
            RecurrenceEditCandidate(
                occurrence_ref=UUID(int=n + 1),
                source_native_ref=SOURCE,
                expected_at=NOW + timedelta(days=1),
                origin_code="recurrence_generated",
            )
            for n in range(10_000)
        ),
    )
    with pytest.raises(EditScopeInputError, match="1-10000"):
        select_recurrence_edit_scope(
            selected_occurrence_ref=_ref(1),
            scope="this_and_following",
            candidates=many,
            captured_at=NOW,
            authoritative_inventory=True,
        )
