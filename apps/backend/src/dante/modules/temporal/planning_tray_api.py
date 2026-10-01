"""Authenticated product API for the unified Activity/Event planning tray."""

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
    ActivityNotFoundError,
    ActivityOperationIdReuseError,
    ActivityPersistenceError,
)
from dante.modules.temporal.event import (
    EventInputError,
    EventNotFoundError,
    EventOperationIdReuseError,
    EventPersistenceError,
    EventReplanConflictError,
)
from dante.modules.temporal.planning_tray import (
    PlanningTrayItemNotFoundError,
    PlanningTrayPersistenceError,
    TemporalPlanningTrayApplication,
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
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/planning-tray", tags=["temporal"])
DanteContextDependency = Annotated[DanteContext, Depends(require_dante_context)]
MutatingDanteContextDependency = Annotated[
    DanteContext,
    Depends(require_mutating_dante_context),
]


class PlanningTrayItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["activity", "event"]
    state: Literal["unplaced", "postponed"]
    subject_ref: UUID
    title: str
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    schedule_ref: UUID | None = None


class PlanningTrayDateSpanPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class PlanningTrayFloatingPlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["floating_local_interval"] = "floating_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime


class PlanningTrayNamedZonePlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["named_zone_local_interval"] = "named_zone_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str = Field(min_length=1, max_length=200)
    disambiguation: Literal["reject", "earlier", "later"] = "reject"


class PlanningTrayAbsolutePlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["absolute_interval"] = "absolute_interval"
    starts_at: datetime
    ends_at: datetime


class PlanningTrayCoarsePlacementRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


PlanningTrayPlacementRequest = Annotated[
    PlanningTrayDateSpanPlacementRequest
    | PlanningTrayFloatingPlacementRequest
    | PlanningTrayNamedZonePlacementRequest
    | PlanningTrayAbsolutePlacementRequest
    | PlanningTrayCoarsePlacementRequest,
    Field(discriminator="kind"),
]


class PlacePlanningTrayItemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    placement: PlanningTrayPlacementRequest


class PlacePlanningTrayItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["activity", "event"]
    subject_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    replayed: bool = False


def get_planning_tray_application(request: Request) -> TemporalPlanningTrayApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalPlanningTrayApplication(database_runtime.session_factory)


PlanningTrayApplicationDependency = Annotated[
    TemporalPlanningTrayApplication,
    Depends(get_planning_tray_application),
]


def _placement(payload: PlanningTrayPlacementRequest) -> SchedulePlacement:
    if isinstance(payload, PlanningTrayDateSpanPlacementRequest):
        return DateSpanPlacement(
            start_date=payload.start_date,
            end_date_exclusive=payload.end_date_exclusive,
        )
    if isinstance(payload, PlanningTrayFloatingPlacementRequest):
        return FloatingLocalIntervalPlacement(
            starts_local_at=payload.starts_local_at,
            ends_local_at=payload.ends_local_at,
        )
    if isinstance(payload, PlanningTrayNamedZonePlacementRequest):
        return NamedZoneLocalIntervalPlacement(
            starts_local_at=payload.starts_local_at,
            ends_local_at=payload.ends_local_at,
            zone_id=payload.zone_id,
            disambiguation=payload.disambiguation,
        )
    if isinstance(payload, PlanningTrayAbsolutePlacementRequest):
        return AbsoluteIntervalPlacement(
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
        )
    return CoarseLocalPeriodPlacement(
        local_date=payload.local_date,
        period=payload.period,
    )


@router.get("", response_model=list[PlanningTrayItemResponse], operation_id="temporal_list_planning_tray")
async def list_planning_tray(
    context: DanteContextDependency,
    application: PlanningTrayApplicationDependency,
    response: Response,
) -> list[PlanningTrayItemResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        items = await application.list_items(self_person_ref=context.self_person_ref)
    except PlanningTrayPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.planning_tray.read_unavailable",
            category="service",
            title="Planning tray unavailable",
            detail="Da collocare could not be read safely.",
            retryable=True,
        ) from exc
    return [
        PlanningTrayItemResponse(
            kind=item.kind,
            state=item.state,
            subject_ref=item.subject_ref,
            title=item.title,
            created_at=item.created_at,
            life_area_ref=item.life_area_ref,
            life_area_assignment_revision=item.life_area_assignment_revision,
            schedule_ref=item.schedule_ref,
        )
        for item in items
    ]


@router.post(
    "/{kind}/{subject_ref}/place",
    response_model=PlacePlanningTrayItemResponse,
    operation_id="temporal_place_planning_tray_item",
)
async def place_planning_tray_item(
    kind: Literal["activity", "event"],
    subject_ref: UUID,
    payload: PlacePlanningTrayItemRequest,
    context: MutatingDanteContextDependency,
    application: PlanningTrayApplicationDependency,
    response: Response,
) -> PlacePlanningTrayItemResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.place_item(
            self_person_ref=context.self_person_ref,
            kind=kind,
            subject_ref=NativeRef(subject_ref),
            operation_id=payload.operation_id,
            placement=_placement(payload.placement),
        )
    except (ActivityInputError, EventInputError, ScheduleInputError) as exc:
        raise ProblemError(
            status=422,
            code="temporal.planning_tray.invalid_placement",
            category="validation",
            title="Invalid placement",
            detail=str(exc),
            retryable=False,
        ) from exc
    except (
        PlanningTrayItemNotFoundError,
        ActivityNotFoundError,
        EventNotFoundError,
        ScheduleNotFoundError,
    ) as exc:
        raise ProblemError(
            status=404,
            code="temporal.planning_tray.item_not_found",
            category="not_found",
            title="Planning item not found",
            detail="The item is no longer available in Da collocare.",
            retryable=False,
        ) from exc
    except (
        ActivityOperationIdReuseError,
        EventOperationIdReuseError,
        ScheduleOperationIdReuseError,
        EventReplanConflictError,
    ) as exc:
        raise ProblemError(
            status=409,
            code="temporal.planning_tray.conflict",
            category="conflict",
            title="Planning item changed",
            detail="The item changed while it was being placed. Refresh and retry.",
            retryable=False,
        ) from exc
    except (
        PlanningTrayPersistenceError,
        ActivityPersistenceError,
        EventPersistenceError,
        SchedulePersistenceError,
    ) as exc:
        raise ProblemError(
            status=503,
            code="temporal.planning_tray.persistence_unavailable",
            category="service",
            title="Planning tray unavailable",
            detail="The placement could not be persisted safely.",
            retryable=True,
        ) from exc

    return PlacePlanningTrayItemResponse(
        kind=result.kind,
        subject_ref=result.subject_ref,
        schedule_ref=result.schedule_ref,
        placement_material_state_ref=result.placement_material_state_ref,
        replayed=result.replayed,
    )
