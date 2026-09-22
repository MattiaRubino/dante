"""Typed B06-C transport for canonical Occurrence commands and reads."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date, datetime, time
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    CyclicCoordinate,
    ElapsedCoordinate,
    OccurrenceAlreadySkippedError,
    OccurrenceApplication,
    OccurrenceCheckpointLimitError,
    OccurrenceInputError,
    OccurrenceMaterializedConflictError,
    OccurrenceOperationReuseError,
    OccurrencePersistenceError,
    OccurrenceSourceInactiveError,
    OccurrenceSourceNotFoundError,
    OccurrenceView,
)
from dante.modules.temporal.api import (
    SchedulePlacementRequest,
    TemporalScheduleApplicationDependency,
    _placement_from_request,
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
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class OccurrenceCheckpointRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str = Field(min_length=1, max_length=200)


class ExplicitExtraOccurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)


class SkipOccurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    reason: str | None = Field(default=None, max_length=500)


class EstablishOccurrenceScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    placement: SchedulePlacementRequest


class OccurrenceDateSpanSchedulePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["date_span"] = "date_span"
    start_date: date
    end_date_exclusive: date


class OccurrenceFloatingSchedulePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["floating_local_interval"] = "floating_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime


class OccurrenceNamedZoneSchedulePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["named_zone_local_interval"] = "named_zone_local_interval"
    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    resolved_start_at: datetime
    resolved_end_at: datetime


class OccurrenceAbsoluteSchedulePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["absolute_interval"] = "absolute_interval"
    starts_at: datetime
    ends_at: datetime


class OccurrenceCoarseSchedulePlacementResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["coarse_local_period"] = "coarse_local_period"
    local_date: date
    period: Literal["morning", "afternoon", "evening"]


OccurrenceSchedulePlacementResponse = Annotated[
    OccurrenceDateSpanSchedulePlacementResponse
    | OccurrenceFloatingSchedulePlacementResponse
    | OccurrenceNamedZoneSchedulePlacementResponse
    | OccurrenceAbsoluteSchedulePlacementResponse
    | OccurrenceCoarseSchedulePlacementResponse,
    Field(discriminator="kind"),
]


class OccurrenceScheduleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    occurrence_ref: UUID
    schedule_ref: UUID
    placement_material_state_ref: UUID
    placement: OccurrenceSchedulePlacementResponse
    replayed: bool = False


class CalendarOccurrenceCoordinate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    family_code: Literal["calendar_wall_clock"] = "calendar_wall_clock"
    generated_date: date
    generated_wall_time: time | None = None
    clock_basis_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None = Field(default=None, min_length=1, max_length=200)
    resolved_at: datetime | None = None


class ElapsedOccurrenceCoordinate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    family_code: Literal["elapsed_interval"] = "elapsed_interval"
    expected_at: datetime


class QuotaOccurrenceCoordinate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    family_code: Literal["quota_per_period"] = "quota_per_period"
    period_start_date: date
    period_end_date_exclusive: date
    frame_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None = Field(default=None, min_length=1, max_length=200)


class CyclicOccurrenceCoordinate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    family_code: Literal["cyclic_positional"] = "cyclic_positional"
    generated_date: date
    position_index: int = Field(ge=0)


OccurrenceCoordinateResponse = Annotated[
    CalendarOccurrenceCoordinate
    | ElapsedOccurrenceCoordinate
    | QuotaOccurrenceCoordinate
    | CyclicOccurrenceCoordinate,
    Field(discriminator="family_code"),
]


class OccurrenceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    occurrence_ref: UUID
    source_native_ref: UUID
    governing_recurrence_state_ref: UUID | None
    origin_code: Literal["recurrence_generated", "explicit_extra"]
    coordinate: OccurrenceCoordinateResponse | None
    skipped: bool
    skip_reason: str | None
    skipped_at: datetime | None


class OccurrenceCheckpointResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_native_ref: UUID
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    occurrences: list[OccurrenceResponse]
    accepted_at: datetime
    replayed: bool


class OccurrenceMutationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    occurrence: OccurrenceResponse
    accepted_at: datetime
    replayed: bool


class StructuralExclusionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    governing_recurrence_state_ref: UUID
    coordinate: Annotated[
        CalendarOccurrenceCoordinate | ElapsedOccurrenceCoordinate | CyclicOccurrenceCoordinate,
        Field(discriminator="family_code"),
    ]


class StructuralExclusionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    exclusion_ref: UUID
    source_native_ref: UUID
    governing_recurrence_state_ref: UUID
    coordinate: (
        CalendarOccurrenceCoordinate | ElapsedOccurrenceCoordinate | CyclicOccurrenceCoordinate
    )
    accepted_at: datetime
    replayed: bool


def _application(request: Request) -> OccurrenceApplication:
    return OccurrenceApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[OccurrenceApplication, Depends(_application)]
_Errors = (
    OccurrenceInputError,
    OccurrenceOperationReuseError,
    OccurrenceSourceNotFoundError,
    OccurrenceAlreadySkippedError,
    OccurrenceMaterializedConflictError,
    OccurrenceCheckpointLimitError,
    OccurrencePersistenceError,
    OccurrenceSourceInactiveError,
)


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, OccurrenceInputError):
        return ProblemError(
            status=422,
            code="temporal.occurrence.invalid_input",
            category="validation",
            title="Occurrence command rejected",
            detail=str(exc),
        )
    if isinstance(exc, OccurrenceCheckpointLimitError):
        return ProblemError(
            status=422,
            code="temporal.occurrence.checkpoint_limit",
            category="validation",
            title="Occurrence checkpoint is too dense",
            detail=str(exc),
        )
    if isinstance(exc, OccurrenceOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.occurrence.operation_id_reused",
            category="conflict",
            title="Occurrence operation id reused",
            detail="Use a fresh operation id for a different intent.",
        )
    if isinstance(exc, OccurrenceAlreadySkippedError):
        return ProblemError(
            status=409,
            code="temporal.occurrence.already_skipped",
            category="conflict",
            title="Occurrence already skipped",
            detail="Skip is an immutable disposition, not a delete or source cancellation.",
        )
    if isinstance(exc, OccurrenceMaterializedConflictError):
        return ProblemError(
            status=409,
            code="temporal.occurrence.exclusion_materialized",
            category="conflict",
            title="Occurrence is already materialized",
            detail="Use the one-Occurrence skip/exception path; structural exclusion is pre-generation only.",
        )
    if isinstance(exc, OccurrenceSourceNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.occurrence.unavailable",
            category="not_found",
            title="Occurrence unavailable",
            detail="The source or Occurrence is not available in this account.",
        )
    if isinstance(exc, OccurrenceSourceInactiveError):
        return ProblemError(
            status=409,
            code="temporal.occurrence.source_inactive",
            category="conflict",
            title="Routine is not active",
            detail="Resume the Routine before creating future or extra Occurrences.",
        )
    return ProblemError(
        status=503,
        code="temporal.occurrence.persistence_unavailable",
        category="service",
        title="Occurrence persistence unavailable",
        detail="Canonical Occurrence state could not be read or written.",
        retryable=True,
    )


def _response(value: OccurrenceView) -> OccurrenceResponse:
    payload = asdict(value)
    return OccurrenceResponse(**payload)


def _domain_coordinate(
    value: CalendarOccurrenceCoordinate | ElapsedOccurrenceCoordinate | CyclicOccurrenceCoordinate,
) -> CalendarCoordinate | ElapsedCoordinate | CyclicCoordinate:
    if isinstance(value, CalendarOccurrenceCoordinate):
        return CalendarCoordinate(**value.model_dump())
    if isinstance(value, ElapsedOccurrenceCoordinate):
        return ElapsedCoordinate(**value.model_dump())
    return CyclicCoordinate(**value.model_dump())


async def _checkpoint(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    payload: OccurrenceCheckpointRequest,
    context: DanteContext,
    application: OccurrenceApplication,
    response: Response,
) -> OccurrenceCheckpointResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.checkpoint(
            owner=owner,
            self_person_ref=context.self_person_ref,
            source_ref=source_ref,
            operation_id=payload.operation_id,
            start_date=payload.start_date,
            end_date_exclusive=payload.end_date_exclusive,
            effective_zone_id=payload.effective_zone_id,
        )
        return OccurrenceCheckpointResponse(
            source_native_ref=value.source_native_ref,
            start_date=value.start_date,
            end_date_exclusive=value.end_date_exclusive,
            effective_zone_id=value.effective_zone_id,
            occurrences=[_response(item) for item in value.occurrences],
            accepted_at=value.accepted_at,
            replayed=value.replayed,
        )
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post(
    "/routines/{routine_ref}/occurrences/checkpoint",
    response_model=OccurrenceCheckpointResponse,
    operation_id="temporal_checkpoint_routine_occurrences",
)
async def checkpoint_routine_occurrences(
    routine_ref: UUID,
    payload: OccurrenceCheckpointRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> OccurrenceCheckpointResponse:
    return await _checkpoint("routine", routine_ref, payload, context, application, response)


@router.post(
    "/events/{event_ref}/occurrences/checkpoint",
    response_model=OccurrenceCheckpointResponse,
    operation_id="temporal_checkpoint_event_occurrences",
)
async def checkpoint_event_occurrences(
    event_ref: UUID,
    payload: OccurrenceCheckpointRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> OccurrenceCheckpointResponse:
    return await _checkpoint("event", event_ref, payload, context, application, response)


def _schedule_placement_response(
    placement: SchedulePlacement,
) -> OccurrenceSchedulePlacementResponse:
    if isinstance(placement, DateSpanPlacement):
        return OccurrenceDateSpanSchedulePlacementResponse(
            start_date=placement.start_date,
            end_date_exclusive=placement.end_date_exclusive,
        )
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return OccurrenceFloatingSchedulePlacementResponse(
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
        )
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        assert placement.resolved_start_at is not None
        assert placement.resolved_end_at is not None
        return OccurrenceNamedZoneSchedulePlacementResponse(
            starts_local_at=placement.starts_local_at,
            ends_local_at=placement.ends_local_at,
            zone_id=placement.zone_id,
            resolved_start_at=placement.resolved_start_at,
            resolved_end_at=placement.resolved_end_at,
        )
    if isinstance(placement, AbsoluteIntervalPlacement):
        return OccurrenceAbsoluteSchedulePlacementResponse(
            starts_at=placement.starts_at,
            ends_at=placement.ends_at,
        )
    assert isinstance(placement, CoarseLocalPeriodPlacement)
    return OccurrenceCoarseSchedulePlacementResponse(
        local_date=placement.local_date,
        period=placement.period,
    )


@router.post(
    "/occurrences/{occurrence_ref}/schedule",
    response_model=OccurrenceScheduleResponse,
    status_code=201,
    operation_id="temporal_establish_occurrence_schedule",
)
async def establish_occurrence_schedule(
    occurrence_ref: UUID,
    payload: EstablishOccurrenceScheduleRequest,
    context: MutatingContext,
    application: TemporalScheduleApplicationDependency,
    response: Response,
) -> OccurrenceScheduleResponse:
    """Attach one accepted shared Schedule placement to a canonical Occurrence."""
    response.headers["Cache-Control"] = "no-store"
    try:
        placement = _placement_from_request(payload.placement)
        value = await application.establish_schedule(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            subject_native_ref=NativeRef(occurrence_ref),
            placement=placement,
        )
    except ScheduleInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.occurrence.schedule_invalid",
            category="validation",
            title="Invalid Occurrence Schedule",
            detail=str(exc),
        ) from exc
    except ScheduleNotFoundError as exc:
        raise ProblemError(
            status=404,
            code="temporal.occurrence.unavailable",
            category="not_found",
            title="Occurrence unavailable",
            detail="The Occurrence is unavailable in the current self scope.",
        ) from exc
    except ScheduleOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.occurrence.schedule_operation_id_reused",
            category="conflict",
            title="Occurrence Schedule operation conflict",
            detail="Use a new operation id for a different Schedule intent.",
        ) from exc
    except SchedulePersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.occurrence.schedule_unavailable",
            category="service",
            title="Occurrence Schedule unavailable",
            detail="Canonical Occurrence Schedule state could not be persisted.",
            retryable=True,
        ) from exc
    if value.replayed:
        response.status_code = 200
    return OccurrenceScheduleResponse(
        occurrence_ref=value.subject_native_ref,
        schedule_ref=value.schedule_ref,
        placement_material_state_ref=value.material_state_ref,
        placement=_schedule_placement_response(value.placement),
        replayed=value.replayed,
    )


async def _extra(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    payload: ExplicitExtraOccurrenceRequest,
    context: DanteContext,
    application: OccurrenceApplication,
    response: Response,
) -> OccurrenceMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.create_extra(
            owner=owner,
            self_person_ref=context.self_person_ref,
            source_ref=source_ref,
            operation_id=payload.operation_id,
        )
        return OccurrenceMutationResponse(
            occurrence=_response(value.occurrence),
            accepted_at=value.accepted_at,
            replayed=value.replayed,
        )
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post(
    "/routines/{routine_ref}/occurrences/extra",
    response_model=OccurrenceMutationResponse,
    operation_id="temporal_create_routine_extra_occurrence",
)
async def create_routine_extra_occurrence(
    routine_ref: UUID,
    payload: ExplicitExtraOccurrenceRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> OccurrenceMutationResponse:
    return await _extra("routine", routine_ref, payload, context, application, response)


@router.post(
    "/events/{event_ref}/occurrences/extra",
    response_model=OccurrenceMutationResponse,
    operation_id="temporal_create_event_extra_occurrence",
)
async def create_event_extra_occurrence(
    event_ref: UUID,
    payload: ExplicitExtraOccurrenceRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> OccurrenceMutationResponse:
    return await _extra("event", event_ref, payload, context, application, response)


@router.get(
    "/occurrences/{occurrence_ref}",
    response_model=OccurrenceResponse,
    operation_id="temporal_get_occurrence",
)
async def get_occurrence(
    occurrence_ref: UUID, context: Context, application: Application, response: Response
) -> OccurrenceResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        return _response(
            await application.get(
                self_person_ref=context.self_person_ref, occurrence_ref=occurrence_ref
            )
        )
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post(
    "/occurrences/{occurrence_ref}/skip",
    response_model=OccurrenceMutationResponse,
    operation_id="temporal_skip_occurrence",
)
async def skip_occurrence(
    occurrence_ref: UUID,
    payload: SkipOccurrenceRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> OccurrenceMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.skip(
            self_person_ref=context.self_person_ref,
            occurrence_ref=occurrence_ref,
            operation_id=payload.operation_id,
            reason=payload.reason,
        )
        return OccurrenceMutationResponse(
            occurrence=_response(value.occurrence),
            accepted_at=value.accepted_at,
            replayed=value.replayed,
        )
    except _Errors as exc:
        raise _problem(exc) from exc


async def _exclude(
    owner: Literal["routine", "event"],
    source_ref: UUID,
    payload: StructuralExclusionRequest,
    context: DanteContext,
    application: OccurrenceApplication,
    response: Response,
) -> StructuralExclusionResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.exclude(
            owner=owner,
            self_person_ref=context.self_person_ref,
            source_ref=source_ref,
            governing_recurrence_state_ref=payload.governing_recurrence_state_ref,
            operation_id=payload.operation_id,
            coordinate=_domain_coordinate(payload.coordinate),
        )
        return StructuralExclusionResponse(**asdict(value))
    except _Errors as exc:
        raise _problem(exc) from exc


@router.post(
    "/routines/{routine_ref}/occurrences/exclusions",
    response_model=StructuralExclusionResponse,
    operation_id="temporal_exclude_routine_occurrence_coordinate",
)
async def exclude_routine_occurrence_coordinate(
    routine_ref: UUID,
    payload: StructuralExclusionRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> StructuralExclusionResponse:
    return await _exclude("routine", routine_ref, payload, context, application, response)


@router.post(
    "/events/{event_ref}/occurrences/exclusions",
    response_model=StructuralExclusionResponse,
    operation_id="temporal_exclude_event_occurrence_coordinate",
)
async def exclude_event_occurrence_coordinate(
    event_ref: UUID,
    payload: StructuralExclusionRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> StructuralExclusionResponse:
    return await _exclude("event", event_ref, payload, context, application, response)
