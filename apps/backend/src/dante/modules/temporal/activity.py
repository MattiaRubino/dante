"""B01/B02 Activity application operations over canonical PostgreSQL state."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.schedule import (
    EstablishedScheduleView,
    FloatingLocalIntervalPlacement,
    ScheduleInputError,
    ScheduleOperationIdReuseError,
    SchedulePlacement,
    establish_schedule_in_session,
)
from dante.platform.database.mappings.activity import ActivityIntentionRow
from dante.platform.database.references import NativeRef, new_native_ref


class ActivityInputError(ValueError):
    """The requested Activity cannot be admitted by the activated contract."""


class ActivityOperationIdReuseError(RuntimeError):
    """One operation id was reused for a different canonical Activity intent."""


class ActivityNotFoundError(LookupError):
    """The requested Activity is not visible inside the authenticated self scope."""


class ActivityPersistenceError(RuntimeError):
    """Canonical Activity persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class ActivityView:
    """Application projection of the minimum Activity state."""

    activity_ref: NativeRef
    title: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class CreateActivityResult:
    """Canonical create result, including truthful idempotent replay state."""

    activity: ActivityView
    replayed: bool


@dataclass(frozen=True, slots=True)
class CreateScheduledActivityResult:
    """Atomic Activity + accepted Schedule authoring result for B02-A."""

    activity: ActivityView
    schedule: EstablishedScheduleView
    replayed: bool


def _normalize_title(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 300:
        raise ActivityInputError("Activity title must contain 1 to 300 non-padding characters.")
    return normalized


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ActivityInputError("Activity operation id must contain 1 to 200 characters.")
    return normalized


def _intent_fingerprint(*, title: str) -> str:
    payload = json.dumps(
        {"title": title},
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _constraint_name(exc: IntegrityError) -> str | None:
    original = exc.orig
    diagnostic = getattr(original, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _activity_from_row(row: RowMapping) -> ActivityView:
    return ActivityView(
        activity_ref=NativeRef(UUID(str(row["activity_ref"]))),
        title=str(row["title"]),
        created_at=row["created_at"],
    )


class TemporalActivityApplication:
    """Transaction-owning Activity operations; adapters never commit independently."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _execute_create_activity(
        self,
        database_session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        requested_activity_ref: NativeRef,
    ) -> CreateActivityResult:
        fingerprint = _intent_fingerprint(title=title)
        statement = text(
            """
            SELECT activity_ref, title, created_at, replayed
            FROM dante.create_self_activity(
                :self_person_ref,
                :operation_id,
                :intent_fingerprint,
                :activity_ref,
                :title
            )
            """
        )
        row = (
            (
                await database_session.execute(
                    statement,
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": operation_id,
                        "intent_fingerprint": fingerprint,
                        "activity_ref": requested_activity_ref,
                        "title": title,
                    },
                )
            )
            .mappings()
            .one()
        )
        return CreateActivityResult(
            activity=_activity_from_row(row),
            replayed=bool(row["replayed"]),
        )

    async def create_activity(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
    ) -> CreateActivityResult:
        normalized_title = _normalize_title(title)
        normalized_operation_id = _normalize_operation_id(operation_id)
        activity_ref = new_native_ref()

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                return await self._execute_create_activity(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=normalized_title,
                    requested_activity_ref=activity_ref,
                )
        except IntegrityError as exc:
            if _constraint_name(exc) == "pk_activity_create_operation":
                raise ActivityOperationIdReuseError() from exc
            raise ActivityPersistenceError() from exc
        except DBAPIError as exc:
            raise ActivityPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise ActivityPersistenceError() from exc

    async def create_activity_with_floating_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        placement: FloatingLocalIntervalPlacement,
    ) -> CreateScheduledActivityResult:
        """Compatibility wrapper for the proven B02-A floating-local path."""
        return await self.create_activity_with_schedule(
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            title=title,
            placement=placement,
        )

    async def create_activity_with_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        placement: SchedulePlacement,
    ) -> CreateScheduledActivityResult:
        """Create Activity and one typed accepted Schedule atomically."""
        normalized_title = _normalize_title(title)
        normalized_operation_id = _normalize_operation_id(operation_id)
        activity_ref = new_native_ref()

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                activity_result = await self._execute_create_activity(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=normalized_title,
                    requested_activity_ref=activity_ref,
                )

                schedule_result = await establish_schedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    subject_native_ref=activity_result.activity.activity_ref,
                    placement=placement,
                )
                if activity_result.replayed is not schedule_result.replayed:
                    raise ActivityPersistenceError(
                        "Activity and Schedule operation receipts diverged."
                    )

                return CreateScheduledActivityResult(
                    activity=activity_result.activity,
                    schedule=schedule_result,
                    replayed=activity_result.replayed,
                )
        except ActivityOperationIdReuseError:
            raise
        except ScheduleOperationIdReuseError as exc:
            raise ActivityOperationIdReuseError() from exc
        except ScheduleInputError as exc:
            raise ActivityInputError(str(exc)) from exc
        except IntegrityError as exc:
            if _constraint_name(exc) in {
                "pk_activity_create_operation",
                "pk_schedule_establish_operation",
            }:
                raise ActivityOperationIdReuseError() from exc
            raise ActivityPersistenceError() from exc
        except DBAPIError as exc:
            raise ActivityPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise ActivityPersistenceError() from exc

    async def schedule_existing_activity(
        self,
        *,
        self_person_ref: NativeRef,
        activity_ref: NativeRef,
        operation_id: str,
        placement: FloatingLocalIntervalPlacement,
    ) -> CreateScheduledActivityResult:
        """Compatibility wrapper for the proven B02-B floating-local path."""
        return await self.schedule_existing_activity_with_placement(
            self_person_ref=self_person_ref,
            activity_ref=activity_ref,
            operation_id=operation_id,
            placement=placement,
        )

    async def schedule_existing_activity_with_placement(
        self,
        *,
        self_person_ref: NativeRef,
        activity_ref: NativeRef,
        operation_id: str,
        placement: SchedulePlacement,
    ) -> CreateScheduledActivityResult:
        """Attach one typed accepted Schedule without cloning the Activity."""
        normalized_operation_id = _normalize_operation_id(operation_id)

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                activity_row = await database_session.scalar(
                    select(ActivityIntentionRow).where(
                        ActivityIntentionRow.activity_ref == activity_ref,
                        ActivityIntentionRow.self_person_ref == self_person_ref,
                    )
                )
                if activity_row is None:
                    raise ActivityNotFoundError()

                activity = ActivityView(
                    activity_ref=activity_row.activity_ref,
                    title=activity_row.title,
                    created_at=activity_row.created_at,
                )
                schedule = await establish_schedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    subject_native_ref=activity.activity_ref,
                    placement=placement,
                )
                return CreateScheduledActivityResult(
                    activity=activity,
                    schedule=schedule,
                    replayed=schedule.replayed,
                )
        except ActivityNotFoundError:
            raise
        except ScheduleOperationIdReuseError as exc:
            raise ActivityOperationIdReuseError() from exc
        except ScheduleInputError as exc:
            raise ActivityInputError(str(exc)) from exc
        except IntegrityError as exc:
            if _constraint_name(exc) == "pk_schedule_establish_operation":
                raise ActivityOperationIdReuseError() from exc
            raise ActivityPersistenceError() from exc
        except DBAPIError as exc:
            raise ActivityPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise ActivityPersistenceError() from exc

    async def list_unplaced(
        self,
        *,
        self_person_ref: NativeRef,
    ) -> tuple[ActivityView, ...]:
        statement = text(
            """
            SELECT intention.activity_ref,
                   intention.title,
                   intention.created_at
            FROM dante.activity_intention AS intention
            WHERE intention.self_person_ref = :self_person_ref
              AND NOT EXISTS (
                  SELECT 1
                  FROM dante.schedule AS schedule
                  JOIN dante.schedule_current_placement AS current
                    ON current.scoped_owner_ref = schedule.schedule_ref
                  WHERE schedule.subject_native_ref = intention.activity_ref
              )
            ORDER BY intention.created_at, intention.activity_ref
            """
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                rows = (
                    (
                        await database_session.execute(
                            statement,
                            {"self_person_ref": self_person_ref},
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise ActivityPersistenceError() from exc

        return tuple(_activity_from_row(row) for row in rows)

    async def get_activity(
        self,
        *,
        self_person_ref: NativeRef,
        activity_ref: NativeRef,
    ) -> ActivityView | None:
        statement = select(ActivityIntentionRow).where(
            ActivityIntentionRow.activity_ref == activity_ref,
            ActivityIntentionRow.self_person_ref == self_person_ref,
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = await database_session.scalar(statement)
        except SQLAlchemyError as exc:
            raise ActivityPersistenceError() from exc

        if row is None:
            return None
        return ActivityView(
            activity_ref=row.activity_ref,
            title=row.title,
            created_at=row.created_at,
        )
