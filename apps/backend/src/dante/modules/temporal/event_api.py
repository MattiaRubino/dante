"""Authenticated B03 API for Event identity, Agenda and shared Schedule authoring."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Any, Literal, cast
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import (
    require_dante_context,
    require_mutating_dante_context,
)
from dante.modules.temporal.event import (
    EventAgendaRevisionConflictError,
    EventInputError,
    EventLifeAreaUnavailableError,
    EventNotFoundError,
    EventOperationIdReuseError,
    EventPersistenceError,
    EventReplanConflictError,
    EventView,
    PostponedEventView,
    TemporalEventApplication,
    _read_event_in_session,
)
from dante.modules.temporal.life_area_assignment import (
    _fingerprint as assignment_fingerprint,
)
from dante.modules.temporal.reality_objective_api import (
    ActivityObjectiveBatchCommand,
    ObjectiveResponse,
    RealityPolicyCommand,
    apply_event_objective_edits_in_session,
)
from dante.modules.temporal.reality_objective_api import (
    _fingerprint as reality_fingerprint,
)
from dante.modules.temporal.responsibility_participation import (
    ResponsibilityConflictError,
    ResponsibilityInputError,
    ResponsibilityNotFoundError,
    ResponsibilityOperationReuseError,
    ResponsibilityParticipationApplication,
    ResponsibilityPersistenceError,
)
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    CoarseLocalPeriodPlacement,
    DateSpanPlacement,
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    SchedulePersistenceError,
    SchedulePlacement,
    SchedulePlacementLockedError,
    ScheduleRevisionConflictError,
    revise_schedule_in_session,
)
from dante.modules.temporal.schedule_reminder import (
    ScheduleReminderApplication,
    ScheduleReminderConflictError,
    ScheduleReminderInputError,
    ScheduleReminderNotFoundError,
    ScheduleReminderPersistenceError,
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
AgendaPart = Annotated[str, Field(min_length=1, max_length=1000)]


class CreateEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area_ref: UUID
    agenda_parts: list[AgendaPart] = Field(default_factory=list, max_length=100)


class ReplaceEventAgendaRequest(BaseModel):
    """Whole-Agenda replacement behind explicit aggregate CAS."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_revision: int = Field(ge=0)
    agenda_parts: list[AgendaPart] = Field(max_length=100)


class EventDateSpanPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class EventFloatingLocalIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["floating_local_interval"] = "floating_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime


class EventNamedZoneLocalIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["named_zone_local_interval"] = "named_zone_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str = Field(min_length=1, max_length=200)
    disambiguation: Literal["reject", "earlier", "later"] = "reject"


class EventAbsoluteIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["absolute_interval"] = "absolute_interval"
    starts_at: datetime
    ends_at: datetime


class EventCoarseLocalPeriodPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


EventSchedulePlacementRequest = Annotated[
    EventDateSpanPlacementRequest
    | EventFloatingLocalIntervalPlacementRequest
    | EventNamedZoneLocalIntervalPlacementRequest
    | EventAbsoluteIntervalPlacementRequest
    | EventCoarseLocalPeriodPlacementRequest,
    Field(discriminator="kind"),
]


class CreateScheduledEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    life_area_ref: UUID
    agenda_parts: list[AgendaPart] = Field(default_factory=list, max_length=100)
    placement: EventSchedulePlacementRequest


class ReplanPostponedEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    unschedule_operation_id: str = Field(min_length=1, max_length=200)
    placement: EventSchedulePlacementRequest


class EventResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    description: str | None = None
    location: str | None = None
    color_code: str | None = None
    profile_revision: int = Field(default=0, ge=0)
    replayed: bool = False


class EventAgendaMutationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    agenda_revision: int = Field(ge=1)
    agenda_parts: list[str]
    replayed: bool = False


class PostponedEventResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    schedule_ref: UUID
    title: str
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    unschedule_operation_id: str


class ScheduledEventFloatingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime
    replayed: bool = False


class ScheduledEventDateSpanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date
    replayed: bool = False


class ScheduledEventNamedZoneResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["named_zone_local"] = "named_zone_local"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime
    replayed: bool = False


class ScheduledEventAbsoluteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime
    replayed: bool = False


class ScheduledEventCoarseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]
    replayed: bool = False


ScheduledEventMutationResponse = Annotated[
    ScheduledEventFloatingResponse
    | ScheduledEventDateSpanResponse
    | ScheduledEventNamedZoneResponse
    | ScheduledEventAbsoluteResponse
    | ScheduledEventCoarseResponse,
    Field(discriminator="temporal_form"),
]


def get_temporal_event_application(request: Request) -> TemporalEventApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalEventApplication(database_runtime.session_factory)


TemporalEventApplicationDependency = Annotated[
    TemporalEventApplication,
    Depends(get_temporal_event_application),
]


def _event_response(event: EventView, *, replayed: bool = False) -> EventResponse:
    return EventResponse(
        event_ref=event.event_ref,
        title=event.title,
        agenda_revision=event.agenda_revision,
        agenda_parts=list(event.agenda_parts),
        created_at=event.created_at,
        life_area_ref=event.life_area_ref,
        life_area_assignment_revision=event.life_area_assignment_revision,
        description=event.description,
        location=event.location,
        color_code=event.color_code,
        profile_revision=event.profile_revision,
        replayed=replayed,
    )


def _postponed_event_response(event: PostponedEventView) -> PostponedEventResponse:
    return PostponedEventResponse(
        event_ref=event.event_ref,
        schedule_ref=event.schedule_ref,
        title=event.title,
        created_at=event.created_at,
        life_area_ref=event.life_area_ref,
        life_area_assignment_revision=event.life_area_assignment_revision,
        unschedule_operation_id=event.unschedule_operation_id,
    )


def _placement_from_request(payload: EventSchedulePlacementRequest) -> SchedulePlacement:
    if isinstance(payload, EventDateSpanPlacementRequest):
        return DateSpanPlacement(
            start_date=payload.start_date,
            end_date_exclusive=payload.end_date_exclusive,
        )
    if isinstance(payload, EventFloatingLocalIntervalPlacementRequest):
        return FloatingLocalIntervalPlacement(
            starts_local_at=payload.starts_local_at,
            ends_local_at=payload.ends_local_at,
        )
    if isinstance(payload, EventNamedZoneLocalIntervalPlacementRequest):
        return NamedZoneLocalIntervalPlacement(
            starts_local_at=payload.starts_local_at,
            ends_local_at=payload.ends_local_at,
            zone_id=payload.zone_id,
            disambiguation=payload.disambiguation,
        )
    if isinstance(payload, EventAbsoluteIntervalPlacementRequest):
        return AbsoluteIntervalPlacement(
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
        )
    if isinstance(payload, EventCoarseLocalPeriodPlacementRequest):
        return CoarseLocalPeriodPlacement(
            local_date=payload.local_date,
            period=payload.period,
        )
    raise TypeError("Unsupported Event authoring placement")


def _scheduled_event_response(
    *,
    event: EventView,
    schedule_ref: UUID,
    material_state_ref: UUID,
    placement: SchedulePlacement,
    replayed: bool,
) -> ScheduledEventMutationResponse:
    common: dict[str, Any] = {
        "event_ref": event.event_ref,
        "title": event.title,
        "agenda_revision": event.agenda_revision,
        "agenda_parts": list(event.agenda_parts),
        "created_at": event.created_at,
        "life_area_ref": event.life_area_ref,
        "life_area_assignment_revision": event.life_area_assignment_revision,
        "schedule_ref": schedule_ref,
        "placement_material_state_ref": material_state_ref,
        "replayed": replayed,
    }
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return ScheduledEventFloatingResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
        )
    if isinstance(placement, DateSpanPlacement):
        return ScheduledEventDateSpanResponse(
            **common,
            start_date=placement.start_date,
            end_date_exclusive=placement.end_date_exclusive,
        )
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        return ScheduledEventNamedZoneResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
            zone_id=placement.zone_id,
            resolved_start_at=cast(datetime, placement.resolved_start_at),
            resolved_end_at=cast(datetime, placement.resolved_end_at),
        )
    if isinstance(placement, AbsoluteIntervalPlacement):
        return ScheduledEventAbsoluteResponse(
            **common,
            starts_at=placement.starts_at,
            ends_at=placement.ends_at,
        )
    return ScheduledEventCoarseResponse(
        **common,
        local_date=placement.local_date,
        period=placement.period,
    )


def _not_found_problem() -> ProblemError:
    return ProblemError(
        status=404,
        code="temporal.event.not_found",
        category="not_found",
        title="Event not found",
        detail="No Event is available at that reference in the current self scope.",
        retryable=False,
    )


@router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(
    payload: CreateEventRequest,
    context: MutatingDanteContextDependency,
    application: TemporalEventApplicationDependency,
    response: Response,
) -> EventResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create_event(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_ref=payload.life_area_ref,
            agenda_parts=payload.agenda_parts,
        )
    except EventInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.event.invalid_create",
            category="validation",
            title="Invalid Event",
            detail=str(exc),
            retryable=False,
        ) from exc
    except EventOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event.operation_id_reused",
            category="conflict",
            title="Event operation conflict",
            detail="The operation id was already used for a different Event intent.",
            retryable=False,
        ) from exc
    except EventLifeAreaUnavailableError as exc:
        raise ProblemError(
            status=422,
            code="temporal.event.life_area_unavailable",
            category="validation",
            title="Unavailable Life Area",
            detail="The primary Life Area is unavailable or archived in the current self scope.",
            retryable=False,
        ) from exc
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.persistence_unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event could not be persisted safely.",
            retryable=True,
        ) from exc

    if result.replayed:
        response.status_code = 200
    return _event_response(result.event, replayed=result.replayed)


@router.post(
    "/events/scheduled",
    response_model=ScheduledEventMutationResponse,
    status_code=201,
)
async def create_scheduled_event(
    payload: CreateScheduledEventRequest,
    context: MutatingDanteContextDependency,
    application: TemporalEventApplicationDependency,
    response: Response,
) -> ScheduledEventMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        placement = _placement_from_request(payload.placement)
        result = await application.create_event_with_schedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_ref=payload.life_area_ref,
            agenda_parts=payload.agenda_parts,
            placement=placement,
        )
    except (EventInputError, ScheduleInputError) as exc:
        raise ProblemError(
            status=422,
            code="temporal.event.invalid_schedule_create",
            category="validation",
            title="Invalid scheduled Event",
            detail=str(exc),
            retryable=False,
        ) from exc
    except EventOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event.operation_id_reused",
            category="conflict",
            title="Event operation conflict",
            detail="The operation id was already used for a different Event intent.",
            retryable=False,
        ) from exc
    except EventLifeAreaUnavailableError as exc:
        raise ProblemError(
            status=422,
            code="temporal.event.life_area_unavailable",
            category="validation",
            title="Unavailable Life Area",
            detail="The primary Life Area is unavailable or archived in the current self scope.",
            retryable=False,
        ) from exc
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.persistence_unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event, Agenda and Schedule could not be persisted atomically.",
            retryable=True,
        ) from exc

    if result.replayed:
        response.status_code = 200
    return _scheduled_event_response(
        event=result.event,
        schedule_ref=result.schedule.schedule_ref,
        material_state_ref=result.schedule.material_state_ref,
        placement=result.schedule.placement,
        replayed=result.replayed,
    )


@router.put("/events/{event_ref}/agenda", response_model=EventAgendaMutationResponse)
async def replace_event_agenda(
    event_ref: UUID,
    payload: ReplaceEventAgendaRequest,
    context: MutatingDanteContextDependency,
    application: TemporalEventApplicationDependency,
    response: Response,
) -> EventAgendaMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.replace_agenda(
            self_person_ref=context.self_person_ref,
            event_ref=NativeRef(event_ref),
            operation_id=payload.operation_id,
            expected_revision=payload.expected_revision,
            agenda_parts=payload.agenda_parts,
        )
    except EventInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.event.invalid_agenda",
            category="validation",
            title="Invalid Event Agenda",
            detail=str(exc),
            retryable=False,
        ) from exc
    except EventOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event.agenda_operation_id_reused",
            category="conflict",
            title="Event Agenda operation conflict",
            detail="The operation id was already used for a different Agenda mutation.",
            retryable=False,
        ) from exc
    except EventAgendaRevisionConflictError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event.agenda_revision_conflict",
            category="conflict",
            title="Event Agenda revision conflict",
            detail="The Event Agenda changed after the expected revision was read.",
            retryable=False,
        ) from exc
    except EventNotFoundError as exc:
        raise _not_found_problem() from exc
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.persistence_unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event Agenda could not be persisted safely.",
            retryable=True,
        ) from exc

    return EventAgendaMutationResponse(
        event_ref=result.event_ref,
        agenda_revision=result.agenda_revision,
        agenda_parts=list(result.agenda_parts),
        replayed=result.replayed,
    )


@router.get(
    "/events/postponed",
    response_model=list[PostponedEventResponse],
    operation_id="temporal_list_postponed_events",
)
async def list_postponed_events(
    context: DanteContextDependency,
    application: TemporalEventApplicationDependency,
    response: Response,
) -> list[PostponedEventResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        events = await application.list_postponed(self_person_ref=context.self_person_ref)
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.postponed_read_unavailable",
            category="service",
            title="Postponed Events unavailable",
            detail="Postponed Events could not be read safely.",
            retryable=True,
        ) from exc
    return [_postponed_event_response(event) for event in events]


@router.put(
    "/events/{event_ref}/schedules/{schedule_ref}/replan",
    response_model=ScheduledEventMutationResponse,
    operation_id="temporal_replan_postponed_event",
)
async def replan_postponed_event(
    event_ref: UUID,
    schedule_ref: UUID,
    payload: ReplanPostponedEventRequest,
    context: MutatingDanteContextDependency,
    application: TemporalEventApplicationDependency,
    response: Response,
) -> ScheduledEventMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.replan_postponed_event(
            self_person_ref=context.self_person_ref,
            event_ref=NativeRef(event_ref),
            schedule_ref=schedule_ref,
            unschedule_operation_id=payload.unschedule_operation_id,
            operation_id=payload.operation_id,
            placement=_placement_from_request(payload.placement),
        )
    except (EventInputError, ScheduleInputError) as exc:
        raise ProblemError(
            status=422,
            code="temporal.event.invalid_replan",
            category="validation",
            title="Invalid Event replan",
            detail=str(exc),
            retryable=False,
        ) from exc
    except EventOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event.replan_operation_id_reused",
            category="conflict",
            title="Event replan operation conflict",
            detail="The operation id was already used for a different Event replan.",
            retryable=False,
        ) from exc
    except EventReplanConflictError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event.replan_conflict",
            category="conflict",
            title="Event replan conflict",
            detail="The Event Schedule is no longer in the postponed state that was read.",
            retryable=False,
        ) from exc
    except EventNotFoundError as exc:
        raise _not_found_problem() from exc
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.persistence_unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event could not be replanned atomically.",
            retryable=True,
        ) from exc
    return _scheduled_event_response(
        event=result.event,
        schedule_ref=result.schedule.schedule_ref,
        material_state_ref=result.schedule.material_state_ref,
        placement=result.schedule.placement,
        replayed=result.replayed,
    )


@router.get("/events/{event_ref}", response_model=EventResponse)
async def get_event(
    event_ref: UUID,
    context: DanteContextDependency,
    application: TemporalEventApplicationDependency,
    response: Response,
) -> EventResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        event = await application.get_event(
            self_person_ref=context.self_person_ref,
            event_ref=NativeRef(event_ref),
        )
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.persistence_unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event could not be read safely.",
            retryable=True,
        ) from exc

    if event is None:
        raise _not_found_problem()
    return _event_response(event)


class ReviseEventProfileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_revision: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    location: str | None = None
    color_code: str | None = None


class RevisedEventProfileResponse(BaseModel):
    event_ref: UUID
    title: str
    description: str | None
    location: str | None
    color_code: str | None
    revision: int = Field(ge=1)
    replayed: bool


class EventAtomicLifeAreaChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_assignment_revision: int = Field(ge=0)
    life_area_ref: UUID | None


class EventAtomicScheduleChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    expected_material_state_ref: UUID
    placement: EventSchedulePlacementRequest


class EventAtomicReminderChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    expected_state_ref: UUID | None = None
    enabled: bool
    lead_minutes: int = Field(ge=0, le=10080)


class EventAtomicParticipantChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    participant_ref: UUID | Literal["self"]
    requirement_code: Literal["required", "optional"] | None
    expected_requirement_code: Literal["required", "optional"] | None


class EventAtomicEditCommand(BaseModel):
    """One-off Event metadata, Agenda, Life Area, Reality and Objectives."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=140)
    profile: ReviseEventProfileRequest | None = None
    agenda: ReplaceEventAgendaRequest | None = None
    life_area: EventAtomicLifeAreaChange | None = None
    schedule: EventAtomicScheduleChange | None = None
    reminder: EventAtomicReminderChange | None = None
    participants: list[EventAtomicParticipantChange] | None = Field(default=None, min_length=1)
    reality: RealityPolicyCommand | None = None
    objectives: ActivityObjectiveBatchCommand | None = None

    @model_validator(mode="after")
    def nonempty(self) -> EventAtomicEditCommand:
        if all(
            value is None
            for value in (
                self.profile,
                self.agenda,
                self.life_area,
                self.schedule,
                self.reminder,
                self.participants,
                self.reality,
                self.objectives,
            )
        ):
            raise ValueError("Select at least one Event change.")
        if self.participants is not None and len(
            {row.participant_ref for row in self.participants}
        ) != len(self.participants):
            raise ValueError("Each Event participant may be changed once per edit.")
        return self


class EventAtomicEditResponse(BaseModel):
    event: EventResponse
    objectives: list[ObjectiveResponse]


@router.put(
    "/events/{event_ref}/profile",
    response_model=RevisedEventProfileResponse,
    operation_id="temporal_revise_self_event_profile",
)
async def revise_event_profile(
    event_ref: UUID,
    body: ReviseEventProfileRequest,
    context: MutatingDanteContextDependency,
    request: Request,
    response: Response,
) -> RevisedEventProfileResponse:
    """Owner-serialized immutable revision of the current Event descriptor."""
    response.headers["Cache-Control"] = "no-store"
    try:
        runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
        async with runtime.session_factory() as session, session.begin():
            accepted = (
                (
                    await session.execute(
                        text("""
                SELECT * FROM dante.revise_self_event_profile(
                    :actor,:event,:operation,:expected,:title,:description,:location,:color)
            """),
                        {
                            "actor": context.self_person_ref,
                            "event": NativeRef(event_ref),
                            "operation": body.operation_id,
                            "expected": body.expected_revision,
                            "title": body.title,
                            "description": body.description,
                            "location": body.location,
                            "color": body.color_code,
                        },
                    )
                )
                .mappings()
                .one()
            )
    except DBAPIError as exc:
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
        if constraint == "event_profile_unavailable":
            raise _not_found_problem() from exc
        if constraint == "event_profile_recurring_source":
            raise ProblemError(
                status=409,
                code="temporal.event.profile_recurring_source",
                category="conflict",
                title="Recurring Event scope required",
                detail="Select an Occurrence and an explicit edit scope; this source is not editable as one Event.",
                retryable=False,
            ) from exc
        if constraint in ("event_profile_revision_conflict", "uq_event_profile_revision_operation"):
            raise ProblemError(
                status=409,
                code="temporal.event.profile_conflict",
                category="conflict",
                title="Event profile changed",
                detail="Reload the Event before revising its metadata.",
                retryable=False,
            ) from exc
        if constraint in ("event_profile_invalid", "event_profile_no_change"):
            raise ProblemError(
                status=422,
                code="temporal.event.profile_invalid",
                category="validation",
                title="Invalid Event metadata",
                detail="Use a nonempty title and canonical optional metadata.",
                retryable=False,
            ) from exc
        raise ProblemError(
            status=503,
            code="temporal.event.profile_unavailable",
            category="service",
            title="Event profile unavailable",
            detail="The Event profile could not be updated safely.",
            retryable=True,
        ) from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.profile_unavailable",
            category="service",
            title="Event profile unavailable",
            detail="The Event profile could not be updated safely.",
            retryable=True,
        ) from exc
    return RevisedEventProfileResponse(**accepted)


@router.put(
    "/events/{event_ref}/atomic-edit",
    response_model=EventAtomicEditResponse,
    operation_id="temporal_apply_one_off_event_atomic_edit",
)
async def apply_one_off_event_atomic_edit(
    event_ref: UUID,
    body: EventAtomicEditCommand,
    context: MutatingDanteContextDependency,
    request: Request,
    response: Response,
) -> EventAtomicEditResponse:
    """Commit the one-off Event's supported edits in one transaction.

    Recurring sources require an explicit occurrence scope; this command
    cannot silently flatten a series or partially persist its descendants.
    """
    response.headers["Cache-Control"] = "no-store"
    actor = context.self_person_ref
    native_event = NativeRef(event_ref)
    runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    try:
        async with runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            await session.execute(
                text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
                {"key": f"event-atomic:{actor}:{event_ref}"},
            )
            current = await _read_event_in_session(
                session, self_person_ref=actor, event_ref=native_event
            )
            if current is None:
                raise _not_found_problem()
            recurrence = await session.execute(
                text("SELECT 1 FROM dante.get_self_event_recurrence(:actor,:source) LIMIT 1"),
                {"actor": actor, "source": native_event},
            )
            if recurrence.first() is not None:
                raise ProblemError(
                    status=409,
                    code="temporal.event_edit.recurring_source",
                    category="conflict",
                    title="Recurring Event scope required",
                    detail="Select an Occurrence and an explicit edit scope.",
                )
            target_schedule = (
                body.schedule.schedule_ref
                if body.schedule is not None
                else body.reminder.schedule_ref
                if body.reminder is not None
                else None
            )
            if target_schedule is not None:
                owned = (
                    await session.execute(
                        text("SELECT dante.assert_self_event_schedule(:actor,:event,:schedule)"),
                        {
                            "actor": actor,
                            "event": native_event,
                            "schedule": target_schedule,
                        },
                    )
                ).scalar_one()
                if not owned:
                    raise ProblemError(
                        status=409,
                        code="temporal.event_edit.schedule_mismatch",
                        category="conflict",
                        title="Event Schedule changed",
                        detail="Reload the Event before changing its Schedule.",
                    )
            if body.reminder is not None:
                change_reminder = body.reminder
                if target_schedule != change_reminder.schedule_ref:
                    raise ProblemError(
                        status=422,
                        code="temporal.event_edit.reminder_schedule_mismatch",
                        category="validation",
                        title="Invalid reminder target",
                        detail="The reminder must belong to the revised Event Schedule.",
                    )

            async def configure_reminder(change_reminder: EventAtomicReminderChange) -> None:
                await ScheduleReminderApplication(runtime.session_factory).configure(
                    self_person_ref=actor,
                    schedule_ref=ScopedRecordRef(change_reminder.schedule_ref),
                    operation_id=f"{body.operation_id}:reminder",
                    expected_material_state_ref=(
                        MaterialStateRef(change_reminder.expected_state_ref)
                        if change_reminder.expected_state_ref is not None
                        else None
                    ),
                    enabled=change_reminder.enabled,
                    lead_minutes=change_reminder.lead_minutes,
                    session=session,
                )

            # A date-span/floating conversion removes the exact start required by
            # an active reminder. Disable it before revising the placement, in
            # the same transaction, so the complete edit remains atomic.
            if body.reminder is not None and not body.reminder.enabled:
                await configure_reminder(body.reminder)
            if body.schedule is not None:
                change_schedule = body.schedule
                await revise_schedule_in_session(
                    session,
                    self_person_ref=actor,
                    operation_id=f"{body.operation_id}:schedule",
                    schedule_ref=ScopedRecordRef(change_schedule.schedule_ref),
                    expected_material_state_ref=MaterialStateRef(
                        change_schedule.expected_material_state_ref
                    ),
                    placement=_placement_from_request(change_schedule.placement),
                )
            if body.reminder is not None and body.reminder.enabled:
                await configure_reminder(body.reminder)
            if body.participants:
                participation = ResponsibilityParticipationApplication(runtime.session_factory)
                for index, change_participant in enumerate(body.participants):
                    await participation.set_expected_participation(
                        self_person_ref=actor,
                        operation_id=f"{body.operation_id}:participant:{index}",
                        event_ref=native_event,
                        participant_person_ref=(
                            actor
                            if change_participant.participant_ref == "self"
                            else NativeRef(change_participant.participant_ref)
                        ),
                        requirement_code=change_participant.requirement_code,
                        expected_requirement_code=change_participant.expected_requirement_code,
                        session=session,
                    )
            if body.profile is not None:
                change = body.profile
                await session.execute(
                    text("""
                        SELECT * FROM dante.revise_self_event_profile(
                            :actor,:event,:operation,:expected,:title,
                            :description,:location,:color)
                    """),
                    {
                        "actor": actor,
                        "event": native_event,
                        "operation": change.operation_id,
                        "expected": change.expected_revision,
                        "title": change.title,
                        "description": change.description,
                        "location": change.location,
                        "color": change.color_code,
                    },
                )
            if body.agenda is not None:
                change_agenda = body.agenda
                await TemporalEventApplication(runtime.session_factory).replace_agenda_in_session(
                    session,
                    self_person_ref=actor,
                    event_ref=native_event,
                    operation_id=change_agenda.operation_id,
                    expected_revision=change_agenda.expected_revision,
                    agenda_parts=change_agenda.agenda_parts,
                )
            if body.life_area is not None:
                change_area = body.life_area
                await session.execute(
                    text("""
                        SELECT * FROM dante.assign_self_event_life_area(
                            :actor,:operation,:fingerprint,:event,:area,:expected)
                    """),
                    {
                        "actor": actor,
                        "operation": f"{body.operation_id}:area",
                        "fingerprint": assignment_fingerprint(
                            kind="event",
                            subject_ref=native_event,
                            life_area_ref=change_area.life_area_ref,
                            expected=change_area.expected_assignment_revision,
                        ),
                        "event": native_event,
                        "area": change_area.life_area_ref,
                        "expected": change_area.expected_assignment_revision,
                    },
                )
            if body.reality is not None:
                change_reality = body.reality
                intent = {
                    "version": 1,
                    "subject_kind": "event",
                    "subject_native_ref": str(event_ref),
                    "mode_code": change_reality.mode_code,
                    "expected_state_ref": (
                        str(change_reality.expected_state_ref)
                        if change_reality.expected_state_ref is not None
                        else None
                    ),
                }
                await session.execute(
                    text("""
                        SELECT * FROM dante.set_self_reality_review_policy(
                            :actor,:operation,:fingerprint,'event',:event,:state,:mode,:expected)
                    """),
                    {
                        "actor": actor,
                        "operation": change_reality.operation_id,
                        "fingerprint": reality_fingerprint(intent),
                        "event": native_event,
                        "state": uuid7(),
                        "mode": change_reality.mode_code,
                        "expected": change_reality.expected_state_ref,
                    },
                )
            objectives = (
                await apply_event_objective_edits_in_session(
                    session,
                    actor=actor,
                    subject_ref=event_ref,
                    payload=body.objectives,
                    effective_zone_id=context.effective_zone_id,
                )
                if body.objectives is not None
                else []
            )
            saved = await _read_event_in_session(
                session, self_person_ref=actor, event_ref=native_event
            )
            if saved is None:
                raise _not_found_problem()
            return EventAtomicEditResponse(event=_event_response(saved), objectives=objectives)
    except EventAgendaRevisionConflictError as exc:
        raise ProblemError(
            status=409,
            code="temporal.event_edit.agenda_conflict",
            category="conflict",
            title="Event Agenda changed",
            detail="Reload the Event and review the Agenda.",
        ) from exc
    except (
        EventInputError,
        ScheduleInputError,
        ScheduleReminderInputError,
        ResponsibilityInputError,
    ) as exc:
        raise ProblemError(
            status=422,
            code="temporal.event_edit.invalid_change",
            category="validation",
            title="Invalid Event change",
            detail=str(exc),
        ) from exc
    except (
        EventOperationIdReuseError,
        EventNotFoundError,
        ScheduleNotFoundError,
        ScheduleOperationIdReuseError,
        SchedulePlacementLockedError,
        ScheduleRevisionConflictError,
        ScheduleReminderConflictError,
        ScheduleReminderNotFoundError,
        ResponsibilityConflictError,
        ResponsibilityNotFoundError,
        ResponsibilityOperationReuseError,
    ) as exc:
        raise ProblemError(
            status=409,
            code="temporal.event_edit.conflict",
            category="conflict",
            title="Event changed",
            detail="Reload the Event before saving.",
        ) from exc
    except DBAPIError as exc:
        constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
        if constraint or getattr(exc.orig, "sqlstate", None) in {"40001", "23505"}:
            raise ProblemError(
                status=409,
                code="temporal.event_edit.conflict",
                category="conflict",
                title="Event changed",
                detail="Reload the Event before saving.",
            ) from exc
        raise ProblemError(
            status=503,
            code="temporal.event_edit.unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event edit could not be saved.",
            retryable=True,
        ) from exc
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event_edit.unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event edit could not be saved.",
            retryable=True,
        ) from exc
    except (
        EventPersistenceError,
        SchedulePersistenceError,
        ScheduleReminderPersistenceError,
        ResponsibilityPersistenceError,
    ) as exc:
        raise ProblemError(
            status=503,
            code="temporal.event_edit.unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event edit could not be saved.",
            retryable=True,
        ) from exc
