"""Self-scoped notices and decisions for renewable open calendar series."""

from dataclasses import asdict
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.open_recurrence_allowance import (
    AllowanceConflictError,
    AllowancePersistenceError,
    AllowanceUnavailableError,
    OpenRecurrenceAllowanceApplication,
)
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/open-recurrence-allowances", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class RenewalNoticeResponse(BaseModel):
    owner: Literal["routine", "event"]
    source_ref: UUID
    title: str
    material_state_ref: UUID
    allowed_count: int
    remaining_count: int
    revision: int


class RenewalDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID
    expected_revision: int = Field(ge=0)
    decision: Literal["extend", "decline"]


def _application(request: Request) -> OpenRecurrenceAllowanceApplication:
    return OpenRecurrenceAllowanceApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[OpenRecurrenceAllowanceApplication, Depends(_application)]


def _problem(error: Exception) -> ProblemError:
    if isinstance(error, AllowanceUnavailableError):
        return ProblemError(
            status=404,
            code="temporal.recurrence.allowance_unavailable",
            category="not_found",
            title="Renewal unavailable",
            detail="This open series has no pending renewal notice.",
        )
    if isinstance(error, AllowanceConflictError):
        return ProblemError(
            status=409,
            code="temporal.recurrence.allowance_conflict",
            category="conflict",
            title="Renewal changed",
            detail="Reload the current series notice and retry.",
        )
    return ProblemError(
        status=503,
        code="temporal.recurrence.allowance_persistence_unavailable",
        category="service",
        title="Renewal unavailable",
        detail="The decision could not be saved.",
        retryable=True,
    )


@router.get(
    "",
    response_model=list[RenewalNoticeResponse],
    operation_id="temporal_list_open_recurrence_allowances",
)
async def list_renewal_notices(
    context: ReadContext, application: Application, response: Response
) -> list[RenewalNoticeResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        notices = await application.list_notices(
            actor=context.self_person_ref,
            today=datetime.now(ZoneInfo(context.effective_zone_id)).date(),
            effective_zone_id=context.effective_zone_id,
        )
        return [RenewalNoticeResponse.model_validate(asdict(notice)) for notice in notices]
    except AllowancePersistenceError as exc:
        raise _problem(exc) from exc


@router.post(
    "/{owner}/{source_ref}/decision",
    status_code=204,
    operation_id="temporal_decide_open_recurrence_allowance",
)
async def decide_renewal(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    payload: RenewalDecisionRequest,
    context: WriteContext,
    application: Application,
    response: Response,
) -> None:
    response.headers["Cache-Control"] = "no-store"
    try:
        await application.decide(
            actor=context.self_person_ref,
            owner=owner,
            source_ref=source_ref,
            title="",
            today=datetime.now(ZoneInfo(context.effective_zone_id)).date(),
            effective_zone_id=context.effective_zone_id,
            expected_state_ref=payload.expected_material_state_ref,
            expected_revision=payload.expected_revision,
            operation_id=payload.operation_id,
            decision=payload.decision,
        )
    except (AllowanceUnavailableError, AllowanceConflictError, AllowancePersistenceError) as exc:
        raise _problem(exc) from exc
