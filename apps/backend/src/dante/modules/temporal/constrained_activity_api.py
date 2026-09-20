"""Authenticated atomic Activity + Temporal Constraint authoring API for B04-F."""

from __future__ import annotations

from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_mutating_dante_context
from dante.modules.temporal.api import ActivityResponse
from dante.modules.temporal.constrained_activity import (
    ConstrainedActivityApplication,
    ConstrainedActivityInputError,
    ConstrainedActivityOperationIdReuseError,
    ConstrainedActivityPersistenceError,
)
from dante.modules.temporal.temporal_constraint_api import (
    CreatedTemporalConstraintResponse,
    TemporalConstraintRuleRequest,
    _created_response,
    _rule_from_request,
)
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
MutatingDanteContextDependency = Annotated[
    DanteContext,
    Depends(require_mutating_dante_context),
]


class CreateConstrainedActivityRequest(BaseModel):
    """Atomic unplaced Activity plus 1..4 public B04 boundary/window rules."""

    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=300)
    rules: list[TemporalConstraintRuleRequest] = Field(min_length=1, max_length=4)


class ConstrainedActivityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity: ActivityResponse
    constraints: list[CreatedTemporalConstraintResponse]
    replayed: bool = False


def get_constrained_activity_application(request: Request) -> ConstrainedActivityApplication:
    database_runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return ConstrainedActivityApplication(database_runtime.session_factory)


ConstrainedActivityApplicationDependency = Annotated[
    ConstrainedActivityApplication,
    Depends(get_constrained_activity_application),
]


@router.post(
    "/activities/constrained",
    response_model=ConstrainedActivityResponse,
    status_code=201,
    operation_id="temporal_create_constrained_activity",
)
async def temporal_create_constrained_activity(
    payload: CreateConstrainedActivityRequest,
    context: MutatingDanteContextDependency,
    application: ConstrainedActivityApplicationDependency,
    response: Response,
) -> ConstrainedActivityResponse:
    """Create one unplaced Activity and its initial B04 constraints atomically."""

    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.create_activity_with_constraints(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            title=payload.title,
            rules=tuple(_rule_from_request(rule) for rule in payload.rules),
        )
    except ConstrainedActivityInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.activity.invalid_constrained_create",
            category="validation",
            title="Invalid constrained Activity",
            detail=str(exc),
            retryable=False,
        ) from exc
    except ConstrainedActivityOperationIdReuseError as exc:
        raise ProblemError(
            status=409,
            code="temporal.activity.constrained_operation_id_reused",
            category="conflict",
            title="Constrained Activity operation conflict",
            detail="The operation id was already used for a different Activity/constraint intent.",
            retryable=False,
        ) from exc
    except ConstrainedActivityPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.activity.constrained_persistence_unavailable",
            category="service",
            title="Constrained Activity unavailable",
            detail="The Activity and its Temporal Constraints could not be persisted atomically.",
            retryable=True,
        ) from exc

    if result.replayed:
        response.status_code = 200
    return ConstrainedActivityResponse(
        activity=ActivityResponse(
            activity_ref=result.activity.activity_ref,
            title=result.activity.title,
            created_at=result.activity.created_at,
            replayed=result.replayed,
        ),
        constraints=[_created_response(value) for value in result.constraints],
        replayed=result.replayed,
    )
