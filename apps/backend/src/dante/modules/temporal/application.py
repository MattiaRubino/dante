"""Temporal Timeline application boundary over canonical current Schedule state."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.context.contracts import DanteContext
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class TimelinePersistenceError(RuntimeError):
    """The canonical Timeline window could not be read safely."""


@dataclass(frozen=True, slots=True)
class TimelineScheduledActivityItem:
    """Normalized current Schedule projection for one Activity."""

    activity_ref: NativeRef
    schedule_ref: ScopedRecordRef
    placement_material_state_ref: MaterialStateRef
    title: str
    starts_local_at: datetime
    ends_local_at: datetime


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
        """Read B02-A floating-local current Schedule items for the authenticated self."""
        start_local_at = datetime.combine(query.start_date, time.min)
        end_local_at = datetime.combine(query.end_date_exclusive, time.min)
        statement = text(
            """
            SELECT intention.activity_ref,
                   intention.title,
                   schedule.schedule_ref,
                   current.material_state_ref,
                   payload.starts_local_at,
                   payload.ends_local_at
            FROM dante.activity_intention AS intention
            JOIN dante.schedule AS schedule
              ON schedule.subject_native_ref = intention.activity_ref
            JOIN dante.schedule_current_placement AS current
              ON current.scoped_owner_ref = schedule.schedule_ref
            JOIN dante.schedule_placement_state AS placement
              ON placement.material_state_ref = current.material_state_ref
             AND placement.schedule_ref = schedule.schedule_ref
            JOIN dante.schedule_placement_floating_local_state AS payload
              ON payload.material_state_ref = placement.material_state_ref
            WHERE intention.self_person_ref = :self_person_ref
              AND placement.temporal_form_code = 'floating_local'
              AND payload.extent_code = 'interval'
              AND payload.starts_local_at < :end_local_at
              AND payload.ends_local_at > :start_local_at
            ORDER BY payload.starts_local_at,
                     payload.ends_local_at,
                     schedule.schedule_ref
            """
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                rows = (
                    (
                        await database_session.execute(
                            statement,
                            {
                                "self_person_ref": context.self_person_ref,
                                "start_local_at": start_local_at,
                                "end_local_at": end_local_at,
                            },
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise TimelinePersistenceError() from exc

        if not rows:
            return empty_timeline_window_result(query=query, context=context)

        return TimelineWindowResult(
            start_date=query.start_date,
            end_date_exclusive=query.end_date_exclusive,
            effective_zone_id=context.effective_zone_id,
            self_person_ref=context.self_person_ref,
            items=tuple(
                TimelineScheduledActivityItem(
                    activity_ref=NativeRef(UUID(str(row["activity_ref"]))),
                    schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
                    placement_material_state_ref=MaterialStateRef(
                        UUID(str(row["material_state_ref"]))
                    ),
                    title=str(row["title"]),
                    starts_local_at=row["starts_local_at"],
                    ends_local_at=row["ends_local_at"],
                )
                for row in rows
            ),
        )
