"""B11-C self-scoped Schedule Reminder HTTP contract."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.schedule_reminder import (
    ScheduleReminderApplication,
    ScheduleReminderConflictError,
    ScheduleReminderInputError,
    ScheduleReminderNotFoundError,
    ScheduleReminderPersistenceError,
    ScheduleReminderView,
)
from dante.platform.database.references import MaterialStateRef, ScopedRecordRef
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class ScheduleReminderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID | None = None
    enabled: bool
    lead_minutes: int = Field(ge=0, le=10080)


class ScheduleReminderResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reminder_ref: UUID
    schedule_ref: UUID
    material_state_ref: UUID
    enabled: bool
    lead_minutes: int
    schedule_starts_at: datetime | None
    due_at: datetime | None
    disposition_code: Literal["pending", "due", "unavailable"]
    replayed: bool


def _application(request: Request) -> ScheduleReminderApplication:
    return ScheduleReminderApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[ScheduleReminderApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ScheduleReminderInputError):
        return ProblemError(
            status=422, code="temporal.reminder.invalid_input", category="validation",
            title="Reminder configuration rejected", detail=str(exc),
        )
    if isinstance(exc, ScheduleReminderNotFoundError):
        return ProblemError(
            status=404, code="temporal.reminder.schedule_unavailable", category="not_found",
            title="Schedule unavailable for Reminder", detail=str(exc),
        )
    if isinstance(exc, ScheduleReminderConflictError):
        return ProblemError(
            status=409, code="temporal.reminder.conflict", category="conflict",
            title="Reminder current state conflict", detail=str(exc),
        )
    return ProblemError(
        status=409, code="temporal.reminder.persistence", category="conflict",
        title="Reminder command rejected", detail="Reminder command was rejected.",
    )


def _response(view: ScheduleReminderView) -> ScheduleReminderResponse:
    return ScheduleReminderResponse(
        reminder_ref=view.reminder_ref,
        schedule_ref=view.schedule_ref,
        material_state_ref=view.material_state_ref,
        enabled=view.enabled,
        lead_minutes=view.lead_minutes,
        schedule_starts_at=view.schedule_starts_at,
        due_at=view.due_at,
        disposition_code=view.disposition_code,
        replayed=view.replayed,
    )


@router.get(
    "/schedules/{schedule_ref}/reminder",
    response_model=ScheduleReminderResponse,
    responses={
        400: {"model": ProblemDetails, "description": "Malformed request."},
        401: {"model": ProblemDetails, "description": "Authentication required."},
        404: {"model": ProblemDetails, "description": "Reminder unavailable."},
        500: {"model": ProblemDetails, "description": "Unexpected server error."},
    },
    operation_id="temporal_get_schedule_reminder",
)
async def get_schedule_reminder(
    schedule_ref: UUID, context: Context, application: Application,
) -> ScheduleReminderResponse:
    try:
        view = await application.get(
            self_person_ref=context.self_person_ref,
            schedule_ref=ScopedRecordRef(schedule_ref),
        )
    except (ScheduleReminderNotFoundError, ScheduleReminderPersistenceError) as exc:
        raise _problem(exc) from exc
    if view is None:
        raise _problem(ScheduleReminderNotFoundError("Reminder unavailable."))
    return _response(view)


@router.put(
    "/schedules/{schedule_ref}/reminder",
    response_model=ScheduleReminderResponse,
    status_code=201,
    responses={
        200: {"model": ScheduleReminderResponse, "description": "Revision or idempotent replay."},
        400: {"model": ProblemDetails, "description": "Malformed request."},
        401: {"model": ProblemDetails, "description": "Authentication required."},
        403: {"model": ProblemDetails, "description": "Mutation rejected by security policy."},
        404: {"model": ProblemDetails, "description": "Exact-start self Schedule unavailable."},
        409: {"model": ProblemDetails, "description": "Current-state or operation conflict."},
        422: {"model": ProblemDetails, "description": "Reminder input rejected."},
        500: {"model": ProblemDetails, "description": "Unexpected server error."},
    },
    operation_id="temporal_configure_schedule_reminder",
)
async def configure_schedule_reminder(
    schedule_ref: UUID,
    payload: ScheduleReminderRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ScheduleReminderResponse:
    try:
        view = await application.configure(
            self_person_ref=context.self_person_ref,
            schedule_ref=ScopedRecordRef(schedule_ref),
            operation_id=payload.operation_id,
            expected_material_state_ref=(
                MaterialStateRef(payload.expected_material_state_ref)
                if payload.expected_material_state_ref is not None else None
            ),
            enabled=payload.enabled,
            lead_minutes=payload.lead_minutes,
        )
    except (
        ScheduleReminderInputError, ScheduleReminderNotFoundError,
        ScheduleReminderConflictError, ScheduleReminderPersistenceError,
    ) as exc:
        raise _problem(exc) from exc
    response.status_code = (
        200 if view.replayed or payload.expected_material_state_ref is not None else 201
    )
    return _response(view)
