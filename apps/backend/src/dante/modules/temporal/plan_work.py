"""B13-A Plan work structure adapter over guarded PostgreSQL functions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef, new_native_ref


class PlanWorkInputError(ValueError):
    """Input is outside the bounded flat Plan structure contract."""


class PlanWorkNotFoundError(LookupError):
    """The Plan is not owned by the authenticated self Person."""


class PlanWorkConflictError(RuntimeError):
    """Stale current revision or reused operation id."""


class PlanWorkPersistenceError(RuntimeError):
    """A canonical Plan operation could not complete."""


@dataclass(frozen=True, slots=True)
class PlanStepView:
    step_ref: UUID
    position: int
    title: str
    activity_ref: UUID | None
    divisible: bool | None
    max_planned_slices: int | None
    merge_compatible: bool | None
    execution_strength_code: str | None


@dataclass(frozen=True, slots=True)
class PlanWorkView:
    plan_ref: UUID
    state_ref: UUID
    title: str
    created_at: datetime
    steps: tuple[PlanStepView, ...]
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class PlanStepInput:
    step_ref: UUID
    title: str
    activity_ref: UUID | None = None
    divisible: bool | None = None
    max_planned_slices: int | None = None
    merge_compatible: bool | None = None
    execution_strength_code: str | None = None


def _view(row: RowMapping) -> PlanWorkView:
    steps = row["steps"]
    if isinstance(steps, str):
        steps = json.loads(steps)
    if not isinstance(steps, list):
        raise PlanWorkPersistenceError("Stored Plan structure is invalid.")
    return PlanWorkView(
        plan_ref=UUID(str(row["plan_ref"])),
        state_ref=UUID(str(row["state_ref"])),
        title=str(row["title"]),
        created_at=row["created_at"],
        steps=tuple(
            PlanStepView(
                step_ref=UUID(str(item["step_ref"])),
                position=int(item["position"]),
                title=str(item["title"]),
                activity_ref=(
                    UUID(str(item["activity_ref"])) if item["activity_ref"] is not None else None
                ),
                divisible=item["divisible"],
                max_planned_slices=item["max_planned_slices"],
                merge_compatible=item["merge_compatible"],
                execution_strength_code=item["execution_strength_code"],
            )
            for item in steps
        ),
        replayed=bool(row.get("replayed", False)),
    )


def _error(exc: DBAPIError) -> Exception:
    original = getattr(exc, "orig", None)
    state = getattr(original, "sqlstate", None)
    message = str(original or exc)
    if state in {"40001", "23505"}:
        return PlanWorkConflictError(message)
    if state == "23503":
        return PlanWorkNotFoundError(message)
    if state in {"23514", "22023"}:
        return PlanWorkInputError(message)
    return PlanWorkPersistenceError(message)


def _fingerprint(intent: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(
            {"version": 1, **intent},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _operation(operation_id: str) -> str:
    normalized = operation_id.strip()
    if not normalized or len(normalized) > 200:
        raise PlanWorkInputError("Plan operation id is invalid.")
    return normalized


def _title(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 300:
        raise PlanWorkInputError("Plan or Step title is invalid.")
    return normalized


class PlanWorkApplication:
    """Self-scoped Plan authoring; Step remains internal to one Plan."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def list(self, *, self_person_ref: NativeRef) -> tuple[PlanWorkView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text("SELECT * FROM dante.list_self_plan_work(:self_ref)"),
                            {"self_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise PlanWorkPersistenceError(str(exc)) from exc
        return tuple(_view(row) for row in rows)

    async def get(self, *, self_person_ref: NativeRef, plan_ref: UUID) -> PlanWorkView | None:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text("SELECT * FROM dante.get_self_plan_work(:self_ref,:plan_ref)"),
                            {"self_ref": self_person_ref, "plan_ref": plan_ref},
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
        except SQLAlchemyError as exc:
            raise PlanWorkPersistenceError(str(exc)) from exc
        return _view(row) if row is not None else None

    async def create(
        self, *, self_person_ref: NativeRef, operation_id: str, title: str
    ) -> PlanWorkView:
        key = _operation(operation_id)
        clean_title = _title(title)
        params = {
            "self_ref": self_person_ref,
            "operation_id": key,
            "fingerprint": _fingerprint({"kind": "create", "title": clean_title}),
            "plan_ref": new_native_ref(),
            "state_ref": new_native_ref(),
            "title": clean_title,
        }
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.create_self_plan_work("
                                ":self_ref,:operation_id,:fingerprint,:plan_ref,:state_ref,:title)"
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
            raise PlanWorkPersistenceError(str(exc)) from exc
        return _view(row)

    async def replace(
        self,
        *,
        self_person_ref: NativeRef,
        plan_ref: UUID,
        expected_state_ref: UUID,
        operation_id: str,
        title: str,
        steps: tuple[PlanStepInput, ...],
    ) -> PlanWorkView:
        key = _operation(operation_id)
        clean_title = _title(title)
        if len(steps) > 1000:
            raise PlanWorkInputError("Plan has too many Steps.")
        payload = [
            {
                "step_ref": str(step.step_ref),
                "title": _title(step.title),
                "activity_ref": str(step.activity_ref) if step.activity_ref else None,
                "divisible": step.divisible,
                "max_planned_slices": step.max_planned_slices,
                "merge_compatible": step.merge_compatible,
                "execution_strength_code": step.execution_strength_code,
            }
            for step in steps
        ]
        params = {
            "self_ref": self_person_ref,
            "operation_id": key,
            "fingerprint": _fingerprint(
                {
                    "kind": "replace",
                    "plan_ref": str(plan_ref),
                    "expected_state_ref": str(expected_state_ref),
                    "title": clean_title,
                    "steps": payload,
                }
            ),
            "plan_ref": plan_ref,
            "expected_state_ref": expected_state_ref,
            "state_ref": new_native_ref(),
            "title": clean_title,
            "steps": json.dumps(payload, separators=(",", ":")),
        }
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.replace_self_plan_work("
                                ":self_ref,:operation_id,:fingerprint,:plan_ref,"
                                ":expected_state_ref,:state_ref,:title,CAST(:steps AS jsonb))"
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
            raise PlanWorkPersistenceError(str(exc)) from exc
        return _view(row)
