"""B10-C HTTP surface for explicit contextual Confirmation authoring and reads."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.confirmation_runtime import (
    ConfirmationApplication,
    ConfirmationCurrentConflictError,
    ConfirmationInputError,
    ConfirmationNotFoundError,
    ConfirmationOperationReuseError,
    ConfirmationPersistenceError,
    ConfirmationView,
)
from dante.platform.database.references import MaterialStateRef, ScopedRecordRef
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class ConfirmationCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    outcome_disposition_material_state_ref: UUID = Field(strict=False)
    expected_material_state_ref: UUID | None = Field(default=None, strict=False)
    purpose_code: str = Field(min_length=1, max_length=120)
    stance_code: str = Field(min_length=1, max_length=120)


class ConfirmationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmation_ref: UUID
    outcome_ref: UUID
    outcome_disposition_material_state_ref: UUID
    confirmer_person_ref: UUID
    purpose_code: str
    material_state_ref: UUID
    stance_code: str
    confirmer_is_self: bool
    replayed: bool


class ConfirmationHistoryResponse(ConfirmationResponse):
    current_from_at: datetime
    current_until_at: datetime | None


_CONFIRMATION_WRITE_RESPONSES = {
    200: {
        "model": ConfirmationResponse,
        "description": "Idempotent replay of the already accepted Confirmation command.",
    },
    400: {"model": ProblemDetails, "description": "Malformed request."},
    401: {"model": ProblemDetails, "description": "Authentication required."},
    403: {"model": ProblemDetails, "description": "Mutation request rejected by security policy."},
    404: {"model": ProblemDetails, "description": "Outcome target unavailable."},
    409: {"model": ProblemDetails, "description": "Operation reuse, stale current state, or persistence conflict."},
    422: {"model": ProblemDetails, "description": "Confirmation payload rejected."},
    500: {"model": ProblemDetails, "description": "Unexpected server error."},
}


def _application(request: Request) -> ConfirmationApplication:
    return ConfirmationApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[ConfirmationApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: ConfirmationView) -> ConfirmationResponse:
    return ConfirmationResponse(
        confirmation_ref=view.confirmation_ref,
        outcome_ref=view.outcome_ref,
        outcome_disposition_material_state_ref=view.outcome_disposition_material_state_ref,
        confirmer_person_ref=view.confirmer_person_ref,
        purpose_code=view.purpose_code,
        material_state_ref=view.material_state_ref,
        stance_code=view.stance_code,
        confirmer_is_self=view.confirmer_is_self,
        replayed=view.replayed,
    )


def _history_response(view: ConfirmationView) -> ConfirmationHistoryResponse:
    if view.current_from_at is None:
        raise ConfirmationPersistenceError("Confirmation current-history chronology is unavailable.")
    response = _response(view)
    return ConfirmationHistoryResponse(
        **response.model_dump(),
        current_from_at=view.current_from_at,
        current_until_at=view.current_until_at,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ConfirmationInputError):
        return ProblemError(
            status=422,
            code="temporal.confirmation.invalid_input",
            category="validation",
            title="Confirmation rejected",
            detail=str(exc),
        )
    if isinstance(exc, ConfirmationNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.confirmation.not_found",
            category="not_found",
            title="Confirmation unavailable",
            detail=str(exc),
        )
    if isinstance(exc, ConfirmationOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.confirmation.operation_id_reused",
            category="conflict",
            title="Confirmation operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, ConfirmationCurrentConflictError):
        return ProblemError(
            status=409,
            code="temporal.confirmation.current_conflict",
            category="conflict",
            title="Confirmation changed",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.confirmation.persistence",
        category="conflict",
        title="Confirmation rejected",
        detail="Confirmation command was rejected.",
    )


@router.post(
    "/outcomes/{outcome_ref}/confirmations",
    response_model=ConfirmationResponse,
    status_code=201,
    responses=_CONFIRMATION_WRITE_RESPONSES,
    operation_id="temporal_record_outcome_confirmation",
)
async def record_outcome_confirmation(
    outcome_ref: UUID,
    payload: ConfirmationCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ConfirmationResponse:
    try:
        view = await application.record(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            outcome_ref=ScopedRecordRef(outcome_ref),
            outcome_disposition_material_state_ref=MaterialStateRef(
                payload.outcome_disposition_material_state_ref
            ),
            expected_material_state_ref=(
                MaterialStateRef(payload.expected_material_state_ref)
                if payload.expected_material_state_ref is not None
                else None
            ),
            purpose_code=payload.purpose_code,
            stance_code=payload.stance_code,
        )
    except (
        ConfirmationInputError,
        ConfirmationNotFoundError,
        ConfirmationOperationReuseError,
        ConfirmationCurrentConflictError,
        ConfirmationPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


@router.get(
    "/outcomes/{outcome_ref}/confirmations",
    response_model=list[ConfirmationResponse],
    operation_id="temporal_list_outcome_confirmations",
)
async def list_outcome_confirmations(
    outcome_ref: UUID,
    context: Context,
    application: Application,
) -> list[ConfirmationResponse]:
    try:
        views = await application.list_for_outcome(
            self_person_ref=context.self_person_ref,
            outcome_ref=ScopedRecordRef(outcome_ref),
        )
    except (ConfirmationInputError, ConfirmationNotFoundError, ConfirmationPersistenceError) as exc:
        raise _problem(exc) from exc
    if views is None:
        raise _problem(ConfirmationNotFoundError("Confirmation Outcome is not in the authenticated self scope."))
    return [_response(view) for view in views]


@router.get(
    "/confirmations/{confirmation_ref}/history",
    response_model=list[ConfirmationHistoryResponse],
    operation_id="temporal_list_confirmation_history",
)
async def list_confirmation_history(
    confirmation_ref: UUID,
    context: Context,
    application: Application,
) -> list[ConfirmationHistoryResponse]:
    try:
        views = await application.history(
            self_person_ref=context.self_person_ref,
            confirmation_ref=ScopedRecordRef(confirmation_ref),
        )
    except (ConfirmationNotFoundError, ConfirmationPersistenceError) as exc:
        raise _problem(exc) from exc
    return [_history_response(view) for view in views]
