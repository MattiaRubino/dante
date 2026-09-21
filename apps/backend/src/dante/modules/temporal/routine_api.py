"""Authenticated B06-A Routine source endpoints.

These endpoints expose source identity and product organization only.  They do
not create recurrence, occurrence, Activity, or Schedule records.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.routine import (
    RoutineApplication, RoutineInputError, RoutineNotFoundError,
    RoutineOperationReuseError, RoutinePersistenceError, RoutineStateConflictError,
)
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class CreateRoutineRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area_ref: UUID
    tag_refs: list[UUID] = Field(default_factory=list, max_length=100)


class RoutineMutationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_source_revision: int = Field(ge=1)


class RenameRoutineRequest(RoutineMutationRequest):
    title: str = Field(min_length=1, max_length=300)


class AssignRoutineLifeAreaRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    life_area_ref: UUID
    expected_assignment_revision: int = Field(ge=1)


class RoutineTagOperationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)


class RoutineResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    routine_ref: UUID
    title: str
    lifecycle_state: Literal["active", "paused", "ended"]
    source_revision: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime
    lifecycle_changed_at: datetime
    life_area_ref: UUID
    life_area_assignment_revision: int = Field(ge=1)
    life_area_assigned_at: datetime
    tag_refs: list[UUID]
    replayed: bool = False


class RoutineMutationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    routine_ref: UUID
    source_revision: int = Field(ge=1)
    lifecycle_state: Literal["active", "paused", "ended"]
    accepted_at: datetime
    replayed: bool


class RoutineLifeAreaResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    life_area_ref: UUID
    assignment_revision: int = Field(ge=1)
    assigned_at: datetime
    replayed: bool


class RoutineTagEffectResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    attached: bool
    accepted_at: datetime
    replayed: bool


def _application(request: Request) -> RoutineApplication:
    return RoutineApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[RoutineApplication, Depends(_application)]
_Errors = (RoutineInputError, RoutineOperationReuseError, RoutineNotFoundError, RoutineStateConflictError, RoutinePersistenceError)


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, RoutineInputError):
        return ProblemError(status=422, code="temporal.routine.invalid_input", category="validation", title="Routine command rejected", detail=str(exc))
    if isinstance(exc, RoutineOperationReuseError):
        return ProblemError(status=409, code="temporal.routine.operation_id_reused", category="conflict", title="Routine operation id reused", detail="Use a new operation id for different intent.")
    if isinstance(exc, RoutineNotFoundError):
        return ProblemError(status=404, code="temporal.routine.unavailable", category="not_found", title="Routine source unavailable", detail="The source or organization target is unavailable in this account.")
    if isinstance(exc, RoutineStateConflictError):
        return ProblemError(status=409, code="temporal.routine.state_conflict", category="conflict", title="Routine state changed", detail="Reload the Routine and retry with current revision.")
    return ProblemError(status=503, code="temporal.routine.persistence_unavailable", category="service", title="Routine persistence unavailable", detail="Canonical Routine state could not be read or written.", retryable=True)


def _view(value: object) -> RoutineResponse:
    return RoutineResponse(**asdict(value))


@router.get("/routines", response_model=list[RoutineResponse], operation_id="temporal_list_routines")
async def list_routines(context: Context, application: Application, response: Response) -> list[RoutineResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        return [_view(item) for item in await application.list(self_person_ref=context.self_person_ref)]
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post("/routines", response_model=RoutineResponse, operation_id="temporal_create_routine")
async def create_routine(payload: CreateRoutineRequest, context: MutatingContext, application: Application, response: Response) -> RoutineResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return _view(await application.create(self_person_ref=context.self_person_ref, operation_id=payload.operation_id, title=payload.title, life_area_ref=payload.life_area_ref, tag_refs=tuple(payload.tag_refs)))
    except _Errors as exc:
        raise _problem(exc) from exc


async def _mutate(routine_ref: UUID, payload: RoutineMutationRequest, context: DanteContext, application: RoutineApplication, response: Response, kind: Literal["rename", "pause", "resume", "end"], title: str | None = None) -> RoutineMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.mutate(self_person_ref=context.self_person_ref, operation_id=payload.operation_id, routine_ref=routine_ref, expected_source_revision=payload.expected_source_revision, kind=kind, title=title)
        return RoutineMutationResponse(**asdict(value))
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post("/routines/{routine_ref}/rename", response_model=RoutineMutationResponse, operation_id="temporal_rename_routine")
async def rename_routine(routine_ref: UUID, payload: RenameRoutineRequest, context: MutatingContext, application: Application, response: Response) -> RoutineMutationResponse:
    return await _mutate(routine_ref, payload, context, application, response, "rename", payload.title)


@router.post("/routines/{routine_ref}/pause", response_model=RoutineMutationResponse, operation_id="temporal_pause_routine")
async def pause_routine(routine_ref: UUID, payload: RoutineMutationRequest, context: MutatingContext, application: Application, response: Response) -> RoutineMutationResponse:
    return await _mutate(routine_ref, payload, context, application, response, "pause")


@router.post("/routines/{routine_ref}/resume", response_model=RoutineMutationResponse, operation_id="temporal_resume_routine")
async def resume_routine(routine_ref: UUID, payload: RoutineMutationRequest, context: MutatingContext, application: Application, response: Response) -> RoutineMutationResponse:
    return await _mutate(routine_ref, payload, context, application, response, "resume")


@router.post("/routines/{routine_ref}/end", response_model=RoutineMutationResponse, operation_id="temporal_end_routine")
async def end_routine(routine_ref: UUID, payload: RoutineMutationRequest, context: MutatingContext, application: Application, response: Response) -> RoutineMutationResponse:
    return await _mutate(routine_ref, payload, context, application, response, "end")


@router.put("/routines/{routine_ref}/life-area", response_model=RoutineLifeAreaResponse, operation_id="temporal_assign_routine_life_area")
async def assign_life_area(routine_ref: UUID, payload: AssignRoutineLifeAreaRequest, context: MutatingContext, application: Application, response: Response) -> RoutineLifeAreaResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.assign_life_area(self_person_ref=context.self_person_ref, operation_id=payload.operation_id, routine_ref=routine_ref, life_area_ref=payload.life_area_ref, expected_assignment_revision=payload.expected_assignment_revision)
        return RoutineLifeAreaResponse(**asdict(value))
    except _Errors as exc:
        raise _problem(exc) from exc


async def _set_tag(routine_ref: UUID, tag_ref: UUID, payload: RoutineTagOperationRequest, context: DanteContext, application: RoutineApplication, response: Response, attached: bool) -> RoutineTagEffectResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.set_tag(self_person_ref=context.self_person_ref, operation_id=payload.operation_id, routine_ref=routine_ref, tag_ref=tag_ref, attached=attached)
        return RoutineTagEffectResponse(**asdict(value))
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post("/routines/{routine_ref}/tags/{tag_ref}/attach", response_model=RoutineTagEffectResponse, operation_id="temporal_attach_routine_tag")
async def attach_tag(routine_ref: UUID, tag_ref: UUID, payload: RoutineTagOperationRequest, context: MutatingContext, application: Application, response: Response) -> RoutineTagEffectResponse:
    return await _set_tag(routine_ref, tag_ref, payload, context, application, response, True)


@router.post("/routines/{routine_ref}/tags/{tag_ref}/detach", response_model=RoutineTagEffectResponse, operation_id="temporal_detach_routine_tag")
async def detach_tag(routine_ref: UUID, tag_ref: UUID, payload: RoutineTagOperationRequest, context: MutatingContext, application: Application, response: Response) -> RoutineTagEffectResponse:
    return await _set_tag(routine_ref, tag_ref, payload, context, application, response, False)
