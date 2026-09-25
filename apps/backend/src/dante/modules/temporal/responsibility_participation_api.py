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
    PersonReferentView,
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

    The holder is self or a Person admitted by the local referent catalog.
    """

    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)
    holder: str | None = None
    expected_holder: str | None = None


class SetExpectedParticipationRequest(BaseModel):
    """Set, change or remove one Person's expected involvement in one Event."""

    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)
    participant: str
    requirement_code: Literal["required", "optional"] | None = None
    expected_requirement_code: Literal["required", "optional"] | None = None


class CreatePersonReferentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)
    display_label: str = Field(min_length=1, max_length=100)


class RenamePersonReferentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    operation_id: str = Field(min_length=1, max_length=200)
    expected_revision: int = Field(ge=1)
    display_label: str = Field(min_length=1, max_length=100)


class PersonReferentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    person_ref: UUID
    display_label: str
    revision: int
    replayed: bool


def _person(view: PersonReferentView) -> PersonReferentResponse:
    return PersonReferentResponse(
        person_ref=view.person_ref,
        display_label=view.display_label,
        revision=view.revision,
        replayed=view.replayed,
    )


def _person_ref(value: str | None, self_ref: NativeRef) -> NativeRef | None:
    if value is None:
        return None
    if value == "self":
        return self_ref
    try:
        parsed = UUID(value)
    except (TypeError, ValueError) as exc:
        raise ResponsibilityInputError("Person reference must be self or UUIDv7.") from exc
    if parsed.version != 7 or str(parsed) != value.lower():
        raise ResponsibilityInputError("Person reference must be self or UUIDv7.")
    return NativeRef(parsed)


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
                _person_ref(payload.holder, context.self_person_ref)
            ),
            expected_responsible_person_ref=(
                _person_ref(payload.expected_holder, context.self_person_ref)
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
        participant_ref = _person_ref(payload.participant, context.self_person_ref)
        if participant_ref is None:
            raise ResponsibilityInputError("A participant Person is required.")
        view = await application.set_expected_participation(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            event_ref=NativeRef(event_ref),
            participant_person_ref=participant_ref,
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


@router.get(
    "/person-referents",
    response_model=list[PersonReferentResponse],
    operation_id="temporal_list_person_referents",
)
async def list_person_referents(
    context: Context, application: Application
) -> list[PersonReferentResponse]:
    try:
        return [
            _person(view) for view in await application.list_person_referents(
                self_person_ref=context.self_person_ref
            )
        ]
    except _ERRORS as exc:
        raise _problem(exc) from exc


@router.post(
    "/person-referents",
    response_model=PersonReferentResponse,
    status_code=201,
    operation_id="temporal_create_person_referent",
)
async def create_person_referent(
    payload: CreatePersonReferentRequest,
    context: MutatingContext,
    application: Application,
) -> PersonReferentResponse:
    try:
        return _person(await application.create_person_referent(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            display_label=payload.display_label,
        ))
    except _ERRORS as exc:
        raise _problem(exc) from exc


@router.patch(
    "/person-referents/{person_ref}",
    response_model=PersonReferentResponse,
    operation_id="temporal_rename_person_referent",
)
async def rename_person_referent(
    person_ref: UUID,
    payload: RenamePersonReferentRequest,
    context: MutatingContext,
    application: Application,
) -> PersonReferentResponse:
    try:
        return _person(await application.rename_person_referent(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            person_ref=NativeRef(person_ref),
            expected_revision=payload.expected_revision,
            display_label=payload.display_label,
        ))
    except _ERRORS as exc:
        raise _problem(exc) from exc
