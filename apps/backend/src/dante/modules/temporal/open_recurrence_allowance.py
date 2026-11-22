"""Owner-scoped renewal of open calendar recurrence generation budgets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.occurrence import (
    RecurrenceHistoryEntry,
    _candidate_instant,
    _history_entry,
    evaluate_open_calendar_allowance,
)
from dante.platform.database.references import NativeRef

AllowanceOwner = Literal["routine", "event"]
AllowanceDecision = Literal["extend", "decline"]
INITIAL_ALLOWANCE = 730
RENEWAL_NOTICE_THRESHOLD_DAYS = 30


class AllowanceConflictError(RuntimeError):
    """The series or renewal revision changed since the notice was read."""


class AllowanceUnavailableError(RuntimeError):
    """The series is unavailable to this actor or is not an open calendar rule."""


class AllowancePersistenceError(RuntimeError):
    """The durable renewal decision was not accepted."""


def pending_open_allowance_days(
    history: tuple[RecurrenceHistoryEntry, ...],
    *,
    today: date,
    effective_zone_id: str,
    allowed_count: int,
) -> int | None:
    """Return remaining expected slots only if the cap is within 30 local days.

    One prefix evaluation counts all accepted expected coordinates through the
    notice window, including skipped dates. Subtracting only the projected
    *future* candidates gives the slots consumed through today. This
    preserves the original remaining-count convention and avoids mistaking
    30 weekly or monthly occurrences for 30 days.
    """
    upcoming, consumed_through_notice = evaluate_open_calendar_allowance(
        history,
        start_date=today,
        end_date_exclusive=today + timedelta(days=RENEWAL_NOTICE_THRESHOLD_DAYS + 1),
        effective_zone_id=effective_zone_id,
        allowed_count=allowed_count,
    )
    if consumed_through_notice < allowed_count:
        return None
    zone = ZoneInfo(effective_zone_id)
    still_future = sum(
        _candidate_instant(candidate.coordinate, zone).astimezone(zone).date() > today
        for candidate in upcoming
    )
    consumed_through_today = consumed_through_notice - still_future
    return max(0, allowed_count - consumed_through_today)


@dataclass(frozen=True, slots=True)
class AllowanceNotice:
    owner: AllowanceOwner
    source_ref: UUID
    title: str
    material_state_ref: UUID
    allowed_count: int
    remaining_count: int
    revision: int


class OpenRecurrenceAllowanceApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _notice(
        self,
        session: AsyncSession,
        *,
        actor: NativeRef,
        owner: AllowanceOwner,
        source_ref: UUID,
        title: str,
        today: date,
        effective_zone_id: str,
    ) -> AllowanceNotice | None:
        allowance = (
            (
                await session.execute(
                    text(
                        "SELECT * FROM dante.get_self_open_recurrence_allowance(:actor,:owner,:source)"
                    ),
                    {"actor": actor, "owner": owner, "source": source_ref},
                )
            )
            .mappings()
            .one_or_none()
        )
        if allowance is None or allowance["declined"]:
            return None
        rows = (
            (
                await session.execute(
                    text(
                        {
                            "routine": "SELECT * FROM dante.list_self_routine_recurrence_history(:actor,:source)",
                            "event": "SELECT * FROM dante.list_self_event_recurrence_history(:actor,:source)",
                        }[owner]
                    ),
                    {"actor": actor, "source": source_ref},
                )
            )
            .mappings()
            .all()
        )
        remaining = pending_open_allowance_days(
            tuple(_history_entry(row) for row in rows),
            today=today,
            effective_zone_id=effective_zone_id,
            allowed_count=int(allowance["allowed_count"]),
        )
        if remaining is None:
            return None
        return AllowanceNotice(
            owner=owner,
            source_ref=source_ref,
            title=title,
            material_state_ref=UUID(str(allowance["material_state_ref"])),
            allowed_count=int(allowance["allowed_count"]),
            remaining_count=remaining,
            revision=int(allowance["revision"]),
        )

    async def list_notices(
        self, *, actor: NativeRef, today: date, effective_zone_id: str
    ) -> tuple[AllowanceNotice, ...]:
        try:
            async with self._session_factory() as session, session.begin():
                sources = (
                    (
                        await session.execute(
                            text("""
                            SELECT 'routine' AS owner, r.routine_ref AS source_ref, r.title
                              FROM dante.list_self_routines(:actor) r
                              JOIN LATERAL dante.get_self_open_recurrence_allowance(
                                :actor, 'routine', r.routine_ref
                              ) allowance ON true
                             WHERE r.lifecycle_state = 'active'
                            UNION ALL
                            SELECT 'event' AS owner, e.event_ref AS source_ref, e.title
                              FROM dante.event_expectation e
                              JOIN LATERAL dante.get_self_open_recurrence_allowance(
                                :actor, 'event', e.event_ref
                              ) allowance ON true
                             WHERE e.self_person_ref = :actor
                        """),
                            {"actor": actor},
                        )
                    )
                    .mappings()
                    .all()
                )
                notices = []
                for source in sources:
                    notice = await self._notice(
                        session,
                        actor=actor,
                        owner=source["owner"],
                        source_ref=UUID(str(source["source_ref"])),
                        title=str(source["title"]),
                        today=today,
                        effective_zone_id=effective_zone_id,
                    )
                    if notice is not None:
                        notices.append(notice)
                return tuple(notices)
        except SQLAlchemyError as exc:
            raise AllowancePersistenceError() from exc

    async def decide(
        self,
        *,
        actor: NativeRef,
        owner: AllowanceOwner,
        source_ref: UUID,
        title: str,
        today: date,
        effective_zone_id: str,
        expected_state_ref: UUID,
        expected_revision: int,
        operation_id: str,
        decision: AllowanceDecision,
    ) -> None:
        if not operation_id.strip() or len(operation_id) > 200:
            raise AllowanceConflictError()
        try:
            async with self._session_factory() as session, session.begin():
                prior = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.get_self_open_recurrence_allowance_operation(:actor,:operation)"
                            ),
                            {"actor": actor, "operation": operation_id},
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
                if prior is not None:
                    if (
                        prior["owner_code"] != owner
                        or UUID(str(prior["source_ref"])) != source_ref
                        or UUID(str(prior["expected_state_ref"])) != expected_state_ref
                        or prior["expected_revision"] != expected_revision
                        or prior["decision"] != decision
                    ):
                        raise AllowanceConflictError()
                    return
                notice = await self._notice(
                    session,
                    actor=actor,
                    owner=owner,
                    source_ref=source_ref,
                    title=title,
                    today=today,
                    effective_zone_id=effective_zone_id,
                )
                if notice is None:
                    raise AllowanceUnavailableError()
                if (notice.material_state_ref, notice.revision) != (
                    expected_state_ref,
                    expected_revision,
                ):
                    raise AllowanceConflictError()
                row = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.decide_self_open_recurrence_allowance(:actor,:owner,:source,:state,:revision,:operation,:decision)"
                            ),
                            {
                                "actor": actor,
                                "owner": owner,
                                "source": source_ref,
                                "state": expected_state_ref,
                                "revision": expected_revision,
                                "operation": operation_id,
                                "decision": decision,
                            },
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
                if row is None:
                    raise AllowanceUnavailableError()
        except AllowanceConflictError, AllowanceUnavailableError:
            raise
        except DBAPIError as exc:
            constraint = getattr(getattr(exc.orig, "diag", None), "constraint_name", "")
            if constraint in {
                "open_recurrence_allowance_state_conflict",
                "open_recurrence_allowance_operation_reused",
            }:
                raise AllowanceConflictError() from exc
            raise AllowancePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise AllowancePersistenceError() from exc
