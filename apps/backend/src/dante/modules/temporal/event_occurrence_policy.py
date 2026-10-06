"""B14 recurring Event occurrence Schedule and Reminder policy."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef

EventOccurrencePlacementKind = Literal["timed", "all_day"]


class EventOccurrencePolicyInputError(ValueError):
    """The recurring Event occurrence policy is malformed."""


class EventOccurrencePolicyNotFoundError(LookupError):
    """The recurring Event source is unavailable in self scope."""


class EventOccurrencePolicyConflictError(RuntimeError):
    """An immutable recurring Event policy already exists with different intent."""


class EventOccurrencePolicyPersistenceError(RuntimeError):
    """Recurring Event policy truth could not be read or written safely."""


@dataclass(frozen=True, slots=True)
class EventOccurrencePolicyView:
    placement_kind: EventOccurrencePlacementKind
    duration_minutes: int | None
    duration_days: int | None
    reminder_lead_minutes: int | None
    created_at: datetime
    replayed: bool = False


def _error(exc: DBAPIError) -> Exception:
    original = getattr(exc, "orig", None)
    diagnostic = getattr(original, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None) if diagnostic else None
    if constraint == "event_occurrence_policy_invalid":
        return EventOccurrencePolicyInputError("Event occurrence policy is invalid.")
    if constraint == "event_occurrence_policy_event_unavailable":
        return EventOccurrencePolicyNotFoundError("Event occurrence policy source unavailable.")
    if constraint == "pk_event_occurrence_policy":
        return EventOccurrencePolicyConflictError(
            "Event occurrence policy already exists with different intent."
        )
    return EventOccurrencePolicyPersistenceError(str(original or exc))


class EventOccurrencePolicyApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def set(
        self,
        *,
        self_person_ref: NativeRef,
        event_ref: UUID,
        placement_kind: EventOccurrencePlacementKind,
        duration_minutes: int | None,
        duration_days: int | None,
        reminder_lead_minutes: int | None,
    ) -> EventOccurrencePolicyView:
        if placement_kind == "timed":
            if duration_minutes is None or not 1 <= duration_minutes <= 525_600:
                raise EventOccurrencePolicyInputError(
                    "Timed Event duration must contain 1 to 525600 minutes."
                )
            if duration_days is not None:
                raise EventOccurrencePolicyInputError(
                    "Timed Event policy cannot contain all-day duration."
                )
        elif placement_kind == "all_day":
            if duration_days is None or not 1 <= duration_days <= 3660:
                raise EventOccurrencePolicyInputError(
                    "All-day Event duration must contain 1 to 3660 days."
                )
            if duration_minutes is not None or reminder_lead_minutes is not None:
                raise EventOccurrencePolicyInputError(
                    "All-day Event policy cannot contain clock duration or Reminder."
                )
        else:
            raise EventOccurrencePolicyInputError("Event placement kind is unsupported.")

        if (
            reminder_lead_minutes is not None
            and not 0 <= reminder_lead_minutes <= 10_080
        ):
            raise EventOccurrencePolicyInputError(
                "Event Reminder lead must contain 0 to 10080 minutes."
            )

        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            """SELECT * FROM dante.set_self_event_occurrence_policy(
                                 :actor,:event,:kind,:minutes,:days,:reminder)"""
                        ),
                        {
                            "actor": self_person_ref,
                            "event": event_ref,
                            "kind": placement_kind,
                            "minutes": duration_minutes,
                            "days": duration_days,
                            "reminder": reminder_lead_minutes,
                        },
                    )
                ).mappings().one()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise EventOccurrencePolicyPersistenceError(str(exc)) from exc
        return EventOccurrencePolicyView(
            placement_kind=row["placement_kind"],
            duration_minutes=(
                None if row["duration_minutes"] is None else int(row["duration_minutes"])
            ),
            duration_days=None if row["duration_days"] is None else int(row["duration_days"]),
            reminder_lead_minutes=(
                None
                if row["reminder_lead_minutes"] is None
                else int(row["reminder_lead_minutes"])
            ),
            created_at=row["created_at"],
            replayed=bool(row["replayed"]),
        )

    async def get(
        self,
        *,
        self_person_ref: NativeRef,
        event_ref: UUID,
    ) -> EventOccurrencePolicyView | None:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_event_occurrence_policy(:actor,:event)"
                        ),
                        {"actor": self_person_ref, "event": event_ref},
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise EventOccurrencePolicyPersistenceError(str(exc)) from exc
        if row is None:
            return None
        return EventOccurrencePolicyView(
            placement_kind=row["placement_kind"],
            duration_minutes=(
                None if row["duration_minutes"] is None else int(row["duration_minutes"])
            ),
            duration_days=None if row["duration_days"] is None else int(row["duration_days"]),
            reminder_lead_minutes=(
                None
                if row["reminder_lead_minutes"] is None
                else int(row["reminder_lead_minutes"])
            ),
            created_at=row["created_at"],
        )
