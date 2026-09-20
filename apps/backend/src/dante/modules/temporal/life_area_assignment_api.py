"""Authenticated B05-B primary Life Area assignment and legacy inventory API."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.life_area_assignment import (
    LifeAreaAssignmentApplication,
    LifeAreaAssignmentConflictError,
    LifeAreaAssignmentInputError,
    LifeAreaAssignmentNotFoundError,
    LifeAreaAssignmentOperationIdReuseError,
    LifeAreaAssignmentPersistenceError,
    LifeAreaAssignmentView,
    UnassignedLifeAreaItemView,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/life-area-assignments", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _application(request: Request) -> LifeAreaAssignmentApplication:
    runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return LifeAreaAssignmentApplication(runtime.session_factory)


Application = Annotated[LifeAreaAssignmentApplication, Depends(_application)]


class AssignLifeAreaRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    life_area_ref: UUID
    expected_assignment_revision: int = Field(ge=0)


class LifeAreaAssignmentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: Literal["activity", "event"]
    subject_native_ref: UUID
    life_area_ref: UUID
    assignment_revision: int = Field(ge=1)
    assigned_at: datetime
    replayed: bool = False


class UnassignedLifeAreaItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: Literal["activity", "event"]
    subject_native_ref: UUID
    title: str
    created_at: datetime


def _response(value: LifeAreaAssignmentView) -> LifeAreaAssignmentResponse:
    return LifeAreaAssignmentResponse(
        subject_kind=value.subject_kind,
        subject_native_ref=value.subject_native_ref,
        life_area_ref=value.life_area_ref,
        assignment_revision=value.assignment_revision,
        assigned_at=value.assigned_at,
        replayed=value.replayed,
    )


def _unassigned_response(value: UnassignedLifeAreaItemView) -> UnassignedLifeAreaItemResponse:
    return UnassignedLifeAreaItemResponse(
        subject_kind=value.subject_kind,
        subject_native_ref=value.subject_native_ref,
        title=value.title,
        created_at=value.created_at,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, LifeAreaAssignmentInputError):
        return ProblemError(
            status=422,
            code="temporal.life_area_assignment.invalid_input",
            category="validation",
            title="Invalid Life Area assignment",
            detail=str(exc),
            retryable=False,
        )
    if isinstance(exc, LifeAreaAssignmentNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.life_area_assignment.not_found",
            category="not_found",
            title="Assignment target unavailable",
            detail="The item or active Life Area is unavailable in this self scope.",
            retryable=False,
        )
    if isinstance(exc, LifeAreaAssignmentOperationIdReuseError):
        return ProblemError(
            status=409,
            code="temporal.life_area_assignment.operation_id_reused",
            category="conflict",
            title="Life Area assignment operation conflict",
            detail="The operation id was used for different assignment intent.",
            retryable=False,
        )
    if isinstance(exc, LifeAreaAssignmentConflictError):
        return ProblemError(
            status=409,
            code="temporal.life_area_assignment.revision_conflict",
            category="conflict",
            title="Life Area assignment state changed",
            detail="Refresh the item organization and submit its current assignment revision.",
            retryable=False,
        )
    return ProblemError(
        status=503,
        code="temporal.life_area_assignment.persistence_unavailable",
        category="service",
        title="Life Area assignment unavailable",
        detail="The assignment could not complete safely.",
        retryable=True,
    )


_Errors = (
    LifeAreaAssignmentInputError,
    LifeAreaAssignmentNotFoundError,
    LifeAreaAssignmentOperationIdReuseError,
    LifeAreaAssignmentConflictError,
    LifeAreaAssignmentPersistenceError,
)


@router.get(
    "",
    response_model=list[LifeAreaAssignmentResponse],
    operation_id="temporal_list_life_area_assignments",
)
async def list_life_area_assignments(
    context: Context, application: Application, response: Response
) -> list[LifeAreaAssignmentResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        values = await application.list_assignments(self_person_ref=context.self_person_ref)
    except _Errors as exc:
        raise _problem(exc) from exc
    return [_response(value) for value in values]


@router.get(
    "/unassigned",
    response_model=list[UnassignedLifeAreaItemResponse],
    operation_id="temporal_list_unassigned_life_area_items",
)
async def list_unassigned_life_area_items(
    context: Context, application: Application, response: Response
) -> list[UnassignedLifeAreaItemResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        values = await application.list_unassigned(self_person_ref=context.self_person_ref)
    except _Errors as exc:
        raise _problem(exc) from exc
    return [_unassigned_response(value) for value in values]


async def _assign(
    *,
    subject_kind: Literal["activity", "event"],
    subject_native_ref: UUID,
    payload: AssignLifeAreaRequest,
    context: DanteContext,
    application: LifeAreaAssignmentApplication,
    response: Response,
) -> LifeAreaAssignmentResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.assign(
            self_person_ref=context.self_person_ref,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_native_ref),
            life_area_ref=payload.life_area_ref,
            expected_assignment_revision=payload.expected_assignment_revision,
            operation_id=payload.operation_id,
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    if value.replayed:
        response.status_code = 200
    return _response(value)


@router.put(
    "/activities/{activity_ref}",
    response_model=LifeAreaAssignmentResponse,
    operation_id="temporal_assign_activity_life_area",
)
async def assign_activity_life_area(
    activity_ref: UUID,
    payload: AssignLifeAreaRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaAssignmentResponse:
    return await _assign(
        subject_kind="activity",
        subject_native_ref=activity_ref,
        payload=payload,
        context=context,
        application=application,
        response=response,
    )


@router.put(
    "/events/{event_ref}",
    response_model=LifeAreaAssignmentResponse,
    operation_id="temporal_assign_event_life_area",
)
async def assign_event_life_area(
    event_ref: UUID,
    payload: AssignLifeAreaRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaAssignmentResponse:
    return await _assign(
        subject_kind="event",
        subject_native_ref=event_ref,
        payload=payload,
        context=context,
        application=application,
        response=response,
    )
