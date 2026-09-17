"""Authenticated B03 API for Event identity and shared Schedule authoring."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Any, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import (
    require_dante_context,
    require_mutating_dante_context,
)
from dante.modules.temporal.event import (
    EventInputError,
    EventOperationIdReuseError,
    EventPersistenceError,
    EventView,
    TemporalEventApplication,
)
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    CoarseLocalPeriodPlacement,
    DateSpanPlacement,
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    SchedulePlacement,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
DanteContextDependency = Annotated[DanteContext, Depends(require_dante_context)]
MutatingDanteContextDependency = Annotated[
    DanteContext,
    Depends(require_mutating_dante_context),
]


class CreateEventRequest(BaseModel):
    """Minimum B03-A CreateEvent command; Schedule remains a separate capability."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)


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
    """Shared Schedule form kept typed but not activated for Event authoring in B03-B."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


EventSchedulePlacementRequest = Annotated[
    EventDateSpanPlacementRequest
    | EventFloatingLocalIntervalPlacementRequest
    | EventNamedZoneLocalIntervalPlacementRequest
    | EventAbsoluteIntervalPlacementRequest,
    Field(discriminator="kind"),
]


class CreateScheduledEventRequest(BaseModel):
    """Atomic Event expectation + shared Schedule authoring command."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    placement: EventSchedulePlacementRequest


class EventResponse(BaseModel):
    """Minimum canonical Event expectation representation."""

    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    created_at: datetime
    replayed: bool = False


class ScheduledEventFloatingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    created_at: datetime
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
    created_at: datetime
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
    created_at: datetime
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
    created_at: datetime
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
    created_at: datetime
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
        created_at=event.created_at,
        replayed=replayed,
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
        "created_at": event.created_at,
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
    except EventPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.event.persistence_unavailable",
            category="service",
            title="Event unavailable",
            detail="The Event and Schedule could not be persisted atomically.",
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
        raise ProblemError(
            status=404,
            code="temporal.event.not_found",
            category="not_found",
            title="Event not found",
            detail="No Event is available at that reference in the current self scope.",
            retryable=False,
        )
    return _event_response(event)