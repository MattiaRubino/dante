"""B10-D HTTP surface for Outcome-owner reconciliation authoring and reads."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.reconciliation_runtime import (
    ReconciliationApplication,
    ReconciliationCurrentConflictError,
    ReconciliationEvidence,
    ReconciliationInputError,
    ReconciliationNotFoundError,
    ReconciliationOperationReuseError,
    ReconciliationPersistenceError,
    ReconciliationView,
)
from dante.platform.database.references import MaterialStateRef, ScopedRecordRef
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class ReconciliationEvidenceCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmation_ref: UUID = Field(strict=False)
    confirmation_attestation_material_state_ref: UUID = Field(strict=False)
    role_code: Literal["considered", "selected"]


class ReconciliationCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    outcome_disposition_material_state_ref: UUID = Field(strict=False)
    expected_material_state_ref: UUID | None = Field(default=None, strict=False)
    purpose_code: str = Field(min_length=1, max_length=120)
    action_code: Literal["unresolved", "select", "accept_multiple", "defer", "escalate"]
    evidence: list[ReconciliationEvidenceCommand] = Field(default_factory=list)


class ReconciliationEvidenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    confirmation_ref: UUID
    confirmation_attestation_material_state_ref: UUID
    role_code: Literal["considered", "selected"]


class ReconciliationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reconciliation_ref: UUID
    outcome_ref: UUID
    outcome_disposition_material_state_ref: UUID
    purpose_code: str
    material_state_ref: UUID
    action_code: Literal["unresolved", "select", "accept_multiple", "defer", "escalate"]
    resolved_by_person_ref: UUID
    evidence: list[ReconciliationEvidenceResponse]
    replayed: bool


class ReconciliationHistoryResponse(ReconciliationResponse):
    current_from_at: datetime
    current_until_at: datetime | None


_RECONCILIATION_WRITE_RESPONSES = {
    200: {
        "model": ReconciliationResponse,
        "description": "Idempotent replay of the already accepted reconciliation command.",
    },
    400: {"model": ProblemDetails, "description": "Malformed request."},
    401: {"model": ProblemDetails, "description": "Authentication required."},
    403: {"model": ProblemDetails, "description": "Mutation request rejected by security policy."},
    404: {"model": ProblemDetails, "description": "Outcome target unavailable."},
    409: {"model": ProblemDetails, "description": "Operation reuse, stale current state, or persistence conflict."},
    422: {"model": ProblemDetails, "description": "Reconciliation payload rejected."},
    500: {"model": ProblemDetails, "description": "Unexpected server error."},
}


def _application(request: Request) -> ReconciliationApplication:
    return ReconciliationApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[ReconciliationApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: ReconciliationView) -> ReconciliationResponse:
    return ReconciliationResponse(
        reconciliation_ref=view.reconciliation_ref,
        outcome_ref=view.outcome_ref,
        outcome_disposition_material_state_ref=view.outcome_disposition_material_state_ref,
        purpose_code=view.purpose_code,
        material_state_ref=view.material_state_ref,
        action_code=view.action_code,
        resolved_by_person_ref=view.resolved_by_person_ref,
        evidence=[
            ReconciliationEvidenceResponse(
                confirmation_ref=item.confirmation_ref,
                confirmation_attestation_material_state_ref=(
                    item.confirmation_attestation_material_state_ref
                ),
                role_code=item.role_code,
            )
            for item in view.evidence
        ],
        replayed=view.replayed,
    )


def _history_response(view: ReconciliationView) -> ReconciliationHistoryResponse:
    if view.current_from_at is None:
        raise ReconciliationPersistenceError(
            "Reconciliation current-history chronology is unavailable."
        )
    response = _response(view)
    return ReconciliationHistoryResponse(
        **response.model_dump(),
        current_from_at=view.current_from_at,
        current_until_at=view.current_until_at,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ReconciliationInputError):
        return ProblemError(
            status=422,
            code="temporal.reconciliation.invalid_input",
            category="validation",
            title="Reconciliation rejected",
            detail=str(exc),
        )
    if isinstance(exc, ReconciliationNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.reconciliation.not_found",
            category="not_found",
            title="Reconciliation unavailable",
            detail=str(exc),
        )
    if isinstance(exc, ReconciliationOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.reconciliation.operation_id_reused",
            category="conflict",
            title="Reconciliation operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, ReconciliationCurrentConflictError):
        return ProblemError(
            status=409,
            code="temporal.reconciliation.current_conflict",
            category="conflict",
            title="Reconciliation changed",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.reconciliation.persistence",
        category="conflict",
        title="Reconciliation rejected",
        detail="Reconciliation command was rejected.",
    )


@router.post(
    "/outcomes/{outcome_ref}/reconciliations",
    response_model=ReconciliationResponse,
    status_code=201,
    responses=_RECONCILIATION_WRITE_RESPONSES,
    operation_id="temporal_record_outcome_reconciliation",
)
async def record_outcome_reconciliation(
    outcome_ref: UUID,
    payload: ReconciliationCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ReconciliationResponse:
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
            action_code=payload.action_code,
            evidence=tuple(
                ReconciliationEvidence(
                    confirmation_ref=ScopedRecordRef(item.confirmation_ref),
                    confirmation_attestation_material_state_ref=MaterialStateRef(
                        item.confirmation_attestation_material_state_ref
                    ),
                    role_code=item.role_code,
                )
                for item in payload.evidence
            ),
        )
    except (
        ReconciliationInputError,
        ReconciliationNotFoundError,
        ReconciliationOperationReuseError,
        ReconciliationCurrentConflictError,
        ReconciliationPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


@router.get(
    "/outcomes/{outcome_ref}/reconciliations",
    response_model=list[ReconciliationResponse],
    responses={404: {"model": ProblemDetails, "description": "Outcome unavailable."}},
    operation_id="temporal_list_outcome_reconciliations",
)
async def list_outcome_reconciliations(
    outcome_ref: UUID,
    context: Context,
    application: Application,
) -> list[ReconciliationResponse]:
    try:
        views = await application.list_for_outcome(
            self_person_ref=context.self_person_ref,
            outcome_ref=ScopedRecordRef(outcome_ref),
        )
    except (ReconciliationInputError, ReconciliationPersistenceError) as exc:
        raise _problem(exc) from exc
    if views is None:
        raise _problem(
            ReconciliationNotFoundError(
                "Reconciliation Outcome is not in the authenticated owner scope."
            )
        )
    return [_response(view) for view in views]


@router.get(
    "/reconciliations/{reconciliation_ref}/history",
    response_model=list[ReconciliationHistoryResponse],
    responses={404: {"model": ProblemDetails, "description": "Reconciliation unavailable."}},
    operation_id="temporal_list_outcome_reconciliation_history",
)
async def list_outcome_reconciliation_history(
    reconciliation_ref: UUID,
    context: Context,
    application: Application,
) -> list[ReconciliationHistoryResponse]:
    try:
        views = await application.history(
            self_person_ref=context.self_person_ref,
            reconciliation_ref=ScopedRecordRef(reconciliation_ref),
        )
    except (ReconciliationNotFoundError, ReconciliationPersistenceError) as exc:
        raise _problem(exc) from exc
    return [_history_response(view) for view in views]
