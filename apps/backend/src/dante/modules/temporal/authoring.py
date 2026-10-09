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
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    ScheduleOperationIdReuseError,
    SchedulePlacement,
    _placement_payload,
    establish_schedule_in_session,
)
from dante.modules.temporal.temporal_constraint import (
    SessionMinimumDurationRule,
    _mutate_in_session,
)
from dante.platform.database.references import (
    NativeRef,
    new_material_state_ref,
    new_native_ref,
    new_scoped_record_ref,
)


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


class TemporalAuthoringStructureConflictError(RuntimeError):
    """The requested child placement or relationship conflicts with current truth."""


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
    child_guard_mode: Literal["none", "confirm", "block"] = "none"
    planned_slices: tuple[EstablishedScheduleView, ...] = ()
    activity_intervals: tuple[EstablishedScheduleView, ...] = ()
    children: tuple[AuthoredActivityChild, ...] = ()


@dataclass(frozen=True, slots=True)
class ActivityChildIntent:
    title: str
    requirement_code: Literal["required", "optional"] = "required"
    presentation_order: int = 1
    description: str | None = None
    placement: SchedulePlacement | None = None
    planned_slices: tuple[SchedulePlacement, ...] = ()
    planned_slice_names: tuple[str, ...] = ()
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"] | None = None


@dataclass(frozen=True, slots=True)
class AuthoredActivityChild:
    item: AuthoredItemView
    decomposition_ref: UUID
    state_ref: UUID
    requirement_code: Literal["required", "optional"]
    presentation_order: int
    schedule: EstablishedScheduleView | None
    planned_slices: tuple[EstablishedScheduleView, ...]
    session_capture_mode: Literal["disabled", "record", "live", "record_and_live"]


@dataclass(frozen=True, slots=True)
class ResolvedAuthoringLifeArea:
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


async def _schedule_role(
    session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    activity_ref: NativeRef,
    schedule: EstablishedScheduleView,
    role_code: Literal["envelope", "planned", "interval"],
    presentation_order: int,
    display_name: str | None = None,
) -> None:
    accepted = (
        (
            await session.execute(
                text("""
                SELECT * FROM dante.set_self_activity_schedule_role(
                    :actor,:activity,:schedule,:role,:position,:display_name
                )
            """),
                {
                    "actor": self_person_ref,
                    "activity": activity_ref,
                    "schedule": schedule.schedule_ref,
                    "role": role_code,
                    "position": presentation_order,
                    "display_name": display_name,
                },
            )
        )
        .mappings()
        .one()
    )
    # A command created before this role relation existed can replay once and
    # attach its previously implicit purpose in the same transaction.
    if bool(accepted["replayed"]) and not schedule.replayed:
        raise TemporalAuthoringOperationIdReuseError(
            "Create and Schedule role replay state diverged."
        )


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
    structure_digest: str | None = None,
) -> str:
    """Preserve B05 v2 replay compatibility for the exact historical shape."""
    if (
        life_area_ref is not None
        and description is None
        and location is None
        and color_code is None
        and session_capture_mode is None
        and structure_digest is None
    ):
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
    if structure_digest is not None:
        intent["version"] = 5
        intent["structure_digest"] = structure_digest
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


async def resolve_authoring_life_area(
    session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    intent: AuthoringLifeAreaIntent | None,
) -> ResolvedAuthoringLifeArea | None:
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

    return ResolvedAuthoringLifeArea(
        life_area_ref=area_ref,
        revision=current_revision,
        color_code=current_color,
    )


def _activity_from_row(row: RowMapping, *, area: ResolvedAuthoringLifeArea | None) -> AuthoredItemView:
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


def _event_from_row(row: RowMapping, *, area: ResolvedAuthoringLifeArea | None) -> AuthoredItemView:
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
        life_area: ResolvedAuthoringLifeArea | None,
        session_capture_mode: str | None,
        structure_digest: str | None = None,
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
            structure_digest=structure_digest,
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
        life_area: ResolvedAuthoringLifeArea | None,
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
        minimum_session_duration_microseconds: int | None = None,
        child_guard_mode: str | None = None,
        planned_slices: tuple[SchedulePlacement | None, ...] = (),
        activity_intervals: tuple[SchedulePlacement, ...] = (),
        planned_slice_names: tuple[str, ...] = (),
        children: tuple[ActivityChildIntent, ...] = (),
    ) -> AuthoringResult:
        normalized_operation = _operation(operation_id)
        normalized_title = _title(title)
        normalized_description = _optional_text(description)
        normalized_location = _optional_text(location)
        normalized_item_color = _color(item_color_code)
        if subject_kind not in {"activity", "event"}:
            raise TemporalAuthoringInputError("Unsupported authoring subject kind.")
        if session_capture_mode is not None and (
            subject_kind != "activity"
            or session_capture_mode not in {"disabled", "record", "live", "record_and_live"}
        ):
            raise TemporalAuthoringInputError("Activity Session capture mode is invalid.")
        if minimum_session_duration_microseconds is not None and (
            subject_kind != "activity"
            or isinstance(minimum_session_duration_microseconds, bool)
            or not isinstance(minimum_session_duration_microseconds, int)
            or minimum_session_duration_microseconds <= 0
            or minimum_session_duration_microseconds > 9_223_372_036_854_775_807
        ):
            raise TemporalAuthoringInputError("Activity Session minimum duration is invalid.")
        if subject_kind != "activity" and (planned_slices or activity_intervals or children):
            raise TemporalAuthoringInputError("Only an Activity can own planned execution rows.")
        if child_guard_mode is not None and (
            subject_kind != "activity" or child_guard_mode not in {"none", "confirm", "block"}
        ):
            raise TemporalAuthoringInputError("Activity parent child policy is invalid.")
        if len(children) > 100 or len(planned_slices) > 100 or len(activity_intervals) > 100:
            raise TemporalAuthoringInputError("Activity structure exceeds its bounded size.")
        if activity_intervals and placement is None:
            raise TemporalAuthoringInputError("Activity intervals require a parent placement.")
        if activity_intervals:
            if not isinstance(
                placement, (FloatingLocalIntervalPlacement, NamedZoneLocalIntervalPlacement)
            ):
                raise TemporalAuthoringInputError("Activity intervals require a timed Activity.")
            previous_end = None
            for interval in activity_intervals:
                if type(interval) is not type(placement):
                    raise TemporalAuthoringInputError(
                        "Activity intervals must use the Activity time frame."
                    )
                if (
                    isinstance(interval, NamedZoneLocalIntervalPlacement)
                    and isinstance(placement, NamedZoneLocalIntervalPlacement)
                    and interval.zone_id != placement.zone_id
                ):
                    raise TemporalAuthoringInputError(
                        "Activity intervals must use the Activity time zone."
                    )
                start, end = interval.starts_local_at, interval.ends_local_at
                if start < placement.starts_local_at or end > placement.ends_local_at:
                    raise TemporalAuthoringInputError(
                        "Activity interval falls outside the Activity envelope."
                    )
                if previous_end is not None and start < previous_end:
                    raise TemporalAuthoringInputError(
                        "Activity intervals must be ordered and non-overlapping."
                    )
                previous_end = end
            if (
                activity_intervals[0].starts_local_at != placement.starts_local_at
                or activity_intervals[-1].ends_local_at != placement.ends_local_at
            ):
                raise TemporalAuthoringInputError(
                    "Activity envelope must exactly cover its first and last interval."
                )
        if planned_slice_names and len(planned_slice_names) != len(planned_slices):
            raise TemporalAuthoringInputError("Planned Session names must match planned rows.")
        if any(len(name.strip()) > 300 for name in planned_slice_names):
            raise TemporalAuthoringInputError("Planned Session name is too long.")
        for child in children:
            _title(child.title)
            if (
                child.requirement_code not in {"required", "optional"}
                or child.presentation_order < 1
            ):
                raise TemporalAuthoringInputError("Child relationship configuration is invalid.")
            if (
                child.session_capture_mode
                not in {None, "disabled", "record", "live", "record_and_live"}
                or len(child.planned_slices) > 100
            ):
                raise TemporalAuthoringInputError("Child execution configuration is invalid.")
            if child.planned_slice_names and len(child.planned_slice_names) != len(
                child.planned_slices
            ):
                raise TemporalAuthoringInputError("Child Session names must match planned rows.")
            if any(len(name.strip()) > 300 for name in child.planned_slice_names):
                raise TemporalAuthoringInputError("Child Session name is too long.")
        structure_digest = None
        if (
            children
            or planned_slices
            or activity_intervals
            or child_guard_mode is not None
            or minimum_session_duration_microseconds is not None
        ):
            structure_digest = _json_fingerprint(
                {
                    "version": 1,
                    "child_guard_mode": child_guard_mode,
                    "minimum_session_duration_microseconds": minimum_session_duration_microseconds,
                    "root_placement": None if placement is None else _placement_payload(placement),
                    "planned_slices": [None if value is None else _placement_payload(value)
                                       for value in planned_slices],
                    **(
                        {
                            "activity_intervals": [
                                _placement_payload(value) for value in activity_intervals
                            ]
                        }
                        if activity_intervals
                        else {}
                    ),
                    **(
                        {"planned_slice_names": [name.strip() for name in planned_slice_names]}
                        if any(name.strip() for name in planned_slice_names)
                        else {}
                    ),
                    "children": [
                        {
                            "title": _title(child.title),
                            "description": _optional_text(child.description),
                            "requirement_code": child.requirement_code,
                            "presentation_order": child.presentation_order,
                            "session_capture_mode": child.session_capture_mode,
                            "placement": (
                                None
                                if child.placement is None
                                else _placement_payload(child.placement)
                            ),
                            "planned_slices": [
                                _placement_payload(value) for value in child.planned_slices
                            ],
                            **(
                                {
                                    "planned_slice_names": [
                                        name.strip() for name in child.planned_slice_names
                                    ]
                                }
                                if any(name.strip() for name in child.planned_slice_names)
                                else {}
                            ),
                        }
                        for child in children
                    ],
                }
            )

        try:
            async with self._session_factory() as session, session.begin():
                life_area = await resolve_authoring_life_area(
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
                        structure_digest=structure_digest,
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
                    if subject_kind == "activity":
                        await _schedule_role(
                            session,
                            self_person_ref=self_person_ref,
                            activity_ref=item.subject_native_ref,
                            schedule=schedule,
                            role_code="envelope",
                            presentation_order=0,
                        )
                if session_capture_mode is not None:
                    policy_operation = _derived_operation(
                        "b14-u6-execution-policy", normalized_operation
                    )
                    policy_fingerprint = _json_fingerprint(
                        {
                            "version": 1,
                            "activity_ref": str(item.subject_native_ref),
                            "mode_code": session_capture_mode,
                            "expected_state_ref": None,
                        }
                    )
                    policy = (
                        (
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
                        )
                        .mappings()
                        .one()
                    )
                    if bool(policy["replayed"]) is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and execution policy replay state diverged."
                        )
                if minimum_session_duration_microseconds is not None:
                    minimum_rule = SessionMinimumDurationRule(
                        duration_microseconds=minimum_session_duration_microseconds
                    )
                    minimum_row = await _mutate_in_session(
                        session,
                        family="duration",
                        self_person_ref=self_person_ref,
                        operation_id=_derived_operation(
                            "b14-u6-session-minimum", normalized_operation
                        ),
                        fingerprint=_json_fingerprint(
                            {
                                "version": 1,
                                "activity_ref": str(item.subject_native_ref),
                                "duration_microseconds": minimum_session_duration_microseconds,
                            }
                        ),
                        mutation_kind="create",
                        subject_native_ref=item.subject_native_ref,
                        constraint_ref=new_scoped_record_ref(),
                        expected_material_state_ref=None,
                        resulting_material_state_ref=new_material_state_ref(),
                        rule=minimum_rule,
                    )
                    if (
                        bool(minimum_row["replayed"]) is not replayed
                        or minimum_row["active"] is not True
                    ):
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and Session minimum replay state diverged."
                        )
                if child_guard_mode is not None:
                    guard_operation = _derived_operation(
                        "b14-u6-parent-guard", normalized_operation
                    )
                    guard_fingerprint = _json_fingerprint(
                        {
                            "version": 1,
                            "activity_ref": str(item.subject_native_ref),
                            "mode_code": child_guard_mode,
                            "expected_state_ref": None,
                        }
                    )
                    guard = (
                        (
                            await session.execute(
                                text("""
                                SELECT * FROM dante.set_self_activity_decomposition_policy(
                                    :actor,:operation,:fingerprint,:activity,:state,:mode,NULL
                                )
                            """),
                                {
                                    "actor": self_person_ref,
                                    "operation": guard_operation,
                                    "fingerprint": guard_fingerprint,
                                    "activity": item.subject_native_ref,
                                    "state": uuid7(),
                                    "mode": child_guard_mode,
                                },
                            )
                        )
                        .mappings()
                        .one()
                    )
                    if bool(guard["replayed"]) is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and parent policy replay state diverged."
                        )
                planned_results: list[EstablishedScheduleView] = []
                interval_results: list[EstablishedScheduleView] = []
                for index, interval in enumerate(activity_intervals):
                    accepted = await establish_schedule_in_session(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=_derived_operation(
                            f"b14-activity-interval-{index}", normalized_operation
                        ),
                        subject_native_ref=item.subject_native_ref,
                        placement=interval,
                    )
                    if accepted.replayed is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and Activity interval replay state diverged."
                        )
                    await _schedule_role(
                        session,
                        self_person_ref=self_person_ref,
                        activity_ref=item.subject_native_ref,
                        schedule=accepted,
                        role_code="interval",
                        presentation_order=index + 1,
                    )
                    interval_results.append(accepted)
                for index, planned in enumerate(planned_slices):
                    if planned is None:
                        row = (await session.execute(text("""
                            SELECT * FROM dante.establish_self_unplaced_planned_schedule(
                                :actor,:activity,:schedule,:position,:display_name)
                        """), {
                            "actor": self_person_ref,
                            "activity": item.subject_native_ref,
                            "schedule": new_scoped_record_ref(),
                            "position": index + 1,
                            "display_name": planned_slice_names[index].strip() or None
                            if planned_slice_names else None,
                        })).mappings().one()
                        if bool(row["replayed"]) is not replayed:
                            raise TemporalAuthoringOperationIdReuseError(
                                "Create and unplaced planned Schedule replay state diverged."
                            )
                        continue
                    accepted = await establish_schedule_in_session(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=_derived_operation(
                            f"b14-u6-planned-{index}", normalized_operation
                        ),
                        subject_native_ref=item.subject_native_ref,
                        placement=planned,
                    )
                    if accepted.replayed is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and planned Schedule replay state diverged."
                        )
                    await _schedule_role(
                        session,
                        self_person_ref=self_person_ref,
                        activity_ref=item.subject_native_ref,
                        schedule=accepted,
                        role_code="planned",
                        presentation_order=index + 1,
                        display_name=planned_slice_names[index].strip() or None
                        if planned_slice_names
                        else None,
                    )
                    planned_results.append(accepted)

                child_results: list[AuthoredActivityChild] = []
                for index, child in enumerate(children):
                    child_operation = _derived_operation(
                        f"b14-u6-child-{index}", normalized_operation
                    )
                    child_item, child_replayed = await self._create_activity(
                        session,
                        self_person_ref=self_person_ref,
                        operation_id=child_operation,
                        title=_title(child.title),
                        description=_optional_text(child.description),
                        location=None,
                        item_color_code=None,
                        life_area=life_area,
                        session_capture_mode=child.session_capture_mode,
                    )
                    if child_replayed is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Root and child Create replay state diverged."
                        )
                    relation_fingerprint = _json_fingerprint(
                        {
                            "version": 1,
                            "parent": str(item.subject_native_ref),
                            "child": str(child_item.subject_native_ref),
                            "requirement": child.requirement_code,
                            "order": child.presentation_order,
                        }
                    )
                    relation = (
                        (
                            await session.execute(
                                text("""
                                SELECT * FROM dante.set_self_activity_decomposition(
                                    :actor,:operation,:fingerprint,:relation,:parent,:child,
                                    :state,true,:requirement,:position,NULL
                                )
                            """),
                                {
                                    "actor": self_person_ref,
                                    "operation": _derived_operation(
                                        f"b14-u6-relation-{index}", normalized_operation
                                    ),
                                    "fingerprint": relation_fingerprint,
                                    "relation": uuid7(),
                                    "parent": item.subject_native_ref,
                                    "child": child_item.subject_native_ref,
                                    "state": uuid7(),
                                    "requirement": child.requirement_code,
                                    "position": child.presentation_order,
                                },
                            )
                        )
                        .mappings()
                        .one()
                    )
                    if bool(relation["replayed"]) is not replayed:
                        raise TemporalAuthoringOperationIdReuseError(
                            "Create and child relation replay state diverged."
                        )
                    child_schedule = None
                    if child.placement is not None:
                        child_schedule = await establish_schedule_in_session(
                            session,
                            self_person_ref=self_person_ref,
                            operation_id=_derived_operation(
                                f"b14-u6-child-placement-{index}", normalized_operation
                            ),
                            subject_native_ref=child_item.subject_native_ref,
                            placement=child.placement,
                        )
                        if child_schedule.replayed is not replayed:
                            raise TemporalAuthoringOperationIdReuseError(
                                "Create and child Schedule replay state diverged."
                            )
                        await _schedule_role(
                            session,
                            self_person_ref=self_person_ref,
                            activity_ref=child_item.subject_native_ref,
                            schedule=child_schedule,
                            role_code="envelope",
                            presentation_order=0,
                        )
                    child_slices: list[EstablishedScheduleView] = []
                    for slice_index, child_planned in enumerate(child.planned_slices):
                        accepted = await establish_schedule_in_session(
                            session,
                            self_person_ref=self_person_ref,
                            operation_id=_derived_operation(
                                f"b14-u6-child-{index}-planned-{slice_index}",
                                normalized_operation,
                            ),
                            subject_native_ref=child_item.subject_native_ref,
                            placement=child_planned,
                        )
                        if accepted.replayed is not replayed:
                            raise TemporalAuthoringOperationIdReuseError(
                                "Create and child planned Schedule replay state diverged."
                            )
                        await _schedule_role(
                            session,
                            self_person_ref=self_person_ref,
                            activity_ref=child_item.subject_native_ref,
                            schedule=accepted,
                            role_code="planned",
                            presentation_order=slice_index + 1,
                            display_name=child.planned_slice_names[slice_index].strip() or None
                            if child.planned_slice_names
                            else None,
                        )
                        child_slices.append(accepted)
                    if child.session_capture_mode is not None:
                        policy_fingerprint = _json_fingerprint(
                            {
                                "version": 1,
                                "activity_ref": str(child_item.subject_native_ref),
                                "mode_code": child.session_capture_mode,
                                "expected_state_ref": None,
                            }
                        )
                        policy = (
                            (
                                await session.execute(
                                    text("""
                                    SELECT * FROM dante.set_self_activity_execution_policy(
                                        :actor,:operation,:fingerprint,:activity,:state,:mode,NULL
                                    )
                                """),
                                    {
                                        "actor": self_person_ref,
                                        "operation": _derived_operation(
                                            f"b14-u6-child-policy-{index}", normalized_operation
                                        ),
                                        "fingerprint": policy_fingerprint,
                                        "activity": child_item.subject_native_ref,
                                        "state": uuid7(),
                                        "mode": child.session_capture_mode,
                                    },
                                )
                            )
                            .mappings()
                            .one()
                        )
                        if bool(policy["replayed"]) is not replayed:
                            raise TemporalAuthoringOperationIdReuseError(
                                "Create and child execution policy replay state diverged."
                            )
                    child_results.append(
                        AuthoredActivityChild(
                            item=child_item,
                            decomposition_ref=relation["decomposition_ref"],
                            state_ref=relation["state_ref"],
                            requirement_code=child.requirement_code,
                            presentation_order=child.presentation_order,
                            schedule=child_schedule,
                            planned_slices=tuple(child_slices),
                            session_capture_mode=child.session_capture_mode or "disabled",
                        )
                    )
                return AuthoringResult(
                    item=item,
                    replayed=replayed,
                    schedule=schedule,
                    session_capture_mode=session_capture_mode or "disabled",
                    child_guard_mode=child_guard_mode or "none",
                    planned_slices=tuple(planned_results),
                    activity_intervals=tuple(interval_results),
                    children=tuple(child_results),
                )
        except (
            TemporalAuthoringInputError,
            TemporalAuthoringLifeAreaUnavailableError,
            TemporalAuthoringLifeAreaConflictError,
            TemporalAuthoringOperationIdReuseError,
            TemporalAuthoringStructureConflictError,
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
            if constraint in {
                "activity_decomposition_temporal_containment",
                "activity_decomposition_depth_or_parent",
                "activity_schedule_role_conflict",
                "uq_activity_schedule_role_owner_role_order",
            }:
                raise TemporalAuthoringStructureConflictError() from exc
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
            if constraint in {
                "activity_decomposition_temporal_containment",
                "activity_decomposition_depth_or_parent",
                "activity_schedule_role_conflict",
                "activity_schedule_role_owner_unavailable",
            }:
                raise TemporalAuthoringStructureConflictError() from exc
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
        minimum_session_duration_microseconds: int | None = None,
        child_guard_mode: str | None = None,
        planned_slices: tuple[SchedulePlacement | None, ...] = (),
        activity_intervals: tuple[SchedulePlacement, ...] = (),
        planned_slice_names: tuple[str, ...] = (),
        children: tuple[ActivityChildIntent, ...] = (),
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
            minimum_session_duration_microseconds=minimum_session_duration_microseconds,
            child_guard_mode=child_guard_mode,
            planned_slices=planned_slices,
            activity_intervals=activity_intervals,
            planned_slice_names=planned_slice_names,
            children=children,
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
