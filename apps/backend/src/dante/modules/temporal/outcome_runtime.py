"""B10-B Outcome application capability over canonical PostgreSQL truth."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
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

_CONTEXT_CODE = re.compile(r"^[a-z][a-z0-9._-]{0,99}$")


class OutcomeInputError(ValueError):
    """The Outcome command is outside the B10-B contract."""


class OutcomeNotFoundError(LookupError):
    """The requested Actual/Outcome is outside the authenticated self scope."""


class OutcomeOperationReuseError(RuntimeError):
    """One operation id was reused for a different Outcome intent."""


class OutcomeCurrentConflictError(RuntimeError):
    """The caller's expected current Outcome state is stale."""


class OutcomePersistenceError(RuntimeError):
    """Canonical Outcome persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class OutcomeView:
    outcome_ref: ScopedRecordRef
    actual_ref: ScopedRecordRef
    vocabulary_code: str
    material_state_ref: MaterialStateRef
    result_code: str
    note: str | None
    replayed: bool = False
    current_from_at: datetime | None = None
    current_until_at: datetime | None = None


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise OutcomeInputError("Outcome operation id must contain 1 to 200 characters.")
    return normalized


def _normalize_context_code(value: str, *, label: str) -> str:
    normalized = value.strip()
    if normalized != value or not _CONTEXT_CODE.fullmatch(normalized):
        raise OutcomeInputError(
            f"Outcome {label} must be a trimmed contextual code of at most 100 characters."
        )
    return normalized


def _normalize_note(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if normalized != value or not normalized or len(normalized) > 2000:
        raise OutcomeInputError("Outcome note must contain 1 to 2000 trimmed characters.")
    return normalized


def _fingerprint(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _constraint_name(exc: BaseException) -> str | None:
    diagnostic = getattr(getattr(exc, "orig", None), "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _view(row: RowMapping, *, replayed: bool = False) -> OutcomeView:
    return OutcomeView(
        outcome_ref=ScopedRecordRef(UUID(str(row["outcome_ref"]))),
        actual_ref=ScopedRecordRef(UUID(str(row["actual_ref"]))),
        vocabulary_code=str(row["vocabulary_code"]),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        result_code=str(row["result_code"]),
        note=str(row["note"]) if row["note"] is not None else None,
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


class OutcomeApplication:
    """Self-scoped append-only contextual Outcome commands and authoritative reads."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def record(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        actual_ref: ScopedRecordRef,
        vocabulary_code: str,
        expected_material_state_ref: MaterialStateRef | None,
        result_code: str,
        note: str | None = None,
    ) -> OutcomeView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        normalized_vocabulary = _normalize_context_code(vocabulary_code, label="vocabulary_code")
        normalized_result = _normalize_context_code(result_code, label="result_code")
        normalized_note = _normalize_note(note)
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "record_actual_outcome",
                "actual_ref": str(actual_ref),
                "vocabulary_code": normalized_vocabulary,
                "expected_material_state_ref": (
                    str(expected_material_state_ref)
                    if expected_material_state_ref is not None
                    else None
                ),
                "result_code": normalized_result,
                "note": normalized_note,
            }
        )
        rows = await self._rows(
            """
            SELECT outcome_ref, actual_ref, vocabulary_code,
                   material_state_ref, result_code, note, replayed
              FROM dante.record_self_actual_outcome(
                :actor, :operation_id, :fingerprint, :actual_ref,
                :vocabulary_code, :outcome_ref, :state_ref,
                :expected_state, :result_code, :note
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized_operation_id,
                "fingerprint": fingerprint,
                "actual_ref": actual_ref,
                "vocabulary_code": normalized_vocabulary,
                "outcome_ref": new_scoped_record_ref(),
                "state_ref": new_material_state_ref(),
                "expected_state": expected_material_state_ref,
                "result_code": normalized_result,
                "note": normalized_note,
            },
        )
        if not rows:
            raise OutcomeNotFoundError("Outcome Actual unavailable.")
        return _view(rows[0], replayed=bool(rows[0]["replayed"]))

    async def get_for_actual(
        self,
        *,
        self_person_ref: NativeRef,
        actual_ref: ScopedRecordRef,
        vocabulary_code: str,
    ) -> OutcomeView:
        normalized_vocabulary = _normalize_context_code(vocabulary_code, label="vocabulary_code")
        rows = await self._rows(
            """
            SELECT outcome_ref, actual_ref, vocabulary_code,
                   material_state_ref, result_code, note
              FROM dante.get_self_actual_outcome(:actor, :actual_ref, :vocabulary_code)
            """,
            {
                "actor": self_person_ref,
                "actual_ref": actual_ref,
                "vocabulary_code": normalized_vocabulary,
            },
        )
        if not rows:
            raise OutcomeNotFoundError(
                "No Outcome is established for this Actual and vocabulary."
            )
        return _view(rows[0])

    async def history(
        self,
        *,
        self_person_ref: NativeRef,
        outcome_ref: ScopedRecordRef,
    ) -> tuple[OutcomeView, ...]:
        rows = await self._rows(
            """
            SELECT outcome_ref, actual_ref, vocabulary_code,
                   material_state_ref, result_code, note,
                   current_from_at, current_until_at
              FROM dante.list_self_outcome_history(:actor, :outcome_ref)
            """,
            {"actor": self_person_ref, "outcome_ref": outcome_ref},
        )
        if not rows:
            raise OutcomeNotFoundError("Outcome is not in the authenticated self scope.")
        return tuple(_view(row) for row in rows)

    async def _rows(self, statement: str, parameters: dict[str, object]) -> list[RowMapping]:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                result = await database_session.execute(text(statement), parameters)
                return list(result.mappings().all())
        except IntegrityError as exc:
            self._raise_known(exc)
            raise OutcomePersistenceError("Outcome command was rejected.") from exc
        except DBAPIError as exc:
            self._raise_known(exc)
            raise OutcomePersistenceError("Outcome command was rejected.") from exc
        except SQLAlchemyError as exc:
            raise OutcomePersistenceError("Outcome command was rejected.") from exc

    def _raise_known(self, exc: BaseException) -> None:
        name = _constraint_name(exc)
        message = str(getattr(exc, "orig", exc))
        if name == "outcome_operation_reused" or "operation id reused" in message:
            raise OutcomeOperationReuseError("Outcome operation id was reused.") from exc
        if name == "outcome_current_conflict" or "expected current state" in message:
            raise OutcomeCurrentConflictError("Outcome current state is stale.") from exc
        if name == "outcome_actual_unavailable" or "Outcome Actual unavailable" in message:
            raise OutcomeNotFoundError("Outcome Actual unavailable.") from exc
        if name in {
            "ck_outcome_result_operation_operation_id",
            "ck_outcome_result_operation_fingerprint",
            "ck_outcome_vocabulary_code",
            "ck_outcome_result_state_result_code",
            "ck_outcome_result_state_note",
        }:
            raise OutcomeInputError("Outcome payload was rejected.") from exc
