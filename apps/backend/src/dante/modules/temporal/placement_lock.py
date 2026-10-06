"""Self-scoped, CAS-protected user lock for accepted Activity Schedules."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef, ScopedRecordRef


class PlacementLockNotFoundError(LookupError):
    """Schedule is not owned by the authenticated self person."""


class PlacementLockConflictError(RuntimeError):
    """The lock changed since the submitted revision."""


class PlacementLockPersistenceError(RuntimeError):
    """Canonical lock state is temporarily unavailable."""


@dataclass(frozen=True, slots=True)
class PlacementLockView:
    schedule_ref: ScopedRecordRef
    locked: bool
    revision: int
    updated_at: datetime | None
    replayed: bool = False


def _error(exc: DBAPIError) -> Exception:
    original = getattr(exc, "orig", None)
    diagnostic = getattr(original, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None) if diagnostic else None
    if constraint == "schedule_placement_lock_schedule_unavailable":
        return PlacementLockNotFoundError()
    if constraint == "schedule_placement_lock_stale":
        return PlacementLockConflictError()
    return PlacementLockPersistenceError(str(original or exc))


def _view(row: object, *, replayed: bool = False) -> PlacementLockView:
    if not isinstance(row, Mapping):
        raise PlacementLockPersistenceError("Invalid canonical lock response")
    return PlacementLockView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        locked=bool(row["locked"]),
        revision=int(row["revision"]),
        updated_at=row["updated_at"],
        replayed=bool(row["replayed"]) if "replayed" in row else replayed,
    )


class PlacementLockApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def get(
        self, *, self_person_ref: NativeRef, schedule_ref: ScopedRecordRef
    ) -> PlacementLockView:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_schedule_placement_lock(:actor,:schedule)"),
                        {"actor": self_person_ref, "schedule": schedule_ref},
                    )
                ).mappings().one_or_none()
        except SQLAlchemyError as exc:
            raise PlacementLockPersistenceError() from exc
        if row is None:
            raise PlacementLockNotFoundError()
        return _view(row)

    async def set(
        self, *, self_person_ref: NativeRef, schedule_ref: ScopedRecordRef,
        locked: bool, expected_revision: int | None,
    ) -> PlacementLockView:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.set_self_schedule_placement_lock("
                            ":actor,:schedule,:locked,:expected_revision)"
                        ),
                        {
                            "actor": self_person_ref,
                            "schedule": schedule_ref,
                            "locked": locked,
                            "expected_revision": expected_revision,
                        },
                    )
                ).mappings().one()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise PlacementLockPersistenceError() from exc
        return _view(row)
