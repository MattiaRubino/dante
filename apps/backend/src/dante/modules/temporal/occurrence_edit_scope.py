"""Pure M1-A selection contract for editing one recurring instance or its future.

This module does not discover Occurrences, authorize them or write persistence.
Callers MUST supply a complete, self-scoped, canonical source snapshot and the
server acceptance time. An apply path must independently recheck its revision
and identity set under a transaction; a preview is never a write entitlement.

Routine != Recurrence != Occurrence != Schedule.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

EditScope = Literal["only_this", "this_and_following"]
MAX_EDIT_SCOPE_CANDIDATES = 10_000


class EditScopeInputError(ValueError):
    """A candidate set is invalid, incomplete or temporally ambiguous."""


@dataclass(frozen=True, slots=True)
class RecurrenceEditCandidate:
    """One self-owned canonical Occurrence, not a Schedule or Activity identity.

    expected_at is the resolved governing Occurrence coordinate (absolute UTC
    after caller-side canonical resolution), NOT a browser local date or a
    movable Schedule time. An explicit-extra Occurrence with no coordinate
    cannot be used as an anchor for following-scope edits.
    """

    occurrence_ref: UUID
    source_native_ref: UUID
    expected_at: datetime | None
    origin_code: Literal["recurrence_generated", "explicit_extra"]
    skipped: bool = False
    has_override: bool = False
    has_recorded_facts: bool = False


@dataclass(frozen=True, slots=True)
class RecurrenceEditScopePlan:
    selected_occurrence_ref: UUID
    source_native_ref: UUID
    scope: EditScope
    captured_at: datetime
    target_occurrence_refs: tuple[UUID, ...]
    blocked_future_occurrence_refs: tuple[UUID, ...]
    untouched_past_occurrence_refs: tuple[UUID, ...]
    update_future_source_template: bool

    @property
    def can_apply(self) -> bool:
        """A complete local preview is free of known override conflicts.

        This is NOT authority to persist; source/Occurrence CAS must be
        revalidated by the eventual database mutation.
        """
        return not self.blocked_future_occurrence_refs


def _instant(value: datetime | None, *, field: str) -> datetime:
    if value is None or value.tzinfo is None or value.utcoffset() is None:
        raise EditScopeInputError(f"{field} requires a resolved aware instant.")
    return value.astimezone(UTC)


def select_recurrence_edit_scope(
    *,
    selected_occurrence_ref: UUID,
    scope: EditScope,
    candidates: tuple[RecurrenceEditCandidate, ...],
    captured_at: datetime,
    authoritative_inventory: bool,
) -> RecurrenceEditScopePlan:
    """Select the clicked item plus *only* later future Occurrences if requested.

    The provided inventory must include the selected item. For following-scope
    it must be a complete bounded authoritative inventory of already
    materialized Occurrences relevant to the preview; any not-yet-materialized
    future Occurrences are governed separately by the accepted source-template
    revision. Incomplete inventories are rejected, never partially applied.

    The selected instance is ALWAYS included, even if skipped, past or
    individually overridden. Every other already-past instance is untouched.
    An overridden or already-realized future instance produces a BLOCKED
    entry rather than being silently overwritten or dropped.
    """
    if scope not in {"only_this", "this_and_following"}:
        raise EditScopeInputError("Unsupported edit scope.")
    now = _instant(captured_at, field="captured_at")
    if not candidates or len(candidates) > MAX_EDIT_SCOPE_CANDIDATES:
        raise EditScopeInputError("Edit scope candidate count is outside 1-10000.")
    if scope == "this_and_following" and not authoritative_inventory:
        raise EditScopeInputError("Following scope requires an authoritative inventory.")

    indexed: dict[UUID, RecurrenceEditCandidate] = {}
    for item in candidates:
        if item.occurrence_ref in indexed:
            raise EditScopeInputError("Duplicate Occurrence identity in edit scope.")
        indexed[item.occurrence_ref] = item
    selected = indexed.get(selected_occurrence_ref)
    if selected is None:
        raise EditScopeInputError("Selected Occurrence is missing from the snapshot.")
    if any(item.source_native_ref != selected.source_native_ref for item in candidates):
        raise EditScopeInputError("Edit scope cannot contain unrelated sources.")

    if scope == "only_this":
        return RecurrenceEditScopePlan(
            selected_occurrence_ref=selected_occurrence_ref,
            source_native_ref=selected.source_native_ref,
            scope=scope,
            captured_at=now,
            target_occurrence_refs=(selected_occurrence_ref,),
            blocked_future_occurrence_refs=(),
            untouched_past_occurrence_refs=(),
            update_future_source_template=False,
        )

    if selected.origin_code != "recurrence_generated":
        raise EditScopeInputError("Following edit requires a recurrence-generated anchor.")
    anchor = _instant(selected.expected_at, field="selected.expected_at")
    later: list[tuple[datetime, UUID]] = []
    blocked: list[tuple[datetime, UUID]] = []
    past: list[tuple[datetime, UUID]] = []
    for item in candidates:
        if item.occurrence_ref == selected_occurrence_ref:
            continue
        if item.origin_code != "recurrence_generated":
            continue  # An explicit extra is not generated by the recurring source.
        instant = _instant(item.expected_at, field="candidate.expected_at")
        if instant <= now:
            past.append((instant, item.occurrence_ref))
        elif instant > anchor:
            if item.skipped or item.has_override or item.has_recorded_facts:
                blocked.append((instant, item.occurrence_ref))
            else:
                later.append((instant, item.occurrence_ref))
    # Repeated equal coordinates have no canonical temporal successor relation.
    # Reject instead of manufacturing one using a UUID tie-breaker.
    if any(
        item.occurrence_ref != selected_occurrence_ref
        and item.origin_code == "recurrence_generated"
        and _instant(item.expected_at, field="candidate.expected_at") == anchor
        for item in candidates
    ):
        raise EditScopeInputError("Equal-time Occurrences need an explicit recurrence order.")

    def refs(items: list[tuple[datetime, UUID]]) -> tuple[UUID, ...]:
        return tuple(ref for _, ref in sorted(items))

    return RecurrenceEditScopePlan(
        selected_occurrence_ref=selected_occurrence_ref,
        source_native_ref=selected.source_native_ref,
        scope=scope,
        captured_at=now,
        target_occurrence_refs=(selected_occurrence_ref, *refs(later)),
        blocked_future_occurrence_refs=refs(blocked),
        untouched_past_occurrence_refs=refs(past),
        update_future_source_template=True,
    )
