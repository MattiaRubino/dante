"""Authenticated self-scoped Movement Policy authoring for a Schedule."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_mutating_dante_context
from dante.modules.temporal.movement_policy import (
    MovementPolicyApplication,
    MovementPolicyInputError,
    MovementPolicyNotFoundError,
    MovementPolicyOperationIdReuseError,
    MovementPolicyPersistenceError,
    MovementPolicyRule,
    MovementPolicyStateConflictError,
)
from dante.platform.database.references import MaterialStateRef, ScopedRecordRef
from dante.platform.http.problem import ProblemDetails, ProblemError

router = APIRouter(prefix="/api/v1/temporal/schedules", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class SetMovementPolicyBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    expected_material_state_ref: UUID | None
    automatic_movement: Literal["blocked", "automatic"]
    acceptance_path: Literal["direct", "confirmation_required"]


class MovementPolicyMutationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_ref: UUID
    material_state_ref: UUID
    recorded_at: datetime
    replayed: bool


def _application(request: Request) -> MovementPolicyApplication:
    return MovementPolicyApplication(request.app.state.database_runtime.session_factory)


Application = Annotated[MovementPolicyApplication, Depends(_application)]


@router.put(
    "/{schedule_ref}/movement-policy",
    response_model=MovementPolicyMutationResponse,
    responses={
        401: {"model": ProblemDetails},
        403: {"model": ProblemDetails},
        404: {"model": ProblemDetails},
        409: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
        503: {"model": ProblemDetails},
    },
    operation_id="temporal_set_self_schedule_movement_policy",
)
async def set_self_schedule_movement_policy(
    schedule_ref: UUID,
    body: SetMovementPolicyBody,
    context: Context,
    application: Application,
    response: Response,
) -> MovementPolicyMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        rule = MovementPolicyRule(body.automatic_movement, body.acceptance_path)
        if body.expected_material_state_ref is None:
            value = await application.create_policy(
                self_person_ref=context.self_person_ref,
                operation_id=body.operation_id,
                schedule_ref=ScopedRecordRef(schedule_ref),
                rule=rule,
            )
        else:
            value = await application.revise_policy(
                self_person_ref=context.self_person_ref,
                operation_id=body.operation_id,
                schedule_ref=ScopedRecordRef(schedule_ref),
                expected_material_state_ref=MaterialStateRef(body.expected_material_state_ref),
                rule=rule,
            )
    except MovementPolicyInputError as exc:
        raise ProblemError(
            status=422,
            code="temporal.movement_policy.invalid",
            category="validation",
            title="Invalid Movement Policy",
            detail=str(exc),
        ) from exc
    except MovementPolicyNotFoundError as exc:
        raise ProblemError(
            status=404,
            code="temporal.movement_policy.unavailable",
            category="not_found",
            title="Schedule unavailable",
            detail="Schedule unavailable in this self scope.",
        ) from exc
    except (MovementPolicyStateConflictError, MovementPolicyOperationIdReuseError) as exc:
        raise ProblemError(
            status=409,
            code="temporal.movement_policy.conflict",
            category="conflict",
            title="Movement Policy changed",
            detail="Refresh and retry the current Schedule.",
        ) from exc
    except MovementPolicyPersistenceError as exc:
        raise ProblemError(
            status=503,
            code="temporal.movement_policy.unavailable",
            category="service",
            title="Movement Policy unavailable",
            detail="Movement Policy could not be saved.",
        ) from exc
    if value.material_state_ref is None:
        raise ProblemError(
            status=503,
            code="temporal.movement_policy.unavailable",
            category="service",
            title="Movement Policy unavailable",
            detail="Movement Policy returned no active state.",
        )
    return MovementPolicyMutationResponse(
        schedule_ref=value.schedule_ref,
        material_state_ref=value.material_state_ref,
        recorded_at=value.recorded_at,
        replayed=value.replayed,
    )
