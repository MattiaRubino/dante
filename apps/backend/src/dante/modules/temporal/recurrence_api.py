"""Typed B06-B Recurrence transport for Routine and Event owners."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date, datetime, time
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.recurrence import (
    CalendarRecurrence, CyclicRecurrence, ElapsedRecurrence, QuotaRecurrence,
    RecurrenceApplication, RecurrenceInputError, RecurrenceNotFoundError,
    RecurrenceOperationReuseError, RecurrencePersistenceError, RecurrenceSpec,
    RecurrenceStateConflictError,
)
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class CalendarOrdinalWeekday(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    weekday_number: int = Field(ge=1, le=7)
    ordinal: int = Field(ge=-5, le=5, ne=0)


class CalendarYearMonthDay(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    month_number: int = Field(ge=1, le=12)
    month_day: int = Field(ge=-31, le=31, ne=0)


class CalendarRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family_code: Literal["calendar_wall_clock"] = "calendar_wall_clock"
    range_kind: Literal["open", "until_boundary", "expected_count"]
    expected_occurrence_count: int | None = Field(default=None, ge=1)
    effective_from: date
    effective_until: date | None = None
    pattern_code: Literal["daily", "weekly_weekdays", "monthly_month_days", "monthly_ordinal_weekdays", "yearly_month_days", "anchor_step"]
    interval_count: int = Field(ge=1, le=10000)
    clock_basis_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None = Field(default=None, min_length=1, max_length=200)
    pattern_anchor_date: date | None = None
    wall_times: list[time] = Field(default_factory=list, max_length=32)
    weekdays: list[int] = Field(default_factory=list, max_length=7)
    month_days: list[int] = Field(default_factory=list, max_length=62)
    ordinal_weekdays: list[CalendarOrdinalWeekday] = Field(default_factory=list, max_length=70)
    year_month_days: list[CalendarYearMonthDay] = Field(default_factory=list, max_length=372)
    nonexistent_local_time_policy: Literal["skip_civil_candidate"] | None = None
    ambiguous_local_time_policy: Literal["earlier", "later"] | None = None
    step_unit_code: Literal["day", "week", "month", "year"] | None = None


class ElapsedRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family_code: Literal["elapsed_interval"] = "elapsed_interval"
    range_kind: Literal["open", "until_boundary", "expected_count"]
    expected_occurrence_count: int | None = Field(default=None, ge=1)
    effective_from: datetime
    effective_until: datetime | None = None
    elapsed_seconds: Decimal = Field(gt=0, max_digits=20, decimal_places=6)
    anchor_mode_code: Literal["fixed_anchor", "previous_expected"]
    anchor_at: datetime


class QuotaRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family_code: Literal["quota_per_period"] = "quota_per_period"
    range_kind: Literal["open", "until_boundary"]
    expected_occurrence_count: None = None
    effective_from: date
    effective_until: date | None = None
    quota_count: int = Field(ge=1, le=10000)
    period_unit_code: Literal["day", "week", "month", "year"]
    period_span: int = Field(ge=1, le=10000)
    frame_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None = Field(default=None, min_length=1, max_length=200)
    week_start: int | None = Field(default=None, ge=1, le=7)
    pattern_anchor_date: date | None = None


class CyclicRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    family_code: Literal["cyclic_positional"] = "cyclic_positional"
    range_kind: Literal["open", "until_boundary", "expected_count"]
    expected_occurrence_count: int | None = Field(default=None, ge=1)
    effective_from: date
    effective_until: date | None = None
    cycle_length: int = Field(ge=1, le=10000)
    position_unit_code: Literal["day", "week"]
    pattern_anchor_date: date
    generates_expected: list[bool] = Field(min_length=1, max_length=10000)


RecurrenceRequest = Annotated[
    CalendarRecurrenceRequest | ElapsedRecurrenceRequest | QuotaRecurrenceRequest | CyclicRecurrenceRequest,
    Field(discriminator="family_code"),
]


class ReplaceRecurrenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID | None = None
    recurrence: RecurrenceRequest


class CalendarRecurrenceResponse(CalendarRecurrenceRequest):
    pass


class ElapsedRecurrenceResponse(ElapsedRecurrenceRequest):
    pass


class QuotaRecurrenceResponse(QuotaRecurrenceRequest):
    pass


class CyclicRecurrenceResponse(CyclicRecurrenceRequest):
    pass


RecurrenceResponse = Annotated[
    CalendarRecurrenceResponse | ElapsedRecurrenceResponse | QuotaRecurrenceResponse | CyclicRecurrenceResponse,
    Field(discriminator="family_code"),
]


class RecurrenceStateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    material_state_ref: UUID
    recurrence: RecurrenceResponse


class RecurrenceMutationResponse(RecurrenceStateResponse):
    accepted_at: datetime
    replayed: bool


def _application(request: Request) -> RecurrenceApplication:
    return RecurrenceApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[RecurrenceApplication, Depends(_application)]
_Errors = (RecurrenceInputError, RecurrenceOperationReuseError, RecurrenceNotFoundError, RecurrenceStateConflictError, RecurrencePersistenceError)


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, RecurrenceInputError):
        return ProblemError(status=422, code="temporal.recurrence.invalid_input", category="validation", title="Recurrence command rejected", detail=str(exc))
    if isinstance(exc, RecurrenceOperationReuseError):
        return ProblemError(status=409, code="temporal.recurrence.operation_id_reused", category="conflict", title="Recurrence operation id reused", detail="Use a fresh operation id for a different Recurrence intent.")
    if isinstance(exc, RecurrenceNotFoundError):
        return ProblemError(status=404, code="temporal.recurrence.unavailable", category="not_found", title="Recurrence owner unavailable", detail="The Routine or Event is not available in this account.")
    if isinstance(exc, RecurrenceStateConflictError):
        return ProblemError(status=409, code="temporal.recurrence.state_conflict", category="conflict", title="Recurrence state changed", detail="Reload the current Recurrence and retry from its MaterialState reference.")
    return ProblemError(status=503, code="temporal.recurrence.persistence_unavailable", category="service", title="Recurrence persistence unavailable", detail="Canonical Recurrence state could not be read or written.", retryable=True)


def _spec(payload: RecurrenceRequest) -> RecurrenceSpec:
    if isinstance(payload, CalendarRecurrenceRequest):
        return CalendarRecurrence(**payload.model_dump(exclude_none=False, exclude={"wall_times", "weekdays", "month_days", "ordinal_weekdays", "year_month_days"}),
            wall_times=tuple(payload.wall_times), weekdays=tuple(payload.weekdays), month_days=tuple(payload.month_days),
            ordinal_weekdays=tuple((item.weekday_number, item.ordinal) for item in payload.ordinal_weekdays),
            year_month_days=tuple((item.month_number, item.month_day) for item in payload.year_month_days))
    if isinstance(payload, ElapsedRecurrenceRequest):
        return ElapsedRecurrence(**payload.model_dump())
    if isinstance(payload, QuotaRecurrenceRequest):
        return QuotaRecurrence(**payload.model_dump())
    return CyclicRecurrence(**payload.model_dump(exclude={"generates_expected"}), generates_expected=tuple(payload.generates_expected))


def _state(value: object) -> RecurrenceStateResponse:
    return RecurrenceStateResponse(material_state_ref=value.material_state_ref, recurrence=asdict(value.recurrence))


@router.get("/routines/{routine_ref}/recurrence", response_model=RecurrenceStateResponse, operation_id="temporal_get_routine_recurrence")
async def get_routine_recurrence(routine_ref: UUID, context: Context, application: Application, response: Response) -> RecurrenceStateResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.get(owner="routine", self_person_ref=context.self_person_ref, owner_ref=routine_ref)
        if value is None:
            raise RecurrenceNotFoundError()
        return _state(value)
    except _Errors as exc:
        raise _problem(exc) from exc


@router.put("/routines/{routine_ref}/recurrence", response_model=RecurrenceMutationResponse, operation_id="temporal_replace_routine_recurrence")
async def replace_routine_recurrence(routine_ref: UUID, payload: ReplaceRecurrenceRequest, context: MutatingContext, application: Application, response: Response) -> RecurrenceMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.replace(owner="routine", self_person_ref=context.self_person_ref, owner_ref=routine_ref, operation_id=payload.operation_id, expected_material_state_ref=payload.expected_material_state_ref, recurrence=_spec(payload.recurrence))
        return RecurrenceMutationResponse(**_state(value.recurrence).model_dump(), accepted_at=value.accepted_at, replayed=value.replayed)
    except _Errors as exc:
        raise _problem(exc) from exc


@router.get("/events/{event_ref}/recurrence", response_model=RecurrenceStateResponse | None, operation_id="temporal_get_event_recurrence")
async def get_event_recurrence(event_ref: UUID, context: Context, application: Application, response: Response) -> RecurrenceStateResponse | None:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.get(owner="event", self_person_ref=context.self_person_ref, owner_ref=event_ref)
        return None if value is None else _state(value)
    except _Errors as exc:
        raise _problem(exc) from exc


@router.put("/events/{event_ref}/recurrence", response_model=RecurrenceMutationResponse, operation_id="temporal_replace_event_recurrence")
async def replace_event_recurrence(event_ref: UUID, payload: ReplaceRecurrenceRequest, context: MutatingContext, application: Application, response: Response) -> RecurrenceMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        value = await application.replace(owner="event", self_person_ref=context.self_person_ref, owner_ref=event_ref, operation_id=payload.operation_id, expected_material_state_ref=payload.expected_material_state_ref, recurrence=_spec(payload.recurrence))
        return RecurrenceMutationResponse(**_state(value.recurrence).model_dump(), accepted_at=value.accepted_at, replayed=value.replayed)
    except _Errors as exc:
        raise _problem(exc) from exc
