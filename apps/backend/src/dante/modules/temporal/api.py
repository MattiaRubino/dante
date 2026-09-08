"""Authenticated public API for the temporal-operational vertical."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.activity import (
    ActivityInputError,
    ActivityOperationIdReuseError,
    ActivityPersistenceError,
    ActivityView,
    TemporalActivityApplication,
)
from dante.modules.temporal.application import TemporalTimelineApplication
from dante.modules.temporal.contracts import TimelineWindowQuery, TimelineWindowValidationError
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
DanteContextDependency = Annotated[DanteContext, Depends(require_dante_context)]
MutatingDanteContextDependency = Annotated[
    DanteContext,
    Depends(require_mutating_dante_context),
]
_TIMELINE_APPLICATION = TemporalTimelineApplication()


class TimelineWindowResponse(BaseModel):
    """B00 transport contract for a truthful empty authenticated Timeline window."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["empty"] = "empty"
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str


class CreateActivityRequest(BaseModel):
    """Minimum B01 CreateActivity command; placement and lifecycle state are not Activity fields."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)


class ActivityResponse(BaseModel):
    """Minimum canonical Activity representation exposed by B01."""

    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    replayed: bool = False


class UnplacedActivitiesResponse(BaseModel):
    """Planning-Tray read surface for Activities without a Schedule in B01."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["unplaced"] = "unplaced"
    items: list[ActivityResponse]


def get_temporal_activity_application(request: Request) -> TemporalActivityApplication:
    """Resolve the Activity application boundary from the process-scoped DB runtime."""
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalActivityApplication(database_runtime.session_factory)


TemporalActivityApplicationDependency = Annotated[
    TemporalActivityApplication,
    Depends(get_temporal_activity_application),
]


def _activity_response(activity: ActivityView, *, replayed: bool = False) -> ActivityResponse:
    return ActivityResponse(
        activity_ref=activity.activity_ref,
        title=activity.title,
        created_at=activity.created_at,
        replayed=replayed,
    )


@router.get("/timeline/window", response_model=TimelineWindowResponse)
async def get_timeline_window(
    context: DanteContextDependency,
    response: Response,
    start_date: date,
    end_date_exclusive: date,
) -> TimelineWindowResponse:
    """Read one bounded half-open local-date Timeline window for the authenticated self."""
    response.headers["Cache-Control"] = "no-store"

    try:
        query = TimelineWindowQuery(
            start_date=start_date,
            end_date_exclusive=end_date_exclusive,
        )
    except TimelineWindowValidationError as exc:
        raise ProblemError(
            status=400,
            code="temporal.invalid_timeline_window",
            category="validation",
            title="Invalid Timeline window",
            detail=str(exc),
            retryable=False,
        ) from exc

    result = _TIMELINE_APPLICATION.read_window(query=query, context=context)
    return TimelineWindowResponse(
        start_date=result.start_date,
        end_date_exclusive=result.end_date_exclusive,
        effective_zone_id=result.effective_zone_id,
    )


@router.post(
    "/activities",
    response_model=ActivityResponse,
    status_code=201,
)
async def create_activity(
    payload: CreateActivityRequest,
    context: MutatingDanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ActivityResponse:
    """Create one canonical unscheduled Activity for the authenticated self Person."""
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create_activity(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
        )
    except ActivityInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.activity.invalid_create",
            category="validation",
            title="Invalid Activity",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ActivityOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.activity.operation_id_reused",
            category="conflict",
            title="Activity operation conflict",
            detail="The operation id was already used for a different Activity intent.",
            retryable=False,
        ) from exc
    except ActivityPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity.persistence_unavailable",
            category="service",
            title="Activity unavailable",
            detail="The Activity could not be persisted safely.",
            retryable=True,
        ) from exc

    if result.replayed:
        response.status_code = 200
    return _activity_response(result.activity, replayed=result.replayed)


@router.get("/activities/unplaced", response_model=UnplacedActivitiesResponse)
async def list_unplaced_activities(
    context: DanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> UnplacedActivitiesResponse:
    """List canonical Activities for this self Person that have no Schedule yet."""
    response.headers["Cache-Control"] = "no-store"
    try:
        activities = await application.list_unplaced(
            self_person_ref=context.self_person_ref,
        )
    except ActivityPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity.read_unavailable",
            category="service",
            title="Activities unavailable",
            detail="Unplaced Activities could not be read safely.",
            retryable=True,
        ) from exc

    return UnplacedActivitiesResponse(
        items=[_activity_response(activity) for activity in activities]
    )


@router.get("/activities/{activity_ref}", response_model=ActivityResponse)
async def get_activity(
    activity_ref: UUID,
    context: DanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ActivityResponse:
    """Read one canonical Activity only inside the authenticated self scope."""
    response.headers["Cache-Control"] = "no-store"
    try:
        activity = await application.get_activity(
            self_person_ref=context.self_person_ref,
            activity_ref=NativeRef(activity_ref),
        )
    except ActivityPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity.read_unavailable",
            category="service",
            title="Activity unavailable",
            detail="The Activity could not be read safely.",
            retryable=True,
        ) from exc

    if activity is None:
        raise ProblemError(
            status=404,
            code="temporal.activity.not_found",
            category="not_found",
            title="Activity not found",
            detail="No Activity is available at that reference in the current self scope.",
            retryable=False,
        )
    return _activity_response(activity)
