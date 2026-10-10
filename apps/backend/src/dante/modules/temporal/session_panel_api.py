"""Read-only, actor-scoped execution desk; never starts work on clock passage."""

from __future__ import annotations

from datetime import UTC, datetime, time, timedelta
from typing import Annotated, Any
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
PREVIEW_LEAD = timedelta(minutes=5)  # v1 approved product constant, not a user setting


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


class SessionPanelPauseRange(BaseModel):
    started_at: datetime
    ended_at: datetime | None


class SessionPanelVisual(BaseModel):
    activity_ref: UUID
    session_ref: UUID
    planned_schedule_ref: UUID | None
    started_at: datetime
    ended_at: datetime | None
    pause_ranges: list[SessionPanelPauseRange]


class SessionPanelResponse(BaseModel):
    evaluated_at: datetime
    next_change_at: datetime | None
    groups: list[SessionPanelGroup]
    visuals: list[SessionPanelVisual] = Field(default_factory=list)


# The DEFINER capability owns the table access and performs the self check.
_READ = text("SELECT * FROM dante.list_self_session_panel_inputs(:actor)")
_VISUAL_READ = text(
    "SELECT * FROM dante.list_self_activity_session_visuals(:actor,:start_at,:end_at)"
)


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


def build_panel(
    records: list[Any],
    now: datetime,
    zone_id: str,
    ended_executions: list[Any] | None = None,
) -> SessionPanelResponse:
    zone = ZoneInfo(zone_id)
    stopped = [item for item in (ended_executions or []) if item["ended_at"] is not None]
    groups: list[SessionPanelGroup] = []
    changes: list[datetime] = []
    for owner in records:
        schedules = [ActivityScheduleResponse.model_validate(s) for s in owner["schedules"]]
        bounds = {s.schedule_ref: _bounds(s, zone) for s in schedules}
        for schedule in schedules:
            boundary = bounds[schedule.schedule_ref]
            if not boundary:
                continue
            start, end = boundary
            changes.extend(value for value in (start, end) if value > now)
            # Only exact-timed boundaries have a meaningful five-minute preview.
            if schedule.temporal_form in {"absolute", "named_zone_local", "floating_local"}:
                preview = start - PREVIEW_LEAD
                if preview > now:
                    changes.append(preview)
        intervals = [s for s in schedules if s.role_code == "interval"]
        if not intervals:
            intervals = [s for s in schedules if s.role_code in {None, "envelope"}]
        active = any(
            b is not None and b[0] <= now < b[1] for s in intervals
            if (b := bounds[s.schedule_ref])
        )
        def ended_during_current_window(
            planned_ref: UUID | None, windows: list[tuple[datetime, datetime]]
        ) -> bool:
            # Stop removes the finished attempt from the operational desk.
            # Re-entering the same planned window does not manufacture a
            # fresh "ready" execution on every polling tick or page refresh.
            return any(
                str(item["activity_ref"]) == str(owner["activity_ref"])
                and (
                    str(item["planned_schedule_ref"])
                    if item["planned_schedule_ref"] is not None else None
                ) == (str(planned_ref) if planned_ref is not None else None)
                and any(
                    item["started_at"] < end
                    and item["ended_at"] >= start - PREVIEW_LEAD
                    for start, end in windows
                )
                for item in stopped
            )

        current_windows = [
            b for schedule in intervals if (b := bounds[schedule.schedule_ref])
            and b[0] - PREVIEW_LEAD <= now < b[1]
        ]
        upcoming = any(
            b is not None and b[0] - PREVIEW_LEAD <= now < b[1]
            if s.temporal_form in {"absolute", "named_zone_local", "floating_local"}
            else b is not None and b[0] <= now < b[1]
            for s in intervals if (b := bounds[s.schedule_ref])
        )
        main_stopped_in_window = ended_during_current_window(None, current_windows)
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
            if timing:
                preview_allowed = schedule.temporal_form in {
                    "absolute", "named_zone_local", "floating_local"
                }
                due = timing[0] - (PREVIEW_LEAD if preview_allowed else timedelta()) <= now < timing[1]
            else:
                due = active
            due = (
                due and owner["mode_code"] in {"live", "record_and_live", "internal_only"}
                and not main_stopped_in_window
            )
            windows = [timing] if timing else current_windows
            if due and not matching and ended_during_current_window(
                schedule.schedule_ref, windows
            ):
                due = False
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
        # A main execution clock is independent from the named planned slices.
        # It coexists with them; it is not an extra fake planned Session.
        if generic or (
            upcoming and owner["mode_code"] in {"live", "record_and_live"}
            and not main_stopped_in_window
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
    visible_start_at: datetime | None = None,
    visible_end_at: datetime | None = None,
) -> SessionPanelResponse:
    response.headers["Cache-Control"] = "no-store"
    now = datetime.now(UTC)
    start_at = visible_start_at or now - timedelta(days=1)
    end_at = visible_end_at or now + timedelta(days=2)
    if (
        start_at.tzinfo is None or end_at.tzinfo is None
        or start_at >= end_at or end_at - start_at > timedelta(days=31)
    ):
        raise ProblemError(
            status=422, code="temporal.session_panel.invalid_window",
            category="validation", title="Invalid Session window",
            detail="L'intervallo di lettura delle Sessioni non è valido.",
        )
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("SET LOCAL statement_timeout = '8s'"))
            records = (
                (await session.execute(_READ, {"actor": context.self_person_ref})).mappings().all()
            )
            visuals = (
                (await session.execute(
                    _VISUAL_READ,
                    {"actor": context.self_person_ref, "start_at": start_at, "end_at": end_at},
                )).mappings().all()
            )
            # The desk always follows server "now", even if the user is
            # viewing a distant Timeline date whose visual range omits today.
            finished = visuals
            if not (start_at <= now < end_at):
                finished = (
                    (await session.execute(
                        _VISUAL_READ,
                        {
                            "actor": context.self_person_ref,
                            "start_at": now - timedelta(days=1),
                            "end_at": now + timedelta(days=1),
                        },
                    )).mappings().all()
                )
            panel = build_panel(
                list(records), now, context.effective_zone_id, list(finished)
            )
            return panel.model_copy(update={
                "visuals": [SessionPanelVisual.model_validate(dict(row)) for row in visuals]
            })
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.session_panel.unavailable",
            category="service",
            title="Session panel unavailable",
            detail="Le sessioni non sono disponibili. Riprova.",
            retryable=True,
        ) from exc
