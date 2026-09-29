"""B12-A authenticated, read-only Plan conflict diagnosis HTTP surface."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.plan_conflict import (
    PlanConflictApplication,
    PlanConflictInputError,
    PlanConflictNotFoundError,
    PlanConflictStateError,
    PlanDiagnosis,
)
from dante.modules.temporal.plan_dependency import PlanDependencyPersistenceError
from dante.modules.temporal.plan_work import PlanWorkPersistenceError
from dante.modules.temporal.temporal_constraint import TemporalConstraintPersistenceError
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/plans", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]


class PlacementBasisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    material_state_ref: UUID
    temporal_form_code: str
    starts_at: datetime | None
    ends_at: datetime | None


class ConstraintFindingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constraint_ref: UUID
    material_state_ref: UUID
    strength: Literal["hard", "soft"]
    evaluation: Literal["satisfied", "violated", "not_evaluable"]
    reason_code: str


class DependencyFindingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dependency_ref: UUID
    state_ref: UUID
    prerequisite_step_ref: UUID
    qualifier_code: Literal["actual_occurred", "outcome_code"]
    evaluation_code: Literal["satisfied", "unsatisfied", "unknown"] | None
    actual_material_state_ref: UUID | None
    outcome_material_state_ref: UUID | None
    cycle: bool


class StepDiagnosisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_ref: UUID
    title: str
    activity_ref: UUID | None
    placements: list[PlacementBasisResponse]
    constraints: list[ConstraintFindingResponse]
    constraint_status: str | None
    hard_set_status: str | None
    dependencies: list[DependencyFindingResponse]
    diagnostics: list[Literal[
        "unlinked_step", "unknown_basis", "multiple_current_placements",
        "unsupported_placement", "known_hard_violation", "dependency_cycle",
        "blocked_prerequisite", "no_known_conflict_in_supported_rules",
    ]]


class PlanDiagnosisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_ref: UUID
    plan_state_ref: UUID
    title: str
    capacity_evaluated: bool
    steps: list[StepDiagnosisResponse]


def _application(request: Request) -> PlanConflictApplication:
    return PlanConflictApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[PlanConflictApplication, Depends(_application)]


@router.get(
    "/{plan_ref}/conflicts",
    response_model=PlanDiagnosisResponse,
    responses={
        401: {"model": ProblemDetails}, 403: {"model": ProblemDetails},
        404: {"model": ProblemDetails}, 409: {"model": ProblemDetails},
        422: {"model": ProblemDetails}, 500: {"model": ProblemDetails},
    },
    operation_id="temporal_diagnose_self_plan_conflicts",
)
async def diagnose_self_plan_conflicts(
    plan_ref: UUID,
    expected_state_ref: UUID,
    context: Context,
    application: Application,
    response: Response,
) -> PlanDiagnosisResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        view = await application.inspect(
            self_person_ref=context.self_person_ref,
            plan_ref=plan_ref,
            expected_state_ref=expected_state_ref,
        )
    except PlanConflictNotFoundError as exc:
        raise ProblemError(
            status=404, code="temporal.plan_conflict.unavailable", category="not_found",
            title="Plan unavailable", detail=str(exc),
        ) from exc
    except PlanConflictInputError as exc:
        raise ProblemError(
            status=422, code="temporal.plan_conflict.limit", category="validation",
            title="Diagnosis outside supported scope", detail=str(exc),
        ) from exc
    except PlanConflictStateError as exc:
        raise ProblemError(
            status=409, code="temporal.plan_conflict.stale", category="conflict",
            title="Diagnosis basis changed", detail=str(exc),
        ) from exc
    except (
        PlanWorkPersistenceError, PlanDependencyPersistenceError,
        TemporalConstraintPersistenceError,
    ) as exc:
        raise ProblemError(
            status=409, code="temporal.plan_conflict.unreadable", category="conflict",
            title="Diagnosis unavailable", detail="Current Plan truth could not be read.",
        ) from exc
    return _response(view)


def _response(view: PlanDiagnosis) -> PlanDiagnosisResponse:
    return PlanDiagnosisResponse(
        plan_ref=view.plan_ref, plan_state_ref=view.plan_state_ref,
        title=view.title, capacity_evaluated=view.capacity_evaluated,
        steps=[StepDiagnosisResponse(
            step_ref=step.step_ref, title=step.title, activity_ref=step.activity_ref,
            placements=[PlacementBasisResponse(
                schedule_ref=item.schedule_ref,
                material_state_ref=item.material_state_ref,
                temporal_form_code=item.temporal_form_code,
                starts_at=item.starts_at, ends_at=item.ends_at,
            ) for item in step.placements],
            constraint_status=step.constraint_status,
            hard_set_status=step.hard_set_status,
            constraints=[ConstraintFindingResponse(
                constraint_ref=item.constraint_ref,
                material_state_ref=item.material_state_ref,
                strength=item.strength, evaluation=item.evaluation,
                reason_code=item.reason_code,
            ) for item in step.constraints],
            dependencies=[DependencyFindingResponse(
                dependency_ref=item.dependency_ref,
                state_ref=item.state_ref,
                prerequisite_step_ref=item.prerequisite_step_ref,
                qualifier_code=item.qualifier_code,
                evaluation_code=item.evaluation_code,
                actual_material_state_ref=item.actual_material_state_ref,
                outcome_material_state_ref=item.outcome_material_state_ref,
                cycle=item.cycle,
            ) for item in step.dependencies],
            diagnostics=list(step.diagnostics),
        ) for step in view.steps],
    )
