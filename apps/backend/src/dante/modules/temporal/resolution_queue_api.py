"""Read-only product inbox derived from accepted B10 owner state.

The inbox has no independent truth or generic resolution mutation. Each item
routes to the exact B10 reconciliation owner and its guarded command.
"""

from __future__ import annotations

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


class ResolutionQueueItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason_code: Literal["reconciliation_open"] = "reconciliation_open"
    subject_kind: Literal["activity", "event"]
    subject_ref: UUID
    title: str
    reconciliation_ref: UUID
    outcome_ref: UUID
    purpose_code: str


class ResolutionQueueResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ResolutionQueueItem]
    count: int


@router.get(
    "/resolution-queue",
    response_model=ResolutionQueueResponse,
    operation_id="temporal_list_resolution_queue",
)
async def list_resolution_queue(
    request: Request, context: Context
) -> ResolutionQueueResponse:
    """Only current unresolved reconciliations on current self-owned truth.

    A missing Actual, Outcome, or Session is never interpreted as failure.
    Outdated reconciliation targets are excluded until the owning B10 vertical
    explicitly creates/updates a decision for the accepted Outcome state.
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
    except SQLAlchemyError as exc:
        raise ProblemError(
            status=503,
            code="temporal.resolution_queue.unavailable",
            category="service",
            title="Resolution queue unavailable",
            detail="The canonical resolution queue could not be read.",
            retryable=True,
        ) from exc

    items = [ResolutionQueueItem.model_validate(row) for row in rows]
    return ResolutionQueueResponse(items=items, count=len(items))
