"""Authenticated public Timeline read API for the temporal-operational vertical."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, ConfigDict

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context
from dante.modules.temporal.application import TemporalTimelineApplication
from dante.modules.temporal.contracts import TimelineWindowQuery, TimelineWindowValidationError
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
DanteContextDependency = Annotated[DanteContext, Depends(require_dante_context)]
_APPLICATION = TemporalTimelineApplication()


class TimelineWindowResponse(BaseModel):
    """B00 transport contract for a truthful empty authenticated Timeline window."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["empty"] = "empty"
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str


@router.get("/timeline/window", response_model=TimelineWindowResponse)
async def get_timeline_window(
    context: DanteContextDependency,
    response: Response,
    start_date: date,
    end_date_exclusive: date,
) -> TimelineWindowResponse:
    """Read one bounded half-open local-date Timeline window for the authenticated self."""
    response.headers["Cache-Control"] = "no-store"

    try:
        query = TimelineWindowQuery(
            start_date=start_date,
            end_date_exclusive=end_date_exclusive,
        )
    except TimelineWindowValidationError as exc:
        raise ProblemError(
            status=400,
            code="temporal.invalid_timeline_window",
            category="validation",
            title="Invalid Timeline window",
            detail=str(exc),
            retryable=False,
        ) from exc

    result = _APPLICATION.read_window(query=query, context=context)
    return TimelineWindowResponse(
        start_date=result.start_date,
        end_date_exclusive=result.end_date_exclusive,
        effective_zone_id=result.effective_zone_id,
    )
