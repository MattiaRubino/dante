"""B10-A Actual realization application capability over canonical PostgreSQL truth."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_material_state_ref,
    new_scoped_record_ref,
)

ActualSubjectKind = Literal["activity", "event", "occurrence"]
ActualExtent = Literal["instant", "start_only", "interval"]


class ActualInputError(ValueError):
    """The realization command is outside the B10-A contract."""


class ActualNotFoundError(LookupError):
    """The Actual subject/owner is outside the authenticated self scope."""


class ActualOperationReuseError(RuntimeError):
    """One operation id was reused for a different realization intent."""


class ActualCurrentConflictError(RuntimeError):
    """The caller's expected current realization is stale."""


class ActualAmbiguousSubjectError(RuntimeError):
    """The bounded B10-A subject maps to multiple pre-existing Actual owners."""


class ActualPersistenceError(RuntimeError):
    """Canonical Actual persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class ActualSessionBasis:
    session_ref: NativeRef
    session_timing_material_state_ref: MaterialStateRef


@dataclass(frozen=True, slots=True)
class ActualRealizationView:
    actual_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    material_state_ref: MaterialStateRef
    realization_occurred: bool
    extent_code: ActualExtent | None
    started_at: datetime | None
    ended_at: datetime | None
    session_bases: tuple[ActualSessionBasis, ...] = ()
    replayed: bool = False
    current_from_at: datetime | None = None
    current_until_at: datetime | None = None


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ActualInputError("Actual operation id must contain 1 to 200 characters.")
    return normalized


def _fingerprint(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _constraint_name(exc: BaseException) -> str | None:
    diagnostic = getattr(getattr(exc, "orig", None), "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _view(row: RowMapping, *, replayed: bool = False) -> ActualRealizationView:
    raw_extent = row["extent_code"]
    extent: ActualExtent | None
    if raw_extent is None:
        extent = None
    elif raw_extent in {"instant", "start_only", "interval"}:
        extent = raw_extent
    else:
        raise ActualPersistenceError("Stored Actual timing extent is invalid.")
    return ActualRealizationView(
        actual_ref=ScopedRecordRef(UUID(str(row["actual_ref"]))),
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        realization_occurred=bool(row["realization_occurred"]),
        extent_code=extent,
        started_at=row["started_at"] if isinstance(row["started_at"], datetime) else None,
        ended_at=row["ended_at"] if isinstance(row["ended_at"], datetime) else None,
        replayed=replayed,
        current_from_at=(
            row["current_from_at"]
            if "current_from_at" in row and isinstance(row["current_from_at"], datetime)
            else None
        ),
        current_until_at=(
            row["current_until_at"]
            if "current_until_at" in row and isinstance(row["current_until_at"], datetime)
            else None
        ),
    )


class ActualApplication:
    """Self-scoped append-only Actual realization commands and authoritative reads."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def record(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_kind: ActualSubjectKind,
        subject_native_ref: NativeRef,
        realization_occurred: bool,
        expected_material_state_ref: MaterialStateRef | None,
        extent_code: ActualExtent | None = None,
        started_at: datetime | None = None,
        ended_at: datetime | None = None,
        session_bases: tuple[ActualSessionBasis, ...] = (),
    ) -> ActualRealizationView:
        if subject_kind not in {"activity", "event", "occurrence"}:
            raise ActualInputError("Actual subjects are Activity, Event and Occurrence only.")
        normalized = _normalize_operation_id(operation_id)
        bases = tuple(
            sorted(
                session_bases,
                key=lambda item: (str(item.session_ref), str(item.session_timing_material_state_ref)),
            )
        )
        if len({basis.session_ref for basis in bases}) != len(bases):
            raise ActualInputError("An Actual state may reference each Session only once.")
        self._validate_payload(
            realization_occurred=realization_occurred,
            extent_code=extent_code,
            started_at=started_at,
            ended_at=ended_at,
            session_bases=bases,
        )
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "record_actual_realization",
                "subject_kind": subject_kind,
                "subject_native_ref": str(subject_native_ref),
                "expected_material_state_ref": (
                    str(expected_material_state_ref)
                    if expected_material_state_ref is not None
                    else None
                ),
                "realization_occurred": realization_occurred,
                "extent_code": extent_code,
                "started_at": started_at.isoformat() if started_at is not None else None,
                "ended_at": ended_at.isoformat() if ended_at is not None else None,
                "session_bases": [
                    {
                        "session_ref": str(basis.session_ref),
                        "session_timing_material_state_ref": str(
                            basis.session_timing_material_state_ref
                        ),
                    }
                    for basis in bases
                ],
            }
        )
        rows = await self._rows(
            """
            SELECT actual_ref, subject_native_ref, material_state_ref,
                   realization_occurred, extent_code, started_at, ended_at, replayed
              FROM dante.record_self_actual_realization(
                :actor, :operation_id, :fingerprint, :actual_ref, :state_ref,
                :subject, :expected_state, :occurred, :extent, :started_at, :ended_at,
                CAST(:session_refs AS uuid[]), CAST(:session_state_refs AS uuid[])
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized,
                "fingerprint": fingerprint,
                "actual_ref": new_scoped_record_ref(),
                "state_ref": new_material_state_ref(),
                "subject": subject_native_ref,
                "expected_state": expected_material_state_ref,
                "occurred": realization_occurred,
                "extent": extent_code,
                "started_at": started_at,
                "ended_at": ended_at,
                "session_refs": [basis.session_ref for basis in bases],
                "session_state_refs": [basis.session_timing_material_state_ref for basis in bases],
            },
        )
        if not rows:
            raise ActualNotFoundError("Actual subject unavailable.")
        view = _view(rows[0], replayed=bool(rows[0]["replayed"]))
        return await self._with_bases(self_person_ref, view)

    async def get_for_subject(
        self, *, self_person_ref: NativeRef, subject_native_ref: NativeRef
    ) -> ActualRealizationView:
        rows = await self._rows(
            """
            SELECT actual_ref, subject_native_ref, material_state_ref,
                   realization_occurred, extent_code, started_at, ended_at
              FROM dante.get_self_subject_actual(:actor, :subject)
            """,
            {"actor": self_person_ref, "subject": subject_native_ref},
        )
        if not rows:
            raise ActualNotFoundError("No Actual is established for this subject.")
        return await self._with_bases(self_person_ref, _view(rows[0]))

    async def history(
        self, *, self_person_ref: NativeRef, actual_ref: ScopedRecordRef
    ) -> tuple[ActualRealizationView, ...]:
        rows = await self._rows(
            """
            SELECT actual_ref, subject_native_ref, material_state_ref,
                   realization_occurred, extent_code, started_at, ended_at,
                   current_from_at, current_until_at
              FROM dante.list_self_actual_history(:actor, :actual_ref)
            """,
            {"actor": self_person_ref, "actual_ref": actual_ref},
        )
        if not rows:
            raise ActualNotFoundError("Actual is not in the authenticated self scope.")
        result: list[ActualRealizationView] = []
        for row in rows:
            result.append(await self._with_bases(self_person_ref, _view(row)))
        return tuple(result)

    async def _with_bases(
        self, self_person_ref: NativeRef, view: ActualRealizationView
    ) -> ActualRealizationView:
        rows = await self._rows(
            """
            SELECT session_ref, session_timing_material_state_ref
              FROM dante.list_self_actual_session_bases(
                :actor, :actual_ref, :material_state_ref
              )
            """,
            {
                "actor": self_person_ref,
                "actual_ref": view.actual_ref,
                "material_state_ref": view.material_state_ref,
            },
        )
        return replace(
            view,
            session_bases=tuple(
                ActualSessionBasis(
                    session_ref=NativeRef(UUID(str(row["session_ref"]))),
                    session_timing_material_state_ref=MaterialStateRef(
                        UUID(str(row["session_timing_material_state_ref"]))
                    ),
                )
                for row in rows
            ),
        )

    @staticmethod
    def _validate_payload(
        *,
        realization_occurred: bool,
        extent_code: ActualExtent | None,
        started_at: datetime | None,
        ended_at: datetime | None,
        session_bases: tuple[ActualSessionBasis, ...],
    ) -> None:
        if not realization_occurred:
            if extent_code is not None or started_at is not None or ended_at is not None or session_bases:
                raise ActualInputError(
                    "Known non-realization cannot carry timing or Session bases."
                )
            return
        if extent_code is None:
            if started_at is not None or ended_at is not None:
                raise ActualInputError("Actual timing requires an extent.")
            return
        if started_at is None:
            raise ActualInputError("Actual timing requires started_at.")
        if extent_code in {"instant", "start_only"}:
            if ended_at is not None:
                raise ActualInputError(f"{extent_code} timing cannot carry ended_at.")
            return
        if extent_code == "interval":
            if ended_at is None or ended_at <= started_at:
                raise ActualInputError("Actual interval requires ended_at after started_at.")
            return
        raise ActualInputError("Unsupported Actual timing extent.")

    async def _rows(self, statement: str, parameters: dict[str, object]) -> list[RowMapping]:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                result = await database_session.execute(text(statement), parameters)
                return list(result.mappings().all())
        except IntegrityError as exc:
            self._raise_known(exc)
            raise ActualPersistenceError("Actual command was rejected.") from exc
        except DBAPIError as exc:
            self._raise_known(exc)
            raise ActualPersistenceError("Actual command was rejected.") from exc
        except SQLAlchemyError as exc:
            raise ActualPersistenceError("Actual command was rejected.") from exc

    def _raise_known(self, exc: BaseException) -> None:
        name = _constraint_name(exc)
        message = str(getattr(exc, "orig", exc))
        if name == "actual_operation_reused" or "operation id reused" in message:
            raise ActualOperationReuseError("Actual operation id was reused.") from exc
        if name == "actual_current_conflict" or "expected current state" in message:
            raise ActualCurrentConflictError("Actual current realization is stale.") from exc
        if name == "actual_subject_ambiguous" or "more than one realization owner" in message:
            raise ActualAmbiguousSubjectError("Actual subject is ambiguous.") from exc
        if name == "actual_subject_unavailable" or "subject unavailable" in message:
            raise ActualNotFoundError("Actual subject unavailable.") from exc
        if name in {
            "actual_non_realization_payload",
            "actual_realization_timing_shape",
            "actual_session_basis_pairing",
            "actual_session_basis_subject",
        }:
            raise ActualInputError("Actual realization payload was rejected.") from exc
