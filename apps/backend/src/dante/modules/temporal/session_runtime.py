"""B08-A Session start, read, and end over the existing Session timing substrate."""

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
    new_material_state_ref,
    new_native_ref,
)

SubjectKind = Literal["activity", "occurrence"]


class SessionInputError(ValueError):
    """The Session command is outside the B08-A contract."""


class SessionNotFoundError(LookupError):
    """The Session subject is outside the authenticated self scope."""


class SessionOperationReuseError(RuntimeError):
    """One Session operation id was reused for a different intent."""


class SessionEndConflictError(RuntimeError):
    """The expected current timing state is no longer open."""

class SessionPauseConflictError(RuntimeError):
    """The Session is already paused or its state is stale."""

class SessionResumeConflictError(RuntimeError):
    """The Session is not paused or its state is stale."""


class SessionPersistenceError(RuntimeError):
    """Canonical Session persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class SessionView:
    """Authoritative Session projection. Ended means this episode stopped."""

    session_ref: NativeRef
    subject_native_ref: NativeRef
    timing_material_state_ref: MaterialStateRef
    started_at: datetime
    ended_at: datetime | None
    replayed: bool = False
    paused: bool = False

    @property
    def open(self) -> bool:
        return self.ended_at is None


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise SessionInputError("Session operation id must contain 1 to 200 characters.")
    return normalized


def _fingerprint(payload: dict[str, str]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _constraint_name(exc: BaseException) -> str | None:
    diagnostic = getattr(getattr(exc, "orig", None), "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _view(row: RowMapping, *, replayed: bool) -> SessionView:
    ended = row["ended_at"]
    return SessionView(
        session_ref=NativeRef(UUID(str(row["session_ref"]))),
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        timing_material_state_ref=MaterialStateRef(UUID(str(row["timing_material_state_ref"]))),
        started_at=row["started_at"],
        ended_at=ended if isinstance(ended, datetime) else None,
        replayed=replayed,
    )


class SessionApplication:
    """Self-scoped immutable Session transitions."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def start(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_kind: SubjectKind,
        subject_native_ref: NativeRef,
    ) -> SessionView:
        if subject_kind not in {"activity", "occurrence"}:
            raise SessionInputError("Session subjects are Activity and Occurrence only.")
        normalized = _normalize_operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "start",
                "subject_kind": subject_kind,
                "subject_native_ref": str(subject_native_ref),
            }
        )
        return await self._call(
            """
            SELECT session_ref, subject_native_ref, timing_material_state_ref,
                   started_at, ended_at, replayed
              FROM dante.start_self_session(
                :actor, :operation_id, :fingerprint, :session_ref, :state_ref,
                :subject_kind, :subject
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized,
                "fingerprint": fingerprint,
                "session_ref": new_native_ref(),
                "state_ref": new_material_state_ref(),
                "subject_kind": subject_kind,
                "subject": subject_native_ref,
            },
        )

    async def end(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        session_ref: NativeRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> SessionView:
        normalized = _normalize_operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "end",
                "session_ref": str(session_ref),
                "expected_material_state_ref": str(expected_material_state_ref),
            }
        )
        # The resulting MaterialStateRef is deliberately not part of the intent
        # fingerprint: retries may allocate a fresh candidate, while the database
        # replays the exact state recorded by the accepted operation receipt.
        resulting_state_ref = new_material_state_ref()
        return await self._call(
            """
            SELECT session_ref, subject_native_ref, timing_material_state_ref,
                   started_at, ended_at, replayed
              FROM dante.end_self_session(
                :actor, :operation_id, :fingerprint, :session_ref,
                :expected_state, :resulting_state
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized,
                "fingerprint": fingerprint,
                "session_ref": session_ref,
                "expected_state": expected_material_state_ref,
                "resulting_state": resulting_state_ref,
            },
        )

    async def pause(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        session_ref: NativeRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> SessionView:
        return replace(await self._transition(
            "pause", self_person_ref, operation_id, session_ref, expected_material_state_ref
        ), paused=True)

    async def resume(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        session_ref: NativeRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> SessionView:
        return replace(await self._transition(
            "resume", self_person_ref, operation_id, session_ref, expected_material_state_ref
        ), paused=False)

    async def _transition(
        self,
        command: Literal["pause", "resume"],
        self_person_ref: NativeRef,
        operation_id: str,
        session_ref: NativeRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> SessionView:
        normalized = _normalize_operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": command,
                "session_ref": str(session_ref),
                "expected_material_state_ref": str(expected_material_state_ref),
            }
        )
        return await self._call(
            f"""SELECT session_ref, subject_native_ref, timing_material_state_ref,
                       started_at, ended_at, replayed
                  FROM dante.{command}_self_session(
                    :actor, :operation_id, :fingerprint, :session_ref,
                    :expected_state, :resulting_state
                  )""",
            {
                "actor": self_person_ref,
                "operation_id": normalized,
                "fingerprint": fingerprint,
                "session_ref": session_ref,
                "expected_state": expected_material_state_ref,
                "resulting_state": new_material_state_ref(),
            },
        )

    async def list_for_subject(
        self, *, self_person_ref: NativeRef, subject_native_ref: NativeRef
    ) -> tuple[SessionView, ...]:
        views = await self._call_many(
            """
            SELECT session_ref, subject_native_ref, timing_material_state_ref,
                   started_at, ended_at
              FROM dante.list_self_subject_sessions(:actor, :subject)
            """,
            {"actor": self_person_ref, "subject": subject_native_ref},
        )
        return tuple(
            replace(view, paused=await self._is_paused(self_person_ref, view.session_ref))
            for view in views
        )

    async def get(
        self, *, self_person_ref: NativeRef, session_ref: NativeRef
    ) -> SessionView:
        view = await self._call(
            """
            SELECT session_ref, subject_native_ref, timing_material_state_ref,
                   started_at, ended_at
              FROM dante.get_self_session(:actor, :session_ref)
            """,
            {"actor": self_person_ref, "session_ref": session_ref},
        )
        return replace(view, paused=await self._is_paused(self_person_ref, session_ref))

    async def _is_paused(self, self_person_ref: NativeRef, session_ref: NativeRef) -> bool:
        rows = await self._rows(
            "SELECT dante.session_is_paused(:actor, :session_ref) AS paused",
            {"actor": self_person_ref, "session_ref": session_ref},
        )
        return bool(rows[0]["paused"]) if rows else False

    async def _call(self, statement: str, parameters: dict[str, object]) -> SessionView:
        rows = await self._rows(statement, parameters)
        if not rows:
            raise SessionNotFoundError("Session is not in the authenticated self scope.")
        replayed = bool(rows[0]["replayed"]) if "replayed" in rows[0] else False
        return _view(rows[0], replayed=replayed)

    async def _call_many(
        self, statement: str, parameters: dict[str, object]
    ) -> tuple[SessionView, ...]:
        return tuple(_view(row, replayed=False) for row in await self._rows(statement, parameters))

    async def _rows(self, statement: str, parameters: dict[str, object]) -> list[RowMapping]:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                result = await database_session.execute(text(statement), parameters)
                return list(result.mappings().all())
        except IntegrityError as exc:
            self._raise_known(exc)
            raise SessionPersistenceError("Session command was rejected.") from exc
        except DBAPIError as exc:
            self._raise_known(exc)
            raise SessionPersistenceError("Session command was rejected.") from exc
        except SQLAlchemyError as exc:
            raise SessionPersistenceError("Session command was rejected.") from exc

    def _raise_known(self, exc: BaseException) -> None:
        name = _constraint_name(exc)
        message = str(getattr(exc, "orig", exc))
        if name == "session_operation_reused" or "reused" in message:
            raise SessionOperationReuseError("Session operation id was reused.") from exc
        if name == "session_end_conflict" or "conflicts with current timing" in message:
            raise SessionEndConflictError("Session end conflicts with current timing.") from exc
        if name == "session_pause_conflict":
            raise SessionPauseConflictError("Session pause conflicts with current timing.") from exc
        if name == "session_resume_conflict":
            raise SessionResumeConflictError("Session resume conflicts with current timing.") from exc
        if name == "session_subject_unavailable" or "unavailable" in message:
            raise SessionNotFoundError("Session subject unavailable.") from exc
