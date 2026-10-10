"""Read-only, actor-scoped execution desk; never starts work on clock passage."""

from __future__ import annotations

from datetime import UTC, datetime, time, timedelta
from typing import Annotated, Any
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class SessionPanelExecution(BaseModel):
    session_ref: UUID
    timing_material_state_ref: UUID
    paused: bool


class SessionPanelRow(BaseModel):
    planned_schedule_ref: UUID | None
    name: str
    starts_at: datetime | None
    execution: SessionPanelExecution | None = None


class SessionPanelGroup(BaseModel):
    activity_ref: UUID
    title: str
    rows: list[SessionPanelRow]


class SessionPanelResponse(BaseModel):
    evaluated_at: datetime
    next_change_at: datetime | None
    groups: list[SessionPanelGroup]


# The DEFINER capability owns the table access and performs the self check.
_READ = text("SELECT * FROM dante.list_self_session_panel_inputs(:actor)")


def _bounds(row: ActivityScheduleResponse, zone: ZoneInfo) -> tuple[datetime, datetime] | None:
    if row.temporal_form == "absolute" and row.starts_at and row.ends_at:
        return row.starts_at, row.ends_at
    if row.temporal_form == "named_zone_local" and row.resolved_start_at and row.resolved_end_at:
        return row.resolved_start_at, row.resolved_end_at
    if row.temporal_form == "floating_local" and row.starts_local_at and row.ends_local_at:
        return row.starts_local_at.replace(tzinfo=zone), row.ends_local_at.replace(tzinfo=zone)
    if row.temporal_form == "date_span" and row.start_date and row.end_date_exclusive:
        return (
            datetime.combine(row.start_date, time.min, zone),
            datetime.combine(row.end_date_exclusive, time.min, zone),
        )
    # A coarse period has no exact start. Do not manufacture an hourly deadline.
    if row.temporal_form == "coarse_local_period" and row.local_date:
        return (
            datetime.combine(row.local_date, time.min, zone),
            datetime.combine(row.local_date + timedelta(days=1), time.min, zone),
        )
    return None


def build_panel(records: list[Any], now: datetime, zone_id: str) -> SessionPanelResponse:
    zone = ZoneInfo(zone_id)
    groups: list[SessionPanelGroup] = []
    changes: list[datetime] = []
    for owner in records:
        schedules = [ActivityScheduleResponse.model_validate(s) for s in owner["schedules"]]
        bounds = {s.schedule_ref: _bounds(s, zone) for s in schedules}
        for boundary in bounds.values():
            if boundary:
                changes.extend(value for value in boundary if value > now)
        intervals = [s for s in schedules if s.role_code == "interval"]
        if not intervals:
            intervals = [s for s in schedules if s.role_code in {None, "envelope"}]
        active = any(
            b is not None and b[0] <= now < b[1] for s in intervals if (b := bounds[s.schedule_ref])
        )
        executions: dict[str | None, list[Any]] = {}
        for execution in owner["executions"]:
            ref = (
                str(execution["planned_schedule_ref"])
                if execution["planned_schedule_ref"]
                else None
            )
            executions.setdefault(ref, []).append(execution)
        rows: list[SessionPanelRow] = []
        for schedule in schedules:
            if schedule.role_code != "planned":
                continue
            matching = executions.pop(str(schedule.schedule_ref), [])
            timing = bounds[schedule.schedule_ref]
            due = ((timing[0] <= now < timing[1]) if timing else active) and owner["mode_code"] in {
                "live",
                "record_and_live",
            }
            if not due and not matching:
                continue
            rows.extend(
                SessionPanelRow(
                    planned_schedule_ref=schedule.schedule_ref,
                    name=schedule.display_name or f"Sessione {schedule.presentation_order or 1}",
                    starts_at=timing[0] if timing else None,
                    execution=SessionPanelExecution.model_validate(execution)
                    if execution
                    else None,
                )
                for execution in matching or [None]
            )
        generic = executions.pop(None, [])
        has_planned = any(s.role_code == "planned" for s in schedules)
        if generic or (
            active and not has_planned and owner["mode_code"] in {"live", "record_and_live"}
        ):
            for execution in generic or [None]:
                rows.insert(
                    0,
                    SessionPanelRow(
                        planned_schedule_ref=None,
                        name="Sessione attività",
                        starts_at=None,
                        execution=SessionPanelExecution.model_validate(execution)
                        if execution
                        else None,
                    ),
                )
        # Open work must remain stoppable after timing/placement changes.
        for ref, remaining in executions.items():
            rows.extend(
                SessionPanelRow(
                    planned_schedule_ref=UUID(ref) if ref else None,
                    name="Sessione in corso",
                    starts_at=None,
                    execution=SessionPanelExecution.model_validate(execution),
                )
                for execution in remaining
            )
        if rows:
            groups.append(
                SessionPanelGroup(
                    activity_ref=owner["activity_ref"], title=owner["title"], rows=rows
                )
            )
    return SessionPanelResponse(
        evaluated_at=now, next_change_at=min(changes, default=None), groups=groups
    )


@router.get(
    "/session-panel", response_model=SessionPanelResponse, operation_id="temporal_get_session_panel"
)
async def get_session_panel(
    context: Annotated[DanteContext, Depends(require_dante_context)],
    request: Request,
    response: Response,
) -> SessionPanelResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET LOCAL statement_timeout = '8s'"))
            records = (
                (await session.execute(_READ, {"actor": context.self_person_ref})).mappings().all()
            )
            return build_panel(list(records), datetime.now(UTC), context.effective_zone_id)
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.session_panel.unavailable",
            category="service",
            title="Session panel unavailable",
            detail="Le sessioni non sono disponibili. Riprova.",
            retryable=True,
        ) from exc
