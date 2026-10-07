"""Self-scoped post-create Activity metadata and removal."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.platform.database.references import NativeRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/activities", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class ActivityProfileResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    activity_ref: UUID
    title: str
    description: str | None
    location: str | None
    color_code: str | None
    revision: int


class ActivityProfileChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    expected_revision: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    location: str | None = None
    color_code: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")


class ActivityRetirementCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)


class ActivityRetirementResponse(BaseModel):
    activity_ref: UUID
    replayed: bool


def _problem(exc: DBAPIError) -> ProblemError:
    constraint = getattr(getattr(getattr(exc, "orig", None), "diag", None), "constraint_name", None)
    if constraint == "activity_profile_unavailable":
        return ProblemError(
            status=404, code="temporal.activity_profile.not_found", category="not_found",
            title="Activity unavailable", detail="Activity unavailable in self scope.",
        )
    if constraint == "activity_profile_active_session":
        return ProblemError(
            status=409, code="temporal.activity_profile.active_session", category="conflict",
            title="Session active", detail="End the active Session before deleting the Activity.",
        )
    if constraint in ("activity_profile_stale", "activity_profile_operation_reused"):
        return ProblemError(
            status=409, code="temporal.activity_profile.conflict", category="conflict",
            title="Activity changed", detail="Refresh and retry the Activity change.",
        )
    if constraint == "activity_profile_invalid":
        return ProblemError(
            status=422, code="temporal.activity_profile.invalid", category="validation",
            title="Invalid Activity", detail="Check the edited Activity fields.",
        )
    return _unavailable()


def _unavailable() -> ProblemError:
    return ProblemError(
        status=503, code="temporal.activity_profile.unavailable", category="service",
        title="Activity unavailable", detail="The Activity operation could not be completed.",
        retryable=True,
    )


@router.get(
    "/{activity_ref}/profile", response_model=ActivityProfileResponse,
    operation_id="temporal_get_self_activity_profile",
)
async def get_self_activity_profile(
    activity_ref: UUID, context: ReadContext, request: Request, response: Response,
) -> ActivityProfileResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            row = (await session.execute(
                text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": context.self_person_ref, "activity": NativeRef(activity_ref)},
            )).mappings().one_or_none()
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    if row is None:
        raise ProblemError(
            status=404, code="temporal.activity_profile.not_found", category="not_found",
            title="Activity unavailable", detail="Activity unavailable in self scope.",
        )
    return ActivityProfileResponse(**{key: row[key] for key in ActivityProfileResponse.model_fields})


@router.put(
    "/{activity_ref}/profile", response_model=ActivityProfileResponse,
    operation_id="temporal_revise_self_activity_profile",
)
async def revise_self_activity_profile(
    activity_ref: UUID, body: ActivityProfileChange, context: WriteContext,
    request: Request, response: Response,
) -> ActivityProfileResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            row = (await session.execute(
                text("SELECT * FROM dante.revise_self_activity_profile("
                     ":actor,:activity,:operation,:revision,:title,:description,:location,:color)"),
                {
                    "actor": context.self_person_ref, "activity": NativeRef(activity_ref),
                    "operation": body.operation_id, "revision": body.expected_revision,
                    "title": body.title.strip(),
                    "description": body.description.strip() or None if body.description else None,
                    "location": body.location.strip() or None if body.location else None,
                    "color": body.color_code.upper() if body.color_code else None,
                },
            )).mappings().one()
    except DBAPIError as exc:
        raise _problem(exc) from exc
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    return ActivityProfileResponse(**{key: row[key] for key in ActivityProfileResponse.model_fields})


@router.post(
    "/{activity_ref}/retire", response_model=ActivityRetirementResponse,
    operation_id="temporal_retire_self_activity",
)
async def retire_self_activity(
    activity_ref: UUID, body: ActivityRetirementCommand, context: WriteContext,
    request: Request, response: Response,
) -> ActivityRetirementResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            replayed = await session.scalar(
                text("SELECT dante.retire_self_activity(:actor,:activity,:operation)"),
                {"actor": context.self_person_ref, "activity": NativeRef(activity_ref),
                 "operation": body.operation_id},
            )
    except DBAPIError as exc:
        raise _problem(exc) from exc
    except SQLAlchemyError as exc:
        raise _unavailable() from exc
    return ActivityRetirementResponse(activity_ref=activity_ref, replayed=bool(replayed))
