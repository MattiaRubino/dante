"""B13-A self-owned Plan work structure HTTP contract."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, cast
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
from dante.modules.temporal.temporal_constraint import (
    AbsoluteIntervalPlacement,
    TemporalConstraintApplication,
    TemporalConstraintInputError,
    TemporalConstraintPersistenceError,
)
from dante.platform.database.references import NativeRef
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/plans", tags=["temporal"])


class PlanStepBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_ref: UUID
    title: str = Field(min_length=1, max_length=300)
    activity_ref: UUID | None = None
    divisible: bool | None = None
    max_planned_slices: int | None = Field(default=None, ge=1, le=100)
    merge_compatible: bool | None = None
    execution_strength_code: Literal["hard", "soft"] | None = None


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
    divisible: bool | None
    max_planned_slices: int | None
    merge_compatible: bool | None
    execution_strength_code: Literal["hard", "soft"] | None


class ProposedSlice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slice_ref: UUID
    starts_at: datetime
    ends_at: datetime


class AssessExecutionBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_state_ref: UUID
    slices: list[ProposedSlice] = Field(max_length=100)
    merge_pair: tuple[UUID, UUID] | None = None


class TemporalRuleAssessment(BaseModel):
    constraint_ref: UUID
    strength: Literal["hard", "soft"]
    evaluation: Literal["satisfied", "violated", "not_evaluable"]
    reason_code: str
    constrained_facet: str


class SliceAssessment(BaseModel):
    slice_ref: UUID
    temporal_status: str
    hard_set_status: str
    temporal_rules: list[TemporalRuleAssessment]


class ExecutionAssessmentResponse(BaseModel):
    plan_ref: UUID
    state_ref: UUID
    step_ref: UUID
    activity_ref: UUID
    basis: str
    proposed_count: int
    count_status: str
    count_reason: str
    slice_assessments: list[SliceAssessment]
    merge_status: str
    merge_reason: str
    merged_temporal_status: str | None
    merged_temporal_rules: list[TemporalRuleAssessment]


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
                divisible=item.divisible,
                max_planned_slices=item.max_planned_slices,
                merge_compatible=item.merge_compatible,
                execution_strength_code=cast(
                    Literal["hard", "soft"] | None, item.execution_strength_code
                ),
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
                    divisible=item.divisible,
                    max_planned_slices=item.max_planned_slices,
                    merge_compatible=item.merge_compatible,
                    execution_strength_code=item.execution_strength_code,
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


@router.post(
    "/{plan_ref}/steps/{step_ref}/execution/assess",
    response_model=ExecutionAssessmentResponse,
    responses={404: {"model": ProblemDetails}, 409: {"model": ProblemDetails},
               422: {"model": ProblemDetails}},
    operation_id="temporal_assess_plan_step_execution",
)
async def assess_plan_step_execution(
    plan_ref: UUID,
    step_ref: UUID,
    payload: AssessExecutionBody,
    context: Context,
    application: Application,
    request: Request,
    response: Response,
) -> ExecutionAssessmentResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        plan = await application.get(self_person_ref=context.self_person_ref, plan_ref=plan_ref)
    except PlanWorkPersistenceError as exc:
        raise _problem(exc) from exc
    if plan is None:
        raise _problem(PlanWorkNotFoundError("Self Plan unavailable."))
    if plan.state_ref != payload.expected_state_ref:
        raise _problem(PlanWorkConflictError("Plan current state changed."))
    step = next((item for item in plan.steps if item.step_ref == step_ref), None)
    if step is None or step.activity_ref is None:
        raise _problem(PlanWorkNotFoundError("Linked Step unavailable."))
    by_ref = {item.slice_ref: item for item in payload.slices}
    if len(by_ref) != len(payload.slices):
        raise _problem(PlanWorkInputError("Proposed slice references must be distinct."))
    try:
        intervals = {
            item.slice_ref: AbsoluteIntervalPlacement(
                starts_at=item.starts_at, ends_at=item.ends_at
            ) for item in payload.slices
        }
    except TemporalConstraintInputError as exc:
        raise _problem(PlanWorkInputError(str(exc))) from exc

    if step.divisible is None or not payload.slices:
        count_status, count_reason = "unknown", (
            "policy_unconfigured" if step.divisible is None else "missing_proposed_slices"
        )
    elif step.max_planned_slices is None:
        count_status, count_reason = "satisfied", "unbounded_proposed_count"
    elif len(payload.slices) <= step.max_planned_slices:
        count_status, count_reason = "satisfied", "within_proposed_count_limit"
    else:
        count_status = "violated_hard" if step.execution_strength_code == "hard" else "violated_soft"
        count_reason = "proposed_count_exceeds_limit"

    temporal = TemporalConstraintApplication(request.app.state.database_runtime.session_factory)
    try:
        assessments = []
        for item in payload.slices:
            result = await temporal.evaluate_constraints(
                self_person_ref=context.self_person_ref,
                subject_native_ref=NativeRef(step.activity_ref),
                placement=intervals[item.slice_ref],
            )
            assessments.append(SliceAssessment(
                slice_ref=item.slice_ref,
                temporal_status=result.status,
                hard_set_status=result.hard_set_status,
                temporal_rules=[TemporalRuleAssessment(
                    constraint_ref=value.constraint_ref, strength=value.strength,
                    evaluation=value.evaluation, reason_code=value.reason_code,
                    constrained_facet=value.constrained_facet,
                ) for value in result.items],
            ))
        merge_status, merge_reason, merged_temporal_status = "not_requested", "no_pair", None
        merged_temporal_rules: list[TemporalRuleAssessment] = []
        if payload.merge_pair is not None:
            left_ref, right_ref = payload.merge_pair
            if left_ref == right_ref or left_ref not in intervals or right_ref not in intervals:
                raise PlanWorkInputError("Merge pair must identify two proposed slices.")
            left, right = intervals[left_ref], intervals[right_ref]
            if step.merge_compatible is None:
                merge_status, merge_reason = "unknown", "policy_unconfigured"
            elif not step.merge_compatible:
                merge_status, merge_reason = "incompatible", "merge_disallowed"
            elif left.ends_at != right.starts_at and right.ends_at != left.starts_at:
                merge_status, merge_reason = "incompatible", "not_contiguous"
            else:
                merged = AbsoluteIntervalPlacement(
                    starts_at=min(left.starts_at, right.starts_at),
                    ends_at=max(left.ends_at, right.ends_at),
                )
                result = await temporal.evaluate_constraints(
                    self_person_ref=context.self_person_ref,
                    subject_native_ref=NativeRef(step.activity_ref),
                    placement=merged,
                )
                merged_temporal_status = result.status
                merged_temporal_rules = [TemporalRuleAssessment(
                    constraint_ref=value.constraint_ref, strength=value.strength,
                    evaluation=value.evaluation, reason_code=value.reason_code,
                    constrained_facet=value.constrained_facet,
                ) for value in result.items]
                if result.status == "not_evaluable":
                    merge_status, merge_reason = "unknown", "temporal_rule_not_evaluable"
                elif result.status == "inadmissible":
                    merge_status, merge_reason = "incompatible", "hard_temporal_rule_violated"
                else:
                    merge_status, merge_reason = "compatible", "contiguous_and_temporally_admissible"
    except (TemporalConstraintInputError, PlanWorkInputError) as exc:
        raise _problem(PlanWorkInputError(str(exc))) from exc
    except TemporalConstraintPersistenceError as exc:
        raise _problem(PlanWorkPersistenceError(str(exc))) from exc
    return ExecutionAssessmentResponse(
        plan_ref=plan_ref, state_ref=plan.state_ref, step_ref=step_ref,
        activity_ref=step.activity_ref, basis="explicit_proposed_slices",
        proposed_count=len(payload.slices), count_status=count_status,
        count_reason=count_reason, slice_assessments=assessments,
        merge_status=merge_status, merge_reason=merge_reason,
        merged_temporal_status=merged_temporal_status,
        merged_temporal_rules=merged_temporal_rules,
    )
