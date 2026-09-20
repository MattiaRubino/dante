"""Self-scoped LR-12 Life Area profile lifecycle; never a Domain owner."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef


class LifeAreaInputError(ValueError):
    """The bounded profile input is invalid."""


class LifeAreaOperationIdReuseError(RuntimeError):
    """An operation key was reused with different intent."""


class LifeAreaNotFoundError(RuntimeError):
    """The area is unavailable in this self scope."""


class LifeAreaStateConflictError(RuntimeError):
    """The requested state was stale or did not change anything."""


class LifeAreaPersistenceError(RuntimeError):
    """Canonical state could not be safely established."""


@dataclass(frozen=True, slots=True)
class LifeAreaView:
    life_area_ref: UUID
    name: str
    created_at: datetime
    revision: int = 1
    sort_order: int = 0
    archived: bool = False
    hidden: bool = False
    icon_code: str | None = None
    color_code: str | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class CreatedLifeArea:
    area: LifeAreaView
    replayed: bool


@dataclass(frozen=True, slots=True)
class LifeAreaMutation:
    accepted_revision: int
    replayed: bool


@dataclass(frozen=True, slots=True)
class LifeAreaReorder:
    affected_count: int
    replayed: bool


def _area_from_row(record: RowMapping) -> LifeAreaView:
    return LifeAreaView(
        life_area_ref=UUID(str(record["life_area_ref"])),
        name=str(record["name"]),
        created_at=record["created_at"],
        revision=int(record["revision"]),
        sort_order=int(record["sort_order"]),
        archived=bool(record["archived"]),
        hidden=bool(record["hidden"]),
        icon_code=record["icon_code"],
        color_code=record["color_code"],
        updated_at=record["updated_at"],
    )


def _fingerprint(intent: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(intent, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def _operation(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise LifeAreaInputError("Operation id must contain 1 to 200 characters.")
    return normalized


def _name(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 100:
        raise LifeAreaInputError("Life Area name must contain 1 to 100 characters.")
    return normalized


def _map_db_error(exc: DBAPIError) -> Exception:
    diagnostic = getattr(exc.orig, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None)
    if constraint in {"pk_life_area_create_operation", "pk_life_area_mutation_operation"}:
        return LifeAreaOperationIdReuseError()
    if constraint == "fk_life_area_mutation_operation_life_area_ref_life_area":
        return LifeAreaNotFoundError()
    if constraint in {
        "life_area_expected_revision",
        "life_area_order_conflict",
        "life_area_no_change",
    }:
        return LifeAreaStateConflictError()
    return LifeAreaPersistenceError()


_LIST_SQL = text("""
    SELECT life_area_ref,name,created_at,revision,sort_order,archived,hidden,
           icon_code,color_code,updated_at
      FROM dante.list_self_life_areas(:self_person_ref)
""")


class LifeAreaApplication:
    """All writes use bounded database routines in one transaction each."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(
        self, *, self_person_ref: NativeRef, operation_id: str, name: str
    ) -> CreatedLifeArea:
        normalized_name = _name(name)
        normalized_operation = _operation(operation_id)
        fingerprint = _fingerprint({"version": 1, "name": normalized_name})
        try:
            async with self._session_factory() as session, session.begin():
                result = (
                    (
                        await session.execute(
                            text("""SELECT life_area_ref,replayed FROM dante.create_self_life_area(
                            :self_person_ref,:operation_id,:fingerprint,:area_ref,:name)"""),
                            {
                                "self_person_ref": self_person_ref,
                                "operation_id": normalized_operation,
                                "fingerprint": fingerprint,
                                "area_ref": uuid7(),
                                "name": normalized_name,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                rows = (
                    (await session.execute(_LIST_SQL, {"self_person_ref": self_person_ref}))
                    .mappings()
                    .all()
                )
                area = next(
                    (row for row in rows if row["life_area_ref"] == result["life_area_ref"]), None
                )
                if area is None:
                    raise LifeAreaPersistenceError("Creation receipt lost its profile.")
                return CreatedLifeArea(_area_from_row(area), bool(result["replayed"]))
        except DBAPIError as exc:
            raise _map_db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise LifeAreaPersistenceError() from exc

    async def list(self, *, self_person_ref: NativeRef) -> tuple[LifeAreaView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (await session.execute(_LIST_SQL, {"self_person_ref": self_person_ref}))
                    .mappings()
                    .all()
                )
                return tuple(_area_from_row(row) for row in rows)
        except SQLAlchemyError as exc:
            raise LifeAreaPersistenceError() from exc

    async def mutate(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        life_area_ref: UUID,
        expected_revision: int,
        kind: str,
        name: str | None = None,
        hidden: bool | None = None,
        icon_code: str | None = None,
        color_code: str | None = None,
    ) -> LifeAreaMutation:
        normalized_operation = _operation(operation_id)
        if expected_revision < 1:
            raise LifeAreaInputError("Expected revision must be positive.")
        if kind == "rename":
            if name is None:
                raise LifeAreaInputError("A name is required.")
            name = _name(name)
            payload: dict[str, object] = {"name": name}
        elif kind == "visibility":
            if hidden is None:
                raise LifeAreaInputError("Hidden must be specified.")
            payload = {"hidden": hidden}
        elif kind == "archive":
            payload = {}
        elif kind == "appearance":
            icon_code = icon_code.strip() if icon_code is not None else None
            color_code = color_code.strip().upper() if color_code is not None else None
            if (
                icon_code is not None
                and (
                    not icon_code
                    or len(icon_code) > 40
                    or not icon_code[0].islower()
                    or not icon_code.isascii()
                    or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in icon_code)
                )
            ) or (
                color_code is not None
                and (
                    len(color_code) != 7
                    or color_code[0] != "#"
                    or any(c not in "0123456789ABCDEF" for c in color_code[1:])
                )
            ):
                raise LifeAreaInputError("Invalid icon or color code.")
            payload = {"icon_code": icon_code, "color_code": color_code}
        else:
            raise LifeAreaInputError("Unsupported Life Area mutation.")
        fingerprint = _fingerprint(
            {
                "version": 1,
                "kind": kind,
                "area": str(life_area_ref),
                "expected_revision": expected_revision,
                "payload": payload,
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                result = (
                    (
                        await session.execute(
                            text("""
                    SELECT accepted_revision,replayed FROM dante.mutate_self_life_area(
                      :self_person_ref,:operation_id,:fingerprint,:life_area_ref,:expected_revision,
                      :kind,:name,:hidden,:icon_code,:color_code)
                """),
                            {
                                "self_person_ref": self_person_ref,
                                "operation_id": normalized_operation,
                                "fingerprint": fingerprint,
                                "life_area_ref": life_area_ref,
                                "expected_revision": expected_revision,
                                "kind": kind,
                                "name": name,
                                "hidden": hidden,
                                "icon_code": icon_code,
                                "color_code": color_code,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                return LifeAreaMutation(int(result["accepted_revision"]), bool(result["replayed"]))
        except DBAPIError as exc:
            raise _map_db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise LifeAreaPersistenceError() from exc

    async def reorder(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        entries: tuple[tuple[UUID, int], ...],
    ) -> LifeAreaReorder:
        normalized_operation = _operation(operation_id)
        if (
            len(entries) > 500
            or len({ref for ref, _ in entries}) != len(entries)
            or any(revision < 1 for _, revision in entries)
        ):
            raise LifeAreaInputError("Order must list each valid Life Area once (maximum 500).")
        fingerprint = _fingerprint(
            {"version": 1, "kind": "reorder", "entries": [[str(ref), rev] for ref, rev in entries]}
        )
        try:
            async with self._session_factory() as session, session.begin():
                result = (
                    (
                        await session.execute(
                            text("""
                    SELECT affected_count,replayed FROM dante.reorder_self_life_areas(
                      :self_person_ref,:operation_id,:fingerprint,CAST(:refs AS uuid[]),CAST(:revisions AS bigint[]))
                """),
                            {
                                "self_person_ref": self_person_ref,
                                "operation_id": normalized_operation,
                                "fingerprint": fingerprint,
                                "refs": [ref for ref, _ in entries],
                                "revisions": [revision for _, revision in entries],
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                return LifeAreaReorder(int(result["affected_count"]), bool(result["replayed"]))
        except DBAPIError as exc:
            raise _map_db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise LifeAreaPersistenceError() from exc
