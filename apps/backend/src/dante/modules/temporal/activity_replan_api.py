"""Coordinated Activity time revisions and planned Session replacement."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from itertools import pairwise
from typing import Annotated
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    _placement_payload,
    _revision_fingerprint,
    _unschedule_fingerprint,
    establish_schedule_in_session,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/activities", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class ReplanRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    expected_material_state_ref: UUID
    starts_local_at: datetime
    ends_local_at: datetime

    @model_validator(mode="after")
    def valid_interval(self) -> ReplanRow:
        if (self.starts_local_at.tzinfo is not None or self.ends_local_at.tzinfo is not None
                or self.ends_local_at <= self.starts_local_at):
            raise ValueError("Planning requires ordered local timestamps without an offset.")
        return self


class NewPlannedRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_ref: UUID
    name: str | None = Field(default=None, min_length=1, max_length=300)
    starts_local_at: datetime | None = None
    ends_local_at: datetime | None = None

    @model_validator(mode="after")
    def valid_interval(self) -> NewPlannedRow:
        if (self.starts_local_at is None) != (self.ends_local_at is None):
            raise ValueError("Both planned Session times must be provided together.")
        if self.starts_local_at is not None and self.ends_local_at is not None and (
            self.starts_local_at.tzinfo is not None or self.ends_local_at.tzinfo is not None
            or self.ends_local_at <= self.starts_local_at
        ):
            raise ValueError("Planning requires ordered local timestamps without an offset.")
        if self.name is not None and self.name != self.name.strip():
            raise ValueError("A planned Session name must be trimmed.")
        return self


class NewIntervalRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_ref: UUID
    starts_local_at: datetime
    ends_local_at: datetime

    @model_validator(mode="after")
    def valid_interval(self) -> NewIntervalRow:
        if (self.starts_local_at.tzinfo is not None or self.ends_local_at.tzinfo is not None
                or self.ends_local_at <= self.starts_local_at):
            raise ValueError("Activity interval requires ordered local timestamps without an offset.")
        return self


class PlacePlannedRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    starts_local_at: datetime
    ends_local_at: datetime

    @model_validator(mode="after")
    def valid_interval(self) -> PlacePlannedRow:
        if (self.starts_local_at.tzinfo is not None or self.ends_local_at.tzinfo is not None
                or self.ends_local_at <= self.starts_local_at):
            raise ValueError("Planning requires ordered local timestamps without an offset.")
        return self


class DeletePlannedRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    expected_material_state_ref: UUID | None


class ActivityReplanCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    envelope: ReplanRow | None = None
    intervals: list[ReplanRow] = Field(default_factory=list, max_length=100)
    new_intervals: list[NewIntervalRow] = Field(default_factory=list, max_length=100)
    remove_intervals: list[ReplanRow] = Field(default_factory=list, max_length=100)
    planned_sessions: list[ReplanRow] = Field(default_factory=list, max_length=100)
    place_planned_sessions: list[PlacePlannedRow] = Field(default_factory=list, max_length=100)
    new_planned_sessions: list[NewPlannedRow] = Field(default_factory=list, max_length=100)
    remove_planned_sessions: list[ReplanRow] = Field(default_factory=list, max_length=100)
    delete_planned_sessions: list[DeletePlannedRow] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def unique_new_rows(self) -> ActivityReplanCommand:
        refs = [row.client_ref for row in (*self.new_intervals, *self.new_planned_sessions)]
        if len(set(refs)) != len(refs):
            raise ValueError("New Activity interval and planned Session identities must be unique.")
        return self


class ReplanChange(BaseModel):
    schedule_ref: UUID | None = None
    client_ref: UUID | None = None
    role: str
    previous_start: datetime | None = None
    previous_end: datetime | None = None
    proposed_start: datetime | None = None
    proposed_end: datetime | None = None


class ActivityReplanPreview(BaseModel):
    activity_ref: UUID
    changes: list[ReplanChange]


def _invalid(detail: str) -> ProblemError:
    return ProblemError(
        status=422, code="temporal.activity_replan.invalid", category="validation",
        title="Invalid Activity replan", detail=detail,
    )


def _conflict(detail: str = "Reload the Activity and review the proposed times.") -> ProblemError:
    return ProblemError(
        status=409, code="temporal.activity_replan.conflict", category="conflict",
        title="Activity planning changed", detail=detail,
    )


def _validated_plan(snapshot: ActivityEditSnapshot, command: ActivityReplanCommand):
    """Pure preflight. Every dependent row is explicit, so none move silently."""
    rows = snapshot.schedules
    intervals = [row for row in rows if row.role_code == "interval"]
    envelope = next((row for row in rows if row.role_code == "envelope"), None)
    planned = [row for row in rows if row.role_code == "planned"
               and row.placement_material_state_ref is not None]
    unplaced = [row for row in rows if row.role_code == "planned"
                and row.placement_material_state_ref is None]
    if envelope is None:
        raise _invalid("This Activity does not have an editable time frame.")
    if (not intervals and (command.envelope is None or command.intervals
                           or command.new_intervals or command.remove_intervals)) or (
        intervals and command.envelope is not None
    ):
        raise _invalid("An Activity without intervals must revise its envelope directly.")
    if (len(command.intervals) + len(command.remove_intervals) != len(intervals)
            or (intervals and not command.intervals and not command.new_intervals)
            or len(command.intervals) + len(command.new_intervals) > 100
            or len(command.planned_sessions) + len(command.remove_planned_sessions)
               + sum(row.expected_material_state_ref is not None
                     for row in command.delete_planned_sessions) != len(planned)
            or len(planned) + len(unplaced) - len(command.delete_planned_sessions)
               + len(command.new_planned_sessions) > 100):
        raise _invalid(
            "Every current row must be accounted for: 1-100 Activity intervals "
            "and at most 100 planned Sessions."
        )
    current = {row.schedule_ref: row for row in (envelope, *intervals, *planned)}
    retained = (*((command.envelope,) if command.envelope else ()),
                *command.intervals, *command.planned_sessions)
    deleted_timed = tuple(row for row in command.delete_planned_sessions
                          if row.expected_material_state_ref is not None)
    accounted = (*retained, *command.remove_intervals, *command.remove_planned_sessions,
                 *deleted_timed)
    if len({row.schedule_ref for row in accounted}) != len(current) - (0 if command.envelope else 1) or (
        command.envelope is not None and command.envelope.schedule_ref != envelope.schedule_ref
    ) or (
        {row.schedule_ref for row in (*command.intervals, *command.remove_intervals)}
        != {row.schedule_ref for row in intervals}
        or {row.schedule_ref for row in (*command.planned_sessions, *command.remove_planned_sessions,
                                        *deleted_timed)}
        != {row.schedule_ref for row in planned}
    ):
        raise _invalid("A planning row is missing, repeated or assigned the wrong role.")
    if envelope.temporal_form not in {"floating_local", "named_zone_local"}:
        raise _invalid("This time frame is not supported for coordinated replanning.")
    if (len({row.schedule_ref for row in command.place_planned_sessions})
            != len(command.place_planned_sessions)
            or {row.schedule_ref for row in command.place_planned_sessions}
            - {row.schedule_ref for row in unplaced}):
        raise _invalid("An unplaced planned Session is missing or repeated.")
    deleted = {row.schedule_ref for row in command.delete_planned_sessions}
    if (len(deleted) != len(command.delete_planned_sessions)
            or deleted & {row.schedule_ref for row in command.place_planned_sessions}
            or any(row.schedule_ref not in {item.schedule_ref for item in (*planned, *unplaced)}
                   or row.expected_material_state_ref != next(
                       item.placement_material_state_ref for item in (*planned, *unplaced)
                       if item.schedule_ref == row.schedule_ref)
                   for row in command.delete_planned_sessions)):
        raise _conflict()
    for row in (envelope, *intervals, *planned):
        if (row.temporal_form != envelope.temporal_form or row.zone_id != envelope.zone_id
                or row.starts_local_at is None or row.ends_local_at is None):
            raise _invalid("All planning rows must share the Activity time frame.")
    for row in accounted:
        if row.expected_material_state_ref != current[row.schedule_ref].placement_material_state_ref:
            raise _conflict()
    ordered = sorted((*command.intervals, *command.new_intervals),
                     key=lambda row: row.starts_local_at) if intervals else [command.envelope]
    if any(a.ends_local_at > b.starts_local_at for a, b in pairwise(ordered)):
        raise _invalid("Activity intervals overlap.")
    start, end = ordered[0].starts_local_at, ordered[-1].ends_local_at
    ordered_planned = sorted((*command.planned_sessions, *command.place_planned_sessions,
                              *(row for row in command.new_planned_sessions
                                if row.starts_local_at is not None)),
                             key=lambda row: row.starts_local_at)
    if any(row.starts_local_at < start or row.ends_local_at > end for row in ordered_planned):
        raise _invalid("A planned Session falls outside the Activity envelope.")
    if any(a.ends_local_at > b.starts_local_at for a, b in pairwise(ordered_planned)):
        raise _invalid("Planned Sessions overlap.")
    if envelope.temporal_form == "named_zone_local" and not envelope.zone_id:
        raise _invalid("The Activity time zone is missing.")
    by_ref = {row.schedule_ref: row for row in retained}
    envelope_new = ReplanRow(
        schedule_ref=envelope.schedule_ref,
        expected_material_state_ref=envelope.placement_material_state_ref,
        starts_local_at=start, ends_local_at=end,
    )
    changes: list[ReplanChange] = []
    placements = []
    # Removed rows are handled by the unschedule path, never by placement revision.
    # Only retained rows can be looked up in by_ref.
    for row in (envelope, *(row for row in (*intervals, *planned)
                             if row.schedule_ref in by_ref)):
        next_row = envelope_new if row.role_code == "envelope" else by_ref[row.schedule_ref]
        if row.starts_local_at == next_row.starts_local_at and row.ends_local_at == next_row.ends_local_at:
            continue
        try:
            placement = (
                NamedZoneLocalIntervalPlacement(
                    starts_local_at=next_row.starts_local_at,
                    ends_local_at=next_row.ends_local_at,
                    zone_id=envelope.zone_id,
                ) if envelope.temporal_form == "named_zone_local" and envelope.zone_id else
                FloatingLocalIntervalPlacement(
                    starts_local_at=next_row.starts_local_at,
                    ends_local_at=next_row.ends_local_at,
                )
            )
        except ScheduleInputError as exc:
            raise _invalid(str(exc)) from exc
        changes.append(ReplanChange(
            schedule_ref=row.schedule_ref, role=row.role_code,
            previous_start=row.starts_local_at, previous_end=row.ends_local_at,
            proposed_start=next_row.starts_local_at, proposed_end=next_row.ends_local_at,
        ))
        placements.append((next_row, placement))
    for row in command.remove_intervals:
        prior = current[row.schedule_ref]
        changes.append(ReplanChange(
            schedule_ref=row.schedule_ref, role="interval_removed",
            previous_start=prior.starts_local_at, previous_end=prior.ends_local_at,
        ))
    changes.extend(
        ReplanChange(
            client_ref=row.client_ref, role="interval_added",
            proposed_start=row.starts_local_at, proposed_end=row.ends_local_at,
        ) for row in command.new_intervals
    )
    for row in command.remove_planned_sessions:
        prior = current[row.schedule_ref]
        changes.append(ReplanChange(
            schedule_ref=row.schedule_ref, role="planned_removed",
            previous_start=prior.starts_local_at, previous_end=prior.ends_local_at,
        ))
    for row in command.delete_planned_sessions:
        prior = next(item for item in (*planned, *unplaced)
                     if item.schedule_ref == row.schedule_ref)
        changes.append(ReplanChange(
            schedule_ref=row.schedule_ref, role="planned_deleted",
            previous_start=prior.starts_local_at, previous_end=prior.ends_local_at,
        ))
    changes.extend(
        ReplanChange(
            client_ref=row.client_ref, role="planned_added",
            proposed_start=row.starts_local_at, proposed_end=row.ends_local_at,
        ) for row in command.new_planned_sessions
    )
    changes.extend(ReplanChange(
        schedule_ref=row.schedule_ref, role="planned_placed",
        proposed_start=row.starts_local_at, proposed_end=row.ends_local_at,
    ) for row in command.place_planned_sessions)
    return changes, placements


async def _read(session, actor: UUID, activity: UUID) -> ActivityEditSnapshot:
    payload = await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity})
    if payload is None:
        raise ProblemError(
            status=404, code="temporal.activity_replan.not_found", category="not_found",
            title="Activity unavailable", detail="Activity unavailable in self scope.",
        )
    return ActivityEditSnapshot.model_validate(payload)


@router.post(
    "/{activity_ref}/replan-preview", response_model=ActivityReplanPreview,
    operation_id="temporal_preview_activity_replan",
)
async def preview_activity_replan(
    activity_ref: UUID, body: ActivityReplanCommand,
    context: ReadContext, request: Request, response: Response,
) -> ActivityReplanPreview:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            snapshot = await _read(session, context.self_person_ref, activity_ref)
            changes, _ = _validated_plan(snapshot, body)
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.activity_replan.unavailable", category="service",
            title="Planning unavailable", detail="Could not read Activity planning.",
            retryable=True,
        ) from exc
    return ActivityReplanPreview(activity_ref=activity_ref, changes=changes)


@router.put(
    "/{activity_ref}/replan", response_model=ActivityEditSnapshot,
    operation_id="temporal_apply_activity_replan",
)
async def apply_activity_replan(
    activity_ref: UUID, body: ActivityReplanCommand,
    context: WriteContext, request: Request, response: Response,
) -> ActivityEditSnapshot:
    response.headers["Cache-Control"] = "no-store"
    digest = hashlib.sha256(body.operation_id.encode("utf-8")).hexdigest()
    actor = context.self_person_ref
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            snapshot = await _read(session, actor, activity_ref)
            _, placements = _validated_plan(snapshot, body)
            changes_required = bool(
                placements or body.remove_intervals or body.new_intervals
                or body.remove_planned_sessions or body.new_planned_sessions
                or body.place_planned_sessions or body.delete_planned_sessions
            )
            # Historical execution is immutable. Current open execution and accepted
            # realization close ordinary planning edits for this bounded command.
            if changes_required and await session.scalar(text("""
                    SELECT EXISTS(SELECT 1 FROM dante.list_self_subject_sessions(:actor,:activity)
                                   WHERE ended_at IS NULL)
                        OR EXISTS(SELECT 1 FROM dante.get_self_subject_actual(
                            :actor,'activity',:activity))
                """), {"actor": actor, "activity": activity_ref}):
                raise _conflict("This Activity has open execution or accepted realization.")
            envelope = next(row for row in snapshot.schedules if row.role_code == "envelope")
            if changes_required and await session.scalar(text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """), {"actor": actor, "schedule": envelope.schedule_ref}):
                raise _conflict("Unlock the Activity placement before replanning.")
            for row in body.remove_intervals:
                if await session.scalar(text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """), {"actor": actor, "schedule": row.schedule_ref}):
                    raise _conflict("Unlock the Activity interval before removing it.")
            for row in (*body.remove_planned_sessions, *body.delete_planned_sessions):
                if await session.scalar(text("""
                    SELECT EXISTS(
                        SELECT 1
                          FROM dante.list_self_subject_sessions(:actor,:activity) AS execution
                         WHERE dante.get_self_session_planned_schedule(
                             :actor,execution.session_ref)=:schedule
                    )
                """), {"actor": actor, "activity": activity_ref,
                       "schedule": row.schedule_ref}):
                    raise _conflict("A planned Session with recorded execution cannot be removed.")
                if await session.scalar(text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """), {"actor": actor, "schedule": row.schedule_ref}):
                    raise _conflict("Unlock the planned Session before removing it.")
            for row, placement in placements:
                locked = await session.scalar(text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """), {"actor": actor, "schedule": row.schedule_ref})
                if locked:
                    raise _conflict("Unlock the Activity placement before replanning.")
                await session.execute(text("""
                    SELECT * FROM dante.revise_self_schedule_placement(
                        :actor,:operation,:fingerprint,:schedule,:expected,
                        :state,CAST(:placement AS jsonb))
                """), {
                    "actor": actor,
                    "operation": f"replan:{digest}:{row.schedule_ref}",
                    "fingerprint": _revision_fingerprint(
                        schedule_ref=ScopedRecordRef(row.schedule_ref),
                        expected_material_state_ref=MaterialStateRef(
                            row.expected_material_state_ref), placement=placement,
                    ),
                    "schedule": row.schedule_ref,
                    "expected": row.expected_material_state_ref,
                    "state": uuid7(),
                    "placement": json.dumps(_placement_payload(placement), sort_keys=True),
                })
            for row in (*body.remove_intervals, *body.remove_planned_sessions,
                        *(item for item in body.delete_planned_sessions
                          if item.expected_material_state_ref is not None)):
                await session.execute(text("""
                    SELECT * FROM dante.unschedule_self_schedule(
                        :actor,:operation,:fingerprint,:schedule,:expected)
                """), {
                    "actor": actor,
                    "operation": f"replan:remove:{digest}:{row.schedule_ref}",
                    "fingerprint": _unschedule_fingerprint(
                        schedule_ref=ScopedRecordRef(row.schedule_ref),
                        expected_material_state_ref=MaterialStateRef(row.expected_material_state_ref),
                    ),
                    "schedule": row.schedule_ref,
                    "expected": row.expected_material_state_ref,
                })
            for row in body.delete_planned_sessions:
                await session.execute(text("""
                    SELECT dante.retire_self_planned_schedule(:actor,:activity,:schedule)
                """), {
                    "actor": actor, "activity": activity_ref,
                    "schedule": row.schedule_ref,
                })
            for row in body.place_planned_sessions:
                if await session.scalar(text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """), {"actor": actor, "schedule": row.schedule_ref}):
                    raise _conflict("Unlock the planned Session before placing it.")
                try:
                    placement = (
                        NamedZoneLocalIntervalPlacement(
                            starts_local_at=row.starts_local_at,
                            ends_local_at=row.ends_local_at, zone_id=envelope.zone_id,
                        ) if envelope.temporal_form == "named_zone_local" else
                        FloatingLocalIntervalPlacement(
                            starts_local_at=row.starts_local_at, ends_local_at=row.ends_local_at,
                        )
                    )
                except ScheduleInputError as exc:
                    raise _invalid(str(exc)) from exc
                payload = _placement_payload(placement)
                await session.execute(text("""
                    SELECT * FROM dante.place_self_unplaced_planned_schedule(
                        :actor,:operation,:fingerprint,:activity,:schedule,:state,
                        CAST(:placement AS jsonb))
                """), {
                    "actor": actor, "operation": f"replan:place:{digest}:{row.schedule_ref}",
                    "fingerprint": hashlib.sha256(json.dumps({
                        "activity": str(activity_ref), "schedule": str(row.schedule_ref),
                        "placement": payload,
                    }, sort_keys=True).encode()).hexdigest(),
                    "activity": activity_ref, "schedule": row.schedule_ref,
                    "state": uuid7(), "placement": json.dumps(payload, sort_keys=True),
                })
            if body.new_intervals:
                next_interval_order = await session.scalar(text("""
                    SELECT COALESCE(MAX(presentation_order),0)
                      FROM dante.get_self_activity_schedule_roles(
                          :actor, CAST(ARRAY[:activity] AS uuid[]))
                     WHERE role_code='interval'
                """), {"actor": actor, "activity": activity_ref})
                for row in body.new_intervals:
                    next_interval_order += 1
                    try:
                        placement = (
                            NamedZoneLocalIntervalPlacement(
                                starts_local_at=row.starts_local_at,
                                ends_local_at=row.ends_local_at,
                                zone_id=envelope.zone_id,
                            ) if envelope.temporal_form == "named_zone_local" else
                            FloatingLocalIntervalPlacement(
                                starts_local_at=row.starts_local_at,
                                ends_local_at=row.ends_local_at,
                            )
                        )
                    except ScheduleInputError as exc:
                        raise _invalid(str(exc)) from exc
                    created = await establish_schedule_in_session(
                        session, self_person_ref=NativeRef(actor),
                        operation_id=f"replan:add-interval:{digest}:{row.client_ref}",
                        subject_native_ref=NativeRef(activity_ref), placement=placement,
                    )
                    await session.execute(text("""
                        SELECT * FROM dante.set_self_activity_schedule_role(
                            :actor,:activity,:schedule,'interval',:position,NULL)
                    """), {
                        "actor": actor, "activity": activity_ref,
                        "schedule": created.schedule_ref,
                        "position": next_interval_order,
                    })
            if body.new_planned_sessions:
                used_orders = set((await session.scalars(text("""
                    SELECT presentation_order
                      FROM dante.get_self_activity_schedule_roles(
                          :actor, CAST(ARRAY[:activity] AS uuid[]))
                     WHERE role_code='planned'
                """), {"actor": actor, "activity": activity_ref})).all())
                last_order = max(used_orders, default=0)
                free_orders = [position for position in range(last_order + 1, 101)
                               if position not in used_orders]
                free_orders += [position for position in range(1, last_order + 1)
                                if position not in used_orders]
                if len(free_orders) < len(body.new_planned_sessions):
                    raise _invalid("At most 100 current planned Sessions are supported.")
                for row, next_order in zip(body.new_planned_sessions, free_orders, strict=True):
                    if row.starts_local_at is None:
                        await session.execute(text("""
                            SELECT * FROM dante.establish_self_unplaced_planned_schedule(
                                :actor,:activity,:schedule,:position,:name)
                        """), {
                            "actor": actor, "activity": activity_ref,
                            "schedule": uuid7(), "position": next_order, "name": row.name,
                        })
                        continue
                    try:
                        placement = (
                            NamedZoneLocalIntervalPlacement(
                                starts_local_at=row.starts_local_at,
                                ends_local_at=row.ends_local_at,
                                zone_id=envelope.zone_id,
                            ) if envelope.temporal_form == "named_zone_local" else
                            FloatingLocalIntervalPlacement(
                                starts_local_at=row.starts_local_at,
                                ends_local_at=row.ends_local_at,
                            )
                        )
                    except ScheduleInputError as exc:
                        raise _invalid(str(exc)) from exc
                    created = await establish_schedule_in_session(
                        session, self_person_ref=NativeRef(actor),
                        operation_id=f"replan:add:{digest}:{row.client_ref}",
                        subject_native_ref=NativeRef(activity_ref), placement=placement,
                    )
                    await session.execute(text("""
                        SELECT * FROM dante.set_self_activity_schedule_role(
                            :actor,:activity,:schedule,'planned',:position,:name)
                    """), {
                        "actor": actor, "activity": activity_ref,
                        "schedule": created.schedule_ref,
                        "position": next_order, "name": row.name,
                    })
            return await _read(session, actor, activity_ref)
    except DBAPIError as exc:
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
        if (getattr(exc.orig, "sqlstate", None) in {"40001", "23505"}
                or (constraint and (constraint.endswith(("_conflict", "_stale", "_locked"))
                                   or "revision" in constraint
                                   or "expected_state" in constraint))):
            raise _conflict() from exc
        raise ProblemError(
            status=503, code="temporal.activity_replan.unavailable", category="service",
            title="Planning unavailable", detail="The replan could not be saved.",
            retryable=True,
        ) from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.activity_replan.unavailable", category="service",
            title="Planning unavailable", detail="The replan could not be saved.",
            retryable=True,
        ) from exc
