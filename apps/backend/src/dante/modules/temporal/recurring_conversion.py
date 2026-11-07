"""Start a Routine from an already accepted Activity without replacing its identity.

The source, recurrence, future template, first occurrence and Activity binding
are committed together. A Timeline checkpoint cannot observe a source whose
first Activity has not been bound yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.activity_edit_snapshot_api import ActivityEditSnapshot, _SNAPSHOT
from dante.modules.temporal.authoring import (
    AuthoringLifeAreaIntent,
    TemporalAuthoringApplication,
    resolve_authoring_life_area,
)
from dante.modules.temporal.event import EventView, _read_event_in_session
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    OccurrenceApplication,
    _calendar_candidates,
)
from dante.modules.temporal.reality_objective_api import ObjectiveResponse
from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_authoring import (
    EventAuthoringPolicy,
    RecurringAuthoringResult,
    RoutineAuthoringPolicy,
    _bootstrap_recurrence,
    _child_operation_id,
    _create_routine_source_in_session,
    _read_recurrence_in_session,
    _replace_recurrence_in_session,
    _routine_bootstrap,
    _validate_recurrence,
)
from dante.modules.temporal.recurring_series_edit import _validate_structure
from dante.modules.temporal.recurring_series_reconciliation import SeriesReconciliationError
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.modules.temporal.temporal_constraint import _READ_CONSTRAINT_BASE
from dante.platform.database.references import NativeRef


class RecurringConversionConflictError(RuntimeError):
    """The selected first instance is stale, foreign, or already linked."""


class RecurringConversionUnsupportedError(ValueError):
    """This existing Activity cannot be represented faithfully as a Routine template."""


@dataclass(frozen=True, slots=True)
class ExistingActivityBasis:
    activity_ref: UUID
    expected_profile_revision: int
    envelope_schedule_ref: UUID
    expected_placement_state_ref: UUID


@dataclass(frozen=True, slots=True)
class ExistingEventBasis:
    event_ref: UUID
    expected_profile_revision: int
    schedule_ref: UUID
    expected_placement_state_ref: UUID


@dataclass(frozen=True, slots=True)
class ExistingActivityCurrent:
    title: str
    life_area_ref: UUID | None
    policy: RoutineAuthoringPolicy


def _minute_offset(anchor: datetime, value: datetime) -> int:
    difference = value - anchor
    minutes, remainder = divmod(difference.total_seconds(), 60)
    if remainder or not -525_600 <= minutes <= 525_600:
        raise RecurringConversionUnsupportedError("The Activity has non-minute Schedule precision.")
    return int(minutes)


def _window(anchor: datetime, start: datetime | None, end: datetime | None) -> dict[str, int]:
    if start is None or end is None:
        raise RecurringConversionUnsupportedError("A scheduled Session has no accepted time.")
    offset = _minute_offset(anchor, start)
    duration = _minute_offset(start, end)
    if duration <= 0:
        raise RecurringConversionUnsupportedError("The Activity has a non-positive interval.")
    return {"start_offset_minutes": offset, "duration_minutes": duration}


async def _existing_activity(
    session: AsyncSession,
    *,
    actor: NativeRef,
    basis: ExistingActivityBasis,
    recurrence: CalendarRecurrence,
) -> tuple[ExistingActivityCurrent, date, datetime | None]:
    profile = (
        (
            await session.execute(
                text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": actor, "activity": basis.activity_ref},
            )
        )
        .mappings()
        .one_or_none()
    )
    if profile is None or profile["revision"] != basis.expected_profile_revision:
        raise RecurringConversionConflictError("The Activity profile changed; reopen Edit.")
    payload = await session.scalar(
        _SNAPSHOT, {"actor": actor, "activity": basis.activity_ref}
    )
    if payload is None:
        raise RecurringConversionConflictError("The Activity is unavailable.")
    snapshot = ActivityEditSnapshot.model_validate(payload)
    if await session.scalar(
        text(
            "SELECT 1 FROM dante.get_self_activity_decomposition(:actor,:activity) "
            "WHERE child_activity_ref IS NOT NULL LIMIT 1"
        ),
        {"actor": actor, "activity": basis.activity_ref},
    ):
        raise RecurringConversionUnsupportedError(
            "An Activity with child Activities needs a complete future child template."
        )
    envelope = next(
        (item for item in snapshot.schedules if item.role_code == "envelope"), None
    )
    if (
        envelope is None
        or envelope.schedule_ref != basis.envelope_schedule_ref
        or envelope.placement_material_state_ref != basis.expected_placement_state_ref
    ):
        raise RecurringConversionConflictError("The Activity Schedule changed; reopen Edit.")
    if recurrence.clock_basis_code != "named_zone" or recurrence.zone_id is None:
        raise RecurringConversionUnsupportedError("The Activity needs a named-zone calendar rule.")

    all_day = envelope.temporal_form == "date_span"
    if all_day:
        if envelope.start_date is None or envelope.end_date_exclusive is None:
            raise RecurringConversionUnsupportedError("The Activity day span is incomplete.")
        first_date = envelope.start_date
        duration_days = (envelope.end_date_exclusive - first_date).days
        if not 1 <= duration_days <= 365 or recurrence.wall_times:
            raise RecurringConversionUnsupportedError("The recurrence must match the day span.")
        anchor = None
        root_window = None
        duration_minutes = duration_days * 1440
    else:
        if (
            envelope.temporal_form != "named_zone_local"
            or envelope.starts_local_at is None
            or envelope.ends_local_at is None
            or envelope.zone_id != recurrence.zone_id
        ):
            raise RecurringConversionUnsupportedError(
                "Only a timed Activity with a matching named-zone Schedule can start a series."
            )
        anchor = envelope.starts_local_at
        first_date = anchor.date()
        root_window = _window(anchor, anchor, envelope.ends_local_at)
        duration_minutes = root_window["duration_minutes"]
        if recurrence.wall_times != (anchor.time(),):
            raise RecurringConversionUnsupportedError(
                "The recurrence must start at the Activity's saved clock time."
            )
        if envelope.resolved_start_at is not None:
            local = envelope.resolved_start_at.astimezone(ZoneInfo(recurrence.zone_id))
            expected_fold = "later" if local.fold else "earlier"
            if recurrence.ambiguous_local_time_policy != expected_fold:
                raise RecurringConversionUnsupportedError(
                    "The recurrence must retain the first Activity's clock resolution."
                )
    if first_date != recurrence.effective_from:
        raise RecurringConversionUnsupportedError(
            "The recurrence must include the existing Activity as its first date."
        )

    constraint_rows = (
        (
            await session.execute(
                text(_READ_CONSTRAINT_BASE +
                     " AND constraint_row.subject_native_ref=:activity"),
                {"self_person_ref": actor, "activity": basis.activity_ref},
            )
        )
        .mappings()
        .all()
    )
    minimum_session_duration: int | None = None
    for constraint in constraint_rows:
        if constraint["material_state_ref"] is None:
            continue
        if (
            constraint["family_code"] == "duration"
            and constraint["duration_kind_code"] == "minimum"
            and constraint["constrained_facet_code"] == "session.active_duration"
            and constraint["strength_code"] == "soft"
            and minimum_session_duration is None
        ):
            minimum_session_duration = constraint["duration_microseconds"]
        else:
            raise RecurringConversionUnsupportedError(
                "The Activity has a planning constraint without a future recurrence template."
            )

    intervals = sorted(
        (item for item in snapshot.schedules if item.role_code == "interval"),
        key=lambda item: (item.presentation_order or 0, item.schedule_ref),
    )
    planned = sorted(
        (item for item in snapshot.schedules if item.role_code == "planned"),
        key=lambda item: (item.presentation_order or 0, item.schedule_ref),
    )
    if all_day and intervals:
        raise RecurringConversionUnsupportedError("All-day Activity intervals are unsupported.")
    if any(item.temporal_form not in {None, "named_zone_local"} for item in planned):
        raise RecurringConversionUnsupportedError("A planned Session uses another time form.")
    if any(
        item.zone_id != recurrence.zone_id
        for item in [*intervals, *planned]
        if item.temporal_form
    ):
        raise RecurringConversionUnsupportedError("The Activity has Schedules in different zones.")
    template = {
        "version": 1,
        **({"placement_kind": "all_day", "duration_days": duration_days} if all_day else {}),
        "root_window": root_window,
        "description": profile["description"],
        "location": profile["location"],
        "item_color_code": profile["color_code"],
        "session_capture_mode": snapshot.execution_policy.mode_code,
        "minimum_session_duration_microseconds": minimum_session_duration,
        "child_guard_mode": snapshot.child_guard_mode,
        "reality_mode": snapshot.reality_policy.mode_code,
        "placement_protected": snapshot.placement_lock is not None
        and snapshot.placement_lock.locked,
        "objectives": [
            {
                "label": objective.label,
                "result_kind": objective.result_kind,
                "comparator_code": objective.comparator_code,
                "target_value": float(objective.target_value)
                if objective.target_value is not None
                else None,
                "target_min": float(objective.target_min)
                if objective.target_min is not None
                else None,
                "target_max": float(objective.target_max)
                if objective.target_max is not None
                else None,
                "unit_code": objective.unit_code,
                "presentation_order": objective.presentation_order,
            }
            for objective in snapshot.objectives
        ],
        "activity_intervals": [
            _window(anchor, item.starts_local_at, item.ends_local_at)
            for item in intervals
        ] if anchor is not None else [],
        "planned_slices": [
            {"name": item.display_name or f"Sessione {index + 1}", "time_enabled": False}
            if item.temporal_form is None else {
                "name": item.display_name or f"Sessione {index + 1}",
                **_window(anchor, item.starts_local_at, item.ends_local_at),
            }
            for index, item in enumerate(planned)
        ],
        "children": [],
    }
    if all_day and any(item.temporal_form is not None for item in planned):
        raise RecurringConversionUnsupportedError("An all-day Session cannot have a clock.")
    if snapshot.reminder is not None and snapshot.reminder.enabled:
        reminder_lead = snapshot.reminder.lead_minutes
    else:
        reminder_lead = None
    policy = RoutineAuthoringPolicy(duration_minutes, reminder_lead, template)
    try:
        _validate_structure("routine", recurrence, {
            "version": 1,
            "duration_minutes": duration_minutes,
            "reminder_lead_minutes": reminder_lead,
            "activity_template": template,
        })
    except SeriesReconciliationError as exc:
        raise RecurringConversionUnsupportedError(str(exc)) from exc
    return ExistingActivityCurrent(
        title=str(profile["title"]),
        life_area_ref=snapshot.life_area_ref,
        policy=policy,
    ), first_date, envelope.resolved_start_at


async def _existing_event(
    session: AsyncSession,
    *,
    actor: NativeRef,
    basis: ExistingEventBasis,
    recurrence: CalendarRecurrence,
) -> tuple[EventView, EventAuthoringPolicy, date, datetime | None]:
    event = await _read_event_in_session(
        session, self_person_ref=actor, event_ref=NativeRef(basis.event_ref)
    )
    if event is None or event.profile_revision != basis.expected_profile_revision:
        raise RecurringConversionConflictError("The Event profile changed; reopen Edit.")
    schedules = (
        (
            await session.execute(
                text("""
                    SELECT schedule_row.schedule_ref,placement.material_state_ref,
                           state.temporal_form_code AS temporal_form,
                           lower(dates.date_span) AS start_date,
                           upper(dates.date_span) AS end_date_exclusive,
                           zoned.starts_local_at,zoned.ends_local_at,zoned.zone_id,
                           zoned.resolved_start_at
                      FROM dante.event_expectation AS owned
                      JOIN dante.schedule AS schedule_row
                        ON schedule_row.subject_native_ref=owned.event_ref
                      JOIN dante.schedule_current_placement AS placement
                        ON placement.scoped_owner_ref=schedule_row.schedule_ref
                      JOIN dante.schedule_placement_state AS state
                        ON state.schedule_ref=schedule_row.schedule_ref
                       AND state.material_state_ref=placement.material_state_ref
                 LEFT JOIN dante.schedule_placement_date_state AS dates
                        ON dates.material_state_ref=state.material_state_ref
                 LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
                        ON zoned.material_state_ref=state.material_state_ref
                     WHERE owned.event_ref=:event
                       AND owned.self_person_ref=:actor
                """),
                {"actor": actor, "event": basis.event_ref},
            )
        )
        .mappings()
        .all()
    )
    if len(schedules) != 1:
        raise RecurringConversionUnsupportedError("An Event needs one current Schedule.")
    schedule = schedules[0]
    if (
        schedule["schedule_ref"] != basis.schedule_ref
        or schedule["material_state_ref"] != basis.expected_placement_state_ref
    ):
        raise RecurringConversionConflictError("The Event Schedule changed; reopen Edit.")
    all_day = schedule["temporal_form"] == "date_span"
    if all_day:
        first_date = schedule["start_date"]
        if first_date is None or schedule["end_date_exclusive"] is None:
            raise RecurringConversionUnsupportedError("The Event day span is incomplete.")
        days = (schedule["end_date_exclusive"] - first_date).days
        if not 1 <= days <= 3660 or recurrence.wall_times:
            raise RecurringConversionUnsupportedError(
                "The recurrence must match the Event day span."
            )
        minutes = None
        first_instant = None
    else:
        if (
            schedule["temporal_form"] != "named_zone_local"
            or schedule["starts_local_at"] is None
            or schedule["ends_local_at"] is None
            or schedule["zone_id"] != recurrence.zone_id
        ):
            raise RecurringConversionUnsupportedError(
                "Only a timed Event with a matching named-zone Schedule can start a series."
            )
        first_date = schedule["starts_local_at"].date()
        minutes = _minute_offset(schedule["starts_local_at"], schedule["ends_local_at"])
        if minutes <= 0 or recurrence.wall_times != (schedule["starts_local_at"].time(),):
            raise RecurringConversionUnsupportedError("The recurrence must match the Event clock.")
        first_instant = schedule["resolved_start_at"]
        days = None
    if recurrence.effective_from != first_date:
        raise RecurringConversionUnsupportedError("The recurrence must start on the Event date.")
    if await session.scalar(
        text("SELECT 1 FROM (" + _READ_CONSTRAINT_BASE +
             " AND constraint_row.subject_native_ref=:event) AS owned "
             "WHERE owned.material_state_ref IS NOT NULL LIMIT 1"),
        {"self_person_ref": actor, "event": basis.event_ref},
    ):
        raise RecurringConversionUnsupportedError(
            "The Event has a planning constraint without a future recurrence template."
        )
    if await session.scalar(
        text("SELECT 1 FROM dante.list_self_event_expected_participation(:actor,:event) "
             "WHERE participant_person_ref<>:actor LIMIT 1"),
        {"actor": actor, "event": basis.event_ref},
    ):
        raise RecurringConversionUnsupportedError(
            "Events with other expected participants need a future participation template."
        )
    reality = await session.scalar(
        text("SELECT mode_code FROM dante.get_self_reality_review_policy(:actor,'event',:event)"),
        {"actor": actor, "event": basis.event_ref},
    )
    objective_rows = (
        (
            await session.execute(
                text("SELECT * FROM dante.list_self_temporal_objectives(:actor,'event',:event)"),
                {"actor": actor, "event": basis.event_ref},
            )
        )
        .mappings()
        .all()
    )
    objectives = tuple(
        {
            "label": item.label,
            "result_kind": item.result_kind,
            "comparator_code": item.comparator_code,
            "target_value": float(item.target_value) if item.target_value is not None else None,
            "target_min": float(item.target_min) if item.target_min is not None else None,
            "target_max": float(item.target_max) if item.target_max is not None else None,
            "unit_code": item.unit_code,
            "presentation_order": item.presentation_order,
        }
        for row in objective_rows
        for item in (ObjectiveResponse.model_validate(dict(row)),)
    )
    reminder = (
        (
            await session.execute(
                text(
                    "SELECT enabled,lead_minutes "
                    "FROM dante.get_self_schedule_reminder(:actor,:schedule)"
                ),
                {"actor": actor, "schedule": basis.schedule_ref},
            )
        )
        .mappings()
        .one_or_none()
    )
    lead = reminder["lead_minutes"] if reminder and reminder["enabled"] else None
    if all_day and lead is not None:
        raise RecurringConversionUnsupportedError("An all-day Event cannot have a clock Reminder.")
    policy = EventAuthoringPolicy(
        placement_kind="all_day" if all_day else "timed",
        duration_minutes=minutes,
        duration_days=days,
        reminder_lead_minutes=lead,
        reality_mode=reality or "manual",
        objectives=objectives,
    )
    try:
        _validate_structure("event", recurrence, {
            "version": 1,
            "placement_kind": policy.placement_kind,
            "duration_minutes": minutes,
            "duration_days": days,
            "reminder_lead_minutes": lead,
            "reality_mode": policy.reality_mode,
            "objectives": list(objectives),
            "agenda_parts": list(event.agenda_parts),
            "life_area_ref": str(event.life_area_ref) if event.life_area_ref else None,
        })
    except SeriesReconciliationError as exc:
        raise RecurringConversionUnsupportedError(str(exc)) from exc
    return event, policy, first_date, first_instant


class RecurringConversionApplication:
    """Accept source + first existing instance as one self-scoped transaction."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._routines = RoutineApplication(session_factory)
        self._events = TemporalAuthoringApplication(session_factory)
        self._event_policies = EventOccurrencePolicyApplication(session_factory)
        self._policies = RoutineOccurrencePolicyApplication(session_factory)
        self._occurrences = OccurrenceApplication(session_factory)

    async def event(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        basis: ExistingEventBasis,
        recurrence: CalendarRecurrence,
    ) -> RecurringAuthoringResult:
        if recurrence.clock_basis_code != "named_zone" or recurrence.zone_id is None:
            raise RecurringConversionUnsupportedError("The Event requires a named-zone rule.")
        _validate_recurrence(recurrence)
        try:
            async with self._session_factory() as session, session.begin():
                await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                event, policy, first_date, first_instant = await _existing_event(
                    session, actor=self_person_ref, basis=basis, recurrence=recurrence
                )
                candidates = _calendar_candidates(
                    basis.event_ref,
                    recurrence,
                    first_date,
                    first_date + timedelta(days=1),
                    ZoneInfo(recurrence.zone_id),
                )
                first = [
                    item.coordinate for item in candidates
                    if isinstance(item.coordinate, CalendarCoordinate)
                    and item.coordinate.generated_date == first_date
                    and (first_instant is None or item.coordinate.resolved_at == first_instant)
                ]
                if len(first) != 1:
                    raise RecurringConversionUnsupportedError(
                        "The rule must generate exactly the existing first Event."
                    )
                area = await resolve_authoring_life_area(
                    session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    intent=(
                        AuthoringLifeAreaIntent(life_area_ref=event.life_area_ref)
                        if event.life_area_ref else None
                    ),
                )
                if area is not None and event.color_code is not None:
                    raise RecurringConversionUnsupportedError(
                        "This Event has an item color alongside a Life Area."
                    )
                source, replayed = await self._events._create_event(
                    session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    title=event.title,
                    agenda_parts=event.agenda_parts,
                    description=event.description,
                    location=event.location,
                    item_color_code=event.color_code,
                    life_area=area,
                )
                source_ref = source.subject_native_ref
                current = await _read_recurrence_in_session(
                    session,
                    owner="event",
                    self_person_ref=self_person_ref,
                    owner_ref=source_ref,
                )
                if replayed:
                    if current is None or current.recurrence != recurrence:
                        raise RecurringConversionConflictError(
                            "This operation already represents another series."
                        )
                elif current is not None:
                    raise RecurringConversionConflictError("The future Event source changed.")
                else:
                    current = (
                        await _replace_recurrence_in_session(
                            session,
                            owner="event",
                            self_person_ref=self_person_ref,
                            owner_ref=source_ref,
                            operation_id=_child_operation_id(
                                operation_id, "existing-event-recurrence"
                            ),
                            expected_material_state_ref=None,
                            recurrence=recurrence,
                        )
                    ).recurrence
                await self._event_policies.set_in_session(
                    session,
                    self_person_ref=self_person_ref,
                    event_ref=source_ref,
                    placement_kind=policy.placement_kind,
                    duration_minutes=policy.duration_minutes,
                    duration_days=policy.duration_days,
                    reminder_lead_minutes=policy.reminder_lead_minutes,
                    reality_mode=policy.reality_mode,
                    objectives=policy.objectives,
                )
                await self._occurrences.exclude_in_session(
                    session,
                    owner="event",
                    self_person_ref=self_person_ref,
                    source_ref=source_ref,
                    governing_recurrence_state_ref=current.material_state_ref,
                    operation_id=_child_operation_id(operation_id, "existing-event-first"),
                    coordinate=first[0],
                )
                await session.execute(
                    text("SELECT * FROM dante.bind_self_event_recurring_seed("
                         ":actor,:event,:source,:schedule,:state,:revision,:first_day)"),
                    {
                        "actor": self_person_ref,
                        "event": basis.event_ref,
                        "source": source_ref,
                        "schedule": basis.schedule_ref,
                        "state": basis.expected_placement_state_ref,
                        "revision": basis.expected_profile_revision,
                        "first_day": first_date,
                    },
                )
                return RecurringAuthoringResult(
                    owner_kind="event",
                    source_ref=source_ref,
                    title=source.title,
                    created_at=source.created_at,
                    recurrence_material_state_ref=current.material_state_ref,
                    replayed=replayed,
                )
        except DBAPIError as exc:
            name = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
            if name in {"event_recurring_seed_unavailable", "event_recurring_seed_conflict"}:
                raise RecurringConversionConflictError(
                    "The Event is already linked or changed; reopen Edit."
                ) from exc
            raise

    async def activity(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        basis: ExistingActivityBasis,
        recurrence: CalendarRecurrence,
    ) -> RecurringAuthoringResult:
        if recurrence.clock_basis_code != "named_zone" or recurrence.zone_id is None:
            raise RecurringConversionUnsupportedError("The Activity requires a named-zone rule.")
        _validate_recurrence(recurrence)
        starts_on, wall_time = _routine_bootstrap(recurrence)
        try:
            async with self._session_factory() as session, session.begin():
                await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                current, first_date, first_instant = await _existing_activity(
                    session, actor=self_person_ref, basis=basis, recurrence=recurrence
                )
                source = await _create_routine_source_in_session(
                    session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    title=current.title,
                    life_area_ref=current.life_area_ref,
                    tag_refs=(),
                    starts_on=starts_on,
                    wall_time=wall_time,
                    application=self._routines,
                )
                saved_recurrence = await _read_recurrence_in_session(
                    session,
                    owner="routine",
                    self_person_ref=self_person_ref,
                    owner_ref=source.routine_ref,
                )
                if saved_recurrence is None:
                    raise RecurringConversionConflictError("The Routine lacks its recurrence.")
                if source.replayed:
                    if saved_recurrence.recurrence != recurrence:
                        raise RecurringConversionConflictError(
                            "The operation has another recurrence."
                        )
                elif saved_recurrence.recurrence != _bootstrap_recurrence(starts_on, wall_time):
                    raise RecurringConversionConflictError("The Routine bootstrap changed.")
                elif saved_recurrence.recurrence != recurrence:
                    saved_recurrence = (
                        await _replace_recurrence_in_session(
                            session,
                            owner="routine",
                            self_person_ref=self_person_ref,
                            owner_ref=source.routine_ref,
                            operation_id=_child_operation_id(
                                operation_id, "existing-activity-recurrence"
                            ),
                            expected_material_state_ref=saved_recurrence.material_state_ref,
                            recurrence=recurrence,
                        )
                    ).recurrence
                policy = current.policy
                await self._policies.set_in_session(
                    session,
                    self_person_ref=self_person_ref,
                    routine_ref=source.routine_ref,
                    duration_minutes=policy.duration_minutes,
                    reminder_lead_minutes=policy.reminder_lead_minutes,
                    activity_template=policy.activity_template,
                )
                checkpoint = await self._occurrences.checkpoint(
                    owner="routine",
                    self_person_ref=self_person_ref,
                    source_ref=source.routine_ref,
                    operation_id=_child_operation_id(operation_id, "existing-activity-first"),
                    start_date=first_date,
                    end_date_exclusive=first_date + timedelta(days=1),
                    effective_zone_id=recurrence.zone_id,
                    session=session,
                )
                first = [
                    item for item in checkpoint.occurrences
                    if not item.skipped
                    and isinstance(item.coordinate, CalendarCoordinate)
                    and item.coordinate.generated_date == first_date
                    and item.coordinate.generated_wall_time
                    == (recurrence.wall_times[0] if recurrence.wall_times else None)
                    and (first_instant is None or item.coordinate.resolved_at == first_instant)
                ]
                if len(first) != 1:
                    raise RecurringConversionUnsupportedError(
                        "The rule must produce exactly the existing first Activity."
                    )
                prior = await session.scalar(
                    text(
                        "SELECT dante.get_self_materialized_activity_occurrence(:actor,:activity)"
                    ),
                    {"actor": self_person_ref, "activity": basis.activity_ref},
                )
                if prior is not None and prior != first[0].occurrence_ref:
                    raise RecurringConversionConflictError(
                        "The Activity is already in another series."
                    )
                await session.execute(
                    text(
                        "SELECT * FROM dante.bind_self_routine_occurrence_activity("
                        ":actor,:occurrence,:activity)"
                    ),
                    {
                        "actor": self_person_ref,
                        "occurrence": first[0].occurrence_ref,
                        "activity": basis.activity_ref,
                    },
                )
                return RecurringAuthoringResult(
                    owner_kind="routine",
                    source_ref=source.routine_ref,
                    title=source.title,
                    created_at=source.created_at,
                    recurrence_material_state_ref=saved_recurrence.material_state_ref,
                    replayed=source.replayed,
                )
        except DBAPIError as exc:
            name = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
            if name in {
                "uq_routine_occurrence_activity_instance_activity",
                "routine_occurrence_activity_instance_conflict",
                "routine_occurrence_activity_instance_unavailable",
            }:
                raise RecurringConversionConflictError(
                    "The Activity cannot be linked to this series."
                ) from exc
            raise
        except SQLAlchemyError as exc:
            raise RecurringConversionConflictError(
                "The Activity conversion could not be committed."
            ) from exc
