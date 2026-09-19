"""B04-D governed automatic Schedule movement over current policy and constraints."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_material_state_ref,
)

ScheduleMoveResultKind = Literal["committed", "pending_confirmation"]


class ScheduleMoveInputError(ValueError):
    """The requested automatic move is outside the activated B04-D contract."""


class ScheduleMoveOperationIdReuseError(RuntimeError):
    """An operation id was reused for materially different movement intent."""


class ScheduleMoveNotFoundError(LookupError):
    """The Schedule or proposal is absent from the authenticated self scope."""


class ScheduleMoveBlockedError(RuntimeError):
    """The current Movement Policy blocks automatic movement."""


class ScheduleMoveHardConstraintViolationError(RuntimeError):
    """The candidate violates at least one current hard Temporal Constraint."""


class ScheduleMoveNotEvaluableError(RuntimeError):
    """The candidate cannot be evaluated without inventing temporal meaning."""


class ScheduleMoveStateConflictError(RuntimeError):
    """The accepted Schedule placement changed from the exact requested basis."""


class ScheduleMovePolicyConflictError(RuntimeError):
    """The Movement Policy changed from the exact proposal basis."""


class ScheduleMovePersistenceError(RuntimeError):
    """Canonical governed movement persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class CommittedScheduleMoveView:
    kind: Literal["committed"]
    schedule_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    movement_policy_material_state_ref: MaterialStateRef
    previous_placement_material_state_ref: MaterialStateRef
    placement_material_state_ref: MaterialStateRef
    placement: AbsoluteIntervalPlacement
    created_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class PendingScheduleMoveView:
    kind: Literal["pending_confirmation"]
    proposal_ref: UUID
    schedule_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    movement_policy_material_state_ref: MaterialStateRef
    expected_placement_material_state_ref: MaterialStateRef
    placement: AbsoluteIntervalPlacement
    created_at: datetime
    replayed: bool


ScheduleMoveRequestView = CommittedScheduleMoveView | PendingScheduleMoveView


@dataclass(frozen=True, slots=True)
class AcceptedScheduleMoveView:
    proposal_ref: UUID
    schedule_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    previous_placement_material_state_ref: MaterialStateRef
    placement_material_state_ref: MaterialStateRef
    created_at: datetime
    replayed: bool


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ScheduleMoveInputError("Schedule move operation id must contain 1 to 200 characters.")
    return normalized


def _require_uuid7(value: UUID, *, label: str) -> None:
    if value.version != 7:
        raise ScheduleMoveInputError(f"{label} must be a canonical UUIDv7 value.")


def _hash(payload: Mapping[str, str]) -> str:
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()


def _request_fingerprint(
    *,
    schedule_ref: ScopedRecordRef,
    expected_placement_material_state_ref: MaterialStateRef,
    placement: AbsoluteIntervalPlacement,
) -> str:
    return _hash(
        {
            "effect": "request-automatic-absolute-schedule-move",
            "schedule_ref": str(schedule_ref),
            "expected_placement_material_state_ref": str(expected_placement_material_state_ref),
            "starts_at": placement.starts_at.isoformat(timespec="microseconds"),
            "ends_at": placement.ends_at.isoformat(timespec="microseconds"),
        }
    )


def _accept_fingerprint(*, proposal_ref: UUID) -> str:
    return _hash(
        {
            "effect": "accept-automatic-absolute-schedule-move-proposal",
            "proposal_ref": str(proposal_ref),
        }
    )


def _constraint_name(exc: IntegrityError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _raise_integrity(exc: IntegrityError) -> None:
    constraint = _constraint_name(exc)
    if constraint in {"pk_schedule_move_request_operation", "pk_schedule_move_accept_operation"}:
        raise ScheduleMoveOperationIdReuseError() from exc
    if constraint in {"schedule_move_schedule_not_found", "schedule_move_proposal_not_found", "schedule_move_policy_not_found"}:
        raise ScheduleMoveNotFoundError() from exc
    if constraint == "schedule_move_automation_blocked":
        raise ScheduleMoveBlockedError() from exc
    if constraint == "schedule_move_hard_constraint_violation":
        raise ScheduleMoveHardConstraintViolationError() from exc
    if constraint == "schedule_move_not_evaluable":
        raise ScheduleMoveNotEvaluableError() from exc
    if constraint == "schedule_move_expected_state":
        raise ScheduleMoveStateConflictError() from exc
    if constraint == "schedule_move_policy_state":
        raise ScheduleMovePolicyConflictError() from exc
    if constraint == "uq_schedule_move_accept_operation_proposal_ref":
        raise ScheduleMoveStateConflictError() from exc
    raise ScheduleMovePersistenceError() from exc


_REQUEST_SQL = text(
    """
    SELECT schedule_ref,
           subject_native_ref,
           movement_policy_material_state_ref,
           result_kind,
           proposal_ref,
           placement_material_state_ref,
           created_at,
           replayed
      FROM dante.request_self_absolute_schedule_move(
           :self_person_ref,
           :operation_id,
           :intent_fingerprint,
           :schedule_ref,
           :expected_placement_material_state_ref,
           :starts_at,
           :ends_at,
           :proposal_ref,
           :resulting_placement_material_state_ref
      )
    """
)

_ACCEPT_SQL = text(
    """
    SELECT proposal_ref,
           schedule_ref,
           subject_native_ref,
           previous_placement_material_state_ref,
           placement_material_state_ref,
           created_at,
           replayed
      FROM dante.accept_self_absolute_schedule_move_proposal(
           :self_person_ref,
           :operation_id,
           :intent_fingerprint,
           :proposal_ref,
           :resulting_placement_material_state_ref
      )
    """
)


async def request_schedule_move_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    schedule_ref: ScopedRecordRef,
    expected_placement_material_state_ref: MaterialStateRef,
    placement: AbsoluteIntervalPlacement,
) -> ScheduleMoveRequestView:
    """Request one automatic move; policy decides direct effect versus proposal."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    _require_uuid7(schedule_ref, label="Schedule reference")
    _require_uuid7(expected_placement_material_state_ref, label="Expected placement state reference")
    proposal_ref = uuid7()
    resulting_ref = new_material_state_ref()
    row = (
        (
            await database_session.execute(
                _REQUEST_SQL,
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": _request_fingerprint(
                        schedule_ref=schedule_ref,
                        expected_placement_material_state_ref=expected_placement_material_state_ref,
                        placement=placement,
                    ),
                    "schedule_ref": schedule_ref,
                    "expected_placement_material_state_ref": expected_placement_material_state_ref,
                    "starts_at": placement.starts_at,
                    "ends_at": placement.ends_at,
                    "proposal_ref": proposal_ref,
                    "resulting_placement_material_state_ref": resulting_ref,
                },
            )
        )
        .mappings()
        .one()
    )
    returned_schedule_ref = ScopedRecordRef(UUID(str(row["schedule_ref"])))
    subject_native_ref = NativeRef(UUID(str(row["subject_native_ref"])))
    policy_ref = MaterialStateRef(UUID(str(row["movement_policy_material_state_ref"])))
    created_at = row["created_at"]
    replayed = bool(row["replayed"])
    if row["result_kind"] == "committed":
        state_ref = row["placement_material_state_ref"]
        if state_ref is None or row["proposal_ref"] is not None:
            raise ScheduleMovePersistenceError("Committed move returned an invalid result shape.")
        return CommittedScheduleMoveView(
            kind="committed",
            schedule_ref=returned_schedule_ref,
            subject_native_ref=subject_native_ref,
            movement_policy_material_state_ref=policy_ref,
            previous_placement_material_state_ref=expected_placement_material_state_ref,
            placement_material_state_ref=MaterialStateRef(UUID(str(state_ref))),
            placement=placement,
            created_at=created_at,
            replayed=replayed,
        )
    if row["result_kind"] == "pending_confirmation":
        returned_proposal_ref = row["proposal_ref"]
        if returned_proposal_ref is None or row["placement_material_state_ref"] is not None:
            raise ScheduleMovePersistenceError("Pending move returned an invalid proposal shape.")
        return PendingScheduleMoveView(
            kind="pending_confirmation",
            proposal_ref=UUID(str(returned_proposal_ref)),
            schedule_ref=returned_schedule_ref,
            subject_native_ref=subject_native_ref,
            movement_policy_material_state_ref=policy_ref,
            expected_placement_material_state_ref=expected_placement_material_state_ref,
            placement=placement,
            created_at=created_at,
            replayed=replayed,
        )
    raise ScheduleMovePersistenceError("Schedule move returned an unsupported result kind.")


async def accept_schedule_move_proposal_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    proposal_ref: UUID,
) -> AcceptedScheduleMoveView:
    """Accept one exact pending proposal into a new monotonic Schedule placement state."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    _require_uuid7(proposal_ref, label="Schedule move proposal reference")
    resulting_ref = new_material_state_ref()
    row = (
        (
            await database_session.execute(
                _ACCEPT_SQL,
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": _accept_fingerprint(proposal_ref=proposal_ref),
                    "proposal_ref": proposal_ref,
                    "resulting_placement_material_state_ref": resulting_ref,
                },
            )
        )
        .mappings()
        .one()
    )
    return AcceptedScheduleMoveView(
        proposal_ref=UUID(str(row["proposal_ref"])),
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        previous_placement_material_state_ref=MaterialStateRef(
            UUID(str(row["previous_placement_material_state_ref"]))
        ),
        placement_material_state_ref=MaterialStateRef(UUID(str(row["placement_material_state_ref"]))),
        created_at=row["created_at"],
        replayed=bool(row["replayed"]),
    )


class ScheduleMoveApplication:
    """Transaction-owning B04-D automatic movement commands."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def request_move(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_placement_material_state_ref: MaterialStateRef,
        placement: AbsoluteIntervalPlacement,
    ) -> ScheduleMoveRequestView:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await request_schedule_move_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    schedule_ref=schedule_ref,
                    expected_placement_material_state_ref=expected_placement_material_state_ref,
                    placement=placement,
                )
        except IntegrityError as exc:
            _raise_integrity(exc)
        except DBAPIError as exc:
            raise ScheduleMovePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise ScheduleMovePersistenceError() from exc
        raise AssertionError("unreachable")

    async def accept_proposal(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        proposal_ref: UUID,
    ) -> AcceptedScheduleMoveView:
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await accept_schedule_move_proposal_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    proposal_ref=proposal_ref,
                )
        except IntegrityError as exc:
            _raise_integrity(exc)
        except DBAPIError as exc:
            raise ScheduleMovePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise ScheduleMovePersistenceError() from exc
        raise AssertionError("unreachable")
