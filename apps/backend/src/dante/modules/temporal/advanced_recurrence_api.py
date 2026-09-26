"""B11-A HTTP surface for completion/anchor-stream relative Recurrence."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.advanced_recurrence import (
    AdvancedCheckpointResult,
    AdvancedElapsedRecurrence,
    AdvancedRecurrenceApplication,
    AdvancedRecurrenceInputError,
    AdvancedRecurrenceMutation,
    AdvancedRecurrenceOperationReuseError,
    AdvancedRecurrencePersistenceError,
    AdvancedRecurrenceStateConflictError,
    AdvancedRecurrenceUnavailableError,
    AdvancedRecurrenceView,
)
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class AdvancedElapsedRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID = Field(strict=False)
    range_kind: Literal["open", "until_boundary", "expected_count"] = "open"
    expected_occurrence_count: int | None = Field(default=None, ge=1)
    effective_from: datetime
    effective_until: datetime | None = None
    elapsed_seconds: Decimal = Field(gt=0)
    anchor_mode_code: Literal["previous_completion", "anchor_stream"]
    anchor_source_family: Literal["routine", "event"] | None = None
    anchor_source_native_ref: UUID | None = Field(default=None, strict=False)


class AdvancedRecurrenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    owner_kind: Literal["routine", "event"]
    source_ref: UUID
    material_state_ref: UUID
    range_kind: Literal["open", "until_boundary", "expected_count"]
    expected_occurrence_count: int | None
    effective_from: datetime
    effective_until: datetime | None
    elapsed_seconds: Decimal
    anchor_mode_code: Literal["previous_completion", "anchor_stream"]
    anchor_source_family: Literal["routine", "event"] | None
    anchor_source_native_ref: UUID | None
    replayed: bool


class AdvancedCheckpointRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    governing_recurrence_state_ref: UUID = Field(strict=False)
    start_at: datetime
    end_at_exclusive: datetime


class AdvancedOccurrenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    occurrence_ref: UUID
    expected_at: datetime
    anchor_occurrence_ref: UUID
    anchor_actual_ref: UUID
    anchor_actual_material_state_ref: UUID
    anchor_completed_at: datetime
    created: bool


class AdvancedCheckpointResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    owner_kind: Literal["routine", "event"]
    source_ref: UUID
    governing_recurrence_state_ref: UUID
    accepted_at: datetime
    occurrences: list[AdvancedOccurrenceResponse]
    replayed: bool


_WRITE_RESPONSES = {
    200: {"model": AdvancedRecurrenceResponse, "description": "Idempotent replay."},
    400: {"model": ProblemDetails, "description": "Malformed request."},
    401: {"model": ProblemDetails, "description": "Authentication required."},
    403: {"model": ProblemDetails, "description": "Mutation rejected by security policy."},
    404: {"model": ProblemDetails, "description": "Source or anchor stream unavailable."},
    409: {"model": ProblemDetails, "description": "Operation reuse or stale current state."},
    422: {"model": ProblemDetails, "description": "Advanced Recurrence payload rejected."},
    500: {"model": ProblemDetails, "description": "Unexpected server error."},
}


def _application(request: Request) -> AdvancedRecurrenceApplication:
    return AdvancedRecurrenceApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[AdvancedRecurrenceApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, AdvancedRecurrenceInputError):
        return ProblemError(
            status=422,
            code="temporal.advanced_recurrence.invalid_input",
            category="validation",
            title="Advanced Recurrence rejected",
            detail=str(exc),
        )
    if isinstance(exc, AdvancedRecurrenceUnavailableError):
        return ProblemError(
            status=404,
            code="temporal.advanced_recurrence.unavailable",
            category="not_found",
            title="Advanced Recurrence unavailable",
            detail=str(exc),
        )
    if isinstance(exc, AdvancedRecurrenceOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.advanced_recurrence.operation_id_reused",
            category="conflict",
            title="Advanced Recurrence operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, AdvancedRecurrenceStateConflictError):
        return ProblemError(
            status=409,
            code="temporal.advanced_recurrence.current_conflict",
            category="conflict",
            title="Advanced Recurrence changed",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.advanced_recurrence.persistence",
        category="conflict",
        title="Advanced Recurrence rejected",
        detail="Advanced Recurrence command was rejected.",
    )


def _response(view: AdvancedRecurrenceView, *, replayed: bool) -> AdvancedRecurrenceResponse:
    spec = view.recurrence
    return AdvancedRecurrenceResponse(
        owner_kind=view.owner_kind,
        source_ref=view.source_ref,
        material_state_ref=view.material_state_ref,
        range_kind=spec.range_kind,
        expected_occurrence_count=spec.expected_occurrence_count,
        effective_from=spec.effective_from,
        effective_until=spec.effective_until,
        elapsed_seconds=spec.elapsed_seconds,
        anchor_mode_code=spec.anchor_mode_code,
        anchor_source_family=spec.anchor_source_family,
        anchor_source_native_ref=spec.anchor_source_native_ref,
        replayed=replayed,
    )


def _checkpoint_response(result: AdvancedCheckpointResult) -> AdvancedCheckpointResponse:
    return AdvancedCheckpointResponse(
        owner_kind=result.owner_kind,
        source_ref=result.source_ref,
        governing_recurrence_state_ref=result.governing_recurrence_state_ref,
        accepted_at=result.accepted_at,
        occurrences=[
            AdvancedOccurrenceResponse(
                occurrence_ref=item.occurrence_ref,
                expected_at=item.expected_at,
                anchor_occurrence_ref=item.anchor_occurrence_ref,
                anchor_actual_ref=item.anchor_actual_ref,
                anchor_actual_material_state_ref=item.anchor_actual_material_state_ref,
                anchor_completed_at=item.anchor_completed_at,
                created=item.created,
            )
            for item in result.occurrences
        ],
        replayed=result.replayed,
    )


async def _get(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    context: DanteContext,
    application: AdvancedRecurrenceApplication,
) -> AdvancedRecurrenceResponse:
    try:
        view = await application.get(
            owner=owner,
            self_person_ref=context.self_person_ref,
            source_ref=source_ref,
        )
    except (
        AdvancedRecurrenceUnavailableError,
        AdvancedRecurrencePersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    if view is None:
        raise _problem(
            AdvancedRecurrenceUnavailableError(
                "Current Recurrence is not a B11-A dynamic elapsed Recurrence."
            )
        )
    return _response(view, replayed=False)


async def _replace(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    payload: AdvancedElapsedRecurrenceRequest,
    context: DanteContext,
    application: AdvancedRecurrenceApplication,
    response: Response,
) -> AdvancedRecurrenceResponse:
    try:
        mutation: AdvancedRecurrenceMutation = await application.replace(
            owner=owner,
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            source_ref=source_ref,
            expected_material_state_ref=payload.expected_material_state_ref,
            recurrence=AdvancedElapsedRecurrence(
                range_kind=payload.range_kind,
                expected_occurrence_count=payload.expected_occurrence_count,
                effective_from=payload.effective_from,
                effective_until=payload.effective_until,
                elapsed_seconds=payload.elapsed_seconds,
                anchor_mode_code=payload.anchor_mode_code,
                anchor_source_family=payload.anchor_source_family,
                anchor_source_native_ref=payload.anchor_source_native_ref,
            ),
        )
    except (
        AdvancedRecurrenceInputError,
        AdvancedRecurrenceUnavailableError,
        AdvancedRecurrenceOperationReuseError,
        AdvancedRecurrenceStateConflictError,
        AdvancedRecurrencePersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if mutation.replayed else 201
    return _response(mutation.recurrence, replayed=mutation.replayed)


async def _checkpoint(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    payload: AdvancedCheckpointRequest,
    context: DanteContext,
    application: AdvancedRecurrenceApplication,
    response: Response,
) -> AdvancedCheckpointResponse:
    try:
        result = await application.checkpoint(
            owner=owner,
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            source_ref=source_ref,
            governing_recurrence_state_ref=payload.governing_recurrence_state_ref,
            start_at=payload.start_at,
            end_at_exclusive=payload.end_at_exclusive,
        )
    except (
        AdvancedRecurrenceInputError,
        AdvancedRecurrenceUnavailableError,
        AdvancedRecurrenceOperationReuseError,
        AdvancedRecurrenceStateConflictError,
        AdvancedRecurrencePersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if result.replayed else 201
    return _checkpoint_response(result)


@router.get(
    "/routines/{source_ref}/advanced-recurrence",
    response_model=AdvancedRecurrenceResponse,
    responses={404: {"model": ProblemDetails, "description": "Advanced Recurrence unavailable."}},
    operation_id="temporal_get_routine_advanced_recurrence",
)
async def get_routine_advanced_recurrence(
    source_ref: UUID, context: Context, application: Application
) -> AdvancedRecurrenceResponse:
    return await _get("routine", source_ref, context, application)


@router.put(
    "/routines/{source_ref}/advanced-recurrence",
    response_model=AdvancedRecurrenceResponse,
    status_code=201,
    responses=_WRITE_RESPONSES,
    operation_id="temporal_replace_routine_advanced_recurrence",
)
async def replace_routine_advanced_recurrence(
    source_ref: UUID,
    payload: AdvancedElapsedRecurrenceRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> AdvancedRecurrenceResponse:
    return await _replace("routine", source_ref, payload, context, application, response)


@router.post(
    "/routines/{source_ref}/advanced-recurrence/checkpoint",
    response_model=AdvancedCheckpointResponse,
    status_code=201,
    responses={**_WRITE_RESPONSES, 200: {"model": AdvancedCheckpointResponse, "description": "Idempotent replay."}},
    operation_id="temporal_checkpoint_routine_advanced_recurrence",
)
async def checkpoint_routine_advanced_recurrence(
    source_ref: UUID,
    payload: AdvancedCheckpointRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> AdvancedCheckpointResponse:
    return await _checkpoint("routine", source_ref, payload, context, application, response)


@router.get(
    "/events/{source_ref}/advanced-recurrence",
    response_model=AdvancedRecurrenceResponse,
    responses={404: {"model": ProblemDetails, "description": "Advanced Recurrence unavailable."}},
    operation_id="temporal_get_event_advanced_recurrence",
)
async def get_event_advanced_recurrence(
    source_ref: UUID, context: Context, application: Application
) -> AdvancedRecurrenceResponse:
    return await _get("event", source_ref, context, application)


@router.put(
    "/events/{source_ref}/advanced-recurrence",
    response_model=AdvancedRecurrenceResponse,
    status_code=201,
    responses=_WRITE_RESPONSES,
    operation_id="temporal_replace_event_advanced_recurrence",
)
async def replace_event_advanced_recurrence(
    source_ref: UUID,
    payload: AdvancedElapsedRecurrenceRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> AdvancedRecurrenceResponse:
    return await _replace("event", source_ref, payload, context, application, response)


@router.post(
    "/events/{source_ref}/advanced-recurrence/checkpoint",
    response_model=AdvancedCheckpointResponse,
    status_code=201,
    responses={**_WRITE_RESPONSES, 200: {"model": AdvancedCheckpointResponse, "description": "Idempotent replay."}},
    operation_id="temporal_checkpoint_event_advanced_recurrence",
)
async def checkpoint_event_advanced_recurrence(
    source_ref: UUID,
    payload: AdvancedCheckpointRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> AdvancedCheckpointResponse:
    return await _checkpoint("event", source_ref, payload, context, application, response)
