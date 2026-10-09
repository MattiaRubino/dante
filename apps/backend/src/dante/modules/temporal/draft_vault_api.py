"""Inert owner-scoped Draft Vault: configuration only, never a product subject."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from dante.context.contracts import DanteContext
from dante.context.dependencies import require_dante_context, require_mutating_dante_context
from dante.platform.http.problem import ProblemError

router = APIRouter(prefix="/api/v1/temporal/drafts", tags=["temporal"])
ReadContext = Annotated[DanteContext, Depends(require_dante_context)]
WriteContext = Annotated[DanteContext, Depends(require_mutating_dante_context)]


class DraftVaultSaveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    draft_ref: UUID
    operation_id: str = Field(min_length=1, max_length=200)
    expected_revision: int | None = Field(default=None, ge=1)
    subject_kind: Literal["activity", "event"]
    title: str = Field(max_length=300)
    payload: dict[str, Any]

    @model_validator(mode="after")
    def validate_payload(self) -> DraftVaultSaveRequest:
        if len(json.dumps(self.payload, ensure_ascii=False).encode("utf-8")) > 131072:
            raise ValueError("Draft payload exceeds 128 KiB.")
        if self.payload.get("version") != 1 or (
            not isinstance(self.payload.get("fields"), dict)
            or not isinstance(self.payload.get("advanced"), dict)
        ):
            raise ValueError("Draft must contain versioned fields and advanced configuration.")
        if self.payload["fields"].get("kind") != self.subject_kind:
            raise ValueError("Draft type must match its content.")
        return self


class DraftVaultResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    draft_ref: UUID
    subject_kind: Literal["activity", "event"]
    title: str
    payload: dict[str, Any]
    revision: int
    created_at: datetime
    updated_at: datetime


def _response(row: Any) -> DraftVaultResponse:
    return DraftVaultResponse.model_validate(dict(row))


def _problem(exc: DBAPIError | SQLAlchemyError) -> ProblemError:
    sqlstate = getattr(exc.orig, "sqlstate", None) if isinstance(exc, DBAPIError) else None
    if sqlstate in {"40001", "23505"}:
        return ProblemError(
            status=409, code="temporal.drafts.conflict", category="conflict",
            title="Draft changed", detail="La bozza è cambiata. Ricarica e riprova.",
        )
    if sqlstate == "42501":
        return ProblemError(
            status=404, code="temporal.drafts.not_found", category="not_found",
            title="Draft unavailable", detail="Bozza non disponibile.",
        )
    if sqlstate == "22023":
        return ProblemError(
            status=422, code="temporal.drafts.invalid", category="validation",
            title="Invalid draft", detail="La configurazione della bozza non è valida.",
        )
    return ProblemError(
        status=503, code="temporal.drafts.unavailable", category="service",
        title="Draft Vault unavailable", detail="Le bozze non sono disponibili.",
        retryable=True,
    )


@router.get("", response_model=list[DraftVaultResponse], operation_id="temporal_list_drafts")
async def list_drafts(
    context: ReadContext, request: Request, response: Response,
) -> list[DraftVaultResponse]:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session:
            rows = (await session.execute(text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """), {"actor": context.self_person_ref})).mappings().all()
        return [_response(row) for row in rows]
    except SQLAlchemyError as exc:
        raise _problem(exc) from exc


@router.put(
    "/{draft_ref}", response_model=DraftVaultResponse,
    operation_id="temporal_save_draft",
)
async def save_draft(
    draft_ref: UUID, payload: DraftVaultSaveRequest, context: WriteContext,
    request: Request, response: Response,
) -> DraftVaultResponse:
    response.headers["Cache-Control"] = "no-store"
    if draft_ref != payload.draft_ref:
        raise ProblemError(
            status=422, code="temporal.drafts.identity", category="validation",
            title="Invalid draft identity", detail="Identità bozza incoerente.",
        )
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            row = (await session.execute(text("""
                SELECT * FROM dante.save_self_temporal_draft(
                    :actor,:ref,:operation,:expected,:kind,:title,CAST(:payload AS jsonb))
            """), {
                "actor": context.self_person_ref,
                "ref": draft_ref, "operation": payload.operation_id,
                "expected": payload.expected_revision,
                "kind": payload.subject_kind, "title": payload.title,
                "payload": json.dumps(payload.payload, ensure_ascii=False),
            })).mappings().one()
        return _response(row)
    except SQLAlchemyError as exc:
        raise _problem(exc) from exc


@router.delete(
    "/{draft_ref}", status_code=204, operation_id="temporal_retire_draft",
)
async def delete_draft(
    draft_ref: UUID, expected_revision: int, context: WriteContext,
    request: Request, response: Response,
) -> None:
    response.headers["Cache-Control"] = "no-store"
    try:
        async with request.app.state.database_runtime.session_factory() as session, session.begin():
            await session.execute(text("""
                SELECT dante.retire_self_temporal_draft(:actor,:ref,:revision)
            """), {"actor": context.self_person_ref, "ref": draft_ref,
                  "revision": expected_revision})
    except SQLAlchemyError as exc:
        raise _problem(exc) from exc
