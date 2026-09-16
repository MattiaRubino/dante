"""Authenticated B03-A API for the minimum Event canonical core."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, cast
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


class EventResponse(BaseModel):
    """Minimum canonical Event expectation representation."""

    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    created_at: datetime
    replayed: bool = False


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
