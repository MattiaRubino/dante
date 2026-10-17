"""Read-only product inbox derived from accepted owner/runtime state.

The inbox has no independent truth or generic resolution mutation. Each item
routes to its owning vertical: B10 Reconciliation or B10 Actual realization.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Any, Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.session_panel_api import _bounds
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
ResolutionReason = Literal[
    "reconciliation_open", "realization_review", "objective_review", "session_unstarted"
]
ResolutionAction = Literal["open_reconciliation", "record_realization", "open_objectives"]


class ResolutionQueueItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason_code: ResolutionReason
    subject_kind: Literal["activity", "event", "occurrence"]
    subject_ref: UUID
    title: str
    summary: str
    effective_at: datetime
    reconciliation_ref: UUID | None
    outcome_ref: UUID | None
    purpose_code: str
    session_ref: UUID | None
    session_timing_material_state_ref: UUID | None
    actions: list[ResolutionAction]
    planned_schedule_ref: UUID | None = None


class ResolutionQueueResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ResolutionQueueItem]
    count: int


def _item(row: RowMapping) -> ResolutionQueueItem:
    values = dict(row)  # SQLAlchemy RowMapping -> ordinary validated payload.
    reason = values["reason_code"]
    if reason == "reconciliation_open":
        return ResolutionQueueItem(
            **values,
            summary="An accepted Outcome has an open reconciliation decision.",
            actions=["open_reconciliation"],
        )
    if reason == "realization_review":
        return ResolutionQueueItem(
            **values,
            summary=(
                "A past planned interval needs an explicit Reality decision."
                if values["purpose_code"] == "activity.policy.past_unstarted"
                else "The requested Reality review is ready."
            ),
            actions=["record_realization"],
        )
    if reason == "objective_review":
        return ResolutionQueueItem(
            **values,
            summary="One or more Objectives are ready for assessment.",
            actions=["open_objectives"],
        )
    raise ValueError("Unsupported resolution queue reason.")


_UNSTARTED_INPUT = text("""
    SELECT owner.*,
           COALESCE((
               SELECT jsonb_agg(jsonb_build_object(
                   'planned_schedule_ref',
                   dante.get_self_session_planned_schedule(:actor,attempt.session_ref),
                   'ended_at', attempt.ended_at
               ))
                 FROM dante.list_self_subject_sessions(:actor,owner.activity_ref) AS attempt
           ),'[]'::jsonb) AS historical_attempts
      FROM dante.list_self_session_panel_inputs(:actor) AS owner
""")


def _unstarted_session_items(
    records: list[Any], now: datetime, zone_id: str
) -> list[ResolutionQueueItem]:
    """Project unstarted Sessions on plan expiry or explicit main Stop.

    A stopped main is a real accepted execution fact, not an inferred
    completion of its never-started children. Neither trigger starts or
    completes a child; the queue remains a read-only review projection.
    """
    zone = ZoneInfo(zone_id)
    result: list[ResolutionQueueItem] = []
    for owner in records:
        schedules = [ActivityScheduleResponse.model_validate(row) for row in owner["schedules"]]
        intervals = [schedule for schedule in schedules if schedule.role_code == "interval"]
        if not intervals:
            intervals = [
                schedule for schedule in schedules if schedule.role_code in {None, "envelope"}
            ]
        bounds = [_bounds(schedule, zone) for schedule in intervals]
        plan_ended_at = (
            max(bound[1] for bound in bounds if bound is not None)
            if bounds and all(bound is not None and bound[1] <= now for bound in bounds)
            else None
        )
        # A deliberate Stop of the main Activity Session is sufficient to
        # require review of configured children that have *never* been
        # started. Waiting for a future Schedule end silently loses that user
        # decision. Keep the fact separate from the accepted placement.
        ended_main_attempts = [
            datetime.fromisoformat(str(attempt["ended_at"]).replace("Z", "+00:00"))
            for attempt in owner["historical_attempts"]
            if attempt.get("planned_schedule_ref") is None
            and attempt.get("ended_at") is not None
        ]
        last_main_stop = max(
            (
                stopped_at
                for stopped_at in ended_main_attempts
                if stopped_at.tzinfo is not None and stopped_at <= now
            ),
            default=None,
        )
        if plan_ended_at is None and last_main_stop is None:
            continue
        effective_at = (
            last_main_stop
            if plan_ended_at is None
            else plan_ended_at
            if last_main_stop is None
            else max(plan_ended_at, last_main_stop)
        )
        attempted = {
            UUID(str(attempt["planned_schedule_ref"]))
            if attempt["planned_schedule_ref"] is not None
            else None
            for attempt in owner["historical_attempts"]
        }
        candidates: list[tuple[UUID | None, str]] = []
        if owner["mode_code"] in {"live", "record_and_live"}:
            candidates.append((None, "Sessione attività"))
        candidates.extend(
            (schedule.schedule_ref, schedule.display_name or "Sessione interna")
            for schedule in schedules
            if schedule.role_code == "planned"
        )
        for planned_ref, name in candidates:
            if planned_ref in attempted:
                continue
            result.append(
                ResolutionQueueItem(
                    reason_code="session_unstarted",
                    subject_kind="activity",
                    subject_ref=UUID(str(owner["activity_ref"])),
                    title=str(owner["title"]),
                    summary=f"{name} · mai avviata",
                    effective_at=effective_at,
                    reconciliation_ref=None,
                    outcome_ref=None,
                    purpose_code="activity.session.unstarted",
                    session_ref=None,
                    session_timing_material_state_ref=None,
                    planned_schedule_ref=planned_ref,
                    actions=[],
                )
            )
    return result


@router.get(
    "/resolution-queue",
    response_model=ResolutionQueueResponse,
    operation_id="temporal_list_resolution_queue",
)
async def list_resolution_queue(request: Request, context: Context) -> ResolutionQueueResponse:
    """Derived current product work, never inferred failure from time passage.

    A past planned Activity without execution may enter Reality review only
    under explicit review/auto policy, or Objective review when an Objective
    awaits assessment. A separately typed read-only item shows every enabled
    Session with no attempt when the current Activity plan is wholly past
    or the real main Activity Session was explicitly stopped. Absence of
    Actual never means that the subject did not happen.
    """
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            rows = (
                (
                    await session.execute(
                        text(
                            "SELECT queue.* FROM dante.list_self_resolution_queue("
                            ":self_person_ref,:effective_zone_id) AS queue "
                            "WHERE queue.subject_kind <> 'activity' OR NOT EXISTS ("
                            "SELECT 1 FROM dante.activity_intention AS activity "
                            "WHERE activity.activity_ref=queue.subject_ref "
                            "AND activity.self_person_ref=:self_person_ref "
                            "AND activity.retired_at IS NOT NULL)"
                        ),
                        {
                            "self_person_ref": context.self_person_ref,
                            "effective_zone_id": context.effective_zone_id,
                        },
                    )
                )
                .mappings()
                .all()
            )
            items = [_item(row) for row in rows]
            session_inputs = (
                (await session.execute(_UNSTARTED_INPUT, {"actor": context.self_person_ref}))
                .mappings()
                .all()
            )
            items.extend(
                _unstarted_session_items(
                    list(session_inputs), datetime.now(UTC), context.effective_zone_id
                )
            )
            items.sort(key=lambda item: item.effective_at, reverse=True)
    except (SQLAlchemyError, ValueError) as exc:
        raise ProblemError(
            status=503,
            code="temporal.resolution_queue.unavailable",
            category="service",
            title="Resolution queue unavailable",
            detail="The canonical resolution queue could not be read.",
            retryable=True,
        ) from exc

    return ResolutionQueueResponse(items=items, count=len(items))


# B14 Home rail: independent history and pending Objective work, not B10 inbox.
class FinishedWorkItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: Literal["activity", "event"]
    subject_ref: UUID
    title: str
    session_ref: UUID | None
    started_at: datetime | None
    ended_at: datetime
    record_kind: Literal["session_ended", "realization_occurred"]


class ObjectiveWorkItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    objective_ref: UUID
    subject_kind: Literal["activity", "event", "occurrence"]
    subject_ref: UUID
    subject_title: str
    label: str
    result_kind: Literal["boolean", "quantity", "qualitative", "range"]
    presentation_order: int
    draft_revision: int | None
    draft_updated_at: datetime | None


@router.get(
    "/home/finished-work",
    response_model=list[FinishedWorkItem],
    operation_id="temporal_list_home_finished_work",
)
async def list_home_finished_work(
    request: Request,
    context: Context,
    response: Response,
    limit: int = 40,
) -> list[FinishedWorkItem]:
    response.headers["Cache-Control"] = "no-store"
    if not 1 <= limit <= 100:
        raise ProblemError(
            status=422,
            code="temporal.home.invalid_limit",
            category="validation",
            title="Invalid limit",
            detail="Richiedi da 1 a 100 elementi.",
        )
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            rows = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.list_self_home_finished_work(:actor,:limit)"),
                        {"actor": context.self_person_ref, "limit": limit},
                    )
                )
                .mappings()
                .all()
            )
            return [FinishedWorkItem.model_validate(dict(row)) for row in rows]
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.home.finished_unavailable",
            category="service",
            title="Finished work unavailable",
            detail="Storico conclusi non disponibile.",
            retryable=True,
        ) from exc


@router.get(
    "/home/objective-work",
    response_model=list[ObjectiveWorkItem],
    operation_id="temporal_list_home_objective_work",
)
async def list_home_objective_work(
    request: Request,
    context: Context,
    response: Response,
    limit: int = 40,
) -> list[ObjectiveWorkItem]:
    response.headers["Cache-Control"] = "no-store"
    if not 1 <= limit <= 100:
        raise ProblemError(
            status=422,
            code="temporal.home.invalid_limit",
            category="validation",
            title="Invalid limit",
            detail="Richiedi da 1 a 100 Obiettivi.",
        )
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            rows = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.list_self_home_objective_work(:actor,:limit)"),
                        {"actor": context.self_person_ref, "limit": limit},
                    )
                )
                .mappings()
                .all()
            )
            return [ObjectiveWorkItem.model_validate(dict(row)) for row in rows]
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.home.objectives_unavailable",
            category="service",
            title="Objective work unavailable",
            detail="Obiettivi da valutare non disponibili.",
            retryable=True,
        ) from exc
