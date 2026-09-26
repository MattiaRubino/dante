"""B10-C Confirmation application capability over canonical PostgreSQL truth."""

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

_CONTEXT_CODE = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,119}$")


class ConfirmationInputError(ValueError):
    """The Confirmation command is outside the B10-C contract."""


class ConfirmationNotFoundError(LookupError):
    """The requested Outcome/Confirmation is outside the authenticated self scope."""


class ConfirmationOperationReuseError(RuntimeError):
    """One operation id was reused for a different Confirmation intent."""


class ConfirmationCurrentConflictError(RuntimeError):
    """The caller's expected current Confirmation state is stale."""


class ConfirmationPersistenceError(RuntimeError):
    """Canonical Confirmation persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class ConfirmationView:
    confirmation_ref: ScopedRecordRef
    outcome_ref: ScopedRecordRef
    outcome_disposition_material_state_ref: MaterialStateRef
    confirmer_person_ref: NativeRef
    purpose_code: str
    material_state_ref: MaterialStateRef
    stance_code: str
    confirmer_is_self: bool
    replayed: bool = False
    current_from_at: datetime | None = None
    current_until_at: datetime | None = None


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ConfirmationInputError("Confirmation operation id must contain 1 to 200 characters.")
    return normalized


def _normalize_context_code(value: str, field: str) -> str:
    normalized = value.strip()
    if normalized != value or not _CONTEXT_CODE.fullmatch(normalized):
        raise ConfirmationInputError(
            f"Confirmation {field} must be a trimmed contextual code of at most 120 characters."
        )
    return normalized


def _fingerprint(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _constraint_name(exc: BaseException) -> str | None:
    diagnostic = getattr(getattr(exc, "orig", None), "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _view(row: RowMapping, *, replayed: bool = False) -> ConfirmationView:
    return ConfirmationView(
        confirmation_ref=ScopedRecordRef(UUID(str(row["confirmation_ref"]))),
        outcome_ref=ScopedRecordRef(UUID(str(row["outcome_ref"]))),
        outcome_disposition_material_state_ref=MaterialStateRef(
            UUID(str(row["outcome_disposition_material_state_ref"]))
        ),
        confirmer_person_ref=NativeRef(UUID(str(row["confirmer_person_ref"]))),
        purpose_code=str(row["purpose_code"]),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        stance_code=str(row["stance_code"]),
        confirmer_is_self=bool(row["confirmer_is_self"]),
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


class ConfirmationApplication:
    """Self-as-confirmer append-only Confirmation commands and owner-scoped reads."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def record(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        outcome_ref: ScopedRecordRef,
        outcome_disposition_material_state_ref: MaterialStateRef,
        expected_material_state_ref: MaterialStateRef | None,
        purpose_code: str,
        stance_code: str,
    ) -> ConfirmationView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        normalized_purpose = _normalize_context_code(purpose_code, "purpose_code")
        normalized_stance = _normalize_context_code(stance_code, "stance_code")
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "record_outcome_confirmation",
                "outcome_ref": str(outcome_ref),
                "outcome_disposition_material_state_ref": str(
                    outcome_disposition_material_state_ref
                ),
                "expected_material_state_ref": (
                    str(expected_material_state_ref)
                    if expected_material_state_ref is not None
                    else None
                ),
                "purpose_code": normalized_purpose,
                "stance_code": normalized_stance,
            }
        )
        rows = await self._rows(
            """
            SELECT confirmation_ref, outcome_ref, outcome_disposition_material_state_ref,
                   confirmer_person_ref, purpose_code, material_state_ref, stance_code,
                   confirmer_is_self, replayed
              FROM dante.record_self_outcome_confirmation(
                :actor, :operation_id, :fingerprint, :outcome_ref,
                :outcome_state_ref, :confirmation_ref, :state_ref,
                :expected_state, :purpose_code, :stance_code
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized_operation_id,
                "fingerprint": fingerprint,
                "outcome_ref": outcome_ref,
                "outcome_state_ref": outcome_disposition_material_state_ref,
                "confirmation_ref": new_scoped_record_ref(),
                "state_ref": new_material_state_ref(),
                "expected_state": expected_material_state_ref,
                "purpose_code": normalized_purpose,
                "stance_code": normalized_stance,
            },
        )
        if not rows:
            raise ConfirmationNotFoundError("Confirmation Outcome target unavailable.")
        return _view(rows[0], replayed=bool(rows[0]["replayed"]))

    async def list_for_outcome(
        self,
        *,
        self_person_ref: NativeRef,
        outcome_ref: ScopedRecordRef,
    ) -> tuple[ConfirmationView, ...] | None:
        owned = await self._rows(
            "SELECT dante._confirmation_outcome_owned(:actor, :outcome_ref) AS owned",
            {"actor": self_person_ref, "outcome_ref": outcome_ref},
        )
        if not owned or not bool(owned[0]["owned"]):
            return None
        rows = await self._rows(
            """
            SELECT confirmation_ref, outcome_ref, outcome_disposition_material_state_ref,
                   confirmer_person_ref, purpose_code, material_state_ref, stance_code,
                   confirmer_is_self
              FROM dante.list_self_outcome_confirmations(:actor, :outcome_ref)
            """,
            {"actor": self_person_ref, "outcome_ref": outcome_ref},
        )
        return tuple(_view(row) for row in rows)

    async def history(
        self,
        *,
        self_person_ref: NativeRef,
        confirmation_ref: ScopedRecordRef,
    ) -> tuple[ConfirmationView, ...]:
        rows = await self._rows(
            """
            SELECT confirmation_ref, outcome_ref, outcome_disposition_material_state_ref,
                   confirmer_person_ref, purpose_code, material_state_ref, stance_code,
                   confirmer_is_self, current_from_at, current_until_at
              FROM dante.list_self_confirmation_history(:actor, :confirmation_ref)
            """,
            {"actor": self_person_ref, "confirmation_ref": confirmation_ref},
        )
        if not rows:
            raise ConfirmationNotFoundError("Confirmation is not in the authenticated self scope.")
        return tuple(_view(row) for row in rows)

    async def _rows(self, statement: str, parameters: dict[str, object]) -> list[RowMapping]:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                result = await database_session.execute(text(statement), parameters)
                return list(result.mappings().all())
        except IntegrityError as exc:
            self._raise_known(exc)
            raise ConfirmationPersistenceError("Confirmation command was rejected.") from exc
        except DBAPIError as exc:
            self._raise_known(exc)
            raise ConfirmationPersistenceError("Confirmation command was rejected.") from exc
        except SQLAlchemyError as exc:
            raise ConfirmationPersistenceError("Confirmation command was rejected.") from exc

    def _raise_known(self, exc: BaseException) -> None:
        name = _constraint_name(exc)
        message = str(getattr(exc, "orig", exc))
        if name == "confirmation_operation_reused" or "operation id reused" in message:
            raise ConfirmationOperationReuseError("Confirmation operation id was reused.") from exc
        if name == "confirmation_current_conflict" or "expected current state" in message:
            raise ConfirmationCurrentConflictError("Confirmation current state is stale.") from exc
        if name == "confirmation_outcome_unavailable" or "Outcome target unavailable" in message:
            raise ConfirmationNotFoundError("Confirmation Outcome target unavailable.") from exc
        if name in {
            "ck_confirmation_attestation_operation_operation_id",
            "ck_confirmation_attestation_operation_fingerprint",
            "ck_confirmation_attestation_state_stance",
            "ck_confirmation_purpose",
        }:
            raise ConfirmationInputError("Confirmation payload was rejected.") from exc
