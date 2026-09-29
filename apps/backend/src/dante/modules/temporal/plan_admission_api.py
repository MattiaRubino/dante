"""Explicitly reviewed B12-C single-candidate move and confirmation."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_mutating_dante_context
from dante.modules.temporal.plan_admission import (
    AdmissionResult,
    PlanAdmissionApplication,
    PlanAdmissionBlockedError,
    PlanAdmissionNotFoundError,
    PlanAdmissionReuseError,
    PlanAdmissionStaleError,
    ReviewedMove,
)
from dante.modules.temporal.plan_candidate import PlanCandidateNotFoundError
from dante.modules.temporal.plan_conflict import (
    PlanConflictInputError,
    PlanConflictNotFoundError,
    PlanConflictStateError,
)
from dante.modules.temporal.plan_dependency import PlanDependencyPersistenceError
from dante.modules.temporal.plan_work import PlanWorkPersistenceError
from dante.modules.temporal.temporal_constraint import TemporalConstraintPersistenceError
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/plans", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class ReviewedMoveBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: UUID
    expected_plan_state_ref: UUID
    expected_schedule_ref: UUID
    expected_schedule_state_ref: UUID
    expected_policy_state_ref: UUID
    basis_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    starts_at: datetime
    ends_at: datetime


class PlanAdmissionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["committed", "pending_confirmation"]
    schedule_ref: UUID
    proposal_ref: UUID | None
    placement_material_state_ref: UUID | None
    replayed: bool


def _application(request: Request) -> PlanAdmissionApplication:
    return PlanAdmissionApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[PlanAdmissionApplication, Depends(_application)]


def _review(plan_ref: UUID, step_ref: UUID, body: ReviewedMoveBody) -> ReviewedMove:
    return ReviewedMove(
        plan_ref=plan_ref, step_ref=step_ref,
        plan_state_ref=body.expected_plan_state_ref,
        schedule_ref=body.expected_schedule_ref,
        schedule_state_ref=body.expected_schedule_state_ref,
        policy_state_ref=body.expected_policy_state_ref,
        basis_fingerprint=body.basis_fingerprint,
        starts_at=body.starts_at, ends_at=body.ends_at,
        operation_id=str(body.operation_id),
    )


def _result(value: AdmissionResult) -> PlanAdmissionResponse:
    return PlanAdmissionResponse(
        kind=value.kind, schedule_ref=value.schedule_ref,
        proposal_ref=value.proposal_ref,
        placement_material_state_ref=value.placement_state_ref,
        replayed=value.replayed,
    )


def _raise_problem(exc: Exception) -> None:
    if isinstance(exc, (PlanCandidateNotFoundError, PlanConflictNotFoundError,
                        PlanAdmissionNotFoundError)):
        raise ProblemError(
            status=404, code="temporal.plan_admission.unavailable", category="not_found",
            title="Reviewed move unavailable", detail=str(exc),
        ) from exc
    if isinstance(exc, PlanAdmissionBlockedError):
        raise ProblemError(
            status=409, code="temporal.plan_admission.blocked", category="conflict",
            title="Move blocked", detail=str(exc),
        ) from exc
    if isinstance(exc, PlanAdmissionReuseError):
        raise ProblemError(
            status=409, code="temporal.plan_admission.operation_reused", category="conflict",
            title="Operation id reused", detail=str(exc),
        ) from exc
    if isinstance(exc, (PlanAdmissionStaleError,
                        PlanConflictStateError,
                        PlanWorkPersistenceError, PlanDependencyPersistenceError,
                        TemporalConstraintPersistenceError)):
        raise ProblemError(
            status=409, code="temporal.plan_admission.stale", category="conflict",
            title="Reviewed move changed", detail=str(exc),
        ) from exc
    if isinstance(exc, PlanConflictInputError):
        raise ProblemError(
            status=422, code="temporal.plan_admission.limit", category="validation",
            title="Plan outside supported scope", detail=str(exc),
        ) from exc
    raise exc


@router.post(
    "/{plan_ref}/steps/{step_ref}/candidate-moves",
    response_model=PlanAdmissionResponse,
    responses={401: {"model": ProblemDetails}, 403: {"model": ProblemDetails},
               404: {"model": ProblemDetails}, 409: {"model": ProblemDetails},
               422: {"model": ProblemDetails}, 500: {"model": ProblemDetails}},
    operation_id="temporal_request_reviewed_plan_candidate_move",
)
async def request_reviewed_plan_candidate_move(
    plan_ref: UUID, step_ref: UUID, body: ReviewedMoveBody,
    context: Context, application: Application, response: Response,
) -> PlanAdmissionResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return _result(await application.request(
            self_ref=context.self_person_ref, review=_review(plan_ref, step_ref, body),
        ))
    except Exception as exc:
        _raise_problem(exc)
        raise AssertionError("unreachable") from exc


@router.post(
    "/{plan_ref}/steps/{step_ref}/candidate-moves/{proposal_ref}/confirm",
    response_model=PlanAdmissionResponse,
    responses={401: {"model": ProblemDetails}, 403: {"model": ProblemDetails},
               404: {"model": ProblemDetails}, 409: {"model": ProblemDetails},
               422: {"model": ProblemDetails}, 500: {"model": ProblemDetails}},
    operation_id="temporal_confirm_reviewed_plan_candidate_move",
)
async def confirm_reviewed_plan_candidate_move(
    plan_ref: UUID, step_ref: UUID, proposal_ref: UUID, body: ReviewedMoveBody,
    context: Context, application: Application, response: Response,
) -> PlanAdmissionResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return _result(await application.accept(
            self_ref=context.self_person_ref, review=_review(plan_ref, step_ref, body),
            proposal_ref=proposal_ref,
        ))
    except Exception as exc:
        _raise_problem(exc)
        raise AssertionError("unreachable") from exc
