"""Read-only product inbox derived from accepted owner/runtime state.

The inbox has no independent truth or generic resolution mutation. Each item
routes to its owning vertical: B10 Reconciliation or B10 Actual realization.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
ResolutionReason = Literal["reconciliation_open", "realization_review", "objective_review"]
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


class ResolutionQueueResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ResolutionQueueItem]
    count: int


def _item(row: object) -> ResolutionQueueItem:
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
            summary="The requested Reality review is ready.",
            actions=["record_realization"],
        )
    if reason == "objective_review":
        return ResolutionQueueItem(
            **values,
            summary="One or more Objectives are ready for assessment.",
            actions=["open_objectives"],
        )
    raise ValueError("Unsupported resolution queue reason.")


@router.get(
    "/resolution-queue",
    response_model=ResolutionQueueResponse,
    operation_id="temporal_list_resolution_queue",
)
async def list_resolution_queue(
    request: Request, context: Context
) -> ResolutionQueueResponse:
    """Derived current product work, never inferred failure from time passage.

    Reality review requires an explicit review-on-end policy and a completed
    bounded Session (Activity) or ended Event placement. Objectives can request
    assessment independently after the same bounded completion. Absence of
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
    "/home/finished-work", response_model=list[FinishedWorkItem],
    operation_id="temporal_list_home_finished_work",
)
async def list_home_finished_work(
    request: Request, context: Context, response: Response, limit: int = 40,
) -> list[FinishedWorkItem]:
    response.headers["Cache-Control"] = "no-store"
    if not 1 <= limit <= 100:
        raise ProblemError(
            status=422, code="temporal.home.invalid_limit", category="validation",
            title="Invalid limit", detail="Richiedi da 1 a 100 elementi.",
        )
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            rows = (await session.execute(text(
                "SELECT * FROM dante.list_self_home_finished_work(:actor,:limit)"
            ), {"actor": context.self_person_ref, "limit": limit})).mappings().all()
            return [FinishedWorkItem.model_validate(dict(row)) for row in rows]
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.home.finished_unavailable", category="service",
            title="Finished work unavailable", detail="Storico conclusi non disponibile.",
            retryable=True,
        ) from exc


@router.get(
    "/home/objective-work", response_model=list[ObjectiveWorkItem],
    operation_id="temporal_list_home_objective_work",
)
async def list_home_objective_work(
    request: Request, context: Context, response: Response, limit: int = 40,
) -> list[ObjectiveWorkItem]:
    response.headers["Cache-Control"] = "no-store"
    if not 1 <= limit <= 100:
        raise ProblemError(
            status=422, code="temporal.home.invalid_limit", category="validation",
            title="Invalid limit", detail="Richiedi da 1 a 100 Obiettivi.",
        )
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            rows = (await session.execute(text(
                "SELECT * FROM dante.list_self_home_objective_work(:actor,:limit)"
            ), {"actor": context.self_person_ref, "limit": limit})).mappings().all()
            return [ObjectiveWorkItem.model_validate(dict(row)) for row in rows]
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503, code="temporal.home.objectives_unavailable", category="service",
            title="Objective work unavailable", detail="Obiettivi da valutare non disponibili.",
            retryable=True,
        ) from exc
