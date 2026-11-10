"""Coordinated Activity time revisions and planned Session replacement."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from itertools import pairwise
from typing import Annotated
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.activity_edit_snapshot_api import (
    _SNAPSHOT,
    ActivityCoreEditCommand,
    ActivityCoreEditResponse,
    ActivityEditSnapshot,
    revise_activity_core_in_session,
)
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.life_area import _fingerprint as life_area_fingerprint
from dante.modules.temporal.life_area_assignment import _fingerprint as assignment_fingerprint
from dante.modules.temporal.reality_objective_api import (
    ActivityObjectiveBatchCommand,
    ObjectiveResponse,
    apply_activity_objective_edits_in_session,
)
from dante.modules.temporal.schedule import (
    DateSpanPlacement,
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
        if (
            self.starts_local_at.tzinfo is not None
            or self.ends_local_at.tzinfo is not None
            or self.ends_local_at <= self.starts_local_at
        ):
            raise ValueError("Planning requires ordered local timestamps without an offset.")
        return self


class ReplanDateSpanRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    expected_material_state_ref: UUID
    start_date: date
    end_date_exclusive: date

    @model_validator(mode="after")
    def valid_span(self) -> ReplanDateSpanRow:
        if self.end_date_exclusive <= self.start_date:
            raise ValueError("The final day must follow the first day.")
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
    date_span: ReplanDateSpanRow | None = None
    target_zone_id: str | None = None
    split_envelope: bool = False
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

    @model_validator(mode="after")
    def unique_new_rows(self) -> ActivityReplanCommand:
        refs = [row.client_ref for row in self.new_intervals] + [
            row.client_ref for row in self.new_planned_sessions
        ]
        if len(set(refs)) != len(refs):
            raise ValueError("New Activity interval and planned Session identities must be unique.")
        return self


class AtomicPlacementLock(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schedule_ref: UUID
    expected_revision: int | None = Field(default=None, ge=0)
    locked: bool


class AtomicPlannedName(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schedule_ref: UUID
    expected_name: str | None = Field(default=None, max_length=300)
    name: str | None = Field(default=None, min_length=1, max_length=300)

    @model_validator(mode="after")
    def trimmed(self) -> AtomicPlannedName:
        if self.name is not None and self.name != self.name.strip():
            raise ValueError("A planned Session name must be trimmed.")
        return self


class AtomicNewLifeArea(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=100)
    color_code: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


class AtomicLifeArea(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=150)
    expected_assignment_revision: int = Field(ge=0)
    life_area_ref: UUID | None = None
    assign: bool = True
    new_area: AtomicNewLifeArea | None = None
    expected_area_revision: int | None = Field(default=None, ge=1)
    color_code: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    icon_code: str | None = None

    @model_validator(mode="after")
    def valid_choice(self) -> AtomicLifeArea:
        if self.new_area is not None and self.life_area_ref is not None:
            raise ValueError("Choose an existing Life Area or create a new one.")
        if self.color_code is not None and (
            self.life_area_ref is None or self.expected_area_revision is None
        ):
            raise ValueError("An existing Life Area color requires its revision.")
        if self.new_area is not None and not self.assign:
            raise ValueError("A new Life Area must be assigned to this Activity.")
        return self


class AtomicOccurrenceProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    occurrence_ref: UUID
    expected_revision: int = Field(ge=0)
    expected_recurrence_state_ref: UUID | None
    profile_patch: dict[str, str | None] = Field(min_length=1, max_length=4)

    @model_validator(mode="after")
    def valid_patch(self) -> AtomicOccurrenceProfile:
        patch = self.profile_patch
        if not set(patch).issubset({"title", "description", "location", "color_code"}):
            raise ValueError("Only occurrence profile metadata can be edited here.")
        title = patch.get("title")
        if "title" in patch and (
            title is None or not title or title != title.strip() or len(title) > 300
        ):
            raise ValueError("Invalid occurrence title.")
        if any(
            value is not None and (not value or value != value.strip())
            for key, value in patch.items()
            if key in {"description", "location"}
        ):
            raise ValueError("Invalid occurrence metadata.")
        color = patch.get("color_code")
        if (
            "color_code" in patch
            and color is not None
            and (
                len(color) != 7
                or not color.startswith("#")
                or any(ch not in "0123456789ABCDEF" for ch in color[1:])
            )
        ):
            raise ValueError("Invalid occurrence color.")
        return self


class ActivityAtomicEditCommand(BaseModel):
    """Compose the Activity's owner capabilities in one serializable Save."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str | None = Field(default=None, min_length=1, max_length=200)
    replan: ActivityReplanCommand | None = None
    objectives: ActivityObjectiveBatchCommand | None = None
    core: ActivityCoreEditCommand | None = None
    placement_lock: AtomicPlacementLock | None = None
    planned_names: list[AtomicPlannedName] = Field(default_factory=list, max_length=100)
    life_area: AtomicLifeArea | None = None
    occurrence_profile: AtomicOccurrenceProfile | None = None

    @model_validator(mode="after")
    def nonempty(self) -> ActivityAtomicEditCommand:
        if not any(
            (
                self.replan,
                self.objectives,
                self.core,
                self.placement_lock,
                self.planned_names,
                self.life_area,
                self.occurrence_profile,
            )
        ):
            raise ValueError("At least one Activity edit is required.")
        if self.occurrence_profile is not None and self.core is not None and self.core.profile:
            raise ValueError("Choose the instance profile instead of the Activity source profile.")
        if self.occurrence_profile is not None and self.operation_id is None:
            raise ValueError("An instance profile edit requires an operation id.")
        return self


class ActivityAtomicEditResponse(BaseModel):
    snapshot: ActivityEditSnapshot
    objectives: list[ObjectiveResponse]
    core: ActivityCoreEditResponse | None = None


class ReplanChange(BaseModel):
    schedule_ref: UUID | None = None
    client_ref: UUID | None = None
    role: str
    previous_start: datetime | None = None
    previous_end: datetime | None = None
    proposed_start: datetime | None = None
    proposed_end: datetime | None = None
    previous_start_date: date | None = None
    previous_end_date_exclusive: date | None = None
    proposed_start_date: date | None = None
    proposed_end_date_exclusive: date | None = None


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


def _validate_planned_rows(
    planned: list[ActivityScheduleResponse], command: ActivityReplanCommand
) -> None:
    if (
        len(command.planned_sessions) + len(command.delete_planned_sessions) != len(planned)
        or len(planned) - len(command.delete_planned_sessions) + len(command.new_planned_sessions)
        > 100
    ):
        raise _invalid("Every named Session must be retained or deleted (at most 100).")
    existing = {row.schedule_ref: row for row in planned}
    retained: list[RetainedPlannedRow | DeletePlannedRow] = [
        *command.planned_sessions,
        *command.delete_planned_sessions,
    ]
    if len({row.schedule_ref for row in retained}) != len(existing) or any(
        row.schedule_ref not in existing
        or row.expected_material_state_ref
        != existing[row.schedule_ref].placement_material_state_ref
        for row in retained
    ):
        raise _conflict()


def _validated_plan(
    snapshot: ActivityEditSnapshot,
    command: ActivityReplanCommand,
) -> tuple[
    list[ReplanChange],
    list[
        tuple[
            ReplanRow | ReplanDateSpanRow,
            DateSpanPlacement | FloatingLocalIntervalPlacement | NamedZoneLocalIntervalPlacement,
        ]
    ],
]:
    """Pure preflight. Every dependent row is explicit, so none move silently."""
    rows = snapshot.schedules
    intervals = [row for row in rows if row.role_code == "interval"]
    envelope = next((row for row in rows if row.role_code == "envelope"), None)
    planned = [row for row in rows if row.role_code == "planned"]
    if envelope is None:
        raise _invalid("This Activity does not have an editable time frame.")
    if command.date_span is not None:
        span = command.date_span
        if (
            intervals
            or command.envelope is not None
            or command.new_intervals
            or command.remove_intervals
            or command.intervals
            or command.split_envelope
            or command.target_zone_id is not None
            or envelope.temporal_form not in {"date_span", "floating_local", "named_zone_local"}
        ):
            raise _invalid("All-day placement requires one Activity period.")
        if (
            span.schedule_ref != envelope.schedule_ref
            or span.expected_material_state_ref != envelope.placement_material_state_ref
        ):
            raise _conflict()
        _validate_planned_rows(planned, command)
        unchanged = (
            envelope.temporal_form == "date_span"
            and envelope.start_date == span.start_date
            and envelope.end_date_exclusive == span.end_date_exclusive
        )
        changes = (
            []
            if unchanged
            else [
                ReplanChange(
                    schedule_ref=envelope.schedule_ref,
                    role="envelope",
                    previous_start=envelope.starts_local_at,
                    previous_end=envelope.ends_local_at,
                    previous_start_date=envelope.start_date,
                    previous_end_date_exclusive=envelope.end_date_exclusive,
                    proposed_start_date=span.start_date,
                    proposed_end_date_exclusive=span.end_date_exclusive,
                )
            ]
        )
        changes.extend(
            ReplanChange(schedule_ref=row.schedule_ref, role="planned_deleted")
            for row in command.delete_planned_sessions
        )
        changes.extend(
            ReplanChange(client_ref=row.client_ref, role="planned_added")
            for row in command.new_planned_sessions
        )
        return changes, [] if unchanged else [
            (span, DateSpanPlacement(span.start_date, span.end_date_exclusive))
        ]
    if envelope.temporal_form == "date_span":
        timed_envelope = command.envelope
        if (
            timed_envelope is None
            or intervals
            or command.intervals
            or command.remove_intervals
            or command.new_intervals
            or command.split_envelope
            or not command.target_zone_id
        ):
            raise _invalid(
                "Changing an all-day period to a time requires one exact interval and a zone."
            )
        if (
            timed_envelope.schedule_ref != envelope.schedule_ref
            or timed_envelope.expected_material_state_ref != envelope.placement_material_state_ref
        ):
            raise _conflict()
        _validate_planned_rows(planned, command)
        try:
            conversion_placement = NamedZoneLocalIntervalPlacement(
                starts_local_at=timed_envelope.starts_local_at,
                ends_local_at=timed_envelope.ends_local_at,
                zone_id=command.target_zone_id,
            )
        except ScheduleInputError as exc:
            raise _invalid(str(exc)) from exc
        changes = [
            ReplanChange(
                schedule_ref=timed_envelope.schedule_ref,
                role="envelope",
                previous_start_date=envelope.start_date,
                previous_end_date_exclusive=envelope.end_date_exclusive,
                proposed_start=timed_envelope.starts_local_at,
                proposed_end=timed_envelope.ends_local_at,
            )
        ]
        changes.extend(
            ReplanChange(schedule_ref=item.schedule_ref, role="planned_deleted")
            for item in command.delete_planned_sessions
        )
        changes.extend(
            ReplanChange(client_ref=item.client_ref, role="planned_added")
            for item in command.new_planned_sessions
        )
        return changes, [(timed_envelope, conversion_placement)]
    if command.target_zone_id is not None or (
        command.split_envelope and (intervals or not command.new_intervals)
    ):
        raise _invalid("The requested Activity time frame is inconsistent.")
    if (
        not intervals
        and (
            command.envelope is None
            or command.intervals
            or (command.new_intervals and not command.split_envelope)
            or command.remove_intervals
        )
    ) or (intervals and command.envelope is not None):
        raise _invalid("An Activity without intervals must revise its envelope directly.")
    if (
        len(command.intervals) + len(command.remove_intervals) != len(intervals)
        or (intervals and not command.intervals and not command.new_intervals)
        or len(command.intervals) + len(command.new_intervals) + int(command.split_envelope) > 100
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
    _validate_planned_rows(planned, command)
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
        ordered_spans = sorted(
            [(command.envelope.starts_local_at, command.envelope.ends_local_at)]
            + [(row.starts_local_at, row.ends_local_at) for row in command.new_intervals],
            key=lambda span: span[0],
        )
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
    changes = []
    placements: list[
        tuple[
            ReplanRow | ReplanDateSpanRow,
            DateSpanPlacement | FloatingLocalIntervalPlacement | NamedZoneLocalIntervalPlacement,
        ]
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
            placement: FloatingLocalIntervalPlacement | NamedZoneLocalIntervalPlacement = (
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
    if command.split_envelope and command.envelope is not None:
        changes.append(
            ReplanChange(
                role="interval_added",
                proposed_start=command.envelope.starts_local_at,
                proposed_end=command.envelope.ends_local_at,
            )
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


async def _set_atomic_lock(
    session: AsyncSession, actor: UUID, change: AtomicPlacementLock, locked: bool
) -> int:
    expected_revision = change.expected_revision
    if expected_revision == 0:
        # The edit snapshot exposes an absent lock as revision 0. The SQL
        # setter represents that same basis with NULL and refuses 0. Check
        # the basis first so an intervening lock still reports a conflict.
        current_revision = await session.scalar(
            text("SELECT revision FROM dante.get_self_schedule_placement_lock(:actor,:schedule)"),
            {"actor": actor, "schedule": change.schedule_ref},
        )
        if current_revision != 0:
            raise _conflict("Il blocco degli spostamenti è cambiato. Riapri Modifica e riprova.")
        expected_revision = None
    row = (
        (
            await session.execute(
                text(
                    "SELECT * FROM dante.set_self_schedule_placement_lock("
                    ":actor,:schedule,:locked,:expected_revision)"
                ),
                {
                    "actor": actor,
                    "schedule": change.schedule_ref,
                    "locked": locked,
                    "expected_revision": expected_revision,
                },
            )
        )
        .mappings()
        .one()
    )
    return int(row["revision"])


async def _apply_atomic_area(
    session: AsyncSession, actor: UUID, activity: UUID, change: AtomicLifeArea
) -> None:
    target = change.life_area_ref
    if change.new_area is not None:
        name = change.new_area.name.strip()
        if not name:
            raise _conflict("Inserisci un nome Life Area valido.")
        fingerprint = life_area_fingerprint({"version": 1, "name": name})
        target = (
            await session.execute(
                text(
                    "SELECT life_area_ref FROM dante.create_self_life_area("
                    ":actor,:operation,:fingerprint,:area_ref,:name)"
                ),
                {
                    "actor": actor,
                    "operation": f"{change.operation_id}:create",
                    "fingerprint": fingerprint,
                    "area_ref": uuid7(),
                    "name": name,
                },
            )
        ).scalar_one()
    color = change.new_area.color_code if change.new_area is not None else change.color_code
    if color is not None:
        if target is None:
            raise _conflict("Seleziona una Life Area prima di cambiarne il colore.")
        revision = 1 if change.new_area is not None else change.expected_area_revision
        fingerprint = life_area_fingerprint(
            {
                "version": 1,
                "kind": "appearance",
                "area": str(target),
                "expected_revision": revision,
                "payload": {"icon_code": change.icon_code, "color_code": color.upper()},
            }
        )
        await session.execute(
            text(
                "SELECT * FROM dante.mutate_self_life_area("
                ":actor,:operation,:fingerprint,:area,:revision,'appearance',"
                "NULL,NULL,:icon,:color)"
            ),
            {
                "actor": actor,
                "operation": f"{change.operation_id}:appearance",
                "fingerprint": fingerprint,
                "area": target,
                "revision": revision,
                "icon": change.icon_code,
                "color": color.upper(),
            },
        )
    if change.assign:
        await session.execute(
            text(
                "SELECT * FROM dante.assign_self_activity_life_area("
                ":actor,:operation,:fingerprint,:activity,:area,:revision)"
            ),
            {
                "actor": actor,
                "operation": f"{change.operation_id}:assignment",
                "fingerprint": assignment_fingerprint(
                    kind="activity",
                    subject_ref=NativeRef(activity),
                    life_area_ref=target,
                    expected=change.expected_assignment_revision,
                ),
                "activity": NativeRef(activity),
                "area": target,
                "revision": change.expected_assignment_revision,
            },
        )


async def _apply_atomic_occurrence_profile(
    session: AsyncSession,
    actor: UUID,
    activity: UUID,
    change: AtomicOccurrenceProfile,
    zone_id: str,
    operation_id: str,
) -> None:
    bound = (
        await session.execute(
            text(
                "SELECT activity_ref FROM dante.list_self_routine_occurrence_activities("
                ":actor,CAST(ARRAY[:occurrence] AS uuid[]))"
            ),
            {"actor": actor, "occurrence": change.occurrence_ref},
        )
    ).scalar_one_or_none()
    if bound != activity:
        raise _conflict("L'istanza ricorrente non appartiene all'attività selezionata.")
    await session.execute(
        text(
            "SELECT * FROM dante.accept_self_occurrence_profile_edit("
            ":actor,:selected,:operation,:expected,:recurrence,'only_this',"
            ":zone,CAST(:patch AS jsonb))"
        ),
        {
            "actor": actor,
            "selected": change.occurrence_ref,
            "operation": operation_id,
            "expected": change.expected_revision,
            "recurrence": change.expected_recurrence_state_ref,
            "zone": zone_id,
            "patch": json.dumps(change.profile_patch, sort_keys=True),
        },
    )


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


async def apply_activity_replan_in_session(
    session: AsyncSession,
    *,
    actor: UUID,
    activity_ref: UUID,
    body: ActivityReplanCommand,
) -> ActivityEditSnapshot:
    """Apply a guarded Activity plan in the caller's transaction.

    Series reconciliation can compose multiple clean instances without
    publishing partial replans; the HTTP route uses the same path.
    """
    digest = hashlib.sha256(body.operation_id.encode("utf-8")).hexdigest()
    snapshot = await _read(session, actor, activity_ref)
    _, placements = _validated_plan(snapshot, body)
    # Re-evaluate facts in this serializable Save transaction. A
    # completed named attempt retains its history, but no longer
    # freezes intended time. Main (even concluded) and open/paused
    # named attempts still freeze it. No direct table lock: the runtime
    # role has SELECT but not UPDATE on activity_intention.
    attempt_rows = (
        (
            await session.execute(
                text("""
                    SELECT s.session_ref, s.ended_at,
                           dante.get_self_session_planned_schedule(
                               :actor,s.session_ref
                           ) AS planned_schedule_ref
                      FROM dante.list_self_subject_sessions(:actor,:activity) AS s
                """),
                {"actor": actor, "activity": activity_ref},
            )
        )
        .mappings()
        .all()
    )
    attempts_present = bool(attempt_rows)
    planning_locked = any(
        row.ended_at is None or row.planned_schedule_ref is None for row in attempt_rows
    )
    if planning_locked and (
        placements or body.remove_intervals or body.new_intervals or body.split_envelope
    ):
        raise _conflict(
            "Elimina le registrazioni attive o della Sessione principale "
            "prima di modificare orari o intervalli."
        )
    if attempts_present and body.delete_planned_sessions:
        recorded_planned = {row.planned_schedule_ref for row in attempt_rows}
        if any(row.schedule_ref in recorded_planned for row in body.delete_planned_sessions):
            raise _conflict("Elimina la registrazione prima di rimuovere la Sessione.")
    envelope = next(row for row in snapshot.schedules if row.role_code == "envelope")
    # The envelope lock protects its accepted time and interval geometry;
    # it does not lock independent named Session configuration. Replacing
    # an unplaced planned Session must not impersonate envelope replanning.
    # Each deleted named Session is checked against its OWN placement lock
    # below, and sessions with recorded attempts remain protected above.
    envelope_placement_changes = bool(
        placements or body.remove_intervals or body.new_intervals or body.split_envelope
    )
    if envelope_placement_changes and await session.scalar(
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
            text("SELECT locked FROM dante.get_self_schedule_placement_lock(:actor,:schedule)"),
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
        (item.schedule_ref, item.expected_material_state_ref) for item in body.remove_intervals
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
    if body.new_intervals or body.split_envelope:
        next_interval_order = await session.scalar(
            text("""
            SELECT COALESCE(MAX(presentation_order),0)
              FROM dante.get_self_activity_schedule_roles(
                  :actor, CAST(ARRAY[:activity] AS uuid[]))
             WHERE role_code='interval'
        """),
            {"actor": actor, "activity": activity_ref},
        )
        additions = [
            *(
                [
                    (
                        "split-first",
                        body.envelope.starts_local_at,
                        body.envelope.ends_local_at,
                    )
                ]
                if body.split_envelope and body.envelope is not None
                else []
            ),
            *(
                (str(row.client_ref), row.starts_local_at, row.ends_local_at)
                for row in body.new_intervals
            ),
        ]
        for client_ref, starts_local_at, ends_local_at in additions:
            next_interval_order += 1
            try:
                placement = (
                    NamedZoneLocalIntervalPlacement(
                        starts_local_at=starts_local_at,
                        ends_local_at=ends_local_at,
                        zone_id=_checked_zone(envelope),
                    )
                    if envelope.temporal_form == "named_zone_local"
                    else FloatingLocalIntervalPlacement(
                        starts_local_at=starts_local_at,
                        ends_local_at=ends_local_at,
                    )
                )
            except ScheduleInputError as exc:
                raise _invalid(str(exc)) from exc
            created = await establish_schedule_in_session(
                session,
                self_person_ref=NativeRef(actor),
                operation_id=f"replan:add-interval:{digest}:{client_ref}",
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
            position for position in range(last_order + 1, 101) if position not in used_orders
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
    actor = context.self_person_ref
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            return await apply_activity_replan_in_session(
                session, actor=actor, activity_ref=activity_ref, body=body
            )
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


@router.put(
    "/{activity_ref}/atomic-edit",
    response_model=ActivityAtomicEditResponse,
    operation_id="temporal_apply_activity_atomic_edit",
)
async def apply_activity_atomic_edit(
    activity_ref: UUID,
    body: ActivityAtomicEditCommand,
    context: WriteContext,
    request: Request,
    response: Response,
) -> ActivityAtomicEditResponse:
    """Commit every ordinary Activity edit in one serializable Save transaction."""
    response.headers["Cache-Control"] = "no-store"
    actor = context.self_person_ref
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            if body.placement_lock is not None and not body.placement_lock.locked:
                await _set_atomic_lock(session, actor, body.placement_lock, False)
            if body.replan is not None:
                await apply_activity_replan_in_session(
                    session, actor=actor, activity_ref=activity_ref, body=body.replan
                )
            for change in body.planned_names:
                await session.execute(
                    text(
                        "SELECT * FROM dante.revise_self_planned_session_name("
                        ":actor,:activity,:schedule,:expected,:name)"
                    ),
                    {
                        "actor": actor,
                        "activity": NativeRef(activity_ref),
                        "schedule": change.schedule_ref,
                        "expected": change.expected_name,
                        "name": change.name,
                    },
                )
            if body.life_area is not None:
                await _apply_atomic_area(session, actor, activity_ref, body.life_area)
            objectives = (
                await apply_activity_objective_edits_in_session(
                    session,
                    actor=actor,
                    subject_ref=activity_ref,
                    payload=body.objectives,
                    effective_zone_id=context.effective_zone_id,
                )
                if body.objectives is not None
                else []
            )
            core = (
                await revise_activity_core_in_session(
                    session, actor=actor, activity_ref=activity_ref, body=body.core
                )
                if body.core is not None
                else None
            )
            if body.placement_lock is not None and body.placement_lock.locked:
                await _set_atomic_lock(session, actor, body.placement_lock, True)
            if body.occurrence_profile is not None:
                await _apply_atomic_occurrence_profile(
                    session,
                    actor,
                    activity_ref,
                    body.occurrence_profile,
                    context.effective_zone_id,
                    body.operation_id or "",
                )
            return ActivityAtomicEditResponse(
                snapshot=await _read(session, actor, activity_ref),
                objectives=objectives,
                core=core,
            )
    except DBAPIError as exc:
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
        if constraint == "temporal_objective_retirement_recorded":
            raise ProblemError(
                status=409,
                code="temporal.activity_edit.objective_recorded",
                category="conflict",
                title="Obiettivo con risultati",
                detail="L'obiettivo ha risultati registrati: non può essere eliminato.",
            ) from exc
        if constraint == "temporal_objective_unavailable":
            raise _conflict("Un obiettivo è cambiato. Riapri Modifica e riprova.") from exc
        if getattr(exc.orig, "sqlstate", None) in {"40001", "23505"} or constraint:
            raise _conflict("L'attività è cambiata. Riapri Modifica e riprova.") from exc
        raise ProblemError(
            status=503,
            code="temporal.activity_edit.unavailable",
            category="service",
            title="Salvataggio non disponibile",
            detail="Non è stato possibile salvare l'attività.",
            retryable=True,
        ) from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity_edit.unavailable",
            category="service",
            title="Salvataggio non disponibile",
            detail="Non è stato possibile salvare l'attività.",
            retryable=True,
        ) from exc
