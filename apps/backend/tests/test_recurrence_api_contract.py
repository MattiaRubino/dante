"""Offline B06-B transport validation contracts."""

from __future__ import annotations

from uuid import UUID

import pytest
from pydantic import BaseModel, ValidationError

from dante.modules.temporal.recurrence import RecurrenceView
from dante.modules.temporal.recurrence_api import (
    CalendarOrdinalWeekday,
    CalendarRecurrenceRequest,
    CalendarYearMonthDay,
    _spec,
    _state,
)


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        (CalendarOrdinalWeekday, {"weekday_number": 1, "ordinal": 0}),
        (CalendarYearMonthDay, {"month_number": 1, "month_day": 0}),
    ],
)
def test_calendar_positional_values_reject_zero(
    model: type[BaseModel], payload: dict[str, int]
) -> None:
    with pytest.raises(ValidationError, match="must not be zero"):
        model(**payload)


@pytest.mark.parametrize(
    ("extra", "expected_field", "expected_value"),
    [
        pytest.param(
            {
                "pattern_code": "monthly_ordinal_weekdays",
                "ordinal_weekdays": [{"weekday_number": 3, "ordinal": 1}],
            },
            "ordinal_weekdays",
            [{"weekday_number": 3, "ordinal": 1}],
            id="monthly-ordinal",
        ),
        pytest.param(
            {
                "pattern_code": "yearly_month_days",
                "year_month_days": [{"month_number": 2, "month_day": 29}],
            },
            "year_month_days",
            [{"month_number": 2, "month_day": 29}],
            id="yearly-month-day",
        ),
    ],
)
def test_recurrence_read_serializes_positional_coordinates_as_named_fields(
    extra: dict[str, object], expected_field: str, expected_value: list[dict[str, int]]
) -> None:
    payload = CalendarRecurrenceRequest.model_validate(
        {
            "range_kind": "open",
            "effective_from": "2026-11-11",
            "interval_count": 1,
            "clock_basis_code": "named_zone",
            "zone_id": "Europe/Rome",
            "wall_times": ["09:00:00"],
            **extra,
        }
    )
    state = _state(
        RecurrenceView(
            material_state_ref=UUID("0199a111-1111-7111-8111-111111111111"),
            recurrence=_spec(payload),
        )
    ).model_dump(mode="json")
    assert state["recurrence"][expected_field] == expected_value
