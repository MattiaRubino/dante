"""B02 Schedule application primitives over the accepted CP6 placement model."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_material_state_ref,
    new_scoped_record_ref,
)
from dante.platform.time import normalize_utc_instant, resolve_local_time, validate_iana_timezone


class ScheduleInputError(ValueError):
    """The requested Schedule placement is outside the activated B02 contract."""


class ScheduleOperationIdReuseError(RuntimeError):
    """One Schedule operation id was reused for materially different intent."""


class ScheduleNotFoundError(LookupError):
    """The Schedule is absent or outside the authenticated self scope."""


class ScheduleRevisionConflictError(RuntimeError):
    """The expected placement state is no longer the Schedule current state."""


class ScheduleUnscheduleConflictError(RuntimeError):
    """The expected placement is no longer current for unschedule."""


class ScheduleUndoConflictError(RuntimeError):
    """The exact Schedule effect targeted by Undo is no longer current."""


class SchedulePersistenceError(RuntimeError):
    """Canonical Schedule persistence could not complete safely."""


CoarseLocalPeriod = Literal["morning", "afternoon", "evening"]
LocalTimeDisambiguation = Literal["reject", "earlier", "later"]


@dataclass(frozen=True, slots=True)
class DateSpanPlacement:
    """Finite half-open civil-date placement; never an inferred 24-hour interval."""

    start_date: date
    end_date_exclusive: date

    def __post_init__(self) -> None:
        if self.end_date_exclusive <= self.start_date:
            raise ScheduleInputError("Schedule date-span end must be after its start.")


@dataclass(frozen=True, slots=True)
class FloatingLocalIntervalPlacement:
    """Offset-free local wall-clock interval with no canonical timezone."""

    starts_local_at: datetime
    ends_local_at: datetime

    def __post_init__(self) -> None:
        if self.starts_local_at.tzinfo is not None or self.ends_local_at.tzinfo is not None:
            raise ScheduleInputError(
                "Floating-local Schedule timestamps must not contain a timezone offset."
            )
        if self.ends_local_at <= self.starts_local_at:
            raise ScheduleInputError("Schedule end must be after Schedule start.")


@dataclass(frozen=True, slots=True)
class NamedZoneLocalIntervalPlacement:
    """Local wall-clock intent plus IANA frame and retained resolved instants."""

    starts_local_at: datetime
    ends_local_at: datetime
    zone_id: str
    # Acceptance policy participates in operation fingerprints, while canonical
    # material equality is carried by local values, zone, and resolved instants.
    disambiguation: LocalTimeDisambiguation = field(default="reject", compare=False)
    resolved_start_at: datetime | None = None
    resolved_end_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.starts_local_at.tzinfo is not None or self.ends_local_at.tzinfo is not None:
            raise ScheduleInputError(
                "Named-zone Schedule local timestamps must not contain an offset."
            )
        if self.ends_local_at <= self.starts_local_at:
            raise ScheduleInputError("Schedule end must be after Schedule start.")
        if self.disambiguation not in {"reject", "earlier", "later"}:
            raise ScheduleInputError("Named-zone disambiguation policy is not supported.")
        try:
            validate_iana_timezone(self.zone_id)
        except ValueError as exc:
            raise ScheduleInputError(str(exc)) from exc
        resolved_start = self.resolved_start_at
        resolved_end = self.resolved_end_at
        if (resolved_start is None) is not (resolved_end is None):
            raise ScheduleInputError(
                "Named-zone Schedule resolution must contain both interval boundaries."
            )
        if resolved_start is None:
            try:
                resolved_start = resolve_local_time(
                    self.starts_local_at,
                    self.zone_id,
                    disambiguation=self.disambiguation,
                )
                resolved_end = resolve_local_time(
                    self.ends_local_at,
                    self.zone_id,
                    disambiguation=self.disambiguation,
                )
            except ValueError as exc:
                raise ScheduleInputError(str(exc)) from exc
        else:
            resolved_start = normalize_utc_instant(resolved_start)
            resolved_end = normalize_utc_instant(cast(datetime, resolved_end))
            if resolved_start not in _accepted_named_zone_resolutions(
                self.starts_local_at,
                self.zone_id,
            ) or resolved_end not in _accepted_named_zone_resolutions(
                self.ends_local_at,
                self.zone_id,
            ):
                raise ScheduleInputError(
                    "Named-zone resolved instants must match an accepted explicit "
                    "resolution of the stored local values."
                )
        if resolved_end <= resolved_start:
            raise ScheduleInputError(
                "Named-zone resolved Schedule end must be after its resolved start."
            )
        object.__setattr__(self, "resolved_start_at", resolved_start)
        object.__setattr__(self, "resolved_end_at", resolved_end)


def _accepted_named_zone_resolutions(local: datetime, zone_id: str) -> frozenset[datetime]:
    """Return the exact earlier/later candidates, including both sides of a DST gap."""
    return frozenset(
        {
            resolve_local_time(local, zone_id, disambiguation="earlier"),
            resolve_local_time(local, zone_id, disambiguation="later"),
        }
    )


@dataclass(frozen=True, slots=True)
class AbsoluteIntervalPlacement:
    """Globally fixed instant interval normalized to UTC."""

    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        try:
            starts_at = normalize_utc_instant(self.starts_at)
            ends_at = normalize_utc_instant(self.ends_at)
        except ValueError as exc:
            raise ScheduleInputError(str(exc)) from exc
        if ends_at <= starts_at:
            raise ScheduleInputError("Absolute Schedule end must be after Schedule start.")
        object.__setattr__(self, "starts_at", starts_at)
        object.__setattr__(self, "ends_at", ends_at)


@dataclass(frozen=True, slots=True)
class CoarseLocalPeriodPlacement:
    """Civil date plus named coarse period without invented clock boundaries."""

    local_date: date
    period: CoarseLocalPeriod

    def __post_init__(self) -> None:
        if self.period not in {"morning", "afternoon", "evening"}:
            raise ScheduleInputError("Coarse local Schedule period is not supported.")


type SchedulePlacement = (
    DateSpanPlacement
    | FloatingLocalIntervalPlacement
    | NamedZoneLocalIntervalPlacement
    | AbsoluteIntervalPlacement
    | CoarseLocalPeriodPlacement
)


@dataclass(frozen=True, slots=True)
class EstablishedScheduleView:
    """Canonical accepted Schedule identity plus its current placement state."""

    subject_native_ref: NativeRef
    schedule_ref: ScopedRecordRef
    material_state_ref: MaterialStateRef
    placement: SchedulePlacement
    created_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RevisedScheduleView:
    """One immutable placement revision and its previous accepted basis."""

    schedule_ref: ScopedRecordRef
    previous_material_state_ref: MaterialStateRef
    material_state_ref: MaterialStateRef
    placement: SchedulePlacement
    created_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class UnscheduledScheduleView:
    """Accepted withdrawal of one exact current Schedule placement."""

    schedule_ref: ScopedRecordRef
    previous_material_state_ref: MaterialStateRef
    unschedule_operation_id: str
    created_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RestoredScheduleView:
    """New monotonic placement created by guarded Undo of unschedule."""

    schedule_ref: ScopedRecordRef
    restored_from_material_state_ref: MaterialStateRef
    material_state_ref: MaterialStateRef
    placement: SchedulePlacement
    created_at: datetime
    replayed: bool


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ScheduleInputError("Schedule operation id must contain 1 to 200 characters.")
    return normalized


def _placement_payload(placement: SchedulePlacement) -> dict[str, str]:
    if isinstance(placement, DateSpanPlacement):
        return {
            "kind": "date_span",
            "start_date": placement.start_date.isoformat(),
            "end_date_exclusive": placement.end_date_exclusive.isoformat(),
        }
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return {
            "kind": "floating_local_interval",
            "starts_local_at": placement.starts_local_at.isoformat(timespec="microseconds"),
            "ends_local_at": placement.ends_local_at.isoformat(timespec="microseconds"),
        }
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        resolved_start_at = cast(datetime, placement.resolved_start_at)
        resolved_end_at = cast(datetime, placement.resolved_end_at)
        return {
            "kind": "named_zone_local_interval",
            "starts_local_at": placement.starts_local_at.isoformat(timespec="microseconds"),
            "ends_local_at": placement.ends_local_at.isoformat(timespec="microseconds"),
            "zone_id": placement.zone_id,
            "resolved_start_at": resolved_start_at.isoformat(timespec="microseconds"),
            "resolved_end_at": resolved_end_at.isoformat(timespec="microseconds"),
        }
    if isinstance(placement, AbsoluteIntervalPlacement):
        return {
            "kind": "absolute_interval",
            "starts_at": placement.starts_at.isoformat(timespec="microseconds"),
            "ends_at": placement.ends_at.isoformat(timespec="microseconds"),
        }
    return {
        "kind": "coarse_local_period",
        "local_date": placement.local_date.isoformat(),
        "period": placement.period,
    }


def _fingerprint_payload(placement: SchedulePlacement) -> dict[str, str]:
    if isinstance(placement, FloatingLocalIntervalPlacement):
        return {
            "extent": "interval",
            "form": "floating_local",
            "starts_local_at": placement.starts_local_at.isoformat(timespec="microseconds"),
            "ends_local_at": placement.ends_local_at.isoformat(timespec="microseconds"),
        }
    payload = _placement_payload(placement)
    if isinstance(placement, NamedZoneLocalIntervalPlacement):
        payload["disambiguation"] = placement.disambiguation
    return payload


def _hash(payload: Mapping[str, str]) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _placement_fingerprint(
    *,
    subject_native_ref: NativeRef,
    placement: SchedulePlacement,
) -> str:
    return _hash(
        {
            "subject_native_ref": str(subject_native_ref),
            **_fingerprint_payload(placement),
        }
    )


def _revision_fingerprint(
    *,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
    placement: SchedulePlacement,
) -> str:
    return _hash(
        {
            "schedule_ref": str(schedule_ref),
            "expected_material_state_ref": str(expected_material_state_ref),
            **_fingerprint_payload(placement),
        }
    )


def _unschedule_fingerprint(
    *,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
) -> str:
    return _hash(
        {
            "schedule_ref": str(schedule_ref),
            "expected_material_state_ref": str(expected_material_state_ref),
            "effect": "no-current-placement",
        }
    )


def _unschedule_undo_fingerprint(
    *,
    schedule_ref: ScopedRecordRef,
    unschedule_operation_id: str,
) -> str:
    return _hash(
        {
            "schedule_ref": str(schedule_ref),
            "unschedule_operation_id": unschedule_operation_id,
            "effect": "restore-prior-placement",
        }
    )


def _placement_from_payload(payload: Mapping[str, object]) -> SchedulePlacement:
    kind = payload.get("kind")
    if kind == "date_span":
        return DateSpanPlacement(
            start_date=date.fromisoformat(str(payload["start_date"])),
            end_date_exclusive=date.fromisoformat(str(payload["end_date_exclusive"])),
        )
    if kind == "floating_local_interval":
        return FloatingLocalIntervalPlacement(
            starts_local_at=datetime.fromisoformat(str(payload["starts_local_at"])),
            ends_local_at=datetime.fromisoformat(str(payload["ends_local_at"])),
        )
    if kind == "named_zone_local_interval":
        return NamedZoneLocalIntervalPlacement(
            starts_local_at=datetime.fromisoformat(str(payload["starts_local_at"])),
            ends_local_at=datetime.fromisoformat(str(payload["ends_local_at"])),
            zone_id=str(payload["zone_id"]),
            resolved_start_at=datetime.fromisoformat(str(payload["resolved_start_at"])),
            resolved_end_at=datetime.fromisoformat(str(payload["resolved_end_at"])),
        )
    if kind == "absolute_interval":
        return AbsoluteIntervalPlacement(
            starts_at=datetime.fromisoformat(str(payload["starts_at"])),
            ends_at=datetime.fromisoformat(str(payload["ends_at"])),
        )
    if kind == "coarse_local_period":
        period = str(payload["period"])
        if period not in {"morning", "afternoon", "evening"}:
            raise ScheduleInputError("Stored coarse Schedule period is unsupported.")
        return CoarseLocalPeriodPlacement(
            local_date=date.fromisoformat(str(payload["local_date"])),
            period=cast(CoarseLocalPeriod, period),
        )
    raise ScheduleInputError("Stored Schedule placement form is unsupported.")


def _constraint_name(exc: IntegrityError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


async def establish_schedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    subject_native_ref: NativeRef,
    placement: SchedulePlacement,
) -> EstablishedScheduleView:
    """Establish one accepted typed Schedule inside the caller-owned transaction."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    schedule_ref = new_scoped_record_ref()
    material_state_ref = new_material_state_ref()
    payload = _placement_payload(placement)
    row = (
        (
            await database_session.execute(
                text(
                    """
                SELECT subject_native_ref,
                       schedule_ref,
                       material_state_ref,
                       created_at,
                       replayed
                  FROM dante.establish_self_schedule_placement(
                       :self_person_ref,
                       :operation_id,
                       :intent_fingerprint,
                       :subject_native_ref,
                       :schedule_ref,
                       :material_state_ref,
                       CAST(:placement_payload AS jsonb)
                  )
                """
                ),
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": _placement_fingerprint(
                        subject_native_ref=subject_native_ref,
                        placement=placement,
                    ),
                    "subject_native_ref": subject_native_ref,
                    "schedule_ref": schedule_ref,
                    "material_state_ref": material_state_ref,
                    "placement_payload": json.dumps(payload, separators=(",", ":"), sort_keys=True),
                },
            )
        )
        .mappings()
        .one()
    )
    return EstablishedScheduleView(
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        placement=placement,
        created_at=row["created_at"],
        replayed=bool(row["replayed"]),
    )


async def establish_floating_schedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    subject_native_ref: NativeRef,
    placement: FloatingLocalIntervalPlacement,
) -> EstablishedScheduleView:
    """Compatibility wrapper for the proven B02-A/B floating-local path."""
    return await establish_schedule_in_session(
        database_session,
        self_person_ref=self_person_ref,
        operation_id=operation_id,
        subject_native_ref=subject_native_ref,
        placement=placement,
    )


async def revise_schedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
    placement: SchedulePlacement,
) -> RevisedScheduleView:
    """Create one new typed placement MaterialState in the caller transaction."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    material_state_ref = new_material_state_ref()
    payload = _placement_payload(placement)
    row = (
        (
            await database_session.execute(
                text(
                    """
                SELECT schedule_ref,
                       previous_material_state_ref,
                       material_state_ref,
                       created_at,
                       replayed
                  FROM dante.revise_self_schedule_placement(
                       :self_person_ref,
                       :operation_id,
                       :intent_fingerprint,
                       :schedule_ref,
                       :expected_material_state_ref,
                       :material_state_ref,
                       CAST(:placement_payload AS jsonb)
                  )
                """
                ),
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": _revision_fingerprint(
                        schedule_ref=schedule_ref,
                        expected_material_state_ref=expected_material_state_ref,
                        placement=placement,
                    ),
                    "schedule_ref": schedule_ref,
                    "expected_material_state_ref": expected_material_state_ref,
                    "material_state_ref": material_state_ref,
                    "placement_payload": json.dumps(payload, separators=(",", ":"), sort_keys=True),
                },
            )
        )
        .mappings()
        .one()
    )
    return RevisedScheduleView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        previous_material_state_ref=MaterialStateRef(UUID(str(row["previous_material_state_ref"]))),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        placement=placement,
        created_at=row["created_at"],
        replayed=bool(row["replayed"]),
    )


async def revise_floating_schedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
    placement: FloatingLocalIntervalPlacement,
) -> RevisedScheduleView:
    """Compatibility wrapper for the proven B02-C floating-local path."""
    return await revise_schedule_in_session(
        database_session,
        self_person_ref=self_person_ref,
        operation_id=operation_id,
        schedule_ref=schedule_ref,
        expected_material_state_ref=expected_material_state_ref,
        placement=placement,
    )


async def unschedule_schedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
) -> UnscheduledScheduleView:
    """Withdraw one exact current placement inside the caller transaction."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    row = (
        (
            await database_session.execute(
                text(
                    """
                SELECT schedule_ref,
                       previous_material_state_ref,
                       unschedule_operation_id,
                       created_at,
                       replayed
                  FROM dante.unschedule_self_schedule(
                       :self_person_ref,
                       :operation_id,
                       :intent_fingerprint,
                       :schedule_ref,
                       :expected_material_state_ref
                  )
                """
                ),
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": _unschedule_fingerprint(
                        schedule_ref=schedule_ref,
                        expected_material_state_ref=expected_material_state_ref,
                    ),
                    "schedule_ref": schedule_ref,
                    "expected_material_state_ref": expected_material_state_ref,
                },
            )
        )
        .mappings()
        .one()
    )
    return UnscheduledScheduleView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        previous_material_state_ref=MaterialStateRef(UUID(str(row["previous_material_state_ref"]))),
        unschedule_operation_id=str(row["unschedule_operation_id"]),
        created_at=row["created_at"],
        replayed=bool(row["replayed"]),
    )


async def undo_schedule_unschedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    schedule_ref: ScopedRecordRef,
    unschedule_operation_id: str,
) -> RestoredScheduleView:
    """Restore any activated prior placement as a new monotonic state."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    normalized_unschedule_operation_id = _normalize_operation_id(unschedule_operation_id)
    material_state_ref = new_material_state_ref()
    row = (
        (
            await database_session.execute(
                text(
                    """
                SELECT schedule_ref,
                       restored_from_material_state_ref,
                       material_state_ref,
                       placement_payload,
                       created_at,
                       replayed
                  FROM dante.undo_self_schedule_unschedule_any(
                       :self_person_ref,
                       :operation_id,
                       :intent_fingerprint,
                       :schedule_ref,
                       :unschedule_operation_id,
                       :material_state_ref
                  )
                """
                ),
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": _unschedule_undo_fingerprint(
                        schedule_ref=schedule_ref,
                        unschedule_operation_id=normalized_unschedule_operation_id,
                    ),
                    "schedule_ref": schedule_ref,
                    "unschedule_operation_id": normalized_unschedule_operation_id,
                    "material_state_ref": material_state_ref,
                },
            )
        )
        .mappings()
        .one()
    )
    placement_payload = row["placement_payload"]
    if not isinstance(placement_payload, Mapping):
        raise SchedulePersistenceError("Schedule Undo returned an invalid placement payload.")
    return RestoredScheduleView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        restored_from_material_state_ref=MaterialStateRef(
            UUID(str(row["restored_from_material_state_ref"]))
        ),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        placement=_placement_from_payload(placement_payload),
        created_at=row["created_at"],
        replayed=bool(row["replayed"]),
    )


class TemporalScheduleApplication:
    """Transaction-owning Schedule mutation operations."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def establish_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_native_ref: NativeRef,
        placement: SchedulePlacement,
    ) -> EstablishedScheduleView:
        """Establish shared Schedule truth for an existing self-owned subject."""
        if subject_native_ref.version != 7:
            raise ScheduleInputError("Schedule subject reference must be a canonical UUIDv7 value.")
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await establish_schedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    subject_native_ref=subject_native_ref,
                    placement=placement,
                )
        except IntegrityError as exc:
            constraint = _constraint_name(exc)
            if constraint == "pk_schedule_establish_operation":
                raise ScheduleOperationIdReuseError() from exc
            if constraint == "schedule_establish_subject_not_found":
                raise ScheduleNotFoundError() from exc
            raise SchedulePersistenceError() from exc
        except DBAPIError as exc:
            raise SchedulePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise SchedulePersistenceError() from exc

    async def revise_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
        placement: SchedulePlacement,
    ) -> RevisedScheduleView:
        if schedule_ref.version != 7 or expected_material_state_ref.version != 7:
            raise ScheduleInputError(
                "Schedule and expected placement references must be canonical UUIDv7 values."
            )
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await revise_schedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    schedule_ref=schedule_ref,
                    expected_material_state_ref=expected_material_state_ref,
                    placement=placement,
                )
        except IntegrityError as exc:
            constraint = _constraint_name(exc)
            if constraint == "pk_schedule_revision_operation":
                raise ScheduleOperationIdReuseError() from exc
            if constraint == "schedule_revision_expected_state":
                raise ScheduleRevisionConflictError() from exc
            if constraint == "schedule_revision_schedule_not_found":
                raise ScheduleNotFoundError() from exc
            raise SchedulePersistenceError() from exc
        except DBAPIError as exc:
            raise SchedulePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise SchedulePersistenceError() from exc

    async def revise_floating_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
        placement: FloatingLocalIntervalPlacement,
    ) -> RevisedScheduleView:
        return await self.revise_schedule(
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            schedule_ref=schedule_ref,
            expected_material_state_ref=expected_material_state_ref,
            placement=placement,
        )

    async def unschedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> UnscheduledScheduleView:
        if schedule_ref.version != 7 or expected_material_state_ref.version != 7:
            raise ScheduleInputError(
                "Schedule and expected placement references must be canonical UUIDv7 values."
            )
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await unschedule_schedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    schedule_ref=schedule_ref,
                    expected_material_state_ref=expected_material_state_ref,
                )
        except IntegrityError as exc:
            constraint = _constraint_name(exc)
            if constraint == "pk_schedule_unschedule_operation":
                raise ScheduleOperationIdReuseError() from exc
            if constraint == "schedule_unschedule_expected_state":
                raise ScheduleUnscheduleConflictError() from exc
            if constraint == "schedule_unschedule_schedule_not_found":
                raise ScheduleNotFoundError() from exc
            raise SchedulePersistenceError() from exc
        except DBAPIError as exc:
            raise SchedulePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise SchedulePersistenceError() from exc

    async def undo_unschedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        unschedule_operation_id: str,
    ) -> RestoredScheduleView:
        if schedule_ref.version != 7:
            raise ScheduleInputError("Schedule reference must be a canonical UUIDv7 value.")
        try:
            async with self._session_factory() as database_session, database_session.begin():
                return await undo_schedule_unschedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=operation_id,
                    schedule_ref=schedule_ref,
                    unschedule_operation_id=unschedule_operation_id,
                )
        except IntegrityError as exc:
            constraint = _constraint_name(exc)
            if constraint == "pk_schedule_unschedule_undo_operation":
                raise ScheduleOperationIdReuseError() from exc
            if constraint == "schedule_unschedule_undo_expected_state":
                raise ScheduleUndoConflictError() from exc
            if constraint == "schedule_unschedule_undo_not_found":
                raise ScheduleNotFoundError() from exc
            if constraint == "schedule_unschedule_undo_unsupported_form":
                raise ScheduleInputError(
                    "The prior Schedule placement form is not activated for Undo."
                ) from exc
            raise SchedulePersistenceError() from exc
        except DBAPIError as exc:
            raise SchedulePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise SchedulePersistenceError() from exc
