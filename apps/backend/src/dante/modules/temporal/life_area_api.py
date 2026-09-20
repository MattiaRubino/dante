"""Authenticated B05-A1 Life Area product catalog (no item assignment yet)."""

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
    LifeAreaOperationIdReuseError,
    LifeAreaPersistenceError,
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


class LifeAreaResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    life_area_ref: UUID
    name: str
    created_at: datetime
    replayed: bool = False


def _response(area: LifeAreaView, *, replayed: bool = False) -> LifeAreaResponse:
    return LifeAreaResponse(
        life_area_ref=area.life_area_ref,
        name=area.name,
        created_at=area.created_at,
        replayed=replayed,
    )


@router.post(
    "",
    status_code=201,
    response_model=LifeAreaResponse,
    operation_id="temporal_create_life_area",
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
    except LifeAreaInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.life_area.invalid_create",
            category="validation",
            title="Invalid Life Area",
            detail=str(exc),
            retryable=False,
        ) from exc
    except LifeAreaOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.life_area.operation_id_reused",
            category="conflict",
            title="Life Area operation conflict",
            detail="This operation id was already used for a different Life Area name.",
            retryable=False,
        ) from exc
    except LifeAreaPersistenceError as exc:
        raise _unavailable() from exc
    if result.replayed:
        response.status_code = 200
    return _response(result.area, replayed=result.replayed)


@router.get("", response_model=list[LifeAreaResponse], operation_id="temporal_list_life_areas")
async def list_life_areas(
    context: Context,
    application: Application,
    response: Response,
) -> list[LifeAreaResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        areas = await application.list(self_person_ref=context.self_person_ref)
    except LifeAreaPersistenceError as exc:
        raise _unavailable() from exc
    return [_response(area) for area in areas]


def _unavailable() -> ProblemError:
    return ProblemError(
        status=503,
        code="temporal.life_area.persistence_unavailable",
        category="service",
        title="Life Areas unavailable",
        detail="The operation could not complete safely.",
        retryable=True,
    )
