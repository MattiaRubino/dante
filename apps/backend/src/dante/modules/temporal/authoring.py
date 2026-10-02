"""B14-U2 transactional quick-authoring application.

This module is intentionally separate from the historical B01/B03 create
applications while the public API migrates to the U2 contract.  It owns one
transaction spanning optional Life Area authoring, Activity/Event creation and
an optional accepted Schedule.  PostgreSQL remains the only canonical truth.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.schedule import (
    EstablishedScheduleView,
    ScheduleInputError,
    ScheduleOperationIdReuseError,
    SchedulePlacement,
    establish_schedule_in_session,
)
from dante.platform.database.references import NativeRef, new_native_ref


class TemporalAuthoringInputError(ValueError):
    """The quick-authoring intent is invalid before persistence."""


class TemporalAuthoringOperationIdReuseError(RuntimeError):
    """One operation id was reused for a different authoring intent."""


class TemporalAuthoringLifeAreaUnavailableError(RuntimeError):
    """The requested Life Area is unavailable in the authenticated self scope."""


class TemporalAuthoringLifeAreaConflictError(RuntimeError):
    """The selected Life Area changed before an accepted appearance update."""


class TemporalAuthoringPersistenceError(RuntimeError):
    """Canonical quick-authoring persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class AuthoringLifeAreaIntent:
    """Optional actor-local organization requested by one Quick Create draft.

    `life_area_ref` selects an existing area. `new_name` requests creation of a
    new area inside the same transaction.  The two forms are mutually
    exclusive. `color_code` belongs to the Life Area, never to the item, when
    either form is present.
    """

    life_area_ref: UUID | None = None
    new_name: str | None = None
    expected_revision: int | None = None
    color_code: str | None = None


@dataclass(frozen=True, slots=True)
class AuthoredItemView:
    subject_kind: str
    subject_native_ref: NativeRef
    title: str
    created_at: datetime
    description: str | None
    location: str | None
    color_code: str | None
    life_area_ref: UUID | None
    life_area_assignment_revision: int | None
    life_area_color_code: str | None
    life_area_revision: int | None
    agenda_revision: int = 0
    agenda_parts: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuthoringResult:
    item: AuthoredItemView
    replayed: bool
    schedule: EstablishedScheduleView | None = None
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"] = "disabled"


@dataclass(frozen=True, slots=True)
class _ResolvedLifeArea:
    life_area_ref: UUID
    revision: int
    color_code: str | None


def _json_fingerprint(intent: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(
            intent,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _operation(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise TemporalAuthoringInputError("Operation id must contain 1 to 200 characters.")
    return normalized


def _derived_operation(prefix: str, operation_id: str) -> str:
    digest = hashlib.sha256(operation_id.encode("utf-8")).hexdigest()
    return f"{prefix}:{digest}"


def _title(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 300:
        raise TemporalAuthoringInputError("Title must contain 1 to 300 non-padding characters.")
    return normalized


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _color(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().upper()
    if not normalized:
        return None
    if (
        len(normalized) != 7
        or normalized[0] != "#"
        or any(character not in "0123456789ABCDEF" for character in normalized[1:])
    ):
        raise TemporalAuthoringInputError("Color must use #RRGGBB notation.")
    return normalized


def _agenda(values: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    if len(values) > 100:
        raise TemporalAuthoringInputError("Event Agenda may contain at most 100 parts.")
    normalized: list[str] = []
    for value in values:
        part = value.strip()
        if not part or len(part) > 1000:
            raise TemporalAuthoringInputError(
                "Event Agenda parts must contain 1 to 1000 non-padding characters."
            )
        normalized.append(part)
    return tuple(normalized)


def _constraint_name(exc: DBAPIError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _item_fingerprint(
    *,
    subject_kind: str,
    title: str,
    agenda_parts: tuple[str, ...],
    life_area_ref: UUID | None,
    description: str | None,
    location: str | None,
    color_code: str | None,
    session_capture_mode: str | None = None,
) -> str:
    """Preserve B05 v2 replay compatibility for the exact historical shape."""
    if (life_area_ref is not None and description is None and location is None
            and color_code is None and session_capture_mode is None):
        intent: dict[str, object] = {
            "version": 2,
            "title": title,
            "life_area_ref": str(life_area_ref),
        }
        if subject_kind == "event" and agenda_parts:
            intent["agenda_parts"] = list(agenda_parts)
        return _json_fingerprint(intent)

    intent = {
        "version": 3,
        "subject_kind": subject_kind,
        "title": title,
        "life_area_ref": None if life_area_ref is None else str(life_area_ref),
        "description": description,
        "location": location,
        "color_code": color_code,
    }
    if subject_kind == "event":
        intent["agenda_parts"] = list(agenda_parts)
    if session_capture_mode is not None:
        intent["version"] = 4
        intent["session_capture_mode"] = session_capture_mode
    return _json_fingerprint(intent)


async def _list_area(
    session: AsyncSession, *, self_person_ref: NativeRef, life_area_ref: UUID
) -> RowMapping | None:
    rows = (
        (
            await session.execute(
                text("""
                    SELECT life_area_ref,name,created_at,revision,sort_order,archived,hidden,
                           icon_code,color_code,updated_at
                      FROM dante.list_self_life_areas(:self_person_ref)
                """),
                {"self_person_ref": self_person_ref},
            )
        )
        .mappings()
        .all()
    )
    return next((row for row in rows if UUID(str(row["life_area_ref"])) == life_area_ref), None)


async def _resolve_life_area(
    session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    intent: AuthoringLifeAreaIntent | None,
) -> _ResolvedLifeArea | None:
    if intent is None:
        return None
    if intent.life_area_ref is not None and intent.new_name is not None:
        raise TemporalAuthoringInputError(
            "Choose an existing Life Area or create a new one, not both."
        )
    desired_color = _color(intent.color_code)

    if intent.life_area_ref is None:
        if intent.new_name is None or not intent.new_name.strip():
            return None
        normalized_name = intent.new_name.strip()
        if len(normalized_name) > 100:
            raise TemporalAuthoringInputError(
                "Life Area name must contain 1 to 100 non-padding characters."
            )
        area_operation = _derived_operation("b14-u2-area-create", operation_id)
        area_fingerprint = _json_fingerprint({"version": 1, "name": normalized_name})
        area_result = (
            (
                await session.execute(
                    text("""
                        SELECT life_area_ref,replayed
                          FROM dante.create_self_life_area(
                            :self_person_ref,:operation_id,:fingerprint,:area_ref,:name)
                    """),
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": area_operation,
                        "fingerprint": area_fingerprint,
                        "area_ref": uuid7(),
                        "name": normalized_name,
                    },
                )
            )
            .mappings()
            .one()
        )
        area_ref = UUID(str(area_result["life_area_ref"]))
        area = await _list_area(session, self_person_ref=self_person_ref, life_area_ref=area_ref)
        if area is None:
            raise TemporalAuthoringPersistenceError("New Life Area disappeared inside authoring.")
    else:
        area_ref = intent.life_area_ref
        area = await _list_area(session, self_person_ref=self_person_ref, life_area_ref=area_ref)
        if area is None or bool(area["archived"]):
            raise TemporalAuthoringLifeAreaUnavailableError()

    current_revision = int(area["revision"])
    current_color = None if area["color_code"] is None else str(area["color_code"])
    if desired_color is not None and desired_color != current_color:
        if intent.life_area_ref is not None:
            if intent.expected_revision is None:
                raise TemporalAuthoringInputError(
                    "Life Area revision is required when changing its color."
                )
            if intent.expected_revision != current_revision:
                raise TemporalAuthoringLifeAreaConflictError()
        appearance_operation = _derived_operation("b14-u2-area-appearance", operation_id)
        payload = {"icon_code": area["icon_code"], "color_code": desired_color}
        appearance_fingerprint = _json_fingerprint(
            {
                "version": 1,
                "kind": "appearance",
                "area": str(area_ref),
                "expected_revision": current_revision,
                "payload": payload,
            }
        )
        mutation = (
            (
                await session.execute(
                    text("""
                        SELECT accepted_revision,replayed
                          FROM dante.mutate_self_life_area(
                            :self_person_ref,:operation_id,:fingerprint,:life_area_ref,
                            :expected_revision,'appearance',NULL,NULL,:icon_code,:color_code)
                    """),
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": appearance_operation,
                        "fingerprint": appearance_fingerprint,
                        "life_area_ref": area_ref,
                        "expected_revision": current_revision,
                        "icon_code": area["icon_code"],
                        "color_code": desired_color,
                    },
                )
            )
            .mappings()
            .one()
        )
        current_revision = int(mutation["accepted_revision"])
        current_color = desired_color

    return _ResolvedLifeArea(
        life_area_ref=area_ref,
        revision=current_revision,
        color_code=current_color,
    )


def _activity_from_row(
    row: RowMapping, *, area: _ResolvedLifeArea | None
) -> AuthoredItemView:
    return AuthoredItemView(
        subject_kind="activity",
        subject_native_ref=NativeRef(UUID(str(row["activity_ref"]))),
        title=str(row["title"]),
        created_at=row["created_at"],
        description=None if row["description"] is None else str(row["description"]),
        location=None if row["location"] is None else str(row["location"]),
        color_code=None if row["color_code"] is None else str(row["color_code"]),
        life_area_ref=None if row["life_area_ref"] is None else UUID(str(row["life_area_ref"])),
        life_area_assignment_revision=(
            None if row["assignment_revision"] is None else int(row["assignment_revision"])
        ),
        life_area_color_code=None if area is None else area.color_code,
        life_area_revision=None if area is None else area.revision,
    )


def _event_from_row(row: RowMapping, *, area: _ResolvedLifeArea | None) -> AuthoredItemView:
    return AuthoredItemView(
        subject_kind="event",
        subject_native_ref=NativeRef(UUID(str(row["event_ref"]))),
        title=str(row["title"]),
        created_at=row["created_at"],
        description=None if row["description"] is None else str(row["description"]),
        location=None if row["location"] is None else str(row["location"]),
        color_code=None if row["color_code"] is None else str(row["color_code"]),
        life_area_ref=None if row["life_area_ref"] is None else UUID(str(row["life_area_ref"])),
        life_area_assignment_revision=(
            None if row["assignment_revision"] is None else int(row["assignment_revision"])
        ),
        life_area_color_code=None if area is None else area.color_code,
        life_area_revision=None if area is None else area.revision,
        agenda_revision=int(row["agenda_revision"]),
        agenda_parts=tuple(str(part) for part in (row["agenda_parts"] or ())),
    )


class TemporalAuthoringApplication:
    """Own U2 Quick Create writes as one atomic transaction."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _create_activity(
        self,
        session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        description: str | None,
        location: str | None,
        item_color_code: str | None,
        life_area: _ResolvedLifeArea | None,
        session_capture_mode: str | None,
    ) -> tuple[AuthoredItemView, bool]:
        if life_area is not None and item_color_code is not None:
            raise TemporalAuthoringInputError(
                "Item color override is only valid when no Life Area is selected."
            )
        fingerprint = _item_fingerprint(
            subject_kind="activity",
            title=title,
            agenda_parts=(),
            life_area_ref=None if life_area is None else life_area.life_area_ref,
            description=description,
            location=location,
            color_code=item_color_code,
            session_capture_mode=session_capture_mode,
        )
        row = (
            (
                await session.execute(
                    text("""
                        SELECT activity_ref,title,created_at,life_area_ref,assignment_revision,
                               description,location,color_code,replayed
                          FROM dante.create_self_activity_authoring(
                            :self_person_ref,:operation_id,:fingerprint,:activity_ref,:title,
                            :life_area_ref,:description,:location,:color_code)
                    """),
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": operation_id,
                        "fingerprint": fingerprint,
                        "activity_ref": new_native_ref(),
                        "title": title,
                        "life_area_ref": None if life_area is None else life_area.life_area_ref,
                        "description": description,
                        "location": location,
                        "color_code": item_color_code,
                    },
                )
            )
            .mappings()
            .one()
        )
        return _activity_from_row(row, area=life_area), bool(row["replayed"])

    async def _create_event(
        self,
        session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        agenda_parts: tuple[str, ...],
        description: str | None,
        location: str | None,
        item_color_code: str | None,
        life_area: _ResolvedLifeArea | None,
    ) -> tuple[AuthoredItemView, bool]:
        if life_area is not None and item_color_code is not None:
            raise TemporalAuthoringInputError(
                "Item color override is only valid when no Life Area is selected."
            )
        fingerprint = _item_fingerprint(
            subject_kind="event",
            title=title,
            agenda_parts=agenda_parts,
            life_area_ref=None if life_area is None else life_area.life_area_ref,
            description=description,
            location=location,
            color_code=item_color_code,
        )
        row = (
            (
                await session.execute(
                    text("""
                        SELECT event_ref,title,created_at,agenda_revision,agenda_parts,
                               life_area_ref,assignment_revision,description,location,
                               color_code,replayed
                          FROM dante.create_self_event_authoring(
                            :self_person_ref,:operation_id,:fingerprint,:event_ref,:title,
                            :agenda_parts,:life_area_ref,:description,:location,:color_code)
                    """),
                    {
                        "self_person_ref": self_person_ref,
                        "operation_id": operation_id,
                        "fingerprint": fingerprint,
                        "event_ref": new_native_ref(),
                        "title": title,
                        "agenda_parts": list(agenda_parts),
                        "life_area_ref": None if life_area is None else life_area.life_area_ref,
                        "description": description,
                        "location": location,
                        "color_code": item_color_code,
                    },
                )
            )
            .mappings()
            .one()
        )
        return _event_from_row(row, area=life_area), bool(row["replayed"])

    async def _execute(
        self,
        *,
        subject_kind: str,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_intent: AuthoringLifeAreaIntent | None,
        description: str | None,
        location: str | None,
        item_color_code: str | None,
        agenda_parts: tuple[str, ...],
        placement: SchedulePlacement | None,
        session_capture_mode: str | None,
    ) -> AuthoringResult:
        normalized_operation = _operation(operation_id)
        normalized_title = _title(title)
        normalized_description = _optional_text(description)
        normalized_location = _optional_text(location)
        normalized_item_color = _color(item_color_code)
        if subject_kind not in {"activity", "event"}:
            raise TemporalAuthoringInputError("Unsupported authoring subject kind.")
        if session_capture_mode is not None and (
            subject_kind != "activity" or session_capture_mode not in {
                "disabled", "record", "live", "record_and_live"
            }
        ):
            raise TemporalAuthoringInputError("Activity Session capture mode is invalid.")

        try:
            async with self._session_factory() as session, session.begin():
                life_area = await _resolve_life_area(
                    session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation,
                    intent=life_area_intent,
                )
                if subject_kind == "activity":
                    item, replayed = await self._create_activity(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=normalized_operation,
                        title=normalized_title,
                        description=normalized_description,
                        location=normalized_location,
                        item_color_code=normalized_item_color,
                        life_area=life_area,
                        session_capture_mode=session_capture_mode,
                    )
                else:
                    item, replayed = await self._create_event(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=normalized_operation,
                        title=normalized_title,
                        agenda_parts=agenda_parts,
                        description=normalized_description,
                        location=normalized_location,
                        item_color_code=normalized_item_color,
                        life_area=life_area,
                    )

                schedule: EstablishedScheduleView | None = None
                if placement is not None:
                    schedule = await establish_schedule_in_session(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=_derived_operation("b14-u2-schedule", normalized_operation),
                        subject_native_ref=item.subject_native_ref,
                        placement=placement,
                    )
                    if replayed is not schedule.replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and Schedule replay state diverged."
                        )
                if session_capture_mode is not None:
                    policy_operation = _derived_operation(
                        "b14-u6-execution-policy", normalized_operation
                    )
                    policy_fingerprint = _json_fingerprint({
                        "version": 1,
                        "activity_ref": str(item.subject_native_ref),
                        "mode_code": session_capture_mode,
                        "expected_state_ref": None,
                    })
                    policy = (
                        await session.execute(
                            text("""
                                SELECT * FROM dante.set_self_activity_execution_policy(
                                    :actor,:operation,:fingerprint,:activity,:state,:mode,NULL
                                )
                            """),
                            {
                                "actor": self_person_ref,
                                "operation": policy_operation,
                                "fingerprint": policy_fingerprint,
                                "activity": item.subject_native_ref,
                                "state": uuid7(),
                                "mode": session_capture_mode,
                            },
                        )
                    ).mappings().one()
                    if bool(policy["replayed"]) is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and execution policy replay state diverged."
                        )
                return AuthoringResult(
                    item=item, replayed=replayed, schedule=schedule,
                    session_capture_mode=session_capture_mode or "disabled",
                )
        except (
            TemporalAuthoringInputError,
            TemporalAuthoringLifeAreaUnavailableError,
            TemporalAuthoringLifeAreaConflictError,
            TemporalAuthoringOperationIdReuseError,
        ):
            raise
        except ScheduleOperationIdReuseError as exc:
            raise TemporalAuthoringOperationIdReuseError() from exc
        except ScheduleInputError as exc:
            raise TemporalAuthoringInputError(str(exc)) from exc
        except IntegrityError as exc:
            constraint = _constraint_name(exc)
            if constraint in {
                "pk_activity_create_operation",
                "pk_event_create_operation",
                "pk_life_area_create_operation",
                "pk_life_area_mutation_operation",
                "pk_schedule_establish_operation",
            }:
                raise TemporalAuthoringOperationIdReuseError() from exc
            if constraint in {
                "life_area_assignment_target_unavailable",
                "fk_life_area_mutation_operation_life_area_ref_life_area",
            }:
                raise TemporalAuthoringLifeAreaUnavailableError() from exc
            if constraint in {"life_area_expected_revision", "life_area_no_change"}:
                raise TemporalAuthoringLifeAreaConflictError() from exc
            if constraint in {
                "ck_activity_intention_color_code",
                "ck_event_expectation_color_code",
            }:
                raise TemporalAuthoringInputError("Invalid item color.") from exc
            raise TemporalAuthoringPersistenceError() from exc
        except DBAPIError as exc:
            constraint = _constraint_name(exc)
            if constraint in {
                "life_area_assignment_target_unavailable",
                "fk_life_area_mutation_operation_life_area_ref_life_area",
            }:
                raise TemporalAuthoringLifeAreaUnavailableError() from exc
            if constraint in {"life_area_expected_revision", "life_area_no_change"}:
                raise TemporalAuthoringLifeAreaConflictError() from exc
            raise TemporalAuthoringPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise TemporalAuthoringPersistenceError() from exc

    async def create_activity(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_intent: AuthoringLifeAreaIntent | None = None,
        description: str | None = None,
        location: str | None = None,
        item_color_code: str | None = None,
        placement: SchedulePlacement | None = None,
        session_capture_mode: str | None = None,
    ) -> AuthoringResult:
        return await self._execute(
            subject_kind="activity",
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            title=title,
            life_area_intent=life_area_intent,
            description=description,
            location=location,
            item_color_code=item_color_code,
            agenda_parts=(),
            placement=placement,
            session_capture_mode=session_capture_mode,
        )

    async def create_event(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_intent: AuthoringLifeAreaIntent | None = None,
        description: str | None = None,
        location: str | None = None,
        item_color_code: str | None = None,
        agenda_parts: tuple[str, ...] | list[str] = (),
        placement: SchedulePlacement | None = None,
    ) -> AuthoringResult:
        return await self._execute(
            subject_kind="event",
            self_person_ref=self_person_ref,
            operation_id=operation_id,
            title=title,
            life_area_intent=life_area_intent,
            description=description,
            location=location,
            item_color_code=item_color_code,
            agenda_parts=_agenda(agenda_parts),
            placement=placement,
            session_capture_mode=None,
        )
