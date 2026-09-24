"""B08-A HTTP surface for Session start, read, and end."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.session_runtime import (
    SessionApplication,
    SessionEndConflictError,
    SessionInputError,
    SessionNotFoundError,
    SessionOperationReuseError,
    SessionPauseConflictError,
    SessionPersistenceError,
    SessionResumeConflictError,
    SessionView,
)
from dante.platform.database.references import MaterialStateRef, NativeRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class SessionCommand(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)


class SessionEndCommand(SessionCommand):
    expected_material_state_ref: UUID

SessionTransitionCommand = SessionEndCommand

class SessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_ref: UUID
    subject_native_ref: UUID
    timing_material_state_ref: UUID
    started_at: datetime
    ended_at: datetime | None
    open: bool
    replayed: bool
    paused: bool


def _application(request: Request) -> SessionApplication:
    return SessionApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[SessionApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _response(view: SessionView) -> SessionResponse:
    return SessionResponse(
        session_ref=view.session_ref,
        subject_native_ref=view.subject_native_ref,
        timing_material_state_ref=view.timing_material_state_ref,
        started_at=view.started_at,
        ended_at=view.ended_at,
        open=view.open,
        replayed=view.replayed,
        paused=view.paused,
    )


def _problem(exc: Exception) -> ProblemError:
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
            status=409, code="temporal.session.pause_conflict", category="conflict",
            title="Session pause conflict", detail=str(exc),
        )
    if isinstance(exc, SessionResumeConflictError):
        return ProblemError(
            status=409, code="temporal.session.resume_conflict", category="conflict",
            title="Session resume conflict", detail=str(exc),
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
    response.status_code = 200 if view.replayed else 200
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
