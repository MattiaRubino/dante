"""B06-B immutable, owner-bound Recurrence authoring.

This boundary deliberately authors Recurrence MaterialStates only.  It does not
expand a series, materialize an Occurrence, create an Activity/Event instance,
or establish a Schedule.  Those effects belong to B06-C/D.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, time
from decimal import Decimal
from typing import Literal, TypeAlias
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef

RecurrenceOwner = Literal["routine", "event"]
RangeKind = Literal["open", "until_boundary", "expected_count"]
CalendarPattern = Literal[
    "daily", "weekly_weekdays", "monthly_month_days", "monthly_ordinal_weekdays",
    "yearly_month_days", "anchor_step",
]
CalendarClockBasis = Literal["floating_local", "named_zone", "absolute_utc"]


class RecurrenceInputError(ValueError):
    """A typed Recurrence command is internally inconsistent."""


class RecurrenceOperationReuseError(RuntimeError):
    """The actor-local idempotency key has a different canonical intent."""


class RecurrenceNotFoundError(RuntimeError):
    """The Routine/Event owner is unavailable in this self scope."""


class RecurrenceStateConflictError(RuntimeError):
    """The replacement was based on a stale administrative current state."""


class RecurrencePersistenceError(RuntimeError):
    """The governed Recurrence persistence capability did not complete."""


@dataclass(frozen=True, slots=True)
class CalendarRecurrence:
    family_code: Literal["calendar_wall_clock"]
    range_kind: RangeKind
    expected_occurrence_count: int | None
    effective_from: date
    effective_until: date | None
    pattern_code: CalendarPattern
    interval_count: int
    clock_basis_code: CalendarClockBasis
    zone_id: str | None
    pattern_anchor_date: date | None
    wall_times: tuple[time, ...]
    weekdays: tuple[int, ...]
    month_days: tuple[int, ...]
    ordinal_weekdays: tuple[tuple[int, int], ...]
    year_month_days: tuple[tuple[int, int], ...]
    nonexistent_local_time_policy: Literal["skip_civil_candidate"] | None
    ambiguous_local_time_policy: Literal["earlier", "later"] | None
    step_unit_code: Literal["day", "week", "month", "year"] | None = None


@dataclass(frozen=True, slots=True)
class ElapsedRecurrence:
    family_code: Literal["elapsed_interval"]
    range_kind: RangeKind
    expected_occurrence_count: int | None
    effective_from: datetime
    effective_until: datetime | None
    elapsed_seconds: Decimal
    anchor_mode_code: Literal["fixed_anchor", "previous_expected"]
    anchor_at: datetime


@dataclass(frozen=True, slots=True)
class QuotaRecurrence:
    family_code: Literal["quota_per_period"]
    range_kind: Literal["open", "until_boundary"]
    expected_occurrence_count: None
    effective_from: date
    effective_until: date | None
    quota_count: int
    period_unit_code: Literal["day", "week", "month", "year"]
    period_span: int
    frame_code: Literal["floating_local", "named_zone", "absolute_utc"]
    zone_id: str | None
    week_start: int | None
    pattern_anchor_date: date | None


@dataclass(frozen=True, slots=True)
class CyclicRecurrence:
    family_code: Literal["cyclic_positional"]
    range_kind: RangeKind
    expected_occurrence_count: int | None
    effective_from: date
    effective_until: date | None
    cycle_length: int
    position_unit_code: Literal["day", "week"]
    pattern_anchor_date: date
    generates_expected: tuple[bool, ...]


RecurrenceSpec: TypeAlias = CalendarRecurrence | ElapsedRecurrence | QuotaRecurrence | CyclicRecurrence


@dataclass(frozen=True, slots=True)
class RecurrenceView:
    material_state_ref: UUID
    recurrence: RecurrenceSpec


@dataclass(frozen=True, slots=True)
class RecurrenceMutation:
    recurrence: RecurrenceView
    accepted_at: datetime
    replayed: bool


def _canonical_json_scalar(value: object) -> str:
    """Serialize non-JSON temporal and numeric values without representation drift."""
    if isinstance(value, Decimal):
        return format(value.normalize(), "f")
    if isinstance(value, (date, datetime, time)):
        return value.isoformat()
    return str(value)


def _fingerprint(*, owner: RecurrenceOwner, owner_ref: UUID, expected_state_ref: UUID | None, recurrence: RecurrenceSpec) -> str:
    """A canonical fingerprint, including all fields that change recurrence truth."""
    payload = json.dumps(
        {
            "version": 1,
            "owner": owner,
            "owner_ref": str(owner_ref),
            "expected_material_state_ref": str(expected_state_ref) if expected_state_ref else None,
            "recurrence": asdict(recurrence),
        },
        default=_canonical_json_scalar,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _bounded_operation_id(value: str) -> str:
    key = value.strip()
    if not key or len(key) > 200:
        raise RecurrenceInputError("Recurrence operation id must contain 1 to 200 characters.")
    return key


def _validate(spec: RecurrenceSpec) -> None:
    """Mirror the important invariants before invoking the SQL security boundary."""
    if spec.range_kind == "expected_count" and (spec.expected_occurrence_count is None or spec.expected_occurrence_count < 1):
        raise RecurrenceInputError("Expected-count Recurrence requires a positive expected occurrence count.")
    if spec.range_kind != "expected_count" and spec.expected_occurrence_count is not None:
        raise RecurrenceInputError("Only expected-count Recurrence may carry expected occurrence count.")
    if spec.range_kind == "until_boundary" and spec.effective_until is None:
        raise RecurrenceInputError("Until-boundary Recurrence requires an effective end boundary.")
    if spec.range_kind != "until_boundary" and spec.effective_until is not None:
        raise RecurrenceInputError("Only until-boundary Recurrence may carry an effective end boundary.")
    if spec.effective_until is not None and spec.effective_until <= spec.effective_from:
        raise RecurrenceInputError("Effective Recurrence range must be non-empty and half-open.")
    if isinstance(spec, CalendarRecurrence):
        if spec.interval_count < 1:
            raise RecurrenceInputError("Calendar interval must be positive.")
        if spec.clock_basis_code == "named_zone":
            if not spec.zone_id or spec.nonexistent_local_time_policy != "skip_civil_candidate" or spec.ambiguous_local_time_policy not in {"earlier", "later"}:
                raise RecurrenceInputError("Named-zone calendar Recurrence requires explicit IANA zone and DST policy.")
        elif spec.zone_id is not None or spec.nonexistent_local_time_policy is not None or spec.ambiguous_local_time_policy is not None:
            raise RecurrenceInputError("Only named-zone calendar Recurrence may carry zone or DST policy.")
        requires_anchor = spec.interval_count > 1 or spec.pattern_code == "anchor_step"
        if requires_anchor != (spec.pattern_anchor_date is not None):
            raise RecurrenceInputError("Calendar pattern-anchor presence does not match its pattern/interval.")
        expected_selector = {
            "daily": 0,
            "weekly_weekdays": len(spec.weekdays),
            "monthly_month_days": len(spec.month_days),
            "monthly_ordinal_weekdays": len(spec.ordinal_weekdays),
            "yearly_month_days": len(spec.year_month_days),
            "anchor_step": 0,
        }[spec.pattern_code]
        actual_other = len(spec.weekdays) + len(spec.month_days) + len(spec.ordinal_weekdays) + len(spec.year_month_days)
        if (spec.pattern_code in {"daily", "anchor_step"} and actual_other) or (expected_selector == 0 and spec.pattern_code not in {"daily", "anchor_step"}) or (expected_selector and actual_other != expected_selector):
            raise RecurrenceInputError("Calendar selectors do not match the requested calendar pattern.")
        if len(set(spec.wall_times)) != len(spec.wall_times) or len(set(spec.weekdays)) != len(spec.weekdays) or len(set(spec.month_days)) != len(spec.month_days) or len(set(spec.ordinal_weekdays)) != len(spec.ordinal_weekdays) or len(set(spec.year_month_days)) != len(spec.year_month_days):
            raise RecurrenceInputError("Calendar selectors must not contain duplicates.")
    elif isinstance(spec, ElapsedRecurrence):
        if spec.elapsed_seconds <= 0 or spec.elapsed_seconds.as_tuple().exponent < -6:
            raise RecurrenceInputError("Elapsed interval must be positive with at most six decimal places.")
        if spec.effective_from.tzinfo is None or spec.anchor_at.tzinfo is None or (spec.effective_until and spec.effective_until.tzinfo is None):
            raise RecurrenceInputError("Elapsed Recurrence requires absolute instants with timezone offsets.")
    elif isinstance(spec, QuotaRecurrence):
        if spec.quota_count < 1 or spec.period_span < 1:
            raise RecurrenceInputError("Quota count and period span must be positive.")
        if (spec.frame_code == "named_zone") != bool(spec.zone_id):
            raise RecurrenceInputError("Quota named-zone frame requires exactly one IANA zone.")
        if (spec.period_unit_code == "week") != (spec.week_start is not None):
            raise RecurrenceInputError("Quota week start is required only for weekly periods.")
        if spec.period_span > 1 and spec.pattern_anchor_date is None:
            raise RecurrenceInputError("Multi-period quota Recurrence requires a period anchor.")
        if spec.period_span == 1 and spec.pattern_anchor_date is not None:
            raise RecurrenceInputError("Single-period quota Recurrence does not accept a period anchor.")
    else:
        if spec.cycle_length < 1 or len(spec.generates_expected) != spec.cycle_length:
            raise RecurrenceInputError("Cyclic Recurrence requires one position disposition for every cycle position.")


def _arrays(spec: RecurrenceSpec) -> dict[str, object]:
    values: dict[str, object] = {
        "effective_from_date": None, "effective_until_date": None,
        "effective_from_instant": None, "effective_until_instant": None,
        "calendar_pattern_code": None, "calendar_interval_count": None, "calendar_clock_basis_code": None,
        "calendar_zone_id": None, "calendar_step_unit_code": None, "calendar_pattern_anchor_date": None,
        "calendar_wall_times": None, "calendar_weekdays": None, "calendar_month_days": None,
        "calendar_ordinal_weekdays": None, "calendar_ordinals": None,
        "calendar_year_months": None, "calendar_year_month_days": None,
        "dst_nonexistent_local_time_policy": None, "dst_ambiguous_local_time_policy": None,
        "elapsed_seconds": None, "elapsed_anchor_mode_code": None, "elapsed_anchor_at": None,
        "quota_count": None, "quota_period_unit_code": None, "quota_period_span": None,
        "quota_frame_code": None, "quota_zone_id": None, "quota_week_start": None,
        "cyclic_cycle_length": None, "cyclic_position_unit_code": None, "cyclic_pattern_anchor_date": None,
        "cyclic_generates_expected": None,
    }
    if isinstance(spec, CalendarRecurrence):
        values.update(effective_from_date=spec.effective_from, effective_until_date=spec.effective_until,
            calendar_pattern_code=spec.pattern_code, calendar_interval_count=spec.interval_count,
            calendar_clock_basis_code=spec.clock_basis_code, calendar_zone_id=spec.zone_id,
            calendar_step_unit_code=spec.step_unit_code, calendar_pattern_anchor_date=spec.pattern_anchor_date,
            calendar_wall_times=list(spec.wall_times), calendar_weekdays=list(spec.weekdays),
            calendar_month_days=list(spec.month_days), calendar_ordinal_weekdays=[pair[0] for pair in spec.ordinal_weekdays],
            calendar_ordinals=[pair[1] for pair in spec.ordinal_weekdays], calendar_year_months=[pair[0] for pair in spec.year_month_days],
            calendar_year_month_days=[pair[1] for pair in spec.year_month_days],
            dst_nonexistent_local_time_policy=spec.nonexistent_local_time_policy,
            dst_ambiguous_local_time_policy=spec.ambiguous_local_time_policy)
    elif isinstance(spec, ElapsedRecurrence):
        values.update(effective_from_instant=spec.effective_from, effective_until_instant=spec.effective_until,
            elapsed_seconds=spec.elapsed_seconds, elapsed_anchor_mode_code=spec.anchor_mode_code, elapsed_anchor_at=spec.anchor_at)
    elif isinstance(spec, QuotaRecurrence):
        values.update(effective_from_date=spec.effective_from, effective_until_date=spec.effective_until,
            calendar_pattern_anchor_date=spec.pattern_anchor_date, quota_count=spec.quota_count,
            quota_period_unit_code=spec.period_unit_code, quota_period_span=spec.period_span,
            quota_frame_code=spec.frame_code, quota_zone_id=spec.zone_id, quota_week_start=spec.week_start)
    else:
        values.update(effective_from_date=spec.effective_from, effective_until_date=spec.effective_until,
            cyclic_cycle_length=spec.cycle_length, cyclic_position_unit_code=spec.position_unit_code,
            cyclic_pattern_anchor_date=spec.pattern_anchor_date, cyclic_generates_expected=list(spec.generates_expected))
    return values


def _view(row: RowMapping) -> RecurrenceView:
    family = str(row["family_code"])
    range_kind = row["range_kind"]
    expected = row["expected_occurrence_count"]
    if family == "calendar_wall_clock":
        recurrence: RecurrenceSpec = CalendarRecurrence(
            family_code="calendar_wall_clock", range_kind=range_kind, expected_occurrence_count=expected,
            effective_from=row["effective_from_date"], effective_until=row["effective_until_date"],
            pattern_code=row["calendar_pattern_code"], interval_count=int(row["calendar_interval_count"]),
            clock_basis_code=row["calendar_clock_basis_code"], zone_id=row["calendar_zone_id"],
            pattern_anchor_date=row["calendar_pattern_anchor_date"], wall_times=tuple(row["calendar_wall_times"] or ()),
            weekdays=tuple(int(v) for v in row["calendar_weekdays"] or ()), month_days=tuple(int(v) for v in row["calendar_month_days"] or ()),
            ordinal_weekdays=tuple(zip((int(v) for v in row["calendar_ordinal_weekdays"] or ()), (int(v) for v in row["calendar_ordinals"] or ()), strict=True)),
            year_month_days=tuple(zip((int(v) for v in row["calendar_year_months"] or ()), (int(v) for v in row["calendar_year_month_days"] or ()), strict=True)),
            nonexistent_local_time_policy=row["dst_nonexistent_local_time_policy"], ambiguous_local_time_policy=row["dst_ambiguous_local_time_policy"],
            step_unit_code=row["calendar_step_unit_code"],
        )
    elif family == "elapsed_interval":
        recurrence = ElapsedRecurrence(family_code="elapsed_interval", range_kind=range_kind, expected_occurrence_count=expected,
            effective_from=row["effective_from_instant"], effective_until=row["effective_until_instant"],
            elapsed_seconds=Decimal(str(row["elapsed_seconds"])), anchor_mode_code=row["elapsed_anchor_mode_code"], anchor_at=row["elapsed_anchor_at"])
    elif family == "quota_per_period":
        recurrence = QuotaRecurrence(family_code="quota_per_period", range_kind=range_kind, expected_occurrence_count=None,
            effective_from=row["effective_from_date"], effective_until=row["effective_until_date"], quota_count=int(row["quota_count"]),
            period_unit_code=row["quota_period_unit_code"], period_span=int(row["quota_period_span"]), frame_code=row["quota_frame_code"],
            zone_id=row["quota_zone_id"], week_start=row["quota_week_start"], pattern_anchor_date=row["calendar_pattern_anchor_date"])
    else:
        recurrence = CyclicRecurrence(family_code="cyclic_positional", range_kind=range_kind, expected_occurrence_count=expected,
            effective_from=row["effective_from_date"], effective_until=row["effective_until_date"], cycle_length=int(row["cyclic_cycle_length"]),
            position_unit_code=row["cyclic_position_unit_code"], pattern_anchor_date=row["cyclic_pattern_anchor_date"],
            generates_expected=tuple(bool(v) for v in row["cyclic_generates_expected"] or ()))
    return RecurrenceView(material_state_ref=UUID(str(row["material_state_ref"])), recurrence=recurrence)


def _error(exc: DBAPIError) -> Exception:
    name = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
    if name in {"pk_routine_recurrence_operation", "pk_event_recurrence_operation"}:
        return RecurrenceOperationReuseError()
    if name in {"routine_recurrence_unavailable", "event_recurrence_unavailable"}:
        return RecurrenceNotFoundError()
    if name in {"routine_recurrence_state_conflict", "event_recurrence_state_conflict"}:
        return RecurrenceStateConflictError()
    return RecurrencePersistenceError()


class RecurrenceApplication:
    """The B06-B temporal command boundary; all writes are SQL-governed and atomic."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def get(self, *, owner: RecurrenceOwner, self_person_ref: NativeRef, owner_ref: UUID) -> RecurrenceView | None:
        try:
            async with self._session_factory() as session, session.begin():
                row = (await session.execute(text(f"SELECT * FROM dante.get_self_{owner}_recurrence(:actor,:owner)"), {"actor": self_person_ref, "owner": owner_ref})).mappings().one_or_none()
                return _view(row) if row is not None else None
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RecurrencePersistenceError() from exc

    async def replace(self, *, owner: RecurrenceOwner, self_person_ref: NativeRef, owner_ref: UUID, operation_id: str, expected_material_state_ref: UUID | None, recurrence: RecurrenceSpec) -> RecurrenceMutation:
        key = _bounded_operation_id(operation_id)
        _validate(recurrence)
        if owner == "routine" and expected_material_state_ref is None:
            raise RecurrenceInputError("Routine Recurrence replacement requires the current MaterialState reference.")
        fingerprint = _fingerprint(owner=owner, owner_ref=owner_ref, expected_state_ref=expected_material_state_ref, recurrence=recurrence)
        parameters: dict[str, object] = {"actor": self_person_ref, "operation": key, "fingerprint": fingerprint, "owner": owner_ref,
            "expected": expected_material_state_ref, "family_code": recurrence.family_code, "range_kind": recurrence.range_kind,
            "expected_occurrence_count": recurrence.expected_occurrence_count}
        parameters.update(_arrays(recurrence))
        statement = text(f"""SELECT * FROM dante.replace_self_{owner}_recurrence(
          :actor,:operation,:fingerprint,:owner,:expected,:family_code,:range_kind,:expected_occurrence_count,
          :effective_from_date,:effective_until_date,:effective_from_instant,:effective_until_instant,
          :calendar_pattern_code,:calendar_interval_count,:calendar_clock_basis_code,:calendar_zone_id,:calendar_step_unit_code,:calendar_pattern_anchor_date,
          :calendar_wall_times,:calendar_weekdays,:calendar_month_days,:calendar_ordinal_weekdays,:calendar_ordinals,:calendar_year_months,:calendar_year_month_days,
          :dst_nonexistent_local_time_policy,:dst_ambiguous_local_time_policy,:elapsed_seconds,:elapsed_anchor_mode_code,:elapsed_anchor_at,
          :quota_count,:quota_period_unit_code,:quota_period_span,:quota_frame_code,:quota_zone_id,:quota_week_start,
          :cyclic_cycle_length,:cyclic_position_unit_code,:cyclic_pattern_anchor_date,:cyclic_generates_expected)""")
        try:
            async with self._session_factory() as session, session.begin():
                receipt = (await session.execute(statement, parameters)).mappings().one()
                row = (await session.execute(text(f"SELECT * FROM dante.get_self_{owner}_recurrence(:actor,:owner)"), {"actor": self_person_ref, "owner": owner_ref})).mappings().one_or_none()
                if row is None or UUID(str(row["material_state_ref"])) != UUID(str(receipt["material_state_ref"])):
                    raise RecurrencePersistenceError("Accepted Recurrence state was not readable as current truth.")
                return RecurrenceMutation(recurrence=_view(row), accepted_at=receipt["accepted_at"], replayed=bool(receipt["replayed"]))
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise RecurrencePersistenceError() from exc
