"""B05-A1 self-scoped Life Area creation and catalog reads."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef


class LifeAreaInputError(ValueError):
    """The profile command violates the bounded product input contract."""


class LifeAreaOperationIdReuseError(RuntimeError):
    """A self-scoped operation key was reused with different intent."""


class LifeAreaPersistenceError(RuntimeError):
    """The profile command could not safely establish canonical state."""


@dataclass(frozen=True, slots=True)
class LifeAreaView:
    """An actor-local product profile, never a Domain NativeRef."""

    life_area_ref: UUID
    name: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CreatedLifeArea:
    area: LifeAreaView
    replayed: bool


def _area_from_row(record: RowMapping) -> LifeAreaView:
    return LifeAreaView(
        life_area_ref=UUID(str(record["life_area_ref"])),
        name=str(record["name"]),
        created_at=record["created_at"],
    )


class LifeAreaApplication:
    """Each public operation owns exactly one database transaction."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create(
        self, *, self_person_ref: NativeRef, operation_id: str, name: str
    ) -> CreatedLifeArea:
        normalized_name = name.strip()
        normalized_operation = operation_id.strip()
        if not normalized_name or len(normalized_name) > 100:
            raise LifeAreaInputError("Life Area name must contain 1 to 100 characters.")
        if not normalized_operation or len(normalized_operation) > 200:
            raise LifeAreaInputError("Life Area operation id must contain 1 to 200 characters.")
        fingerprint = hashlib.sha256(
            json.dumps(
                {"version": 1, "name": normalized_name},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        try:
            async with self._session_factory() as session, session.begin():
                result = (
                    (
                        await session.execute(
                            text("""
                    SELECT life_area_ref, name, created_at, replayed
                      FROM dante.create_self_life_area(
                        :self_person_ref, :operation_id, :fingerprint, :area_ref, :name
                      )
                """),
                            {
                                "self_person_ref": self_person_ref,
                                "operation_id": normalized_operation,
                                "fingerprint": fingerprint,
                                "area_ref": uuid7(),
                                "name": normalized_name,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                return CreatedLifeArea(_area_from_row(result), bool(result["replayed"]))
        except IntegrityError as exc:
            diagnostic = getattr(exc.orig, "diag", None)
            if getattr(diagnostic, "constraint_name", None) == "pk_life_area_create_operation":
                raise LifeAreaOperationIdReuseError() from exc
            raise LifeAreaPersistenceError() from exc
        except DBAPIError as exc:
            raise LifeAreaPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise LifeAreaPersistenceError() from exc

    async def list(self, *, self_person_ref: NativeRef) -> tuple[LifeAreaView, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    (
                        await session.execute(
                            text("""
                    SELECT life_area_ref, name, created_at
                      FROM dante.list_self_life_areas(:self_person_ref)
                """),
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                return tuple(_area_from_row(row) for row in rows)
        except SQLAlchemyError as exc:
            raise LifeAreaPersistenceError() from exc
