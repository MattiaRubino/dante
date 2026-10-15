"""Coordinated Activity time revisions and planned Session replacement."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from itertools import pairwise
from typing import Annotated, Literal
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    _placement_payload,
    _revision_fingerprint,
    _unschedule_fingerprint,
    _unschedule_undo_fingerprint,
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
        if (
            self.starts_local_at.tzinfo is not None
            or self.ends_local_at.tzinfo is not None
            or self.ends_local_at <= self.starts_local_at
        ):
            raise ValueError("Planning requires ordered local timestamps without an offset.")
        return self


class NewPlannedRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_ref: UUID
    name: str | None = Field(default=None, min_length=1, max_length=300)

    @model_validator(mode="after")
    def valid_interval(self) -> NewPlannedRow:
        if self.name is not None and self.name != self.name.strip():
            raise ValueError("A planned Session name must be trimmed.")
        return self


class RetainedPlannedRow(BaseModel):
    """A named internal Session retained by an Activity edit.

    It has identity and order, but deliberately no calendar placement.
    """

    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    expected_material_state_ref: UUID | None = None


class NewIntervalRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_ref: UUID
    starts_local_at: datetime
    ends_local_at: datetime

    @model_validator(mode="after")
    def valid_interval(self) -> NewIntervalRow:
        if (
            self.starts_local_at.tzinfo is not None
            or self.ends_local_at.tzinfo is not None
            or self.ends_local_at <= self.starts_local_at
        ):
            raise ValueError(
                "Activity interval requires ordered local timestamps without an offset."
            )
        return self


class PlacePlannedRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    starts_local_at: datetime
    ends_local_at: datetime

    @model_validator(mode="after")
    def valid_interval(self) -> PlacePlannedRow:
        if (
            self.starts_local_at.tzinfo is not None
            or self.ends_local_at.tzinfo is not None
            or self.ends_local_at <= self.starts_local_at
        ):
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
    planned_sessions: list[RetainedPlannedRow] = Field(default_factory=list, max_length=100)
    # Retained only for an explicit validation error for stale clients. Named
    # Sessions no longer have their own placement.
    place_planned_sessions: list[PlacePlannedRow] = Field(default_factory=list, max_length=0)
    new_planned_sessions: list[NewPlannedRow] = Field(default_factory=list, max_length=100)
    remove_planned_sessions: list[RetainedPlannedRow] = Field(default_factory=list, max_length=0)
    delete_planned_sessions: list[DeletePlannedRow] = Field(default_factory=list, max_length=100)
    session_disposition: Literal["keep", "delete"] | None = None
    expected_session_fingerprint: str | None = Field(
        default=None, pattern=r"^[a-f0-9]{64}$"
    )

    @model_validator(mode="after")
    def unique_new_rows(self) -> ActivityReplanCommand:
        refs = [row.client_ref for row in self.new_intervals] + [
            row.client_ref for row in self.new_planned_sessions
        ]
        if len(set(refs)) != len(refs):
            raise ValueError("New Activity interval and planned Session identities must be unique.")
        if (self.session_disposition is None) != (
            self.expected_session_fingerprint is None
        ):
            raise ValueError("Session disposition requires its expected impact fingerprint.")
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
        status=422,
        code="temporal.activity_replan.invalid",
        category="validation",
        title="Invalid Activity replan",
        detail=detail,
    )


def _conflict(detail: str = "Reload the Activity and review the proposed times.") -> ProblemError:
    return ProblemError(
        status=409,
        code="temporal.activity_replan.conflict",
        category="conflict",
        title="Activity planning changed",
        detail=detail,
    )


def _validated_plan(
    snapshot: ActivityEditSnapshot,
    command: ActivityReplanCommand,
) -> tuple[
    list[ReplanChange],
    list[tuple[ReplanRow, FloatingLocalIntervalPlacement | NamedZoneLocalIntervalPlacement]],
]:
    """Pure preflight. Every dependent row is explicit, so none move silently."""
    rows = snapshot.schedules
    intervals = [row for row in rows if row.role_code == "interval"]
    envelope = next((row for row in rows if row.role_code == "envelope"), None)
    planned = [row for row in rows if row.role_code == "planned"]
    if envelope is None:
        raise _invalid("This Activity does not have an editable time frame.")
    if (
        not intervals
        and (
            command.envelope is None
            or command.intervals
            or command.new_intervals
            or command.remove_intervals
        )
    ) or (intervals and command.envelope is not None):
        raise _invalid("An Activity without intervals must revise its envelope directly.")
    if (
        len(command.intervals) + len(command.remove_intervals) != len(intervals)
        or (intervals and not command.intervals and not command.new_intervals)
        or len(command.intervals) + len(command.new_intervals) > 100
        or len(command.planned_sessions) + len(command.delete_planned_sessions) != len(planned)
        or len(planned) - len(command.delete_planned_sessions) + len(command.new_planned_sessions)
        > 100
    ):
        raise _invalid(
            "Every current row must be accounted for: 1-100 Activity intervals "
            "and at most 100 planned Sessions."
        )
    current = {row.schedule_ref: row for row in (envelope, *intervals)}
    retained: list[ReplanRow] = [
        *((command.envelope,) if command.envelope else ()),
        *command.intervals,
    ]
    accounted: list[ReplanRow] = [*retained, *command.remove_intervals]
    if (
        len({row.schedule_ref for row in accounted})
        != len(current) - (0 if command.envelope else 1)
        or (command.envelope is not None and command.envelope.schedule_ref != envelope.schedule_ref)
        or (
            {row.schedule_ref for row in (*command.intervals, *command.remove_intervals)}
            != {row.schedule_ref for row in intervals}
            or {row.schedule_ref for row in command.planned_sessions}
            | {row.schedule_ref for row in command.delete_planned_sessions}
            != {row.schedule_ref for row in planned}
        )
    ):
        raise _invalid("A planning row is missing, repeated or assigned the wrong role.")
    if envelope.temporal_form not in {"floating_local", "named_zone_local"}:
        raise _invalid("This time frame is not supported for coordinated replanning.")
    deleted = {row.schedule_ref for row in command.delete_planned_sessions}
    if len(deleted) != len(command.delete_planned_sessions) or deleted | {
        row.schedule_ref for row in command.planned_sessions
    } != {row.schedule_ref for row in planned}:
        raise _conflict()
    planned_by_ref = {row.schedule_ref: row for row in planned}
    planned_basis = [
        (row.schedule_ref, row.expected_material_state_ref) for row in command.planned_sessions
    ] + [
        (row.schedule_ref, row.expected_material_state_ref)
        for row in command.delete_planned_sessions
    ]
    if any(
        state_ref != planned_by_ref[schedule_ref].placement_material_state_ref
        for schedule_ref, state_ref in planned_basis
    ):
        raise _conflict()
    for row in (envelope, *intervals):
        if (
            row.temporal_form != envelope.temporal_form
            or row.zone_id != envelope.zone_id
            or row.starts_local_at is None
            or row.ends_local_at is None
        ):
            raise _invalid("All planning rows must share the Activity time frame.")
    for accounted_row in accounted:
        if (
            accounted_row.expected_material_state_ref
            != current[accounted_row.schedule_ref].placement_material_state_ref
        ):
            raise _conflict()
    # Normalize the typed intervals to pairs before sorting. Python's mixed
    # Pydantic-model tuple otherwise infers only BaseModel in mypy and loses
    # the fields shared by ReplanRow, NewIntervalRow and PlacePlannedRow.
    if intervals:
        ordered_spans = sorted(
            [(row.starts_local_at, row.ends_local_at) for row in command.intervals]
            + [(row.starts_local_at, row.ends_local_at) for row in command.new_intervals],
            key=lambda span: span[0],
        )
    else:
        if command.envelope is None:
            raise _invalid("An Activity without intervals must revise its envelope.")
        ordered_spans = [(command.envelope.starts_local_at, command.envelope.ends_local_at)]
    if any(a[1] > b[0] for a, b in pairwise(ordered_spans)):
        raise _invalid("Activity intervals overlap.")
    start, end = ordered_spans[0][0], ordered_spans[-1][1]

    if envelope.temporal_form == "named_zone_local" and not envelope.zone_id:
        raise _invalid("The Activity time zone is missing.")
    by_ref = {row.schedule_ref: row for row in retained}
    if envelope.placement_material_state_ref is None:
        raise _invalid("The Activity envelope requires an accepted current placement.")
    envelope_new = ReplanRow(
        schedule_ref=envelope.schedule_ref,
        expected_material_state_ref=envelope.placement_material_state_ref,
        starts_local_at=start,
        ends_local_at=end,
    )
    changes: list[ReplanChange] = []
    placements: list[
        tuple[ReplanRow, FloatingLocalIntervalPlacement | NamedZoneLocalIntervalPlacement]
    ] = []
    # Removed rows are handled by the unschedule path, never by placement revision.
    # Only retained rows can be looked up in by_ref.
    for existing_row in (
        envelope,
        *(schedule for schedule in intervals if schedule.schedule_ref in by_ref),
    ):
        next_row = (
            envelope_new
            if existing_row.role_code == "envelope"
            else by_ref[existing_row.schedule_ref]
        )
        if (
            existing_row.starts_local_at == next_row.starts_local_at
            and existing_row.ends_local_at == next_row.ends_local_at
        ):
            continue
        try:
            placement = (
                NamedZoneLocalIntervalPlacement(
                    starts_local_at=next_row.starts_local_at,
                    ends_local_at=next_row.ends_local_at,
                    zone_id=_checked_zone(envelope),
                )
                if envelope.temporal_form == "named_zone_local" and envelope.zone_id
                else FloatingLocalIntervalPlacement(
                    starts_local_at=next_row.starts_local_at,
                    ends_local_at=next_row.ends_local_at,
                )
            )
        except ScheduleInputError as exc:
            raise _invalid(str(exc)) from exc
        if existing_row.role_code is None:
            raise _invalid("An Activity Schedule role is missing.")
        changes.append(
            ReplanChange(
                schedule_ref=existing_row.schedule_ref,
                role=existing_row.role_code,
                previous_start=existing_row.starts_local_at,
                previous_end=existing_row.ends_local_at,
                proposed_start=next_row.starts_local_at,
                proposed_end=next_row.ends_local_at,
            )
        )
        placements.append((next_row, placement))
    for removed_interval in command.remove_intervals:
        prior = current[removed_interval.schedule_ref]
        changes.append(
            ReplanChange(
                schedule_ref=removed_interval.schedule_ref,
                role="interval_removed",
                previous_start=prior.starts_local_at,
                previous_end=prior.ends_local_at,
            )
        )
    changes.extend(
        ReplanChange(
            client_ref=row.client_ref,
            role="interval_added",
            proposed_start=row.starts_local_at,
            proposed_end=row.ends_local_at,
        )
        for row in command.new_intervals
    )
    changes.extend(
        ReplanChange(schedule_ref=row.schedule_ref, role="planned_deleted")
        for row in command.delete_planned_sessions
    )
    changes.extend(
        ReplanChange(client_ref=row.client_ref, role="planned_added")
        for row in command.new_planned_sessions
    )
    return changes, placements


def _checked_zone(envelope: ActivityScheduleResponse) -> str:
    if envelope.zone_id is None:
        raise _invalid("The Activity time zone is missing.")
    return envelope.zone_id


async def _read(session: AsyncSession, actor: UUID, activity: UUID) -> ActivityEditSnapshot:
    payload = await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity})
    if payload is None:
        raise ProblemError(
            status=404,
            code="temporal.activity_replan.not_found",
            category="not_found",
            title="Activity unavailable",
            detail="Activity unavailable in self scope.",
        )
    return ActivityEditSnapshot.model_validate(payload)


@router.post(
    "/{activity_ref}/replan-preview",
    response_model=ActivityReplanPreview,
    operation_id="temporal_preview_activity_replan",
)
async def preview_activity_replan(
    activity_ref: UUID,
    body: ActivityReplanCommand,
    context: ReadContext,
    request: Request,
    response: Response,
) -> ActivityReplanPreview:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            snapshot = await _read(session, context.self_person_ref, activity_ref)
            changes, _ = _validated_plan(snapshot, body)
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity_replan.unavailable",
            category="service",
            title="Planning unavailable",
            detail="Could not read Activity planning.",
            retryable=True,
        ) from exc
    return ActivityReplanPreview(activity_ref=activity_ref, changes=changes)


@router.put(
    "/{activity_ref}/replan",
    response_model=ActivityEditSnapshot,
    operation_id="temporal_apply_activity_replan",
)
async def apply_activity_replan(
    activity_ref: UUID,
    body: ActivityReplanCommand,
    context: WriteContext,
    request: Request,
    response: Response,
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
                placements
                or body.remove_intervals
                or body.new_intervals
                or body.new_planned_sessions
                or body.delete_planned_sessions
            )
            # Accepted v2 lifecycle: planning never rewrites real attempts.
            # A deliberate Keep/Delete decision is required when attempts exist,
            # and the DB checks its CAS token again under SERIALIZABLE isolation.
            current_session_fingerprint = await session.scalar(
                text("SELECT dante.get_self_activity_session_impact_hash(:actor,:activity)"),
                {"actor": actor, "activity": activity_ref},
            )
            attempts_present = bool(
                await session.scalar(
                    text("""
                        SELECT EXISTS(
                            SELECT 1 FROM dante.list_self_subject_sessions(:actor,:activity)
                        )
                    """),
                    {"actor": actor, "activity": activity_ref},
                )
            )
            if changes_required and attempts_present and body.session_disposition is None:
                raise _conflict("Scegli Mantieni Sessioni, Elimina Sessioni o Annulla.")
            if body.session_disposition is not None:
                if (
                    current_session_fingerprint is None
                    or current_session_fingerprint != body.expected_session_fingerprint
                ):
                    raise _conflict("Session attempts changed. Reload before confirming.")
                if body.session_disposition == "delete":
                    await session.scalar(
                        text("""
                            SELECT dante.delete_self_activity_sessions(
                                :actor,:activity,:fingerprint
                            )
                        """),
                        {
                            "actor": actor,
                            "activity": activity_ref,
                            "fingerprint": current_session_fingerprint,
                        },
                    )
            envelope = next(row for row in snapshot.schedules if row.role_code == "envelope")
            # A placement lock freezes existing Schedule coordinates, not new
            # Activity structure. Adding a planned Session inside the already
            # accepted envelope (timed or untimed) does not move that envelope.
            # Real placement revisions, removals and interval changes stay guarded.
            existing_placement_changes = bool(
                placements
                or body.remove_intervals
                or body.new_intervals
                or body.delete_planned_sessions
            )
            if existing_placement_changes and await session.scalar(
                text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """),
                {"actor": actor, "schedule": envelope.schedule_ref},
            ):
                raise _conflict("Unlock the Activity placement before replanning.")
            for removed_interval in body.remove_intervals:
                if await session.scalar(
                    text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """),
                    {"actor": actor, "schedule": removed_interval.schedule_ref},
                ):
                    raise _conflict("Unlock the Activity interval before removing it.")
            for removed_schedule in body.delete_planned_sessions:
                if await session.scalar(
                    text(
                        "SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)"
                    ),
                    {"actor": actor, "schedule": removed_schedule.schedule_ref},
                ):
                    raise _conflict("Unlock the named Session placement before removing it.")
            for revised_schedule, placement in placements:
                locked = await session.scalar(
                    text("""
                    SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)
                """),
                    {"actor": actor, "schedule": revised_schedule.schedule_ref},
                )
                if locked:
                    raise _conflict("Unlock the Activity placement before replanning.")
                await session.execute(
                    text("""
                    SELECT * FROM dante.revise_self_schedule_placement(
                        :actor,:operation,:fingerprint,:schedule,:expected,
                        :state,CAST(:placement AS jsonb))
                """),
                    {
                        "actor": actor,
                        "operation": f"replan:{digest}:{revised_schedule.schedule_ref}",
                        "fingerprint": _revision_fingerprint(
                            schedule_ref=ScopedRecordRef(revised_schedule.schedule_ref),
                            expected_material_state_ref=MaterialStateRef(
                                revised_schedule.expected_material_state_ref
                            ),
                            placement=placement,
                        ),
                        "schedule": revised_schedule.schedule_ref,
                        "expected": revised_schedule.expected_material_state_ref,
                        "state": uuid7(),
                        "placement": json.dumps(_placement_payload(placement), sort_keys=True),
                    },
                )
            unscheduled_rows = [
                (item.schedule_ref, item.expected_material_state_ref)
                for item in body.remove_intervals
            ]
            for schedule_ref, expected_state in unscheduled_rows:
                await session.execute(
                    text("""
                    SELECT * FROM dante.unschedule_self_schedule(
                        :actor,:operation,:fingerprint,:schedule,:expected)
                    """),
                    {
                        "actor": actor,
                        "operation": f"replan:remove:{digest}:{schedule_ref}",
                        "fingerprint": _unschedule_fingerprint(
                            schedule_ref=ScopedRecordRef(schedule_ref),
                            expected_material_state_ref=MaterialStateRef(expected_state),
                        ),
                        "schedule": schedule_ref,
                        "expected": expected_state,
                    },
                )
            for retired_row in body.delete_planned_sessions:
                # X is draft-only until Save. Here both the named configuration
                # and its linked real attempts disappear in the SAME transaction;
                # the other retained Session attempts remain unchanged.
                current_session_fingerprint = await session.scalar(
                    text("SELECT dante.get_self_activity_session_impact_hash(:actor,:activity)"),
                    {"actor": actor, "activity": activity_ref},
                )
                await session.scalar(
                    text("""
                        SELECT dante.delete_self_named_activity_session(
                            :actor,:activity,:schedule,:fingerprint
                        )
                    """),
                    {
                        "actor": actor,
                        "activity": activity_ref,
                        "schedule": retired_row.schedule_ref,
                        "fingerprint": current_session_fingerprint,
                    },
                )
            if body.new_intervals:
                next_interval_order = await session.scalar(
                    text("""
                    SELECT COALESCE(MAX(presentation_order),0)
                      FROM dante.get_self_activity_schedule_roles(
                          :actor, CAST(ARRAY[:activity] AS uuid[]))
                     WHERE role_code='interval'
                """),
                    {"actor": actor, "activity": activity_ref},
                )
                for new_interval in body.new_intervals:
                    next_interval_order += 1
                    try:
                        placement = (
                            NamedZoneLocalIntervalPlacement(
                                starts_local_at=new_interval.starts_local_at,
                                ends_local_at=new_interval.ends_local_at,
                                zone_id=_checked_zone(envelope),
                            )
                            if envelope.temporal_form == "named_zone_local"
                            else FloatingLocalIntervalPlacement(
                                starts_local_at=new_interval.starts_local_at,
                                ends_local_at=new_interval.ends_local_at,
                            )
                        )
                    except ScheduleInputError as exc:
                        raise _invalid(str(exc)) from exc
                    created = await establish_schedule_in_session(
                        session,
                        self_person_ref=NativeRef(actor),
                        operation_id=f"replan:add-interval:{digest}:{new_interval.client_ref}",
                        subject_native_ref=NativeRef(activity_ref),
                        placement=placement,
                    )
                    await session.execute(
                        text("""
                        SELECT * FROM dante.set_self_activity_schedule_role(
                            :actor,:activity,:schedule,'interval',:position,NULL)
                    """),
                        {
                            "actor": actor,
                            "activity": activity_ref,
                            "schedule": created.schedule_ref,
                            "position": next_interval_order,
                        },
                    )
            if body.new_planned_sessions:
                used_orders = set(
                    (
                        await session.scalars(
                            text("""
                    SELECT presentation_order
                      FROM dante.get_self_activity_schedule_roles(
                          :actor, CAST(ARRAY[:activity] AS uuid[]))
                     WHERE role_code='planned'
                """),
                            {"actor": actor, "activity": activity_ref},
                        )
                    ).all()
                )
                last_order = max(used_orders, default=0)
                free_orders = [
                    position
                    for position in range(last_order + 1, 101)
                    if position not in used_orders
                ]
                free_orders += [
                    position for position in range(1, last_order + 1) if position not in used_orders
                ]
                if len(free_orders) < len(body.new_planned_sessions):
                    raise _invalid("At most 100 current planned Sessions are supported.")
                for new_planned, next_order in zip(
                    body.new_planned_sessions,
                    free_orders[: len(body.new_planned_sessions)],
                    strict=True,
                ):
                    await session.execute(
                        text("""
                        SELECT * FROM dante.establish_self_unplaced_planned_schedule(
                            :actor,:activity,:schedule,:position,:name)
                    """),
                        {
                            "actor": actor,
                            "activity": activity_ref,
                            "schedule": uuid7(),
                            "position": next_order,
                            "name": new_planned.name,
                        },
                    )
            return await _read(session, actor, activity_ref)
    except DBAPIError as exc:
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
        if getattr(exc.orig, "sqlstate", None) in {"40001", "23505"} or (
            constraint
            and (
                constraint.endswith(("_conflict", "_stale", "_locked"))
                or "revision" in constraint
                or "expected_state" in constraint
            )
        ):
            raise _conflict() from exc
        raise ProblemError(
            status=503,
            code="temporal.activity_replan.unavailable",
            category="service",
            title="Planning unavailable",
            detail="The replan could not be saved.",
            retryable=True,
        ) from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity_replan.unavailable",
            category="service",
            title="Planning unavailable",
            detail="The replan could not be saved.",
            retryable=True,
        ) from exc


# A Timeline removal is a Schedule mutation, NOT the hard deletion of an
# Activity or any historical Session. The public generic Schedule paths
# deliberately fail closed for interval-governed Activity schedules.
class ActivityTimelineUnplaceCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    schedule_ref: UUID
    expected_material_state_ref: UUID
    session_disposition: Literal["keep", "delete"] | None = None
    expected_session_fingerprint: str | None = Field(
        default=None, pattern=r"^[0-9a-f]{64}$"
    )

    @model_validator(mode="after")
    def paired_session_decision(self) -> ActivityTimelineUnplaceCommand:
        if (self.session_disposition is None) != (
            self.expected_session_fingerprint is None
        ):
            raise ValueError("Session choice must carry the current impact fingerprint.")
        return self


class ActivityTimelineUndoCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    schedule_ref: UUID
    unschedule_operation_id: str = Field(min_length=1, max_length=200)
    expected_session_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")


class ActivityTimelineMutationResult(BaseModel):
    activity_ref: UUID
    schedule_ref: UUID
    operation_id: str
    placement_material_state_ref: UUID | None


class ActivityTimelineUndoReceipt(BaseModel):
    schedule_ref: UUID
    unschedule_operation_id: str


async def _guard_timeline_role(
    session: AsyncSession,
    actor: UUID,
    activity_ref: UUID,
    schedule_ref: UUID,
    *,
    require_current: bool,
) -> str:
    role = await session.scalar(
        text("""
            SELECT role.role_code
              FROM dante.activity_intention AS owned
              JOIN dante.schedule AS schedule
                ON schedule.subject_native_ref=owned.activity_ref
              JOIN dante.get_self_activity_schedule_roles(
                :actor,CAST(ARRAY[:activity] AS uuid[])
              ) AS role ON role.schedule_ref=schedule.schedule_ref
             WHERE owned.activity_ref=:activity
               AND owned.self_person_ref=:actor
               AND owned.retired_at IS NULL
               AND schedule.schedule_ref=:schedule
        """),
        {"actor": actor, "activity": activity_ref, "schedule": schedule_ref},
    )
    if role not in {"envelope", "interval"}:
        raise _conflict("La Schedule non appartiene all'Activity selezionata.")
    if require_current:
        siblings = await session.scalar(
            text("""
                SELECT count(*)
                  FROM dante.get_self_activity_schedule_roles(
                      :actor,CAST(ARRAY[:activity] AS uuid[])
                  ) AS role
                  JOIN dante.schedule_current_placement AS current
                    ON current.scoped_owner_ref=role.schedule_ref
                 WHERE role.role_code='interval'
                   AND role.schedule_ref<>:schedule
            """),
            {"actor": actor, "activity": activity_ref, "schedule": schedule_ref},
        )
        # With sibling intervals the envelope is their factual plan bounding
        # identity. Removing only the envelope would leave an invalid plan.
        if role == "envelope" and siblings:
            raise _conflict(
                "L'Activity contiene intervalli attivi: rimuovili con il replan coordinato."
            )
    locked = await session.scalar(
        text("SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)"),
        {"actor": actor, "schedule": schedule_ref},
    )
    if locked:
        raise _conflict("Sblocca la collocazione prima di modificarla.")
    return role


async def _timeline_session_guard(
    session: AsyncSession, actor: UUID, activity_ref: UUID,
    expected_fingerprint: str | None, disposition: str | None,
) -> str:
    impact = await session.scalar(
        text("SELECT dante.get_self_activity_session_impact_hash(:actor,:activity)"),
        {"actor": actor, "activity": activity_ref},
    )
    if impact is None:
        raise _conflict("Activity non più disponibile.")
    if expected_fingerprint is not None and impact != expected_fingerprint:
        raise _conflict("Le Sessioni sono cambiate: ricarica e riprova.")
    if disposition is None:
        attempts = await session.scalar(
            text(
                "SELECT EXISTS(SELECT 1 FROM "
                "dante.list_self_subject_sessions(:actor,:activity))"
            ),
            {"actor": actor, "activity": activity_ref},
        )
        if attempts:
            raise _conflict("Scegli Mantieni Sessioni, Elimina Sessioni o Annulla.")
    elif disposition == "delete":
        await session.scalar(
            text("SELECT dante.delete_self_activity_sessions(:actor,:activity,:fingerprint)"),
            {"actor": actor, "activity": activity_ref, "fingerprint": impact},
        )
    return str(impact)


@router.get(
    "/{activity_ref}/timeline-undo-receipts",
    response_model=list[ActivityTimelineUndoReceipt],
    operation_id="temporal_list_activity_timeline_undo",
)
async def list_activity_timeline_undo(
    activity_ref: UUID,
    context: ReadContext,
    request: Request,
    response: Response,
) -> list[ActivityTimelineUndoReceipt]:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            rows = (await session.execute(
                text(
                    "SELECT * FROM dante.list_self_activity_timeline_undo(:actor,:activity)"
                ),
                {"actor": context.self_person_ref, "activity": activity_ref},
            )).mappings().all()
    except SQLAlchemyError as exc:
        raise _conflict("Impossibile leggere gli Undo della Timeline.") from exc
    return [ActivityTimelineUndoReceipt.model_validate(dict(row)) for row in rows]


@router.post(
    "/{activity_ref}/timeline-unplace",
    response_model=ActivityTimelineMutationResult,
    operation_id="temporal_unplace_activity_timeline",
)
async def unplace_activity_timeline(
    activity_ref: UUID,
    body: ActivityTimelineUnplaceCommand,
    context: WriteContext,
    request: Request,
    response: Response,
) -> ActivityTimelineMutationResult:
    response.headers["Cache-Control"] = "no-store"
    actor = context.self_person_ref
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            await session.execute(text("SET LOCAL lock_timeout = '5s'"))
            await _guard_timeline_role(
                session,actor,activity_ref,body.schedule_ref,require_current=True
            )
            await _timeline_session_guard(
                session,actor,activity_ref,
                body.expected_session_fingerprint,body.session_disposition,
            )
            row = (await session.execute(
                text("""
                  SELECT * FROM dante.unschedule_self_schedule(
                    :actor,:operation,:fingerprint,:schedule,:expected
                  )
                """),
                {
                    "actor": actor,
                    "operation": body.operation_id,
                    "fingerprint": _unschedule_fingerprint(
                        schedule_ref=ScopedRecordRef(body.schedule_ref),
                        expected_material_state_ref=MaterialStateRef(
                            body.expected_material_state_ref
                        ),
                    ),
                    "schedule": body.schedule_ref,
                    "expected": body.expected_material_state_ref,
                },
            )).mappings().one()
    except DBAPIError as exc:
        raise _conflict("La collocazione è cambiata: ricarica prima di confermare.") from exc
    except SQLAlchemyError as exc:
        raise _conflict("Rimozione dalla Timeline non completata.") from exc
    return ActivityTimelineMutationResult(
        activity_ref=activity_ref,
        schedule_ref=body.schedule_ref,
        operation_id=str(row["unschedule_operation_id"]),
        placement_material_state_ref=None,
    )


@router.post(
    "/{activity_ref}/timeline-undo",
    response_model=ActivityTimelineMutationResult,
    operation_id="temporal_undo_activity_timeline",
)
async def undo_activity_timeline(
    activity_ref: UUID,
    body: ActivityTimelineUndoCommand,
    context: WriteContext,
    request: Request,
    response: Response,
) -> ActivityTimelineMutationResult:
    response.headers["Cache-Control"] = "no-store"
    actor = context.self_person_ref
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            await session.execute(text("SET LOCAL lock_timeout = '5s'"))
            await _guard_timeline_role(
                session,actor,activity_ref,body.schedule_ref,require_current=False
            )
            await _timeline_session_guard(
                session,actor,activity_ref,body.expected_session_fingerprint,"keep"
            )
            # Dedicated owner-only SQL capability bypasses ONLY the generic
            # interval-Undo guard. It retains all CAS/receipt constraints and
            # monotonic history of the original Schedule Undo procedure.
            row = (await session.execute(
                text("""
                    SELECT * FROM dante.undo_self_activity_timeline(
                        :actor,:operation,:fingerprint,:schedule,:removed,:next_state,
                        :activity,:session_fingerprint
                    )
                """),
                {
                    "actor": actor,
                    "operation": body.operation_id,
                    "fingerprint": _unschedule_undo_fingerprint(
                        schedule_ref=ScopedRecordRef(body.schedule_ref),
                        unschedule_operation_id=body.unschedule_operation_id,
                    ),
                    "schedule": body.schedule_ref,
                    "removed": body.unschedule_operation_id,
                    "next_state": uuid7(),
                    "activity": activity_ref,
                    "session_fingerprint": body.expected_session_fingerprint,
                },
            )).mappings().one()
    except DBAPIError as exc:
        raise _conflict("Undo non disponibile: la Schedule o le Sessioni sono cambiate.") from exc
    except SQLAlchemyError as exc:
        raise _conflict("Impossibile ripristinare la precedente collocazione.") from exc
    return ActivityTimelineMutationResult(
        activity_ref=activity_ref,
        schedule_ref=body.schedule_ref,
        operation_id=body.operation_id,
        placement_material_state_ref=row["material_state_ref"],
    )
