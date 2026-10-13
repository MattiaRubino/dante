"""B06-B canonical Recurrence idempotency fingerprints."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from dante.modules.temporal.recurrence import (
    ElapsedRecurrence,
    QuotaRecurrence,
    RecurrenceInputError,
    _fingerprint,
    _validate,
)


def test_elapsed_recurrence_fingerprint_is_decimal_safe_and_value_canonical() -> None:
    recurrence = ElapsedRecurrence(
        family_code="elapsed_interval",
        range_kind="expected_count",
        expected_occurrence_count=4,
        effective_from=datetime(2026, 11, 5, 10, tzinfo=UTC),
        effective_until=None,
        elapsed_seconds=Decimal("900.000000"),
        anchor_mode_code="fixed_anchor",
        anchor_at=datetime(2026, 11, 5, 10, tzinfo=UTC),
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


@pytest.mark.parametrize(
    "interval", [Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("0.0000001")]
)
def test_elapsed_recurrence_rejects_nonpositive_nonfinite_and_overprecise_intervals(
    interval: Decimal,
) -> None:
    recurrence = ElapsedRecurrence(
        family_code="elapsed_interval",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=datetime(2026, 11, 5, 10, tzinfo=UTC),
        effective_until=None,
        elapsed_seconds=interval,
        anchor_mode_code="fixed_anchor",
        anchor_at=datetime(2026, 11, 5, 10, tzinfo=UTC),
    )
    with pytest.raises(RecurrenceInputError, match="Elapsed interval must be positive"):
        _validate(recurrence)


def test_elapsed_interval_validation_does_not_apply_to_quota_recurrence() -> None:
    recurrence = QuotaRecurrence(
        family_code="quota_per_period",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 11, 5),
        effective_until=None,
        quota_count=2,
        period_unit_code="day",
        period_span=1,
        frame_code="floating_local",
        zone_id=None,
        week_start=None,
        pattern_anchor_date=None,
    )
    _validate(recurrence)


def test_elapsed_recurrence_accepts_six_decimal_places_and_requires_absolute_instants() -> None:
    recurrence = ElapsedRecurrence(
        family_code="elapsed_interval",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=datetime(2026, 11, 5, 10, tzinfo=UTC),
        effective_until=None,
        elapsed_seconds=Decimal("0.000001"),
        anchor_mode_code="fixed_anchor",
        anchor_at=datetime(2026, 11, 5, 10, tzinfo=UTC),
    )
    _validate(recurrence)
    with pytest.raises(RecurrenceInputError, match="absolute instants"):
        _validate(replace(recurrence, anchor_at=recurrence.anchor_at.replace(tzinfo=None)))
