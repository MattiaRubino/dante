"""Untimed recurring Session templates preserve an unplaced planned row."""

from typing import cast
from uuid import UUID

import pytest

from dante.modules.temporal.occurrence import CalendarCoordinate, OccurrenceInputError
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)


def test_untimed_planned_session_has_no_invented_clock() -> None:
    occurrence = UUID("0199a111-1111-7111-8111-111111111111")
    coordinate = cast(CalendarCoordinate, None)
    assert (
        RoutineOccurrenceMaterializationApplication._planned_template_window(
            occurrence, coordinate, {"name": "Cernita", "time_enabled": False}
        )
        is None
    )
    with pytest.raises(OccurrenceInputError):
        RoutineOccurrenceMaterializationApplication._planned_template_window(
            occurrence, coordinate, {"name": "", "time_enabled": False}
        )
