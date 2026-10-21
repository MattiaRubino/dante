"""Reconcile calendar Occurrence identities under an authoritative series preview.

This is a pure plan. The caller must validate the inventory under the source
lock and persist every transition together with the revised source policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date
from uuid import UUID

from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    _calendar_candidates,
    _candidate_instant,
    _zone,
)
from dante.modules.temporal.occurrence_edit_scope import RecurrenceEditScopePlan
from dante.modules.temporal.recurrence import CalendarRecurrence, _validate


class SeriesReconciliationError(ValueError):
    """A proposed cadence or materialized inventory is ambiguous."""


MAX_SERIES_INVENTORY = 10_000
MAX_SERIES_SCAN_DAYS = 366_000


@dataclass(frozen=True, slots=True)
class SeriesReconciliationWindow:
    """Complete materialized horizon, not a browser viewport.

    Enumerate both the source and proposed coordinates for the exact window.
    A subsequent write must recheck it under the authoritative source lock.
    """

    start_date: date
    end_date_exclusive: date

    def __post_init__(self) -> None:
        days = (self.end_date_exclusive - self.start_date).days
        if not 1 <= days <= MAX_SERIES_SCAN_DAYS:
            raise SeriesReconciliationError("Invalid bounded reconciliation horizon.")

    def contains(self, coordinate: CalendarCoordinate) -> bool:
        return self.start_date <= coordinate.generated_date < self.end_date_exclusive


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
    window: SeriesReconciliationWindow,
    authoritative_inventory: bool,
) -> SeriesReconciliation:
    """Keep local/factual exceptions, retain matches, replace clean mismatches.

    The regenerated coordinates must cover the same bounded horizon as the
    complete materialized source inventory; callers may not use a viewport.
    """
    if not scope.update_future_source_template or not authoritative_inventory:
        raise SeriesReconciliationError("A following edit requires a complete source inventory.")
    if len(materialized) > MAX_SERIES_INVENTORY or len(regenerated) > MAX_SERIES_INVENTORY:
        raise SeriesReconciliationError("Reconciliation exceeds the bounded instance limit.")
    if any(not window.contains(item.coordinate) for item in materialized):
        raise SeriesReconciliationError("Source inventory escapes its declared horizon.")
    if any(not window.contains(item) for item in regenerated):
        raise SeriesReconciliationError("Regenerated cadence escapes its declared horizon.")
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


def preview_calendar_series_reconciliation(
    *,
    scope: RecurrenceEditScopePlan,
    materialized: tuple[MaterializedSeriesInstance, ...],
    proposed_recurrence: CalendarRecurrence,
    window: SeriesReconciliationWindow,
    effective_zone_id: str,
    authoritative_inventory: bool,
) -> SeriesReconciliation:
    """Generate a bounded calendar change preview without writing canonical truth.

    This never grants persistence authority. The eventual acceptance must lock
    its source, re-read the inventory and revision, then atomically reconcile
    the same coordinates with the new versioned source policy.
    """
    if scope.scope not in {"this_and_following", "from_next"}:
        raise SeriesReconciliationError("Calendar source changes require a following scope.")
    if not authoritative_inventory or not scope.update_future_source_template:
        raise SeriesReconciliationError("A following edit requires a complete source inventory.")
    if len(materialized) > MAX_SERIES_INVENTORY:
        raise SeriesReconciliationError("Reconciliation exceeds the bounded instance limit.")
    if any(not window.contains(item.coordinate) for item in materialized):
        raise SeriesReconciliationError("Source inventory escapes its declared horizon.")
    selected = next(
        (
            item.coordinate
            for item in materialized
            if item.occurrence_ref == scope.selected_occurrence_ref
        ),
        None,
    )
    if selected is None:
        raise SeriesReconciliationError("Selected Occurrence is absent from source inventory.")

    _validate(proposed_recurrence)
    zone = _zone(effective_zone_id)
    anchor = _candidate_instant(selected, zone).astimezone(UTC)
    accepted = scope.captured_at.astimezone(UTC)
    if scope.scope == "this_and_following" and anchor < accepted:
        raise SeriesReconciliationError("Structural series edits cannot rewrite a past anchor.")
    cutover = max(anchor, accepted)

    # The canonical generator enforces named-zone DST ambiguity/gap semantics
    # and expected-count limits; never approximate calendar rules in the UI.
    candidates = _calendar_candidates(
        scope.source_native_ref,
        proposed_recurrence,
        window.start_date,
        window.end_date_exclusive,
        zone,
    )

    def is_in_scope(coordinate: CalendarCoordinate) -> bool:
        expected_at = _candidate_instant(coordinate, zone).astimezone(UTC)
        return expected_at > cutover if scope.scope == "from_next" else expected_at >= cutover

    regenerated = tuple(
        candidate.coordinate
        for candidate in candidates
        if isinstance(candidate.coordinate, CalendarCoordinate)
        and is_in_scope(candidate.coordinate)
    )
    return reconcile_materialized_series(
        scope=scope,
        materialized=materialized,
        regenerated=regenerated,
        window=window,
        authoritative_inventory=authoritative_inventory,
    )
