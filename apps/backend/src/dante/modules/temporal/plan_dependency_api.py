"""Plan-scoped B13-B qualified Dependency HTTP contract."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.plan_dependency import (
    PlanDependencyApplication,
    PlanDependencyConflictError,
    PlanDependencyHistoryView,
    PlanDependencyInputError,
    PlanDependencyNotFoundError,
    PlanDependencyPersistenceError,
    PlanDependencyView,
)
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/plans/{plan_ref}/dependencies", tags=["temporal"])


class CreatePlanDependencyBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    prerequisite_step_ref: UUID
    dependent_step_ref: UUID
    qualifier_code: str
    disposition_code: str | None = None


class RevisePlanDependencyBody(CreatePlanDependencyBody):
    expected_state_ref: UUID
    active: bool = True


class PlanDependencyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dependency_ref: UUID
    plan_ref: UUID
    prerequisite_step_ref: UUID
    prerequisite_activity_ref: UUID
    dependent_step_ref: UUID
    dependent_activity_ref: UUID
    state_ref: UUID
    purpose_code: str
    qualifier_code: str
    disposition_code: str | None
    active: bool
    recorded_at: datetime
    evaluation_code: str | None
    actual_material_state_ref: UUID | None
    outcome_material_state_ref: UUID | None
    cycle: bool
    replayed: bool


class PlanDependencyHistoryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    state_ref: UUID
    qualifier_code: str
    disposition_code: str | None
    active: bool
    recorded_at: datetime
    current_from_at: datetime
    current_until_at: datetime | None


def _application(request: Request) -> PlanDependencyApplication:
    return PlanDependencyApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[PlanDependencyApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(item: PlanDependencyView) -> PlanDependencyResponse:
    return PlanDependencyResponse(
        dependency_ref=item.dependency_ref,
        plan_ref=item.plan_ref,
        prerequisite_step_ref=item.prerequisite_step_ref,
        prerequisite_activity_ref=item.prerequisite_activity_ref,
        dependent_step_ref=item.dependent_step_ref,
        dependent_activity_ref=item.dependent_activity_ref,
        state_ref=item.state_ref,
        purpose_code=item.purpose_code,
        qualifier_code=item.qualifier_code,
        disposition_code=item.disposition_code,
        active=item.active,
        recorded_at=item.recorded_at,
        evaluation_code=item.evaluation_code,
        actual_material_state_ref=item.actual_material_state_ref,
        outcome_material_state_ref=item.outcome_material_state_ref,
        cycle=item.cycle,
        replayed=item.replayed,
    )


def _history(item: PlanDependencyHistoryView) -> PlanDependencyHistoryResponse:
    return PlanDependencyHistoryResponse(
        state_ref=item.state_ref,
        qualifier_code=item.qualifier_code,
        disposition_code=item.disposition_code,
        active=item.active,
        recorded_at=item.recorded_at,
        current_from_at=item.current_from_at,
        current_until_at=item.current_until_at,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, PlanDependencyInputError):
        return ProblemError(
            status=422,
            code="temporal.plan_dependency.invalid_input",
            category="validation",
            title="Dependency input rejected",
            detail=str(exc),
        )
    if isinstance(exc, PlanDependencyNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.plan_dependency.unavailable",
            category="not_found",
            title="Dependency unavailable",
            detail=str(exc),
        )
    if isinstance(exc, PlanDependencyConflictError):
        return ProblemError(
            status=409,
            code="temporal.plan_dependency.conflict",
            category="conflict",
            title="Dependency state conflict",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.plan_dependency.persistence",
        category="conflict",
        title="Dependency command rejected",
        detail="Dependency command was rejected.",
    )


@router.get(
    "",
    response_model=list[PlanDependencyResponse],
    responses={400: {"model": ProblemDetails}, 401: {"model": ProblemDetails}},
    operation_id="temporal_list_self_plan_dependencies",
)
async def list_self_plan_dependencies(
    plan_ref: UUID,
    context: Context,
    application: Application,
) -> list[PlanDependencyResponse]:
    try:
        return [
            _response(item)
            for item in await application.list(
                self_person_ref=context.self_person_ref, plan_ref=plan_ref
            )
        ]
    except PlanDependencyPersistenceError as exc:
        raise _problem(exc) from exc


@router.get(
    "/{dependency_ref}",
    response_model=PlanDependencyResponse,
    responses={
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
    },
    operation_id="temporal_get_self_plan_dependency",
)
async def get_self_plan_dependency(
    plan_ref: UUID,
    dependency_ref: UUID,
    context: Context,
    application: Application,
) -> PlanDependencyResponse:
    try:
        item = await application.get(
            self_person_ref=context.self_person_ref,
            plan_ref=plan_ref,
            dependency_ref=dependency_ref,
        )
    except PlanDependencyPersistenceError as exc:
        raise _problem(exc) from exc
    if item is None:
        raise _problem(PlanDependencyNotFoundError("Self Dependency unavailable."))
    return _response(item)


@router.get(
    "/{dependency_ref}/history",
    response_model=list[PlanDependencyHistoryResponse],
    responses={
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
    },
    operation_id="temporal_list_self_plan_dependency_history",
)
async def list_self_plan_dependency_history(
    plan_ref: UUID,
    dependency_ref: UUID,
    context: Context,
    application: Application,
) -> list[PlanDependencyHistoryResponse]:
    try:
        item = await application.get(
            self_person_ref=context.self_person_ref,
            plan_ref=plan_ref,
            dependency_ref=dependency_ref,
        )
        if item is None:
            raise PlanDependencyNotFoundError("Self Dependency unavailable.")
        return [
            _history(row)
            for row in await application.history(
                self_person_ref=context.self_person_ref,
                plan_ref=plan_ref,
                dependency_ref=dependency_ref,
            )
        ]
    except (PlanDependencyNotFoundError, PlanDependencyPersistenceError) as exc:
        raise _problem(exc) from exc


@router.post(
    "",
    response_model=PlanDependencyResponse,
    status_code=201,
    responses={
        200: {"model": PlanDependencyResponse},
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        403: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
        409: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
    },
    operation_id="temporal_create_self_plan_dependency",
)
async def create_self_plan_dependency(
    plan_ref: UUID,
    payload: CreatePlanDependencyBody,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> PlanDependencyResponse:
    try:
        item = await application.write(
            self_person_ref=context.self_person_ref,
            plan_ref=plan_ref,
            operation_id=payload.operation_id,
            prerequisite_step_ref=payload.prerequisite_step_ref,
            dependent_step_ref=payload.dependent_step_ref,
            qualifier_code=payload.qualifier_code,
            disposition_code=payload.disposition_code,
        )
    except (
        PlanDependencyInputError,
        PlanDependencyNotFoundError,
        PlanDependencyConflictError,
        PlanDependencyPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if item.replayed else 201
    return _response(item)


@router.put(
    "/{dependency_ref}",
    response_model=PlanDependencyResponse,
    responses={
        400: {"model": ProblemDetails},
        401: {"model": ProblemDetails},
        403: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
        409: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
    },
    operation_id="temporal_revise_self_plan_dependency",
)
async def revise_self_plan_dependency(
    plan_ref: UUID,
    dependency_ref: UUID,
    payload: RevisePlanDependencyBody,
    context: MutatingContext,
    application: Application,
) -> PlanDependencyResponse:
    try:
        item = await application.write(
            self_person_ref=context.self_person_ref,
            plan_ref=plan_ref,
            dependency_ref=dependency_ref,
            expected_state_ref=payload.expected_state_ref,
            operation_id=payload.operation_id,
            prerequisite_step_ref=payload.prerequisite_step_ref,
            dependent_step_ref=payload.dependent_step_ref,
            qualifier_code=payload.qualifier_code,
            disposition_code=payload.disposition_code,
            active=payload.active,
        )
    except (
        PlanDependencyInputError,
        PlanDependencyNotFoundError,
        PlanDependencyConflictError,
        PlanDependencyPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    return _response(item)
