"""Self-scoped direct Activity decomposition commands and current children."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from typing import Annotated, Literal
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/activities", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class DecompositionCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    decomposition_ref: UUID | None = None
    expected_state_ref: UUID | None = None
    active: bool = True
    requirement_code: Literal["required", "optional"] = "required"
    presentation_order: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def validate_revision(self) -> DecompositionCommand:
        if self.expected_state_ref is not None and self.decomposition_ref is None:
            raise ValueError("A revision requires its decomposition reference.")
        if not self.active and self.expected_state_ref is None:
            raise ValueError("Detach requires the accepted current state.")
        return self


class DecompositionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decomposition_ref: UUID
    state_ref: UUID
    active: bool
    replayed: bool


class ActivityScheduleResponse(BaseModel):
    """One current Schedule placement; it does not represent a future Session."""

    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    role_code: Literal["envelope", "planned", "interval"] | None
    presentation_order: int | None
    display_name: str | None
    placement_material_state_ref: UUID
    temporal_form: Literal[
        "date_span", "floating_local", "named_zone_local", "absolute", "coarse_local_period"
    ]
    start_date: date | None
    end_date_exclusive: date | None
    starts_local_at: datetime | None
    ends_local_at: datetime | None
    zone_id: str | None
    resolved_start_at: datetime | None
    resolved_end_at: datetime | None
    starts_at: datetime | None
    ends_at: datetime | None
    local_date: date | None
    period_code: str | None


class ActivityChildResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decomposition_ref: UUID
    parent_activity_ref: UUID
    child_activity_ref: UUID
    child_title: str
    state_ref: UUID
    requirement_code: Literal["required", "optional"]
    presentation_order: int
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"]
    schedules: list[ActivityScheduleResponse]


class ActivityChildrenResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    parent_activity_ref: UUID
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"]
    child_guard_mode: Literal["none", "confirm", "block"]
    schedules: list[ActivityScheduleResponse]
    children: list[ActivityChildResponse]


def _unavailable() -> ProblemError:
    return ProblemError(
        status=503,
        code="temporal.decomposition.unavailable",
        category="service",
        title="Activity structure unavailable",
        detail="The canonical Activity structure could not be read or changed.",
        retryable=True,
    )


def _not_found() -> ProblemError:
    return ProblemError(
        status=404,
        code="temporal.decomposition.activity_unavailable",
        category="not_found",
        title="Activity unavailable",
        detail="Activity is unavailable in this self scope.",
        retryable=False,
    )


def _problem(exc: DBAPIError) -> ProblemError:
    diagnostic = getattr(exc.orig, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None)
    if constraint in {
        "activity_decomposition_owner_unavailable",
        "activity_decomposition_relation_unavailable",
    }:
        return _not_found()
    if constraint in {
        "activity_decomposition_current_conflict",
        "activity_decomposition_operation_reused",
        "activity_decomposition_retired",
        "activity_decomposition_depth_or_parent",
        "activity_decomposition_temporal_containment",
    }:
        return ProblemError(
            status=409,
            code="temporal.decomposition.conflict",
            category="conflict",
            title="Activity structure conflict",
            detail="Refresh the Activity and its Schedule before changing its structure.",
            retryable=False,
        )
    if constraint == "activity_decomposition_invalid":
        return ProblemError(
            status=422,
            code="temporal.decomposition.invalid",
            category="validation",
            title="Invalid Activity structure",
            detail="The relationship command is invalid.",
            retryable=False,
        )
    return _unavailable()


def _owner_schedules(
    rows: list,
    activity_ref: UUID,
    roles: dict[UUID, tuple[Literal["envelope", "planned", "interval"], int, str | None]],
) -> list[ActivityScheduleResponse]:
    return [
        ActivityScheduleResponse(
            **{key: value for key, value in row.items() if key != "subject_native_ref"},
            role_code=roles[row["schedule_ref"]][0] if row["schedule_ref"] in roles else None,
            presentation_order=roles[row["schedule_ref"]][1]
            if row["schedule_ref"] in roles
            else None,
            display_name=roles[row["schedule_ref"]][2] if row["schedule_ref"] in roles else None,
        )
        for row in sorted(
            (row for row in rows if row["subject_native_ref"] == activity_ref),
            key=lambda row: (
                0
                if roles.get(row["schedule_ref"], (None, 0))[0] == "envelope"
                else 1
                if roles.get(row["schedule_ref"], (None, 0))[0] == "interval"
                else 2
                if roles.get(row["schedule_ref"], (None, 0))[0] == "planned"
                else 3,
                roles.get(row["schedule_ref"], (None, 0))[1],
                str(row["schedule_ref"]),
            ),
        )
    ]


@router.get(
    "/{parent_activity_ref}/children",
    response_model=ActivityChildrenResponse,
    operation_id="temporal_get_activity_children",
)
async def get_activity_children(
    parent_activity_ref: UUID,
    context: ReadContext,
    request: Request,
) -> ActivityChildrenResponse:
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            owner = (
                (
                    await session.execute(
                        text(
                            "SELECT mode_code FROM dante.get_self_activity_execution_policy(:actor,:parent)"
                        ),
                        {"actor": context.self_person_ref, "parent": parent_activity_ref},
                    )
                )
                .mappings()
                .one_or_none()
            )
            if owner is None:
                raise _not_found()
            child_guard_mode = (
                await session.execute(
                    text(
                        "SELECT mode_code FROM dante.get_self_activity_decomposition_policy(:actor,:parent)"
                    ),
                    {"actor": context.self_person_ref, "parent": parent_activity_ref},
                )
            ).scalar_one()
            rows = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_activity_decomposition(:actor,:parent)"),
                        {"actor": context.self_person_ref, "parent": parent_activity_ref},
                    )
                )
                .mappings()
                .all()
            )
            schedule_rows = (
                (
                    await session.execute(
                        text("""
                        SELECT schedule.subject_native_ref,schedule.schedule_ref,
                               current.material_state_ref AS placement_material_state_ref,
                               state.temporal_form_code AS temporal_form,
                               lower(dates.date_span) AS start_date,
                               upper(dates.date_span) AS end_date_exclusive,
                               COALESCE(floating.starts_local_at,zoned.starts_local_at)
                                   AS starts_local_at,
                               COALESCE(floating.ends_local_at,zoned.ends_local_at)
                                   AS ends_local_at,
                               zoned.zone_id,zoned.resolved_start_at,zoned.resolved_end_at,
                               absolute.starts_at,absolute.ends_at,
                               coarse.local_date,coarse.period_code
                          FROM dante.schedule AS schedule
                          JOIN dante.schedule_current_placement AS current
                            ON current.scoped_owner_ref=schedule.schedule_ref
                          JOIN dante.schedule_placement_state AS state
                            ON state.schedule_ref=schedule.schedule_ref
                           AND state.material_state_ref=current.material_state_ref
                     LEFT JOIN dante.schedule_placement_date_state AS dates
                            ON dates.material_state_ref=state.material_state_ref
                     LEFT JOIN dante.schedule_placement_floating_local_state AS floating
                            ON floating.material_state_ref=state.material_state_ref
                     LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
                            ON zoned.material_state_ref=state.material_state_ref
                     LEFT JOIN dante.schedule_placement_absolute_state AS absolute
                            ON absolute.material_state_ref=state.material_state_ref
                     LEFT JOIN dante.schedule_placement_coarse_local_period_state AS coarse
                            ON coarse.material_state_ref=state.material_state_ref
                         WHERE schedule.subject_native_ref=ANY(CAST(:subjects AS uuid[]))
                         ORDER BY schedule.schedule_ref
                    """),
                        {
                            "subjects": [
                                parent_activity_ref,
                                *(row["child_activity_ref"] for row in rows),
                            ]
                        },
                    )
                )
                .mappings()
                .all()
            )
            role_rows = (
                (
                    await session.execute(
                        text("""
                        SELECT * FROM dante.get_self_activity_schedule_roles(
                            :actor,CAST(:subjects AS uuid[])
                        )
                    """),
                        {
                            "actor": context.self_person_ref,
                            "subjects": [
                                parent_activity_ref,
                                *(row["child_activity_ref"] for row in rows),
                            ],
                        },
                    )
                )
                .mappings()
                .all()
            )
            roles = {
                row["schedule_ref"]: (
                    row["role_code"],
                    row["presentation_order"],
                    row["display_name"],
                )
                for row in role_rows
            }
            modes = {}
            for child in rows:
                modes[child["child_activity_ref"]] = (
                    await session.execute(
                        text("""
                            SELECT mode_code FROM dante.get_self_activity_execution_policy(
                                :actor,:child
                            )
                        """),
                        {"actor": context.self_person_ref, "child": child["child_activity_ref"]},
                    )
                ).scalar_one()
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    return ActivityChildrenResponse(
        parent_activity_ref=parent_activity_ref,
        session_capture_mode=owner["mode_code"],
        child_guard_mode=child_guard_mode,
        schedules=_owner_schedules(schedule_rows, parent_activity_ref, roles),
        children=[
            ActivityChildResponse(
                **{key: value for key, value in row.items() if key != "current_from_at"},
                session_capture_mode=modes[row["child_activity_ref"]],
                schedules=_owner_schedules(schedule_rows, row["child_activity_ref"], roles),
            )
            for row in rows
        ],
    )


@router.post(
    "/{parent_activity_ref}/children/{child_activity_ref}",
    response_model=DecompositionResponse,
    operation_id="temporal_set_activity_child",
)
async def set_activity_child(
    parent_activity_ref: UUID,
    child_activity_ref: UUID,
    payload: DecompositionCommand,
    context: WriteContext,
    request: Request,
    response: Response,
) -> DecompositionResponse:
    intent = {
        "version": 1,
        "parent_activity_ref": str(parent_activity_ref),
        "child_activity_ref": str(child_activity_ref),
        "active": payload.active,
        "requirement_code": payload.requirement_code,
        "presentation_order": payload.presentation_order,
        "expected_state_ref": (
            None if payload.expected_state_ref is None else str(payload.expected_state_ref)
        ),
        "decomposition_ref": (
            None if payload.expected_state_ref is None else str(payload.decomposition_ref)
        ),
    }
    fingerprint = hashlib.sha256(
        json.dumps(intent, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                (
                    await session.execute(
                        text("""
                        SELECT * FROM dante.set_self_activity_decomposition(
                            :actor,:operation,:fingerprint,:relation,:parent,:child,
                            :state,:active,:requirement,:position,:expected
                        )
                    """),
                        {
                            "actor": context.self_person_ref,
                            "operation": payload.operation_id,
                            "fingerprint": fingerprint,
                            "relation": payload.decomposition_ref or uuid7(),
                            "parent": parent_activity_ref,
                            "child": child_activity_ref,
                            "state": uuid7(),
                            "active": payload.active,
                            "requirement": payload.requirement_code,
                            "position": payload.presentation_order,
                            "expected": payload.expected_state_ref,
                        },
                    )
                )
                .mappings()
                .one()
            )
    except DBAPIError as exc:
        raise _problem(exc) from exc
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    response.status_code = 200 if row["replayed"] else 201
    response.headers["Cache-Control"] = "no-store"
    return DecompositionResponse(**row)
