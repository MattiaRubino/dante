"""Reconcile calendar Occurrence identities under an authoritative series preview.

This is a pure plan. The caller must validate the inventory under the source
lock and persist every transition together with the revised source policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from uuid import UUID

from dante.modules.temporal.occurrence import CalendarCoordinate
from dante.modules.temporal.occurrence_edit_scope import RecurrenceEditScopePlan


class SeriesReconciliationError(ValueError):
    """A proposed cadence or materialized inventory is ambiguous."""


@dataclass(frozen=True, slots=True)
class MaterializedSeriesInstance:
    occurrence_ref: UUID
    coordinate: CalendarCoordinate


@dataclass(frozen=True, slots=True)
class SeriesReconciliation:
    retained_occurrence_refs: tuple[UUID, ...]
    superseded_occurrence_refs: tuple[UUID, ...]
    new_coordinates: tuple[CalendarCoordinate, ...]
    protected_occurrence_refs: tuple[UUID, ...]


def _key(coordinate: CalendarCoordinate) -> tuple[str, ...]:
    resolved = coordinate.resolved_at
    if resolved is not None and (resolved.tzinfo is None or resolved.utcoffset() is None):
        raise SeriesReconciliationError("Resolved coordinate must be aware.")
    return (
        coordinate.generated_date.isoformat(),
        ""
        if coordinate.generated_wall_time is None
        else coordinate.generated_wall_time.isoformat(),
        coordinate.clock_basis_code,
        coordinate.zone_id or "",
        "" if resolved is None else resolved.astimezone(UTC).isoformat(),
    )


def reconcile_materialized_series(
    *,
    scope: RecurrenceEditScopePlan,
    materialized: tuple[MaterializedSeriesInstance, ...],
    regenerated: tuple[CalendarCoordinate, ...],
    authoritative_inventory: bool,
) -> SeriesReconciliation:
    """Keep local/factual exceptions, retain matches, replace clean mismatches.

    The regenerated coordinates must cover the same bounded horizon as the
    complete materialized source inventory; callers may not use a viewport.
    """
    if not scope.update_future_source_template or not authoritative_inventory:
        raise SeriesReconciliationError("A following edit requires a complete source inventory.")
    indexed: dict[UUID, CalendarCoordinate] = {}
    for item in materialized:
        if item.occurrence_ref in indexed:
            raise SeriesReconciliationError("Duplicate materialized Occurrence identity.")
        indexed[item.occurrence_ref] = item.coordinate
    clean = set(scope.target_occurrence_refs)
    protected = set(scope.protected_future_occurrence_refs)
    if (
        clean & protected
        or scope.selected_occurrence_ref not in indexed
        or not clean.issubset(indexed)
        or not protected.issubset(indexed)
    ):
        raise SeriesReconciliationError("Scope and materialized inventory disagree.")
    if scope.scope == "from_next" and scope.selected_occurrence_ref in clean:
        raise SeriesReconciliationError("Recorded selected instance must remain unchanged.")
    existing_by_key: dict[tuple[str, ...], UUID] = {}
    for ref, coordinate in indexed.items():
        key = _key(coordinate)
        if key in existing_by_key:
            raise SeriesReconciliationError("Materialized coordinates are ambiguous.")
        existing_by_key[key] = ref
    proposed: dict[tuple[str, ...], CalendarCoordinate] = {}
    for coordinate in regenerated:
        key = _key(coordinate)
        if key in proposed:
            raise SeriesReconciliationError("New cadence generated a duplicate coordinate.")
        if key in existing_by_key and existing_by_key[key] not in clean:
            raise SeriesReconciliationError("New cadence collides with an unchanged instance.")
        proposed[key] = coordinate
    return SeriesReconciliation(
        retained_occurrence_refs=tuple(
            ref for ref in scope.target_occurrence_refs if _key(indexed[ref]) in proposed
        ),
        superseded_occurrence_refs=tuple(
            ref for ref in scope.target_occurrence_refs if _key(indexed[ref]) not in proposed
        ),
        new_coordinates=tuple(
            value for key, value in sorted(proposed.items()) if key not in existing_by_key
        ),
        protected_occurrence_refs=scope.protected_future_occurrence_refs,
    )
