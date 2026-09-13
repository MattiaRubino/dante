"""B02 Schedule application primitives over the accepted CP6 placement model."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
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


class ScheduleInputError(ValueError):
    """The requested Schedule placement is outside the activated B02 contract."""


class ScheduleOperationIdReuseError(RuntimeError):
    """One Schedule operation id was reused for materially different intent."""


class ScheduleNotFoundError(LookupError):
    """The Schedule is absent or outside the authenticated self scope."""


class ScheduleRevisionConflictError(RuntimeError):
    """The expected placement state is no longer the Schedule current state."""


class SchedulePersistenceError(RuntimeError):
    """Canonical Schedule persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class FloatingLocalIntervalPlacement:
    """Lossless floating-local interval accepted by the first B02 slice."""

    starts_local_at: datetime
    ends_local_at: datetime

    def __post_init__(self) -> None:
        if (
            self.starts_local_at.tzinfo is not None
            or self.ends_local_at.tzinfo is not None
        ):
            raise ScheduleInputError(
                "Floating-local Schedule timestamps must not contain a timezone offset."
            )
        if self.ends_local_at <= self.starts_local_at:
            raise ScheduleInputError("Schedule end must be after Schedule start.")


@dataclass(frozen=True, slots=True)
class EstablishedScheduleView:
    """Canonical accepted Schedule identity plus its current placement state."""

    subject_native_ref: NativeRef
    schedule_ref: ScopedRecordRef
    material_state_ref: MaterialStateRef
    placement: FloatingLocalIntervalPlacement
    created_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RevisedScheduleView:
    """One immutable placement revision and its previous accepted basis."""

    schedule_ref: ScopedRecordRef
    previous_material_state_ref: MaterialStateRef
    material_state_ref: MaterialStateRef
    placement: FloatingLocalIntervalPlacement
    created_at: datetime
    replayed: bool


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ScheduleInputError(
            "Schedule operation id must contain 1 to 200 characters."
        )
    return normalized


def _placement_fingerprint(
    *,
    subject_native_ref: NativeRef,
    placement: FloatingLocalIntervalPlacement,
) -> str:
    payload = json.dumps(
        {
            "extent": "interval",
            "form": "floating_local",
            "subject_native_ref": str(subject_native_ref),
            "starts_local_at": placement.starts_local_at.isoformat(
                timespec="microseconds"
            ),
            "ends_local_at": placement.ends_local_at.isoformat(timespec="microseconds"),
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _revision_fingerprint(
    *,
    schedule_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
    placement: FloatingLocalIntervalPlacement,
) -> str:
    payload = json.dumps(
        {
            "schedule_ref": str(schedule_ref),
            "expected_material_state_ref": str(expected_material_state_ref),
            "extent": "interval",
            "form": "floating_local",
            "starts_local_at": placement.starts_local_at.isoformat(
                timespec="microseconds"
            ),
            "ends_local_at": placement.ends_local_at.isoformat(timespec="microseconds"),
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _constraint_name(exc: IntegrityError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


async def establish_floating_schedule_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    subject_native_ref: NativeRef,
    placement: FloatingLocalIntervalPlacement,
) -> EstablishedScheduleView:
    """Establish one accepted Schedule inside the caller-owned transaction."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    schedule_ref = new_scoped_record_ref()
    material_state_ref = new_material_state_ref()
    fingerprint = _placement_fingerprint(
        subject_native_ref=subject_native_ref,
        placement=placement,
    )

    statement = text(
        """
        SELECT subject_native_ref,
               schedule_ref,
               material_state_ref,
               starts_local_at,
               ends_local_at,
               created_at,
               replayed
        FROM dante.establish_self_floating_schedule(
            :self_person_ref,
            :operation_id,
            :intent_fingerprint,
            :subject_native_ref,
            :schedule_ref,
            :material_state_ref,
            :starts_local_at,
            :ends_local_at
        )
        """
    )

    try:
        row = (
            (
                await database_session.execute(
                    statement,
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": normalized_operation_id,
                        "intent_fingerprint": fingerprint,
                        "subject_native_ref": subject_native_ref,
                        "schedule_ref": schedule_ref,
                        "material_state_ref": material_state_ref,
                        "starts_local_at": placement.starts_local_at,
                        "ends_local_at": placement.ends_local_at,
                    },
                )
            )
            .mappings()
            .one()
        )
    except IntegrityError as exc:
        if _constraint_name(exc) == "pk_schedule_establish_operation":
            raise ScheduleOperationIdReuseError() from exc
        raise

    return EstablishedScheduleView(
        subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        placement=FloatingLocalIntervalPlacement(
            starts_local_at=row["starts_local_at"],
            ends_local_at=row["ends_local_at"],
        ),
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
    """Create one new placement MaterialState inside the caller-owned transaction."""
    normalized_operation_id = _normalize_operation_id(operation_id)
    material_state_ref = new_material_state_ref()
    fingerprint = _revision_fingerprint(
        schedule_ref=schedule_ref,
        expected_material_state_ref=expected_material_state_ref,
        placement=placement,
    )
    statement = text(
        """
        SELECT schedule_ref,
               previous_material_state_ref,
               material_state_ref,
               starts_local_at,
               ends_local_at,
               created_at,
               replayed
        FROM dante.revise_self_floating_schedule(
            :self_person_ref,
            :operation_id,
            :intent_fingerprint,
            :schedule_ref,
            :expected_material_state_ref,
            :material_state_ref,
            :starts_local_at,
            :ends_local_at
        )
        """
    )
    row = (
        (
            await database_session.execute(
                statement,
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": normalized_operation_id,
                    "intent_fingerprint": fingerprint,
                    "schedule_ref": schedule_ref,
                    "expected_material_state_ref": expected_material_state_ref,
                    "material_state_ref": material_state_ref,
                    "starts_local_at": placement.starts_local_at,
                    "ends_local_at": placement.ends_local_at,
                },
            )
        )
        .mappings()
        .one()
    )
    return RevisedScheduleView(
        schedule_ref=ScopedRecordRef(UUID(str(row["schedule_ref"]))),
        previous_material_state_ref=MaterialStateRef(
            UUID(str(row["previous_material_state_ref"]))
        ),
        material_state_ref=MaterialStateRef(UUID(str(row["material_state_ref"]))),
        placement=FloatingLocalIntervalPlacement(
            starts_local_at=row["starts_local_at"],
            ends_local_at=row["ends_local_at"],
        ),
        created_at=row["created_at"],
        replayed=bool(row["replayed"]),
    )


class TemporalScheduleApplication:
    """Transaction-owning Schedule revision operations."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def revise_floating_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        schedule_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
        placement: FloatingLocalIntervalPlacement,
    ) -> RevisedScheduleView:
        if schedule_ref.version != 7 or expected_material_state_ref.version != 7:
            raise ScheduleInputError(
                "Schedule and expected placement references must be canonical UUIDv7 values."
            )
        if placement.starts_local_at.date() != placement.ends_local_at.date():
            raise ScheduleInputError(
                "B02-C currently activates only same-local-day floating Schedule intervals."
            )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                return await revise_floating_schedule_in_session(
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
