"""B14 composition from Routine Occurrences to Schedule and Reminder truth.

B06 remains the authority that evaluates and materializes Occurrence identities.
B02 remains the authority for each concrete Schedule. B11-C remains the authority
for each concrete Reminder. This module only applies the immutable manual-Create
Routine policy to newly/readably materialized Occurrences.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
import hashlib
import json
from typing import Literal, cast
from uuid import UUID, uuid7
from zoneinfo import ZoneInfo

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.authoring import (
    ActivityChildIntent,
    AuthoringLifeAreaIntent,
    AuthoringResult,
    TemporalAuthoringApplication,
)
from dante.modules.temporal.event_occurrence_policy import (
    EventOccurrencePolicyApplication,
    EventOccurrencePolicyPersistenceError,
    EventOccurrencePolicyView,
)
from dante.modules.temporal.movement_policy import (
    MovementPolicyApplication,
    MovementPolicyRule,
)
from dante.modules.temporal.placement_lock import PlacementLockApplication
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
    DateSpanPlacement,
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
        self._event_policies = EventOccurrencePolicyApplication(session_factory)
        self._schedules = TemporalScheduleApplication(session_factory)
        self._reminders = ScheduleReminderApplication(session_factory)
        self._authoring = TemporalAuthoringApplication(session_factory)
        self._movement = MovementPolicyApplication(session_factory)
        self._locks = PlacementLockApplication(session_factory)

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

    @staticmethod
    def _event_placement(
        occurrence_ref: UUID,
        coordinate: CalendarCoordinate,
        policy: EventOccurrencePolicyView,
    ):
        if policy.placement_kind == "all_day":
            if policy.duration_days is None:
                raise OccurrenceInputError(
                    "Recurring all-day Event policy has no duration."
                )
            start_date = coordinate.generated_date
            return DateSpanPlacement(
                start_date=start_date,
                end_date_exclusive=start_date + timedelta(days=policy.duration_days),
            )

        if policy.duration_minutes is None:
            raise OccurrenceInputError("Recurring timed Event policy has no duration.")
        wall_time = coordinate.generated_wall_time
        if wall_time is None:
            raise OccurrenceInputError(
                f"Event Occurrence {occurrence_ref} has no wall time for its Schedule policy."
            )
        starts_local = datetime.combine(coordinate.generated_date, wall_time)
        ends_local = starts_local + timedelta(minutes=policy.duration_minutes)
        if coordinate.clock_basis_code == "floating_local":
            return FloatingLocalIntervalPlacement(
                starts_local_at=starts_local,
                ends_local_at=ends_local,
            )
        if coordinate.clock_basis_code == "absolute_utc":
            starts_at = starts_local.replace(tzinfo=UTC)
            return AbsoluteIntervalPlacement(
                starts_at=starts_at,
                ends_at=starts_at + timedelta(minutes=policy.duration_minutes),
            )
        if coordinate.zone_id is None:
            raise OccurrenceInputError("Named-zone Event Occurrence has no zone id.")
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

    async def _apply_event_policy(
        self,
        *,
        self_person_ref: NativeRef,
        source_ref: UUID,
        checkpoint: OccurrenceCheckpoint,
    ) -> None:
        policy = await self._event_policies.get(
            self_person_ref=self_person_ref,
            event_ref=source_ref,
        )
        if policy is None:
            return

        for occurrence in checkpoint.occurrences:
            if occurrence.skipped or occurrence.coordinate is None:
                continue
            if not isinstance(occurrence.coordinate, CalendarCoordinate):
                raise OccurrenceInputError(
                    "Recurring Event Create currently requires calendar Occurrences."
                )
            schedule = await self._schedules.establish_schedule(
                self_person_ref=self_person_ref,
                operation_id=f"b14:event-schedule:{occurrence.occurrence_ref}",
                subject_native_ref=NativeRef(occurrence.occurrence_ref),
                placement=self._event_placement(
                    occurrence.occurrence_ref,
                    occurrence.coordinate,
                    policy,
                ),
            )
            if policy.reminder_lead_minutes is not None:
                await self._reminders.configure(
                    self_person_ref=self_person_ref,
                    schedule_ref=schedule.schedule_ref,
                    operation_id=f"b14:event-reminder:{occurrence.occurrence_ref}",
                    expected_material_state_ref=None,
                    enabled=True,
                    lead_minutes=policy.reminder_lead_minutes,
                )
            await self._set_reality(
                self_person_ref=self_person_ref,
                subject_kind="occurrence",
                subject_ref=occurrence.occurrence_ref,
                mode=policy.reality_mode,
                operation_suffix=f"event:{source_ref}",
            )
            await self._create_objectives(
                self_person_ref=self_person_ref,
                subject_kind="occurrence",
                subject_ref=occurrence.occurrence_ref,
                objectives=policy.objectives,
            )

    async def _routine_source(
        self, *, self_person_ref: NativeRef, routine_ref: UUID
    ) -> tuple[str, UUID | None]:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            """SELECT title,life_area_ref
                                 FROM dante.list_self_routines(:actor)
                                WHERE routine_ref=:routine"""
                        ),
                        {"actor": self_person_ref, "routine": routine_ref},
                    )
                ).mappings().one_or_none()
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc
        if row is None:
            raise OccurrencePersistenceError()
        return str(row["title"]), (
            None if row["life_area_ref"] is None else UUID(str(row["life_area_ref"]))
        )

    @staticmethod
    def _template_window(
        occurrence_ref: UUID,
        coordinate: CalendarCoordinate,
        value: object,
    ) -> NamedZoneLocalIntervalPlacement:
        if not isinstance(value, dict):
            raise OccurrenceInputError("Recurring Activity template window is invalid.")
        offset = value.get("start_offset_minutes")
        duration = value.get("duration_minutes")
        if (
            isinstance(offset, bool)
            or not isinstance(offset, int)
            or isinstance(duration, bool)
            or not isinstance(duration, int)
            or duration <= 0
        ):
            raise OccurrenceInputError("Recurring Activity template window is invalid.")
        wall_time = coordinate.generated_wall_time
        if wall_time is None or coordinate.zone_id is None:
            raise OccurrenceInputError(
                f"Routine Occurrence {occurrence_ref} cannot resolve its Activity template."
            )
        if coordinate.clock_basis_code != "named_zone":
            raise OccurrenceInputError(
                "Manual recurring Activity templates require named-zone calendar recurrence."
            )
        base = datetime.combine(coordinate.generated_date, wall_time)
        starts_local = base + timedelta(minutes=offset)
        ends_local = starts_local + timedelta(minutes=duration)
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

    async def _bind_activity(
        self,
        *,
        self_person_ref: NativeRef,
        occurrence_ref: UUID,
        activity_ref: NativeRef,
    ) -> None:
        try:
            async with self._session_factory() as session, session.begin():
                await session.execute(
                    text(
                        "SELECT * FROM dante.bind_self_routine_occurrence_activity("
                        ":actor,:occurrence,:activity)"
                    ),
                    {
                        "actor": self_person_ref,
                        "occurrence": occurrence_ref,
                        "activity": activity_ref,
                    },
                )
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

    async def _set_reality(
        self,
        *,
        self_person_ref: NativeRef,
        subject_kind: Literal["activity", "event", "occurrence"],
        subject_ref: UUID,
        mode: object,
        operation_suffix: str,
    ) -> None:
        if mode == "manual":
            return
        if mode not in {"review_on_end", "auto_confirm_outcome"}:
            raise OccurrenceInputError("Recurring Reality policy is invalid.")
        operation_id = f"b14:reality:{operation_suffix}:{subject_ref}"
        intent = {
            "version": 1,
            "subject_kind": subject_kind,
            "subject_native_ref": str(subject_ref),
            "mode_code": mode,
            "expected_state_ref": None,
        }
        fingerprint = hashlib.sha256(
            json.dumps(intent, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        try:
            async with self._session_factory() as session, session.begin():
                await session.execute(
                    text(
                        """SELECT * FROM dante.set_self_reality_review_policy(
                             :actor,:operation,:fingerprint,:kind,:subject,
                             :state,:mode,NULL)"""
                    ),
                    {
                        "actor": self_person_ref,
                        "operation": operation_id,
                        "fingerprint": fingerprint,
                        "kind": subject_kind,
                        "subject": subject_ref,
                        "state": uuid7(),
                        "mode": mode,
                    },
                )
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

    async def _create_objectives(
        self,
        *,
        self_person_ref: NativeRef,
        subject_kind: Literal["activity", "event", "occurrence"],
        subject_ref: UUID,
        objectives: object,
    ) -> None:
        if objectives is None:
            return
        if not isinstance(objectives, (list, tuple)) or len(objectives) > 100:
            raise OccurrenceInputError("Recurring Objectives template is invalid.")

        for index, raw in enumerate(objectives):
            if not isinstance(raw, dict):
                raise OccurrenceInputError("Recurring Objective template is invalid.")
            label = str(raw.get("label", "")).strip()
            result_kind = raw.get("result_kind")
            comparator = raw.get("comparator_code")
            target_value = raw.get("target_value")
            target_min = raw.get("target_min")
            target_max = raw.get("target_max")
            unit_code = raw.get("unit_code")
            presentation_order = raw.get("presentation_order", index)
            if not label or not isinstance(presentation_order, int):
                raise OccurrenceInputError("Recurring Objective template is invalid.")

            intent = {
                "version": 1,
                "subject_kind": subject_kind,
                "subject_native_ref": str(subject_ref),
                "label": label,
                "result_kind": result_kind,
                "comparator_code": comparator,
                "target_value": target_value,
                "target_min": target_min,
                "target_max": target_max,
                "unit_code": unit_code,
                "presentation_order": presentation_order,
            }
            fingerprint = hashlib.sha256(
                json.dumps(intent, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            operation_id = f"b14:objective:{subject_kind}:{subject_ref}:{index}"
            params = {
                "actor": self_person_ref,
                "operation": operation_id,
                "fingerprint": fingerprint,
                "objective": uuid7(),
                "subject": subject_ref,
                "label": label,
                "result_kind": result_kind,
                "comparator": comparator,
                "target_value": target_value,
                "target_min": target_min,
                "target_max": target_max,
                "unit": unit_code,
                "presentation_order": presentation_order,
            }
            if subject_kind == "occurrence":
                statement = """
                    SELECT * FROM dante.create_self_occurrence_objective(
                        :actor,:operation,:fingerprint,:objective,:subject,
                        :label,:result_kind,:comparator,:target_value,
                        :target_min,:target_max,:unit,:presentation_order
                    )
                """
            else:
                statement = """
                    SELECT * FROM dante.create_self_temporal_objective(
                        :actor,:operation,:fingerprint,:objective,:kind,:subject,
                        :label,:result_kind,:comparator,:target_value,
                        :target_min,:target_max,:unit,:presentation_order
                    )
                """
                params["kind"] = subject_kind
            try:
                async with self._session_factory() as session, session.begin():
                    await session.execute(text(statement), params)
            except SQLAlchemyError as exc:
                raise OccurrencePersistenceError() from exc

    async def _protect_schedules(
        self,
        *,
        self_person_ref: NativeRef,
        occurrence_ref: UUID,
        result: AuthoringResult,
    ) -> None:
        schedules = [
            *( [result.schedule] if result.schedule is not None else [] ),
            *result.activity_intervals,
            *result.planned_slices,
            *[
                schedule
                for child in result.children
                for schedule in (
                    *( [child.schedule] if child.schedule is not None else [] ),
                    *child.planned_slices,
                )
            ],
        ]
        for index, schedule in enumerate(schedules):
            await self._movement.create_policy(
                self_person_ref=self_person_ref,
                operation_id=f"b14:movement-lock:{index}:{occurrence_ref}",
                schedule_ref=schedule.schedule_ref,
                rule=MovementPolicyRule(
                    automatic_movement="blocked",
                    acceptance_path="direct",
                ),
            )
            await self._locks.set(
                self_person_ref=self_person_ref,
                schedule_ref=schedule.schedule_ref,
                locked=True,
                expected_revision=None,
            )

    async def _materialize_activity(
        self,
        *,
        self_person_ref: NativeRef,
        source_ref: UUID,
        occurrence_ref: UUID,
        coordinate: CalendarCoordinate,
        policy: RoutineOccurrencePolicyView,
    ) -> None:
        template = policy.activity_template
        title, life_area_ref = await self._routine_source(
            self_person_ref=self_person_ref,
            routine_ref=source_ref,
        )
        root_window = template.get(
            "root_window",
            {
                "start_offset_minutes": 0,
                "duration_minutes": policy.duration_minutes,
            },
        )
        root_placement = self._template_window(
            occurrence_ref,
            coordinate,
            root_window,
        )
        intervals = tuple(
            self._template_window(occurrence_ref, coordinate, value)
            for value in template.get("activity_intervals", [])
        )
        planned_rows = template.get("planned_slices", [])
        if not isinstance(planned_rows, list):
            raise OccurrenceInputError("Recurring Activity planned Sessions are invalid.")
        planned_slices = tuple(
            self._template_window(occurrence_ref, coordinate, value)
            for value in planned_rows
        )
        planned_names = tuple(
            str(value.get("name", "")).strip()
            for value in planned_rows
            if isinstance(value, dict)
        )
        if len(planned_names) != len(planned_slices):
            raise OccurrenceInputError("Recurring Activity Session names are invalid.")

        child_rows = template.get("children", [])
        if not isinstance(child_rows, list):
            raise OccurrenceInputError("Recurring Activity children are invalid.")
        children: list[ActivityChildIntent] = []
        child_reality: list[object] = []
        for row in child_rows:
            if not isinstance(row, dict):
                raise OccurrenceInputError("Recurring Activity child is invalid.")
            child_planned = row.get("planned_slices", [])
            if not isinstance(child_planned, list):
                raise OccurrenceInputError("Recurring child Sessions are invalid.")
            placement_value = row.get("placement")
            children.append(
                ActivityChildIntent(
                    title=str(row.get("title", "")).strip(),
                    requirement_code=cast(
                        Literal["required", "optional"],
                        row.get("requirement_code", "required"),
                    ),
                    presentation_order=len(children) + 1,
                    placement=(
                        None
                        if placement_value is None
                        else self._template_window(
                            occurrence_ref, coordinate, placement_value
                        )
                    ),
                    planned_slices=tuple(
                        self._template_window(occurrence_ref, coordinate, value)
                        for value in child_planned
                    ),
                    planned_slice_names=tuple(
                        str(value.get("name", "")).strip()
                        for value in child_planned
                        if isinstance(value, dict)
                    ),
                    session_capture_mode=cast(
                        Literal["disabled", "record", "live", "record_and_live"],
                        row.get("session_capture_mode", "disabled"),
                    ),
                )
            )
            child_reality.append(row.get("reality_mode", "manual"))

        minimum = template.get("minimum_session_duration_microseconds")
        if minimum is not None and (
            isinstance(minimum, bool) or not isinstance(minimum, int) or minimum <= 0
        ):
            raise OccurrenceInputError("Recurring Activity Session minimum is invalid.")

        result = await self._authoring.create_activity(
            self_person_ref=self_person_ref,
            operation_id=f"b14:occurrence-activity:{occurrence_ref}",
            title=title,
            life_area_intent=(
                None
                if life_area_ref is None
                else AuthoringLifeAreaIntent(life_area_ref=life_area_ref)
            ),
            description=cast(str | None, template.get("description")),
            location=cast(str | None, template.get("location")),
            item_color_code=cast(str | None, template.get("item_color_code")),
            placement=root_placement,
            session_capture_mode=cast(
                str, template.get("session_capture_mode", "disabled")
            ),
            minimum_session_duration_microseconds=cast(int | None, minimum),
            child_guard_mode=cast(str, template.get("child_guard_mode", "none")),
            planned_slices=planned_slices,
            activity_intervals=intervals,
            planned_slice_names=planned_names,
            children=tuple(children),
        )
        await self._set_reality(
            self_person_ref=self_person_ref,
            subject_kind="activity",
            subject_ref=result.item.subject_native_ref,
            mode=template.get("reality_mode", "manual"),
            operation_suffix=f"routine-root:{occurrence_ref}",
        )
        await self._create_objectives(
            self_person_ref=self_person_ref,
            subject_kind="activity",
            subject_ref=result.item.subject_native_ref,
            objectives=template.get("objectives", []),
        )
        for index, child in enumerate(result.children):
            await self._set_reality(
                self_person_ref=self_person_ref,
                subject_kind="activity",
                subject_ref=child.item.subject_native_ref,
                mode=child_reality[index] if index < len(child_reality) else "manual",
                operation_suffix=f"routine-child:{occurrence_ref}:{index}",
            )
        if bool(template.get("placement_protected", False)):
            await self._protect_schedules(
                self_person_ref=self_person_ref,
                occurrence_ref=occurrence_ref,
                result=result,
            )
        if policy.reminder_lead_minutes is not None:
            if result.schedule is None:
                raise OccurrenceInputError(
                    "Recurring Activity Reminder requires an accepted root Schedule."
                )
            await self._reminders.configure(
                self_person_ref=self_person_ref,
                schedule_ref=result.schedule.schedule_ref,
                operation_id=f"b14:reminder:{occurrence_ref}",
                expected_material_state_ref=None,
                enabled=True,
                lead_minutes=policy.reminder_lead_minutes,
            )
        # Binding is the completion marker for one occurrence instance. Keep it
        # last so a partial policy application is retried deterministically
        # instead of being mistaken for a fully materialized Activity.
        await self._bind_activity(
            self_person_ref=self_person_ref,
            occurrence_ref=occurrence_ref,
            activity_ref=result.item.subject_native_ref,
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
            if policy.activity_template:
                if not isinstance(coordinate, CalendarCoordinate):
                    raise OccurrenceInputError(
                        "Recurring Activity templates require calendar Occurrences."
                    )
                await self._materialize_activity(
                    self_person_ref=self_person_ref,
                    source_ref=source_ref,
                    occurrence_ref=occurrence.occurrence_ref,
                    coordinate=coordinate,
                    policy=policy,
                )
                continue
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
                elif owner == "event":
                    await self._apply_event_policy(
                        self_person_ref=self_person_ref,
                        source_ref=source_ref,
                        checkpoint=checkpoint,
                    )
        except (
            RoutineOccurrencePolicyPersistenceError,
            EventOccurrencePolicyPersistenceError,
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
