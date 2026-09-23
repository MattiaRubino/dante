# ruff: noqa: S608
"""B06-C canonical Occurrence evaluation and command boundary.

The browser submits a bounded checkpoint intent.  This module evaluates the
immutable Recurrence history while the database transaction holds the source
current/generation namespaces, then asks typed database capabilities to reuse
or materialize canonical Occurrence identities.  It never creates an Activity,
Event instance or Schedule.
"""

from __future__ import annotations

import calendar
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import ROUND_CEILING, Decimal
from typing import Literal
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    CyclicRecurrence,
    ElapsedRecurrence,
    QuotaRecurrence,
    RecurrenceSpec,
)
from dante.modules.temporal.recurrence import (
    _view as recurrence_view_from_row,
)
from dante.platform.database.references import NativeRef

OccurrenceOwner = Literal["routine", "event"]
MAX_CHECKPOINT_DAYS = 62
MAX_CHECKPOINT_OCCURRENCES = 10_000
_MAX_CALENDAR_SCAN_DAYS = 366_000


class OccurrenceInputError(ValueError):
    """The checkpoint or one-instance intent is invalid."""


class OccurrenceOperationReuseError(RuntimeError):
    """An actor-local operation id already represents another intent."""


class OccurrenceSourceNotFoundError(RuntimeError):
    """The source/Occurrence is outside the authenticated self scope."""


class OccurrenceSourceInactiveError(RuntimeError):
    """A paused or ended Routine cannot create future Occurrences."""


class OccurrenceAlreadySkippedError(RuntimeError):
    """The immutable skip disposition already exists."""


class OccurrenceMaterializedConflictError(RuntimeError):
    """A structural exclusion targeted an already materialized Occurrence."""


class OccurrenceCheckpointLimitError(RuntimeError):
    """One bounded checkpoint would still materialize too many identities."""


class OccurrencePersistenceError(RuntimeError):
    """The governed Occurrence persistence boundary did not complete."""


@dataclass(frozen=True, slots=True)
class CalendarCoordinate:
    family_code: Literal["calendar_wall_clock"]
    generated_date: date
    generated_wall_time: time | None
    clock_basis_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None
    resolved_at: datetime | None


@dataclass(frozen=True, slots=True)
class ElapsedCoordinate:
    family_code: Literal["elapsed_interval"]
    expected_at: datetime


@dataclass(frozen=True, slots=True)
class QuotaCoordinate:
    family_code: Literal["quota_per_period"]
    period_start_date: date
    period_end_date_exclusive: date
    frame_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None


@dataclass(frozen=True, slots=True)
class CyclicCoordinate:
    family_code: Literal["cyclic_positional"]
    generated_date: date
    position_index: int


type OccurrenceCoordinate = (
    CalendarCoordinate | ElapsedCoordinate | QuotaCoordinate | CyclicCoordinate
)


@dataclass(frozen=True, slots=True)
class OccurrenceCandidate:
    governing_recurrence_state_ref: UUID
    coordinate: OccurrenceCoordinate


@dataclass(frozen=True, slots=True)
class RecurrenceHistoryEntry:
    material_state_ref: UUID
    current_from_at: datetime
    current_until_at: datetime | None
    recurrence: RecurrenceSpec


@dataclass(frozen=True, slots=True)
class OccurrenceView:
    occurrence_ref: UUID
    source_native_ref: UUID
    governing_recurrence_state_ref: UUID | None
    origin_code: Literal["recurrence_generated", "explicit_extra"]
    coordinate: OccurrenceCoordinate | None
    skipped: bool
    skip_reason: str | None
    skipped_at: datetime | None


@dataclass(frozen=True, slots=True)
class OccurrenceCheckpoint:
    source_native_ref: UUID
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    occurrences: tuple[OccurrenceView, ...]
    accepted_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class OccurrenceWindowCheckpoint:
    start_date: date
    end_date_exclusive: date
    effective_zone_id: str
    source_count: int
    occurrence_count: int
    replayed_source_count: int


@dataclass(frozen=True, slots=True)
class OccurrenceMutation:
    occurrence: OccurrenceView
    accepted_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class OccurrenceExclusion:
    exclusion_ref: UUID
    source_native_ref: UUID
    governing_recurrence_state_ref: UUID
    coordinate: CalendarCoordinate | ElapsedCoordinate | CyclicCoordinate
    accepted_at: datetime
    replayed: bool


def _bounded_operation_id(value: str) -> str:
    result = value.strip()
    if not result or len(result) > 200:
        raise OccurrenceInputError("Occurrence operation id must contain 1 to 200 characters.")
    return result


def _window_source_operation_id(
    *,
    root_operation_id: str,
    owner: OccurrenceOwner,
    source_ref: UUID,
    start_date: date,
    end_date_exclusive: date,
    effective_zone_id: str,
) -> str:
    digest = hashlib.sha256(
        json.dumps(
            {
                "version": 1,
                "root_operation_id": root_operation_id,
                "owner": owner,
                "source_ref": str(source_ref),
                "start_date": start_date.isoformat(),
                "end_date_exclusive": end_date_exclusive.isoformat(),
                "effective_zone_id": effective_zone_id,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return f"timeline-window:{digest}"


def _fingerprint(payload: dict[str, object]) -> str:
    canonical = json.dumps(
        {"version": 1, **payload},
        default=lambda value: (
            value.isoformat() if isinstance(value, date | datetime | time) else str(value)
        ),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(canonical).hexdigest()


def _zone(value: str) -> ZoneInfo:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise OccurrenceInputError("Effective timezone must be a bounded IANA zone id.")
    try:
        return ZoneInfo(normalized)
    except ZoneInfoNotFoundError as exc:
        raise OccurrenceInputError("Effective timezone must be a valid IANA zone id.") from exc


def _normalize_exclusion_coordinate(
    coordinate: CalendarCoordinate | ElapsedCoordinate | CyclicCoordinate,
) -> CalendarCoordinate | ElapsedCoordinate | CyclicCoordinate:
    """Validate a structural coordinate before it crosses the SQL boundary."""
    if isinstance(coordinate, ElapsedCoordinate):
        if coordinate.expected_at.tzinfo is None or coordinate.expected_at.utcoffset() is None:
            raise OccurrenceInputError(
                "Elapsed exclusion coordinate requires an absolute instant with timezone offset."
            )
        return coordinate
    if isinstance(coordinate, CyclicCoordinate):
        if coordinate.position_index < 0:
            raise OccurrenceInputError(
                "Cyclic exclusion coordinate position must be zero or greater."
            )
        return coordinate

    if coordinate.generated_wall_time is not None and coordinate.generated_wall_time.tzinfo:
        raise OccurrenceInputError(
            "Calendar exclusion wall time must be a local time without timezone offset."
        )
    if coordinate.clock_basis_code == "named_zone":
        if coordinate.zone_id is None:
            raise OccurrenceInputError(
                "Named-zone calendar exclusion coordinate requires an IANA zone id."
            )
        zone = _zone(coordinate.zone_id)
        if coordinate.resolved_at is not None:
            if (
                coordinate.generated_wall_time is None
                or coordinate.resolved_at.tzinfo is None
                or coordinate.resolved_at.utcoffset() is None
            ):
                raise OccurrenceInputError(
                    "Resolved named-zone exclusion coordinate requires an absolute instant "
                    "and wall time."
                )
            local = coordinate.resolved_at.astimezone(zone)
            wall = coordinate.generated_wall_time
            if local.date() != coordinate.generated_date or (
                local.hour,
                local.minute,
                local.second,
                local.microsecond,
            ) != (wall.hour, wall.minute, wall.second, wall.microsecond):
                raise OccurrenceInputError(
                    "Resolved named-zone exclusion instant does not match its civil coordinate."
                )
    elif coordinate.zone_id is not None or coordinate.resolved_at is not None:
        raise OccurrenceInputError(
            "Only named-zone calendar exclusion coordinates may carry zone or resolved instant."
        )

    if coordinate.resolved_at is None:
        return coordinate
    # Structural identity is civil; overlap resolution cannot create a second exclusion.
    return CalendarCoordinate(
        family_code=coordinate.family_code,
        generated_date=coordinate.generated_date,
        generated_wall_time=coordinate.generated_wall_time,
        clock_basis_code=coordinate.clock_basis_code,
        zone_id=coordinate.zone_id,
        resolved_at=None,
    )


def _validate_window(start: date, end: date) -> None:
    days = (end - start).days
    if days < 1 or days > MAX_CHECKPOINT_DAYS:
        raise OccurrenceInputError(
            f"Occurrence checkpoint range must contain 1 to {MAX_CHECKPOINT_DAYS} local dates."
        )


def _resolved_named_local(
    local_value: datetime,
    zone: ZoneInfo,
    policy: Literal["earlier", "later"],
) -> datetime | None:
    """Resolve one civil value without accepting ZoneInfo's implicit gap policy."""
    accepted: dict[datetime, datetime] = {}
    for fold in (0, 1):
        aware = local_value.replace(tzinfo=zone, fold=fold)
        instant = aware.astimezone(UTC)
        round_trip = instant.astimezone(zone).replace(tzinfo=None)
        if round_trip == local_value:
            accepted[instant] = instant
    if not accepted:
        return None
    ordered = sorted(accepted)
    return ordered[0] if policy == "earlier" else ordered[-1]


def _month_day_matches(value: date, selector: int) -> bool:
    days = calendar.monthrange(value.year, value.month)[1]
    expected = selector if selector > 0 else days + selector + 1
    return value.day == expected


def _ordinal_weekdays(value: date) -> tuple[int, int]:
    days = calendar.monthrange(value.year, value.month)[1]
    return (value.day - 1) // 7 + 1, -((days - value.day) // 7 + 1)


def _calendar_phase_matches(spec: CalendarRecurrence, value: date) -> bool:
    anchor = spec.pattern_anchor_date
    if spec.pattern_code == "daily":
        return spec.interval_count == 1 or (
            anchor is not None and (value - anchor).days % spec.interval_count == 0
        )
    if spec.pattern_code == "weekly_weekdays":
        if value.isoweekday() not in spec.weekdays:
            return False
        if spec.interval_count == 1:
            return True
        if anchor is None:
            raise OccurrenceInputError("Weekly interval Recurrence is missing its phase anchor.")
        anchor_week = anchor - timedelta(days=anchor.isoweekday() - 1)
        value_week = value - timedelta(days=value.isoweekday() - 1)
        return ((value_week - anchor_week).days // 7) % spec.interval_count == 0
    if spec.pattern_code == "monthly_month_days":
        selector_match = any(_month_day_matches(value, item) for item in spec.month_days)
    elif spec.pattern_code == "monthly_ordinal_weekdays":
        ordinals = set(_ordinal_weekdays(value))
        selector_match = any(
            weekday == value.isoweekday() and ordinal in ordinals
            for weekday, ordinal in spec.ordinal_weekdays
        )
    elif spec.pattern_code == "yearly_month_days":
        selector_match = any(
            month == value.month and _month_day_matches(value, month_day)
            for month, month_day in spec.year_month_days
        )
    else:
        if anchor is None or spec.step_unit_code is None:
            raise OccurrenceInputError("Anchor-step Recurrence is missing its phase contract.")
        if value < anchor:
            return False
        if spec.step_unit_code == "day":
            return (value - anchor).days % spec.interval_count == 0
        if spec.step_unit_code == "week":
            days = (value - anchor).days
            return days % 7 == 0 and (days // 7) % spec.interval_count == 0
        if spec.step_unit_code == "month":
            months = (value.year - anchor.year) * 12 + value.month - anchor.month
            return value.day == anchor.day and months >= 0 and months % spec.interval_count == 0
        years = value.year - anchor.year
        return (
            value.month == anchor.month
            and value.day == anchor.day
            and years >= 0
            and years % spec.interval_count == 0
        )
    if not selector_match:
        return False
    if spec.interval_count == 1:
        return True
    if anchor is None:
        raise OccurrenceInputError("Calendar interval Recurrence is missing its phase anchor.")
    if spec.pattern_code.startswith("monthly"):
        delta = (value.year - anchor.year) * 12 + value.month - anchor.month
    else:
        delta = value.year - anchor.year
    return delta >= 0 and delta % spec.interval_count == 0


def _candidate_local_date(candidate: OccurrenceCoordinate, effective_zone: ZoneInfo) -> date:
    if isinstance(candidate, ElapsedCoordinate):
        return candidate.expected_at.astimezone(effective_zone).date()
    if isinstance(candidate, QuotaCoordinate):
        return candidate.period_start_date
    if isinstance(candidate, CalendarCoordinate):
        if candidate.resolved_at is not None:
            return candidate.resolved_at.astimezone(effective_zone).date()
        if (
            candidate.clock_basis_code == "absolute_utc"
            and candidate.generated_wall_time is not None
        ):
            return (
                datetime.combine(
                    candidate.generated_date,
                    candidate.generated_wall_time,
                    tzinfo=UTC,
                )
                .astimezone(effective_zone)
                .date()
            )
    return candidate.generated_date


def _candidate_instant(candidate: OccurrenceCoordinate, effective_zone: ZoneInfo) -> datetime:
    if isinstance(candidate, ElapsedCoordinate):
        return candidate.expected_at
    if isinstance(candidate, CalendarCoordinate):
        if candidate.resolved_at is not None:
            return candidate.resolved_at
        zone = UTC if candidate.clock_basis_code == "absolute_utc" else effective_zone
        return datetime.combine(
            candidate.generated_date,
            candidate.generated_wall_time or time.min,
            tzinfo=zone,
        ).astimezone(UTC)
    if isinstance(candidate, QuotaCoordinate):
        return datetime.combine(
            candidate.period_start_date, time.min, tzinfo=effective_zone
        ).astimezone(UTC)
    return datetime.combine(candidate.generated_date, time.min, tzinfo=effective_zone).astimezone(
        UTC
    )


def _is_superseded(
    candidate: OccurrenceCoordinate,
    successors: tuple[RecurrenceHistoryEntry, ...],
    effective_zone: ZoneInfo,
) -> bool:
    for successor in successors:
        spec = successor.recurrence
        if isinstance(spec, ElapsedRecurrence):
            if _candidate_instant(candidate, effective_zone) >= spec.effective_from:
                return True
        elif _candidate_local_date(candidate, effective_zone) >= spec.effective_from:
            return True
    return False


def _in_window(candidate: OccurrenceCoordinate, start: date, end: date, zone: ZoneInfo) -> bool:
    if isinstance(candidate, QuotaCoordinate):
        return candidate.period_start_date < end and candidate.period_end_date_exclusive > start
    if isinstance(candidate, ElapsedCoordinate):
        local_date = candidate.expected_at.astimezone(zone).date()
    elif isinstance(candidate, CalendarCoordinate) and candidate.resolved_at is not None:
        local_date = candidate.resolved_at.astimezone(zone).date()
    elif (
        isinstance(candidate, CalendarCoordinate)
        and candidate.clock_basis_code == "absolute_utc"
        and candidate.generated_wall_time is not None
    ):
        local_date = (
            datetime.combine(
                candidate.generated_date,
                candidate.generated_wall_time,
                tzinfo=UTC,
            )
            .astimezone(zone)
            .date()
        )
    else:
        local_date = candidate.generated_date
    return start <= local_date < end


def _calendar_candidates(
    state_ref: UUID,
    spec: CalendarRecurrence,
    start: date,
    end: date,
    effective_zone: ZoneInfo,
) -> list[OccurrenceCandidate]:
    scan_start = max(spec.effective_from, start - timedelta(days=2))
    if spec.range_kind == "expected_count":
        scan_start = spec.effective_from
    scan_end = end + timedelta(days=2)
    if spec.effective_until is not None:
        scan_end = min(scan_end, spec.effective_until)
    if (scan_end - scan_start).days > _MAX_CALENDAR_SCAN_DAYS:
        raise OccurrenceInputError(
            "Calendar Recurrence history is outside the bounded evaluator horizon."
        )
    generated_rank = 0
    results: list[OccurrenceCandidate] = []
    rule_zone = ZoneInfo(spec.zone_id) if spec.zone_id else None
    value = scan_start
    while value < scan_end:
        if value >= spec.effective_from and _calendar_phase_matches(spec, value):
            wall_times = spec.wall_times or (None,)
            for wall in wall_times:
                resolved: datetime | None = None
                if wall is not None and spec.clock_basis_code == "named_zone":
                    if rule_zone is None or spec.ambiguous_local_time_policy is None:
                        raise OccurrenceInputError(
                            "Named-zone Recurrence is missing its explicit DST contract."
                        )
                    resolved = _resolved_named_local(
                        datetime.combine(value, wall), rule_zone, spec.ambiguous_local_time_policy
                    )
                    if resolved is None:
                        continue
                candidate = CalendarCoordinate(
                    family_code="calendar_wall_clock",
                    generated_date=value,
                    generated_wall_time=wall,
                    clock_basis_code=spec.clock_basis_code,
                    zone_id=spec.zone_id,
                    resolved_at=resolved,
                )
                generated_rank += 1
                if spec.range_kind == "expected_count" and generated_rank > int(
                    spec.expected_occurrence_count or 0
                ):
                    return results
                if _in_window(candidate, start, end, effective_zone):
                    results.append(OccurrenceCandidate(state_ref, candidate))
                    if len(results) > MAX_CHECKPOINT_OCCURRENCES:
                        return results
        value += timedelta(days=1)
    return results


def _ceil_decimal(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_CEILING))


def _timedelta_decimal_seconds(value: Decimal) -> timedelta:
    microseconds = int((value * 1_000_000).to_integral_exact())
    return timedelta(microseconds=microseconds)


def _decimal_total_seconds(value: timedelta) -> Decimal:
    microseconds = value.days * 86_400_000_000 + value.seconds * 1_000_000 + value.microseconds
    return Decimal(microseconds) / Decimal(1_000_000)


def _elapsed_candidates(
    state_ref: UUID,
    spec: ElapsedRecurrence,
    start: date,
    end: date,
    effective_zone: ZoneInfo,
) -> list[OccurrenceCandidate]:
    start_at = datetime.combine(start, time.min, tzinfo=effective_zone).astimezone(UTC)
    end_at = datetime.combine(end, time.min, tzinfo=effective_zone).astimezone(UTC)
    lower = max(start_at, spec.effective_from)
    if spec.effective_until is not None:
        end_at = min(end_at, spec.effective_until)
    if lower >= end_at:
        return []
    interval = spec.elapsed_seconds
    offset = _decimal_total_seconds(lower - spec.anchor_at) / interval
    step = max(1, _ceil_decimal(offset))
    first_effective = max(
        1,
        _ceil_decimal(_decimal_total_seconds(spec.effective_from - spec.anchor_at) / interval),
    )
    results: list[OccurrenceCandidate] = []
    while True:
        expected = spec.anchor_at + _timedelta_decimal_seconds(interval * step)
        if expected >= end_at:
            break
        rank = step - first_effective + 1
        if spec.range_kind == "expected_count" and rank > int(spec.expected_occurrence_count or 0):
            break
        if expected >= lower:
            results.append(
                OccurrenceCandidate(
                    state_ref,
                    ElapsedCoordinate(family_code="elapsed_interval", expected_at=expected),
                )
            )
            if len(results) > MAX_CHECKPOINT_OCCURRENCES:
                break
        step += 1
    return results


def _period_floor(spec: QuotaRecurrence, value: date) -> date:
    if spec.period_unit_code == "day":
        anchor = spec.pattern_anchor_date or spec.effective_from
        delta = max(0, (value - anchor).days)
        return anchor + timedelta(days=(delta // spec.period_span) * spec.period_span)
    if spec.period_unit_code == "week":
        week_start = int(spec.week_start or 1)
        base = value - timedelta(days=(value.isoweekday() - week_start) % 7)
        anchor = spec.pattern_anchor_date
        if spec.period_span == 1 or anchor is None:
            return base
        anchor_base = anchor - timedelta(days=(anchor.isoweekday() - week_start) % 7)
        weeks = max(0, (base - anchor_base).days // 7)
        return anchor_base + timedelta(weeks=(weeks // spec.period_span) * spec.period_span)
    if spec.period_unit_code == "month":
        anchor = spec.pattern_anchor_date or date(value.year, value.month, 1)
        months = max(0, (value.year - anchor.year) * 12 + value.month - anchor.month)
        index = (months // spec.period_span) * spec.period_span
        return date(
            anchor.year + (anchor.month - 1 + index) // 12, (anchor.month - 1 + index) % 12 + 1, 1
        )
    anchor = spec.pattern_anchor_date or date(value.year, 1, 1)
    years = max(0, value.year - anchor.year)
    return date(anchor.year + (years // spec.period_span) * spec.period_span, 1, 1)


def _period_end(spec: QuotaRecurrence, start: date) -> date:
    if spec.period_unit_code == "day":
        return start + timedelta(days=spec.period_span)
    if spec.period_unit_code == "week":
        return start + timedelta(weeks=spec.period_span)
    if spec.period_unit_code == "month":
        index = start.month - 1 + spec.period_span
        return date(start.year + index // 12, index % 12 + 1, 1)
    return date(start.year + spec.period_span, 1, 1)


def _quota_candidates(
    state_ref: UUID,
    spec: QuotaRecurrence,
    start: date,
    end: date,
) -> list[OccurrenceCandidate]:
    period_start = _period_floor(spec, max(start, spec.effective_from))
    results: list[OccurrenceCandidate] = []
    while period_start < end:
        period_end = _period_end(spec, period_start)
        if (
            period_start >= spec.effective_from
            and (spec.effective_until is None or period_end <= spec.effective_until)
            and period_end > start
        ):
            coordinate = QuotaCoordinate(
                family_code="quota_per_period",
                period_start_date=period_start,
                period_end_date_exclusive=period_end,
                frame_code=spec.frame_code,
                zone_id=spec.zone_id,
            )
            for _ in range(spec.quota_count):
                results.append(OccurrenceCandidate(state_ref, coordinate))
                if len(results) > MAX_CHECKPOINT_OCCURRENCES:
                    return results
        period_start = period_end
    return results


def _cyclic_candidates(
    state_ref: UUID,
    spec: CyclicRecurrence,
    start: date,
    end: date,
) -> list[OccurrenceCandidate]:
    step_days = 1 if spec.position_unit_code == "day" else 7
    lower = max(start, spec.effective_from, spec.pattern_anchor_date)
    delta = (lower - spec.pattern_anchor_date).days
    first_step = max(0, _ceil_decimal(Decimal(delta) / Decimal(step_days)))
    results: list[OccurrenceCandidate] = []
    rank = 0
    if spec.range_kind == "expected_count":
        effective_delta = max(0, (spec.effective_from - spec.pattern_anchor_date).days)
        first_effective_step = _ceil_decimal(Decimal(effective_delta) / Decimal(step_days))
        prior_steps = max(0, first_step - first_effective_step)
        full_cycles, remainder = divmod(prior_steps, spec.cycle_length)
        rank = full_cycles * sum(spec.generates_expected)
        rank += sum(
            spec.generates_expected[(first_effective_step + offset) % spec.cycle_length]
            for offset in range(remainder)
        )
    step = first_step
    while True:
        generated = spec.pattern_anchor_date + timedelta(days=step * step_days)
        if generated >= end or (
            spec.effective_until is not None and generated >= spec.effective_until
        ):
            break
        position = step % spec.cycle_length
        if generated >= spec.effective_from and spec.generates_expected[position]:
            rank += 1
            if spec.range_kind == "expected_count" and rank > int(
                spec.expected_occurrence_count or 0
            ):
                break
            results.append(
                OccurrenceCandidate(
                    state_ref,
                    CyclicCoordinate(
                        family_code="cyclic_positional",
                        generated_date=generated,
                        position_index=position,
                    ),
                )
            )
        step += 1
    return results


def evaluate_recurrence_history(
    history: tuple[RecurrenceHistoryEntry, ...],
    *,
    start_date: date,
    end_date_exclusive: date,
    effective_zone_id: str,
) -> tuple[OccurrenceCandidate, ...]:
    """Evaluate one immutable state sequence under a bounded civil window."""
    _validate_window(start_date, end_date_exclusive)
    effective_zone = _zone(effective_zone_id)
    ordered = tuple(
        sorted(history, key=lambda item: (item.current_from_at, item.material_state_ref))
    )
    results: list[OccurrenceCandidate] = []
    for index, entry in enumerate(ordered):
        spec = entry.recurrence
        if isinstance(spec, CalendarRecurrence):
            candidates = _calendar_candidates(
                entry.material_state_ref, spec, start_date, end_date_exclusive, effective_zone
            )
        elif isinstance(spec, ElapsedRecurrence):
            candidates = _elapsed_candidates(
                entry.material_state_ref, spec, start_date, end_date_exclusive, effective_zone
            )
        elif isinstance(spec, QuotaRecurrence):
            candidates = _quota_candidates(
                entry.material_state_ref, spec, start_date, end_date_exclusive
            )
        else:
            candidates = _cyclic_candidates(
                entry.material_state_ref, spec, start_date, end_date_exclusive
            )
        successors = ordered[index + 1 :]
        for candidate in candidates:
            if not _is_superseded(candidate.coordinate, successors, effective_zone):
                results.append(candidate)
                if len(results) > MAX_CHECKPOINT_OCCURRENCES:
                    raise OccurrenceCheckpointLimitError(
                        "Checkpoint would materialize more than 10,000 Occurrences; narrow the requested horizon."
                    )
    return tuple(results)


def _history_entry(row: RowMapping) -> RecurrenceHistoryEntry:
    view = recurrence_view_from_row(row)
    return RecurrenceHistoryEntry(
        material_state_ref=view.material_state_ref,
        current_from_at=row["current_from_at"],
        current_until_at=row["current_until_at"],
        recurrence=view.recurrence,
    )


def _coordinate(row: RowMapping) -> OccurrenceCoordinate | None:
    family = row["family_code"]
    if family == "calendar_wall_clock":
        return CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=row["generated_date"],
            generated_wall_time=row["generated_wall_time"],
            clock_basis_code=row["clock_basis_code"],
            zone_id=row["zone_id"],
            resolved_at=row["resolved_at"],
        )
    if family == "elapsed_interval":
        return ElapsedCoordinate(family_code="elapsed_interval", expected_at=row["expected_at"])
    if family == "quota_per_period":
        return QuotaCoordinate(
            family_code="quota_per_period",
            period_start_date=row["period_start_date"],
            period_end_date_exclusive=row["period_end_date_exclusive"],
            frame_code=row["frame_code"],
            zone_id=row["quota_zone_id"],
        )
    if family == "cyclic_positional":
        return CyclicCoordinate(
            family_code="cyclic_positional",
            generated_date=row["generated_date"],
            position_index=int(row["position_index"]),
        )
    return None


def _occurrence(row: RowMapping) -> OccurrenceView:
    return OccurrenceView(
        occurrence_ref=UUID(str(row["occurrence_ref"])),
        source_native_ref=UUID(str(row["source_native_ref"])),
        governing_recurrence_state_ref=(
            UUID(str(row["governing_recurrence_state_ref"]))
            if row["governing_recurrence_state_ref"] is not None
            else None
        ),
        origin_code=row["origin_code"],
        coordinate=_coordinate(row),
        skipped=bool(row["skipped"]),
        skip_reason=row["skip_reason"],
        skipped_at=row["skipped_at"],
    )


def _occurrence_order(value: OccurrenceView) -> tuple[str, str, str]:
    coordinate = value.coordinate
    if isinstance(coordinate, CalendarCoordinate):
        primary = f"{coordinate.generated_date.isoformat()}T{(coordinate.generated_wall_time or time.min).isoformat()}"
    elif isinstance(coordinate, ElapsedCoordinate):
        primary = coordinate.expected_at.astimezone(UTC).isoformat()
    elif isinstance(coordinate, QuotaCoordinate):
        primary = coordinate.period_start_date.isoformat()
    elif isinstance(coordinate, CyclicCoordinate):
        primary = coordinate.generated_date.isoformat()
    else:
        primary = "9999-12-31"
    return (
        primary,
        coordinate.family_code if coordinate is not None else "explicit_extra",
        str(value.occurrence_ref),
    )


def _candidate_parameters(candidate: OccurrenceCandidate) -> dict[str, object]:
    coordinate = candidate.coordinate
    values: dict[str, object] = {
        "state": candidate.governing_recurrence_state_ref,
        "family": coordinate.family_code,
        "generated_date": None,
        "generated_wall_time": None,
        "clock_basis": None,
        "zone_id": None,
        "resolved_at": None,
        "expected_at": None,
        "period_start": None,
        "period_end": None,
        "frame_code": None,
        "quota_zone_id": None,
        "position_index": None,
    }
    if isinstance(coordinate, CalendarCoordinate):
        values.update(
            generated_date=coordinate.generated_date,
            generated_wall_time=coordinate.generated_wall_time,
            clock_basis=coordinate.clock_basis_code,
            zone_id=coordinate.zone_id,
            resolved_at=coordinate.resolved_at,
        )
    elif isinstance(coordinate, ElapsedCoordinate):
        values["expected_at"] = coordinate.expected_at
    elif isinstance(coordinate, QuotaCoordinate):
        values.update(
            period_start=coordinate.period_start_date,
            period_end=coordinate.period_end_date_exclusive,
            frame_code=coordinate.frame_code,
            quota_zone_id=coordinate.zone_id,
        )
    else:
        values.update(
            generated_date=coordinate.generated_date,
            position_index=coordinate.position_index,
        )
    return values


def _error(exc: DBAPIError) -> Exception:
    name = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
    if name in {
        "pk_occurrence_checkpoint_operation",
        "pk_occurrence_extra_operation",
        "pk_occurrence_exclusion_operation",
        "uq_occurrence_skip_operation",
    }:
        return OccurrenceOperationReuseError()
    if name in {
        "routine_occurrence_source_unavailable",
        "event_occurrence_source_unavailable",
        "routine_occurrence_checkpoint_unavailable",
        "event_occurrence_checkpoint_unavailable",
        "routine_occurrence_recurrence_unavailable",
        "event_occurrence_recurrence_unavailable",
        "occurrence_unavailable",
    }:
        return OccurrenceSourceNotFoundError()
    if name == "routine_occurrence_source_inactive":
        return OccurrenceSourceInactiveError()
    if name == "pk_occurrence_skip":
        return OccurrenceAlreadySkippedError()
    if name == "occurrence_exclusion_materialized_conflict":
        return OccurrenceMaterializedConflictError()
    return OccurrencePersistenceError()


class OccurrenceApplication:
    """Transactional B06-C command service."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def checkpoint_window(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        start_date: date,
        end_date_exclusive: date,
        effective_zone_id: str,
    ) -> OccurrenceWindowCheckpoint:
        """Explicitly checkpoint every current self recurrence source for one window."""
        root_operation_id = _bounded_operation_id(operation_id)
        _validate_window(start_date, end_date_exclusive)
        zone_id = _zone(effective_zone_id).key
        statement = text(
            """
            WITH self_routine AS (
                SELECT routine_ref, lifecycle_state
                  FROM dante.list_self_routines(:actor)
            )
            SELECT 'routine'::text AS owner, routine.routine_ref AS source_ref
              FROM self_routine AS routine
              JOIN dante.routine_recurrence_current_history AS current
                ON current.routine_ref = routine.routine_ref
               AND current.current_until_at IS NULL
             WHERE routine.lifecycle_state = 'active'
            UNION ALL
            SELECT 'event'::text AS owner, expectation.event_ref AS source_ref
              FROM dante.event_expectation AS expectation
              JOIN dante.event_recurrence_current_history AS current
                ON current.event_ref = expectation.event_ref
               AND current.current_until_at IS NULL
             WHERE expectation.self_person_ref = :actor
             ORDER BY owner, source_ref
            """
        )
        try:
            async with self._session_factory() as session, session.begin():
                source_rows = (
                    (await session.execute(statement, {"actor": self_person_ref}))
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

        checkpoints: list[OccurrenceCheckpoint] = []
        for row in source_rows:
            owner = row["owner"]
            if owner not in {"routine", "event"}:
                raise OccurrencePersistenceError()
            source_ref = UUID(str(row["source_ref"]))
            checkpoints.append(
                await self.checkpoint(
                    owner=owner,
                    self_person_ref=self_person_ref,
                    source_ref=source_ref,
                    operation_id=_window_source_operation_id(
                        root_operation_id=root_operation_id,
                        owner=owner,
                        source_ref=source_ref,
                        start_date=start_date,
                        end_date_exclusive=end_date_exclusive,
                        effective_zone_id=zone_id,
                    ),
                    start_date=start_date,
                    end_date_exclusive=end_date_exclusive,
                    effective_zone_id=zone_id,
                )
            )

        return OccurrenceWindowCheckpoint(
            start_date=start_date,
            end_date_exclusive=end_date_exclusive,
            effective_zone_id=zone_id,
            source_count=len(checkpoints),
            occurrence_count=sum(len(item.occurrences) for item in checkpoints),
            replayed_source_count=sum(item.replayed for item in checkpoints),
        )

    async def checkpoint(
        self,
        *,
        owner: OccurrenceOwner,
        self_person_ref: NativeRef,
        source_ref: UUID,
        operation_id: str,
        start_date: date,
        end_date_exclusive: date,
        effective_zone_id: str,
    ) -> OccurrenceCheckpoint:
        key = _bounded_operation_id(operation_id)
        _validate_window(start_date, end_date_exclusive)
        zone_id = _zone(effective_zone_id).key
        fingerprint = _fingerprint(
            {
                "kind": "checkpoint",
                "owner": owner,
                "source_ref": source_ref,
                "start_date": start_date,
                "end_date_exclusive": end_date_exclusive,
                "effective_zone_id": zone_id,
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                accepted = (
                    (
                        await session.execute(
                            text(
                                f"SELECT * FROM dante.begin_self_{owner}_occurrence_checkpoint("
                                ":actor,:operation,:fingerprint,:source,:start,:end,:zone)"
                            ),
                            {
                                "actor": self_person_ref,
                                "operation": key,
                                "fingerprint": fingerprint,
                                "source": source_ref,
                                "start": start_date,
                                "end": end_date_exclusive,
                                "zone": zone_id,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                replayed = bool(accepted["replayed"])
                if not replayed:
                    rows = (
                        (
                            await session.execute(
                                text(
                                    f"SELECT * FROM dante.list_self_{owner}_recurrence_history("
                                    ":actor,:source)"
                                ),
                                {"actor": self_person_ref, "source": source_ref},
                            )
                        )
                        .mappings()
                        .all()
                    )
                    history = tuple(_history_entry(row) for row in rows)
                    candidates = evaluate_recurrence_history(
                        history,
                        start_date=start_date,
                        end_date_exclusive=end_date_exclusive,
                        effective_zone_id=zone_id,
                    )
                    for candidate in candidates:
                        parameters = {
                            "actor": self_person_ref,
                            "operation": key,
                            "source": source_ref,
                            **_candidate_parameters(candidate),
                        }
                        await session.execute(
                            text(
                                f"SELECT * FROM dante.materialize_self_{owner}_occurrence_candidate("
                                ":actor,:operation,:source,:state,:family,:generated_date,"
                                ":generated_wall_time,:clock_basis,:zone_id,:resolved_at,"
                                ":expected_at,:period_start,:period_end,:frame_code,"
                                ":quota_zone_id,:position_index)"
                            ),
                            parameters,
                        )
                result_rows = (
                    (
                        await session.execute(
                            text(
                                f"SELECT * FROM dante.get_self_{owner}_occurrence_checkpoint_result("
                                ":actor,:operation,:source)"
                            ),
                            {"actor": self_person_ref, "operation": key, "source": source_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
                result = tuple(
                    sorted((_occurrence(row) for row in result_rows), key=_occurrence_order)
                )
            return OccurrenceCheckpoint(
                source_native_ref=source_ref,
                start_date=start_date,
                end_date_exclusive=end_date_exclusive,
                effective_zone_id=zone_id,
                occurrences=result,
                accepted_at=accepted["accepted_at"],
                replayed=replayed,
            )
        except OccurrenceInputError, OccurrenceCheckpointLimitError:
            raise
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

    async def get(self, *, self_person_ref: NativeRef, occurrence_ref: UUID) -> OccurrenceView:
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text("SELECT * FROM dante.get_self_occurrence(:actor,:occurrence)"),
                            {"actor": self_person_ref, "occurrence": occurrence_ref},
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
                if row is None:
                    raise OccurrenceSourceNotFoundError()
                return _occurrence(row)
        except OccurrenceSourceNotFoundError:
            raise
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

    async def create_extra(
        self,
        *,
        owner: OccurrenceOwner,
        self_person_ref: NativeRef,
        source_ref: UUID,
        operation_id: str,
    ) -> OccurrenceMutation:
        key = _bounded_operation_id(operation_id)
        fingerprint = _fingerprint(
            {"kind": "explicit_extra", "owner": owner, "source_ref": source_ref}
        )
        try:
            async with self._session_factory() as session, session.begin():
                accepted = (
                    (
                        await session.execute(
                            text(
                                f"SELECT * FROM dante.create_self_{owner}_extra_occurrence("
                                ":actor,:operation,:fingerprint,:source)"
                            ),
                            {
                                "actor": self_person_ref,
                                "operation": key,
                                "fingerprint": fingerprint,
                                "source": source_ref,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                row = (
                    (
                        await session.execute(
                            text("SELECT * FROM dante.get_self_occurrence(:actor,:occurrence)"),
                            {"actor": self_person_ref, "occurrence": accepted["occurrence_ref"]},
                        )
                    )
                    .mappings()
                    .one()
                )
            return OccurrenceMutation(
                occurrence=_occurrence(row),
                accepted_at=accepted["accepted_at"],
                replayed=bool(accepted["replayed"]),
            )
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

    async def skip(
        self,
        *,
        self_person_ref: NativeRef,
        occurrence_ref: UUID,
        operation_id: str,
        reason: str | None,
    ) -> OccurrenceMutation:
        key = _bounded_operation_id(operation_id)
        normalized_reason = reason.strip() if reason is not None else None
        if normalized_reason == "":
            normalized_reason = None
        if normalized_reason is not None and len(normalized_reason) > 500:
            raise OccurrenceInputError("Skip reason must contain at most 500 characters.")
        fingerprint = _fingerprint(
            {
                "kind": "skip",
                "occurrence_ref": occurrence_ref,
                "reason": normalized_reason,
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                accepted = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.skip_self_occurrence("
                                ":actor,:operation,:fingerprint,:occurrence,:reason)"
                            ),
                            {
                                "actor": self_person_ref,
                                "operation": key,
                                "fingerprint": fingerprint,
                                "occurrence": occurrence_ref,
                                "reason": normalized_reason,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                row = (
                    (
                        await session.execute(
                            text("SELECT * FROM dante.get_self_occurrence(:actor,:occurrence)"),
                            {"actor": self_person_ref, "occurrence": occurrence_ref},
                        )
                    )
                    .mappings()
                    .one()
                )
            return OccurrenceMutation(
                occurrence=_occurrence(row),
                accepted_at=accepted["skipped_at"],
                replayed=bool(accepted["replayed"]),
            )
        except OccurrenceInputError:
            raise
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc

    async def exclude(
        self,
        *,
        owner: OccurrenceOwner,
        self_person_ref: NativeRef,
        source_ref: UUID,
        governing_recurrence_state_ref: UUID,
        operation_id: str,
        coordinate: CalendarCoordinate | ElapsedCoordinate | CyclicCoordinate,
    ) -> OccurrenceExclusion:
        key = _bounded_operation_id(operation_id)
        coordinate = _normalize_exclusion_coordinate(coordinate)
        fingerprint = _fingerprint(
            {
                "kind": "structural_exclusion",
                "owner": owner,
                "source_ref": source_ref,
                "governing_recurrence_state_ref": governing_recurrence_state_ref,
                "coordinate": asdict(coordinate),
            }
        )
        values = _candidate_parameters(
            OccurrenceCandidate(governing_recurrence_state_ref, coordinate)
        )
        try:
            async with self._session_factory() as session, session.begin():
                row = (
                    (
                        await session.execute(
                            text(
                                f"SELECT * FROM dante.exclude_self_{owner}_occurrence_coordinate("
                                ":actor,:operation,:fingerprint,:source,:state,:family,"
                                ":generated_date,:generated_wall_time,:expected_at,:position_index)"
                            ),
                            {
                                "actor": self_person_ref,
                                "operation": key,
                                "fingerprint": fingerprint,
                                "source": source_ref,
                                **values,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
            return OccurrenceExclusion(
                exclusion_ref=UUID(str(row["exclusion_ref"])),
                source_native_ref=source_ref,
                governing_recurrence_state_ref=governing_recurrence_state_ref,
                coordinate=coordinate,
                accepted_at=row["accepted_at"],
                replayed=bool(row["replayed"]),
            )
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc
