"""B13-A self-owned Plan work structure HTTP contract."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.plan_work import (
    PlanStepInput,
    PlanWorkApplication,
    PlanWorkConflictError,
    PlanWorkInputError,
    PlanWorkNotFoundError,
    PlanWorkPersistenceError,
    PlanWorkView,
)
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/plans", tags=["temporal"])


class PlanStepBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_ref: UUID
    title: str = Field(min_length=1, max_length=300)
    activity_ref: UUID | None = None


class CreatePlanBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)


class ReplacePlanBody(CreatePlanBody):
    expected_state_ref: UUID
    steps: list[PlanStepBody] = Field(max_length=1000)


class PlanStepResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_ref: UUID
    position: int
    title: str
    activity_ref: UUID | None


class PlanWorkResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_ref: UUID
    state_ref: UUID
    title: str
    created_at: datetime
    steps: list[PlanStepResponse]
    replayed: bool


def _application(request: Request) -> PlanWorkApplication:
    return PlanWorkApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[PlanWorkApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: PlanWorkView) -> PlanWorkResponse:
    return PlanWorkResponse(
        plan_ref=view.plan_ref,
        state_ref=view.state_ref,
        title=view.title,
        created_at=view.created_at,
        steps=[
            PlanStepResponse(
                step_ref=item.step_ref,
                position=item.position,
                title=item.title,
                activity_ref=item.activity_ref,
            )
            for item in view.steps
        ],
        replayed=view.replayed,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, PlanWorkInputError):
        return ProblemError(
            status=422,
            code="temporal.plan.invalid_input",
            category="validation",
            title="Plan input rejected",
            detail=str(exc),
        )
    if isinstance(exc, PlanWorkNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.plan.unavailable",
            category="not_found",
            title="Plan unavailable",
            detail=str(exc),
        )
    if isinstance(exc, PlanWorkConflictError):
        return ProblemError(
            status=409,
            code="temporal.plan.conflict",
            category="conflict",
            title="Plan state conflict",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.plan.persistence",
        category="conflict",
        title="Plan command rejected",
        detail="Plan command was rejected.",
    )


@router.get(
    "",
    response_model=list[PlanWorkResponse],
    responses={
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        500: {"model": ProblemDetails},
    },
    operation_id="temporal_list_self_plans",
)
async def list_self_plans(
    context: Context,
    application: Application,
) -> list[PlanWorkResponse]:
    try:
        return [
            _response(view)
            for view in await application.list(self_person_ref=context.self_person_ref)
        ]
    except PlanWorkPersistenceError as exc:
        raise _problem(exc) from exc


@router.get(
    "/{plan_ref}",
    response_model=PlanWorkResponse,
    responses={
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
        500: {"model": ProblemDetails},
    },
    operation_id="temporal_get_self_plan",
)
async def get_self_plan(
    plan_ref: UUID,
    context: Context,
    application: Application,
) -> PlanWorkResponse:
    try:
        view = await application.get(self_person_ref=context.self_person_ref, plan_ref=plan_ref)
    except PlanWorkPersistenceError as exc:
        raise _problem(exc) from exc
    if view is None:
        raise _problem(PlanWorkNotFoundError("Self Plan unavailable."))
    return _response(view)


@router.post(
    "",
    response_model=PlanWorkResponse,
    status_code=201,
    responses={
        200: {"model": PlanWorkResponse},
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        403: {"model": ProblemDetails},
        409: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
        500: {"model": ProblemDetails},
    },
    operation_id="temporal_create_self_plan",
)
async def create_self_plan(
    payload: CreatePlanBody,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> PlanWorkResponse:
    try:
        view = await application.create(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
        )
    except (
        PlanWorkInputError,
        PlanWorkNotFoundError,
        PlanWorkConflictError,
        PlanWorkPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


@router.put(
    "/{plan_ref}",
    response_model=PlanWorkResponse,
    responses={
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        403: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
        409: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
        500: {"model": ProblemDetails},
    },
    operation_id="temporal_replace_self_plan_work",
)
async def replace_self_plan_work(
    plan_ref: UUID,
    payload: ReplacePlanBody,
    context: MutatingContext,
    application: Application,
) -> PlanWorkResponse:
    try:
        view = await application.replace(
            self_person_ref=context.self_person_ref,
            plan_ref=plan_ref,
            expected_state_ref=payload.expected_state_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            steps=tuple(
                PlanStepInput(
                    step_ref=item.step_ref,
                    title=item.title,
                    activity_ref=item.activity_ref,
                )
                for item in payload.steps
            ),
        )
    except (
        PlanWorkInputError,
        PlanWorkNotFoundError,
        PlanWorkConflictError,
        PlanWorkPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    return _response(view)
