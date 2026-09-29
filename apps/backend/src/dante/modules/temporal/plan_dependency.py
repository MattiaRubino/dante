"""B13-B qualified Plan Dependency over guarded canonical PostgreSQL truth."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, replace
from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef, new_native_ref, new_scoped_record_ref

_CODE = re.compile(r"^[a-z0-9][a-z0-9._:-]{0,119}$")
_QUALIFIERS = frozenset({"actual_occurred", "outcome_code"})


class PlanDependencyInputError(ValueError):
    """Intent is outside the B13-B relation contract."""


class PlanDependencyNotFoundError(LookupError):
    """The requested relation or one of its endpoints is unavailable."""


class PlanDependencyConflictError(RuntimeError):
    """Current state or operation id conflicts with accepted truth."""


class PlanDependencyPersistenceError(RuntimeError):
    """Guarded PostgreSQL operation failed unexpectedly."""


@dataclass(frozen=True, slots=True)
class PlanDependencyView:
    dependency_ref: UUID
    plan_ref: UUID
    prerequisite_step_ref: UUID
    prerequisite_activity_ref: UUID
    dependent_step_ref: UUID
    dependent_activity_ref: UUID
    purpose_code: str
    state_ref: UUID
    qualifier_code: str
    disposition_code: str | None
    active: bool
    recorded_at: datetime
    evaluation_code: str | None
    actual_material_state_ref: UUID | None
    outcome_material_state_ref: UUID | None
    cycle: bool = False
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class PlanDependencyHistoryView:
    state_ref: UUID
    qualifier_code: str
    disposition_code: str | None
    active: bool
    recorded_at: datetime
    current_from_at: datetime
    current_until_at: datetime | None


def _read(row: RowMapping) -> PlanDependencyView:
    return PlanDependencyView(
        dependency_ref=row["dependency_ref"],
        plan_ref=row["plan_ref"],
        prerequisite_step_ref=row["prerequisite_step_ref"],
        prerequisite_activity_ref=row["prerequisite_activity_ref"],
        dependent_step_ref=row["dependent_step_ref"],
        dependent_activity_ref=row["dependent_activity_ref"],
        purpose_code=row["purpose_code"],
        state_ref=row["state_ref"],
        qualifier_code=row["qualifier_code"],
        disposition_code=row["disposition_code"],
        active=row["active"],
        recorded_at=row["recorded_at"],
        evaluation_code=row["evaluation_code"],
        actual_material_state_ref=row["actual_material_state_ref"],
        outcome_material_state_ref=row["outcome_material_state_ref"],
    )


def _operation(value: str) -> str:
    clean = value.strip()
    if clean != value or not clean or len(clean) > 200:
        raise PlanDependencyInputError("Invalid Dependency operation id.")
    return clean


def _qualifier(kind: str, code: str | None) -> tuple[str, str | None]:
    if kind not in _QUALIFIERS or (
        (kind == "actual_occurred" and code is not None)
        or (kind == "outcome_code" and (code is None or _CODE.fullmatch(code) is None))
    ):
        raise PlanDependencyInputError("Invalid typed prerequisite condition.")
    return kind, code


def _fingerprint(payload: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps({"version": 1, **payload}, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _error(exc: DBAPIError) -> Exception:
    cause = getattr(exc, "orig", None)
    state = getattr(cause, "sqlstate", None)
    message = str(cause or exc)
    if state in {"23505", "40001"}:
        return PlanDependencyConflictError(message)
    if state == "23503":
        return PlanDependencyNotFoundError(message)
    if state in {"23514", "22023"}:
        return PlanDependencyInputError(message)
    return PlanDependencyPersistenceError(message)


def _cycle_flags(items: tuple[PlanDependencyView, ...]) -> tuple[PlanDependencyView, ...]:
    """Mark direct assertions participating in a cycle, without inferring new edges."""
    adjacency: dict[UUID, set[UUID]] = {}
    for item in items:
        if item.active:
            adjacency.setdefault(item.prerequisite_step_ref, set()).add(item.dependent_step_ref)
    marked: list[PlanDependencyView] = []
    for item in items:
        if not item.active:
            marked.append(item)
            continue
        seen: set[UUID] = set()
        pending = [item.dependent_step_ref]
        cyclic = False
        while pending:
            node = pending.pop()
            if node == item.prerequisite_step_ref:
                cyclic = True
                break
            if node in seen:
                continue
            seen.add(node)
            pending.extend(adjacency.get(node, ()))
        marked.append(replace(item, cycle=cyclic))
    return tuple(marked)


class PlanDependencyApplication:
    """Read/evaluate and author a self-owned Plan-scoped qualified relation."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def list(
        self, *, self_person_ref: NativeRef, plan_ref: UUID
    ) -> tuple[PlanDependencyView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.list_self_plan_dependencies(:self_ref,:plan_ref)"
                            ),
                            {"self_ref": self_person_ref, "plan_ref": plan_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise PlanDependencyPersistenceError(str(exc)) from exc
        return _cycle_flags(tuple(_read(row) for row in rows))

    async def get(
        self,
        *,
        self_person_ref: NativeRef,
        plan_ref: UUID,
        dependency_ref: UUID,
        state_ref: UUID | None = None,
    ) -> PlanDependencyView | None:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.get_self_plan_dependency("
                                ":self_ref,:plan_ref,:dependency_ref,:state_ref)"
                            ),
                            {
                                "self_ref": self_person_ref,
                                "plan_ref": plan_ref,
                                "dependency_ref": dependency_ref,
                                "state_ref": state_ref,
                            },
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
        except SQLAlchemyError as exc:
            raise PlanDependencyPersistenceError(str(exc)) from exc
        if row is None:
            return None
        view = _read(row)
        if view.active and view.evaluation_code is not None:
            all_items = await self.list(self_person_ref=self_person_ref, plan_ref=plan_ref)
            return next((item for item in all_items if item.dependency_ref == dependency_ref), view)
        return view

    async def history(
        self, *, self_person_ref: NativeRef, plan_ref: UUID, dependency_ref: UUID
    ) -> tuple[PlanDependencyHistoryView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.list_self_plan_dependency_history("
                                ":self_ref,:plan_ref,:dependency_ref)"
                            ),
                            {
                                "self_ref": self_person_ref,
                                "plan_ref": plan_ref,
                                "dependency_ref": dependency_ref,
                            },
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise PlanDependencyPersistenceError(str(exc)) from exc
        return tuple(PlanDependencyHistoryView(**row) for row in rows)

    async def write(
        self,
        *,
        self_person_ref: NativeRef,
        plan_ref: UUID,
        operation_id: str,
        prerequisite_step_ref: UUID,
        dependent_step_ref: UUID,
        qualifier_code: str,
        disposition_code: str | None,
        dependency_ref: UUID | None = None,
        expected_state_ref: UUID | None = None,
        active: bool = True,
    ) -> PlanDependencyView:
        _operation(operation_id)
        _qualifier(qualifier_code, disposition_code)
        if prerequisite_step_ref == dependent_step_ref:
            raise PlanDependencyInputError("A Dependency requires distinct Steps.")
        if dependency_ref is None and (expected_state_ref is not None or not active):
            raise PlanDependencyInputError("A new Dependency must be active.")
        if dependency_ref is not None and expected_state_ref is None:
            raise PlanDependencyInputError("A revision requires its expected current state.")
        chosen_ref = dependency_ref or new_scoped_record_ref()
        params = {
            "self_ref": self_person_ref,
            "operation_id": operation_id,
            "fingerprint": _fingerprint(
                {
                    "plan_ref": str(plan_ref),
                    "dependency_ref": str(dependency_ref) if dependency_ref else None,
                    "expected_state_ref": str(expected_state_ref) if expected_state_ref else None,
                    "prerequisite_step_ref": str(prerequisite_step_ref),
                    "dependent_step_ref": str(dependent_step_ref),
                    "qualifier_code": qualifier_code,
                    "disposition_code": disposition_code,
                    "active": active,
                }
            ),
            "plan_ref": plan_ref,
            "dependency_ref": chosen_ref,
            "expected_state_ref": expected_state_ref,
            "state_ref": new_native_ref(),
            "prerequisite_step_ref": prerequisite_step_ref,
            "dependent_step_ref": dependent_step_ref,
            "qualifier_code": qualifier_code,
            "disposition_code": disposition_code,
            "active": active,
        }
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.write_self_plan_dependency("
                                ":self_ref,:operation_id,:fingerprint,:plan_ref,"
                                ":dependency_ref,:expected_state_ref,:state_ref,"
                                ":prerequisite_step_ref,:dependent_step_ref,"
                                ":qualifier_code,:disposition_code,:active)"
                            ),
                            params,
                        )
                    )
                    .mappings()
                    .one()
                )
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise PlanDependencyPersistenceError(str(exc)) from exc
        result = await self.get(
            self_person_ref=self_person_ref,
            plan_ref=plan_ref,
            dependency_ref=row["dependency_ref"],
            state_ref=row["state_ref"],
        )
        if result is None:
            raise PlanDependencyPersistenceError("Accepted Dependency state unavailable.")
        return replace(result, replayed=row["replayed"])
