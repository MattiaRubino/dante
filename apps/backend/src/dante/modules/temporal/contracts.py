"""Typed temporal Timeline read contracts for the first real-data spine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Final

from dante.platform.database.references import NativeRef

MAX_TIMELINE_WINDOW_DAYS: Final[int] = 62


class TimelineWindowValidationError(ValueError):
    """Requested Timeline window violates the bounded read contract."""


@dataclass(frozen=True, slots=True)
class TimelineWindowQuery:
    """One half-open local-date Timeline read request."""

    start_date: date
    end_date_exclusive: date

    def __post_init__(self) -> None:
        if self.end_date_exclusive <= self.start_date:
            raise TimelineWindowValidationError(
                "Timeline window end_date_exclusive must be after start_date"
            )
        if (self.end_date_exclusive - self.start_date).days > MAX_TIMELINE_WINDOW_DAYS:
            raise TimelineWindowValidationError(
                f"Timeline window cannot exceed {MAX_TIMELINE_WINDOW_DAYS} local days"
            )


@dataclass(frozen=True, slots=True)
class EmptyTimelineWindow:
    """Truthful B00 read result while no temporal projection family is activated yet."""

    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    self_person_ref: NativeRef
