"""B10-B HTTP surface for explicit contextual Outcome disposition authoring and reads."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.outcome_runtime import (
    OutcomeApplication,
    OutcomeCurrentConflictError,
    OutcomeInputError,
    OutcomeNotFoundError,
    OutcomeOperationReuseError,
    OutcomePersistenceError,
    OutcomeView,
)
from dante.platform.database.references import MaterialStateRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class OutcomeCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    actual_realization_material_state_ref: UUID = Field(strict=False)
    expected_material_state_ref: UUID | None = Field(default=None, strict=False)
    disposition_code: str = Field(min_length=1, max_length=120)


class OutcomeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    outcome_ref: UUID
    actual_ref: UUID
    actual_realization_material_state_ref: UUID
    material_state_ref: UUID
    disposition_code: str
    replayed: bool


class OutcomeHistoryResponse(OutcomeResponse):
    current_from_at: datetime
    current_until_at: datetime | None


def _application(request: Request) -> OutcomeApplication:
    return OutcomeApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[OutcomeApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: OutcomeView) -> OutcomeResponse:
    return OutcomeResponse(
        outcome_ref=view.outcome_ref,
        actual_ref=view.actual_ref,
        actual_realization_material_state_ref=view.actual_realization_material_state_ref,
        material_state_ref=view.material_state_ref,
        disposition_code=view.disposition_code,
        replayed=view.replayed,
    )


def _history_response(view: OutcomeView) -> OutcomeHistoryResponse:
    if view.current_from_at is None:
        raise OutcomePersistenceError("Outcome current-history chronology is unavailable.")
    response = _response(view)
    return OutcomeHistoryResponse(
        **response.model_dump(),
        current_from_at=view.current_from_at,
        current_until_at=view.current_until_at,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, OutcomeInputError):
        return ProblemError(
            status=422,
            code="temporal.outcome.invalid_input",
            category="validation",
            title="Outcome rejected",
            detail=str(exc),
        )
    if isinstance(exc, OutcomeNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.outcome.not_found",
            category="not_found",
            title="Outcome unavailable",
            detail=str(exc),
        )
    if isinstance(exc, OutcomeOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.outcome.operation_id_reused",
            category="conflict",
            title="Outcome operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, OutcomeCurrentConflictError):
        return ProblemError(
            status=409,
            code="temporal.outcome.current_conflict",
            category="conflict",
            title="Outcome changed",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.outcome.persistence",
        category="conflict",
        title="Outcome rejected",
        detail="Outcome command was rejected.",
    )


@router.post(
    "/actuals/{actual_ref}/outcome",
    response_model=OutcomeResponse,
    operation_id="temporal_record_actual_outcome",
)
async def record_actual_outcome(
    actual_ref: UUID,
    payload: OutcomeCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> OutcomeResponse:
    try:
        view = await application.record(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            actual_ref=ScopedRecordRef(actual_ref),
            actual_realization_material_state_ref=MaterialStateRef(
                payload.actual_realization_material_state_ref
            ),
            expected_material_state_ref=(
                MaterialStateRef(payload.expected_material_state_ref)
                if payload.expected_material_state_ref is not None
                else None
            ),
            disposition_code=payload.disposition_code,
        )
    except (
        OutcomeInputError,
        OutcomeNotFoundError,
        OutcomeOperationReuseError,
        OutcomeCurrentConflictError,
        OutcomePersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


@router.get(
    "/actuals/{actual_ref}/outcome",
    response_model=OutcomeResponse,
    operation_id="temporal_get_actual_outcome",
)
async def get_actual_outcome(
    actual_ref: UUID,
    context: Context,
    application: Application,
) -> OutcomeResponse:
    try:
        view = await application.get_for_actual(
            self_person_ref=context.self_person_ref,
            actual_ref=ScopedRecordRef(actual_ref),
        )
    except (OutcomeInputError, OutcomeNotFoundError, OutcomePersistenceError) as exc:
        raise _problem(exc) from exc
    return _response(view)


@router.get(
    "/outcomes/{outcome_ref}/history",
    response_model=list[OutcomeHistoryResponse],
    operation_id="temporal_list_outcome_history",
)
async def list_outcome_history(
    outcome_ref: UUID,
    context: Context,
    application: Application,
) -> list[OutcomeHistoryResponse]:
    try:
        views = await application.history(
            self_person_ref=context.self_person_ref,
            outcome_ref=ScopedRecordRef(outcome_ref),
        )
    except (OutcomeNotFoundError, OutcomePersistenceError) as exc:
        raise _problem(exc) from exc
    return [_history_response(view) for view in views]
