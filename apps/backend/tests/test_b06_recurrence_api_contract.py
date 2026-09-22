"""Offline B06-B transport validation contracts."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from dante.modules.temporal.recurrence_api import CalendarOrdinalWeekday, CalendarYearMonthDay


@pytest.mark.parametrize(
    ("model", "payload"),
    [
        (CalendarOrdinalWeekday, {"weekday_number": 1, "ordinal": 0}),
        (CalendarYearMonthDay, {"month_number": 1, "month_day": 0}),
    ],
)
def test_calendar_positional_values_reject_zero(model: type[BaseModel], payload: dict[str, int]) -> None:
    with pytest.raises(ValidationError, match="must not be zero"):
        model(**payload)
