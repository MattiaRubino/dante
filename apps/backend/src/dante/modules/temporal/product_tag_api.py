"""Authenticated self-scoped B05-C secondary Tags and typed item association."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.modules.temporal.product_tag import (
    ProductTagApplication,
    ProductTagConflictError,
    ProductTagInputError,
    ProductTagOperationReuseError,
    ProductTagPersistenceError,
    ProductTagUnavailableError,
    ProductTagView,
)
from dante.platform.database.runtime import DatabaseRuntime
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal", tags=["temporal"])
Context = Annotated[DanteContext, Depends(require_dante_context)]
MutatingContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


def _application(request: Request) -> ProductTagApplication:
    runtime = cast(DatabaseRuntime, request.app.state.database_runtime)
    return ProductTagApplication(runtime.session_factory)


Application = Annotated[ProductTagApplication, Depends(_application)]


class CreateProductTagRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)
    name: str = Field(min_length=1, max_length=100)


class TagOperationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=200)


class RenameProductTagRequest(TagOperationRequest):
    expected_revision: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=100)


class ArchiveProductTagRequest(TagOperationRequest):
    expected_revision: int = Field(ge=1)


class ProductTagResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tag_ref: UUID
    name: str
    revision: int
    archived: bool
    created_at: datetime
    updated_at: datetime
    replayed: bool = False


class ProductTagMutationResponse(BaseModel):
    tag_ref: UUID
    accepted_revision: int
    replayed: bool


class ProductTagEdgeResponse(BaseModel):
    subject_kind: Literal["activity", "event", "routine"]
    subject_native_ref: UUID
    tag_ref: UUID
    attached_at: datetime


class ProductTagEffectResponse(BaseModel):
    attached: bool
    accepted_at: datetime
    replayed: bool


def _problem(exc: Exception) -> ProblemError:
    if isinstance(exc, ProductTagInputError):
        return ProblemError(
            status=422,
            code="temporal.tag.invalid_input",
            category="validation",
            title="Invalid Tag input",
            detail=str(exc),
            retryable=False,
        )
    if isinstance(exc, ProductTagOperationReuseError):
        return ProblemError(
            status=409,
            code="temporal.tag.operation_id_reused",
            category="conflict",
            title="Tag operation conflict",
            detail="The operation key has different intent.",
            retryable=False,
        )
    if isinstance(exc, ProductTagUnavailableError):
        return ProblemError(
            status=404,
            code="temporal.tag.unavailable",
            category="not_found",
            title="Tag or item unavailable",
            detail="No Tag or item is available in this self scope.",
            retryable=False,
        )
    if isinstance(exc, ProductTagConflictError):
        return ProblemError(
            status=409,
            code="temporal.tag.state_conflict",
            category="conflict",
            title="Tag state changed",
            detail="Refresh and submit the current state.",
            retryable=False,
        )
    return ProblemError(
        status=503,
        code="temporal.tag.persistence_unavailable",
        category="service",
        title="Tags unavailable",
        detail="The operation could not complete safely.",
        retryable=True,
    )


_Errors = (
    ProductTagInputError,
    ProductTagOperationReuseError,
    ProductTagUnavailableError,
    ProductTagConflictError,
    ProductTagPersistenceError,
)


def _response(tag: ProductTagView, *, replayed: bool = False) -> ProductTagResponse:
    return ProductTagResponse(
        tag_ref=tag.tag_ref,
        name=tag.name,
        revision=tag.revision,
        archived=tag.archived,
        created_at=tag.created_at,
        updated_at=tag.updated_at,
        replayed=replayed,
    )


@router.post(
    "/tags",
    status_code=201,
    response_model=ProductTagResponse,
    operation_id="temporal_create_product_tag",
)
async def create_tag(
    payload: CreateProductTagRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        tag, replayed = await application.create(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            name=payload.name,
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    if replayed:
        response.status_code = 200
    return _response(tag, replayed=replayed)


@router.get(
    "/tags", response_model=list[ProductTagResponse], operation_id="temporal_list_product_tags"
)
async def list_tags(
    context: Context, application: Application, response: Response
) -> list[ProductTagResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        tags = await application.list(self_person_ref=context.self_person_ref)
    except _Errors as exc:
        raise _problem(exc) from exc
    return [_response(tag) for tag in tags]


@router.put(
    "/tags/{tag_ref}/name",
    response_model=ProductTagMutationResponse,
    operation_id="temporal_rename_product_tag",
)
async def rename_tag(
    tag_ref: UUID,
    payload: RenameProductTagRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.mutate(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            tag_ref=tag_ref,
            expected_revision=payload.expected_revision,
            kind="rename",
            name=payload.name,
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    return ProductTagMutationResponse(
        tag_ref=result.tag_ref, accepted_revision=result.accepted_revision, replayed=result.replayed
    )


@router.post(
    "/tags/{tag_ref}/archive",
    response_model=ProductTagMutationResponse,
    operation_id="temporal_archive_product_tag",
)
async def archive_tag(
    tag_ref: UUID,
    payload: ArchiveProductTagRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagMutationResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.mutate(
            self_person_ref=context.self_person_ref,
            operation_id=payload.operation_id,
            tag_ref=tag_ref,
            expected_revision=payload.expected_revision,
            kind="archive",
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    return ProductTagMutationResponse(
        tag_ref=result.tag_ref, accepted_revision=result.accepted_revision, replayed=result.replayed
    )


@router.get(
    "/tags/assignments",
    response_model=list[ProductTagEdgeResponse],
    operation_id="temporal_list_item_tags",
)
async def list_item_tags(
    context: Context, application: Application, response: Response
) -> list[ProductTagEdgeResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        edges = await application.list_edges(self_person_ref=context.self_person_ref)
    except _Errors as exc:
        raise _problem(exc) from exc
    return [
        ProductTagEdgeResponse(
            subject_kind=edge.subject_kind,
            subject_native_ref=edge.subject_native_ref,
            tag_ref=edge.tag_ref,
            attached_at=edge.attached_at,
        )
        for edge in edges
    ]


async def _set_tag(
    context: DanteContext,
    application: ProductTagApplication,
    response: Response,
    subject_kind: Literal["activity", "event"],
    subject_ref: UUID,
    tag_ref: UUID,
    operation_id: str,
    attached: bool,
) -> ProductTagEffectResponse:
    response.headers["Cache-Control"] = "no-store"
    try:
        result = await application.set_item_tag(
            self_person_ref=context.self_person_ref,
            operation_id=operation_id,
            subject_kind=subject_kind,
            subject_native_ref=subject_ref,
            tag_ref=tag_ref,
            attached=attached,
        )
    except _Errors as exc:
        raise _problem(exc) from exc
    return ProductTagEffectResponse(
        attached=result.attached, accepted_at=result.accepted_at, replayed=result.replayed
    )


@router.post(
    "/activities/{activity_ref}/tags/{tag_ref}/attach",
    response_model=ProductTagEffectResponse,
    operation_id="temporal_attach_activity_tag",
)
async def attach_activity_tag(
    activity_ref: UUID,
    tag_ref: UUID,
    payload: TagOperationRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagEffectResponse:
    return await _set_tag(
        context,
        application,
        response,
        "activity",
        activity_ref,
        tag_ref,
        payload.operation_id,
        True,
    )


@router.post(
    "/activities/{activity_ref}/tags/{tag_ref}/detach",
    response_model=ProductTagEffectResponse,
    operation_id="temporal_detach_activity_tag",
)
async def detach_activity_tag(
    activity_ref: UUID,
    tag_ref: UUID,
    payload: TagOperationRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagEffectResponse:
    return await _set_tag(
        context,
        application,
        response,
        "activity",
        activity_ref,
        tag_ref,
        payload.operation_id,
        False,
    )


@router.post(
    "/events/{event_ref}/tags/{tag_ref}/attach",
    response_model=ProductTagEffectResponse,
    operation_id="temporal_attach_event_tag",
)
async def attach_event_tag(
    event_ref: UUID,
    tag_ref: UUID,
    payload: TagOperationRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagEffectResponse:
    return await _set_tag(
        context, application, response, "event", event_ref, tag_ref, payload.operation_id, True
    )


@router.post(
    "/events/{event_ref}/tags/{tag_ref}/detach",
    response_model=ProductTagEffectResponse,
    operation_id="temporal_detach_event_tag",
)
async def detach_event_tag(
    event_ref: UUID,
    tag_ref: UUID,
    payload: TagOperationRequest,
    context: MutatingContext,
    application: Application,
    response: Response,
) -> ProductTagEffectResponse:
    return await _set_tag(
        context, application, response, "event", event_ref, tag_ref, payload.operation_id, False
    )
