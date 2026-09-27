"""B11-B bounded conditional temporal capability over canonical Actual truth.

The application never accepts a caller-provided condition result. PostgreSQL
reads accepted-current Actual realization truth and returns an immutable,
evidence-pinned evaluation. ``allow`` is a gating signal, not an executed effect.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_scoped_record_ref,
)

ConditionalSubjectKind = Literal["activity", "event", "occurrence"]
ConditionalResult = Literal["satisfied", "not_satisfied", "indeterminate"]
ConditionalDisposition = Literal["allow", "withhold"]


class ConditionalTemporalInputError(ValueError):
    """The B11-B command is outside the bounded conditional contract."""


class ConditionalTemporalNotFoundError(LookupError):
    """Condition or subject is outside the authenticated self scope."""


class ConditionalTemporalOperationReuseError(RuntimeError):
    """One operation id was reused for a different conditional intent."""


class ConditionalTemporalPersistenceError(RuntimeError):
    """Canonical conditional persistence/evaluation could not complete safely."""


@dataclass(frozen=True, slots=True)
class ActualRealizationConditionView:
    condition_ref: ScopedRecordRef
    subject_kind: ConditionalSubjectKind
    subject_native_ref: NativeRef
    family_code: Literal["actual_realization"]
    created_at: datetime
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class ConditionalEvaluationView:
    evaluation_ref: ScopedRecordRef
    condition_ref: ScopedRecordRef
    result_code: ConditionalResult
    disposition_code: ConditionalDisposition
    actual_ref: ScopedRecordRef | None
    actual_realization_material_state_ref: MaterialStateRef | None
    evaluated_at: datetime
    replayed: bool = False


def _operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ConditionalTemporalInputError(
            "Conditional operation id must contain 1 to 200 characters."
        )
    return normalized


def _fingerprint(payload: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _db_error(exc: DBAPIError) -> RuntimeError:
    original = getattr(exc, "orig", None)
    sqlstate = getattr(original, "sqlstate", None)
    diagnostic = getattr(original, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None) if diagnostic else None
    message = str(original or exc)
    if sqlstate == "23505" or constraint == "conditional_temporal_operation_reused":
        return ConditionalTemporalOperationReuseError(message)
    if sqlstate in {"23503", "P0002"}:
        return ConditionalTemporalNotFoundError(message)
    if sqlstate in {"22023", "23514"}:
        return ConditionalTemporalInputError(message)
    return ConditionalTemporalPersistenceError(message)


def _condition(row: RowMapping, *, replayed: bool = False) -> ActualRealizationConditionView:
    subject_kind = row["subject_family"]
    if subject_kind not in {"activity", "event", "occurrence"}:
        raise ConditionalTemporalPersistenceError("Stored conditional subject family is invalid.")
    if row["family_code"] != "actual_realization":
        raise ConditionalTemporalPersistenceError("Stored conditional family is invalid.")
    return ActualRealizationConditionView(
        condition_ref=ScopedRecordRef(UUID(str(row["condition_ref"]))),
        subject_kind=subject_kind,
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        family_code="actual_realization",
        created_at=row["created_at"],
        replayed=replayed,
    )


def _evaluation(row: RowMapping, *, replayed: bool = False) -> ConditionalEvaluationView:
    result = row["result_code"]
    disposition = row["disposition_code"]
    if result not in {"satisfied", "not_satisfied", "indeterminate"}:
        raise ConditionalTemporalPersistenceError("Stored conditional result is invalid.")
    if disposition not in {"allow", "withhold"}:
        raise ConditionalTemporalPersistenceError("Stored conditional disposition is invalid.")
    actual_ref = row["actual_ref"]
    actual_state_ref = row["actual_realization_material_state_ref"]
    return ConditionalEvaluationView(
        evaluation_ref=ScopedRecordRef(UUID(str(row["evaluation_ref"]))),
        condition_ref=ScopedRecordRef(UUID(str(row["condition_ref"]))),
        result_code=result,
        disposition_code=disposition,
        actual_ref=(ScopedRecordRef(UUID(str(actual_ref))) if actual_ref is not None else None),
        actual_realization_material_state_ref=(
            MaterialStateRef(UUID(str(actual_state_ref)))
            if actual_state_ref is not None
            else None
        ),
        evaluated_at=row["evaluated_at"],
        replayed=replayed,
    )


class ConditionalTemporalApplication:
    """Create and evaluate the bounded B11-B actual-realization condition."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create_actual_realization_condition(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_kind: ConditionalSubjectKind,
        subject_native_ref: NativeRef,
    ) -> ActualRealizationConditionView:
        if subject_kind not in {"activity", "event", "occurrence"}:
            raise ConditionalTemporalInputError(
                "Conditional subjects are Activity, Event and Occurrence only."
            )
        key = _operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": 1,
                "command": "create_actual_realization_condition",
                "subject_kind": subject_kind,
                "subject_native_ref": str(subject_native_ref),
                "family_code": "actual_realization",
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            """
                            SELECT *
                              FROM dante.create_self_actual_realization_condition(
                                :actor,:subject_kind,:operation_id,:fingerprint,
                                :condition_ref,:subject_ref
                              )
                            """
                        ),
                        {
                            "actor": self_person_ref,
                            "subject_kind": subject_kind,
                            "operation_id": key,
                            "fingerprint": fingerprint,
                            "condition_ref": new_scoped_record_ref(),
                            "subject_ref": subject_native_ref,
                        },
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ConditionalTemporalPersistenceError() from exc
        if row is None:
            raise ConditionalTemporalNotFoundError("Conditional subject unavailable.")
        return _condition(row, replayed=bool(row["replayed"]))

    async def get_actual_realization_condition(
        self,
        *,
        self_person_ref: NativeRef,
        condition_ref: ScopedRecordRef,
    ) -> ActualRealizationConditionView | None:
        try:
            async with self._session_factory() as session:
                row = (
                    await session.execute(
                        text(
                            """
                            SELECT *
                              FROM dante.get_self_actual_realization_condition(
                                :actor,:condition_ref
                              )
                            """
                        ),
                        {"actor": self_person_ref, "condition_ref": condition_ref},
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ConditionalTemporalPersistenceError() from exc
        return _condition(row) if row is not None else None

    async def evaluate_actual_realization_condition(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        condition_ref: ScopedRecordRef,
    ) -> ConditionalEvaluationView:
        key = _operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": 1,
                "command": "evaluate_actual_realization_condition",
                "condition_ref": str(condition_ref),
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            """
                            SELECT *
                              FROM dante.evaluate_self_actual_realization_condition(
                                :actor,:operation_id,:fingerprint,
                                :evaluation_ref,:condition_ref
                              )
                            """
                        ),
                        {
                            "actor": self_person_ref,
                            "operation_id": key,
                            "fingerprint": fingerprint,
                            "evaluation_ref": new_scoped_record_ref(),
                            "condition_ref": condition_ref,
                        },
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _db_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ConditionalTemporalPersistenceError() from exc
        if row is None:
            raise ConditionalTemporalNotFoundError("Conditional temporal intent unavailable.")
        return _evaluation(row, replayed=bool(row["replayed"]))
