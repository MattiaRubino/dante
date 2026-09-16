"""Temporal Timeline application boundary over canonical current Schedule state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.context.contracts import DanteContext
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.schedule import CoarseLocalPeriod
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.time import local_day_utc_bounds, validate_iana_timezone


class TimelinePersistenceError(RuntimeError):
    """The canonical Timeline window could not be read safely."""


@dataclass(frozen=True, slots=True)
class _TimelineScheduledActivityBase:
    """Identity shared by every current Activity Schedule projection."""

    activity_ref: NativeRef
    schedule_ref: ScopedRecordRef
    placement_material_state_ref: MaterialStateRef
    title: str


@dataclass(frozen=True, slots=True)
class TimelineDateSpanActivityItem(_TimelineScheduledActivityBase):
    """Finite half-open civil-date placement with no fabricated instants."""

    start_date: date
    end_date_exclusive: date


@dataclass(frozen=True, slots=True)
class TimelineFloatingLocalActivityItem(_TimelineScheduledActivityBase):
    """Offset-free local wall-clock interval."""

    starts_local_at: datetime
    ends_local_at: datetime


@dataclass(frozen=True, slots=True)
class TimelineNamedZoneLocalActivityItem(_TimelineScheduledActivityBase):
    """Named-zone local intent plus retained and viewing-zone projections."""

    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime
    display_starts_local_at: datetime
    display_ends_local_at: datetime


@dataclass(frozen=True, slots=True)
class TimelineAbsoluteActivityItem(_TimelineScheduledActivityBase):
    """Absolute interval plus its request-effective-zone projection."""

    starts_at: datetime
    ends_at: datetime
    display_starts_local_at: datetime
    display_ends_local_at: datetime


@dataclass(frozen=True, slots=True)
class TimelineCoarseLocalPeriodActivityItem(_TimelineScheduledActivityBase):
    """Civil date and bounded coarse period without time-grid geometry."""

    local_date: date
    period: CoarseLocalPeriod


type TimelineScheduledActivityItem = (
    TimelineDateSpanActivityItem
    | TimelineFloatingLocalActivityItem
    | TimelineNamedZoneLocalActivityItem
    | TimelineAbsoluteActivityItem
    | TimelineCoarseLocalPeriodActivityItem
)


@dataclass(frozen=True, slots=True)
class TimelineWindowResult:
    """Authenticated current Timeline read result for one bounded local-date window."""

    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    self_person_ref: NativeRef
    items: tuple[TimelineScheduledActivityItem, ...]


def empty_timeline_window_result(
    *,
    query: TimelineWindowQuery,
    context: DanteContext,
) -> TimelineWindowResult:
    """Build the truthful empty projection used by B00 and empty B02 windows."""
    return TimelineWindowResult(
        start_date=query.start_date,
        end_date_exclusive=query.end_date_exclusive,
        effective_zone_id=context.effective_zone_id,
        self_person_ref=context.self_person_ref,
        items=(),
    )


def _identity(row: RowMapping) -> dict[str, Any]:
    return {
        "activity_ref": NativeRef(UUID(str(row["activity_ref"]))),
        "schedule_ref": ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        "placement_material_state_ref": MaterialStateRef(UUID(str(row["material_state_ref"]))),
        "title": str(row["title"]),
    }


def _view_local(value: datetime, *, zone_id: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timeline instant projection requires an aware timestamp")
    return value.astimezone(validate_iana_timezone(zone_id)).replace(tzinfo=None)


def _item_from_row(
    row: RowMapping,
    *,
    effective_zone_id: str,
) -> TimelineScheduledActivityItem:
    identity = _identity(row)
    temporal_form = str(row["temporal_form_code"])
    if temporal_form == "date_span":
        return TimelineDateSpanActivityItem(
            **identity,
            start_date=row["start_date"],
            end_date_exclusive=row["end_date_exclusive"],
        )
    if temporal_form == "floating_local":
        return TimelineFloatingLocalActivityItem(
            **identity,
            starts_local_at=row["floating_starts_local_at"],
            ends_local_at=row["floating_ends_local_at"],
        )
    if temporal_form == "named_zone_local":
        resolved_start_at = row["resolved_start_at"]
        resolved_end_at = row["resolved_end_at"]
        return TimelineNamedZoneLocalActivityItem(
            **identity,
            starts_local_at=row["named_starts_local_at"],
            ends_local_at=row["named_ends_local_at"],
            zone_id=str(row["zone_id"]),
            resolved_start_at=resolved_start_at,
            resolved_end_at=resolved_end_at,
            display_starts_local_at=_view_local(
                resolved_start_at,
                zone_id=effective_zone_id,
            ),
            display_ends_local_at=_view_local(
                resolved_end_at,
                zone_id=effective_zone_id,
            ),
        )
    if temporal_form == "absolute":
        starts_at = row["starts_at"]
        ends_at = row["ends_at"]
        return TimelineAbsoluteActivityItem(
            **identity,
            starts_at=starts_at,
            ends_at=ends_at,
            display_starts_local_at=_view_local(starts_at, zone_id=effective_zone_id),
            display_ends_local_at=_view_local(ends_at, zone_id=effective_zone_id),
        )
    if temporal_form == "coarse_local_period":
        period = str(row["period_code"])
        if period not in {"morning", "afternoon", "evening"}:
            raise ValueError("Timeline coarse local period is outside the activated vocabulary")
        return TimelineCoarseLocalPeriodActivityItem(
            **identity,
            local_date=row["coarse_local_date"],
            period=cast(CoarseLocalPeriod, period),
        )
    raise ValueError("Timeline placement form is outside the activated projection")


class TemporalTimelineApplication:
    """Read current accepted temporal truth through bounded PostgreSQL queries."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def read_window(
        self,
        *,
        query: TimelineWindowQuery,
        context: DanteContext,
    ) -> TimelineWindowResult:
        """Read every activated current Schedule form in one half-open local-date window."""
        start_local_at = datetime.combine(query.start_date, time.min)
        end_local_at = datetime.combine(query.end_date_exclusive, time.min)
        start_instant, _ = local_day_utc_bounds(
            query.start_date,
            context.effective_zone_id,
        )
        end_instant, _ = local_day_utc_bounds(
            query.end_date_exclusive,
            context.effective_zone_id,
        )
        statement = text(
            """
            SELECT intention.activity_ref,
                   intention.title,
                   schedule.schedule_ref,
                   current.material_state_ref,
                   placement.temporal_form_code,
                   lower(date_payload.date_span) AS start_date,
                   upper(date_payload.date_span) AS end_date_exclusive,
                   floating_payload.starts_local_at AS floating_starts_local_at,
                   floating_payload.ends_local_at AS floating_ends_local_at,
                   named_payload.starts_local_at AS named_starts_local_at,
                   named_payload.ends_local_at AS named_ends_local_at,
                   named_payload.zone_id,
                   named_payload.resolved_start_at,
                   named_payload.resolved_end_at,
                   absolute_payload.starts_at,
                   absolute_payload.ends_at,
                   coarse_payload.local_date AS coarse_local_date,
                   coarse_payload.period_code
              FROM dante.activity_intention AS intention
              JOIN dante.schedule AS schedule
                ON schedule.subject_native_ref = intention.activity_ref
              JOIN dante.schedule_current_placement AS current
                ON current.scoped_owner_ref = schedule.schedule_ref
              JOIN dante.schedule_placement_state AS placement
                ON placement.material_state_ref = current.material_state_ref
               AND placement.schedule_ref = schedule.schedule_ref
              LEFT JOIN dante.schedule_placement_date_state AS date_payload
                ON date_payload.material_state_ref = placement.material_state_ref
              LEFT JOIN dante.schedule_placement_floating_local_state AS floating_payload
                ON floating_payload.material_state_ref = placement.material_state_ref
              LEFT JOIN dante.schedule_placement_named_zone_state AS named_payload
                ON named_payload.material_state_ref = placement.material_state_ref
              LEFT JOIN dante.schedule_placement_absolute_state AS absolute_payload
                ON absolute_payload.material_state_ref = placement.material_state_ref
              LEFT JOIN dante.schedule_placement_coarse_local_period_state AS coarse_payload
                ON coarse_payload.material_state_ref = placement.material_state_ref
             WHERE intention.self_person_ref = :self_person_ref
               AND (
                    (
                        placement.temporal_form_code = 'date_span'
                        AND date_payload.date_span
                            && daterange(:start_date, :end_date_exclusive, '[)')
                    )
                    OR (
                        placement.temporal_form_code = 'floating_local'
                        AND floating_payload.extent_code = 'interval'
                        AND floating_payload.starts_local_at < :end_local_at
                        AND floating_payload.ends_local_at > :start_local_at
                    )
                    OR (
                        placement.temporal_form_code = 'named_zone_local'
                        AND named_payload.extent_code = 'interval'
                        AND named_payload.resolved_start_at IS NOT NULL
                        AND named_payload.resolved_end_at IS NOT NULL
                        AND named_payload.resolved_start_at < :end_instant
                        AND named_payload.resolved_end_at > :start_instant
                    )
                    OR (
                        placement.temporal_form_code = 'absolute'
                        AND absolute_payload.extent_code = 'interval'
                        AND absolute_payload.starts_at < :end_instant
                        AND absolute_payload.ends_at > :start_instant
                    )
                    OR (
                        placement.temporal_form_code = 'coarse_local_period'
                        AND coarse_payload.local_date >= :start_date
                        AND coarse_payload.local_date < :end_date_exclusive
                    )
               )
             ORDER BY
                   CASE placement.temporal_form_code
                       WHEN 'date_span' THEN lower(date_payload.date_span)::timestamp
                       WHEN 'floating_local' THEN floating_payload.starts_local_at
                       WHEN 'named_zone_local' THEN timezone(
                           CAST(:effective_zone_id AS text),
                           named_payload.resolved_start_at
                       )
                       WHEN 'absolute' THEN timezone(
                           CAST(:effective_zone_id AS text),
                           absolute_payload.starts_at
                       )
                       WHEN 'coarse_local_period' THEN coarse_payload.local_date::timestamp
                   END,
                   CASE placement.temporal_form_code
                       WHEN 'date_span' THEN 0
                       WHEN 'coarse_local_period' THEN 1
                       ELSE 2
                   END,
                   schedule.schedule_ref
            """
        )

        try:
            async with self._session_factory() as database_session, database_session.begin():
                rows = (
                    (
                        await database_session.execute(
                            statement,
                            {
                                "self_person_ref": context.self_person_ref,
                                "start_date": query.start_date,
                                "end_date_exclusive": query.end_date_exclusive,
                                "start_local_at": start_local_at,
                                "end_local_at": end_local_at,
                                "start_instant": start_instant,
                                "end_instant": end_instant,
                                "effective_zone_id": context.effective_zone_id,
                            },
                        )
                    )
                    .mappings()
                    .all()
                )
            items = tuple(
                _item_from_row(row, effective_zone_id=context.effective_zone_id) for row in rows
            )
        except (SQLAlchemyError, KeyError, TypeError, ValueError) as exc:
            raise TimelinePersistenceError() from exc

        if not items:
            return empty_timeline_window_result(query=query, context=context)

        return TimelineWindowResult(
            start_date=query.start_date,
            end_date_exclusive=query.end_date_exclusive,
            effective_zone_id=context.effective_zone_id,
            self_person_ref=context.self_person_ref,
            items=items,
        )
