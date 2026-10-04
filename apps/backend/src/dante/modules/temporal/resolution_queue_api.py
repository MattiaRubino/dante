"""Read-only product inbox derived from accepted owner/runtime state.

The inbox has no independent truth or generic resolution mutation. Each item
routes to its owning vertical: B10 Reconciliation or B10 Actual realization.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
ResolutionReason = Literal["reconciliation_open", "realization_review"]
ResolutionAction = Literal["open_reconciliation", "record_realization"]


class ResolutionQueueItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason_code: ResolutionReason
    subject_kind: Literal["activity", "event"]
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
            summary="A real Session ended and this Activity asks you to record what happened.",
            actions=["record_realization"],
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

    `realization_review` exists only when the Activity explicitly requests
    review-on-end and a bounded B08 Session really exists. Schedule expiry or
    absence of Actual never creates an item by itself.
    """
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            rows = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.list_self_resolution_queue(:self_person_ref)"),
                        {"self_person_ref": context.self_person_ref},
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
