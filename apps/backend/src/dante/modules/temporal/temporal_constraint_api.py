"""Authenticated B04-A API for canonical Temporal Constraint authoring and reads."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import (
    require_dante_context,
    require_mutating_dante_context,
)
from dante.modules.temporal.temporal_constraint import (
    AbsoluteEarliestStartRule,
    CreatedTemporalConstraintView,
    RevisedTemporalConstraintView,
    RetiredTemporalConstraintView,
    TemporalConstraintApplication,
    TemporalConstraintInputError,
    TemporalConstraintNotFoundError,
    TemporalConstraintOperationIdReuseError,
    TemporalConstraintPersistenceError,
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
    """First public typed Temporal Constraint rule activated by B04-A."""

    model_config = ConfigDict(extra="forbid")

    family: Literal["boundary"] = "boundary"
    boundary_kind: Literal["earliest_start"] = "earliest_start"
    constrained_facet: Literal["schedule.start"] = "schedule.start"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    boundary_at: datetime


class CreateTemporalConstraintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    subject_ref: UUID
    rule: AbsoluteEarliestStartRuleRequest


class ReviseTemporalConstraintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID
    rule: AbsoluteEarliestStartRuleRequest


class RetireTemporalConstraintRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID


class TemporalConstraintCurrentRuleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    material_state_ref: UUID
    family: Literal["boundary"] = "boundary"
    boundary_kind: Literal["earliest_start"] = "earliest_start"
    constrained_facet: Literal["schedule.start"] = "schedule.start"
    strength: Literal["hard", "soft"]
    temporal_form: Literal["absolute"] = "absolute"
    boundary_at: datetime


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
    rule: AbsoluteEarliestStartRuleRequest
    recorded_at: datetime
    replayed: bool = False


class RevisedTemporalConstraintResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constraint_ref: UUID
    subject_ref: UUID
    subject_kind: Literal["activity", "event"]
    previous_material_state_ref: UUID
    material_state_ref: UUID
    rule: AbsoluteEarliestStartRuleRequest
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


def get_temporal_constraint_application(request: Request) -> TemporalConstraintApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalConstraintApplication(database_runtime.session_factory)


TemporalConstraintApplicationDependency = Annotated[
    TemporalConstraintApplication,
    Depends(get_temporal_constraint_application),
]


def _rule_from_request(payload: AbsoluteEarliestStartRuleRequest) -> AbsoluteEarliestStartRule:
    return AbsoluteEarliestStartRule(
        strength=payload.strength,
        boundary_at=payload.boundary_at,
    )


def _rule_request(rule: AbsoluteEarliestStartRule) -> AbsoluteEarliestStartRuleRequest:
    return AbsoluteEarliestStartRuleRequest(
        strength=rule.strength,
        boundary_at=rule.boundary_at,
    )


def _constraint_response(value: TemporalConstraintView) -> TemporalConstraintResponse:
    current_rule = value.current_rule
    return TemporalConstraintResponse(
        constraint_ref=value.constraint_ref,
        subject_ref=value.subject_native_ref,
        subject_kind=value.subject_kind,
        status=value.status,
        current_rule=(
            None
            if current_rule is None
            else TemporalConstraintCurrentRuleResponse(
                material_state_ref=current_rule.material_state_ref,
                strength=current_rule.strength,
                boundary_at=current_rule.boundary_at,
            )
        ),
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
            expected_material_state_ref=MaterialStateRef(
                payload.expected_material_state_ref
            ),
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
            expected_material_state_ref=MaterialStateRef(
                payload.expected_material_state_ref
            ),
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
    return TemporalConstraintListResponse(
        items=[_constraint_response(value) for value in results]
    )
