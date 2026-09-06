"""Unit proof for canonical DANTE Clock and IANA timezone behavior."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import pytest

from dante.platform.time import (
    AmbiguousLocalTimeError,
    FixedClock,
    InvalidInstantError,
    InvalidTimeZoneError,
    MissingDeviceTimeZoneError,
    NonexistentLocalTimeError,
    SystemClock,
    TimeZoneMode,
    TimeZonePolicy,
    classify_local_time,
    local_day_utc_bounds,
    normalize_utc_instant,
    resolve_local_time,
    validate_iana_timezone,
)


def _local(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    assert parsed.tzinfo is None
    return parsed


def _instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    return parsed


def test_system_clock_returns_aware_utc_instant() -> None:
    now = SystemClock().now()
    assert now.tzinfo is UTC
    assert now.utcoffset() == timedelta(0)


def test_fixed_clock_normalizes_offset_aware_instant_to_utc() -> None:
    clock = FixedClock(_instant("2026-09-06T15:30:00+02:00"))
    assert clock.now() == _instant("2026-09-06T13:30:00Z")
    assert clock.now().tzinfo is UTC


def test_naive_application_instant_is_rejected() -> None:
    with pytest.raises(InvalidInstantError):
        normalize_utc_instant(_local("2026-09-06T13:30:00"))


def test_iana_timezone_validation_accepts_real_zones_and_rejects_invalid_values() -> None:
    assert validate_iana_timezone("Europe/Rome").key == "Europe/Rome"
    assert validate_iana_timezone("America/New_York").key == "America/New_York"

    for invalid in ("", " Europe/Rome", "Etc/Definitely_Not_A_Zone"):
        with pytest.raises(InvalidTimeZoneError):
            validate_iana_timezone(invalid)


def test_rome_dst_gap_and_overlap_are_classified_explicitly() -> None:
    gap = classify_local_time(_local("2026-03-29T02:30:00"), "Europe/Rome")
    overlap = classify_local_time(_local("2026-10-25T02:30:00"), "Europe/Rome")

    assert gap.kind == "nonexistent"
    assert gap.candidate_instants == ()
    assert overlap.kind == "ambiguous"
    assert overlap.candidate_instants == (
        _instant("2026-10-25T00:30:00Z"),
        _instant("2026-10-25T01:30:00Z"),
    )


def test_new_york_dst_gap_and_overlap_are_classified_explicitly() -> None:
    gap = classify_local_time(_local("2026-03-08T02:30:00"), "America/New_York")
    overlap = classify_local_time(_local("2026-11-01T01:30:00"), "America/New_York")

    assert gap.kind == "nonexistent"
    assert overlap.kind == "ambiguous"
    assert overlap.candidate_instants == (
        _instant("2026-11-01T05:30:00Z"),
        _instant("2026-11-01T06:30:00Z"),
    )


def test_overlap_resolution_requires_or_applies_explicit_policy() -> None:
    local = _local("2026-10-25T02:30:00")

    with pytest.raises(AmbiguousLocalTimeError):
        resolve_local_time(local, "Europe/Rome")

    assert resolve_local_time(local, "Europe/Rome", disambiguation="earlier") == _instant(
        "2026-10-25T00:30:00Z"
    )
    assert resolve_local_time(local, "Europe/Rome", disambiguation="later") == _instant(
        "2026-10-25T01:30:00Z"
    )
    assert resolve_local_time(local, "Europe/Rome", disambiguation="compatible") == _instant(
        "2026-10-25T00:30:00Z"
    )


def test_gap_resolution_matches_temporal_compatible_semantics() -> None:
    local = _local("2026-03-29T02:30:00")

    with pytest.raises(NonexistentLocalTimeError):
        resolve_local_time(local, "Europe/Rome")

    assert resolve_local_time(local, "Europe/Rome", disambiguation="earlier") == _instant(
        "2026-03-29T00:30:00Z"
    )
    assert resolve_local_time(local, "Europe/Rome", disambiguation="later") == _instant(
        "2026-03-29T01:30:00Z"
    )
    assert resolve_local_time(local, "Europe/Rome", disambiguation="compatible") == _instant(
        "2026-03-29T01:30:00Z"
    )


def test_local_day_bounds_preserve_real_23_and_25_hour_days() -> None:
    rome_spring = local_day_utc_bounds(date(2026, 3, 29), "Europe/Rome")
    rome_fall = local_day_utc_bounds(date(2026, 10, 25), "Europe/Rome")
    new_york_spring = local_day_utc_bounds(date(2026, 3, 8), "America/New_York")
    new_york_fall = local_day_utc_bounds(date(2026, 11, 1), "America/New_York")

    assert rome_spring[1] - rome_spring[0] == timedelta(hours=23)
    assert rome_fall[1] - rome_fall[0] == timedelta(hours=25)
    assert new_york_spring[1] - new_york_spring[0] == timedelta(hours=23)
    assert new_york_fall[1] - new_york_fall[0] == timedelta(hours=25)


def test_timezone_policy_follows_device_by_default_contract() -> None:
    policy = TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE)

    assert policy.resolve(device_zone_id="Europe/Rome") == "Europe/Rome"
    assert policy.resolve(device_zone_id="America/New_York") == "America/New_York"

    with pytest.raises(MissingDeviceTimeZoneError):
        policy.resolve(device_zone_id=None)


def test_timezone_policy_can_be_fixed_independently_of_device_location() -> None:
    policy = TimeZonePolicy(mode=TimeZoneMode.FIXED, fixed_zone_id="Europe/Rome")

    assert policy.resolve(device_zone_id="America/New_York") == "Europe/Rome"

    with pytest.raises(InvalidTimeZoneError):
        TimeZonePolicy(mode=TimeZoneMode.FIXED)
