"""B05-B actor-local primary Life Area assignment capabilities."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef

SubjectKind = Literal["activity", "event"]


class LifeAreaAssignmentInputError(ValueError):
    """The bounded assignment command is malformed."""


class LifeAreaAssignmentOperationIdReuseError(RuntimeError):
    """The idempotency key was reused for another actor-local move."""


class LifeAreaAssignmentNotFoundError(RuntimeError):
    """The item or target is unavailable to this actor."""


class LifeAreaAssignmentConflictError(RuntimeError):
    """The requested assignment revision is stale or unchanged."""


class LifeAreaAssignmentPersistenceError(RuntimeError):
    """The primary organization change could not complete safely."""


@dataclass(frozen=True, slots=True)
class LifeAreaAssignmentView:
    subject_kind: SubjectKind
    subject_native_ref: NativeRef
    life_area_ref: UUID
    assignment_revision: int
    assigned_at: datetime
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class UnassignedLifeAreaItemView:
    subject_kind: SubjectKind
    subject_native_ref: NativeRef
    title: str
    created_at: datetime


def _operation(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise LifeAreaAssignmentInputError("Operation id must contain 1 to 200 characters.")
    return normalized


def _fingerprint(
    *, kind: SubjectKind, subject_ref: NativeRef, life_area_ref: UUID, expected: int
) -> str:
    return hashlib.sha256(
        json.dumps(
            {
                "version": 1,
                "subject_kind": kind,
                "subject_native_ref": str(subject_ref),
                "life_area_ref": str(life_area_ref),
                "expected_assignment_revision": expected,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _assignment_from_row(row: RowMapping, *, replayed: bool = False) -> LifeAreaAssignmentView:
    return LifeAreaAssignmentView(
        subject_kind=cast(SubjectKind, row["subject_kind"]),
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        life_area_ref=UUID(str(row["life_area_ref"])),
        assignment_revision=int(row["assignment_revision"]),
        assigned_at=row["assigned_at"],
        replayed=replayed or bool(row.get("replayed", False)),
    )


def _map_error(exc: DBAPIError) -> Exception:
    diagnostic = getattr(exc.orig, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None)
    if constraint in {
        "pk_activity_life_area_assignment_operation",
        "pk_event_life_area_assignment_operation",
    }:
        return LifeAreaAssignmentOperationIdReuseError()
    if constraint in {
        "life_area_assignment_target_unavailable",
        "fk_activity_life_area_assignment_activity_ref_activity",
        "fk_event_life_area_assignment_event_ref_event",
    }:
        return LifeAreaAssignmentNotFoundError()
    if constraint in {
        "life_area_assignment_revision_conflict",
        "life_area_assignment_no_change",
    }:
        return LifeAreaAssignmentConflictError()
    return LifeAreaAssignmentPersistenceError()


class LifeAreaAssignmentApplication:
    """Each capability owns one transaction and uses only bounded DB functions."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def assign(
        self,
        *,
        self_person_ref: NativeRef,
        subject_kind: SubjectKind,
        subject_native_ref: NativeRef,
        life_area_ref: UUID,
        expected_assignment_revision: int,
        operation_id: str,
    ) -> LifeAreaAssignmentView:
        if expected_assignment_revision < 0:
            raise LifeAreaAssignmentInputError("Expected assignment revision cannot be negative.")
        if subject_kind not in ("activity", "event"):
            raise LifeAreaAssignmentInputError("Unsupported typed assignment subject.")
        normalized_operation = _operation(operation_id)
        fingerprint = _fingerprint(
            kind=subject_kind,
            subject_ref=subject_native_ref,
            life_area_ref=life_area_ref,
            expected=expected_assignment_revision,
        )
        if subject_kind == "activity":
            statement = text("""
                SELECT :kind AS subject_kind,:subject_ref AS subject_native_ref,
                       life_area_ref,assignment_revision,assigned_at,replayed
                  FROM dante.assign_self_activity_life_area(
                    :self_person_ref,:operation_id,:fingerprint,:subject_ref,
                    :life_area_ref,:expected_assignment_revision)
            """)
        else:
            statement = text("""
                SELECT :kind AS subject_kind,:subject_ref AS subject_native_ref,
                       life_area_ref,assignment_revision,assigned_at,replayed
                  FROM dante.assign_self_event_life_area(
                    :self_person_ref,:operation_id,:fingerprint,:subject_ref,
                    :life_area_ref,:expected_assignment_revision)
            """)
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            statement,
                            {
                                "kind": subject_kind,
                                "self_person_ref": self_person_ref,
                                "operation_id": normalized_operation,
                                "fingerprint": fingerprint,
                                "subject_ref": subject_native_ref,
                                "life_area_ref": life_area_ref,
                                "expected_assignment_revision": expected_assignment_revision,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                return _assignment_from_row(row)
        except DBAPIError as exc:
            raise _map_error(exc) from exc
        except SQLAlchemyError as exc:
            raise LifeAreaAssignmentPersistenceError() from exc

    async def list_assignments(
        self, *, self_person_ref: NativeRef
    ) -> tuple[LifeAreaAssignmentView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text("""
                            SELECT subject_kind,subject_native_ref,life_area_ref,
                                   assignment_revision,assigned_at
                              FROM dante.list_self_life_area_assignments(:self_person_ref)
                        """),
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                return tuple(_assignment_from_row(row) for row in rows)
        except SQLAlchemyError as exc:
            raise LifeAreaAssignmentPersistenceError() from exc

    async def list_unassigned(
        self, *, self_person_ref: NativeRef
    ) -> tuple[UnassignedLifeAreaItemView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text("""
                            SELECT subject_kind,subject_native_ref,title,created_at
                              FROM dante.list_self_unassigned_life_area_items(:self_person_ref)
                        """),
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                return tuple(
                    UnassignedLifeAreaItemView(
                        subject_kind=cast(SubjectKind, row["subject_kind"]),
                        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
                        title=str(row["title"]),
                        created_at=row["created_at"],
                    )
                    for row in rows
                )
        except SQLAlchemyError as exc:
            raise LifeAreaAssignmentPersistenceError() from exc
