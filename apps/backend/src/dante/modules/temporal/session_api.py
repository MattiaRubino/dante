"""B08 HTTP surface for Session runtime commands and authoritative reads."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionCaptureDisabledError,
    SessionEditorConflictError,
    SessionEditorWrite,
    SessionEndConflictError,
    SessionInputError,
    SessionNotFoundError,
    SessionOperationReuseError,
    SessionPauseConflictError,
    SessionPersistenceError,
    SessionResumeConflictError,
    SessionView,
)
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class SessionCommand(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)


class SessionEndCommand(SessionCommand):
    expected_material_state_ref: UUID = Field(strict=False)


class SessionManualCommand(SessionCommand):
    started_at: datetime = Field(strict=False)
    ended_at: datetime = Field(strict=False)


class SessionEditorPause(BaseModel):
    model_config = ConfigDict(extra="forbid")
    started_at: datetime
    ended_at: datetime | None


class SessionEditorPauseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    started_at: datetime
    ended_at: datetime


class SessionEditorCommand(SessionCommand):
    started_at: datetime = Field(strict=False)
    ended_at: datetime = Field(strict=False)
    planned_schedule_ref: UUID | None = Field(default=None, strict=False)
    session_ref: UUID | None = Field(default=None, strict=False)
    expected_material_state_ref: UUID | None = Field(default=None, strict=False)
    pause_ranges: list[SessionEditorPauseInput] = Field(default_factory=list, max_length=99)



class SessionEditorBatchCommand(BaseModel):
    """Atomic group of corrections and new concluded recordings."""

    model_config = ConfigDict(extra="forbid", strict=True)

    commands: list[SessionEditorCommand] = Field(min_length=1, max_length=101)


class SessionEditorAttempt(BaseModel):
    session_ref: UUID
    planned_schedule_ref: UUID | None
    timing_material_state_ref: UUID
    started_at: datetime
    ended_at: datetime | None
    pause_ranges: list[SessionEditorPause]


SessionTransitionCommand = SessionEndCommand


class SessionDurationEvaluationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constraint_ref: UUID
    material_state_ref: UUID
    minimum_duration_microseconds: int = Field(gt=0)
    strength: Literal["soft"]
    evaluation: Literal["pending", "satisfied", "violated"]


class SessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_ref: UUID
    planned_schedule_ref: UUID | None = None
    subject_native_ref: UUID
    timing_material_state_ref: UUID
    started_at: datetime
    ended_at: datetime | None
    open: bool
    replayed: bool
    paused: bool
    evaluated_at: datetime
    elapsed_seconds: float = Field(ge=0)
    paused_seconds: float = Field(ge=0)
    active_seconds: float = Field(ge=0)
    duration_evaluations: list[SessionDurationEvaluationResponse]


def _application(request: Request) -> SessionApplication:
    return SessionApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[SessionApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: SessionView) -> SessionResponse:
    if view.evaluated_at is None:
        raise SessionPersistenceError("Session runtime metrics are unavailable.")
    return SessionResponse(
        session_ref=view.session_ref,
        planned_schedule_ref=view.planned_schedule_ref,
        subject_native_ref=view.subject_native_ref,
        timing_material_state_ref=view.timing_material_state_ref,
        started_at=view.started_at,
        ended_at=view.ended_at,
        open=view.open,
        replayed=view.replayed,
        paused=view.paused,
        evaluated_at=view.evaluated_at,
        elapsed_seconds=view.elapsed_seconds,
        paused_seconds=view.paused_seconds,
        active_seconds=view.active_seconds,
        duration_evaluations=[
            SessionDurationEvaluationResponse(
                constraint_ref=evaluation.constraint_ref,
                material_state_ref=evaluation.material_state_ref,
                minimum_duration_microseconds=evaluation.minimum_duration_microseconds,
                strength=evaluation.strength,
                evaluation=evaluation.evaluation,
            )
            for evaluation in view.duration_evaluations
        ],
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, SessionCaptureDisabledError):
        return ProblemError(
            status=409,
            code="temporal.session.capture_disabled",
            category="conflict",
            title="Session capture disabled",
            detail="Enable the requested Session capture mode on this Activity.",
        )
    if isinstance(exc, SessionInputError):
        return ProblemError(
            status=422,
            code="temporal.session.invalid_input",
            category="validation",
            title="Session command rejected",
            detail=str(exc),
        )
    if isinstance(exc, SessionNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.session.not_found",
            category="not_found",
            title="Session subject unavailable",
            detail=str(exc),
        )
    if isinstance(exc, SessionOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.session.operation_id_reused",
            category="conflict",
            title="Session operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, SessionEditorConflictError):
        return ProblemError(
            status=409,
            code="temporal.session.editor_conflict",
            category="conflict",
            title="Session recording changed",
            detail=str(exc),
        )
    if isinstance(exc, SessionEndConflictError):
        return ProblemError(
            status=409,
            code="temporal.session.end_conflict",
            category="conflict",
            title="Session end conflict",
            detail=str(exc),
        )
    if isinstance(exc, SessionPauseConflictError):
        return ProblemError(
            status=409,
            code="temporal.session.pause_conflict",
            category="conflict",
            title="Session pause conflict",
            detail=str(exc),
        )
    if isinstance(exc, SessionResumeConflictError):
        return ProblemError(
            status=409,
            code="temporal.session.resume_conflict",
            category="conflict",
            title="Session resume conflict",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.session.persistence",
        category="conflict",
        title="Session command rejected",
        detail="Session command was rejected.",
    )


async def _start(
    subject_kind: Literal["activity", "occurrence"],
    subject_ref: UUID,
    payload: SessionCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    try:
        view = await application.start(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_ref),
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionPersistenceError,
        SessionCaptureDisabledError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


@router.post(
    "/activities/{activity_ref}/sessions",
    response_model=SessionResponse,
    operation_id="temporal_start_activity_session",
)
async def start_activity_session(
    activity_ref: UUID,
    payload: SessionCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    return await _start("activity", activity_ref, payload, context, application, response)


@router.post(
    "/activities/{activity_ref}/planned-sessions/{schedule_ref}/sessions",
    response_model=SessionResponse,
    operation_id="temporal_start_planned_activity_session",
)
async def start_planned_activity_session(
    activity_ref: UUID,
    schedule_ref: UUID,
    payload: SessionCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    try:
        view = await application.start_planned(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            activity_ref=NativeRef(activity_ref),
            schedule_ref=ScopedRecordRef(schedule_ref),
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionPersistenceError,
        SessionCaptureDisabledError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)


@router.post(
    "/occurrences/{occurrence_ref}/sessions",
    response_model=SessionResponse,
    operation_id="temporal_start_occurrence_session",
)
async def start_occurrence_session(
    occurrence_ref: UUID,
    payload: SessionCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    return await _start("occurrence", occurrence_ref, payload, context, application, response)


@router.post(
    "/activities/{activity_ref}/sessions/manual",
    response_model=SessionResponse,
    operation_id="temporal_record_manual_activity_session",
)
async def record_manual_activity_session(
    activity_ref: UUID,
    payload: SessionManualCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    try:
        view = await application.record_manual(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            activity_ref=NativeRef(activity_ref),
            started_at=payload.started_at,
            ended_at=payload.ended_at,
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionPersistenceError,
        SessionCaptureDisabledError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed else 201
    return _response(view)



@router.post(
    "/activities/{activity_ref}/sessions/editor/batch",
    response_model=list[SessionResponse],
    operation_id="temporal_write_activity_session_editor_batch",
)
async def write_activity_session_editor_batch(
    activity_ref: UUID,
    payload: SessionEditorBatchCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> list[SessionResponse]:
    try:
        views = await application.write_editor_batch(
            self_person_ref=context.self_person_ref,
            activity_ref=NativeRef(activity_ref),
            commands=tuple(
                SessionEditorWrite(
                    operation_id=command.operation_id,
                    planned_schedule_ref=(
                        ScopedRecordRef(command.planned_schedule_ref)
                        if command.planned_schedule_ref is not None
                        else None
                    ),
                    session_ref=NativeRef(command.session_ref) if command.session_ref else None,
                    expected_material_state_ref=(
                        MaterialStateRef(command.expected_material_state_ref)
                        if command.expected_material_state_ref
                        else None
                    ),
                    started_at=command.started_at,
                    ended_at=command.ended_at,
                    pause_ranges=tuple(
                        (item.started_at, item.ended_at) for item in command.pause_ranges
                    ),
                )
                for command in payload.commands
            ),
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionPersistenceError,
        SessionCaptureDisabledError,
        SessionEditorConflictError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = (
        200
        if all(view.replayed for view in views)
        or all(command.session_ref is not None for command in payload.commands)
        else 201
    )
    response.headers["Cache-Control"] = "no-store"
    return [_response(view) for view in views]


@router.get(
    "/activities/{activity_ref}/sessions/editor",
    response_model=list[SessionEditorAttempt],
    operation_id="temporal_list_activity_session_editor_attempts",
)
async def list_activity_session_editor_attempts(
    activity_ref: UUID,
    context: Context,
    request: Request,
    response: Response,
) -> list[SessionEditorAttempt]:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            result = await session.execute(
                text(
                    "SELECT * FROM dante.list_self_activity_session_editor_attempts(:actor,:activity)"
                ),
                {"actor": context.self_person_ref, "activity": activity_ref},
            )
            return [SessionEditorAttempt.model_validate(dict(row)) for row in result.mappings()]
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.session.unavailable",
            category="unavailable",
            title="Session recordings unavailable",
            detail="Riprova a caricare le registrazioni.",
        ) from exc


@router.post(
    "/activities/{activity_ref}/sessions/editor",
    response_model=SessionResponse,
    operation_id="temporal_write_activity_session_editor_attempt",
)
async def write_activity_session_editor_attempt(
    activity_ref: UUID,
    payload: SessionEditorCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    try:
        view = await application.write_editor(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            activity_ref=NativeRef(activity_ref),
            planned_schedule_ref=(
                ScopedRecordRef(payload.planned_schedule_ref)
                if payload.planned_schedule_ref is not None
                else None
            ),
            session_ref=NativeRef(payload.session_ref) if payload.session_ref else None,
            expected_material_state_ref=(
                MaterialStateRef(payload.expected_material_state_ref)
                if payload.expected_material_state_ref
                else None
            ),
            started_at=payload.started_at,
            ended_at=payload.ended_at,
            pause_ranges=[(row.started_at, row.ended_at) for row in payload.pause_ranges],
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionPersistenceError,
        SessionCaptureDisabledError,
        SessionEditorConflictError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200 if view.replayed or payload.session_ref else 201
    response.headers["Cache-Control"] = "no-store"
    return _response(view)


@router.get(
    "/activities/{activity_ref}/sessions",
    response_model=list[SessionResponse],
    operation_id="temporal_list_activity_sessions",
)
async def list_activity_sessions(
    activity_ref: UUID,
    context: Context,
    application: Application,
) -> list[SessionResponse]:
    try:
        views = await application.list_for_subject(
            self_person_ref=context.self_person_ref,
            subject_native_ref=NativeRef(activity_ref),
        )
    except (SessionNotFoundError, SessionPersistenceError) as exc:
        raise _problem(exc) from exc
    return [_response(view) for view in views]


@router.get(
    "/occurrences/{occurrence_ref}/sessions",
    response_model=list[SessionResponse],
    operation_id="temporal_list_occurrence_sessions",
)
async def list_occurrence_sessions(
    occurrence_ref: UUID,
    context: Context,
    application: Application,
) -> list[SessionResponse]:
    try:
        views = await application.list_for_subject(
            self_person_ref=context.self_person_ref,
            subject_native_ref=NativeRef(occurrence_ref),
        )
    except (SessionNotFoundError, SessionPersistenceError) as exc:
        raise _problem(exc) from exc
    return [_response(view) for view in views]


@router.get(
    "/sessions/{session_ref}",
    response_model=SessionResponse,
    operation_id="temporal_get_session",
)
async def get_session(
    session_ref: UUID,
    context: Context,
    application: Application,
) -> SessionResponse:
    try:
        view = await application.get(
            self_person_ref=context.self_person_ref,
            session_ref=NativeRef(session_ref),
        )
    except (SessionNotFoundError, SessionPersistenceError) as exc:
        raise _problem(exc) from exc
    return _response(view)


@router.post(
    "/sessions/{session_ref}/end",
    response_model=SessionResponse,
    operation_id="temporal_end_session",
)
async def end_session(
    session_ref: UUID,
    payload: SessionEndCommand,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> SessionResponse:
    try:
        view = await application.end(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            session_ref=NativeRef(session_ref),
            expected_material_state_ref=MaterialStateRef(payload.expected_material_state_ref),
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionEndConflictError,
        SessionPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = 200
    return _response(view)


async def _transition(
    command: Literal["pause", "resume"],
    session_ref: UUID,
    payload: SessionTransitionCommand,
    context: MutatingContext,
    application: Application,
) -> SessionResponse:
    try:
        view = await getattr(application, command)(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            session_ref=NativeRef(session_ref),
            expected_material_state_ref=MaterialStateRef(payload.expected_material_state_ref),
        )
    except (
        SessionInputError,
        SessionNotFoundError,
        SessionOperationReuseError,
        SessionPauseConflictError,
        SessionResumeConflictError,
        SessionPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    return _response(view)


@router.post(
    "/sessions/{session_ref}/pause",
    response_model=SessionResponse,
    operation_id="temporal_pause_session",
)
async def pause_session(
    session_ref: UUID,
    payload: SessionTransitionCommand,
    context: MutatingContext,
    application: Application,
) -> SessionResponse:
    return await _transition("pause", session_ref, payload, context, application)


@router.post(
    "/sessions/{session_ref}/resume",
    response_model=SessionResponse,
    operation_id="temporal_resume_session",
)
async def resume_session(
    session_ref: UUID,
    payload: SessionTransitionCommand,
    context: MutatingContext,
    application: Application,
) -> SessionResponse:
    return await _transition("resume", session_ref, payload, context, application)
