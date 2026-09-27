"""B11-B HTTP surface for bounded Actual-realization conditional intent."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.conditional_temporal import (
    ActualRealizationConditionView,
    ConditionalEvaluationView,
    ConditionalTemporalApplication,
    ConditionalTemporalInputError,
    ConditionalTemporalNotFoundError,
    ConditionalTemporalOperationReuseError,
    ConditionalTemporalPersistenceError,
)
from dante.platform.database.references import NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class ActualRealizationConditionRequest(BaseModel):
    """Create one bounded condition over canonical Actual realization truth."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    subject_kind: Literal["activity", "event", "occurrence"]
    subject_native_ref: UUID = Field(strict=False)


class ActualRealizationConditionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    condition_ref: UUID
    subject_kind: Literal["activity", "event", "occurrence"]
    subject_native_ref: UUID
    family_code: Literal["actual_realization"]
    created_at: datetime
    replayed: bool


class ConditionalEvaluationRequest(BaseModel):
    """Evaluate from PostgreSQL truth; callers never provide the result."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)


class ConditionalEvaluationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evaluation_ref: UUID
    condition_ref: UUID
    result_code: Literal["satisfied", "not_satisfied", "indeterminate"]
    disposition_code: Literal["allow", "withhold"]
    actual_ref: UUID | None
    actual_realization_material_state_ref: UUID | None
    evaluated_at: datetime
    replayed: bool


_CONDITION_WRITE_RESPONSES = {
    200: {
        "model": ActualRealizationConditionResponse,
        "description": "Idempotent replay.",
    },
    400: {"model": ProblemDetails, "description": "Malformed request."},
    401: {"model": ProblemDetails, "description": "Authentication required."},
    403: {"model": ProblemDetails, "description": "Mutation rejected by security policy."},
    404: {"model": ProblemDetails, "description": "Conditional subject unavailable."},
    409: {"model": ProblemDetails, "description": "Operation id reuse conflict."},
    422: {"model": ProblemDetails, "description": "Conditional payload rejected."},
    500: {"model": ProblemDetails, "description": "Unexpected server error."},
}

_EVALUATION_WRITE_RESPONSES = {
    200: {
        "model": ConditionalEvaluationResponse,
        "description": "Idempotent replay.",
    },
    400: {"model": ProblemDetails, "description": "Malformed request."},
    401: {"model": ProblemDetails, "description": "Authentication required."},
    403: {"model": ProblemDetails, "description": "Mutation rejected by security policy."},
    404: {"model": ProblemDetails, "description": "Conditional intent unavailable."},
    409: {"model": ProblemDetails, "description": "Operation id reuse conflict."},
    422: {"model": ProblemDetails, "description": "Conditional evaluation rejected."},
    500: {"model": ProblemDetails, "description": "Unexpected server error."},
}


def _application(request: Request) -> ConditionalTemporalApplication:
    return ConditionalTemporalApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[ConditionalTemporalApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ConditionalTemporalInputError):
        return ProblemError(
            status=422,
            code="temporal.conditional.invalid_input",
            category="validation",
            title="Conditional temporal intent rejected",
            detail=str(exc),
        )
    if isinstance(exc, ConditionalTemporalNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.conditional.not_found",
            category="not_found",
            title="Conditional temporal intent unavailable",
            detail=str(exc),
        )
    if isinstance(exc, ConditionalTemporalOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.conditional.operation_id_reused",
            category="conflict",
            title="Conditional temporal operation id reused",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.conditional.persistence",
        category="conflict",
        title="Conditional temporal command rejected",
        detail="Conditional temporal command was rejected.",
    )


def _condition_response(
    view: ActualRealizationConditionView,
) -> ActualRealizationConditionResponse:
    return ActualRealizationConditionResponse(
        condition_ref=view.condition_ref,
        subject_kind=view.subject_kind,
        subject_native_ref=view.subject_native_ref,
        family_code=view.family_code,
        created_at=view.created_at,
        replayed=view.replayed,
    )


def _evaluation_response(view: ConditionalEvaluationView) -> ConditionalEvaluationResponse:
    return ConditionalEvaluationResponse(
        evaluation_ref=view.evaluation_ref,
        condition_ref=view.condition_ref,
        result_code=view.result_code,
        disposition_code=view.disposition_code,
        actual_ref=view.actual_ref,
        actual_realization_material_state_ref=view.actual_realization_material_state_ref,
        evaluated_at=view.evaluated_at,
        replayed=view.replayed,
    )


@router.post(
    "/conditions/actual-realization",
    response_model=ActualRealizationConditionResponse,
    status_code=201,
    responses=_CONDITION_WRITE_RESPONSES,
    operation_id="temporal_create_actual_realization_condition",
)
async def create_actual_realization_condition(
    payload: ActualRealizationConditionRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ActualRealizationConditionResponse:
    try:
        view = await application.create_actual_realization_condition(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            subject_kind=payload.subject_kind,
            subject_native_ref=NativeRef(payload.subject_native_ref),
        )
    except (
        ConditionalTemporalInputError,
        ConditionalTemporalNotFoundError,
        ConditionalTemporalOperationReuseError,
        ConditionalTemporalPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _condition_response(view)


@router.get(
    "/conditions/actual-realization",
    response_model=ActualRealizationConditionResponse,
    responses={
        401: {"model": ProblemDetails, "description": "Authentication required."},
        404: {"model": ProblemDetails, "description": "Conditional intent unavailable."},
    },
    operation_id="temporal_find_actual_realization_condition",
)
async def find_actual_realization_condition(
    subject_kind: Literal["activity", "event", "occurrence"],
    subject_native_ref: UUID,
    context: Context,
    application: Application,
) -> ActualRealizationConditionResponse:
    try:
        view = await application.find_actual_realization_condition(
            self_person_ref=context.self_person_ref,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_native_ref),
        )
    except (
        ConditionalTemporalInputError,
        ConditionalTemporalNotFoundError,
        ConditionalTemporalPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    if view is None:
        raise _problem(
            ConditionalTemporalNotFoundError("Conditional temporal intent unavailable.")
        )
    return _condition_response(view)


@router.get(
    "/conditions/actual-realization/{condition_ref}",
    response_model=ActualRealizationConditionResponse,
    responses={
        401: {"model": ProblemDetails, "description": "Authentication required."},
        404: {"model": ProblemDetails, "description": "Conditional intent unavailable."},
    },
    operation_id="temporal_get_actual_realization_condition",
)
async def get_actual_realization_condition(
    condition_ref: UUID,
    context: Context,
    application: Application,
) -> ActualRealizationConditionResponse:
    try:
        view = await application.get_actual_realization_condition(
            self_person_ref=context.self_person_ref,
            condition_ref=ScopedRecordRef(condition_ref),
        )
    except (
        ConditionalTemporalNotFoundError,
        ConditionalTemporalPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    if view is None:
        raise _problem(
            ConditionalTemporalNotFoundError("Conditional temporal intent unavailable.")
        )
    return _condition_response(view)


@router.post(
    "/conditions/actual-realization/{condition_ref}/evaluations",
    response_model=ConditionalEvaluationResponse,
    status_code=201,
    responses=_EVALUATION_WRITE_RESPONSES,
    operation_id="temporal_evaluate_actual_realization_condition",
)
async def evaluate_actual_realization_condition(
    condition_ref: UUID,
    payload: ConditionalEvaluationRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ConditionalEvaluationResponse:
    try:
        view = await application.evaluate_actual_realization_condition(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            condition_ref=ScopedRecordRef(condition_ref),
        )
    except (
        ConditionalTemporalInputError,
        ConditionalTemporalNotFoundError,
        ConditionalTemporalOperationReuseError,
        ConditionalTemporalPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _evaluation_response(view)
