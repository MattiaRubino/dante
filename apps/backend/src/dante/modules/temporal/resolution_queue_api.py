"""Read-only product inbox derived from accepted owner/runtime state.

The inbox has no independent truth or generic resolution mutation. Each item
routes to its owning vertical: B10 Reconciliation or B10 Actual realization.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Annotated, Any, Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query, Request, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.decomposition_api import ActivityScheduleResponse
from dante.modules.temporal.session_panel_api import _bounds
from dante.platform.http.problem import ProblemError
from dante.platform.time import InvalidTimeZoneError, validate_iana_timezone

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
    """Derive never-started review without inventing execution facts.

    Before the first main Play, expired plans need review. While a main
    Session is open (including pause), review is suspended. A real main
    Stop never makes a future plan overdue; once an expired plan is reviewed,
    only its never-started named children remain eligible because the main
    itself was started.
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
        plan_expired = bool(bounds) and all(
            bound is not None and bound[1] <= now for bound in bounds
        )
        plan_ended_at = (
            max(bound[1] for bound in bounds if bound is not None) if plan_expired else None
        )
        history = owner["historical_attempts"]
        main_enabled = owner["mode_code"] in {"live", "record_and_live"}
        main_attempts = [attempt for attempt in history if attempt["planned_schedule_ref"] is None]
        if main_enabled and any(attempt.get("ended_at") is None for attempt in main_attempts):
            # Play/Pause is an open real Session. No "mai avviata" notices
            # while children can still be started under their active main.
            continue
        if plan_ended_at is None:
            continue
        effective_at = plan_ended_at
        attempted = {
            UUID(str(attempt["planned_schedule_ref"]))
            if attempt["planned_schedule_ref"] is not None
            else None
            for attempt in history
        }
        candidates: list[tuple[UUID | None, str]] = []
        if main_enabled and not main_attempts and plan_ended_at is not None:
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
    Unstarted Sessions after plan expiry or real main Stop; no child
    is inferred complete just because its main has an execution history.
    Absence of Actual never means that the subject did not happen.
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
                            "AND activity.retired_at IS NOT NULL) "
                            "AND (queue.reason_code <> 'objective_review' OR EXISTS ("
                            "SELECT 1 FROM dante.list_self_temporal_objectives("
                            ":self_person_ref,queue.subject_kind,queue.subject_ref) objective "
                            "CROSS JOIN LATERAL dante.get_self_objective_verification("
                            ":self_person_ref,objective.objective_ref) mode "
                            "WHERE mode.mode_code='review_on_end' "
                            "AND objective.observation_ref IS NULL))"
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


class ChronologyCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    end_local_at: datetime
    view_date: date


class ChronologyCandidatePage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ChronologyCandidate]
    next_end_local_at: datetime | None
    next_schedule_ref: UUID | None


_CHRONOLOGY_CANDIDATES = text("""
    WITH self_subject AS (
        SELECT 'activity'::text AS kind, a.activity_ref AS ref
          FROM dante.activity_intention AS a
         WHERE a.self_person_ref=:actor AND a.retired_at IS NULL
           AND NOT dante.is_self_recurring_occurrence_superseded(
               :actor,dante.get_self_materialized_activity_occurrence(:actor,a.activity_ref)
           )
        UNION ALL
        SELECT 'event', e.event_ref
          FROM dante.event_expectation AS e
         WHERE e.self_person_ref=:actor
        UNION ALL
        SELECT DISTINCT 'occurrence', o.occurrence_ref
          FROM dante.schedule AS candidate
          JOIN dante.schedule_current_placement AS candidate_current
            ON candidate_current.scoped_owner_ref=candidate.schedule_ref
         CROSS JOIN LATERAL dante.get_self_occurrence(
             :actor,candidate.subject_native_ref
         ) AS o
     LEFT JOIN dante.list_self_routines(:actor) AS r
            ON r.routine_ref=o.source_native_ref
     LEFT JOIN dante.event_expectation AS e
            ON e.event_ref=o.source_native_ref AND e.self_person_ref=:actor
         WHERE (r.routine_ref IS NOT NULL OR e.event_ref IS NOT NULL)
           AND NOT o.skipped
           AND NOT dante.is_self_recurring_occurrence_superseded(:actor,o.occurrence_ref)
    ), placed AS (
        SELECT s.schedule_ref, owner.kind,
               CASE p.temporal_form_code
                   WHEN 'date_span' THEN upper(d.date_span)::timestamp
                   WHEN 'floating_local' THEN f.ends_local_at
                   WHEN 'named_zone_local' THEN timezone(
                       CAST(:zone AS text), n.resolved_end_at
                   )
                   WHEN 'absolute' THEN timezone(
                       CAST(:zone AS text), z.ends_at
                   )
                   WHEN 'coarse_local_period' THEN c.local_date::timestamp + interval '1 day'
               END AS end_key
          FROM self_subject AS owner
          JOIN dante.schedule AS s ON s.subject_native_ref=owner.ref
          JOIN dante.schedule_current_placement AS current
            ON current.scoped_owner_ref=s.schedule_ref
          JOIN dante.schedule_placement_state AS p
            ON p.material_state_ref=current.material_state_ref
           AND p.schedule_ref=s.schedule_ref
     LEFT JOIN dante.schedule_placement_date_state AS d
            ON d.material_state_ref=p.material_state_ref
     LEFT JOIN dante.schedule_placement_floating_local_state AS f
            ON f.material_state_ref=p.material_state_ref AND f.extent_code='interval'
     LEFT JOIN dante.schedule_placement_named_zone_state AS n
            ON n.material_state_ref=p.material_state_ref AND n.extent_code='interval'
     LEFT JOIN dante.schedule_placement_absolute_state AS z
            ON z.material_state_ref=p.material_state_ref AND z.extent_code='interval'
     LEFT JOIN dante.schedule_placement_coarse_local_period_state AS c
            ON c.material_state_ref=p.material_state_ref
     LEFT JOIN LATERAL dante.get_self_activity_schedule_roles(
         :actor, ARRAY[owner.ref]
     ) AS role ON owner.kind='activity' AND role.schedule_ref=s.schedule_ref
         WHERE (owner.kind <> 'activity' OR (
             role.role_code IS DISTINCT FROM 'planned'
             AND (role.role_code IS DISTINCT FROM 'envelope' OR NOT EXISTS (
                 SELECT 1 FROM dante.get_self_activity_schedule_roles(
                     :actor, ARRAY[owner.ref]
                 ) AS occupied WHERE occupied.role_code='interval'
             ))
         ))
           AND (owner.kind <> 'occurrence' OR s.schedule_ref=(
               SELECT candidate.schedule_ref
                 FROM dante.schedule AS candidate
                 JOIN dante.schedule_current_placement AS candidate_current
                   ON candidate_current.scoped_owner_ref=candidate.schedule_ref
                WHERE candidate.subject_native_ref=owner.ref
                ORDER BY candidate.schedule_ref
                LIMIT 1
           ))
    )
    SELECT schedule_ref, end_key AS end_local_at,
           (end_key - interval '1 microsecond')::date AS view_date
      FROM placed
     WHERE end_key IS NOT NULL AND end_key <= :now_local
       AND (CAST(:before_end AS timestamp) IS NULL OR
            (end_key,schedule_ref) < (CAST(:before_end AS timestamp),CAST(:before_ref AS uuid)))
     ORDER BY end_key DESC,schedule_ref DESC
     LIMIT :batch
""")


@router.get(
    "/home/chronology-candidates",
    response_model=ChronologyCandidatePage,
    operation_id="temporal_list_home_chronology_candidates",
)
async def list_home_chronology_candidates(
    request: Request,
    context: Context,
    response: Response,
    before_end_local_at: datetime | None = None,
    before_schedule_ref: UUID | None = None,
    limit: int = 40,
    view_zone_id: Annotated[str | None, Query(include_in_schema=False)] = None,
) -> ChronologyCandidatePage:
    response.headers["Cache-Control"] = "no-store"
    if not 1 <= limit <= 100 or (before_end_local_at is None) != (before_schedule_ref is None) or (
        before_end_local_at is not None and before_end_local_at.tzinfo is not None
    ):
        raise ProblemError(
            status=422,
            code="temporal.home.invalid_chronology_cursor",
            category="validation",
            title="Invalid chronology cursor",
            detail="Richiedi una pagina valida dello storico.",
        )
    try:
        if view_zone_id is not None:
            validate_iana_timezone(view_zone_id)
        zone_id = view_zone_id or context.effective_zone_id
    except InvalidTimeZoneError as exc:
        raise ProblemError(
            status=400,
            code="temporal.home.invalid_chronology_zone",
            category="validation",
            title="Invalid chronology viewing timezone",
            detail="Scegli un fuso orario valido.",
        ) from exc
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            rows = (
                (await session.execute(_CHRONOLOGY_CANDIDATES, {
                    "actor": context.self_person_ref,
                    "zone": zone_id,
                    "now_local": datetime.now(ZoneInfo(zone_id)).replace(tzinfo=None),
                    "before_end": before_end_local_at,
                    "before_ref": before_schedule_ref,
                    "batch": limit + 1,
                })).mappings().all()
            )
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.home.chronology_unavailable",
            category="service",
            title="Chronology unavailable",
            detail="Cronologia non disponibile.",
            retryable=True,
        ) from exc
    items = [ChronologyCandidate.model_validate(dict(row)) for row in rows[:limit]]
    last = items[-1] if len(rows) > limit else None
    return ChronologyCandidatePage(
        items=items,
        next_end_local_at=last.end_local_at if last else None,
        next_schedule_ref=last.schedule_ref if last else None,
    )


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
