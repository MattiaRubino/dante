"""Authenticated read-only B12-B Plan Step candidate endpoint."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.movement_policy import MovementPolicyPersistenceError
from dante.modules.temporal.plan_candidate import (
    PlanCandidateApplication,
    PlanCandidateNotFoundError,
    PlanCandidateView,
)
from dante.modules.temporal.plan_conflict import (
    PlanConflictInputError,
    PlanConflictNotFoundError,
    PlanConflictStateError,
)
from dante.modules.temporal.plan_conflict_api import (
    ConstraintFindingResponse,
    DependencyFindingResponse,
    PlacementBasisResponse,
)
from dante.modules.temporal.plan_dependency import PlanDependencyPersistenceError
from dante.modules.temporal.plan_work import PlanWorkPersistenceError
from dante.modules.temporal.temporal_constraint import TemporalConstraintPersistenceError
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/plans", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]


class ConstraintBasisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constraint_ref: UUID
    material_state_ref: UUID | None


class CandidateIntervalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    starts_at: datetime
    ends_at: datetime
    grid_index: int
    soft_findings: list[ConstraintFindingResponse]


class PlanCandidateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_ref: UUID
    plan_state_ref: UUID
    step_ref: UUID
    step_title: str
    activity_ref: UUID | None
    placement: PlacementBasisResponse | None
    dependencies: list[DependencyFindingResponse]
    constraint_states: list[ConstraintBasisResponse]
    movement_policy_material_state_ref: UUID | None
    movement_policy_status: Literal["automatic", "blocked", "missing"]
    basis_status: Literal["supported", "unknown", "blocked", "unsupported"]
    reason_code: str
    solver_status: Literal["OPTIMAL", "FEASIBLE", "INFEASIBLE", "MODEL_INVALID", "UNKNOWN"] | None
    candidates: list[CandidateIntervalResponse]
    horizon_starts_at: datetime | None
    horizon_ends_at: datetime | None
    duration_microseconds: int | None
    grid_minutes: int
    grid_size: int
    max_seconds_per_solve: float
    model_version: str
    solver_version: str
    capacity_evaluated: bool


def _application(request: Request) -> PlanCandidateApplication:
    return PlanCandidateApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[PlanCandidateApplication, Depends(_application)]


@router.get(
    "/{plan_ref}/steps/{step_ref}/candidates",
    response_model=PlanCandidateResponse,
    responses={
        401: {"model": ProblemDetails}, 403: {"model": ProblemDetails},
        404: {"model": ProblemDetails}, 409: {"model": ProblemDetails},
        422: {"model": ProblemDetails}, 500: {"model": ProblemDetails},
    },
    operation_id="temporal_search_self_plan_step_candidates",
)
async def search_self_plan_step_candidates(
    plan_ref: UUID, step_ref: UUID, expected_state_ref: UUID,
    context: Context, application: Application, response: Response,
) -> PlanCandidateResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        view = await application.search(
            self_person_ref=context.self_person_ref, plan_ref=plan_ref,
            step_ref=step_ref, expected_state_ref=expected_state_ref,
        )
    except (PlanConflictNotFoundError, PlanCandidateNotFoundError) as exc:
        raise ProblemError(
            status=404, code="temporal.plan_candidate.unavailable", category="not_found",
            title="Plan Step unavailable", detail=str(exc),
        ) from exc
    except PlanConflictInputError as exc:
        raise ProblemError(
            status=422, code="temporal.plan_candidate.limit", category="validation",
            title="Candidate scope exceeded", detail=str(exc),
        ) from exc
    except PlanConflictStateError as exc:
        raise ProblemError(
            status=409, code="temporal.plan_candidate.stale", category="conflict",
            title="Candidate basis changed", detail=str(exc),
        ) from exc
    except (
        PlanWorkPersistenceError, PlanDependencyPersistenceError,
        TemporalConstraintPersistenceError, MovementPolicyPersistenceError,
    ) as exc:
        raise ProblemError(
            status=409, code="temporal.plan_candidate.unreadable", category="conflict",
            title="Candidate basis unavailable", detail="Current Plan truth could not be read.",
        ) from exc
    return _response(view)


def _response(view: PlanCandidateView) -> PlanCandidateResponse:
    placement = view.placement
    return PlanCandidateResponse(
        plan_ref=view.plan_ref, plan_state_ref=view.plan_state_ref,
        step_ref=view.step_ref, step_title=view.step_title,
        activity_ref=view.activity_ref,
        placement=PlacementBasisResponse(
            schedule_ref=placement.schedule_ref,
            material_state_ref=placement.material_state_ref,
            temporal_form_code=placement.temporal_form_code,
            starts_at=placement.starts_at, ends_at=placement.ends_at,
        ) if placement else None,
        dependencies=[DependencyFindingResponse(
            dependency_ref=item.dependency_ref, state_ref=item.state_ref,
            prerequisite_step_ref=item.prerequisite_step_ref,
            qualifier_code=cast(Literal["actual_occurred", "outcome_code"], item.qualifier_code),
            evaluation_code=cast(Literal["satisfied", "unsatisfied", "unknown"] | None,
                                 item.evaluation_code),
            actual_material_state_ref=item.actual_material_state_ref,
            outcome_material_state_ref=item.outcome_material_state_ref, cycle=item.cycle,
        ) for item in view.dependencies],
        constraint_states=[ConstraintBasisResponse(
            constraint_ref=ref, material_state_ref=state,
        ) for ref, state in view.constraint_states],
        movement_policy_material_state_ref=view.movement_policy_material_state_ref,
        movement_policy_status=view.movement_policy_status,
        basis_status=view.basis_status, reason_code=view.reason_code,
        solver_status=view.solver_status,
        candidates=[CandidateIntervalResponse(
            starts_at=item.starts_at, ends_at=item.ends_at,
            grid_index=item.grid_index,
            soft_findings=[ConstraintFindingResponse(
                constraint_ref=rule.constraint_ref, material_state_ref=rule.material_state_ref,
                strength=cast(Literal["hard", "soft"], rule.strength),
                evaluation=cast(Literal["satisfied", "violated", "not_evaluable"],
                                rule.evaluation),
                reason_code=rule.reason_code,
            ) for rule in item.soft_findings],
        ) for item in view.candidates],
        horizon_starts_at=view.horizon_starts_at,
        horizon_ends_at=view.horizon_ends_at,
        duration_microseconds=view.duration_microseconds,
        grid_minutes=view.grid_minutes, grid_size=view.grid_size,
        max_seconds_per_solve=view.max_seconds_per_solve,
        model_version=view.model_version, solver_version=view.solver_version,
        capacity_evaluated=view.capacity_evaluated,
    )
