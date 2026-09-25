"""B09-B HTTP surface for Responsibility and expected Participation authoring."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.responsibility_participation import (
    ExpectedParticipationView,
    ParticipationRequirement,
    ResponsibilityConflictError,
    ResponsibilityInputError,
    ResponsibilityNotFoundError,
    ResponsibilityOperationReuseError,
    ResponsibilityParticipationApplication,
    ResponsibilityPersistenceError,
    ResponsibilitySubjectKind,
    ResponsibilityView,
)
from dante.platform.database.references import NativeRef
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])


class SetResponsibilityRequest(BaseModel):
    """Set, replace or clear the single current Responsibility holder.

    The holder is a bounded intent rather than a raw reference: the server
    resolves it against the authenticated context. A later Person-referent
    slice widens the vocabulary without changing this contract's meaning.
    """

    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)
    holder: Literal["self"] | None = None
    expected_holder: Literal["self"] | None = None


class SetExpectedParticipationRequest(BaseModel):
    """Set, change or remove one Person's expected involvement in one Event."""

    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)
    participant: Literal["self"]
    requirement_code: Literal["required", "optional"] | None = None
    expected_requirement_code: Literal["required", "optional"] | None = None


class ResponsibilityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: Literal["activity", "event"]
    subject_native_ref: UUID
    responsible_person_ref: UUID | None
    responsible_is_self: bool
    established_at: datetime | None
    replayed: bool


class ExpectedParticipationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_ref: UUID
    participant_person_ref: UUID
    participant_is_self: bool
    requirement_code: Literal["required", "optional"] | None
    established_at: datetime | None
    replayed: bool


def _application(request: Request) -> ResponsibilityParticipationApplication:
    return ResponsibilityParticipationApplication(
        request.app.state.database_runtime.session_factory
    )


Application = Annotated[ResponsibilityParticipationApplication, Depends(_application)]
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]

_ERRORS = (
    ResponsibilityInputError,
    ResponsibilityNotFoundError,
    ResponsibilityOperationReuseError,
    ResponsibilityConflictError,
    ResponsibilityPersistenceError,
)


def _responsibility(
    view: ResponsibilityView, *, self_person_ref: NativeRef
) -> ResponsibilityResponse:
    return ResponsibilityResponse(
        subject_kind=view.subject_kind,
        subject_native_ref=view.subject_native_ref,
        responsible_person_ref=view.responsible_person_ref,
        responsible_is_self=view.responsible_person_ref == self_person_ref,
        established_at=view.established_at,
        replayed=view.replayed,
    )


def _participation(
    view: ExpectedParticipationView, *, self_person_ref: NativeRef
) -> ExpectedParticipationResponse:
    return ExpectedParticipationResponse(
        event_ref=view.event_ref,
        participant_person_ref=view.participant_person_ref,
        participant_is_self=view.participant_person_ref == self_person_ref,
        requirement_code=view.requirement_code,
        established_at=view.established_at,
        replayed=view.replayed,
    )


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ResponsibilityInputError):
        return ProblemError(
            status=422,
            code="temporal.responsibility.invalid_input",
            category="validation",
            title="Responsibility command rejected",
            detail=str(exc),
        )
    if isinstance(exc, ResponsibilityNotFoundError):
        return ProblemError(
            status=404,
            code="temporal.responsibility.not_found",
            category="not_found",
            title="Subject or Person unavailable",
            detail=str(exc),
        )
    if isinstance(exc, ResponsibilityOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.responsibility.operation_id_reused",
            category="conflict",
            title="Operation id reused",
            detail=str(exc),
        )
    if isinstance(exc, ResponsibilityConflictError):
        return ProblemError(
            status=409,
            code="temporal.responsibility.state_conflict",
            category="conflict",
            title="Responsibility state conflict",
            detail=str(exc),
        )
    return ProblemError(
        status=409,
        code="temporal.responsibility.persistence",
        category="conflict",
        title="Responsibility command rejected",
        detail="Responsibility command was rejected.",
    )


async def _set_responsibility(
    subject_kind: ResponsibilitySubjectKind,
    subject_ref: UUID,
    payload: SetResponsibilityRequest,
    context: DanteContext,
    application: ResponsibilityParticipationApplication,
) -> ResponsibilityResponse:
    try:
        view = await application.set_responsibility(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_ref),
            responsible_person_ref=(
                None if payload.holder is None else context.self_person_ref
            ),
            expected_responsible_person_ref=(
                None if payload.expected_holder is None else context.self_person_ref
            ),
        )
    except _ERRORS as exc:
        raise _problem(exc) from exc
    return _responsibility(view, self_person_ref=context.self_person_ref)


async def _get_responsibility(
    subject_kind: ResponsibilitySubjectKind,
    subject_ref: UUID,
    context: DanteContext,
    application: ResponsibilityParticipationApplication,
) -> ResponsibilityResponse:
    try:
        view = await application.get_responsibility(
            self_person_ref=context.self_person_ref,
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(subject_ref),
        )
    except _ERRORS as exc:
        raise _problem(exc) from exc
    return _responsibility(view, self_person_ref=context.self_person_ref)


@router.put(
    "/activities/{activity_ref}/responsibility",
    response_model=ResponsibilityResponse,
    status_code=200,
    operation_id="temporal_set_activity_responsibility",
)
async def set_activity_responsibility(
    activity_ref: UUID,
    payload: SetResponsibilityRequest,
    context: MutatingContext,
    application: Application,
) -> ResponsibilityResponse:
    return await _set_responsibility("activity", activity_ref, payload, context, application)


@router.get(
    "/activities/{activity_ref}/responsibility",
    response_model=ResponsibilityResponse,
    status_code=200,
    operation_id="temporal_get_activity_responsibility",
)
async def get_activity_responsibility(
    activity_ref: UUID,
    context: Context,
    application: Application,
) -> ResponsibilityResponse:
    return await _get_responsibility("activity", activity_ref, context, application)


@router.put(
    "/events/{event_ref}/responsibility",
    response_model=ResponsibilityResponse,
    status_code=200,
    operation_id="temporal_set_event_responsibility",
)
async def set_event_responsibility(
    event_ref: UUID,
    payload: SetResponsibilityRequest,
    context: MutatingContext,
    application: Application,
) -> ResponsibilityResponse:
    return await _set_responsibility("event", event_ref, payload, context, application)


@router.get(
    "/events/{event_ref}/responsibility",
    response_model=ResponsibilityResponse,
    status_code=200,
    operation_id="temporal_get_event_responsibility",
)
async def get_event_responsibility(
    event_ref: UUID,
    context: Context,
    application: Application,
) -> ResponsibilityResponse:
    return await _get_responsibility("event", event_ref, context, application)


@router.put(
    "/events/{event_ref}/expected-participation",
    response_model=ExpectedParticipationResponse,
    status_code=200,
    operation_id="temporal_set_event_expected_participation",
)
async def set_event_expected_participation(
    event_ref: UUID,
    payload: SetExpectedParticipationRequest,
    context: MutatingContext,
    application: Application,
) -> ExpectedParticipationResponse:
    requirement: ParticipationRequirement | None = payload.requirement_code
    expected: ParticipationRequirement | None = payload.expected_requirement_code
    try:
        view = await application.set_expected_participation(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            event_ref=NativeRef(event_ref),
            participant_person_ref=context.self_person_ref,
            requirement_code=requirement,
            expected_requirement_code=expected,
        )
    except _ERRORS as exc:
        raise _problem(exc) from exc
    return _participation(view, self_person_ref=context.self_person_ref)


@router.get(
    "/events/{event_ref}/expected-participation",
    response_model=list[ExpectedParticipationResponse],
    status_code=200,
    operation_id="temporal_list_event_expected_participation",
)
async def list_event_expected_participation(
    event_ref: UUID,
    context: Context,
    application: Application,
) -> list[ExpectedParticipationResponse]:
    try:
        views = await application.list_expected_participation(
            self_person_ref=context.self_person_ref,
            event_ref=NativeRef(event_ref),
        )
    except _ERRORS as exc:
        raise _problem(exc) from exc
    return [
        _participation(view, self_person_ref=context.self_person_ref) for view in views
    ]
