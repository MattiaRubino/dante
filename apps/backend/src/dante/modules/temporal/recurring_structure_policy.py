"""Versioned, self-owned structure snapshots for recurring materialization.

The initial Create policy is still the fallback for Occurrences governed by an
older Recurrence state. A replacement state can carry one complete snapshot;
it is never assembled from partially updated Activity/Event fields.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyView
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyView
from dante.platform.database.references import NativeRef

type RecurringStructureOwner = Literal["routine", "event"]


class RecurringStructurePolicyError(RuntimeError):
    """The policy state could not be read or accepted without ambiguity."""


@dataclass(frozen=True, slots=True)
class RecurringStructureRevision:
    accepted_at: datetime
    replayed: bool


class RecurringStructurePolicyApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def supersede_clean_in_session(
        self,
        session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        occurrence_ref: UUID,
        source_ref: UUID,
        replacement_state_ref: UUID,
        operation_id: str,
        effective_zone_id: str,
    ) -> RecurringStructureRevision:
        """Retain history while retiring one rechecked, clean future plan."""
        try:
            row = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.supersede_self_clean_recurring_occurrence("
                            ":actor,:occurrence,:source,:state,:operation,:zone)"
                        ),
                        {
                            "actor": self_person_ref,
                            "occurrence": occurrence_ref,
                            "source": source_ref,
                            "state": replacement_state_ref,
                            "operation": operation_id,
                            "zone": effective_zone_id,
                        },
                    )
                )
                .mappings()
                .one()
            )
        except SQLAlchemyError as exc:
            raise RecurringStructurePolicyError("Future instance changed during revision.") from exc
        return RecurringStructureRevision(accepted_at=row["accepted_at"], replayed=row["replayed"])

    async def replace_in_session(
        self,
        session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        owner: RecurringStructureOwner,
        source_ref: UUID,
        previous_state_ref: UUID,
        recurrence_state_ref: UUID,
        operation_id: str,
        structure_snapshot: dict[str, object],
        request_hash: str,
        preview_fingerprint: str,
        superseded_count: int,
        protected_count: int,
    ) -> RecurringStructureRevision:
        """Persist after Recurrence.replace_in_session, before outer commit."""
        if not structure_snapshot or structure_snapshot.get("version") != 1:
            raise ValueError("Unsupported recurring structure snapshot.")
        try:
            row = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.set_self_recurring_structure_policy_revision("
                            ":actor,:operation,:owner,:source,:previous,:state,CAST(:snapshot AS jsonb),"
                            ":request_hash,:preview,:superseded,:protected)"
                        ),
                        {
                            "actor": self_person_ref,
                            "operation": operation_id,
                            "owner": owner,
                            "source": source_ref,
                            "previous": previous_state_ref,
                            "state": recurrence_state_ref,
                            "snapshot": json.dumps(structure_snapshot, sort_keys=True),
                            "request_hash": request_hash,
                            "preview": preview_fingerprint,
                            "superseded": superseded_count,
                            "protected": protected_count,
                        },
                    )
                )
                .mappings()
                .one()
            )
        except SQLAlchemyError as exc:
            raise RecurringStructurePolicyError("Structure revision was not accepted.") from exc
        return RecurringStructureRevision(accepted_at=row["accepted_at"], replayed=row["replayed"])

    async def _get_snapshot(
        self,
        *,
        self_person_ref: NativeRef,
        owner: RecurringStructureOwner,
        source_ref: UUID,
        recurrence_state_ref: UUID,
    ) -> tuple[dict[str, object], datetime] | None:
        try:
            async with self._session_factory() as session, session.begin():
                result = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.get_self_recurring_structure_policy_revision("
                                ":actor,:owner,:source,:state)"
                            ),
                            {
                                "actor": self_person_ref,
                                "owner": owner,
                                "source": source_ref,
                                "state": recurrence_state_ref,
                            },
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
        except SQLAlchemyError as exc:
            raise RecurringStructurePolicyError("Structure revision could not be read.") from exc
        if result is None:
            return None
        snapshot = result["structure_snapshot"]
        if not isinstance(snapshot, dict) or snapshot.get("version") != 1:
            raise RecurringStructurePolicyError("Stored structure revision is invalid.")
        return snapshot, result["accepted_at"]

    async def get_snapshot_in_session(
        self,
        session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        owner: RecurringStructureOwner,
        source_ref: UUID,
        recurrence_state_ref: UUID,
    ) -> dict[str, object] | None:
        """Read the complete source revision in the caller's consistent snapshot."""
        row = (
            (
                await session.execute(
                    text(
                        "SELECT * FROM dante.get_self_recurring_structure_policy_revision("
                        ":actor,:owner,:source,:state)"
                    ),
                    {
                        "actor": self_person_ref,
                        "owner": owner,
                        "source": source_ref,
                        "state": recurrence_state_ref,
                    },
                )
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        snapshot = row["structure_snapshot"]
        if not isinstance(snapshot, dict) or snapshot.get("version") != 1:
            raise RecurringStructurePolicyError("Stored structure revision is invalid.")
        return snapshot

    async def routine(
        self,
        *,
        self_person_ref: NativeRef,
        routine_ref: UUID,
        recurrence_state_ref: UUID,
    ) -> RoutineOccurrencePolicyView | None:
        found = await self._get_snapshot(
            self_person_ref=self_person_ref,
            owner="routine",
            source_ref=routine_ref,
            recurrence_state_ref=recurrence_state_ref,
        )
        if found is None:
            return None
        value, accepted_at = found
        duration = value.get("duration_minutes")
        reminder = value.get("reminder_lead_minutes")
        template = value.get("activity_template")
        if (
            type(duration) is not int
            or not 1 <= duration <= 525_600
            or (reminder is not None and (type(reminder) is not int or not 0 <= reminder <= 10_080))
            or not isinstance(template, dict)
            or template.get("version") != 1
        ):
            raise RecurringStructurePolicyError("Stored Routine template is invalid.")
        return RoutineOccurrencePolicyView(
            duration_minutes=duration,
            reminder_lead_minutes=reminder,
            activity_template=template,
            created_at=accepted_at,
        )

    async def event(
        self,
        *,
        self_person_ref: NativeRef,
        event_ref: UUID,
        recurrence_state_ref: UUID,
    ) -> EventOccurrencePolicyView | None:
        found = await self._get_snapshot(
            self_person_ref=self_person_ref,
            owner="event",
            source_ref=event_ref,
            recurrence_state_ref=recurrence_state_ref,
        )
        if found is None:
            return None
        value, accepted_at = found
        kind = value.get("placement_kind")
        minutes = value.get("duration_minutes")
        days = value.get("duration_days")
        reminder = value.get("reminder_lead_minutes")
        mode = value.get("reality_mode")
        objectives = value.get("objectives")
        if (
            (
                kind == "timed"
                and (type(minutes) is not int or not 1 <= minutes <= 525_600 or days is not None)
            )
            or (
                kind == "all_day"
                and (
                    type(days) is not int
                    or not 1 <= days <= 3660
                    or minutes is not None
                    or reminder is not None
                )
            )
            or kind not in {"timed", "all_day"}
            or (reminder is not None and (type(reminder) is not int or not 0 <= reminder <= 10_080))
            or mode not in {"manual", "review_on_end", "auto_confirm_outcome"}
            or not isinstance(objectives, list)
            or len(objectives) > 100
            or any(not isinstance(item, dict) for item in objectives)
        ):
            raise RecurringStructurePolicyError("Stored Event template is invalid.")
        return EventOccurrencePolicyView(
            placement_kind=kind,
            duration_minutes=cast(int | None, minutes),
            duration_days=cast(int | None, days),
            reminder_lead_minutes=reminder,
            reality_mode=mode,
            objectives=tuple(objectives),
            created_at=accepted_at,
        )
