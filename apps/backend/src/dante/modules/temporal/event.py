"""B03 Event application operations over canonical PostgreSQL state."""

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
    ScheduleInputError,
    SchedulePlacement,
    establish_schedule_in_session,
)
from dante.platform.database.mappings.event import (
    EventAgendaCurrentRow,
    EventAgendaPartRow,
    EventExpectationRow,
)
from dante.platform.database.references import NativeRef, new_native_ref


class EventInputError(ValueError):
    """The requested Event cannot be admitted by the activated B03 contract."""


class EventOperationIdReuseError(RuntimeError):
    """One operation id was reused for a different canonical Event intent."""


class EventAgendaRevisionConflictError(RuntimeError):
    """An Event Agenda mutation was based on stale canonical Agenda truth."""


class EventNotFoundError(LookupError):
    """The requested Event is not visible inside the authenticated self scope."""


class EventPersistenceError(RuntimeError):
    """Canonical Event persistence could not complete safely."""


class EventLifeAreaUnavailableError(RuntimeError):
    """The requested actor-local Life Area is unavailable for Event creation."""


@dataclass(frozen=True, slots=True)
class EventView:
    """Application projection of the accepted Event expectation state."""

    event_ref: NativeRef
    title: str
    agenda_revision: int
    agenda_parts: tuple[str, ...]
    created_at: datetime
    life_area_ref: UUID | None = None
    life_area_assignment_revision: int | None = None


@dataclass(frozen=True, slots=True)
class CreateEventResult:
    """Canonical create result, including truthful idempotent replay state."""

    event: EventView
    replayed: bool


@dataclass(frozen=True, slots=True)
class CreateScheduledEventResult:
    """Atomic Event expectation plus accepted shared Schedule."""

    event: EventView
    schedule: EstablishedScheduleView
    replayed: bool


@dataclass(frozen=True, slots=True)
class ReplaceEventAgendaResult:
    """Accepted whole-Agenda replacement at one aggregate CAS revision."""

    event_ref: NativeRef
    agenda_revision: int
    agenda_parts: tuple[str, ...]
    replayed: bool


def _normalize_title(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 300:
        raise EventInputError("Event title must contain 1 to 300 non-padding characters.")
    return normalized


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise EventInputError("Event operation id must contain 1 to 200 characters.")
    return normalized


def _normalize_agenda_parts(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    if len(values) > 100:
        raise EventInputError("Event Agenda may contain at most 100 parts.")
    normalized: list[str] = []
    for value in values:
        part = value.strip()
        if not part or len(part) > 1000:
            raise EventInputError(
                "Event Agenda parts must contain 1 to 1000 non-padding characters."
            )
        normalized.append(part)
    return tuple(normalized)


def _intent_fingerprint(*, title: str, agenda_parts: tuple[str, ...], life_area_ref: UUID) -> str:
    """Bind Event identity creation to its required primary Life Area."""
    intent: dict[str, object] = {"version": 2, "title": title, "life_area_ref": str(life_area_ref)}
    if agenda_parts:
        intent["agenda_parts"] = list(agenda_parts)
    payload = json.dumps(
        intent,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _agenda_mutation_fingerprint(
    *,
    event_ref: NativeRef,
    expected_revision: int,
    agenda_parts: tuple[str, ...],
) -> str:
    payload = json.dumps(
        {
            "agenda_parts": list(agenda_parts),
            "event_ref": str(event_ref),
            "expected_revision": expected_revision,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _schedule_operation_id(event_operation_id: str) -> str:
    """Derive a stable Schedule command identity without collapsing the two commands."""
    digest = hashlib.sha256(event_operation_id.encode("utf-8")).hexdigest()
    return f"event-create-schedule:{digest}"


def _constraint_name(exc: DBAPIError) -> str | None:
    original = exc.orig
    diagnostic = getattr(original, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _event_from_row(row: RowMapping) -> EventView:
    raw_agenda = row.get("agenda_parts")
    agenda_parts = () if raw_agenda is None else tuple(str(part) for part in raw_agenda)
    return EventView(
        event_ref=NativeRef(UUID(str(row["event_ref"]))),
        title=str(row["title"]),
        agenda_revision=int(row.get("agenda_revision") or 0),
        agenda_parts=agenda_parts,
        created_at=row["created_at"],
        life_area_ref=(
            UUID(str(row["life_area_ref"])) if row.get("life_area_ref") is not None else None
        ),
        life_area_assignment_revision=(
            int(row["assignment_revision"]) if row.get("assignment_revision") is not None else None
        ),
    )


class TemporalEventApplication:
    """Transaction-owning Event operations; adapters never commit independently."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _execute_create_event(
        self,
        database_session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        agenda_parts: tuple[str, ...],
        requested_event_ref: NativeRef,
        life_area_ref: UUID,
    ) -> CreateEventResult:
        fingerprint = _intent_fingerprint(
            title=title, agenda_parts=agenda_parts, life_area_ref=life_area_ref
        )
        statement = text(
            """
            SELECT event_ref, title, created_at, agenda_revision, agenda_parts,
                   life_area_ref, assignment_revision, replayed
            FROM dante.create_self_event_with_agenda_in_life_area(
                :self_person_ref,
                :operation_id,
                :intent_fingerprint,
                :event_ref,
                :title,
                :agenda_parts,
                :life_area_ref
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
                        "event_ref": requested_event_ref,
                        "title": title,
                        "agenda_parts": list(agenda_parts),
                        "life_area_ref": life_area_ref,
                    },
                )
            )
            .mappings()
            .one()
        )
        return CreateEventResult(
            event=_event_from_row(row),
            replayed=bool(row["replayed"]),
        )

    async def create_event(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_ref: UUID,
        agenda_parts: tuple[str, ...] | list[str] = (),
    ) -> CreateEventResult:
        """Create one self-owned Event expectation through the bounded DB capability."""
        normalized_title = _normalize_title(title)
        normalized_agenda = _normalize_agenda_parts(agenda_parts)
        normalized_operation_id = _normalize_operation_id(operation_id)
        event_ref = new_native_ref()

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                return await self._execute_create_event(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=normalized_title,
                    agenda_parts=normalized_agenda,
                    requested_event_ref=event_ref,
                    life_area_ref=life_area_ref,
                )
        except IntegrityError as exc:
            if _constraint_name(exc) == "pk_event_create_operation":
                raise EventOperationIdReuseError() from exc
            if _constraint_name(exc) == "life_area_assignment_target_unavailable":
                raise EventLifeAreaUnavailableError() from exc
            raise EventPersistenceError() from exc
        except DBAPIError as exc:
            raise EventPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise EventPersistenceError() from exc

    async def create_event_with_schedule(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_ref: UUID,
        placement: SchedulePlacement,
        agenda_parts: tuple[str, ...] | list[str] = (),
    ) -> CreateScheduledEventResult:
        """Create Event identity/expectation, Agenda and first shared Schedule atomically."""
        normalized_title = _normalize_title(title)
        normalized_agenda = _normalize_agenda_parts(agenda_parts)
        normalized_operation_id = _normalize_operation_id(operation_id)
        event_ref = new_native_ref()
        schedule_operation_id = _schedule_operation_id(normalized_operation_id)

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                event_result = await self._execute_create_event(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=normalized_title,
                    agenda_parts=normalized_agenda,
                    requested_event_ref=event_ref,
                    life_area_ref=life_area_ref,
                )
                schedule_result = await establish_schedule_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=schedule_operation_id,
                    subject_native_ref=event_result.event.event_ref,
                    placement=placement,
                )
                if event_result.replayed is not schedule_result.replayed:
                    raise EventOperationIdReuseError(
                        "Event operation id was reused across incompatible create commands."
                    )
                return CreateScheduledEventResult(
                    event=event_result.event,
                    schedule=schedule_result,
                    replayed=event_result.replayed,
                )
        except EventOperationIdReuseError:
            raise
        except ScheduleInputError as exc:
            raise EventInputError(str(exc)) from exc
        except IntegrityError as exc:
            if _constraint_name(exc) == "life_area_assignment_target_unavailable":
                raise EventLifeAreaUnavailableError() from exc
            if _constraint_name(exc) in {
                "pk_event_create_operation",
                "pk_schedule_establish_operation",
            }:
                raise EventOperationIdReuseError() from exc
            raise EventPersistenceError() from exc
        except DBAPIError as exc:
            raise EventPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise EventPersistenceError() from exc

    async def replace_agenda(
        self,
        *,
        self_person_ref: NativeRef,
        event_ref: NativeRef,
        operation_id: str,
        expected_revision: int,
        agenda_parts: tuple[str, ...] | list[str],
    ) -> ReplaceEventAgendaResult:
        """Atomically replace one Event's ordered Agenda behind aggregate CAS."""
        normalized_operation_id = _normalize_operation_id(operation_id)
        normalized_agenda = _normalize_agenda_parts(agenda_parts)
        if expected_revision < 0:
            raise EventInputError("Event Agenda expected revision must be non-negative.")
        fingerprint = _agenda_mutation_fingerprint(
            event_ref=event_ref,
            expected_revision=expected_revision,
            agenda_parts=normalized_agenda,
        )
        statement = text(
            """
            SELECT event_ref, agenda_revision, agenda_parts, replayed
            FROM dante.replace_self_event_agenda(
                :self_person_ref,
                :operation_id,
                :intent_fingerprint,
                :event_ref,
                :expected_revision,
                :agenda_parts
            )
            """
        )
        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = (
                    (
                        await database_session.execute(
                            statement,
                            {
                                "self_person_ref": self_person_ref,
                                "operation_id": normalized_operation_id,
                                "intent_fingerprint": fingerprint,
                                "event_ref": event_ref,
                                "expected_revision": expected_revision,
                                "agenda_parts": list(normalized_agenda),
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
        except IntegrityError as exc:
            constraint = _constraint_name(exc)
            if constraint == "pk_event_agenda_mutation_operation":
                raise EventOperationIdReuseError() from exc
            if constraint == "event_agenda_revision_conflict":
                raise EventAgendaRevisionConflictError() from exc
            if constraint == "fk_event_agenda_mutation_operation_event_ref_event_expectation":
                raise EventNotFoundError() from exc
            raise EventPersistenceError() from exc
        except DBAPIError as exc:
            raise EventPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise EventPersistenceError() from exc

        raw_agenda = row["agenda_parts"]
        return ReplaceEventAgendaResult(
            event_ref=NativeRef(UUID(str(row["event_ref"]))),
            agenda_revision=int(row["agenda_revision"]),
            agenda_parts=tuple(str(part) for part in raw_agenda),
            replayed=bool(row["replayed"]),
        )

    async def get_event(
        self,
        *,
        self_person_ref: NativeRef,
        event_ref: NativeRef,
    ) -> EventView | None:
        """Read one Event and its ordered Agenda inside authenticated self scope."""
        expectation_statement = select(EventExpectationRow).where(
            EventExpectationRow.event_ref == event_ref,
            EventExpectationRow.self_person_ref == self_person_ref,
        )
        agenda_statement = (
            select(EventAgendaPartRow.content)
            .where(EventAgendaPartRow.event_ref == event_ref)
            .order_by(EventAgendaPartRow.position)
        )
        revision_statement = select(EventAgendaCurrentRow.revision).where(
            EventAgendaCurrentRow.event_ref == event_ref
        )
        assignment_statement = text("""
            SELECT life_area_ref, assignment_revision
              FROM dante.list_self_life_area_assignments(:self_person_ref)
             WHERE subject_kind='event' AND subject_native_ref=:event_ref
        """)

        try:
            async with (
                self._session_factory() as database_session,
                database_session.begin(),
            ):
                row = await database_session.scalar(expectation_statement)
                if row is None:
                    return None
                agenda_parts = tuple((await database_session.scalars(agenda_statement)).all())
                agenda_revision = await database_session.scalar(revision_statement)
                assignment = (
                    (
                        await database_session.execute(
                            assignment_statement,
                            {"self_person_ref": self_person_ref, "event_ref": event_ref},
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
        except SQLAlchemyError as exc:
            raise EventPersistenceError() from exc

        return EventView(
            event_ref=row.event_ref,
            title=row.title,
            agenda_revision=0 if agenda_revision is None else int(agenda_revision),
            agenda_parts=agenda_parts,
            created_at=row.created_at,
            life_area_ref=UUID(str(assignment["life_area_ref"])) if assignment else None,
            life_area_assignment_revision=(
                int(assignment["assignment_revision"]) if assignment else None
            ),
        )
