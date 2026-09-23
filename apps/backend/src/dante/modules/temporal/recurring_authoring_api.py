"""B06-D recurring source authoring transport."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_mutating_dante_context
from dante.modules.temporal.event import (
    EventAgendaRevisionConflictError,
    EventInputError,
    EventLifeAreaUnavailableError,
    EventNotFoundError,
    EventOperationIdReuseError,
    EventPersistenceError,
)
from dante.modules.temporal.recurrence import (
    RecurrenceInputError,
    RecurrenceNotFoundError,
    RecurrenceOperationReuseError,
    RecurrencePersistenceError,
    RecurrenceStateConflictError,
)
from dante.modules.temporal.recurrence_api import RecurrenceRequest, _spec
from dante.modules.temporal.recurring_authoring import (
    RecurringAuthoringApplication,
    RecurringAuthoringOperationReuseError,
    RecurringAuthoringPersistenceError,
)
from dante.modules.temporal.routine import (
    RoutineInputError,
    RoutineNotFoundError,
    RoutineOperationReuseError,
    RoutinePersistenceError,
    RoutineStateConflictError,
)
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class CreateRecurringRoutineRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area_ref: UUID
    tag_refs: list[UUID] = Field(default_factory=list, max_length=100)
    recurrence: RecurrenceRequest


class CreateRecurringEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area_ref: UUID
    agenda_parts: list[str] = Field(default_factory=list, max_length=100)
    recurrence: RecurrenceRequest


class RecurringAuthoringResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    owner_kind: Literal["routine", "event"]
    source_ref: UUID
    title: str
    created_at: datetime
    recurrence_material_state_ref: UUID
    replayed: bool


def _application(request: Request) -> RecurringAuthoringApplication:
    return RecurringAuthoringApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[RecurringAuthoringApplication, Depends(_application)]


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, (RoutineInputError, EventInputError, RecurrenceInputError)):
        return ProblemError(
            status=422,
            code="temporal.recurring_authoring.invalid_input",
            category="validation",
            title="Recurring authoring rejected",
            detail=str(exc),
        )
    if isinstance(
        exc,
        (
            RecurringAuthoringOperationReuseError,
            RoutineOperationReuseError,
            EventOperationIdReuseError,
            RecurrenceOperationReuseError,
        ),
    ):
        return ProblemError(
            status=409,
            code="temporal.recurring_authoring.operation_id_reused",
            category="conflict",
            title="Recurring authoring operation id reused",
            detail="Use a fresh operation id for a different source or Recurrence intent.",
        )
    if isinstance(exc, (RoutineStateConflictError, EventAgendaRevisionConflictError, RecurrenceStateConflictError)):
        return ProblemError(
            status=409,
            code="temporal.recurring_authoring.state_conflict",
            category="conflict",
            title="Recurring authoring state changed",
            detail="Reload canonical state and retry.",
        )
    if isinstance(exc, (RoutineNotFoundError, EventLifeAreaUnavailableError, EventNotFoundError, RecurrenceNotFoundError)):
        return ProblemError(
            status=404,
            code="temporal.recurring_authoring.unavailable",
            category="not_found",
            title="Recurring authoring target unavailable",
            detail="The source organization target is unavailable in this account.",
        )
    if isinstance(exc, (RoutinePersistenceError, EventPersistenceError, RecurrencePersistenceError, RecurringAuthoringPersistenceError)):
        return ProblemError(
            status=503,
            code="temporal.recurring_authoring.persistence_unavailable",
            category="service",
            title="Recurring authoring unavailable",
            detail="Canonical recurring source state could not be committed safely.",
            retryable=True,
        )
    return ProblemError(
        status=503,
        code="temporal.recurring_authoring.unavailable",
        category="service",
        title="Recurring authoring unavailable",
        detail="The recurring authoring capability could not complete.",
        retryable=True,
    )


@router.post(
    "/recurring/routines",
    response_model=RecurringAuthoringResponse,
    operation_id="temporal_create_recurring_routine",
)
async def create_recurring_routine(
    payload: CreateRecurringRoutineRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> RecurringAuthoringResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.create_routine(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_ref=payload.life_area_ref,
            tag_refs=tuple(payload.tag_refs),
            recurrence=_spec(payload.recurrence),
        )
        return RecurringAuthoringResponse(**asdict(value))
    except Exception as exc:
        raise _problem(exc) from exc


@router.post(
    "/recurring/events",
    response_model=RecurringAuthoringResponse,
    operation_id="temporal_create_recurring_event",
)
async def create_recurring_event(
    payload: CreateRecurringEventRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> RecurringAuthoringResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.create_event(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_ref=payload.life_area_ref,
            agenda_parts=tuple(payload.agenda_parts),
            recurrence=_spec(payload.recurrence),
        )
        return RecurringAuthoringResponse(**asdict(value))
    except Exception as exc:
        raise _problem(exc) from exc
