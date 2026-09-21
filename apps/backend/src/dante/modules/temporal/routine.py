"""B06-A self-owned Routine source lifecycle and product organization.

The module intentionally has no recurrence or occurrence command.  A Routine
is the source that may later govern immutable recurrence states; it is never a
materialized Activity and it never implies a Schedule by itself.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef

RoutineLifecycleState = Literal["active", "paused", "ended"]
RoutineMutationKind = Literal["rename", "pause", "resume", "end"]


class RoutineInputError(ValueError):
    """The Routine source command is malformed."""


class RoutineOperationReuseError(RuntimeError):
    """An actor-local operation id was reused with different intent."""


class RoutineNotFoundError(RuntimeError):
    """The source, Life Area, or Tag is unavailable in this self scope."""


class RoutineStateConflictError(RuntimeError):
    """A source or organization CAS was stale or would do nothing."""


class RoutinePersistenceError(RuntimeError):
    """The canonical Routine write/read could not safely complete."""


@dataclass(frozen=True, slots=True)
class RoutineView:
    routine_ref: UUID
    title: str
    lifecycle_state: RoutineLifecycleState
    source_revision: int
    created_at: datetime
    updated_at: datetime
    lifecycle_changed_at: datetime
    life_area_ref: UUID
    life_area_assignment_revision: int
    life_area_assigned_at: datetime
    tag_refs: tuple[UUID, ...] = ()
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class RoutineMutation:
    routine_ref: UUID
    source_revision: int
    lifecycle_state: RoutineLifecycleState
    accepted_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RoutineLifeAreaAssignment:
    life_area_ref: UUID
    assignment_revision: int
    assigned_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RoutineTagEffect:
    attached: bool
    accepted_at: datetime
    replayed: bool


def _bounded(value: str, limit: int, label: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > limit:
        raise RoutineInputError(f"{label} must contain 1 to {limit} characters.")
    return normalized


def _fingerprint(intent: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(intent, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _as_view(row: RowMapping, tags: tuple[UUID, ...] = (), *, replayed: bool = False) -> RoutineView:
    return RoutineView(
        routine_ref=UUID(str(row["routine_ref"])),
        title=str(row["title"]),
        lifecycle_state=row["lifecycle_state"],
        source_revision=int(row["source_revision"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        lifecycle_changed_at=row["lifecycle_changed_at"],
        life_area_ref=UUID(str(row["life_area_ref"])),
        life_area_assignment_revision=int(row["life_area_assignment_revision"]),
        life_area_assigned_at=row["life_area_assigned_at"],
        tag_refs=tags,
        replayed=replayed,
    )


def _error(exc: DBAPIError) -> Exception:
    constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
    if constraint in {
        "pk_routine_operation",
        "pk_routine_life_area_assignment_operation",
        "pk_routine_tag_operation",
    }:
        return RoutineOperationReuseError()
    if constraint in {
        "routine_unavailable",
        "routine_life_area_unavailable",
        "routine_tag_unavailable",
    }:
        return RoutineNotFoundError()
    if constraint in {"routine_source_conflict", "routine_life_area_conflict", "routine_tag_no_change"}:
        return RoutineStateConflictError()
    return RoutinePersistenceError()


_LIST = text("""
 SELECT routine_ref,title,lifecycle_state,source_revision,created_at,updated_at,
        lifecycle_changed_at,life_area_ref,life_area_assignment_revision,life_area_assigned_at
 FROM dante.list_self_routines(:self_person_ref)
""")
_TAGS = text("""
 SELECT routine_ref,tag_ref FROM dante.list_self_routine_tags(:self_person_ref)
""")


class RoutineApplication:
    """All Routine commands are bounded SQL capabilities, one transaction each."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _list_in_session(
        self, session: AsyncSession, self_person_ref: NativeRef
    ) -> tuple[RoutineView, ...]:
        rows = (await session.execute(_LIST, {"self_person_ref": self_person_ref})).mappings().all()
        tag_rows = (await session.execute(_TAGS, {"self_person_ref": self_person_ref})).mappings().all()
        tags: dict[UUID, list[UUID]] = {}
        for edge in tag_rows:
            tags.setdefault(UUID(str(edge["routine_ref"])), []).append(UUID(str(edge["tag_ref"])))
        return tuple(_as_view(row, tuple(tags.get(UUID(str(row["routine_ref"])), ()))) for row in rows)

    async def list(self, *, self_person_ref: NativeRef) -> tuple[RoutineView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                return await self._list_in_session(session, self_person_ref)
        except SQLAlchemyError as exc:
            raise RoutinePersistenceError() from exc

    async def create(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_ref: UUID,
        tag_refs: tuple[UUID, ...] = (),
    ) -> RoutineView:
        key = _bounded(operation_id, 200, "Operation id")
        label = _bounded(title, 300, "Routine title")
        if len(set(tag_refs)) != len(tag_refs):
            raise RoutineInputError("Routine Tags must not contain duplicates.")
        fingerprint = _fingerprint({"version": 1, "kind": "create", "title": label,
                                    "life_area_ref": str(life_area_ref),
                                    "tag_refs": sorted(str(tag) for tag in tag_refs)})
        try:
            async with self._session_factory() as session, session.begin():
                receipt = (
                    await session.execute(
                        text("""SELECT routine_ref,source_revision,life_area_assignment_revision,
                                      accepted_at,replayed
                                 FROM dante.create_self_routine(
                                   :actor,:operation,:fingerprint,:routine,:title,:area,:tags)"""),
                        {"actor": self_person_ref, "operation": key, "fingerprint": fingerprint,
                         "routine": uuid7(), "title": label, "area": life_area_ref,
                         "tags": list(tag_refs)},
                    )
                ).mappings().one()
                routines = await self._list_in_session(session, self_person_ref)
                view = next((item for item in routines if item.routine_ref == receipt["routine_ref"]), None)
                if view is None:
                    raise RoutinePersistenceError("Routine creation receipt lost its source.")
                return replace(view, replayed=bool(receipt["replayed"]))
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RoutinePersistenceError() from exc

    async def mutate(
        self, *, self_person_ref: NativeRef, operation_id: str, routine_ref: UUID,
        expected_source_revision: int, kind: RoutineMutationKind, title: str | None = None,
    ) -> RoutineMutation:
        key = _bounded(operation_id, 200, "Operation id")
        if expected_source_revision < 1:
            raise RoutineInputError("Expected source revision must be positive.")
        if kind == "rename":
            if title is None:
                raise RoutineInputError("A Routine title is required for rename.")
            title = _bounded(title, 300, "Routine title")
        elif kind not in {"pause", "resume", "end"} or title is not None:
            raise RoutineInputError("Unsupported Routine mutation.")
        fingerprint = _fingerprint({"version": 1, "kind": kind, "routine_ref": str(routine_ref),
                                    "expected_source_revision": expected_source_revision, "title": title})
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text("""SELECT routine_ref,source_revision,lifecycle_state,accepted_at,replayed
                                 FROM dante.mutate_self_routine(
                                   :actor,:operation,:fingerprint,:routine,:expected,:kind,:title)"""),
                        {"actor": self_person_ref, "operation": key, "fingerprint": fingerprint,
                         "routine": routine_ref, "expected": expected_source_revision,
                         "kind": kind, "title": title},
                    )
                ).mappings().one()
                return RoutineMutation(
                    routine_ref=UUID(str(row["routine_ref"])), source_revision=int(row["source_revision"]),
                    lifecycle_state=row["lifecycle_state"], accepted_at=row["accepted_at"],
                    replayed=bool(row["replayed"]),
                )
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RoutinePersistenceError() from exc

    async def assign_life_area(
        self, *, self_person_ref: NativeRef, operation_id: str, routine_ref: UUID,
        life_area_ref: UUID, expected_assignment_revision: int,
    ) -> RoutineLifeAreaAssignment:
        key = _bounded(operation_id, 200, "Operation id")
        if expected_assignment_revision < 1:
            raise RoutineInputError("Expected Life Area revision must be positive.")
        fingerprint = _fingerprint({"version": 1, "routine_ref": str(routine_ref),
                                    "life_area_ref": str(life_area_ref),
                                    "expected_assignment_revision": expected_assignment_revision})
        try:
            async with self._session_factory() as session, session.begin():
                row = (await session.execute(text("""SELECT life_area_ref,assignment_revision,assigned_at,replayed
                    FROM dante.assign_self_routine_life_area(:actor,:operation,:fingerprint,:routine,:area,:expected)"""),
                    {"actor": self_person_ref, "operation": key, "fingerprint": fingerprint,
                     "routine": routine_ref, "area": life_area_ref, "expected": expected_assignment_revision})).mappings().one()
                return RoutineLifeAreaAssignment(UUID(str(row["life_area_ref"])), int(row["assignment_revision"]), row["assigned_at"], bool(row["replayed"]))
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RoutinePersistenceError() from exc

    async def set_tag(
        self, *, self_person_ref: NativeRef, operation_id: str, routine_ref: UUID,
        tag_ref: UUID, attached: bool,
    ) -> RoutineTagEffect:
        key = _bounded(operation_id, 200, "Operation id")
        fingerprint = _fingerprint({"version": 1, "routine_ref": str(routine_ref),
                                    "tag_ref": str(tag_ref), "attached": attached})
        try:
            async with self._session_factory() as session, session.begin():
                row = (await session.execute(text("""SELECT attached,accepted_at,replayed
                    FROM dante.set_self_routine_tag(:actor,:operation,:fingerprint,:routine,:tag,:attached)"""),
                    {"actor": self_person_ref, "operation": key, "fingerprint": fingerprint,
                     "routine": routine_ref, "tag": tag_ref, "attached": attached})).mappings().one()
                return RoutineTagEffect(bool(row["attached"]), row["accepted_at"], bool(row["replayed"]))
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RoutinePersistenceError() from exc
