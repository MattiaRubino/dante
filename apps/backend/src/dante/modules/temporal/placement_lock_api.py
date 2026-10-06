"""Authenticated Schedule placement lock read and mutation endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.placement_lock import (
    PlacementLockApplication,
    PlacementLockConflictError,
    PlacementLockNotFoundError,
    PlacementLockPersistenceError,
    PlacementLockView,
)
from dante.platform.database.references import ScopedRecordRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/schedules", tags=["temporal"])


class PlacementLockRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    locked: bool
    expected_revision: int | None = Field(default=None, ge=0)


class PlacementLockResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schedule_ref: UUID
    locked: bool
    revision: int
    updated_at: datetime | None
    replayed: bool


def _application(request: Request) -> PlacementLockApplication:
    return PlacementLockApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[PlacementLockApplication, Depends(_application)]
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: PlacementLockView) -> PlacementLockResponse:
    return PlacementLockResponse(
        schedule_ref=view.schedule_ref,
        locked=view.locked,
        revision=view.revision,
        updated_at=view.updated_at,
        replayed=view.replayed,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, PlacementLockNotFoundError):
        return ProblemError(
            status=404, code="temporal.placement_lock.not_found", category="not_found",
            title="Schedule unavailable", detail="Schedule unavailable in self scope.",
        )
    if isinstance(exc, PlacementLockConflictError):
        return ProblemError(
            status=409, code="temporal.placement_lock.conflict", category="conflict",
            title="Placement lock changed", detail="Refresh the Schedule and retry.",
        )
    return ProblemError(
        status=503, code="temporal.placement_lock.unavailable", category="service",
        title="Placement lock unavailable", detail="Placement lock could not be saved safely.",
        retryable=True,
    )


@router.get(
    "/{schedule_ref}/placement-lock",
    response_model=PlacementLockResponse,
    operation_id="temporal_get_self_schedule_placement_lock",
)
async def get_self_schedule_placement_lock(
    schedule_ref: UUID, context: ReadContext, application: Application, response: Response,
) -> PlacementLockResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return _response(await application.get(
            self_person_ref=context.self_person_ref,
            schedule_ref=ScopedRecordRef(schedule_ref),
        ))
    except (PlacementLockNotFoundError, PlacementLockPersistenceError) as exc:
        raise _problem(exc) from exc


@router.put(
    "/{schedule_ref}/placement-lock",
    response_model=PlacementLockResponse,
    operation_id="temporal_set_self_schedule_placement_lock",
)
async def set_self_schedule_placement_lock(
    schedule_ref: UUID, body: PlacementLockRequest, context: WriteContext,
    application: Application, response: Response,
) -> PlacementLockResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return _response(await application.set(
            self_person_ref=context.self_person_ref,
            schedule_ref=ScopedRecordRef(schedule_ref),
            locked=body.locked,
            expected_revision=body.expected_revision,
        ))
    except (
        PlacementLockNotFoundError, PlacementLockConflictError,
        PlacementLockPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
