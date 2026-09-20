"""B05-C guarded, actor-local secondary product Tags (not Domain labels)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef

SubjectKind = Literal["activity", "event"]


class ProductTagInputError(ValueError):
    """A bounded Tag request is invalid."""


class ProductTagOperationReuseError(RuntimeError):
    """The actor reused an operation key for different intent."""


class ProductTagUnavailableError(RuntimeError):
    """The self-scoped Tag or item is unavailable."""


class ProductTagConflictError(RuntimeError):
    """An expected state is stale or already matches the requested change."""


class ProductTagPersistenceError(RuntimeError):
    """The canonical write/read failed safely."""


@dataclass(frozen=True, slots=True)
class ProductTagView:
    tag_ref: UUID
    name: str
    revision: int
    archived: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class ProductTagMutation:
    tag_ref: UUID
    accepted_revision: int
    replayed: bool


@dataclass(frozen=True, slots=True)
class ProductTagEdge:
    subject_kind: SubjectKind
    subject_native_ref: UUID
    tag_ref: UUID
    attached_at: datetime


@dataclass(frozen=True, slots=True)
class ProductTagEffect:
    attached: bool
    accepted_at: datetime
    replayed: bool


def _bounded(value: str, limit: int, label: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > limit:
        raise ProductTagInputError(f"{label} must contain 1 to {limit} characters.")
    return normalized


def _fingerprint(intent: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(intent, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def _map_db_error(exc: DBAPIError) -> Exception:
    constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
    if constraint in {
        "pk_product_tag_operation",
        "pk_activity_tag_operation",
        "pk_event_tag_operation",
    }:
        return ProductTagOperationReuseError()
    if constraint in {
        "product_tag_unavailable",
        "activity_tag_item_unavailable",
        "event_tag_item_unavailable",
    }:
        return ProductTagUnavailableError()
    if constraint in {
        "product_tag_revision_conflict",
        "activity_tag_no_change",
        "event_tag_no_change",
    }:
        return ProductTagConflictError()
    return ProductTagPersistenceError()


_CATALOG = text("""
    SELECT tag_ref,name,revision,archived,created_at,updated_at
      FROM dante.list_self_product_tags(:self_person_ref)
""")


class ProductTagApplication:
    """Tag commands and reads are exclusively bounded database functions."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(
        self, *, self_person_ref: NativeRef, operation_id: str, name: str
    ) -> tuple[ProductTagView, bool]:
        label = _bounded(name, 100, "Tag name")
        key = _bounded(operation_id, 200, "Operation id")
        try:
            async with self._session_factory() as session, session.begin():
                result = (
                    (
                        await session.execute(
                            text("""SELECT tag_ref,replayed FROM dante.create_self_product_tag(
                            :actor,:key,:fingerprint,:tag,:name)"""),
                            {
                                "actor": self_person_ref,
                                "key": key,
                                "fingerprint": _fingerprint(
                                    {"version": 1, "kind": "create", "name": label}
                                ),
                                "tag": uuid7(),
                                "name": label,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                rows = (
                    (await session.execute(_CATALOG, {"self_person_ref": self_person_ref}))
                    .mappings()
                    .all()
                )
                tag = next((row for row in rows if row["tag_ref"] == result["tag_ref"]), None)
                if tag is None:
                    raise ProductTagPersistenceError("Tag creation receipt lost its profile.")
                return ProductTagView(**tag), bool(result["replayed"])
        except DBAPIError as exc:
            raise _map_db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ProductTagPersistenceError() from exc

    async def list(self, *, self_person_ref: NativeRef) -> tuple[ProductTagView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (await session.execute(_CATALOG, {"self_person_ref": self_person_ref}))
                    .mappings()
                    .all()
                )
                return tuple(ProductTagView(**row) for row in rows)
        except SQLAlchemyError as exc:
            raise ProductTagPersistenceError() from exc

    async def mutate(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        tag_ref: UUID,
        expected_revision: int,
        kind: Literal["rename", "archive"],
        name: str | None = None,
    ) -> ProductTagMutation:
        key = _bounded(operation_id, 200, "Operation id")
        if expected_revision < 1:
            raise ProductTagInputError("Expected revision must be positive.")
        if kind == "rename":
            if name is None:
                raise ProductTagInputError("A Tag name is required.")
            name = _bounded(name, 100, "Tag name")
        elif kind != "archive" or name is not None:
            raise ProductTagInputError("Unsupported Tag mutation.")
        fingerprint = _fingerprint(
            {
                "version": 1,
                "kind": kind,
                "tag_ref": str(tag_ref),
                "expected_revision": expected_revision,
                "name": name,
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text("""SELECT tag_ref,accepted_revision,replayed FROM dante.mutate_self_product_tag(
                        :actor,:key,:fingerprint,:tag,:revision,:kind,:name)"""),
                            {
                                "actor": self_person_ref,
                                "key": key,
                                "fingerprint": fingerprint,
                                "tag": tag_ref,
                                "revision": expected_revision,
                                "kind": kind,
                                "name": name,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                return ProductTagMutation(**row)
        except DBAPIError as exc:
            raise _map_db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ProductTagPersistenceError() from exc

    async def set_item_tag(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_kind: SubjectKind,
        subject_native_ref: UUID,
        tag_ref: UUID,
        attached: bool,
    ) -> ProductTagEffect:
        key = _bounded(operation_id, 200, "Operation id")
        if subject_kind not in ("activity", "event"):
            raise ProductTagInputError("Only Activity and Event support Tags in B05-C.")
        fingerprint = _fingerprint(
            {
                "version": 1,
                "kind": subject_kind,
                "item": str(subject_native_ref),
                "tag": str(tag_ref),
                "attached": attached,
            }
        )
        statement = (
            text("""SELECT attached,accepted_at,replayed FROM dante.set_self_activity_tag(
                :actor,:key,:fingerprint,:item,:tag,:attached)""")
            if subject_kind == "activity"
            else text("""SELECT attached,accepted_at,replayed FROM dante.set_self_event_tag(
                :actor,:key,:fingerprint,:item,:tag,:attached)""")
        )
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            statement,
                            {
                                "actor": self_person_ref,
                                "key": key,
                                "fingerprint": fingerprint,
                                "item": subject_native_ref,
                                "tag": tag_ref,
                                "attached": attached,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                return ProductTagEffect(**row)
        except DBAPIError as exc:
            raise _map_db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ProductTagPersistenceError() from exc

    async def list_edges(self, *, self_person_ref: NativeRef) -> tuple[ProductTagEdge, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text("""SELECT subject_kind,subject_native_ref,tag_ref,attached_at
                        FROM dante.list_self_item_tags(:actor)"""),
                            {"actor": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                return tuple(ProductTagEdge(**row) for row in rows)
        except SQLAlchemyError as exc:
            raise ProductTagPersistenceError() from exc
