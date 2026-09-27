"""B11-C personal Schedule Reminder adapter over guarded PostgreSQL authority."""

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
    new_material_state_ref,
    new_scoped_record_ref,
)

ReminderDisposition = Literal["pending", "due", "unavailable"]


class ScheduleReminderInputError(ValueError):
    """Requested configuration is outside the bounded B11-C contract."""


class ScheduleReminderNotFoundError(LookupError):
    """Schedule or Reminder is not in this self scope."""


class ScheduleReminderConflictError(RuntimeError):
    """Stale current MaterialState or reused operation id."""


class ScheduleReminderPersistenceError(RuntimeError):
    """Canonical database operation could not complete."""


@dataclass(frozen=True, slots=True)
class ScheduleReminderView:
    reminder_ref: ScopedRecordRef
    schedule_ref: ScopedRecordRef
    material_state_ref: MaterialStateRef
    enabled: bool
    lead_minutes: int
    schedule_starts_at: datetime | None
    due_at: datetime | None
    disposition_code: ReminderDisposition
    replayed: bool = False


def _view(row: RowMapping) -> ScheduleReminderView:
    disposition = row["disposition_code"]
    if disposition not in {"pending", "due", "unavailable"}:
        raise ScheduleReminderPersistenceError("Stored Reminder disposition is invalid.")
    return ScheduleReminderView(
        reminder_ref=ScopedRecordRef(UUID(str(row["reminder_ref"]))),
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        enabled=bool(row["enabled"]),
        lead_minutes=int(row["lead_minutes"]),
        schedule_starts_at=row["schedule_starts_at"],
        due_at=row["due_at"],
        disposition_code=disposition,
        replayed=bool(row.get("replayed", False)),
    )


def _error(exc: DBAPIError) -> RuntimeError:
    original = getattr(exc, "orig", None)
    sqlstate = getattr(original, "sqlstate", None)
    diagnostic = getattr(original, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None) if diagnostic else None
    message = str(original or exc)
    if sqlstate in {"40001", "23505"} or constraint in {
        "schedule_reminder_current_conflict", "schedule_reminder_operation_reused"
    }:
        return ScheduleReminderConflictError(message)
    if sqlstate in {"23503", "P0002"}:
        return ScheduleReminderNotFoundError(message)
    if sqlstate in {"23514", "22023"}:
        return ScheduleReminderInputError(message)
    return ScheduleReminderPersistenceError(message)


class ScheduleReminderApplication:
    """Read and configure one personal Reminder per owned Schedule."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def get(
        self, *, self_person_ref: NativeRef, schedule_ref: ScopedRecordRef
    ) -> ScheduleReminderView | None:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_schedule_reminder(:actor,:schedule_ref)"),
                        {"actor": self_person_ref, "schedule_ref": schedule_ref},
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise ScheduleReminderPersistenceError(str(exc)) from exc
        return _view(row) if row is not None else None

    async def configure(
        self,
        *,
        self_person_ref: NativeRef,
        schedule_ref: ScopedRecordRef,
        operation_id: str,
        expected_material_state_ref: MaterialStateRef | None,
        enabled: bool,
        lead_minutes: int,
    ) -> ScheduleReminderView:
        key = operation_id.strip()
        if not key or len(key) > 200 or not 0 <= lead_minutes <= 10080:
            raise ScheduleReminderInputError("Reminder operation id or lead is invalid.")
        fingerprint = hashlib.sha256(
            json.dumps(
                {
                    "version": 1,
                    "schedule_ref": str(schedule_ref),
                    "expected_material_state_ref": (
                        str(expected_material_state_ref)
                        if expected_material_state_ref is not None else None
                    ),
                    "enabled": enabled,
                    "lead_minutes": lead_minutes,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            """SELECT * FROM dante.configure_self_schedule_reminder(
                                 :actor,:operation_id,:fingerprint,:schedule_ref,
                                 :expected_state,:reminder_ref,:material_state_ref,
                                 :enabled,:lead_minutes)"""
                        ),
                        {
                            "actor": self_person_ref,
                            "operation_id": key,
                            "fingerprint": fingerprint,
                            "schedule_ref": schedule_ref,
                            "expected_state": expected_material_state_ref,
                            "reminder_ref": new_scoped_record_ref(),
                            "material_state_ref": new_material_state_ref(),
                            "enabled": enabled,
                            "lead_minutes": lead_minutes,
                        },
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise ScheduleReminderPersistenceError(str(exc)) from exc
        if row is None:
            raise ScheduleReminderPersistenceError("Reminder write returned no canonical state.")
        return _view(row)
