"""Public B14-U2 Quick Create authoring API.

The historical B01/B03 create endpoints remain available while the product UI
moves to this richer transactional contract.  This endpoint does not invent a
second persistence model: it delegates to TemporalAuthoringApplication and the
same canonical Schedule placement types used by the established temporal API.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_mutating_dante_context
from dante.modules.temporal.api import SchedulePlacementRequest, _placement_from_request
from dante.modules.temporal.authoring import (
    ActivityChildIntent,
    AuthoringLifeAreaIntent,
    AuthoringResult,
    TemporalAuthoringApplication,
    TemporalAuthoringInputError,
    TemporalAuthoringLifeAreaConflictError,
    TemporalAuthoringLifeAreaUnavailableError,
    TemporalAuthoringOperationIdReuseError,
    TemporalAuthoringPersistenceError,
    TemporalAuthoringStructureConflictError,
)
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    CoarseLocalPeriodPlacement,
    DateSpanPlacement,
    EstablishedScheduleView,
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    SchedulePlacement,
)
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/authoring", tags=["temporal"])
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class AuthoringLifeAreaRequest(BaseModel):
    """Select one existing Life Area or request creation of one new area."""

    model_config = ConfigDict(extra="forbid")

    life_area_ref: UUID | None = None
    new_name: str | None = Field(default=None, min_length=1, max_length=100)
    expected_revision: int | None = Field(default=None, ge=1)
    color_code: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")

    @model_validator(mode="after")
    def validate_shape(self) -> AuthoringLifeAreaRequest:
        if self.life_area_ref is not None and self.new_name is not None:
            raise ValueError("Choose an existing Life Area or create a new one, not both.")
        if self.life_area_ref is None and self.new_name is None:
            raise ValueError("Life Area intent must select or create an area.")
        if self.life_area_ref is None and self.expected_revision is not None:
            raise ValueError("A new Life Area does not have an expected revision.")
        return self


class AuthorItemRequest(BaseModel):
    """Shared transactional item fields."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    location: str | None = None
    item_color_code: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    life_area: AuthoringLifeAreaRequest | None = None
    placement: SchedulePlacementRequest | None = None


class AuthorActivityChildRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    requirement_code: Literal["required", "optional"] = "required"
    presentation_order: int = Field(default=1, ge=1)
    placement: SchedulePlacementRequest | None = None
    planned_slices: list[SchedulePlacementRequest] = Field(default_factory=list, max_length=100)
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"] | None = None


class AuthorActivityRequest(AuthorItemRequest):
    """Atomic root, direct children and planned placements."""

    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"] | None = None
    child_guard_mode: Literal["none", "confirm", "block"] | None = None
    planned_slices: list[SchedulePlacementRequest] = Field(default_factory=list, max_length=100)
    children: list[AuthorActivityChildRequest] = Field(default_factory=list, max_length=100)


class AuthorEventRequest(AuthorItemRequest):
    """One transactional Event Quick Create command."""

    agenda_parts: list[str] = Field(default_factory=list, max_length=100)


class AcceptedDateSpanPlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class AcceptedFloatingLocalPlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["floating_local_interval"] = "floating_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime


class AcceptedNamedZonePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["named_zone_local_interval"] = "named_zone_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    disambiguation: Literal["reject", "earlier", "later"]
    resolved_start_at: datetime
    resolved_end_at: datetime


class AcceptedAbsolutePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["absolute_interval"] = "absolute_interval"
    starts_at: datetime
    ends_at: datetime


class AcceptedCoarseLocalPlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


AcceptedAuthoringPlacementResponse = Annotated[
    AcceptedDateSpanPlacementResponse
    | AcceptedFloatingLocalPlacementResponse
    | AcceptedNamedZonePlacementResponse
    | AcceptedAbsolutePlacementResponse
    | AcceptedCoarseLocalPlacementResponse,
    Field(discriminator="kind"),
]


class AcceptedAuthoringScheduleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    placement_material_state_ref: UUID
    placement: AcceptedAuthoringPlacementResponse


class AuthoredActivityChildResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    decomposition_ref: UUID
    decomposition_state_ref: UUID
    requirement_code: Literal["required", "optional"]
    presentation_order: int
    schedule: AcceptedAuthoringScheduleResponse | None
    planned_slices: list[AcceptedAuthoringScheduleResponse]
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"]


class AuthoredActivityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    title: str
    created_at: datetime
    description: str | None
    location: str | None
    color_code: str | None
    life_area_ref: UUID | None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    life_area_color_code: str | None
    life_area_revision: int | None = Field(default=None, ge=1)
    schedule: AcceptedAuthoringScheduleResponse | None
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"]
    child_guard_mode: Literal["none", "confirm", "block"]
    planned_slices: list[AcceptedAuthoringScheduleResponse] = Field(default_factory=list)
    children: list[AuthoredActivityChildResponse] = Field(default_factory=list)
    replayed: bool


class AuthoredEventResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    title: str
    created_at: datetime
    description: str | None
    location: str | None
    color_code: str | None
    life_area_ref: UUID | None
    life_area_assignment_revision: int | None = Field(default=None, ge=1)
    life_area_color_code: str | None
    life_area_revision: int | None = Field(default=None, ge=1)
    agenda_revision: int = Field(ge=0)
    agenda_parts: list[str]
    schedule: AcceptedAuthoringScheduleResponse | None
    replayed: bool


def _application(request: Request) -> TemporalAuthoringApplication:
    runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return TemporalAuthoringApplication(runtime.session_factory)


Application = Annotated[TemporalAuthoringApplication, Depends(_application)]


def _life_area_intent(payload: AuthoringLifeAreaRequest | None) -> AuthoringLifeAreaIntent | None:
    if payload is None:
        return None
    return AuthoringLifeAreaIntent(
        life_area_ref=payload.life_area_ref,
        new_name=payload.new_name,
        expected_revision=payload.expected_revision,
        color_code=payload.color_code,
    )


def _accepted_placement(placement: SchedulePlacement) -> AcceptedAuthoringPlacementResponse:
    if isinstance(placement, DateSpanPlacement):
        return AcceptedDateSpanPlacementResponse(
            start_date=placement.start_date,
            end_date_exclusive=placement.end_date_exclusive,
        )
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return AcceptedFloatingLocalPlacementResponse(
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
        )
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        if placement.resolved_start_at is None or placement.resolved_end_at is None:
            raise TemporalAuthoringPersistenceError(
                "Accepted named-zone Schedule lost its resolved boundaries."
            )
        return AcceptedNamedZonePlacementResponse(
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
            zone_id=placement.zone_id,
            disambiguation=placement.disambiguation,
            resolved_start_at=placement.resolved_start_at,
            resolved_end_at=placement.resolved_end_at,
        )
    if isinstance(placement, AbsoluteIntervalPlacement):
        return AcceptedAbsolutePlacementResponse(
            starts_at=placement.starts_at,
            ends_at=placement.ends_at,
        )
    if isinstance(placement, CoarseLocalPeriodPlacement):
        return AcceptedCoarseLocalPlacementResponse(
            local_date=placement.local_date,
            period=placement.period,
        )
    raise TemporalAuthoringPersistenceError("Accepted Schedule placement is unsupported.")


def _accepted_schedule(schedule: EstablishedScheduleView) -> AcceptedAuthoringScheduleResponse:
    return AcceptedAuthoringScheduleResponse(
        schedule_ref=schedule.schedule_ref,
        placement_material_state_ref=schedule.material_state_ref,
        placement=_accepted_placement(schedule.placement),
    )


def _schedule_response(result: AuthoringResult) -> AcceptedAuthoringScheduleResponse | None:
    return None if result.schedule is None else _accepted_schedule(result.schedule)


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, TemporalAuthoringStructureConflictError):
        return ProblemError(
            status=409,
            code="temporal.authoring.structure_conflict",
            category="conflict",
            title="Activity structure conflict",
            detail="A child placement does not fit the parent temporal envelope.",
            retryable=False,
        )
    if isinstance(exc, TemporalAuthoringInputError):
        return ProblemError(
            status=422,
            code="temporal.authoring.invalid_input",
            category="validation",
            title="Invalid authoring input",
            detail=str(exc),
            retryable=False,
        )
    if isinstance(exc, TemporalAuthoringLifeAreaUnavailableError):
        return ProblemError(
            status=404,
            code="temporal.authoring.life_area_unavailable",
            category="not_found",
            title="Life Area unavailable",
            detail="The selected Life Area is unavailable in this self scope.",
            retryable=False,
        )
    if isinstance(exc, TemporalAuthoringLifeAreaConflictError):
        return ProblemError(
            status=409,
            code="temporal.authoring.life_area_conflict",
            category="conflict",
            title="Life Area changed",
            detail="Refresh the Life Area catalog before changing its appearance.",
            retryable=False,
        )
    if isinstance(exc, TemporalAuthoringOperationIdReuseError):
        return ProblemError(
            status=409,
            code="temporal.authoring.operation_id_reused",
            category="conflict",
            title="Authoring operation conflict",
            detail="This operation id was already used for different authoring intent.",
            retryable=False,
        )
    return ProblemError(
        status=503,
        code="temporal.authoring.persistence_unavailable",
        category="service",
        title="Authoring unavailable",
        detail="The authoring operation could not complete safely.",
        retryable=True,
    )


_Errors = (
    TemporalAuthoringInputError,
    TemporalAuthoringLifeAreaUnavailableError,
    TemporalAuthoringLifeAreaConflictError,
    TemporalAuthoringOperationIdReuseError,
    TemporalAuthoringPersistenceError,
    TemporalAuthoringStructureConflictError,
)


@router.post(
    "/activities",
    status_code=201,
    response_model=AuthoredActivityResponse,
    operation_id="temporal_author_activity",
)
async def author_activity(
    payload: AuthorActivityRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> AuthoredActivityResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create_activity(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_intent=_life_area_intent(payload.life_area),
            description=payload.description,
            location=payload.location,
            item_color_code=payload.item_color_code,
            placement=None
            if payload.placement is None
            else _placement_from_request(payload.placement),
            session_capture_mode=payload.session_capture_mode,
            child_guard_mode=payload.child_guard_mode,
            planned_slices=tuple(
                _placement_from_request(value) for value in payload.planned_slices
            ),
            children=tuple(
                ActivityChildIntent(
                    title=child.title,
                    description=child.description,
                    requirement_code=child.requirement_code,
                    presentation_order=child.presentation_order,
                    placement=(
                        None
                        if child.placement is None
                        else _placement_from_request(child.placement)
                    ),
                    planned_slices=tuple(
                        _placement_from_request(value) for value in child.planned_slices
                    ),
                    session_capture_mode=child.session_capture_mode,
                )
                for child in payload.children
            ),
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    if result.replayed:
        response.status_code = 200
    item = result.item
    return AuthoredActivityResponse(
        activity_ref=item.subject_native_ref,
        title=item.title,
        created_at=item.created_at,
        description=item.description,
        location=item.location,
        color_code=item.color_code,
        life_area_ref=item.life_area_ref,
        life_area_assignment_revision=item.life_area_assignment_revision,
        life_area_color_code=item.life_area_color_code,
        life_area_revision=item.life_area_revision,
        schedule=_schedule_response(result),
        session_capture_mode=result.session_capture_mode,
        child_guard_mode=result.child_guard_mode,
        planned_slices=[_accepted_schedule(value) for value in result.planned_slices],
        children=[
            AuthoredActivityChildResponse(
                activity_ref=child.item.subject_native_ref,
                title=child.item.title,
                decomposition_ref=child.decomposition_ref,
                decomposition_state_ref=child.state_ref,
                requirement_code=child.requirement_code,
                presentation_order=child.presentation_order,
                schedule=(None if child.schedule is None else _accepted_schedule(child.schedule)),
                planned_slices=[_accepted_schedule(value) for value in child.planned_slices],
                session_capture_mode=child.session_capture_mode,
            )
            for child in result.children
        ],
        replayed=result.replayed,
    )


@router.post(
    "/events",
    status_code=201,
    response_model=AuthoredEventResponse,
    operation_id="temporal_author_event",
)
async def author_event(
    payload: AuthorEventRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> AuthoredEventResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create_event(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            life_area_intent=_life_area_intent(payload.life_area),
            description=payload.description,
            location=payload.location,
            item_color_code=payload.item_color_code,
            agenda_parts=payload.agenda_parts,
            placement=None
            if payload.placement is None
            else _placement_from_request(payload.placement),
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    if result.replayed:
        response.status_code = 200
    item = result.item
    return AuthoredEventResponse(
        event_ref=item.subject_native_ref,
        title=item.title,
        created_at=item.created_at,
        description=item.description,
        location=item.location,
        color_code=item.color_code,
        life_area_ref=item.life_area_ref,
        life_area_assignment_revision=item.life_area_assignment_revision,
        life_area_color_code=item.life_area_color_code,
        life_area_revision=item.life_area_revision,
        agenda_revision=item.agenda_revision,
        agenda_parts=list(item.agenda_parts),
        schedule=_schedule_response(result),
        replayed=result.replayed,
    )
