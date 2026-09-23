"""B06-D atomic authoring for recurring Routine and Event sources.

The public Create flow must never leave a source committed without the Recurrence
that made the user choose a recurring object.  This application composes the
already-governed B06-A/B SQL capabilities in one database transaction; it adds
no persistence model and never materializes Occurrences or Schedules.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from typing import Literal
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.event import (
    EventAgendaRevisionConflictError,
    EventInputError,
    EventLifeAreaUnavailableError,
    EventNotFoundError,
    EventOperationIdReuseError,
    EventPersistenceError,
    TemporalEventApplication,
    _constraint_name as _event_constraint_name,
    _normalize_agenda_parts,
    _normalize_operation_id as _normalize_event_operation_id,
    _normalize_title as _normalize_event_title,
)
from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    CyclicRecurrence,
    ElapsedRecurrence,
    QuotaRecurrence,
    RecurrenceInputError,
    RecurrenceMutation,
    RecurrenceNotFoundError,
    RecurrenceOperationReuseError,
    RecurrencePersistenceError,
    RecurrenceSpec,
    RecurrenceStateConflictError,
    RecurrenceView,
    _arrays as _recurrence_arrays,
    _bounded_operation_id as _bounded_recurrence_operation_id,
    _error as _recurrence_error,
    _fingerprint as _recurrence_fingerprint,
    _validate as _validate_recurrence,
    _view as _recurrence_view,
)
from dante.modules.temporal.routine import (
    RoutineApplication,
    RoutineInputError,
    RoutineNotFoundError,
    RoutineOperationReuseError,
    RoutinePersistenceError,
    RoutineStateConflictError,
    RoutineView,
    _bounded as _bounded_routine_value,
    _error as _routine_error,
    _fingerprint as _routine_fingerprint,
)
from dante.platform.database.references import NativeRef, new_native_ref

RecurringOwner = Literal["routine", "event"]


class RecurringAuthoringOperationReuseError(RuntimeError):
    """The outer authoring id was reused for a different source/Recurrence intent."""


class RecurringAuthoringPersistenceError(RuntimeError):
    """The composed recurring authoring transaction could not complete safely."""


@dataclass(frozen=True, slots=True)
class RecurringAuthoringResult:
    owner_kind: RecurringOwner
    source_ref: UUID
    title: str
    created_at: datetime
    recurrence_material_state_ref: UUID
    replayed: bool


def _child_operation_id(parent: str, purpose: str) -> str:
    digest = hashlib.sha256(parent.encode("utf-8")).hexdigest()
    return f"b06d:{purpose}:{digest}"


def _routine_bootstrap(recurrence: RecurrenceSpec) -> tuple[date, time | None]:
    """Return deterministic B06-A bootstrap inputs kept transaction-internal.

    CP6/B06-A requires every Routine to be born with a Recurrence companion.
    For non-daily families that mandatory bootstrap state is immediately replaced
    inside the same transaction, so it is never externally observable as current
    truth.  No extra DDL or bypass of the governed Recurrence capability is used.
    """
    if isinstance(recurrence, ElapsedRecurrence):
        starts_on = recurrence.effective_from.astimezone(timezone.utc).date()
        return starts_on, None

    starts_on = recurrence.effective_from
    if (
        isinstance(recurrence, CalendarRecurrence)
        and recurrence.clock_basis_code == "floating_local"
        and len(recurrence.wall_times) == 1
    ):
        return starts_on, recurrence.wall_times[0]
    return starts_on, None


def _bootstrap_recurrence(starts_on: date, wall_time: time | None) -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=starts_on,
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="floating_local",
        zone_id=None,
        pattern_anchor_date=None,
        wall_times=() if wall_time is None else (wall_time,),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy=None,
        ambiguous_local_time_policy=None,
        step_unit_code=None,
    )


async def _read_recurrence_in_session(
    session: AsyncSession,
    *,
    owner: RecurringOwner,
    self_person_ref: NativeRef,
    owner_ref: UUID,
) -> RecurrenceView | None:
    try:
        row = (
            await session.execute(
                text(f"SELECT * FROM dante.get_self_{owner}_recurrence(:actor,:owner)"),
                {"actor": self_person_ref, "owner": owner_ref},
            )
        ).mappings().one_or_none()
    except DBAPIError as exc:
        raise _recurrence_error(exc) from exc
    return None if row is None else _recurrence_view(row)


async def _replace_recurrence_in_session(
    session: AsyncSession,
    *,
    owner: RecurringOwner,
    self_person_ref: NativeRef,
    owner_ref: UUID,
    operation_id: str,
    expected_material_state_ref: UUID | None,
    recurrence: RecurrenceSpec,
) -> RecurrenceMutation:
    key = _bounded_recurrence_operation_id(operation_id)
    _validate_recurrence(recurrence)
    if owner == "routine" and expected_material_state_ref is None:
        raise RecurrenceInputError(
            "Routine Recurrence replacement requires the current MaterialState reference."
        )

    fingerprint = _recurrence_fingerprint(
        owner=owner,
        owner_ref=owner_ref,
        expected_state_ref=expected_material_state_ref,
        recurrence=recurrence,
    )
    parameters: dict[str, object] = {
        "actor": self_person_ref,
        "operation": key,
        "fingerprint": fingerprint,
        "owner": owner_ref,
        "expected": expected_material_state_ref,
        "family_code": recurrence.family_code,
        "range_kind": recurrence.range_kind,
        "expected_occurrence_count": recurrence.expected_occurrence_count,
    }
    parameters.update(_recurrence_arrays(recurrence))
    statement = text(
        f"""SELECT * FROM dante.replace_self_{owner}_recurrence(
          :actor,:operation,:fingerprint,:owner,:expected,:family_code,:range_kind,:expected_occurrence_count,
          :effective_from_date,:effective_until_date,:effective_from_instant,:effective_until_instant,
          :calendar_pattern_code,:calendar_interval_count,:calendar_clock_basis_code,:calendar_zone_id,:calendar_step_unit_code,:calendar_pattern_anchor_date,
          :calendar_wall_times,:calendar_weekdays,:calendar_month_days,:calendar_ordinal_weekdays,:calendar_ordinals,:calendar_year_months,:calendar_year_month_days,
          :dst_nonexistent_local_time_policy,:dst_ambiguous_local_time_policy,:elapsed_seconds,:elapsed_anchor_mode_code,:elapsed_anchor_at,
          :quota_count,:quota_period_unit_code,:quota_period_span,:quota_frame_code,:quota_zone_id,:quota_week_start,
          :cyclic_cycle_length,:cyclic_position_unit_code,:cyclic_pattern_anchor_date,:cyclic_generates_expected)"""
    )
    try:
        receipt = (await session.execute(statement, parameters)).mappings().one()
    except DBAPIError as exc:
        raise _recurrence_error(exc) from exc

    current = await _read_recurrence_in_session(
        session,
        owner=owner,
        self_person_ref=self_person_ref,
        owner_ref=owner_ref,
    )
    if (
        current is None
        or current.material_state_ref != UUID(str(receipt["material_state_ref"]))
    ):
        raise RecurrencePersistenceError(
            "Accepted Recurrence state was not readable as current truth."
        )
    return RecurrenceMutation(
        recurrence=current,
        accepted_at=receipt["accepted_at"],
        replayed=bool(receipt["replayed"]),
    )


async def _create_routine_source_in_session(
    session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    title: str,
    life_area_ref: UUID,
    tag_refs: tuple[UUID, ...],
    starts_on: date,
    wall_time: time | None,
    application: RoutineApplication,
) -> RoutineView:
    key = _bounded_routine_value(operation_id, 200, "Operation id")
    label = _bounded_routine_value(title, 300, "Routine title")
    if len(set(tag_refs)) != len(tag_refs):
        raise RoutineInputError("Routine Tags must not contain duplicates.")
    fingerprint = _routine_fingerprint(
        {
            "version": 1,
            "kind": "create",
            "title": label,
            "life_area_ref": str(life_area_ref),
            "tag_refs": sorted(str(tag) for tag in tag_refs),
            "initial_recurrence": {
                "family": "calendar_wall_clock",
                "pattern": "daily",
                "clock_basis": "floating_local",
                "starts_on": starts_on.isoformat(),
                "wall_time": wall_time.isoformat() if wall_time else None,
            },
        }
    )
    try:
        receipt = (
            await session.execute(
                text(
                    """SELECT routine_ref,source_revision,life_area_assignment_revision,
                              accepted_at,replayed
                         FROM dante.create_self_routine(
                           :actor,:operation,:fingerprint,:routine,:title,:area,:tags,:starts_on,:wall_time)"""
                ),
                {
                    "actor": self_person_ref,
                    "operation": key,
                    "fingerprint": fingerprint,
                    "routine": uuid7(),
                    "title": label,
                    "area": life_area_ref,
                    "tags": list(tag_refs),
                    "starts_on": starts_on,
                    "wall_time": wall_time,
                },
            )
        ).mappings().one()
    except DBAPIError as exc:
        raise _routine_error(exc) from exc

    routines = await application._list_in_session(session, self_person_ref)
    view = next(
        (item for item in routines if item.routine_ref == UUID(str(receipt["routine_ref"]))),
        None,
    )
    if view is None:
        raise RoutinePersistenceError("Routine creation receipt lost its source.")
    return RoutineView(
        routine_ref=view.routine_ref,
        title=view.title,
        lifecycle_state=view.lifecycle_state,
        source_revision=view.source_revision,
        created_at=view.created_at,
        updated_at=view.updated_at,
        lifecycle_changed_at=view.lifecycle_changed_at,
        life_area_ref=view.life_area_ref,
        life_area_assignment_revision=view.life_area_assignment_revision,
        life_area_assigned_at=view.life_area_assigned_at,
        tag_refs=view.tag_refs,
        replayed=bool(receipt["replayed"]),
    )


class RecurringAuthoringApplication:
    """Transaction-owning B06-D source + Recurrence authoring composition."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._routine_application = RoutineApplication(session_factory)
        self._event_application = TemporalEventApplication(session_factory)

    async def create_routine(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_ref: UUID,
        recurrence: RecurrenceSpec,
        tag_refs: tuple[UUID, ...] = (),
    ) -> RecurringAuthoringResult:
        _validate_recurrence(recurrence)
        normalized_operation_id = _bounded_routine_value(operation_id, 200, "Operation id")
        starts_on, wall_time = _routine_bootstrap(recurrence)

        try:
            async with self._session_factory() as session, session.begin():
                source = await _create_routine_source_in_session(
                    session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=title,
                    life_area_ref=life_area_ref,
                    tag_refs=tag_refs,
                    starts_on=starts_on,
                    wall_time=wall_time,
                    application=self._routine_application,
                )
                current = await _read_recurrence_in_session(
                    session,
                    owner="routine",
                    self_person_ref=self_person_ref,
                    owner_ref=source.routine_ref,
                )
                if current is None:
                    raise RecurringAuthoringPersistenceError(
                        "Routine source was not born with its mandatory Recurrence."
                    )

                if source.replayed:
                    if current.recurrence != recurrence:
                        raise RecurringAuthoringOperationReuseError()
                    return RecurringAuthoringResult(
                        owner_kind="routine",
                        source_ref=source.routine_ref,
                        title=source.title,
                        created_at=source.created_at,
                        recurrence_material_state_ref=current.material_state_ref,
                        replayed=True,
                    )

                bootstrap = _bootstrap_recurrence(starts_on, wall_time)
                if current.recurrence != bootstrap:
                    raise RecurringAuthoringPersistenceError(
                        "Routine bootstrap Recurrence did not match the B06-A contract."
                    )
                if recurrence != bootstrap:
                    mutation = await _replace_recurrence_in_session(
                        session,
                        owner="routine",
                        self_person_ref=self_person_ref,
                        owner_ref=source.routine_ref,
                        operation_id=_child_operation_id(
                            normalized_operation_id, "routine-recurrence"
                        ),
                        expected_material_state_ref=current.material_state_ref,
                        recurrence=recurrence,
                    )
                    current = mutation.recurrence

                return RecurringAuthoringResult(
                    owner_kind="routine",
                    source_ref=source.routine_ref,
                    title=source.title,
                    created_at=source.created_at,
                    recurrence_material_state_ref=current.material_state_ref,
                    replayed=False,
                )
        except RecurringAuthoringOperationReuseError:
            raise
        except RecurrenceOperationReuseError as exc:
            raise RecurringAuthoringOperationReuseError() from exc
        except (RoutineInputError, RecurrenceInputError):
            raise
        except (
            RoutineNotFoundError,
            RoutineStateConflictError,
            RoutinePersistenceError,
            RecurrenceNotFoundError,
            RecurrenceStateConflictError,
            RecurrencePersistenceError,
        ):
            raise
        except SQLAlchemyError as exc:
            raise RecurringAuthoringPersistenceError() from exc

    async def create_event(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_ref: UUID,
        recurrence: RecurrenceSpec,
        agenda_parts: tuple[str, ...] | list[str] = (),
    ) -> RecurringAuthoringResult:
        _validate_recurrence(recurrence)
        normalized_operation_id = _normalize_event_operation_id(operation_id)
        normalized_title = _normalize_event_title(title)
        normalized_agenda = _normalize_agenda_parts(agenda_parts)

        try:
            async with self._session_factory() as session, session.begin():
                try:
                    source = await self._event_application._execute_create_event(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=normalized_operation_id,
                        title=normalized_title,
                        agenda_parts=normalized_agenda,
                        requested_event_ref=new_native_ref(),
                        life_area_ref=life_area_ref,
                    )
                except IntegrityError as exc:
                    constraint = _event_constraint_name(exc)
                    if constraint == "pk_event_create_operation":
                        raise EventOperationIdReuseError() from exc
                    if constraint == "life_area_assignment_target_unavailable":
                        raise EventLifeAreaUnavailableError() from exc
                    raise EventPersistenceError() from exc
                except DBAPIError as exc:
                    raise EventPersistenceError() from exc

                event_ref = UUID(str(source.event.event_ref))
                current = await _read_recurrence_in_session(
                    session,
                    owner="event",
                    self_person_ref=self_person_ref,
                    owner_ref=event_ref,
                )

                if source.replayed:
                    if current is None or current.recurrence != recurrence:
                        raise RecurringAuthoringOperationReuseError()
                    return RecurringAuthoringResult(
                        owner_kind="event",
                        source_ref=event_ref,
                        title=source.event.title,
                        created_at=source.event.created_at,
                        recurrence_material_state_ref=current.material_state_ref,
                        replayed=True,
                    )

                if current is not None:
                    raise RecurringAuthoringPersistenceError(
                        "New Event unexpectedly had current Recurrence truth."
                    )
                mutation = await _replace_recurrence_in_session(
                    session,
                    owner="event",
                    self_person_ref=self_person_ref,
                    owner_ref=event_ref,
                    operation_id=_child_operation_id(
                        normalized_operation_id, "event-recurrence"
                    ),
                    expected_material_state_ref=None,
                    recurrence=recurrence,
                )
                return RecurringAuthoringResult(
                    owner_kind="event",
                    source_ref=event_ref,
                    title=source.event.title,
                    created_at=source.event.created_at,
                    recurrence_material_state_ref=mutation.recurrence.material_state_ref,
                    replayed=False,
                )
        except RecurringAuthoringOperationReuseError:
            raise
        except (EventOperationIdReuseError, RecurrenceOperationReuseError) as exc:
            raise RecurringAuthoringOperationReuseError() from exc
        except (
            EventInputError,
            EventAgendaRevisionConflictError,
            RecurrenceInputError,
        ):
            raise
        except (
            EventLifeAreaUnavailableError,
            EventNotFoundError,
            EventPersistenceError,
            RecurrenceNotFoundError,
            RecurrenceStateConflictError,
            RecurrencePersistenceError,
        ):
            raise
        except SQLAlchemyError as exc:
            raise RecurringAuthoringPersistenceError() from exc
