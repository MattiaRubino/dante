"""B14 recurring Activity placement and Reminder policy.

A Routine owns the reusable policy for the Schedules created from its Occurrences.
Schedule placement remains B02 truth and every concrete Reminder remains B11-C
truth on the resulting Schedule.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef


class RoutineOccurrencePolicyInputError(ValueError):
    """The recurring placement/Reminder policy is malformed."""


class RoutineOccurrencePolicyNotFoundError(LookupError):
    """The Routine is unavailable in the authenticated self scope."""


class RoutineOccurrencePolicyConflictError(RuntimeError):
    """An existing policy represents different immutable Create intent."""


class RoutineOccurrencePolicyPersistenceError(RuntimeError):
    """Canonical policy state could not be read or written safely."""


@dataclass(frozen=True, slots=True)
class RoutineOccurrencePolicyView:
    duration_minutes: int
    reminder_lead_minutes: int | None
    created_at: datetime
    replayed: bool = False


def _error(exc: DBAPIError) -> Exception:
    original = getattr(exc, "orig", None)
    diagnostic = getattr(original, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None) if diagnostic else None
    if constraint == "routine_occurrence_policy_invalid":
        return RoutineOccurrencePolicyInputError("Routine occurrence policy is invalid.")
    if constraint == "routine_occurrence_policy_routine_unavailable":
        return RoutineOccurrencePolicyNotFoundError("Routine occurrence policy source unavailable.")
    if constraint == "pk_routine_occurrence_policy":
        return RoutineOccurrencePolicyConflictError(
            "Routine occurrence policy already exists with different intent."
        )
    return RoutineOccurrencePolicyPersistenceError(str(original or exc))


class RoutineOccurrencePolicyApplication:
    """Adapter over the B14 policy capabilities introduced by migration 107."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def set(
        self,
        *,
        self_person_ref: NativeRef,
        routine_ref: UUID,
        duration_minutes: int,
        reminder_lead_minutes: int | None,
    ) -> RoutineOccurrencePolicyView:
        if not 1 <= duration_minutes <= 525_600:
            raise RoutineOccurrencePolicyInputError(
                "Routine duration must contain 1 to 525600 minutes."
            )
        if reminder_lead_minutes is not None and not 0 <= reminder_lead_minutes <= 10_080:
            raise RoutineOccurrencePolicyInputError(
                "Routine Reminder lead must contain 0 to 10080 minutes."
            )
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            """SELECT * FROM dante.set_self_routine_occurrence_policy(
                                 :actor,:routine,:duration,:reminder)"""
                        ),
                        {
                            "actor": self_person_ref,
                            "routine": routine_ref,
                            "duration": duration_minutes,
                            "reminder": reminder_lead_minutes,
                        },
                    )
                ).mappings().one()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RoutineOccurrencePolicyPersistenceError(str(exc)) from exc
        return RoutineOccurrencePolicyView(
            duration_minutes=int(row["duration_minutes"]),
            reminder_lead_minutes=(
                int(row["reminder_lead_minutes"])
                if row["reminder_lead_minutes"] is not None
                else None
            ),
            created_at=row["created_at"],
            replayed=bool(row["replayed"]),
        )

    async def get(
        self,
        *,
        self_person_ref: NativeRef,
        routine_ref: UUID,
    ) -> RoutineOccurrencePolicyView | None:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_routine_occurrence_policy(:actor,:routine)"
                        ),
                        {"actor": self_person_ref, "routine": routine_ref},
                    )
                ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RoutineOccurrencePolicyPersistenceError(str(exc)) from exc
        if row is None:
            return None
        return RoutineOccurrencePolicyView(
            duration_minutes=int(row["duration_minutes"]),
            reminder_lead_minutes=(
                int(row["reminder_lead_minutes"])
                if row["reminder_lead_minutes"] is not None
                else None
            ),
            created_at=row["created_at"],
        )
