"""B14 composition from Routine Occurrences to Schedule and Reminder truth.

B06 remains the authority that evaluates and materializes Occurrence identities.
B02 remains the authority for each concrete Schedule. B11-C remains the authority
for each concrete Reminder. This module only applies the immutable manual-Create
Routine policy to newly/readably materialized Occurrences.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Literal, cast
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    ElapsedCoordinate,
    OccurrenceApplication,
    OccurrenceCheckpoint,
    OccurrenceInputError,
    OccurrenceOwner,
    OccurrencePersistenceError,
    OccurrenceWindowCheckpoint,
    _window_source_operation_id,
)
from dante.modules.temporal.routine_occurrence_policy import (
    RoutineOccurrencePolicyApplication,
    RoutineOccurrencePolicyPersistenceError,
    RoutineOccurrencePolicyView,
)
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    SchedulePersistenceError,
    TemporalScheduleApplication,
)
from dante.modules.temporal.schedule_reminder import (
    ScheduleReminderApplication,
    ScheduleReminderPersistenceError,
)
from dante.platform.database.references import NativeRef


class RoutineOccurrenceMaterializationApplication:
    """Checkpoint current sources and apply manual recurring Activity policy."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._occurrences = OccurrenceApplication(session_factory)
        self._policies = RoutineOccurrencePolicyApplication(session_factory)
        self._schedules = TemporalScheduleApplication(session_factory)
        self._reminders = ScheduleReminderApplication(session_factory)

    async def _sources(
        self, self_person_ref: NativeRef
    ) -> tuple[tuple[OccurrenceOwner, UUID], ...]:
        statement = text(
            """
            WITH self_routine AS (
                SELECT routine_ref,lifecycle_state
                  FROM dante.list_self_routines(:actor)
            )
            SELECT 'routine'::text AS owner,routine.routine_ref AS source_ref
              FROM self_routine AS routine
              JOIN dante.routine_recurrence_current_history AS current
                ON current.routine_ref=routine.routine_ref
               AND current.current_until_at IS NULL
             WHERE routine.lifecycle_state='active'
            UNION ALL
            SELECT 'event'::text AS owner,expectation.event_ref AS source_ref
              FROM dante.event_expectation AS expectation
              JOIN dante.event_recurrence_current_history AS current
                ON current.event_ref=expectation.event_ref
               AND current.current_until_at IS NULL
             WHERE expectation.self_person_ref=:actor
             ORDER BY owner,source_ref
            """
        )
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    await session.execute(statement, {"actor": self_person_ref})
                ).mappings().all()
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc
        sources: list[tuple[OccurrenceOwner, UUID]] = []
        for row in rows:
            owner = str(row["owner"])
            if owner not in {"routine", "event"}:
                raise OccurrencePersistenceError()
            sources.append((cast(OccurrenceOwner, owner), UUID(str(row["source_ref"]))))
        return tuple(sources)

    @staticmethod
    def _placement(
        occurrence_ref: UUID,
        coordinate: CalendarCoordinate | ElapsedCoordinate,
        policy: RoutineOccurrencePolicyView,
    ):
        duration = timedelta(minutes=policy.duration_minutes)
        if isinstance(coordinate, ElapsedCoordinate):
            return AbsoluteIntervalPlacement(
                starts_at=coordinate.expected_at,
                ends_at=coordinate.expected_at + duration,
            )

        wall_time = coordinate.generated_wall_time
        if wall_time is None:
            raise OccurrenceInputError(
                f"Routine Occurrence {occurrence_ref} has no wall time for its Schedule policy."
            )
        starts_local = datetime.combine(coordinate.generated_date, wall_time)
        ends_local = starts_local + duration
        if coordinate.clock_basis_code == "floating_local":
            return FloatingLocalIntervalPlacement(
                starts_local_at=starts_local,
                ends_local_at=ends_local,
            )
        if coordinate.clock_basis_code == "absolute_utc":
            starts_at = starts_local.replace(tzinfo=UTC)
            return AbsoluteIntervalPlacement(
                starts_at=starts_at,
                ends_at=starts_at + duration,
            )
        if coordinate.zone_id is None:
            raise OccurrenceInputError("Named-zone Routine Occurrence has no zone id.")
        disambiguation: Literal["earlier", "later"] = "earlier"
        if coordinate.resolved_at is not None:
            local = coordinate.resolved_at.astimezone(ZoneInfo(coordinate.zone_id))
            disambiguation = "later" if local.fold == 1 else "earlier"
        return NamedZoneLocalIntervalPlacement(
            starts_local_at=starts_local,
            ends_local_at=ends_local,
            zone_id=coordinate.zone_id,
            disambiguation=disambiguation,
        )

    async def _apply_routine_policy(
        self,
        *,
        self_person_ref: NativeRef,
        source_ref: UUID,
        checkpoint: OccurrenceCheckpoint,
    ) -> None:
        policy = await self._policies.get(
            self_person_ref=self_person_ref,
            routine_ref=source_ref,
        )
        if policy is None:
            return

        for occurrence in checkpoint.occurrences:
            if occurrence.skipped or occurrence.coordinate is None:
                continue
            coordinate = occurrence.coordinate
            if not isinstance(coordinate, CalendarCoordinate | ElapsedCoordinate):
                raise OccurrenceInputError(
                    "Manual recurring Activity policy requires a concrete calendar or elapsed coordinate."
                )
            schedule = await self._schedules.establish_schedule(
                self_person_ref=self_person_ref,
                operation_id=f"b14:schedule:{occurrence.occurrence_ref}",
                subject_native_ref=NativeRef(occurrence.occurrence_ref),
                placement=self._placement(
                    occurrence.occurrence_ref,
                    coordinate,
                    policy,
                ),
            )
            if policy.reminder_lead_minutes is not None:
                await self._reminders.configure(
                    self_person_ref=self_person_ref,
                    schedule_ref=schedule.schedule_ref,
                    operation_id=f"b14:reminder:{occurrence.occurrence_ref}",
                    expected_material_state_ref=None,
                    enabled=True,
                    lead_minutes=policy.reminder_lead_minutes,
                )

    async def checkpoint_window(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        start_date: date,
        end_date_exclusive: date,
        effective_zone_id: str,
    ) -> OccurrenceWindowCheckpoint:
        checkpoints: list[OccurrenceCheckpoint] = []
        try:
            for owner, source_ref in await self._sources(self_person_ref):
                checkpoint = await self._occurrences.checkpoint(
                    owner=owner,
                    self_person_ref=self_person_ref,
                    source_ref=source_ref,
                    operation_id=_window_source_operation_id(
                        root_operation_id=operation_id,
                        owner=owner,
                        source_ref=source_ref,
                        start_date=start_date,
                        end_date_exclusive=end_date_exclusive,
                        effective_zone_id=effective_zone_id,
                    ),
                    start_date=start_date,
                    end_date_exclusive=end_date_exclusive,
                    effective_zone_id=effective_zone_id,
                )
                checkpoints.append(checkpoint)
                if owner == "routine":
                    await self._apply_routine_policy(
                        self_person_ref=self_person_ref,
                        source_ref=source_ref,
                        checkpoint=checkpoint,
                    )
        except (
            RoutineOccurrencePolicyPersistenceError,
            SchedulePersistenceError,
            ScheduleReminderPersistenceError,
        ) as exc:
            raise OccurrencePersistenceError() from exc

        return OccurrenceWindowCheckpoint(
            start_date=start_date,
            end_date_exclusive=end_date_exclusive,
            effective_zone_id=effective_zone_id,
            source_count=len(checkpoints),
            occurrence_count=sum(len(item.occurrences) for item in checkpoints),
            replayed_source_count=sum(int(item.replayed) for item in checkpoints),
        )
