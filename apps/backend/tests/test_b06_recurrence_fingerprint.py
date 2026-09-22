"""B06-B canonical Recurrence idempotency fingerprints."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from dante.modules.temporal.recurrence import ElapsedRecurrence, _fingerprint


def test_elapsed_recurrence_fingerprint_is_decimal_safe_and_value_canonical() -> None:
    recurrence = ElapsedRecurrence(
        family_code="elapsed_interval",
        range_kind="expected_count",
        expected_occurrence_count=4,
        effective_from=datetime(2026, 11, 5, 10, tzinfo=timezone.utc),
        effective_until=None,
        elapsed_seconds=Decimal("900.000000"),
        anchor_mode_code="fixed_anchor",
        anchor_at=datetime(2026, 11, 5, 10, tzinfo=timezone.utc),
    )
    owner_ref = UUID("018f5c36-7f00-7000-8000-000000000001")

    fingerprint = _fingerprint(
        owner="routine",
        owner_ref=owner_ref,
        expected_state_ref=None,
        recurrence=recurrence,
    )
    equivalent_fingerprint = _fingerprint(
        owner="routine",
        owner_ref=owner_ref,
        expected_state_ref=None,
        recurrence=replace(recurrence, elapsed_seconds=Decimal("900")),
    )

    assert len(fingerprint) == 64
    assert fingerprint == equivalent_fingerprint
