"""B04-D Movement Policy application operations over canonical PostgreSQL state."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_material_state_ref,
)

MovementPolicyAutomaticMovement = Literal["blocked", "automatic"]
MovementPolicyAcceptancePath = Literal["direct", "confirmation_required"]
MovementPolicyMutationKind = Literal["create", "revise", "retire"]


class MovementPolicyInputError(ValueError):
    """Requested Movement Policy state is outside the activated B04-D contract."""


class MovementPolicyNotFoundError(LookupError):
    """Schedule or current Movement Policy is absent from the authenticated self scope."""


class MovementPolicyOperationIdReuseError(RuntimeError):
    """One operation id was reused for materially different Movement Policy intent."""


class MovementPolicyStateConflictError(RuntimeError):
    """Expected Movement Policy MaterialStateRef is no longer current."""


class MovementPolicyPersistenceError(RuntimeError):
    """Canonical Movement Policy persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class MovementPolicyRule:
    """Bounded self-governed movement authority and acceptance path."""

    automatic_movement: MovementPolicyAutomaticMovement
    acceptance_path: MovementPolicyAcceptancePath

    def __post_init__(self) -> None:
        if self.automatic_movement not in {"blocked", "automatic"}:
            raise MovementPolicyInputError("Automatic movement must be blocked or automatic.")
        if self.acceptance_path not in {"direct", "confirmation_required"}:
            raise MovementPolicyInputError(
                "Movement acceptance path must be direct or confirmation_required."
            )
        if self.automatic_movement == "blocked" and self.acceptance_path != "direct":
            raise MovementPolicyInputError(
                "A policy that blocks automatic movement cannot require confirmation for an automatic move."
            )


@dataclass(frozen=True, slots=True)
class MovementPolicyView:
    schedule_ref: ScopedRecordRef
    material_state_ref: MaterialStateRef
    rule: MovementPolicyRule


@dataclass(frozen=True, slots=True)
class MovementPolicyMutationView:
    schedule_ref: ScopedRecordRef
    material_state_ref: MaterialStateRef | None
    active: bool
    recorded_at: datetime
    replayed: bool


_MUTATE_SQL = text(
    """
    SELECT schedule_ref, material_state_ref, active, created_at, replayed
      FROM dante.mutate_self_schedule_movement_policy(
           :self_person_ref,:operation_id,:intent_fingerprint,:mutation_kind,
           :schedule_ref,:expected_material_state_ref,:resulting_material_state_ref,
           :automatic_movement_code,:acceptance_path_code
      )
    """
)

_RESOLVE_SQL = text(
    """
    SELECT schedule_ref, material_state_ref, automatic_movement_code, acceptance_path_code
      FROM dante.resolve_self_schedule_movement_policy(:self_person_ref,:schedule_ref)
    """
)


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise MovementPolicyInputError(
            "Movement Policy operation id must contain 1 to 200 characters."
        )
    return normalized


def _require_uuid7(value: UUID, *, label: str) -> None:
    if value.version != 7:
        raise MovementPolicyInputError(f"{label} must be a canonical UUIDv7 value.")


def _fingerprint(
    *,
    mutation_kind: MovementPolicyMutationKind,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef | None,
    rule: MovementPolicyRule | None,
) -> str:
    payload = {
        "mutation_kind": mutation_kind,
        "schedule_ref": str(schedule_ref),
        "expected_material_state_ref": (
            None if expected_material_state_ref is None else str(expected_material_state_ref)
        ),
        "automatic_movement": None if rule is None else rule.automatic_movement,
        "acceptance_path": None if rule is None else rule.acceptance_path,
    }
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()


def _constraint_name(exc: IntegrityError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _raise_integrity(exc: IntegrityError) -> None:
    constraint = _constraint_name(exc)
    if constraint == "pk_schedule_movement_policy_mutation_operation":
        raise MovementPolicyOperationIdReuseError() from exc
    if constraint == "movement_policy_state_conflict":
        raise MovementPolicyStateConflictError() from exc
    if constraint == "movement_policy_schedule_not_found":
        raise MovementPolicyNotFoundError() from exc
    raise MovementPolicyPersistenceError() from exc


async def _mutate_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    mutation_kind: MovementPolicyMutationKind,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef | None,
    rule: MovementPolicyRule | None,
) -> MovementPolicyMutationView:
    resulting_material_state_ref = (
        None if mutation_kind == "retire" else new_material_state_ref()
    )
    row = (
        (
            await database_session.execute(
                _MUTATE_SQL,
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": operation_id,
                    "intent_fingerprint": _fingerprint(
                        mutation_kind=mutation_kind,
                        schedule_ref=schedule_ref,
                        expected_material_state_ref=expected_material_state_ref,
                        rule=rule,
                    ),
                    "mutation_kind": mutation_kind,
                    "schedule_ref": schedule_ref,
                    "expected_material_state_ref": expected_material_state_ref,
                    "resulting_material_state_ref": resulting_material_state_ref,
                    "automatic_movement_code": (
                        None if rule is None else rule.automatic_movement
                    ),
                    "acceptance_path_code": None if rule is None else rule.acceptance_path,
                },
            )
        )
        .mappings()
        .one()
    )
    returned_state = row["material_state_ref"]
    return MovementPolicyMutationView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        material_state_ref=(
            None if returned_state is None else MaterialStateRef(UUID(str(returned_state)))
        ),
        active=bool(row["active"]),
        recorded_at=cast(datetime, row["created_at"]),
        replayed=bool(row["replayed"]),
    )


async def resolve_movement_policy_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    schedule_ref: ScopedRecordRef,
) -> MovementPolicyView | None:
    row = (
        (
            await database_session.execute(
                _RESOLVE_SQL,
                {"self_person_ref": self_person_ref, "schedule_ref": schedule_ref},
            )
        )
        .mappings()
        .one_or_none()
    )
    if row is None:
        return None
    return MovementPolicyView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        rule=MovementPolicyRule(
            automatic_movement=cast(
                MovementPolicyAutomaticMovement,
                str(row["automatic_movement_code"]),
            ),
            acceptance_path=cast(
                MovementPolicyAcceptancePath,
                str(row["acceptance_path_code"]),
            ),
        ),
    )


class MovementPolicyApplication:
    """Transaction-owning Movement Policy commands and current-state read."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create_policy(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        rule: MovementPolicyRule,
    ) -> MovementPolicyMutationView:
        return await self._mutate(
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            mutation_kind="create",
            schedule_ref=schedule_ref,
            expected_material_state_ref=None,
            rule=rule,
        )

    async def revise_policy(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
        rule: MovementPolicyRule,
    ) -> MovementPolicyMutationView:
        _require_uuid7(
            expected_material_state_ref,
            label="Expected Movement Policy state reference",
        )
        return await self._mutate(
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            mutation_kind="revise",
            schedule_ref=schedule_ref,
            expected_material_state_ref=expected_material_state_ref,
            rule=rule,
        )

    async def retire_policy(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> MovementPolicyMutationView:
        _require_uuid7(
            expected_material_state_ref,
            label="Expected Movement Policy state reference",
        )
        return await self._mutate(
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            mutation_kind="retire",
            schedule_ref=schedule_ref,
            expected_material_state_ref=expected_material_state_ref,
            rule=None,
        )

    async def get_policy(
        self,
        *,
        self_person_ref: NativeRef,
        schedule_ref: ScopedRecordRef,
    ) -> MovementPolicyView:
        _require_uuid7(schedule_ref, label="Schedule reference")
        try:
            async with self._session_factory() as database_session, database_session.begin():
                value = await resolve_movement_policy_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    schedule_ref=schedule_ref,
                )
        except SQLAlchemyError as exc:
            raise MovementPolicyPersistenceError() from exc
        if value is None:
            raise MovementPolicyNotFoundError()
        return value

    async def _mutate(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        mutation_kind: MovementPolicyMutationKind,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef | None,
        rule: MovementPolicyRule | None,
    ) -> MovementPolicyMutationView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        _require_uuid7(schedule_ref, label="Schedule reference")
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await _mutate_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    mutation_kind=mutation_kind,
                    schedule_ref=schedule_ref,
                    expected_material_state_ref=expected_material_state_ref,
                    rule=rule,
                )
        except IntegrityError as exc:
            _raise_integrity(exc)
        except DBAPIError as exc:
            raise MovementPolicyPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise MovementPolicyPersistenceError() from exc
        raise MovementPolicyPersistenceError("Movement Policy mutation returned no result.")
