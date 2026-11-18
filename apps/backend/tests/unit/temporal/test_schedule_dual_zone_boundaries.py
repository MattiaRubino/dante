"""Regression contract for one-off Schedules with two IANA end boundaries."""

from datetime import UTC, datetime, timedelta

import pytest

from dante.modules.temporal.api import NamedZoneLocalIntervalPlacementRequest
from dante.modules.temporal.schedule import (
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    _placement_from_payload,
    _placement_payload,
)


def _local(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, 18, hour, minute)  # noqa: DTZ001


def test_dual_zone_allows_end_clock_earlier_than_start_clock() -> None:
    placement = NamedZoneLocalIntervalPlacement(
        starts_local_at=_local(10),
        ends_local_at=_local(8),
        zone_id="Europe/Rome",
        end_zone_id="America/New_York",
    )
    assert placement.resolved_start_at == datetime(2026, 11, 18, 9, tzinfo=UTC)
    assert placement.resolved_end_at == datetime(2026, 11, 18, 13, tzinfo=UTC)
    assert placement.resolved_end_at - placement.resolved_start_at == timedelta(hours=4)
    payload = _placement_payload(placement)
    assert payload["end_zone_id"] == "America/New_York"
    assert _placement_from_payload(payload) == placement


def test_single_zone_ordering_and_legacy_payload_remain_unchanged() -> None:
    with pytest.raises(ScheduleInputError, match="after"):
        NamedZoneLocalIntervalPlacement(
            starts_local_at=_local(10),
            ends_local_at=_local(8),
            zone_id="Europe/Rome",
        )
    placement = NamedZoneLocalIntervalPlacement(
        starts_local_at=_local(10),
        ends_local_at=_local(11),
        zone_id="Europe/Rome",
    )
    payload = _placement_payload(placement)
    assert "end_zone_id" not in payload
    assert _placement_from_payload(payload).end_zone_id is None


@pytest.mark.parametrize(
    ("end_hour", "end_minute"),
    [(3, 0), (3, 30)],
)
def test_dual_zone_rejects_real_end_before_start(
    end_hour: int,
    end_minute: int,
) -> None:
    with pytest.raises(ScheduleInputError, match="resolved"):
        NamedZoneLocalIntervalPlacement(
            starts_local_at=_local(10),
            ends_local_at=_local(end_hour, end_minute),
            zone_id="Europe/Rome",
            end_zone_id="America/New_York",
        )


def test_dual_zone_rejects_invalid_or_redundant_end_zone() -> None:
    for zone in ("Mars/Phobos", "Europe/Rome"):
        with pytest.raises(ScheduleInputError):
            NamedZoneLocalIntervalPlacement(
                starts_local_at=_local(10),
                ends_local_at=_local(11),
                zone_id="Europe/Rome",
                end_zone_id=zone,
            )


def test_dual_zone_rejects_nonexistent_local_wall_time() -> None:
    with pytest.raises(ScheduleInputError):
        NamedZoneLocalIntervalPlacement(
            starts_local_at=datetime(2026, 3, 29, 2, 30),  # noqa: DTZ001
            ends_local_at=datetime(2026, 3, 29, 8, 0),  # noqa: DTZ001
            zone_id="Europe/Rome",
            end_zone_id="America/New_York",
        )


def test_api_accepts_distinct_boundary_zone_without_requiring_it_for_legacy() -> None:
    request = NamedZoneLocalIntervalPlacementRequest.model_validate({
        "kind": "named_zone_local_interval",
        "starts_local_at": "2026-11-18T10:00:00",
        "ends_local_at": "2026-11-18T08:00:00",
        "zone_id": "Europe/Rome",
        "end_zone_id": "America/New_York",
    })
    assert request.end_zone_id == "America/New_York"
    older = NamedZoneLocalIntervalPlacementRequest.model_validate({
        "kind": "named_zone_local_interval",
        "starts_local_at": "2026-11-18T10:00:00",
        "ends_local_at": "2026-11-18T11:00:00",
        "zone_id": "Europe/Rome",
    })
    assert older.end_zone_id is None
