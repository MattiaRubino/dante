"""B03-A Event application operations over canonical PostgreSQL state."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.mappings.event import EventExpectationRow
from dante.platform.database.references import NativeRef, new_native_ref


class EventInputError(ValueError):
    """The requested Event cannot be admitted by the activated B03-A contract."""


class EventOperationIdReuseError(RuntimeError):
    """One operation id was reused for a different canonical Event intent."""


class EventNotFoundError(LookupError):
    """The requested Event is not visible inside the authenticated self scope."""


class EventPersistenceError(RuntimeError):
    """Canonical Event persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class EventView:
    """Application projection of the minimum Event expectation state."""

    event_ref: NativeRef
    title: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CreateEventResult:
    """Canonical create result, including truthful idempotent replay state."""

    event: EventView
    replayed: bool


def _normalize_title(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 300:
        raise EventInputError("Event title must contain 1 to 300 non-padding characters.")
    return normalized


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise EventInputError("Event operation id must contain 1 to 200 characters.")
    return normalized


def _intent_fingerprint(*, title: str) -> str:
    payload = json.dumps(
        {"title": title},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _constraint_name(exc: IntegrityError) -> str | None:
    original = exc.orig
    diagnostic = getattr(original, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _event_from_row(row: RowMapping) -> EventView:
    return EventView(
        event_ref=NativeRef(UUID(str(row["event_ref"]))),
        title=str(row["title"]),
        created_at=row["created_at"],
    )


class TemporalEventApplication:
    """Transaction-owning Event operations; adapters never commit independently."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _execute_create_event(
        self,
        database_session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        requested_event_ref: NativeRef,
    ) -> CreateEventResult:
        fingerprint = _intent_fingerprint(title=title)
        statement = text(
            """
            SELECT event_ref, title, created_at, replayed
            FROM dante.create_self_event(
                :self_person_ref,
                :operation_id,
                :intent_fingerprint,
                :event_ref,
                :title
            )
            """
        )
        row = (
            (
                await database_session.execute(
                    statement,
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": operation_id,
                        "intent_fingerprint": fingerprint,
                        "event_ref": requested_event_ref,
                        "title": title,
                    },
                )
            )
            .mappings()
            .one()
        )
        return CreateEventResult(
            event=_event_from_row(row),
            replayed=bool(row["replayed"]),
        )

    async def create_event(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
    ) -> CreateEventResult:
        """Create one self-owned Event expectation through the bounded DB capability."""
        normalized_title = _normalize_title(title)
        normalized_operation_id = _normalize_operation_id(operation_id)
        event_ref = new_native_ref()

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                return await self._execute_create_event(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=normalized_title,
                    requested_event_ref=event_ref,
                )
        except IntegrityError as exc:
            if _constraint_name(exc) == "pk_event_create_operation":
                raise EventOperationIdReuseError() from exc
            raise EventPersistenceError() from exc
        except DBAPIError as exc:
            raise EventPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise EventPersistenceError() from exc

    async def get_event(
        self,
        *,
        self_person_ref: NativeRef,
        event_ref: NativeRef,
    ) -> EventView | None:
        """Read one Event only inside the authenticated self Person scope."""
        statement = select(EventExpectationRow).where(
            EventExpectationRow.event_ref == event_ref,
            EventExpectationRow.self_person_ref == self_person_ref,
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = await database_session.scalar(statement)
        except SQLAlchemyError as exc:
            raise EventPersistenceError() from exc

        if row is None:
            return None
        return EventView(
            event_ref=row.event_ref,
            title=row.title,
            created_at=row.created_at,
        )
