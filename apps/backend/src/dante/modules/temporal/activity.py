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
    establish_floating_schedule_in_session,
)
from dante.platform.database.mappings.activity import ActivityIntentionRow
from dante.platform.database.mappings.schedule import ScheduleRow
from dante.platform.database.references import NativeRef, new_native_ref


class ActivityInputError(ValueError):
    """The requested Activity cannot be admitted by the activated contract."""


class ActivityOperationIdReuseError(RuntimeError):
    """One operation id was reused for a different canonical Activity intent."""


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
        """Create Activity and first accepted Schedule atomically for the B02-A form subset."""
        normalized_title = _normalize_title(title)
        normalized_operation_id = _normalize_operation_id(operation_id)
        if placement.starts_local_at.date() != placement.ends_local_at.date():
            raise ActivityInputError(
                "B02-A currently activates only same-local-day floating Schedule intervals."
            )
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

                schedule_result = await establish_floating_schedule_in_session(
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

    async def list_unplaced(
        self,
        *,
        self_person_ref: NativeRef,
    ) -> tuple[ActivityView, ...]:
        statement = (
            select(ActivityIntentionRow)
            .outerjoin(
                ScheduleRow,
                ScheduleRow.subject_native_ref == ActivityIntentionRow.activity_ref,
            )
            .where(
                ActivityIntentionRow.self_person_ref == self_person_ref,
                ScheduleRow.schedule_ref.is_(None),
            )
            .order_by(
                ActivityIntentionRow.created_at,
                ActivityIntentionRow.activity_ref,
            )
        )

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                rows = (await database_session.scalars(statement)).all()
        except SQLAlchemyError as exc:
            raise ActivityPersistenceError() from exc

        return tuple(
            ActivityView(
                activity_ref=row.activity_ref,
                title=row.title,
                created_at=row.created_at,
            )
            for row in rows
        )

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
