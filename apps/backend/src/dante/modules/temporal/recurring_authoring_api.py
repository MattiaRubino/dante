"""B06-D recurring source authoring transport."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_mutating_dante_context
from dante.modules.temporal.authoring import (
    AuthoringLifeAreaIntent,
    TemporalAuthoringInputError,
    TemporalAuthoringLifeAreaConflictError,
    TemporalAuthoringLifeAreaUnavailableError,
    TemporalAuthoringPersistenceError,
)
from dante.modules.temporal.authoring_api import AuthoringLifeAreaRequest
from dante.modules.temporal.event_occurrence_policy import (
    EventOccurrencePolicyApplication,
    EventOccurrencePolicyConflictError,
    EventOccurrencePolicyInputError,
    EventOccurrencePolicyNotFoundError,
    EventOccurrencePolicyPersistenceError,
)
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
from dante.modules.temporal.routine_occurrence_policy import (
    RoutineOccurrencePolicyApplication,
    RoutineOccurrencePolicyConflictError,
    RoutineOccurrencePolicyInputError,
    RoutineOccurrencePolicyNotFoundError,
    RoutineOccurrencePolicyPersistenceError,
)
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class CreateRecurringRoutineRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area: AuthoringLifeAreaRequest | None = None
    tag_refs: list[UUID] = Field(default_factory=list, max_length=100)
    recurrence: RecurrenceRequest
    duration_minutes: int = Field(ge=1, le=525_600)
    reminder_lead_minutes: int | None = Field(default=None, ge=0, le=10_080)
    activity_template: dict[str, Any] | None = None


class CreateRecurringEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area: AuthoringLifeAreaRequest | None = None
    description: str | None = None
    location: str | None = None
    item_color_code: str | None = None
    agenda_parts: list[str] = Field(default_factory=list, max_length=100)
    recurrence: RecurrenceRequest
    placement_kind: Literal["timed", "all_day"]
    duration_minutes: int | None = Field(default=None, ge=1, le=525_600)
    duration_days: int | None = Field(default=None, ge=1, le=3660)
    reminder_lead_minutes: int | None = Field(default=None, ge=0, le=10_080)


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


def _policy_application(request: Request) -> RoutineOccurrencePolicyApplication:
    return RoutineOccurrencePolicyApplication(request.app.state.database_runtime.session_factory)


def _event_policy_application(request: Request) -> EventOccurrencePolicyApplication:
    return EventOccurrencePolicyApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[RecurringAuthoringApplication, Depends(_application)]
PolicyApplication = Annotated[RoutineOccurrencePolicyApplication, Depends(_policy_application)]
EventPolicyApplication = Annotated[
    EventOccurrencePolicyApplication, Depends(_event_policy_application)
]


def _life_area_intent(payload: AuthoringLifeAreaRequest | None) -> AuthoringLifeAreaIntent | None:
    if payload is None:
        return None
    return AuthoringLifeAreaIntent(
        life_area_ref=payload.life_area_ref,
        new_name=payload.new_name,
        expected_revision=payload.expected_revision,
        color_code=payload.color_code,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(
        exc,
        (
            RoutineInputError,
            EventInputError,
            RecurrenceInputError,
            RoutineOccurrencePolicyInputError,
            EventOccurrencePolicyInputError,
            TemporalAuthoringInputError,
        ),
    ):
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
            RoutineOccurrencePolicyConflictError,
            EventOccurrencePolicyConflictError,
            TemporalAuthoringLifeAreaConflictError,
        ),
    ):
        return ProblemError(
            status=409,
            code="temporal.recurring_authoring.operation_id_reused",
            category="conflict",
            title="Recurring authoring operation id reused",
            detail="Use a fresh operation id for a different source or Recurrence intent.",
        )
    if isinstance(
        exc,
        (RoutineStateConflictError, EventAgendaRevisionConflictError, RecurrenceStateConflictError),
    ):
        return ProblemError(
            status=409,
            code="temporal.recurring_authoring.state_conflict",
            category="conflict",
            title="Recurring authoring state changed",
            detail="Reload canonical state and retry.",
        )
    if isinstance(
        exc,
        (
            RoutineNotFoundError,
            EventLifeAreaUnavailableError,
            EventNotFoundError,
            RecurrenceNotFoundError,
            RoutineOccurrencePolicyNotFoundError,
            EventOccurrencePolicyNotFoundError,
            TemporalAuthoringLifeAreaUnavailableError,
        ),
    ):
        return ProblemError(
            status=404,
            code="temporal.recurring_authoring.unavailable",
            category="not_found",
            title="Recurring authoring target unavailable",
            detail="The source organization target is unavailable in this account.",
        )
    if isinstance(
        exc,
        (
            RoutinePersistenceError,
            EventPersistenceError,
            RecurrencePersistenceError,
            RecurringAuthoringPersistenceError,
            RoutineOccurrencePolicyPersistenceError,
            EventOccurrencePolicyPersistenceError,
            TemporalAuthoringPersistenceError,
        ),
    ):
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
    policy_application: PolicyApplication,
    response: Response,
) -> RecurringAuthoringResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.create_routine(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_intent=_life_area_intent(payload.life_area),
            tag_refs=tuple(payload.tag_refs),
            recurrence=_spec(payload.recurrence),
        )
        await policy_application.set(
            self_person_ref=context.self_person_ref,
            routine_ref=value.source_ref,
            duration_minutes=payload.duration_minutes,
            reminder_lead_minutes=payload.reminder_lead_minutes,
            activity_template=payload.activity_template,
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
    policy_application: EventPolicyApplication,
    response: Response,
) -> RecurringAuthoringResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.create_event(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_intent=_life_area_intent(payload.life_area),
            agenda_parts=tuple(payload.agenda_parts),
            description=payload.description,
            location=payload.location,
            item_color_code=payload.item_color_code,
            recurrence=_spec(payload.recurrence),
        )
        await policy_application.set(
            self_person_ref=context.self_person_ref,
            event_ref=value.source_ref,
            placement_kind=payload.placement_kind,
            duration_minutes=payload.duration_minutes,
            duration_days=payload.duration_days,
            reminder_lead_minutes=payload.reminder_lead_minutes,
        )
        return RecurringAuthoringResponse(**asdict(value))
    except Exception as exc:
        raise _problem(exc) from exc
