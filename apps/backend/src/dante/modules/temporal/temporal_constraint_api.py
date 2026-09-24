"""Authenticated API for canonical Temporal Constraint authoring, reads and evaluation."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    AbsoluteIntervalPlacement,
    AbsoluteWindowRule,
    SessionMinimumDurationRule,
    ScheduleDurationRule,
    CreatedTemporalConstraintView,
    RevisedTemporalConstraintView,
    RetiredTemporalConstraintView,
    TemporalConstraintApplication,
    TemporalConstraintEvaluationView,
    TemporalConstraintInputError,
    TemporalConstraintNotFoundError,
    TemporalConstraintOperationIdReuseError,
    TemporalConstraintPersistenceError,
    TemporalConstraintRule,
    TemporalConstraintStateConflictError,
    TemporalConstraintView,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
DanteContextDependency = Annotated[DanteContext, Depends(require_dante_context)]
MutatingDanteContextDependency = Annotated[
    DanteContext,
    Depends(require_mutating_dante_context),
]


class AbsoluteEarliestStartRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["boundary"] = "boundary"
    boundary_kind: Literal["earliest_start"] = "earliest_start"
    constrained_facet: Literal["schedule.start"] = "schedule.start"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    boundary_at: datetime


class AbsoluteLatestStartRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["boundary"] = "boundary"
    boundary_kind: Literal["latest_start"] = "latest_start"
    constrained_facet: Literal["schedule.start"] = "schedule.start"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    boundary_at: datetime


class AbsoluteLatestCompletionRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["boundary"] = "boundary"
    boundary_kind: Literal["latest_completion"] = "latest_completion"
    constrained_facet: Literal["schedule.completion"] = "schedule.completion"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    boundary_at: datetime


class AbsoluteStartWithinWindowRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["window"] = "window"
    relationship: Literal["start_within"] = "start_within"
    constrained_facet: Literal["schedule.start"] = "schedule.start"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime


class AbsoluteCompletionWithinWindowRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["window"] = "window"
    relationship: Literal["completion_within"] = "completion_within"
    constrained_facet: Literal["schedule.completion"] = "schedule.completion"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime


class AbsoluteFullPlacementContainedWindowRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["window"] = "window"
    relationship: Literal["full_placement_contained"] = "full_placement_contained"
    constrained_facet: Literal["schedule.placement"] = "schedule.placement"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime


class AbsolutePlacementOverlapsWindowRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["window"] = "window"
    relationship: Literal["placement_overlaps"] = "placement_overlaps"
    constrained_facet: Literal["schedule.placement"] = "schedule.placement"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime


class SessionMinimumDurationRuleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family: Literal["duration"] = "duration"
    duration_kind: Literal["minimum"] = "minimum"
    constrained_facet: Literal["session.active_duration"] = "session.active_duration"
    strength: Literal["soft"] = "soft"
    duration_microseconds: int = Field(gt=0)


TemporalConstraintRuleRequest = (
    AbsoluteEarliestStartRuleRequest
    | AbsoluteLatestStartRuleRequest
    | AbsoluteLatestCompletionRuleRequest
    | AbsoluteStartWithinWindowRuleRequest
    | AbsoluteCompletionWithinWindowRuleRequest
    | AbsoluteFullPlacementContainedWindowRuleRequest
    | AbsolutePlacementOverlapsWindowRuleRequest
    | SessionMinimumDurationRuleRequest
)


class CreateTemporalConstraintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    subject_ref: UUID
    rule: TemporalConstraintRuleRequest


class ReviseTemporalConstraintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID
    rule: TemporalConstraintRuleRequest


class RetireTemporalConstraintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID


class AbsoluteEarliestStartCurrentRuleResponse(AbsoluteEarliestStartRuleRequest):
    material_state_ref: UUID


class AbsoluteLatestStartCurrentRuleResponse(AbsoluteLatestStartRuleRequest):
    material_state_ref: UUID


class AbsoluteLatestCompletionCurrentRuleResponse(AbsoluteLatestCompletionRuleRequest):
    material_state_ref: UUID


class AbsoluteStartWithinWindowCurrentRuleResponse(AbsoluteStartWithinWindowRuleRequest):
    material_state_ref: UUID


class AbsoluteCompletionWithinWindowCurrentRuleResponse(AbsoluteCompletionWithinWindowRuleRequest):
    material_state_ref: UUID


class AbsoluteFullPlacementContainedWindowCurrentRuleResponse(
    AbsoluteFullPlacementContainedWindowRuleRequest
):
    material_state_ref: UUID


class AbsolutePlacementOverlapsWindowCurrentRuleResponse(
    AbsolutePlacementOverlapsWindowRuleRequest
):
    material_state_ref: UUID


class TemporalConstraintCurrentDurationRuleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    family: Literal["duration"] = "duration"
    duration_kind: Literal["minimum", "maximum"]
    constrained_facet: Literal["schedule.placement", "session.active_duration"]
    strength: Literal["hard", "soft"]
    duration_microseconds: int = Field(gt=0)
    material_state_ref: UUID


TemporalConstraintCurrentRuleResponse = (
    AbsoluteEarliestStartCurrentRuleResponse
    | AbsoluteLatestStartCurrentRuleResponse
    | AbsoluteLatestCompletionCurrentRuleResponse
    | AbsoluteStartWithinWindowCurrentRuleResponse
    | AbsoluteCompletionWithinWindowCurrentRuleResponse
    | AbsoluteFullPlacementContainedWindowCurrentRuleResponse
    | AbsolutePlacementOverlapsWindowCurrentRuleResponse
    | TemporalConstraintCurrentDurationRuleResponse
)


class TemporalConstraintResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    constraint_ref: UUID
    subject_ref: UUID
    subject_kind: Literal["activity", "event"]
    status: Literal["active", "retired"]
    current_rule: TemporalConstraintCurrentRuleResponse | None


class TemporalConstraintListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[TemporalConstraintResponse]


class CreatedTemporalConstraintResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    constraint_ref: UUID
    subject_ref: UUID
    subject_kind: Literal["activity", "event"]
    material_state_ref: UUID
    rule: TemporalConstraintRuleRequest
    recorded_at: datetime
    replayed: bool = False


class RevisedTemporalConstraintResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    constraint_ref: UUID
    subject_ref: UUID
    subject_kind: Literal["activity", "event"]
    previous_material_state_ref: UUID
    material_state_ref: UUID
    rule: TemporalConstraintRuleRequest
    recorded_at: datetime
    replayed: bool = False


class RetiredTemporalConstraintResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    constraint_ref: UUID
    subject_ref: UUID
    subject_kind: Literal["activity", "event"]
    previous_material_state_ref: UUID
    recorded_at: datetime
    replayed: bool = False


class AbsoluteIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    form: Literal["absolute_interval"] = "absolute_interval"
    starts_at: datetime
    ends_at: datetime


class EvaluateTemporalConstraintsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subject_ref: UUID
    placement: AbsoluteIntervalPlacementRequest


class TemporalConstraintEvaluationItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    constraint_ref: UUID
    material_state_ref: UUID
    family: Literal["boundary", "window"]
    rule_code: str
    constrained_facet: Literal["schedule.start", "schedule.completion", "schedule.placement"]
    strength: Literal["hard", "soft"]
    evaluation: Literal["satisfied", "violated", "not_evaluable"]
    reason_code: str


class TemporalConstraintEvaluationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subject_ref: UUID
    placement: AbsoluteIntervalPlacementRequest
    status: Literal[
        "admissible",
        "admissible_with_soft_violations",
        "inadmissible",
        "not_evaluable",
    ]
    hard_set_status: Literal["feasible", "infeasible", "undetermined"]
    items: list[TemporalConstraintEvaluationItemResponse]


def get_temporal_constraint_application(request: Request) -> TemporalConstraintApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalConstraintApplication(database_runtime.session_factory)


TemporalConstraintApplicationDependency = Annotated[
    TemporalConstraintApplication,
    Depends(get_temporal_constraint_application),
]


def _rule_from_request(payload: TemporalConstraintRuleRequest) -> TemporalConstraintRule:
    if isinstance(payload, SessionMinimumDurationRuleRequest):
        return SessionMinimumDurationRule(
            duration_microseconds=payload.duration_microseconds,
        )
    if isinstance(
        payload,
        (
            AbsoluteStartWithinWindowRuleRequest,
            AbsoluteCompletionWithinWindowRuleRequest,
            AbsoluteFullPlacementContainedWindowRuleRequest,
            AbsolutePlacementOverlapsWindowRuleRequest,
        ),
    ):
        return AbsoluteWindowRule(
            relationship=payload.relationship,
            constrained_facet=payload.constrained_facet,
            strength=payload.strength,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
        )
    return AbsoluteBoundaryRule(
        boundary_kind=payload.boundary_kind,
        constrained_facet=payload.constrained_facet,
        strength=payload.strength,
        boundary_at=payload.boundary_at,
    )


def _rule_request(rule: TemporalConstraintRule) -> TemporalConstraintRuleRequest:
    if isinstance(rule, SessionMinimumDurationRule):
        return SessionMinimumDurationRuleRequest(
            duration_microseconds=rule.duration_microseconds,
        )
    if isinstance(rule, ScheduleDurationRule):
        raise TemporalConstraintInputError(
            "Schedule duration API request is not activated on this route."
        )
    if isinstance(rule, AbsoluteWindowRule):
        common = {
            "strength": rule.strength,
            "starts_at": rule.starts_at,
            "ends_at": rule.ends_at,
        }
        if rule.relationship == "start_within":
            return AbsoluteStartWithinWindowRuleRequest(**common)
        if rule.relationship == "completion_within":
            return AbsoluteCompletionWithinWindowRuleRequest(**common)
        if rule.relationship == "full_placement_contained":
            return AbsoluteFullPlacementContainedWindowRuleRequest(**common)
        return AbsolutePlacementOverlapsWindowRuleRequest(**common)
    if rule.boundary_kind == "earliest_start":
        return AbsoluteEarliestStartRuleRequest(
            strength=rule.strength,
            boundary_at=rule.boundary_at,
        )
    if rule.boundary_kind == "latest_start":
        return AbsoluteLatestStartRuleRequest(
            strength=rule.strength,
            boundary_at=rule.boundary_at,
        )
    return AbsoluteLatestCompletionRuleRequest(
        strength=rule.strength,
        boundary_at=rule.boundary_at,
    )


def _current_rule_response(
    value: TemporalConstraintView,
) -> TemporalConstraintCurrentRuleResponse | None:
    current_rule = value.current_rule
    if current_rule is None:
        return None
    if current_rule.family == "window":
        common = {
            "material_state_ref": current_rule.material_state_ref,
            "strength": current_rule.strength,
            "starts_at": current_rule.starts_at,
            "ends_at": current_rule.ends_at,
        }
        if current_rule.relationship == "start_within":
            return AbsoluteStartWithinWindowCurrentRuleResponse(**common)
        if current_rule.relationship == "completion_within":
            return AbsoluteCompletionWithinWindowCurrentRuleResponse(**common)
        if current_rule.relationship == "full_placement_contained":
            return AbsoluteFullPlacementContainedWindowCurrentRuleResponse(**common)
        return AbsolutePlacementOverlapsWindowCurrentRuleResponse(**common)
    if current_rule.family == "duration":
        return TemporalConstraintCurrentDurationRuleResponse(
            material_state_ref=current_rule.material_state_ref,
            duration_kind=current_rule.duration_kind,
            constrained_facet=current_rule.constrained_facet,
            strength=current_rule.strength,
            duration_microseconds=current_rule.duration_microseconds,
        )
    common = {
        "material_state_ref": current_rule.material_state_ref,
        "strength": current_rule.strength,
        "boundary_at": current_rule.boundary_at,
    }
    if current_rule.boundary_kind == "earliest_start":
        return AbsoluteEarliestStartCurrentRuleResponse(**common)
    if current_rule.boundary_kind == "latest_start":
        return AbsoluteLatestStartCurrentRuleResponse(**common)
    return AbsoluteLatestCompletionCurrentRuleResponse(**common)


def _constraint_response(value: TemporalConstraintView) -> TemporalConstraintResponse:
    return TemporalConstraintResponse(
        constraint_ref=value.constraint_ref,
        subject_ref=value.subject_native_ref,
        subject_kind=value.subject_kind,
        status=value.status,
        current_rule=_current_rule_response(value),
    )


def _created_response(value: CreatedTemporalConstraintView) -> CreatedTemporalConstraintResponse:
    return CreatedTemporalConstraintResponse(
        constraint_ref=value.constraint_ref,
        subject_ref=value.subject_native_ref,
        subject_kind=value.subject_kind,
        material_state_ref=value.material_state_ref,
        rule=_rule_request(value.rule),
        recorded_at=value.recorded_at,
        replayed=value.replayed,
    )


def _revised_response(value: RevisedTemporalConstraintView) -> RevisedTemporalConstraintResponse:
    return RevisedTemporalConstraintResponse(
        constraint_ref=value.constraint_ref,
        subject_ref=value.subject_native_ref,
        subject_kind=value.subject_kind,
        previous_material_state_ref=value.previous_material_state_ref,
        material_state_ref=value.material_state_ref,
        rule=_rule_request(value.rule),
        recorded_at=value.recorded_at,
        replayed=value.replayed,
    )


def _retired_response(value: RetiredTemporalConstraintView) -> RetiredTemporalConstraintResponse:
    return RetiredTemporalConstraintResponse(
        constraint_ref=value.constraint_ref,
        subject_ref=value.subject_native_ref,
        subject_kind=value.subject_kind,
        previous_material_state_ref=value.previous_material_state_ref,
        recorded_at=value.recorded_at,
        replayed=value.replayed,
    )


def _evaluation_response(value: TemporalConstraintEvaluationView) -> TemporalConstraintEvaluationResponse:
    return TemporalConstraintEvaluationResponse(
        subject_ref=value.subject_native_ref,
        placement=AbsoluteIntervalPlacementRequest(
            starts_at=value.placement.starts_at,
            ends_at=value.placement.ends_at,
        ),
        status=value.status,
        hard_set_status=value.hard_set_status,
        items=[
            TemporalConstraintEvaluationItemResponse(
                constraint_ref=item.constraint_ref,
                material_state_ref=item.material_state_ref,
                family=item.family,
                rule_code=item.rule_code,
                constrained_facet=item.constrained_facet,
                strength=item.strength,
                evaluation=item.evaluation,
                reason_code=item.reason_code,
            )
            for item in value.items
        ],
    )


def _not_found_problem() -> ProblemError:
    return ProblemError(
        status=404,
        code="temporal.constraint.not_found",
        category="not_found",
        title="Temporal Constraint not found",
        detail="No matching Temporal Constraint or subject is available in the current self scope.",
        retryable=False,
    )


def _operation_reuse_problem() -> ProblemError:
    return ProblemError(
        status=409,
        code="temporal.constraint.operation_id_reused",
        category="conflict",
        title="Temporal Constraint operation conflict",
        detail="The operation id was already used for materially different Temporal Constraint intent.",
        retryable=False,
    )


def _state_conflict_problem() -> ProblemError:
    return ProblemError(
        status=409,
        code="temporal.constraint.state_conflict",
        category="conflict",
        title="Temporal Constraint state conflict",
        detail="The Temporal Constraint rule changed after the submitted expected state was read.",
        retryable=False,
    )


def _persistence_problem() -> ProblemError:
    return ProblemError(
        status=503,
        code="temporal.constraint.persistence_unavailable",
        category="service",
        title="Temporal Constraint unavailable",
        detail="The Temporal Constraint operation could not complete safely.",
        retryable=True,
    )


@router.post(
    "/constraints",
    response_model=CreatedTemporalConstraintResponse,
    status_code=201,
    operation_id="temporal_create_constraint",
)
async def create_temporal_constraint(
    payload: CreateTemporalConstraintRequest,
    context: MutatingDanteContextDependency,
    application: TemporalConstraintApplicationDependency,
    response: Response,
) -> CreatedTemporalConstraintResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create_constraint(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            subject_native_ref=NativeRef(payload.subject_ref),
            rule=_rule_from_request(payload.rule),
        )
    except TemporalConstraintInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.constraint.invalid_create",
            category="validation",
            title="Invalid Temporal Constraint",
            detail=str(exc),
            retryable=False,
        ) from exc
    except TemporalConstraintNotFoundError as exc:
        raise _not_found_problem() from exc
    except TemporalConstraintOperationIdReuseError as exc:
        raise _operation_reuse_problem() from exc
    except TemporalConstraintPersistenceError as exc:
        raise _persistence_problem() from exc
    if result.replayed:
        response.status_code = 200
    return _created_response(result)


@router.patch(
    "/constraints/{constraint_ref}/rule",
    response_model=RevisedTemporalConstraintResponse,
    operation_id="temporal_revise_constraint_rule",
)
async def revise_temporal_constraint_rule(
    constraint_ref: UUID,
    payload: ReviseTemporalConstraintRequest,
    context: MutatingDanteContextDependency,
    application: TemporalConstraintApplicationDependency,
    response: Response,
) -> RevisedTemporalConstraintResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.revise_constraint(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            constraint_ref=ScopedRecordRef(constraint_ref),
            expected_material_state_ref=MaterialStateRef(payload.expected_material_state_ref),
            rule=_rule_from_request(payload.rule),
        )
    except TemporalConstraintInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.constraint.invalid_revision",
            category="validation",
            title="Invalid Temporal Constraint revision",
            detail=str(exc),
            retryable=False,
        ) from exc
    except TemporalConstraintNotFoundError as exc:
        raise _not_found_problem() from exc
    except TemporalConstraintOperationIdReuseError as exc:
        raise _operation_reuse_problem() from exc
    except TemporalConstraintStateConflictError as exc:
        raise _state_conflict_problem() from exc
    except TemporalConstraintPersistenceError as exc:
        raise _persistence_problem() from exc
    return _revised_response(result)


@router.post(
    "/constraints/{constraint_ref}/retire",
    response_model=RetiredTemporalConstraintResponse,
    operation_id="temporal_retire_constraint",
)
async def retire_temporal_constraint(
    constraint_ref: UUID,
    payload: RetireTemporalConstraintRequest,
    context: MutatingDanteContextDependency,
    application: TemporalConstraintApplicationDependency,
    response: Response,
) -> RetiredTemporalConstraintResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.retire_constraint(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            constraint_ref=ScopedRecordRef(constraint_ref),
            expected_material_state_ref=MaterialStateRef(payload.expected_material_state_ref),
        )
    except TemporalConstraintInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.constraint.invalid_retirement",
            category="validation",
            title="Invalid Temporal Constraint retirement",
            detail=str(exc),
            retryable=False,
        ) from exc
    except TemporalConstraintNotFoundError as exc:
        raise _not_found_problem() from exc
    except TemporalConstraintOperationIdReuseError as exc:
        raise _operation_reuse_problem() from exc
    except TemporalConstraintStateConflictError as exc:
        raise _state_conflict_problem() from exc
    except TemporalConstraintPersistenceError as exc:
        raise _persistence_problem() from exc
    return _retired_response(result)


@router.post(
    "/constraints/evaluate",
    response_model=TemporalConstraintEvaluationResponse,
    operation_id="temporal_evaluate_constraints",
)
async def evaluate_temporal_constraints(
    payload: EvaluateTemporalConstraintsRequest,
    context: DanteContextDependency,
    application: TemporalConstraintApplicationDependency,
    response: Response,
) -> TemporalConstraintEvaluationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.evaluate_constraints(
            self_person_ref=context.self_person_ref,
            subject_native_ref=NativeRef(payload.subject_ref),
            placement=AbsoluteIntervalPlacement(
                starts_at=payload.placement.starts_at,
                ends_at=payload.placement.ends_at,
            ),
        )
    except TemporalConstraintInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.constraint.invalid_evaluation",
            category="validation",
            title="Invalid Temporal Constraint evaluation",
            detail=str(exc),
            retryable=False,
        ) from exc
    except TemporalConstraintNotFoundError as exc:
        raise _not_found_problem() from exc
    except TemporalConstraintPersistenceError as exc:
        raise _persistence_problem() from exc
    return _evaluation_response(result)


@router.get(
    "/constraints/{constraint_ref}",
    response_model=TemporalConstraintResponse,
    operation_id="temporal_get_constraint",
)
async def get_temporal_constraint(
    constraint_ref: UUID,
    context: DanteContextDependency,
    application: TemporalConstraintApplicationDependency,
    response: Response,
) -> TemporalConstraintResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.get_constraint(
            self_person_ref=context.self_person_ref,
            constraint_ref=ScopedRecordRef(constraint_ref),
        )
    except TemporalConstraintInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.constraint.invalid_reference",
            category="validation",
            title="Invalid Temporal Constraint reference",
            detail=str(exc),
            retryable=False,
        ) from exc
    except TemporalConstraintNotFoundError as exc:
        raise _not_found_problem() from exc
    except TemporalConstraintPersistenceError as exc:
        raise _persistence_problem() from exc
    return _constraint_response(result)


@router.get(
    "/constraints",
    response_model=TemporalConstraintListResponse,
    operation_id="temporal_list_constraints_by_subject",
)
async def list_temporal_constraints_by_subject(
    context: DanteContextDependency,
    application: TemporalConstraintApplicationDependency,
    response: Response,
    subject_ref: UUID = Query(...),
) -> TemporalConstraintListResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        results = await application.list_constraints_by_subject(
            self_person_ref=context.self_person_ref,
            subject_native_ref=NativeRef(subject_ref),
        )
    except TemporalConstraintInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.constraint.invalid_subject_reference",
            category="validation",
            title="Invalid Temporal Constraint subject reference",
            detail=str(exc),
            retryable=False,
        ) from exc
    except TemporalConstraintNotFoundError as exc:
        raise _not_found_problem() from exc
    except TemporalConstraintPersistenceError as exc:
        raise _persistence_problem() from exc
    return TemporalConstraintListResponse(items=[_constraint_response(value) for value in results])
