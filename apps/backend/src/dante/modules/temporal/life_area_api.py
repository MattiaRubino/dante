"""Authenticated self-scoped B05-A Life Area catalog and lifecycle."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.life_area import (
    LifeAreaApplication,
    LifeAreaInputError,
    LifeAreaNotFoundError,
    LifeAreaOperationIdReuseError,
    LifeAreaPersistenceError,
    LifeAreaStateConflictError,
    LifeAreaView,
)
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/life-areas", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _application(request: Request) -> LifeAreaApplication:
    runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return LifeAreaApplication(runtime.session_factory)


Application = Annotated[LifeAreaApplication, Depends(_application)]


class CreateLifeAreaRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    name: str = Field(min_length=1, max_length=100)


class MutationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_revision: int = Field(ge=1)


class RenameLifeAreaRequest(MutationRequest):
    name: str = Field(min_length=1, max_length=100)


class VisibilityLifeAreaRequest(MutationRequest):
    hidden: bool


class AppearanceLifeAreaRequest(MutationRequest):
    icon_code: str | None = Field(default=None, max_length=40)
    color_code: str | None = Field(default=None, max_length=7)


class OrderEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    life_area_ref: UUID
    expected_revision: int = Field(ge=1)


class ReorderLifeAreasRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    entries: list[OrderEntry] = Field(max_length=500)


class LifeAreaResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    life_area_ref: UUID
    name: str
    created_at: datetime
    revision: int
    sort_order: int
    archived: bool
    hidden: bool
    icon_code: str | None
    color_code: str | None
    updated_at: datetime
    replayed: bool = False


class LifeAreaMutationResponse(BaseModel):
    life_area_ref: UUID
    accepted_revision: int
    replayed: bool


class LifeAreaReorderResponse(BaseModel):
    affected_count: int
    replayed: bool


def _response(area: LifeAreaView, *, replayed: bool = False) -> LifeAreaResponse:
    if area.updated_at is None:
        raise LifeAreaPersistenceError("Life Area timestamp is unavailable.")
    return LifeAreaResponse(
        life_area_ref=area.life_area_ref,
        name=area.name,
        created_at=area.created_at,
        revision=area.revision,
        sort_order=area.sort_order,
        archived=area.archived,
        hidden=area.hidden,
        icon_code=area.icon_code,
        color_code=area.color_code,
        updated_at=area.updated_at,
        replayed=replayed,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, LifeAreaInputError):
        return ProblemError(
            status=422,
            code="temporal.life_area.invalid_input",
            category="validation",
            title="Invalid Life Area input",
            detail=str(exc),
            retryable=False,
        )
    if isinstance(exc, LifeAreaNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.life_area.not_found",
            category="not_found",
            title="Life Area unavailable",
            detail="No Life Area is available in this self scope.",
            retryable=False,
        )
    if isinstance(exc, LifeAreaOperationIdReuseError):
        return ProblemError(
            status=409,
            code="temporal.life_area.operation_id_reused",
            category="conflict",
            title="Life Area operation conflict",
            detail="This operation id was used for different intent.",
            retryable=False,
        )
    if isinstance(exc, LifeAreaStateConflictError):
        return ProblemError(
            status=409,
            code="temporal.life_area.state_conflict",
            category="conflict",
            title="Life Area state changed",
            detail="Refresh the catalog and submit the new revision.",
            retryable=False,
        )
    return ProblemError(
        status=503,
        code="temporal.life_area.persistence_unavailable",
        category="service",
        title="Life Areas unavailable",
        detail="The operation could not complete safely.",
        retryable=True,
    )


_Errors = (
    LifeAreaInputError,
    LifeAreaNotFoundError,
    LifeAreaOperationIdReuseError,
    LifeAreaStateConflictError,
    LifeAreaPersistenceError,
)


@router.post(
    "", status_code=201, response_model=LifeAreaResponse, operation_id="temporal_create_life_area"
)
async def create_life_area(
    payload: CreateLifeAreaRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            name=payload.name,
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    if result.replayed:
        response.status_code = 200
    return _response(result.area, replayed=result.replayed)


@router.get("", response_model=list[LifeAreaResponse], operation_id="temporal_list_life_areas")
async def list_life_areas(
    context: Context, application: Application, response: Response
) -> list[LifeAreaResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        areas = await application.list(self_person_ref=context.self_person_ref)
    except _Errors as exc:
        raise _problem(exc) from exc
    return [_response(area) for area in areas]


@router.put(
    "/order", response_model=LifeAreaReorderResponse, operation_id="temporal_reorder_life_areas"
)
async def reorder_life_areas(
    payload: ReorderLifeAreasRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaReorderResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.reorder(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            entries=tuple(
                (entry.life_area_ref, entry.expected_revision) for entry in payload.entries
            ),
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    return LifeAreaReorderResponse(affected_count=result.affected_count, replayed=result.replayed)


async def _mutate(
    application: LifeAreaApplication,
    context: DanteContext,
    response: Response,
    life_area_ref: UUID,
    payload: MutationRequest,
    kind: str,
    **fields: object,
) -> LifeAreaMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.mutate(
            self_person_ref=context.self_person_ref,
            life_area_ref=life_area_ref,
            operation_id=payload.operation_id,
            expected_revision=payload.expected_revision,
            kind=kind,
            name=cast(str | None, fields.get("name")),
            hidden=cast(bool | None, fields.get("hidden")),
            icon_code=cast(str | None, fields.get("icon_code")),
            color_code=cast(str | None, fields.get("color_code")),
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    return LifeAreaMutationResponse(
        life_area_ref=life_area_ref,
        accepted_revision=result.accepted_revision,
        replayed=result.replayed,
    )


@router.patch(
    "/{life_area_ref}/name",
    response_model=LifeAreaMutationResponse,
    operation_id="temporal_rename_life_area",
)
async def rename_life_area(
    life_area_ref: UUID,
    payload: RenameLifeAreaRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaMutationResponse:
    return await _mutate(
        application, context, response, life_area_ref, payload, "rename", name=payload.name
    )


@router.post(
    "/{life_area_ref}/archive",
    response_model=LifeAreaMutationResponse,
    operation_id="temporal_archive_life_area",
)
async def archive_life_area(
    life_area_ref: UUID,
    payload: MutationRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaMutationResponse:
    return await _mutate(application, context, response, life_area_ref, payload, "archive")


@router.put(
    "/{life_area_ref}/visibility",
    response_model=LifeAreaMutationResponse,
    operation_id="temporal_set_life_area_visibility",
)
async def set_life_area_visibility(
    life_area_ref: UUID,
    payload: VisibilityLifeAreaRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaMutationResponse:
    return await _mutate(
        application, context, response, life_area_ref, payload, "visibility", hidden=payload.hidden
    )


@router.put(
    "/{life_area_ref}/appearance",
    response_model=LifeAreaMutationResponse,
    operation_id="temporal_set_life_area_appearance",
)
async def set_life_area_appearance(
    life_area_ref: UUID,
    payload: AppearanceLifeAreaRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> LifeAreaMutationResponse:
    return await _mutate(
        application,
        context,
        response,
        life_area_ref,
        payload,
        "appearance",
        icon_code=payload.icon_code,
        color_code=payload.color_code,
    )
