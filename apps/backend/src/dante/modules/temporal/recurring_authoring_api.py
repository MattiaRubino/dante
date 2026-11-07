"""B06-D recurring source authoring transport."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.authoring import (
    AuthoringLifeAreaIntent,
    TemporalAuthoringInputError,
    TemporalAuthoringLifeAreaConflictError,
    TemporalAuthoringLifeAreaUnavailableError,
    TemporalAuthoringPersistenceError,
)
from dante.modules.temporal.authoring_api import AuthoringLifeAreaRequest
from dante.modules.temporal.event import (
    EventAgendaRevisionConflictError,
    EventInputError,
    EventLifeAreaUnavailableError,
    EventNotFoundError,
    EventOperationIdReuseError,
    EventPersistenceError,
)
from dante.modules.temporal.event_occurrence_policy import (
    EventOccurrencePolicyConflictError,
    EventOccurrencePolicyInputError,
    EventOccurrencePolicyNotFoundError,
    EventOccurrencePolicyPersistenceError,
)
from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    RecurrenceInputError,
    RecurrenceNotFoundError,
    RecurrenceOperationReuseError,
    RecurrencePersistenceError,
    RecurrenceStateConflictError,
)
from dante.modules.temporal.recurrence_api import (
    CalendarRecurrenceRequest,
    RecurrenceRequest,
    _spec,
)
from dante.modules.temporal.recurring_authoring import (
    EventAuthoringPolicy,
    RecurringAuthoringApplication,
    RecurringAuthoringOperationReuseError,
    RecurringAuthoringPersistenceError,
    RoutineAuthoringPolicy,
)
from dante.modules.temporal.recurring_conversion import (
    ExistingActivityBasis,
    ExistingEventBasis,
    RecurringConversionApplication,
    RecurringConversionConflictError,
    RecurringConversionUnsupportedError,
)
from dante.modules.temporal.recurring_series_edit import _validate_structure
from dante.modules.temporal.recurring_series_reconciliation import SeriesReconciliationError
from dante.modules.temporal.routine import (
    RoutineInputError,
    RoutineNotFoundError,
    RoutineOperationReuseError,
    RoutinePersistenceError,
    RoutineStateConflictError,
)
from dante.modules.temporal.routine_occurrence_policy import (
    RoutineOccurrencePolicyConflictError,
    RoutineOccurrencePolicyInputError,
    RoutineOccurrencePolicyNotFoundError,
    RoutineOccurrencePolicyPersistenceError,
)
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]
Context = Annotated[DanteContext, Depends(require_dante_context)]


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

    @model_validator(mode="after")
    def valid_all_day(self) -> CreateRecurringRoutineRequest:
        template = self.activity_template or {}
        recurrence = self.recurrence
        if template.get("placement_kind") == "all_day":
            days = template.get("duration_days")
            if (
                type(days) is not int
                or not 1 <= days <= 365
                or self.duration_minutes != days * 1440
                or self.reminder_lead_minutes is not None
                or not isinstance(recurrence, CalendarRecurrenceRequest)
                or recurrence.clock_basis_code != "named_zone"
                or recurrence.zone_id is None
                or recurrence.wall_times
            ):
                raise ValueError(
                    "Recurring all-day Activity requires calendar dates without an hour."
                )
            try:
                calendar_spec = _spec(recurrence)
                if not isinstance(calendar_spec, CalendarRecurrence):
                    raise ValueError("Recurring all-day Activity requires a calendar recurrence.")
                _validate_structure(
                    "routine",
                    calendar_spec,
                    {
                        "version": 1,
                        "duration_minutes": self.duration_minutes,
                        "reminder_lead_minutes": self.reminder_lead_minutes,
                        "activity_template": template,
                    },
                )
            except SeriesReconciliationError as exc:
                raise ValueError(str(exc)) from exc
        return self


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
    reality_mode: Literal["manual", "review_on_end", "auto_confirm_outcome"] = "manual"
    objectives: list[dict[str, Any]] = Field(default_factory=list, max_length=100)


class StartExistingActivityRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_profile_revision: int = Field(ge=0)
    envelope_schedule_ref: UUID
    expected_placement_state_ref: UUID
    recurrence: CalendarRecurrenceRequest


class StartExistingEventRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_profile_revision: int = Field(ge=0)
    schedule_ref: UUID
    expected_placement_state_ref: UUID
    recurrence: CalendarRecurrenceRequest


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


def _conversion(request: Request) -> RecurringConversionApplication:
    return RecurringConversionApplication(request.app.state.database_runtime.session_factory)


Conversion = Annotated[RecurringConversionApplication, Depends(_conversion)]


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
    if isinstance(exc, RecurringConversionUnsupportedError):
        return ProblemError(
            status=422,
            code="temporal.recurring_authoring.existing_unsupported",
            category="validation",
            title="Existing Activity cannot start this recurrence",
            detail=str(exc),
        )
    if isinstance(exc, RecurringConversionConflictError):
        return ProblemError(
            status=409,
            code="temporal.recurring_authoring.existing_conflict",
            category="conflict",
            title="Existing Activity changed",
            detail=str(exc),
        )
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
    "/recurring/activities/{activity_ref}/start",
    response_model=RecurringAuthoringResponse,
    operation_id="temporal_start_existing_activity_recurrence",
)
async def start_existing_activity_recurrence(
    activity_ref: UUID,
    payload: StartExistingActivityRecurrenceRequest,
    context: MutatingContext,
    application: Conversion,
    response: Response,
) -> RecurringAuthoringResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        recurrence = _spec(payload.recurrence)
        if not isinstance(recurrence, CalendarRecurrence):
            raise RecurringConversionUnsupportedError("Choose a calendar recurrence.")
        result = await application.activity(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            basis=ExistingActivityBasis(
                activity_ref=activity_ref,
                expected_profile_revision=payload.expected_profile_revision,
                envelope_schedule_ref=payload.envelope_schedule_ref,
                expected_placement_state_ref=payload.expected_placement_state_ref,
            ),
            recurrence=recurrence,
        )
        return RecurringAuthoringResponse(**asdict(result))
    except Exception as exc:
        raise _problem(exc) from exc


@router.post(
    "/recurring/events/{event_ref}/start",
    response_model=RecurringAuthoringResponse,
    operation_id="temporal_start_existing_event_recurrence",
)
async def start_existing_event_recurrence(
    event_ref: UUID,
    payload: StartExistingEventRecurrenceRequest,
    context: MutatingContext,
    application: Conversion,
    response: Response,
) -> RecurringAuthoringResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        recurrence = _spec(payload.recurrence)
        if not isinstance(recurrence, CalendarRecurrence):
            raise RecurringConversionUnsupportedError("Choose a calendar recurrence.")
        result = await application.event(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            basis=ExistingEventBasis(
                event_ref=event_ref,
                expected_profile_revision=payload.expected_profile_revision,
                schedule_ref=payload.schedule_ref,
                expected_placement_state_ref=payload.expected_placement_state_ref,
            ),
            recurrence=recurrence,
        )
        return RecurringAuthoringResponse(**asdict(result))
    except Exception as exc:
        raise _problem(exc) from exc


@router.get(
    "/recurring/events/{event_ref}/seed",
    response_model=UUID | None,
    operation_id="temporal_get_existing_event_recurrence_seed",
)
async def get_existing_event_recurrence_seed(
    event_ref: UUID,
    context: Context,
    request: Request,
    response: Response,
) -> UUID | None:
    response.headers["Cache-Control"] = "no-store"
    async with request.app.state.database_runtime.session_factory() as session:
        async with session.begin():
            source_ref = await session.scalar(
                text(
                    "SELECT source_event_ref FROM dante.get_self_event_recurring_seed(:actor,:event)"
                ),
                {"actor": context.self_person_ref, "event": event_ref},
            )
        return UUID(str(source_ref)) if source_ref is not None else None


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
            life_area_intent=_life_area_intent(payload.life_area),
            tag_refs=tuple(payload.tag_refs),
            recurrence=_spec(payload.recurrence),
            policy=RoutineAuthoringPolicy(
                duration_minutes=payload.duration_minutes,
                reminder_lead_minutes=payload.reminder_lead_minutes,
                activity_template=payload.activity_template,
            ),
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
            life_area_intent=_life_area_intent(payload.life_area),
            agenda_parts=tuple(payload.agenda_parts),
            description=payload.description,
            location=payload.location,
            item_color_code=payload.item_color_code,
            recurrence=_spec(payload.recurrence),
            policy=EventAuthoringPolicy(
                placement_kind=payload.placement_kind,
                duration_minutes=payload.duration_minutes,
                duration_days=payload.duration_days,
                reminder_lead_minutes=payload.reminder_lead_minutes,
                reality_mode=payload.reality_mode,
                objectives=tuple(payload.objectives),
            ),
        )
        return RecurringAuthoringResponse(**asdict(value))
    except Exception as exc:
        raise _problem(exc) from exc
