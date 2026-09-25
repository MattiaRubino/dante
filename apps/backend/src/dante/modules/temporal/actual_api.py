"""B10-A HTTP surface for Actual realization authoring and authoritative reads."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.actual_runtime import (
    ActualAmbiguousSubjectError,
    ActualApplication,
    ActualCurrentConflictError,
    ActualInputError,
    ActualNotFoundError,
    ActualOperationReuseError,
    ActualPersistenceError,
    ActualRealizationView,
    ActualSessionBasis,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])

SubjectKind = Literal["activity", "event", "occurrence"]


class ActualTimingInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    extent_code: Literal["instant", "start_only", "interval"]
    started_at: datetime
    ended_at: datetime | None = None

    @model_validator(mode="after")
    def validate_extent(self) -> "ActualTimingInput":
        if self.extent_code in {"instant", "start_only"} and self.ended_at is not None:
            raise ValueError(f"{self.extent_code} timing cannot carry ended_at")
        if self.extent_code == "interval" and (
            self.ended_at is None or self.ended_at <= self.started_at
        ):
            raise ValueError("interval timing requires ended_at after started_at")
        return self


class ActualSessionBasisInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_ref: UUID = Field(strict=False)
    session_timing_material_state_ref: UUID = Field(strict=False)


class ActualRealizationCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID | None = Field(default=None, strict=False)
    realization_occurred: bool
    timing: ActualTimingInput | None = None
    session_bases: list[ActualSessionBasisInput] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_realization_payload(self) -> "ActualRealizationCommand":
        if not self.realization_occurred and (self.timing is not None or self.session_bases):
            raise ValueError("known non-realization cannot carry timing or Session bases")
        session_refs = [basis.session_ref for basis in self.session_bases]
        if len(set(session_refs)) != len(session_refs):
            raise ValueError("each Session may appear at most once in an Actual state")
        return self


class ActualTimingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    extent_code: Literal["instant", "start_only", "interval"]
    started_at: datetime
    ended_at: datetime | None


class ActualSessionBasisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_ref: UUID
    session_timing_material_state_ref: UUID


class ActualRealizationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    actual_ref: UUID
    subject_native_ref: UUID
    material_state_ref: UUID
    realization_occurred: bool
    timing: ActualTimingResponse | None
    session_bases: list[ActualSessionBasisResponse]
    replayed: bool


class ActualRealizationHistoryResponse(ActualRealizationResponse):
    current_from_at: datetime
    current_until_at: datetime | None


def _application(request: Request) -> ActualApplication:
    return ActualApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[ActualApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: ActualRealizationView) -> ActualRealizationResponse:
    timing = (
        ActualTimingResponse(
            extent_code=view.extent_code,
            started_at=view.started_at,
            ended_at=view.ended_at,
        )
        if view.extent_code is not None and view.started_at is not None
        else None
    )
    return ActualRealizationResponse(
        actual_ref=view.actual_ref,
        subject_native_ref=view.subject_native_ref,
        material_state_ref=view.material_state_ref,
        realization_occurred=view.realization_occurred,
        timing=timing,
        session_bases=[
            ActualSessionBasisResponse(
                session_ref=basis.session_ref,
                session_timing_material_state_ref=basis.session_timing_material_state_ref,
            )
            for basis in view.session_bases
        ],
        replayed=view.replayed,
    )


def _history_response(view: ActualRealizationView) -> ActualRealizationHistoryResponse:
    if view.current_from_at is None:
        raise ActualPersistenceError("Actual current-history chronology is unavailable.")
    response = _response(view)
    return ActualRealizationHistoryResponse(
        **response.model_dump(),
        current_from_at=view.current_from_at,
        current_until_at=view.current_until_at,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ActualInputError):
        return ProblemError(
            status=422,
            code="temporal.actual.invalid_input",
            category="validation",
            title="Actual realization rejected",
            detail=str(exc),
        )
    if isinstance(exc, ActualNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.actual.not_found",
            category="not_found",
            title="Actual unavailable",
            detail=str(exc),
        )
    if isinstance(exc, ActualOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.actual.operation_id_reused",
            category="conflict",
            title="Actual operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, ActualCurrentConflictError):
        return ProblemError(
            status=409,
            code="temporal.actual.current_conflict",
            category="conflict",
            title="Actual realization changed",
            detail=str(exc),
        )
    if isinstance(exc, ActualAmbiguousSubjectError):
        return ProblemError(
            status=409,
            code="temporal.actual.ambiguous_subject",
            category="conflict",
            title="Actual subject is ambiguous",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.actual.persistence",
        category="conflict",
        title="Actual realization rejected",
        detail="Actual realization command was rejected.",
    )


async def _record(
    subject_kind: SubjectKind,
    subject_ref: UUID,
    payload: ActualRealizationCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ActualRealizationResponse:
    timing = payload.timing
    try:
        view = await application.record(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_ref),
            expected_material_state_ref=(
                MaterialStateRef(payload.expected_material_state_ref)
                if payload.expected_material_state_ref is not None
                else None
            ),
            realization_occurred=payload.realization_occurred,
            extent_code=timing.extent_code if timing is not None else None,
            started_at=timing.started_at if timing is not None else None,
            ended_at=timing.ended_at if timing is not None else None,
            session_bases=tuple(
                ActualSessionBasis(
                    session_ref=NativeRef(basis.session_ref),
                    session_timing_material_state_ref=MaterialStateRef(
                        basis.session_timing_material_state_ref
                    ),
                )
                for basis in payload.session_bases
            ),
        )
    except (
        ActualInputError,
        ActualNotFoundError,
        ActualOperationReuseError,
        ActualCurrentConflictError,
        ActualAmbiguousSubjectError,
        ActualPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


async def _get(
    subject_kind: SubjectKind,
    subject_ref: UUID,
    context: Context,
    application: Application,
) -> ActualRealizationResponse:
    try:
        view = await application.get_for_subject(
            self_person_ref=context.self_person_ref,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_ref),
        )
    except (
        ActualInputError,
        ActualNotFoundError,
        ActualAmbiguousSubjectError,
        ActualPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    return _response(view)


@router.post(
    "/activities/{activity_ref}/actual",
    response_model=ActualRealizationResponse,
    operation_id="temporal_record_activity_actual",
)
async def record_activity_actual(
    activity_ref: UUID,
    payload: ActualRealizationCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ActualRealizationResponse:
    return await _record("activity", activity_ref, payload, context, application, response)


@router.get(
    "/activities/{activity_ref}/actual",
    response_model=ActualRealizationResponse,
    operation_id="temporal_get_activity_actual",
)
async def get_activity_actual(
    activity_ref: UUID, context: Context, application: Application
) -> ActualRealizationResponse:
    return await _get("activity", activity_ref, context, application)


@router.post(
    "/events/{event_ref}/actual",
    response_model=ActualRealizationResponse,
    operation_id="temporal_record_event_actual",
)
async def record_event_actual(
    event_ref: UUID,
    payload: ActualRealizationCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ActualRealizationResponse:
    return await _record("event", event_ref, payload, context, application, response)


@router.get(
    "/events/{event_ref}/actual",
    response_model=ActualRealizationResponse,
    operation_id="temporal_get_event_actual",
)
async def get_event_actual(
    event_ref: UUID, context: Context, application: Application
) -> ActualRealizationResponse:
    return await _get("event", event_ref, context, application)


@router.post(
    "/occurrences/{occurrence_ref}/actual",
    response_model=ActualRealizationResponse,
    operation_id="temporal_record_occurrence_actual",
)
async def record_occurrence_actual(
    occurrence_ref: UUID,
    payload: ActualRealizationCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ActualRealizationResponse:
    return await _record("occurrence", occurrence_ref, payload, context, application, response)


@router.get(
    "/occurrences/{occurrence_ref}/actual",
    response_model=ActualRealizationResponse,
    operation_id="temporal_get_occurrence_actual",
)
async def get_occurrence_actual(
    occurrence_ref: UUID, context: Context, application: Application
) -> ActualRealizationResponse:
    return await _get("occurrence", occurrence_ref, context, application)


@router.get(
    "/actuals/{actual_ref}/history",
    response_model=list[ActualRealizationHistoryResponse],
    operation_id="temporal_list_actual_history",
)
async def list_actual_history(
    actual_ref: UUID,
    context: Context,
    application: Application,
) -> list[ActualRealizationHistoryResponse]:
    try:
        views = await application.history(
            self_person_ref=context.self_person_ref,
            actual_ref=ScopedRecordRef(actual_ref),
        )
    except (ActualNotFoundError, ActualPersistenceError) as exc:
        raise _problem(exc) from exc
    return [_history_response(view) for view in views]
