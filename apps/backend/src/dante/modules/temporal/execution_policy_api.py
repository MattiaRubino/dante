"""Self-scoped Activity Session capture policy, independent of duration rules."""

from __future__ import annotations

import hashlib
import json
from typing import Annotated, Literal
from uuid import UUID, uuid7

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/activities", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]
CaptureMode = Literal["disabled", "record", "live", "record_and_live"]


class ExecutionPolicyCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation_id: str = Field(min_length=1, max_length=200)
    mode_code: CaptureMode
    expected_state_ref: UUID | None = None


class ExecutionPolicyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_ref: UUID
    state_ref: UUID | None
    mode_code: CaptureMode
    replayed: bool = False


def _problem(exc: DBAPIError) -> ProblemError:
    diagnostic = getattr(exc.orig, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None)
    if constraint == "activity_execution_policy_owner_unavailable":
        return ProblemError(
            status=404, code="temporal.execution_policy.activity_unavailable",
            category="not_found", title="Activity unavailable",
            detail="Activity is unavailable in this self scope.", retryable=False,
        )
    if constraint in {
        "activity_execution_policy_operation_reused",
        "activity_execution_policy_current_conflict",
    }:
        return ProblemError(
            status=409, code="temporal.execution_policy.conflict",
            category="conflict", title="Execution policy conflict",
            detail="Refresh the Activity policy before changing it.", retryable=False,
        )
    if constraint == "activity_execution_policy_invalid":
        return ProblemError(
            status=422, code="temporal.execution_policy.invalid",
            category="validation", title="Invalid execution policy",
            detail="The requested execution policy is invalid.", retryable=False,
        )
    return _unavailable()


def _unavailable() -> ProblemError:
    return ProblemError(
        status=503, code="temporal.execution_policy.unavailable",
        category="service", title="Execution policy unavailable",
        detail="The canonical execution policy could not be read or changed.", retryable=True,
    )


@router.get(
    "/{activity_ref}/execution-policy",
    response_model=ExecutionPolicyResponse,
    operation_id="temporal_get_activity_execution_policy",
)
async def get_execution_policy(
    activity_ref: UUID, context: Context, request: Request,
) -> ExecutionPolicyResponse:
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                await session.execute(
                    text("SELECT * FROM dante.get_self_activity_execution_policy(:actor,:activity)"),
                    {"actor": context.self_person_ref, "activity": activity_ref},
                )
            ).mappings().one_or_none()
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    if row is None:
        raise ProblemError(
            status=404, code="temporal.execution_policy.activity_unavailable",
            category="not_found", title="Activity unavailable",
            detail="Activity is unavailable in this self scope.", retryable=False,
        )
    return ExecutionPolicyResponse(
        activity_ref=activity_ref, state_ref=row["state_ref"],
        mode_code=row["mode_code"],
    )


@router.post(
    "/{activity_ref}/execution-policy",
    response_model=ExecutionPolicyResponse,
    operation_id="temporal_set_activity_execution_policy",
)
async def set_execution_policy(
    activity_ref: UUID,
    payload: ExecutionPolicyCommand,
    context: MutatingContext,
    request: Request,
    response: Response,
) -> ExecutionPolicyResponse:
    intent = {
        "version": 1,
        "activity_ref": str(activity_ref),
        "mode_code": payload.mode_code,
        "expected_state_ref": (
            None if payload.expected_state_ref is None else str(payload.expected_state_ref)
        ),
    }
    fingerprint = hashlib.sha256(
        json.dumps(intent, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    try:
        async with (
            request.app.state.database_runtime.session_factory() as session,
            session.begin(),
        ):
            row = (
                await session.execute(
                    text("""
                        SELECT * FROM dante.set_self_activity_execution_policy(
                            :actor,:operation,:fingerprint,:activity,:state,:mode,:expected
                        )
                    """),
                    {
                        "actor": context.self_person_ref,
                        "operation": payload.operation_id,
                        "fingerprint": fingerprint,
                        "activity": activity_ref,
                        "state": uuid7(),
                        "mode": payload.mode_code,
                        "expected": payload.expected_state_ref,
                    },
                )
            ).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc) from exc
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    response.status_code = 200 if row["replayed"] else 201
    response.headers["Cache-Control"] = "no-store"
    return ExecutionPolicyResponse(
        activity_ref=activity_ref,
        state_ref=row["state_ref"],
        mode_code=row["mode_code"],
        replayed=bool(row["replayed"]),
    )
