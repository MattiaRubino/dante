"""Authenticated public API for the temporal-operational vertical."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from dante.context.contracts import DanteContext
from dante.context.dependencies import (
    require_dante_context,
    require_mutating_dante_context,
)
from dante.modules.temporal.activity import (
    ActivityInputError,
    ActivityNotFoundError,
    ActivityOperationIdReuseError,
    ActivityPersistenceError,
    ActivityView,
    TemporalActivityApplication,
)
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelinePersistenceError,
)
from dante.modules.temporal.contracts import (
    TimelineWindowQuery,
    TimelineWindowValidationError,
)
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    RestoredScheduleView,
    RevisedScheduleView,
    ScheduleInputError,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    SchedulePersistenceError,
    ScheduleRevisionConflictError,
    ScheduleUndoConflictError,
    ScheduleUnscheduleConflictError,
    TemporalScheduleApplication,
    UnscheduledScheduleView,
)
from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
)
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
DanteContextDependency = Annotated[DanteContext, Depends(require_dante_context)]
MutatingDanteContextDependency = Annotated[
    DanteContext,
    Depends(require_mutating_dante_context),
]

class TimelineWindowEmptyResponse(BaseModel):
    """Truthful authenticated Timeline window with no activated current items."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["empty"] = "empty"
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str

class TimelineScheduledActivityResponse(BaseModel):
    """Current accepted B02-A Schedule projection for one Activity."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_activity"] = "scheduled_activity"
    activity_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime

class TimelineWindowItemsResponse(BaseModel):
    """Populated authenticated Timeline window."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["window"] = "window"
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    items: list[TimelineScheduledActivityResponse]

TimelineWindowResponse = TimelineWindowEmptyResponse | TimelineWindowItemsResponse

class CreateActivityRequest(BaseModel):
    """Minimum B01 CreateActivity command; placement is not an Activity field."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)

class FloatingLocalIntervalPlacementRequest(BaseModel):
    """First lossless accepted Schedule transport form activated by B02-A."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["floating_local_interval"] = "floating_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime

class CreateScheduledActivityRequest(BaseModel):
    """Atomic Activity + accepted Schedule authoring command for B02-A."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    placement: FloatingLocalIntervalPlacementRequest

class EstablishActivityScheduleRequest(BaseModel):
    """Attach an accepted Schedule to one existing canonical Activity."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    placement: FloatingLocalIntervalPlacementRequest

class ReviseFloatingScheduleRequest(BaseModel):
    """Revise one current Schedule from an exact accepted placement basis."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_placement_material_state_ref: UUID
    placement: FloatingLocalIntervalPlacementRequest

class UnscheduleScheduleRequest(BaseModel):
    """Withdraw one exact current accepted Schedule placement."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_placement_material_state_ref: UUID

class UndoScheduleUnscheduleRequest(BaseModel):
    """Restore the placement withdrawn by one exact unschedule operation."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    unschedule_operation_id: str = Field(min_length=1, max_length=200)

class ActivityResponse(BaseModel):
    """Minimum canonical Activity representation exposed by B01."""

    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    replayed: bool = False

class ScheduledActivityResponse(BaseModel):
    """Canonical Activity plus the first accepted Schedule/current placement."""

    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime
    replayed: bool = False

class RevisedScheduleResponse(BaseModel):
    """Accepted current Schedule placement after one governed revision."""

    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime
    replayed: bool = False

class UnscheduledScheduleResponse(BaseModel):
    """Accepted withdrawal of the current Schedule placement."""

    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    unschedule_operation_id: str
    replayed: bool = False

class RestoredScheduleResponse(BaseModel):
    """New current placement produced by guarded Undo of unschedule."""

    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    restored_from_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime
    replayed: bool = False

class UnplacedActivitiesResponse(BaseModel):
    """Planning-Tray Activities without a current accepted Schedule placement."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["unplaced"] = "unplaced"
    items: list[ActivityResponse]

def get_temporal_activity_application(request: Request) -> TemporalActivityApplication:
    """Resolve the Activity application boundary from the process-scoped DB runtime."""
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalActivityApplication(database_runtime.session_factory)

def get_temporal_timeline_application(request: Request) -> TemporalTimelineApplication:
    """Resolve the Timeline application boundary from the process-scoped DB runtime."""
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalTimelineApplication(database_runtime.session_factory)

def get_temporal_schedule_application(request: Request) -> TemporalScheduleApplication:
    """Resolve the Schedule mutation boundary from the process-scoped DB runtime."""
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalScheduleApplication(database_runtime.session_factory)

TemporalActivityApplicationDependency = Annotated[
    TemporalActivityApplication,
    Depends(get_temporal_activity_application),
]
TemporalTimelineApplicationDependency = Annotated[
    TemporalTimelineApplication,
    Depends(get_temporal_timeline_application),
]
TemporalScheduleApplicationDependency = Annotated[
    TemporalScheduleApplication,
    Depends(get_temporal_schedule_application),
]

def _activity_response(
    activity: ActivityView, *, replayed: bool = False
) -> ActivityResponse:
    return ActivityResponse(
        activity_ref=activity.activity_ref,
        title=activity.title,
        created_at=activity.created_at,
        replayed=replayed,
    )

@router.get("/timeline/window", response_model=TimelineWindowResponse)
async def get_timeline_window(
    context: DanteContextDependency,
    application: TemporalTimelineApplicationDependency,
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

    try:
        result = await application.read_window(query=query, context=context)
    except TimelinePersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.timeline.read_unavailable",
            category="service",
            title="Timeline unavailable",
            detail="The Timeline could not be read safely.",
            retryable=True,
        ) from exc

    if not result.items:
        return TimelineWindowEmptyResponse(
            start_date=result.start_date,
            end_date_exclusive=result.end_date_exclusive,
            effective_zone_id=result.effective_zone_id,
        )

    return TimelineWindowItemsResponse(
        start_date=result.start_date,
        end_date_exclusive=result.end_date_exclusive,
        effective_zone_id=result.effective_zone_id,
        items=[
            TimelineScheduledActivityResponse(
                activity_ref=item.activity_ref,
                schedule_ref=item.schedule_ref,
                placement_material_state_ref=item.placement_material_state_ref,
                title=item.title,
                starts_local_at=item.starts_local_at,
                ends_local_at=item.ends_local_at,
            )
            for item in result.items
        ],
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

@router.post(
    "/activities/scheduled",
    response_model=ScheduledActivityResponse,
    status_code=201,
)
async def create_scheduled_activity(
    payload: CreateScheduledActivityRequest,
    context: MutatingDanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ScheduledActivityResponse:
    """Create Activity + first accepted Schedule atomically for the B02-A subset."""
    response.headers["Cache-Control"] = "no-store"
    try:
        placement = FloatingLocalIntervalPlacement(
            starts_local_at=payload.placement.starts_local_at,
            ends_local_at=payload.placement.ends_local_at,
        )
        result = await application.create_activity_with_floating_schedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            placement=placement,
        )
    except (ActivityInputError, ScheduleInputError) as exc:
        raise ProblemError(
            status=422,
            code="temporal.schedule.invalid_establish",
            category="validation",
            title="Invalid Schedule",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ActivityOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.operation_id_reused",
            category="conflict",
            title="Schedule operation conflict",
            detail="The operation id was already used for a different temporal intent.",
            retryable=False,
        ) from exc
    except ActivityPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.schedule.persistence_unavailable",
            category="service",
            title="Schedule unavailable",
            detail="The Activity and Schedule could not be persisted atomically.",
            retryable=True,
        ) from exc

    if result.replayed:
        response.status_code = 200
    return ScheduledActivityResponse(
        activity_ref=result.activity.activity_ref,
        title=result.activity.title,
        created_at=result.activity.created_at,
        schedule_ref=result.schedule.schedule_ref,
        placement_material_state_ref=result.schedule.material_state_ref,
        starts_local_at=result.schedule.placement.starts_local_at,
        ends_local_at=result.schedule.placement.ends_local_at,
        replayed=result.replayed,
    )

@router.post(
    "/activities/{activity_ref}/schedule",
    response_model=ScheduledActivityResponse,
    status_code=201,
)
async def establish_activity_schedule(
    activity_ref: UUID,
    payload: EstablishActivityScheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ScheduledActivityResponse:
    """Attach a first accepted Schedule to an existing Activity without cloning it."""
    response.headers["Cache-Control"] = "no-store"
    try:
        placement = FloatingLocalIntervalPlacement(
            starts_local_at=payload.placement.starts_local_at,
            ends_local_at=payload.placement.ends_local_at,
        )
        result = await application.schedule_existing_activity(
            self_person_ref=context.self_person_ref,
            activity_ref=NativeRef(activity_ref),
            operation_id=payload.operation_id,
            placement=placement,
        )
    except (ActivityInputError, ScheduleInputError) as exc:
        raise ProblemError(
            status=422,
            code="temporal.schedule.invalid_establish",
            category="validation",
            title="Invalid Schedule",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ActivityNotFoundError as exc:
        raise ProblemError(
            status=404,
            code="temporal.activity.not_found",
            category="not_found",
            title="Activity not found",
            detail="No Activity is available at that reference in the current self scope.",
            retryable=False,
        ) from exc
    except ActivityOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.operation_id_reused",
            category="conflict",
            title="Schedule operation conflict",
            detail="The operation id was already used for a different temporal intent.",
            retryable=False,
        ) from exc
    except ActivityPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.schedule.persistence_unavailable",
            category="service",
            title="Schedule unavailable",
            detail="The Schedule could not be persisted atomically.",
            retryable=True,
        ) from exc

    if result.replayed:
        response.status_code = 200
    return ScheduledActivityResponse(
        activity_ref=result.activity.activity_ref,
        title=result.activity.title,
        created_at=result.activity.created_at,
        schedule_ref=result.schedule.schedule_ref,
        placement_material_state_ref=result.schedule.material_state_ref,
        starts_local_at=result.schedule.placement.starts_local_at,
        ends_local_at=result.schedule.placement.ends_local_at,
        replayed=result.replayed,
    )

@router.patch(
    "/schedules/{schedule_ref}/placement",
    response_model=RevisedScheduleResponse,
)
async def revise_schedule_placement(
    schedule_ref: UUID,
    payload: ReviseFloatingScheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalScheduleApplicationDependency,
    response: Response,
) -> RevisedScheduleResponse:
    """Create a new accepted placement state without changing Schedule identity."""
    response.headers["Cache-Control"] = "no-store"
    try:
        result: RevisedScheduleView = await application.revise_floating_schedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            schedule_ref=ScopedRecordRef(schedule_ref),
            expected_material_state_ref=MaterialStateRef(
                payload.expected_placement_material_state_ref
            ),
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=payload.placement.starts_local_at,
                ends_local_at=payload.placement.ends_local_at,
            ),
        )
    except ScheduleInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.schedule.invalid_revision",
            category="validation",
            title="Invalid Schedule revision",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ScheduleNotFoundError as exc:
        raise ProblemError(
            status=404,
            code="temporal.schedule.not_found",
            category="not_found",
            title="Schedule not found",
            detail="No current Schedule is available at that reference in the current self scope.",
            retryable=False,
        ) from exc
    except ScheduleOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.operation_id_reused",
            category="conflict",
            title="Schedule operation conflict",
            detail="The operation id was already used for a different Schedule revision.",
            retryable=False,
        ) from exc
    except ScheduleRevisionConflictError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.revision_conflict",
            category="conflict",
            title="Schedule revision conflict",
            detail="The Schedule placement changed after the submitted revision basis.",
            retryable=False,
        ) from exc
    except SchedulePersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.schedule.persistence_unavailable",
            category="service",
            title="Schedule unavailable",
            detail="The Schedule revision could not be persisted safely.",
            retryable=True,
        ) from exc

    return RevisedScheduleResponse(
        schedule_ref=result.schedule_ref,
        previous_placement_material_state_ref=result.previous_material_state_ref,
        placement_material_state_ref=result.material_state_ref,
        starts_local_at=result.placement.starts_local_at,
        ends_local_at=result.placement.ends_local_at,
        replayed=result.replayed,
    )

@router.post(
    "/schedules/{schedule_ref}/unschedule",
    response_model=UnscheduledScheduleResponse,
)
async def unschedule_schedule(
    schedule_ref: UUID,
    payload: UnscheduleScheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalScheduleApplicationDependency,
    response: Response,
) -> UnscheduledScheduleResponse:
    """Withdraw one exact current placement without deleting Schedule history."""
    response.headers["Cache-Control"] = "no-store"
    try:
        result: UnscheduledScheduleView = await application.unschedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            schedule_ref=ScopedRecordRef(schedule_ref),
            expected_material_state_ref=MaterialStateRef(
                payload.expected_placement_material_state_ref
            ),
        )
    except ScheduleInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.schedule.invalid_unschedule",
            category="validation",
            title="Invalid Schedule unschedule",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ScheduleNotFoundError as exc:
        raise ProblemError(
            status=404,
            code="temporal.schedule.not_found",
            category="not_found",
            title="Schedule not found",
            detail="No Schedule is available at that reference in the current self scope.",
            retryable=False,
        ) from exc
    except ScheduleOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.operation_id_reused",
            category="conflict",
            title="Schedule operation conflict",
            detail="The operation id was already used for a different unschedule intent.",
            retryable=False,
        ) from exc
    except ScheduleUnscheduleConflictError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.unschedule_conflict",
            category="conflict",
            title="Schedule unschedule conflict",
            detail="The Schedule placement changed after the submitted unschedule basis.",
            retryable=False,
        ) from exc
    except SchedulePersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.schedule.persistence_unavailable",
            category="service",
            title="Schedule unavailable",
            detail="The Schedule could not be unscheduled safely.",
            retryable=True,
        ) from exc

    return UnscheduledScheduleResponse(
        schedule_ref=result.schedule_ref,
        previous_placement_material_state_ref=result.previous_material_state_ref,
        unschedule_operation_id=result.unschedule_operation_id,
        replayed=result.replayed,
    )

@router.post(
    "/schedules/{schedule_ref}/unschedule/undo",
    response_model=RestoredScheduleResponse,
)
async def undo_schedule_unschedule(
    schedule_ref: UUID,
    payload: UndoScheduleUnscheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalScheduleApplicationDependency,
    response: Response,
) -> RestoredScheduleResponse:
    """Restore withdrawn placement semantics through one new MaterialState."""
    response.headers["Cache-Control"] = "no-store"
    try:
        result: RestoredScheduleView = await application.undo_unschedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            schedule_ref=ScopedRecordRef(schedule_ref),
            unschedule_operation_id=payload.unschedule_operation_id,
        )
    except ScheduleInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.schedule.invalid_undo",
            category="validation",
            title="Invalid Schedule Undo",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ScheduleNotFoundError as exc:
        raise ProblemError(
            status=404,
            code="temporal.schedule.undo_not_found",
            category="not_found",
            title="Schedule Undo unavailable",
            detail="The Schedule or exact unschedule basis is unavailable in the current self scope.",
            retryable=False,
        ) from exc
    except ScheduleOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.operation_id_reused",
            category="conflict",
            title="Schedule operation conflict",
            detail="The operation id was already used for a different Undo intent.",
            retryable=False,
        ) from exc
    except ScheduleUndoConflictError as exc:
        raise ProblemError(
            status=409,
            code="temporal.schedule.undo_conflict",
            category="conflict",
            title="Schedule Undo conflict",
            detail="Newer Schedule truth prevents this Undo.",
            retryable=False,
        ) from exc
    except SchedulePersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.schedule.persistence_unavailable",
            category="service",
            title="Schedule unavailable",
            detail="The Schedule Undo could not be persisted safely.",
            retryable=True,
        ) from exc

    return RestoredScheduleResponse(
        schedule_ref=result.schedule_ref,
        restored_from_placement_material_state_ref=(
            result.restored_from_material_state_ref
        ),
        placement_material_state_ref=result.material_state_ref,
        starts_local_at=result.placement.starts_local_at,
        ends_local_at=result.placement.ends_local_at,
        replayed=result.replayed,
    )

@router.get("/activities/unplaced", response_model=UnplacedActivitiesResponse)
async def list_unplaced_activities(
    context: DanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> UnplacedActivitiesResponse:
    """List canonical Activities that have no current accepted Schedule placement."""
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
