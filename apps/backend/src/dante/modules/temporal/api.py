"""Authenticated public API for the temporal-operational vertical."""

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
    TimelineAbsoluteActivityItem,
    TimelineAbsoluteEventItem,
    TimelineCoarseLocalPeriodActivityItem,
    TimelineCoarseLocalPeriodEventItem,
    TimelineDateSpanActivityItem,
    TimelineDateSpanEventItem,
    TimelineFloatingLocalActivityItem,
    TimelineFloatingLocalEventItem,
    TimelineNamedZoneLocalActivityItem,
    TimelineNamedZoneLocalEventItem,
    TimelinePersistenceError,
    TimelineScheduledActivityItem,
    TimelineScheduledEventItem,
    TimelineScheduledItem,
)
from dante.modules.temporal.contracts import (
    TimelineWindowQuery,
    TimelineWindowValidationError,
)
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    CoarseLocalPeriodPlacement,
    DateSpanPlacement,
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    RestoredScheduleView,
    RevisedScheduleView,
    ScheduleInputError,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    SchedulePersistenceError,
    SchedulePlacement,
    ScheduleRevisionConflictError,
    ScheduleUndoConflictError,
    ScheduleUnscheduleConflictError,
    TemporalScheduleApplication,
    UnscheduledScheduleView,
)
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
LocalDateTimeText = Annotated[
    str,
    Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?$",
        examples=["2026-03-29T01:50:00"],
    ),
]


class TimelineWindowEmptyResponse(BaseModel):
    """Truthful authenticated Timeline window with no activated current items."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["empty"] = "empty"
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str


class TimelineScheduledActivityResponse(BaseModel):
    """Current accepted floating-local Schedule projection for one Activity."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_activity"] = "scheduled_activity"
    activity_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: LocalDateTimeText
    ends_local_at: LocalDateTimeText


class TimelineDateSpanActivityResponse(BaseModel):
    """Current accepted half-open civil-date Activity Schedule projection."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_activity"] = "scheduled_activity"
    activity_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class TimelineNamedZoneLocalActivityResponse(BaseModel):
    """Current named-zone Activity intent and viewing projection."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_activity"] = "scheduled_activity"
    activity_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["named_zone_local"] = "named_zone_local"
    starts_local_at: LocalDateTimeText
    ends_local_at: LocalDateTimeText
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime
    display_starts_local_at: LocalDateTimeText
    display_ends_local_at: LocalDateTimeText


class TimelineAbsoluteActivityResponse(BaseModel):
    """Current absolute Activity Schedule plus request-zone projection."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_activity"] = "scheduled_activity"
    activity_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime
    display_starts_local_at: LocalDateTimeText
    display_ends_local_at: LocalDateTimeText


class TimelineCoarseLocalPeriodActivityResponse(BaseModel):
    """Current coarse Activity placement with no manufactured clock boundaries."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_activity"] = "scheduled_activity"
    activity_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


TimelineScheduledActivityItemResponse = Annotated[
    TimelineScheduledActivityResponse
    | TimelineDateSpanActivityResponse
    | TimelineNamedZoneLocalActivityResponse
    | TimelineAbsoluteActivityResponse
    | TimelineCoarseLocalPeriodActivityResponse,
    Field(discriminator="temporal_form"),
]


class TimelineScheduledEventResponse(BaseModel):
    """Current accepted floating-local Schedule projection for one Event."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_event"] = "scheduled_event"
    event_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: LocalDateTimeText
    ends_local_at: LocalDateTimeText


class TimelineDateSpanEventResponse(BaseModel):
    """Current accepted half-open civil-date Event Schedule projection."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_event"] = "scheduled_event"
    event_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class TimelineNamedZoneLocalEventResponse(BaseModel):
    """Current named-zone Event intent and viewing projection."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_event"] = "scheduled_event"
    event_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["named_zone_local"] = "named_zone_local"
    starts_local_at: LocalDateTimeText
    ends_local_at: LocalDateTimeText
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime
    display_starts_local_at: LocalDateTimeText
    display_ends_local_at: LocalDateTimeText


class TimelineAbsoluteEventResponse(BaseModel):
    """Current absolute Event Schedule plus request-zone projection."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_event"] = "scheduled_event"
    event_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime
    display_starts_local_at: LocalDateTimeText
    display_ends_local_at: LocalDateTimeText


class TimelineCoarseLocalPeriodEventResponse(BaseModel):
    """Current coarse Event placement with no manufactured clock boundaries."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["scheduled_event"] = "scheduled_event"
    event_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    title: str
    temporal_form: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


TimelineScheduledEventItemResponse = Annotated[
    TimelineScheduledEventResponse
    | TimelineDateSpanEventResponse
    | TimelineNamedZoneLocalEventResponse
    | TimelineAbsoluteEventResponse
    | TimelineCoarseLocalPeriodEventResponse,
    Field(discriminator="temporal_form"),
]

TimelineScheduledItemResponse = (
    TimelineScheduledActivityItemResponse | TimelineScheduledEventItemResponse
)


class TimelineWindowItemsResponse(BaseModel):
    """Populated authenticated Timeline window."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["window"] = "window"
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    items: list[TimelineScheduledItemResponse]


TimelineWindowResponse = TimelineWindowEmptyResponse | TimelineWindowItemsResponse


class CreateActivityRequest(BaseModel):
    """Minimum B01 CreateActivity command; placement is not an Activity field."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)


class DateSpanPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class FloatingLocalIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["floating_local_interval"] = "floating_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime


class NamedZoneLocalIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["named_zone_local_interval"] = "named_zone_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str = Field(min_length=1, max_length=200)
    disambiguation: Literal["reject", "earlier", "later"] = "reject"


class AbsoluteIntervalPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["absolute_interval"] = "absolute_interval"
    starts_at: datetime
    ends_at: datetime


class CoarseLocalPeriodPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


SchedulePlacementRequest = Annotated[
    DateSpanPlacementRequest
    | FloatingLocalIntervalPlacementRequest
    | NamedZoneLocalIntervalPlacementRequest
    | AbsoluteIntervalPlacementRequest
    | CoarseLocalPeriodPlacementRequest,
    Field(discriminator="kind"),
]


class CreateScheduledActivityRequest(BaseModel):
    """Atomic Activity + accepted Schedule authoring command."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    placement: SchedulePlacementRequest


class EstablishActivityScheduleRequest(BaseModel):
    """Attach one accepted Schedule to an existing canonical Activity."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    placement: SchedulePlacementRequest


class ReviseScheduleRequest(BaseModel):
    """Revise one current Schedule from an exact accepted placement basis."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_placement_material_state_ref: UUID
    placement: SchedulePlacementRequest


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


class ScheduledActivityDateSpanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date
    replayed: bool = False


class ScheduledActivityNamedZoneResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
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


class ScheduledActivityAbsoluteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime
    replayed: bool = False


class ScheduledActivityCoarseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    schedule_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]
    replayed: bool = False


ScheduledActivityMutationResponse = Annotated[
    ScheduledActivityResponse
    | ScheduledActivityDateSpanResponse
    | ScheduledActivityNamedZoneResponse
    | ScheduledActivityAbsoluteResponse
    | ScheduledActivityCoarseResponse,
    Field(discriminator="temporal_form"),
]


class RevisedScheduleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime
    replayed: bool = False


class RevisedScheduleDateSpanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date
    replayed: bool = False


class RevisedScheduleNamedZoneResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["named_zone_local"] = "named_zone_local"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime
    replayed: bool = False


class RevisedScheduleAbsoluteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime
    replayed: bool = False


class RevisedScheduleCoarseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]
    replayed: bool = False


RevisedScheduleMutationResponse = Annotated[
    RevisedScheduleResponse
    | RevisedScheduleDateSpanResponse
    | RevisedScheduleNamedZoneResponse
    | RevisedScheduleAbsoluteResponse
    | RevisedScheduleCoarseResponse,
    Field(discriminator="temporal_form"),
]


class UnscheduledScheduleResponse(BaseModel):
    """Accepted withdrawal of the current Schedule placement."""

    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    previous_placement_material_state_ref: UUID
    unschedule_operation_id: str
    replayed: bool = False


class RestoredScheduleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    restored_from_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["floating_local"] = "floating_local"
    starts_local_at: datetime
    ends_local_at: datetime
    replayed: bool = False


class RestoredScheduleDateSpanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    restored_from_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date
    replayed: bool = False


class RestoredScheduleNamedZoneResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    restored_from_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["named_zone_local"] = "named_zone_local"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime
    replayed: bool = False


class RestoredScheduleAbsoluteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    restored_from_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["absolute"] = "absolute"
    starts_at: datetime
    ends_at: datetime
    replayed: bool = False


class RestoredScheduleCoarseResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    restored_from_placement_material_state_ref: UUID
    placement_material_state_ref: UUID
    temporal_form: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]
    replayed: bool = False


RestoredScheduleMutationResponse = Annotated[
    RestoredScheduleResponse
    | RestoredScheduleDateSpanResponse
    | RestoredScheduleNamedZoneResponse
    | RestoredScheduleAbsoluteResponse
    | RestoredScheduleCoarseResponse,
    Field(discriminator="temporal_form"),
]


class UnplacedActivitiesResponse(BaseModel):
    """Planning-Tray Activities without a current accepted Schedule placement."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["unplaced"] = "unplaced"
    items: list[ActivityResponse]


def get_temporal_activity_application(request: Request) -> TemporalActivityApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalActivityApplication(database_runtime.session_factory)


def get_temporal_timeline_application(request: Request) -> TemporalTimelineApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalTimelineApplication(database_runtime.session_factory)


def get_temporal_schedule_application(request: Request) -> TemporalScheduleApplication:
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


def _activity_response(activity: ActivityView, *, replayed: bool = False) -> ActivityResponse:
    return ActivityResponse(
        activity_ref=activity.activity_ref,
        title=activity.title,
        created_at=activity.created_at,
        replayed=replayed,
    )


def _local_datetime_text(value: datetime) -> str:
    return value.isoformat()


def _timeline_activity_item_response(
    item: TimelineScheduledActivityItem,
) -> TimelineScheduledActivityItemResponse:
    common: dict[str, Any] = {
        "activity_ref": item.activity_ref,
        "schedule_ref": item.schedule_ref,
        "placement_material_state_ref": item.placement_material_state_ref,
        "title": item.title,
    }
    if isinstance(item, TimelineFloatingLocalActivityItem):
        return TimelineScheduledActivityResponse(
            **common,
            starts_local_at=_local_datetime_text(item.starts_local_at),
            ends_local_at=_local_datetime_text(item.ends_local_at),
        )
    if isinstance(item, TimelineDateSpanActivityItem):
        return TimelineDateSpanActivityResponse(
            **common,
            start_date=item.start_date,
            end_date_exclusive=item.end_date_exclusive,
        )
    if isinstance(item, TimelineNamedZoneLocalActivityItem):
        return TimelineNamedZoneLocalActivityResponse(
            **common,
            starts_local_at=_local_datetime_text(item.starts_local_at),
            ends_local_at=_local_datetime_text(item.ends_local_at),
            zone_id=item.zone_id,
            resolved_start_at=item.resolved_start_at,
            resolved_end_at=item.resolved_end_at,
            display_starts_local_at=_local_datetime_text(item.display_starts_local_at),
            display_ends_local_at=_local_datetime_text(item.display_ends_local_at),
        )
    if isinstance(item, TimelineAbsoluteActivityItem):
        return TimelineAbsoluteActivityResponse(
            **common,
            starts_at=item.starts_at,
            ends_at=item.ends_at,
            display_starts_local_at=_local_datetime_text(item.display_starts_local_at),
            display_ends_local_at=_local_datetime_text(item.display_ends_local_at),
        )
    if isinstance(item, TimelineCoarseLocalPeriodActivityItem):
        return TimelineCoarseLocalPeriodActivityResponse(
            **common,
            local_date=item.local_date,
            period=item.period,
        )
    raise TypeError("Unsupported Activity Timeline item")


def _timeline_event_item_response(
    item: TimelineScheduledEventItem,
) -> TimelineScheduledEventItemResponse:
    common: dict[str, Any] = {
        "event_ref": item.event_ref,
        "schedule_ref": item.schedule_ref,
        "placement_material_state_ref": item.placement_material_state_ref,
        "title": item.title,
    }
    if isinstance(item, TimelineFloatingLocalEventItem):
        return TimelineScheduledEventResponse(
            **common,
            starts_local_at=_local_datetime_text(item.starts_local_at),
            ends_local_at=_local_datetime_text(item.ends_local_at),
        )
    if isinstance(item, TimelineDateSpanEventItem):
        return TimelineDateSpanEventResponse(
            **common,
            start_date=item.start_date,
            end_date_exclusive=item.end_date_exclusive,
        )
    if isinstance(item, TimelineNamedZoneLocalEventItem):
        return TimelineNamedZoneLocalEventResponse(
            **common,
            starts_local_at=_local_datetime_text(item.starts_local_at),
            ends_local_at=_local_datetime_text(item.ends_local_at),
            zone_id=item.zone_id,
            resolved_start_at=item.resolved_start_at,
            resolved_end_at=item.resolved_end_at,
            display_starts_local_at=_local_datetime_text(item.display_starts_local_at),
            display_ends_local_at=_local_datetime_text(item.display_ends_local_at),
        )
    if isinstance(item, TimelineAbsoluteEventItem):
        return TimelineAbsoluteEventResponse(
            **common,
            starts_at=item.starts_at,
            ends_at=item.ends_at,
            display_starts_local_at=_local_datetime_text(item.display_starts_local_at),
            display_ends_local_at=_local_datetime_text(item.display_ends_local_at),
        )
    if isinstance(item, TimelineCoarseLocalPeriodEventItem):
        return TimelineCoarseLocalPeriodEventResponse(
            **common,
            local_date=item.local_date,
            period=item.period,
        )
    raise TypeError("Unsupported Event Timeline item")


def _timeline_item_response(item: TimelineScheduledItem) -> TimelineScheduledItemResponse:
    if isinstance(
        item,
        (
            TimelineFloatingLocalEventItem,
            TimelineDateSpanEventItem,
            TimelineNamedZoneLocalEventItem,
            TimelineAbsoluteEventItem,
            TimelineCoarseLocalPeriodEventItem,
        ),
    ):
        return _timeline_event_item_response(item)
    return _timeline_activity_item_response(cast(TimelineScheduledActivityItem, item))


def _placement_from_request(payload: SchedulePlacementRequest) -> SchedulePlacement:
    if isinstance(payload, DateSpanPlacementRequest):
        return DateSpanPlacement(
            start_date=payload.start_date,
            end_date_exclusive=payload.end_date_exclusive,
        )
    if isinstance(payload, FloatingLocalIntervalPlacementRequest):
        return FloatingLocalIntervalPlacement(
            starts_local_at=payload.starts_local_at,
            ends_local_at=payload.ends_local_at,
        )
    if isinstance(payload, NamedZoneLocalIntervalPlacementRequest):
        return NamedZoneLocalIntervalPlacement(
            starts_local_at=payload.starts_local_at,
            ends_local_at=payload.ends_local_at,
            zone_id=payload.zone_id,
            disambiguation=payload.disambiguation,
        )
    if isinstance(payload, AbsoluteIntervalPlacementRequest):
        return AbsoluteIntervalPlacement(
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
        )
    return CoarseLocalPeriodPlacement(
        local_date=payload.local_date,
        period=payload.period,
    )


def _scheduled_activity_response(
    *,
    activity: ActivityView,
    schedule_ref: UUID,
    material_state_ref: UUID,
    placement: SchedulePlacement,
    replayed: bool,
) -> ScheduledActivityMutationResponse:
    common: dict[str, Any] = {
        "activity_ref": activity.activity_ref,
        "title": activity.title,
        "created_at": activity.created_at,
        "schedule_ref": schedule_ref,
        "placement_material_state_ref": material_state_ref,
        "replayed": replayed,
    }
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return ScheduledActivityResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
        )
    if isinstance(placement, DateSpanPlacement):
        return ScheduledActivityDateSpanResponse(
            **common,
            start_date=placement.start_date,
            end_date_exclusive=placement.end_date_exclusive,
        )
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        return ScheduledActivityNamedZoneResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
            zone_id=placement.zone_id,
            resolved_start_at=cast(datetime, placement.resolved_start_at),
            resolved_end_at=cast(datetime, placement.resolved_end_at),
        )
    if isinstance(placement, AbsoluteIntervalPlacement):
        return ScheduledActivityAbsoluteResponse(
            **common,
            starts_at=placement.starts_at,
            ends_at=placement.ends_at,
        )
    return ScheduledActivityCoarseResponse(
        **common,
        local_date=placement.local_date,
        period=placement.period,
    )


def _revised_schedule_response(result: RevisedScheduleView) -> RevisedScheduleMutationResponse:
    common: dict[str, Any] = {
        "schedule_ref": result.schedule_ref,
        "previous_placement_material_state_ref": result.previous_material_state_ref,
        "placement_material_state_ref": result.material_state_ref,
        "replayed": result.replayed,
    }
    placement = result.placement
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return RevisedScheduleResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
        )
    if isinstance(placement, DateSpanPlacement):
        return RevisedScheduleDateSpanResponse(
            **common,
            start_date=placement.start_date,
            end_date_exclusive=placement.end_date_exclusive,
        )
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        return RevisedScheduleNamedZoneResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
            zone_id=placement.zone_id,
            resolved_start_at=cast(datetime, placement.resolved_start_at),
            resolved_end_at=cast(datetime, placement.resolved_end_at),
        )
    if isinstance(placement, AbsoluteIntervalPlacement):
        return RevisedScheduleAbsoluteResponse(
            **common,
            starts_at=placement.starts_at,
            ends_at=placement.ends_at,
        )
    return RevisedScheduleCoarseResponse(
        **common,
        local_date=placement.local_date,
        period=placement.period,
    )


def _restored_schedule_response(
    result: RestoredScheduleView,
) -> RestoredScheduleMutationResponse:
    common: dict[str, Any] = {
        "schedule_ref": result.schedule_ref,
        "restored_from_placement_material_state_ref": result.restored_from_material_state_ref,
        "placement_material_state_ref": result.material_state_ref,
        "replayed": result.replayed,
    }
    placement = result.placement
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return RestoredScheduleResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
        )
    if isinstance(placement, DateSpanPlacement):
        return RestoredScheduleDateSpanResponse(
            **common,
            start_date=placement.start_date,
            end_date_exclusive=placement.end_date_exclusive,
        )
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        return RestoredScheduleNamedZoneResponse(
            **common,
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
            zone_id=placement.zone_id,
            resolved_start_at=cast(datetime, placement.resolved_start_at),
            resolved_end_at=cast(datetime, placement.resolved_end_at),
        )
    if isinstance(placement, AbsoluteIntervalPlacement):
        return RestoredScheduleAbsoluteResponse(
            **common,
            starts_at=placement.starts_at,
            ends_at=placement.ends_at,
        )
    return RestoredScheduleCoarseResponse(
        **common,
        local_date=placement.local_date,
        period=placement.period,
    )


@router.get("/timeline/window", response_model=TimelineWindowResponse)
async def get_timeline_window(
    context: DanteContextDependency,
    application: TemporalTimelineApplicationDependency,
    response: Response,
    start_date: date,
    end_date_exclusive: date,
) -> TimelineWindowResponse:
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
        items=[_timeline_item_response(item) for item in result.items],
    )


@router.post("/activities", response_model=ActivityResponse, status_code=201)
async def create_activity(
    payload: CreateActivityRequest,
    context: MutatingDanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ActivityResponse:
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
    response_model=ScheduledActivityMutationResponse,
    status_code=201,
)
async def create_scheduled_activity(
    payload: CreateScheduledActivityRequest,
    context: MutatingDanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ScheduledActivityMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        placement = _placement_from_request(payload.placement)
        result = await application.create_activity_with_schedule(
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
    return _scheduled_activity_response(
        activity=result.activity,
        schedule_ref=result.schedule.schedule_ref,
        material_state_ref=result.schedule.material_state_ref,
        placement=result.schedule.placement,
        replayed=result.replayed,
    )


@router.post(
    "/activities/{activity_ref}/schedule",
    response_model=ScheduledActivityMutationResponse,
    status_code=201,
)
async def establish_activity_schedule(
    activity_ref: UUID,
    payload: EstablishActivityScheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> ScheduledActivityMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        placement = _placement_from_request(payload.placement)
        result = await application.schedule_existing_activity_with_placement(
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
    return _scheduled_activity_response(
        activity=result.activity,
        schedule_ref=result.schedule.schedule_ref,
        material_state_ref=result.schedule.material_state_ref,
        placement=result.schedule.placement,
        replayed=result.replayed,
    )


@router.patch(
    "/schedules/{schedule_ref}/placement",
    response_model=RevisedScheduleMutationResponse,
)
async def revise_schedule_placement(
    schedule_ref: UUID,
    payload: ReviseScheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalScheduleApplicationDependency,
    response: Response,
) -> RevisedScheduleMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.revise_schedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            schedule_ref=ScopedRecordRef(schedule_ref),
            expected_material_state_ref=MaterialStateRef(
                payload.expected_placement_material_state_ref
            ),
            placement=_placement_from_request(payload.placement),
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
    return _revised_schedule_response(result)


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
    response_model=RestoredScheduleMutationResponse,
)
async def undo_schedule_unschedule(
    schedule_ref: UUID,
    payload: UndoScheduleUnscheduleRequest,
    context: MutatingDanteContextDependency,
    application: TemporalScheduleApplicationDependency,
    response: Response,
) -> RestoredScheduleMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.undo_unschedule(
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
    return _restored_schedule_response(result)


@router.get("/activities/unplaced", response_model=UnplacedActivitiesResponse)
async def list_unplaced_activities(
    context: DanteContextDependency,
    application: TemporalActivityApplicationDependency,
    response: Response,
) -> UnplacedActivitiesResponse:
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
