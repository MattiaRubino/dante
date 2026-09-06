"""Canonical wall-clock and IANA timezone primitives for DANTE application code."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from datetime import time as datetime_time
from enum import StrEnum
from typing import Literal, Protocol
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

LocalTimeKind = Literal["unique", "ambiguous", "nonexistent"]
LocalTimeDisambiguation = Literal["compatible", "earlier", "later", "reject"]


class InvalidTimeZoneError(ValueError):
    """Raised when a timezone identifier is not a valid IANA zone available to the runtime."""


class InvalidInstantError(ValueError):
    """Raised when an application instant is naive instead of timezone-aware."""


class InvalidLocalTimeError(ValueError):
    """Raised when a local wall-clock value unexpectedly carries timezone information."""


class AmbiguousLocalTimeError(ValueError):
    """Raised when an overlap maps one local wall-clock value to two instants."""


class NonexistentLocalTimeError(ValueError):
    """Raised when a DST/calendar gap contains no such local wall-clock value."""


class NonexistentLocalDateError(ValueError):
    """Raised when a named zone contains no positive-duration representation of a date."""


class MissingDeviceTimeZoneError(ValueError):
    """Raised when follow-device policy has no client/device timezone to follow."""


class TimeZoneMode(StrEnum):
    """User-level timezone selection policy; persistence is decided by the user-context layer."""

    FOLLOW_DEVICE = "follow_device"
    FIXED = "fixed"


class Clock(Protocol):
    """Application wall-clock authority. Returned instants are always aware UTC datetimes."""

    def now(self) -> datetime:
        """Return the current application instant in UTC."""
        ...


@dataclass(frozen=True, slots=True)
class SystemClock:
    """Production clock backed by the operating system wall clock."""

    def now(self) -> datetime:
        """Return the current application instant in UTC."""
        return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class FixedClock:
    """Deterministic test clock fixed to one application instant."""

    instant: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "instant", normalize_utc_instant(self.instant))

    def now(self) -> datetime:
        """Return the configured instant in UTC."""
        return self.instant


@dataclass(frozen=True, slots=True)
class LocalTimeClassification:
    """Classification of a naive local wall-clock value in one named IANA timezone."""

    local: datetime
    zone_id: str
    kind: LocalTimeKind
    candidate_instants: tuple[datetime, ...]


@dataclass(frozen=True, slots=True)
class TimeZonePolicy:
    """Resolve a user-level effective timezone without owning where the preference is stored."""

    mode: TimeZoneMode
    fixed_zone_id: str | None = None

    def __post_init__(self) -> None:
        if self.mode is TimeZoneMode.FIXED:
            if self.fixed_zone_id is None:
                raise InvalidTimeZoneError("fixed timezone policy requires fixed_zone_id")
            validate_iana_timezone(self.fixed_zone_id)
            return

        if self.fixed_zone_id is not None:
            raise InvalidTimeZoneError("follow-device timezone policy cannot carry fixed_zone_id")

    def resolve(self, *, device_zone_id: str | None) -> str:
        """Resolve the effective zone for this request/device context."""
        if self.mode is TimeZoneMode.FIXED:
            if self.fixed_zone_id is None:  # pragma: no cover - guarded by __post_init__
                raise InvalidTimeZoneError("fixed timezone policy requires fixed_zone_id")
            return self.fixed_zone_id

        if device_zone_id is None:
            raise MissingDeviceTimeZoneError(
                "follow-device timezone policy requires device_zone_id"
            )
        validate_iana_timezone(device_zone_id)
        return device_zone_id


def normalize_utc_instant(value: datetime) -> datetime:
    """Require an aware datetime and normalize the same instant to UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise InvalidInstantError("application instants must be timezone-aware")
    return value.astimezone(UTC)


def validate_iana_timezone(zone_id: str) -> ZoneInfo:
    """Validate one runtime-available IANA timezone identifier and return its ZoneInfo."""
    if not zone_id or zone_id != zone_id.strip():
        raise InvalidTimeZoneError("timezone must be a non-empty unpadded IANA identifier")
    try:
        return ZoneInfo(zone_id)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise InvalidTimeZoneError(f"unknown IANA timezone: {zone_id}") from exc


def classify_local_time(local: datetime, zone_id: str) -> LocalTimeClassification:
    """Classify a naive local time as unique, ambiguous (overlap), or nonexistent (gap)."""
    _require_naive_local(local)
    zone = validate_iana_timezone(zone_id)

    valid_instants: set[datetime] = set()
    for fold in (0, 1):
        instant, round_trip_local = _fold_projection(local, zone, fold)
        if round_trip_local == local:
            valid_instants.add(instant)

    ordered_instants = tuple(sorted(valid_instants))
    if len(ordered_instants) == 1:
        kind: LocalTimeKind = "unique"
    elif len(ordered_instants) == 2:
        kind = "ambiguous"
    else:
        kind = "nonexistent"

    return LocalTimeClassification(
        local=local,
        zone_id=zone_id,
        kind=kind,
        candidate_instants=ordered_instants,
    )


def resolve_local_time(
    local: datetime,
    zone_id: str,
    *,
    disambiguation: LocalTimeDisambiguation = "reject",
) -> datetime:
    """Resolve local wall time to UTC with explicit Temporal-compatible DST disambiguation.

    ``compatible`` chooses the earlier instant during overlaps and the later projection during
    gaps. ``earlier``/``later`` select the corresponding instant. ``reject`` refuses both
    ambiguous and nonexistent local times.
    """
    classification = classify_local_time(local, zone_id)

    if classification.kind == "unique":
        return classification.candidate_instants[0]

    if classification.kind == "ambiguous":
        if disambiguation == "reject":
            raise AmbiguousLocalTimeError(f"ambiguous local time {local!s} in {zone_id}")
        if disambiguation in {"earlier", "compatible"}:
            return classification.candidate_instants[0]
        return classification.candidate_instants[-1]

    if disambiguation == "reject":
        raise NonexistentLocalTimeError(f"nonexistent local time {local!s} in {zone_id}")

    zone = validate_iana_timezone(zone_id)
    projected_instants = tuple(sorted({_fold_projection(local, zone, fold)[0] for fold in (0, 1)}))
    if len(projected_instants) != 2:
        raise NonexistentLocalTimeError(
            f"could not disambiguate nonexistent local time {local!s} in {zone_id}"
        )
    if disambiguation == "earlier":
        return projected_instants[0]
    return projected_instants[-1]


def local_day_utc_bounds(day: date, zone_id: str) -> tuple[datetime, datetime]:
    """Return the half-open UTC interval covering one local calendar date in a named zone.

    This correctly produces 23-hour and 25-hour intervals across DST transitions. Midnight
    transitions use ``compatible`` semantics: earliest instant for overlaps, first valid instant
    after gaps.
    """
    validate_iana_timezone(zone_id)
    local_start = datetime.combine(day, datetime_time.min)
    local_end = datetime.combine(day + timedelta(days=1), datetime_time.min)
    start = resolve_local_time(local_start, zone_id, disambiguation="compatible")
    end = resolve_local_time(local_end, zone_id, disambiguation="compatible")
    if end <= start:
        raise NonexistentLocalDateError(f"local date {day.isoformat()} does not exist in {zone_id}")
    return start, end


def _require_naive_local(value: datetime) -> None:
    if value.tzinfo is not None and value.utcoffset() is not None:
        raise InvalidLocalTimeError("local wall-clock values must be timezone-naive")


def _fold_projection(local: datetime, zone: ZoneInfo, fold: int) -> tuple[datetime, datetime]:
    aware_local = local.replace(tzinfo=zone, fold=fold)
    instant = aware_local.astimezone(UTC)
    round_trip_local = instant.astimezone(zone).replace(tzinfo=None)
    return instant, round_trip_local
