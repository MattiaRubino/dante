"""Unified product planning tray over canonical Activity/Event/Schedule truth."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.schedule import (
    SchedulePlacement,
    TemporalScheduleApplication,
)
from dante.platform.database.references import NativeRef

PlanningTrayKind = Literal["activity", "event"]
PlanningTrayState = Literal["unplaced", "postponed"]


class PlanningTrayPersistenceError(RuntimeError):
    """Canonical planning-tray truth could not be read safely."""


class PlanningTrayItemNotFoundError(LookupError):
    """The requested subject is no longer available in the planning tray."""


@dataclass(frozen=True, slots=True)
class PlanningTrayItemView:
    kind: PlanningTrayKind
    state: PlanningTrayState
    subject_ref: NativeRef
    title: str
    created_at: datetime
    life_area_ref: UUID | None
    life_area_assignment_revision: int | None
    schedule_ref: UUID | None = None
    unschedule_operation_id: str | None = None


@dataclass(frozen=True, slots=True)
class PlanningTrayPlacementView:
    kind: PlanningTrayKind
    subject_ref: NativeRef
    schedule_ref: UUID
    placement_material_state_ref: UUID
    replayed: bool


class TemporalPlanningTrayApplication:
    """Product projection/action boundary for every item currently needing placement.

    The tray deliberately unifies presentation only. A never-placed Event and a
    postponed Event remain different canonical states; postponed Events retain
    their existing Schedule identity and replan through the B03 guarded path.
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._activity = TemporalActivityApplication(session_factory)
        self._event = TemporalEventApplication(session_factory)
        self._schedule = TemporalScheduleApplication(session_factory)

    async def list_items(
        self,
        *,
        self_person_ref: NativeRef,
    ) -> tuple[PlanningTrayItemView, ...]:
        activity_statement = text(
            """
            SELECT intention.activity_ref AS subject_ref,
                   intention.title,
                   intention.created_at,
                   assignment.life_area_ref,
                   assignment.assignment_revision AS life_area_assignment_revision
              FROM dante.activity_intention AS intention
              LEFT JOIN dante.list_self_life_area_assignments(:self_person_ref) AS assignment
                ON assignment.subject_kind='activity'
               AND assignment.subject_native_ref=intention.activity_ref
             WHERE intention.self_person_ref=:self_person_ref
               AND intention.retired_at IS NULL
               AND NOT EXISTS (
                   SELECT 1
                     FROM dante.schedule AS schedule
                     JOIN dante.schedule_current_placement AS current
                       ON current.scoped_owner_ref=schedule.schedule_ref
                    WHERE schedule.subject_native_ref=intention.activity_ref
               )
            """
        )
        event_statement = text(
            """
            SELECT expectation.event_ref AS subject_ref,
                   expectation.title,
                   expectation.created_at,
                   assignment.life_area_ref,
                   assignment.assignment_revision AS life_area_assignment_revision
              FROM dante.event_expectation AS expectation
              LEFT JOIN dante.list_self_life_area_assignments(:self_person_ref) AS assignment
                ON assignment.subject_kind='event'
               AND assignment.subject_native_ref=expectation.event_ref
             WHERE expectation.self_person_ref=:self_person_ref
               AND NOT EXISTS (
                   SELECT 1
                     FROM dante.schedule AS schedule
                     JOIN dante.schedule_current_placement AS current
                       ON current.scoped_owner_ref=schedule.schedule_ref
                    WHERE schedule.subject_native_ref=expectation.event_ref
               )
            """
        )
        postponed_statement = text(
            """
            SELECT event_ref,
                   schedule_ref,
                   unschedule_operation_id
              FROM dante.list_self_postponed_events(:self_person_ref)
            """
        )

        try:
            async with self._session_factory() as database_session, database_session.begin():
                activities = (
                    (
                        await database_session.execute(
                            activity_statement,
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                events = (
                    (
                        await database_session.execute(
                            event_statement,
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                postponed_rows = (
                    (
                        await database_session.execute(
                            postponed_statement,
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise PlanningTrayPersistenceError() from exc

        postponed = {
            UUID(str(row["event_ref"])): row for row in postponed_rows
        }
        items: list[PlanningTrayItemView] = [
            PlanningTrayItemView(
                kind="activity",
                state="unplaced",
                subject_ref=NativeRef(UUID(str(row["subject_ref"]))),
                title=str(row["title"]),
                created_at=row["created_at"],
                life_area_ref=(
                    None
                    if row["life_area_ref"] is None
                    else UUID(str(row["life_area_ref"]))
                ),
                life_area_assignment_revision=(
                    None
                    if row["life_area_assignment_revision"] is None
                    else int(row["life_area_assignment_revision"])
                ),
            )
            for row in activities
        ]

        for row in events:
            event_ref = UUID(str(row["subject_ref"]))
            postponed_row = postponed.get(event_ref)
            items.append(
                PlanningTrayItemView(
                    kind="event",
                    state="postponed" if postponed_row is not None else "unplaced",
                    subject_ref=NativeRef(event_ref),
                    title=str(row["title"]),
                    created_at=row["created_at"],
                    life_area_ref=(
                        None
                        if row["life_area_ref"] is None
                        else UUID(str(row["life_area_ref"]))
                    ),
                    life_area_assignment_revision=(
                        None
                        if row["life_area_assignment_revision"] is None
                        else int(row["life_area_assignment_revision"])
                    ),
                    schedule_ref=(
                        None
                        if postponed_row is None
                        else UUID(str(postponed_row["schedule_ref"]))
                    ),
                    unschedule_operation_id=(
                        None
                        if postponed_row is None
                        else str(postponed_row["unschedule_operation_id"])
                    ),
                )
            )

        items.sort(key=lambda item: (item.created_at, item.kind, str(item.subject_ref)))
        return tuple(items)

    async def place_item(
        self,
        *,
        self_person_ref: NativeRef,
        kind: PlanningTrayKind,
        subject_ref: NativeRef,
        operation_id: str,
        placement: SchedulePlacement,
    ) -> PlanningTrayPlacementView:
        item = next(
            (
                candidate
                for candidate in await self.list_items(self_person_ref=self_person_ref)
                if candidate.kind == kind and candidate.subject_ref == subject_ref
            ),
            None,
        )
        if item is None:
            raise PlanningTrayItemNotFoundError()

        if kind == "activity":
            result = await self._activity.schedule_existing_activity_with_placement(
                self_person_ref=self_person_ref,
                activity_ref=subject_ref,
                operation_id=operation_id,
                placement=placement,
            )
            return PlanningTrayPlacementView(
                kind="activity",
                subject_ref=subject_ref,
                schedule_ref=UUID(str(result.schedule.schedule_ref)),
                placement_material_state_ref=UUID(str(result.schedule.material_state_ref)),
                replayed=result.replayed,
            )

        if item.state == "postponed":
            if item.schedule_ref is None or item.unschedule_operation_id is None:
                raise PlanningTrayPersistenceError("Postponed Event is missing retained Schedule truth.")
            result = await self._event.replan_postponed_event(
                self_person_ref=self_person_ref,
                event_ref=subject_ref,
                schedule_ref=item.schedule_ref,
                unschedule_operation_id=item.unschedule_operation_id,
                operation_id=operation_id,
                placement=placement,
            )
            return PlanningTrayPlacementView(
                kind="event",
                subject_ref=subject_ref,
                schedule_ref=UUID(str(result.schedule.schedule_ref)),
                placement_material_state_ref=UUID(str(result.schedule.material_state_ref)),
                replayed=result.replayed,
            )

        result = await self._schedule.establish_schedule(
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            subject_native_ref=subject_ref,
            placement=placement,
        )
        return PlanningTrayPlacementView(
            kind="event",
            subject_ref=subject_ref,
            schedule_ref=UUID(str(result.schedule_ref)),
            placement_material_state_ref=UUID(str(result.material_state_ref)),
            replayed=result.replayed,
        )
