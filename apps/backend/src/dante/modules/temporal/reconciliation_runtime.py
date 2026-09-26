"""B10-D Outcome reconciliation capability over canonical PostgreSQL truth."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
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

_CONTEXT_CODE = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,119}$")
_ACTIONS = {"unresolved", "select", "accept_multiple", "defer", "escalate"}
_ROLES = {"considered", "selected"}

ReconciliationAction = Literal["unresolved", "select", "accept_multiple", "defer", "escalate"]
EvidenceRole = Literal["considered", "selected"]


class ReconciliationInputError(ValueError):
    """The reconciliation command is outside the frozen B10-D contract."""


class ReconciliationNotFoundError(LookupError):
    """The requested Outcome/reconciliation is outside authenticated owner scope."""


class ReconciliationOperationReuseError(RuntimeError):
    """One operation id was reused for a different reconciliation intent."""


class ReconciliationCurrentConflictError(RuntimeError):
    """The caller's expected current reconciliation state is stale."""


class ReconciliationPersistenceError(RuntimeError):
    """Canonical reconciliation persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class ReconciliationEvidence:
    confirmation_ref: ScopedRecordRef
    confirmation_attestation_material_state_ref: MaterialStateRef
    role_code: EvidenceRole


@dataclass(frozen=True, slots=True)
class ReconciliationView:
    reconciliation_ref: ScopedRecordRef
    outcome_ref: ScopedRecordRef
    outcome_disposition_material_state_ref: MaterialStateRef
    purpose_code: str
    material_state_ref: MaterialStateRef
    action_code: ReconciliationAction
    resolved_by_person_ref: NativeRef
    evidence: tuple[ReconciliationEvidence, ...]
    replayed: bool = False
    current_from_at: datetime | None = None
    current_until_at: datetime | None = None


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ReconciliationInputError(
            "Reconciliation operation id must contain 1 to 200 characters."
        )
    return normalized


def _normalize_context_code(value: str, field: str) -> str:
    normalized = value.strip()
    if normalized != value or not _CONTEXT_CODE.fullmatch(normalized):
        raise ReconciliationInputError(
            f"Reconciliation {field} must be a trimmed contextual code of at most 120 characters."
        )
    return normalized


def _normalize_action(value: str) -> ReconciliationAction:
    if value not in _ACTIONS:
        raise ReconciliationInputError("Reconciliation action_code is not supported.")
    return value  # type: ignore[return-value]


def _normalize_evidence(
    evidence: tuple[ReconciliationEvidence, ...],
    action: ReconciliationAction,
) -> tuple[ReconciliationEvidence, ...]:
    seen: set[tuple[UUID, UUID]] = set()
    normalized: list[ReconciliationEvidence] = []
    selected = 0
    for item in evidence:
        if item.role_code not in _ROLES:
            raise ReconciliationInputError("Reconciliation evidence role_code is not supported.")
        key = (UUID(str(item.confirmation_ref)), UUID(str(item.confirmation_attestation_material_state_ref)))
        if key in seen:
            raise ReconciliationInputError("Reconciliation evidence contains duplicate Confirmation states.")
        seen.add(key)
        selected += int(item.role_code == "selected")
        normalized.append(item)

    if action == "select" and selected != 1:
        raise ReconciliationInputError("Reconciliation select requires exactly one selected evidence state.")
    if action == "accept_multiple" and selected < 2:
        raise ReconciliationInputError(
            "Reconciliation accept_multiple requires at least two selected evidence states."
        )
    if action in {"unresolved", "defer", "escalate"} and selected:
        raise ReconciliationInputError(
            f"Reconciliation {action} cannot contain selected evidence states."
        )

    return tuple(
        sorted(
            normalized,
            key=lambda item: (
                str(item.confirmation_ref),
                str(item.confirmation_attestation_material_state_ref),
                item.role_code,
            ),
        )
    )


def _fingerprint(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _constraint_name(exc: BaseException) -> str | None:
    diagnostic = getattr(getattr(exc, "orig", None), "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _evidence_from_value(value: object) -> tuple[ReconciliationEvidence, ...]:
    parsed = json.loads(value) if isinstance(value, str) else value
    if parsed is None:
        return ()
    if not isinstance(parsed, list):
        raise ReconciliationPersistenceError("Reconciliation evidence payload is malformed.")
    result: list[ReconciliationEvidence] = []
    for raw in parsed:
        if not isinstance(raw, dict):
            raise ReconciliationPersistenceError("Reconciliation evidence payload is malformed.")
        role = str(raw["role_code"])
        if role not in _ROLES:
            raise ReconciliationPersistenceError("Reconciliation evidence role is malformed.")
        result.append(
            ReconciliationEvidence(
                confirmation_ref=ScopedRecordRef(UUID(str(raw["confirmation_ref"]))),
                confirmation_attestation_material_state_ref=MaterialStateRef(
                    UUID(str(raw["confirmation_attestation_material_state_ref"]))
                ),
                role_code=role,  # type: ignore[arg-type]
            )
        )
    return tuple(result)


def _view(row: RowMapping, *, replayed: bool = False) -> ReconciliationView:
    action = str(row["action_code"])
    if action not in _ACTIONS:
        raise ReconciliationPersistenceError("Reconciliation action is malformed.")
    return ReconciliationView(
        reconciliation_ref=ScopedRecordRef(UUID(str(row["reconciliation_ref"]))),
        outcome_ref=ScopedRecordRef(UUID(str(row["outcome_ref"]))),
        outcome_disposition_material_state_ref=MaterialStateRef(
            UUID(str(row["outcome_disposition_material_state_ref"]))
        ),
        purpose_code=str(row["purpose_code"]),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        action_code=action,  # type: ignore[arg-type]
        resolved_by_person_ref=NativeRef(UUID(str(row["resolved_by_person_ref"]))),
        evidence=_evidence_from_value(row["evidence"]),
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


class ReconciliationApplication:
    """Outcome-owner reconciliation commands and owner-scoped reads."""

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
        action_code: str,
        evidence: tuple[ReconciliationEvidence, ...],
    ) -> ReconciliationView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        normalized_purpose = _normalize_context_code(purpose_code, "purpose_code")
        normalized_action = _normalize_action(action_code)
        normalized_evidence = _normalize_evidence(evidence, normalized_action)

        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "record_outcome_reconciliation",
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
                "action_code": normalized_action,
                "evidence": [
                    {
                        "confirmation_ref": str(item.confirmation_ref),
                        "confirmation_attestation_material_state_ref": str(
                            item.confirmation_attestation_material_state_ref
                        ),
                        "role_code": item.role_code,
                    }
                    for item in normalized_evidence
                ],
            }
        )

        rows = await self._rows(
            """
            SELECT reconciliation_ref, outcome_ref,
                   outcome_disposition_material_state_ref, purpose_code,
                   material_state_ref, action_code, resolved_by_person_ref,
                   evidence, replayed
              FROM dante.record_self_outcome_reconciliation(
                :actor, :operation_id, :fingerprint, :outcome_ref,
                :outcome_state_ref, :reconciliation_ref, :state_ref,
                :expected_state, :purpose_code, :action_code,
                CAST(:confirmation_refs AS uuid[]),
                CAST(:confirmation_state_refs AS uuid[]),
                CAST(:role_codes AS text[])
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized_operation_id,
                "fingerprint": fingerprint,
                "outcome_ref": outcome_ref,
                "outcome_state_ref": outcome_disposition_material_state_ref,
                "reconciliation_ref": new_scoped_record_ref(),
                "state_ref": new_material_state_ref(),
                "expected_state": expected_material_state_ref,
                "purpose_code": normalized_purpose,
                "action_code": normalized_action,
                "confirmation_refs": [item.confirmation_ref for item in normalized_evidence],
                "confirmation_state_refs": [
                    item.confirmation_attestation_material_state_ref
                    for item in normalized_evidence
                ],
                "role_codes": [item.role_code for item in normalized_evidence],
            },
        )
        if not rows:
            raise ReconciliationNotFoundError("Reconciliation Outcome target unavailable.")
        return _view(rows[0], replayed=bool(rows[0]["replayed"]))

    async def list_for_outcome(
        self,
        *,
        self_person_ref: NativeRef,
        outcome_ref: ScopedRecordRef,
    ) -> tuple[ReconciliationView, ...] | None:
        owned = await self._rows(
            "SELECT dante._reconciliation_outcome_owned(:actor, :outcome_ref) AS owned",
            {"actor": self_person_ref, "outcome_ref": outcome_ref},
        )
        if not owned or not bool(owned[0]["owned"]):
            return None
        rows = await self._rows(
            """
            SELECT reconciliation_ref, outcome_ref,
                   outcome_disposition_material_state_ref, purpose_code,
                   material_state_ref, action_code, resolved_by_person_ref, evidence
              FROM dante.list_self_outcome_reconciliations(:actor, :outcome_ref)
            """,
            {"actor": self_person_ref, "outcome_ref": outcome_ref},
        )
        return tuple(_view(row) for row in rows)

    async def history(
        self,
        *,
        self_person_ref: NativeRef,
        reconciliation_ref: ScopedRecordRef,
    ) -> tuple[ReconciliationView, ...]:
        rows = await self._rows(
            """
            SELECT reconciliation_ref, outcome_ref,
                   outcome_disposition_material_state_ref, purpose_code,
                   material_state_ref, action_code, resolved_by_person_ref,
                   evidence, current_from_at, current_until_at
              FROM dante.list_self_outcome_reconciliation_history(
                :actor, :reconciliation_ref
              )
            """,
            {"actor": self_person_ref, "reconciliation_ref": reconciliation_ref},
        )
        if not rows:
            raise ReconciliationNotFoundError(
                "Reconciliation is not in the authenticated Outcome-owner scope."
            )
        return tuple(_view(row) for row in rows)

    async def _rows(self, statement: str, parameters: dict[str, object]) -> list[RowMapping]:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                result = await database_session.execute(text(statement), parameters)
                return list(result.mappings().all())
        except IntegrityError as exc:
            self._raise_known(exc)
            raise ReconciliationPersistenceError("Reconciliation command was rejected.") from exc
        except DBAPIError as exc:
            self._raise_known(exc)
            raise ReconciliationPersistenceError("Reconciliation command was rejected.") from exc
        except SQLAlchemyError as exc:
            raise ReconciliationPersistenceError("Reconciliation command was rejected.") from exc

    def _raise_known(self, exc: BaseException) -> None:
        name = _constraint_name(exc)
        message = str(getattr(exc, "orig", exc))
        if name == "reconciliation_operation_reused" or "operation id reused" in message:
            raise ReconciliationOperationReuseError(
                "Reconciliation operation id was reused."
            ) from exc
        if name == "reconciliation_current_conflict" or "expected current state" in message:
            raise ReconciliationCurrentConflictError(
                "Reconciliation current state is stale."
            ) from exc
        if name == "reconciliation_outcome_unavailable" or "Outcome unavailable" in message or "Outcome target unavailable" in message:
            raise ReconciliationNotFoundError("Reconciliation Outcome target unavailable.") from exc
        if name == "reconciliation_evidence_unavailable" or "evidence does not belong" in message:
            raise ReconciliationInputError(
                "Reconciliation evidence does not belong to the exact Outcome state."
            ) from exc
        if name in {
            "ck_outcome_reconciliation_operation_operation_id",
            "ck_outcome_reconciliation_operation_fingerprint",
            "ck_outcome_reconciliation_purpose",
            "ck_outcome_reconciliation_state_action",
            "ck_outcome_reconciliation_evidence_role",
            "reconciliation_evidence_shape_invalid",
            "reconciliation_evidence_duplicate",
            "reconciliation_action_evidence_invalid",
        }:
            raise ReconciliationInputError("Reconciliation payload was rejected.") from exc
