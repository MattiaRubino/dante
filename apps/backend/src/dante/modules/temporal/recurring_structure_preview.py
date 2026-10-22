"""Read-only structural series preview from a complete canonical inventory.

The preview never authorizes a mutation. Structural acceptance must re-read
and revalidate everything under the recurrence source lock.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    OccurrenceView,
    _candidate_instant,
    _zone,
)
from dante.modules.temporal.occurrence_edit_inventory import (
    OccurrenceEditInventory,
    OccurrenceEditInventoryApplication,
)
from dante.modules.temporal.occurrence_edit_scope import (
    EditScope,
    RecurrenceEditCandidate,
    RecurrenceEditScopePlan,
    select_recurrence_edit_scope,
)
from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_series_reconciliation import (
    MaterializedSeriesInstance,
    SeriesReconciliation,
    SeriesReconciliationWindow,
    preview_calendar_series_reconciliation,
)
from dante.platform.database.references import NativeRef


class StructuralSeriesPreviewConflict(ValueError):
    """The SQL protection preview and Python inventory do not agree."""


@dataclass(frozen=True, slots=True)
class StructuralSeriesPreview:
    source_native_ref: UUID
    recurrence_state_ref: UUID | None
    profile_edit_revision: int
    selected_occurrence_ref: UUID
    scope_code: EditScope
    source_preview_fingerprint: str
    proposed_preview_fingerprint: str
    reconciliation: SeriesReconciliation
    protected_occurrences: tuple[dict[str, object], ...]
    apply_authorized: bool = False


def structural_scope(
    *,
    inventory: OccurrenceEditInventory,
    protections: dict[UUID, str | None],
    scope_code: EditScope,
    effective_zone_id: str,
) -> tuple[RecurrenceEditScopePlan, tuple[MaterializedSeriesInstance, ...]]:
    """Classify generated identities from guarded database protection reasons."""
    zone = _zone(effective_zone_id)
    expected = {item.occurrence_ref for item in inventory.occurrences}
    if set(protections) != expected:
        raise StructuralSeriesPreviewConflict("Protection inventory is incomplete.")
    candidates: list[RecurrenceEditCandidate] = []
    generated: list[MaterializedSeriesInstance] = []
    for item in inventory.occurrences:
        coordinate = item.coordinate
        if item.origin_code == "recurrence_generated":
            if not isinstance(coordinate, CalendarCoordinate):
                raise StructuralSeriesPreviewConflict(
                    "Structural calendar preview requires calendar-generated instances."
                )
            generated.append(MaterializedSeriesInstance(item.occurrence_ref, coordinate))
        reason = protections[item.occurrence_ref]
        if reason not in {None, "registration", "skipped", "local_change", "legacy_unknown"}:
            raise StructuralSeriesPreviewConflict("Unknown protected exception reason.")
        candidates.append(
            RecurrenceEditCandidate(
                occurrence_ref=item.occurrence_ref,
                source_native_ref=item.source_native_ref,
                expected_at=(
                    _candidate_instant(coordinate, zone)
                    if isinstance(coordinate, CalendarCoordinate)
                    else None
                ),
                origin_code=item.origin_code,
                skipped=item.skipped or reason == "skipped",
                has_override=reason in {"local_change", "legacy_unknown"},
                has_recorded_facts=reason == "registration",
            )
        )
    scope = select_recurrence_edit_scope(
        selected_occurrence_ref=inventory.selected_occurrence_ref,
        scope=scope_code,
        candidates=tuple(candidates),
        captured_at=inventory.captured_at,
        authoritative_inventory=True,
    )
    return scope, tuple(generated)


class RecurringStructurePreviewApplication:
    """Prepare the guarded candidate in one consistent read-only transaction."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._inventories = OccurrenceEditInventoryApplication(session_factory)

    async def preview(
        self,
        *,
        self_person_ref: NativeRef,
        selected_occurrence_ref: UUID,
        scope_code: EditScope,
        proposed_recurrence: CalendarRecurrence,
        window: SeriesReconciliationWindow,
        effective_zone_id: str,
    ) -> StructuralSeriesPreview:
        if scope_code not in {"this_and_following", "from_next"}:
            raise StructuralSeriesPreviewConflict("Use a following scope for series edits.")
        async with self._session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
            inventory = await self._inventories.read_in_session(
                session,
                self_person_ref=self_person_ref,
                selected_occurrence_ref=selected_occurrence_ref,
            )
            rows = (
                await session.execute(
                    text(
                        "SELECT occurrence_ref, "
                        "dante.get_self_occurrence_edit_protection(:actor,occurrence_ref) "
                        "AS reason FROM dante.list_self_recurrence_edit_occurrences("
                        ":actor,:selected)"
                    ),
                    {"actor": self_person_ref, "selected": selected_occurrence_ref},
                )
            ).mappings().all()
            protections = {
                UUID(str(row["occurrence_ref"])): row["reason"]
                for row in rows
            }
            scope, generated = structural_scope(
                inventory=inventory,
                protections=protections,
                scope_code=scope_code,
                effective_zone_id=effective_zone_id,
            )
            source_preview = (
                await session.execute(
                    text(
                        "SELECT * FROM dante.get_self_occurrence_profile_edit_preview("
                        ":actor,:selected,:scope,:zone)"
                    ),
                    {
                        "actor": self_person_ref,
                        "selected": selected_occurrence_ref,
                        "scope": scope_code,
                        "zone": effective_zone_id,
                    },
                )
            ).mappings().one()
            protected = tuple(source_preview["protected_occurrences"] or ())
            if (
                source_preview["source_native_ref"] != inventory.source_native_ref
                or set(source_preview["target_occurrence_refs"] or ())
                != set(scope.target_occurrence_refs)
                or {
                    UUID(str(row["occurrence_ref"])) for row in protected
                } != set(scope.protected_future_occurrence_refs)
            ):
                raise StructuralSeriesPreviewConflict(
                    "Canonical preview changed during structural planning."
                )
            plan = preview_calendar_series_reconciliation(
                scope=scope,
                materialized=generated,
                proposed_recurrence=proposed_recurrence,
                window=window,
                effective_zone_id=effective_zone_id,
                authoritative_inventory=True,
            )
            intent = {
                "source_fingerprint": source_preview["fingerprint"],
                "scope": scope_code,
                "recurrence": asdict(proposed_recurrence),
                "window": asdict(window),
                "retained": plan.retained_occurrence_refs,
                "superseded": plan.superseded_occurrence_refs,
                "new": tuple(asdict(x) for x in plan.new_coordinates),
                "protected": plan.protected_occurrence_refs,
            }
            fingerprint = hashlib.sha256(
                json.dumps(intent, sort_keys=True, default=str, separators=(",", ":")).encode(
                    "utf-8"
                )
            ).hexdigest()
            return StructuralSeriesPreview(
                source_native_ref=inventory.source_native_ref,
                recurrence_state_ref=source_preview["recurrence_state_ref"],
                profile_edit_revision=int(source_preview["edit_revision"]),
                selected_occurrence_ref=selected_occurrence_ref,
                scope_code=scope_code,
                source_preview_fingerprint=source_preview["fingerprint"],
                proposed_preview_fingerprint=fingerprint,
                reconciliation=plan,
                protected_occurrences=protected,
            )
