"""Authoritative, bounded preparation of a structural recurring-series revision.

The returned plan is intentionally private to the transaction. A browser
fingerprint alone never grants permission to replace Recurrence or facts.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from itertools import pairwise
from typing import Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.event import _read_event_in_session
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.occurrence import CalendarCoordinate, OccurrenceApplication, _occurrence
from dante.modules.temporal.occurrence_edit_inventory import OccurrenceEditInventoryApplication
from dante.modules.temporal.occurrence_edit_scope import RecurrenceEditScopePlan
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication, _view
from dante.modules.temporal.recurring_series_reconciliation import (
    SeriesReconciliation,
    SeriesReconciliationError,
    SeriesReconciliationWindow,
)
from dante.modules.temporal.recurring_structure_policy import RecurringStructurePolicyApplication
from dante.modules.temporal.recurring_structure_preview import (
    RecurringStructurePreviewApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.platform.database.references import NativeRef

type SeriesScope = Literal["this_and_following", "from_next"]
type SeriesOwner = Literal["routine", "event"]
type ProtectionReason = Literal["registration", "skipped", "local_change", "legacy_unknown"]


class RecurringSeriesEditConflictError(RuntimeError):
    """The source, preview, selected identity or inventory changed."""


@dataclass(frozen=True, slots=True)
class RecurringSeriesPrepared:
    source_ref: UUID
    owner: SeriesOwner
    selected_ref: UUID
    prior_state_ref: UUID
    scope: RecurrenceEditScopePlan
    reconciliation: SeriesReconciliation
    fingerprint: str
    source_fingerprint: str
    protected_occurrences: tuple[tuple[UUID, ProtectionReason, datetime], ...]


@dataclass(frozen=True, slots=True)
class RecurringSeriesAccepted:
    source_ref: UUID
    recurrence_state_ref: UUID
    superseded_count: int
    protected_count: int
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class RecurringSeriesSource:
    source_ref: UUID
    owner: SeriesOwner
    edit_revision: int
    recurrence_state_ref: UUID
    recurrence: CalendarRecurrence
    structure_snapshot: dict[str, object]
    title: str
    selected_date: date
    description: str | None
    location: str | None
    color_code: str | None


def _child_operation(parent: str, purpose: str) -> str:
    return f"series:{purpose}:{hashlib.sha256(parent.encode()).hexdigest()}"


def _protection_reason(value: str) -> ProtectionReason:
    if value == "registration":
        return "registration"
    if value == "skipped":
        return "skipped"
    if value == "local_change":
        return "local_change"
    if value == "legacy_unknown":
        return "legacy_unknown"
    raise RecurringSeriesEditConflictError("Unknown future-instance protection.")


def _request_hash(
    *,
    self_person_ref: NativeRef,
    selected_occurrence_ref: UUID,
    requested_scope: SeriesScope,
    expected_revision: int,
    expected_state_ref: UUID,
    effective_zone_id: str,
    proposed_recurrence: CalendarRecurrence,
    proposed_structure: dict[str, object],
    profile_patch: dict[str, str | None] | None,
) -> str:
    intent = {
        "actor": str(self_person_ref),
        "selected": str(selected_occurrence_ref),
        "scope": requested_scope,
        "revision": expected_revision,
        "state": str(expected_state_ref),
        "zone": effective_zone_id,
        "recurrence": asdict(proposed_recurrence),
        "structure": proposed_structure,
        "profile": profile_patch,
    }
    return hashlib.sha256(
        json.dumps(intent, sort_keys=True, default=str, separators=(",", ":")).encode()
    ).hexdigest()


def _validate_structure(
    owner: SeriesOwner,
    recurrence: CalendarRecurrence,
    structure: dict[str, object],
) -> None:
    if structure.get("version") != 1:
        raise SeriesReconciliationError("Unsupported series structure version.")
    duration_minutes = structure.get("duration_minutes")
    duration_days = structure.get("duration_days")
    reminder = structure.get("reminder_lead_minutes")
    if reminder is not None and (type(reminder) is not int or not 0 <= reminder <= 10_080):
        raise SeriesReconciliationError("Recurring Reminder is invalid.")

    def window(value: object) -> tuple[int, int]:
        if not isinstance(value, dict) or set(value) != {
            "start_offset_minutes",
            "duration_minutes",
        }:
            raise SeriesReconciliationError("Recurring Activity window is invalid.")
        start = value["start_offset_minutes"]
        length = value["duration_minutes"]
        if (
            type(start) is not int
            or type(length) is not int
            or not -525_600 <= start <= 525_600
            or not 1 <= length <= 525_600
        ):
            raise SeriesReconciliationError("Recurring Activity window is invalid.")
        return start, start + length

    def text_value(value: object, *, limit: int = 300) -> bool:
        return (
            isinstance(value, str)
            and bool(value)
            and value == value.strip()
            and len(value) <= limit
        )

    def objectives(value: object) -> None:
        if not isinstance(value, list) or len(value) > 100:
            raise SeriesReconciliationError("Recurring Objectives are invalid.")
        for item in value:
            if not isinstance(item, dict) or not text_value(item.get("label")):
                raise SeriesReconciliationError("Recurring Objective is invalid.")
            kind = item.get("result_kind")
            if kind not in {"boolean", "quantity", "range", "qualitative"}:
                raise SeriesReconciliationError("Recurring Objective kind is invalid.")
            if type(item.get("presentation_order")) is not int:
                raise SeriesReconciliationError("Recurring Objective order is invalid.")
            if kind == "quantity" and (
                item.get("comparator_code") not in {"eq", "gte", "lte"}
                or type(item.get("target_value")) not in {float, int}
            ):
                raise SeriesReconciliationError("Recurring Objective quantity is invalid.")
            if kind == "range" and (
                item.get("comparator_code") != "between"
                or type(item.get("target_min")) not in {float, int}
                or type(item.get("target_max")) not in {float, int}
                or item["target_min"] > item["target_max"]
            ):
                raise SeriesReconciliationError("Recurring Objective range is invalid.")

    if owner == "routine":
        template = structure.get("activity_template")
        if (
            recurrence.clock_basis_code != "named_zone"
            or len(recurrence.wall_times) != 1
            or not isinstance(template, dict)
            or template.get("version") != 1
            or type(duration_minutes) is not int
            or not 1 <= duration_minutes <= 525_600
        ):
            raise SeriesReconciliationError(
                "Recurring Activity requires one named-zone time and a complete timed template."
            )
        objectives(template.get("objectives"))
        root_start, root_end = window(template.get("root_window"))
        if root_end - root_start != duration_minutes:
            raise SeriesReconciliationError("Recurring Activity duration disagrees with its plan.")
        if reminder is not None and root_start != 0:
            raise SeriesReconciliationError("Recurring Reminder needs the root plan.")
        if (
            template.get("session_capture_mode")
            not in {"disabled", "record", "live", "record_and_live"}
            or template.get("reality_mode")
            not in {"manual", "review_on_end", "auto_confirm_outcome"}
            or template.get("child_guard_mode") not in {"none", "confirm", "block"}
        ):
            raise SeriesReconciliationError("Recurring Activity execution policy is invalid.")
        if type(template.get("placement_protected")) is not bool:
            raise SeriesReconciliationError("Recurring Activity placement policy is invalid.")
        for field in ("description", "location", "item_color_code"):
            value = template.get(field)
            if value is not None and not text_value(value, limit=2000):
                raise SeriesReconciliationError("Recurring Activity text is invalid.")
        minimum = template.get("minimum_session_duration_microseconds")
        if minimum is not None and (type(minimum) is not int or minimum <= 0):
            raise SeriesReconciliationError("Recurring Session minimum is invalid.")
        for key in ("activity_intervals", "planned_slices", "children"):
            if not isinstance(template.get(key), list) or len(template[key]) > 100:
                raise SeriesReconciliationError(f"Recurring Activity {key} is invalid.")
        intervals = sorted(window(value) for value in template["activity_intervals"])
        if intervals and (
            intervals[0][0] != root_start
            or intervals[-1][1] != root_end
            or any(left[1] > right[0] for left, right in pairwise(intervals))
        ):
            raise SeriesReconciliationError("Recurring Activity intervals disagree with the root.")
        for item in template["planned_slices"]:
            if not isinstance(item, dict) or not text_value(item.get("name")):
                raise SeriesReconciliationError("Recurring Session name is invalid.")
            if item.get("time_enabled") is False:
                if set(item) != {"name", "time_enabled"}:
                    raise SeriesReconciliationError("Untimed recurring Session is invalid.")
            else:
                window({key: item.get(key) for key in ("start_offset_minutes", "duration_minutes")})
        for child in template["children"]:
            if not isinstance(child, dict) or not text_value(child.get("title")):
                raise SeriesReconciliationError("Recurring child Activity is invalid.")
            if (
                child.get("requirement_code") not in {"required", "optional"}
                or child.get("session_capture_mode")
                not in {"disabled", "record", "live", "record_and_live"}
                or child.get("reality_mode")
                not in {"manual", "review_on_end", "auto_confirm_outcome"}
            ):
                raise SeriesReconciliationError("Recurring child policy is invalid.")
            if child.get("placement") is not None:
                window(child["placement"])
            planned = child.get("planned_slices")
            if not isinstance(planned, list) or len(planned) > 100:
                raise SeriesReconciliationError("Recurring child Sessions are invalid.")
            for planned_item in planned:
                if not isinstance(planned_item, dict) or not text_value(planned_item.get("name")):
                    raise SeriesReconciliationError("Recurring child Session name is invalid.")
                window(
                    {
                        key: planned_item.get(key)
                        for key in ("start_offset_minutes", "duration_minutes")
                    }
                )
        if "life_area_ref" in template and template["life_area_ref"] is not None:
            try:
                UUID(str(template["life_area_ref"]))
            except (TypeError, ValueError) as exc:
                raise SeriesReconciliationError("Recurring Life Area is invalid.") from exc
    else:
        objectives(structure.get("objectives"))
        kind = structure.get("placement_kind")
        if kind == "timed":
            valid = (
                len(recurrence.wall_times) == 1
                and recurrence.clock_basis_code == "named_zone"
                and type(duration_minutes) is int
                and 1 <= duration_minutes <= 525_600
                and duration_days is None
            )
        elif kind == "all_day":
            valid = (
                len(recurrence.wall_times) == 0
                and recurrence.clock_basis_code == "named_zone"
                and recurrence.zone_id is not None
                and type(duration_days) is int
                and 1 <= duration_days <= 3_660
                and duration_minutes is None
            )
        else:
            valid = False
        if (
            not valid
            or (kind == "all_day" and reminder is not None)
            or structure.get("reality_mode")
            not in {"manual", "review_on_end", "auto_confirm_outcome"}
        ):
            raise SeriesReconciliationError("Recurring Event structure is invalid.")
        if "agenda_parts" not in structure or "life_area_ref" not in structure:
            raise SeriesReconciliationError("Recurring Event structure is incomplete.")
        agenda = structure["agenda_parts"]
        if (
            not isinstance(agenda, list)
            or len(agenda) > 100
            or any(not text_value(part, limit=1000) for part in agenda)
        ):
            raise SeriesReconciliationError("Recurring Event agenda is invalid.")
        area = structure.get("life_area_ref")
        if area is not None:
            try:
                UUID(str(area))
            except (TypeError, ValueError) as exc:
                raise SeriesReconciliationError("Recurring Event Life Area is invalid.") from exc


class RecurringSeriesEditApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._recurrences = RecurrenceApplication(session_factory)
        self._occurrences = OccurrenceApplication(session_factory)
        self._policies = RecurringStructurePolicyApplication(session_factory)
        self._previews = RecurringStructurePreviewApplication(session_factory)
        self._inventories = OccurrenceEditInventoryApplication(session_factory)
        self._initial_routine = RoutineOccurrencePolicyApplication(session_factory)
        self._initial_event = EventOccurrencePolicyApplication(session_factory)

    async def source(
        self, *, self_person_ref: NativeRef, selected_occurrence_ref: UUID
    ) -> RecurringSeriesSource:
        """Hydrate an editor from one current, owner-scoped source snapshot."""
        async with self._session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
            revision = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_occurrence_edit_revision(:actor,:selected)"
                        ),
                        {"actor": self_person_ref, "selected": selected_occurrence_ref},
                    )
                )
                .mappings()
                .one_or_none()
            )
            if revision is None or revision["recurrence_state_ref"] is None:
                raise RecurringSeriesEditConflictError("Recurring source is unavailable.")
            selected_row = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_occurrence(:actor,:selected)"),
                        {"actor": self_person_ref, "selected": selected_occurrence_ref},
                    )
                )
                .mappings()
                .one_or_none()
            )
            if (
                selected_row is None
                or selected_row["origin_code"] != "recurrence_generated"
                or selected_row["generated_date"] is None
            ):
                raise RecurringSeriesEditConflictError("Selected calendar instance is unavailable.")
            source_ref = UUID(str(revision["source_native_ref"]))
            routine = (
                (
                    await session.execute(
                        text(
                            "SELECT title,life_area_ref FROM dante.list_self_routines(:actor) "
                            "WHERE routine_ref=:source"
                        ),
                        {"actor": self_person_ref, "source": source_ref},
                    )
                )
                .mappings()
                .one_or_none()
            )
            owner: SeriesOwner = "routine" if routine is not None else "event"
            recurrence_query = (
                text("SELECT * FROM dante.get_self_routine_recurrence(:actor,:source)")
                if owner == "routine"
                else text("SELECT * FROM dante.get_self_event_recurrence(:actor,:source)")
            )
            row = (
                (
                    await session.execute(
                        recurrence_query,
                        {"actor": self_person_ref, "source": source_ref},
                    )
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise RecurringSeriesEditConflictError("Recurring source is unavailable.")
            recurrence_view = _view(row)
            if recurrence_view.material_state_ref != revision[
                "recurrence_state_ref"
            ] or not isinstance(recurrence_view.recurrence, CalendarRecurrence):
                raise RecurringSeriesEditConflictError("Recurring source changed. Reload Edit.")
            structure = await self._policies.get_snapshot_in_session(
                session,
                self_person_ref=self_person_ref,
                owner=owner,
                source_ref=source_ref,
                recurrence_state_ref=recurrence_view.material_state_ref,
            )
            if owner == "routine":
                initial = await self._initial_routine.get_in_session(
                    session, self_person_ref=self_person_ref, routine_ref=source_ref
                )
                if initial is None or not initial.activity_template:
                    raise RecurringSeriesEditConflictError(
                        "Activity source has no complete template."
                    )
                structure = structure or {
                    "version": 1,
                    "duration_minutes": initial.duration_minutes,
                    "reminder_lead_minutes": initial.reminder_lead_minutes,
                    "activity_template": {
                        **initial.activity_template,
                        "life_area_ref": (
                            str(routine["life_area_ref"])
                            if routine["life_area_ref"] is not None
                            else None
                        ),
                    },
                }
                title = str(routine["title"])
                template_description = structure["activity_template"]
                if not isinstance(template_description, dict):
                    raise RecurringSeriesEditConflictError("Activity template is invalid.")
                description = template_description.get("description")
                location = template_description.get("location")
                color_code = template_description.get("item_color_code")
            else:
                initial_event = await self._initial_event.get_in_session(
                    session, self_person_ref=self_person_ref, event_ref=source_ref
                )
                event = await _read_event_in_session(
                    session, self_person_ref=self_person_ref, event_ref=NativeRef(source_ref)
                )
                if initial_event is None or event is None:
                    raise RecurringSeriesEditConflictError("Event source is unavailable.")
                structure = structure or {
                    "version": 1,
                    "placement_kind": initial_event.placement_kind,
                    "duration_minutes": initial_event.duration_minutes,
                    "duration_days": initial_event.duration_days,
                    "reminder_lead_minutes": initial_event.reminder_lead_minutes,
                    "reality_mode": initial_event.reality_mode,
                    "objectives": list(initial_event.objectives),
                }
                structure = {
                    **structure,
                    "agenda_parts": structure.get("agenda_parts", list(event.agenda_parts)),
                    "life_area_ref": structure.get(
                        "life_area_ref", str(event.life_area_ref) if event.life_area_ref else None
                    ),
                }
                title = event.title
                description = event.description
                location = event.location
                color_code = event.color_code
            _validate_structure(owner, recurrence_view.recurrence, structure)
            return RecurringSeriesSource(
                source_ref=source_ref,
                owner=owner,
                edit_revision=int(revision["edit_revision"]),
                recurrence_state_ref=recurrence_view.material_state_ref,
                recurrence=recurrence_view.recurrence,
                structure_snapshot=structure,
                title=title,
                selected_date=selected_row["generated_date"],
                description=description if isinstance(description, str) else None,
                location=location if isinstance(location, str) else None,
                color_code=color_code if isinstance(color_code, str) else None,
            )

    async def preview(
        self,
        *,
        self_person_ref: NativeRef,
        selected_occurrence_ref: UUID,
        requested_scope: SeriesScope,
        expected_revision: int,
        expected_state_ref: UUID,
        effective_zone_id: str,
        proposed_recurrence: CalendarRecurrence,
        proposed_structure: dict[str, object],
        profile_patch: dict[str, str | None] | None = None,
    ) -> RecurringSeriesPrepared:
        async with self._session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"))
            return await self.prepare_in_session(
                session,
                self_person_ref=self_person_ref,
                selected_occurrence_ref=selected_occurrence_ref,
                requested_scope=requested_scope,
                expected_revision=expected_revision,
                expected_state_ref=expected_state_ref,
                effective_zone_id=effective_zone_id,
                proposed_recurrence=proposed_recurrence,
                proposed_structure=proposed_structure,
                profile_patch=profile_patch,
            )

    async def accept(
        self,
        *,
        self_person_ref: NativeRef,
        selected_occurrence_ref: UUID,
        requested_scope: SeriesScope,
        expected_revision: int,
        expected_state_ref: UUID,
        effective_zone_id: str,
        proposed_recurrence: CalendarRecurrence,
        proposed_structure: dict[str, object],
        profile_patch: dict[str, str | None] | None,
        expected_fingerprint: str,
        operation_id: str,
    ) -> RecurringSeriesAccepted:
        """Accept source and materialized-plan transitions in one transaction."""
        request_hash = _request_hash(
            self_person_ref=self_person_ref,
            selected_occurrence_ref=selected_occurrence_ref,
            requested_scope=requested_scope,
            expected_revision=expected_revision,
            expected_state_ref=expected_state_ref,
            effective_zone_id=effective_zone_id,
            proposed_recurrence=proposed_recurrence,
            proposed_structure=proposed_structure,
            profile_patch=profile_patch,
        )
        try:
            async with self._session_factory() as session, session.begin():
                await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                prior = (
                    (
                        await session.execute(
                            text(
                                "SELECT * FROM dante.get_self_recurring_structure_policy_operation("
                                ":actor,:operation)"
                            ),
                            {"actor": self_person_ref, "operation": operation_id},
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
                if prior is not None:
                    if (
                        prior["request_hash"] != request_hash
                        or prior["preview_fingerprint"] != expected_fingerprint
                        or prior["previous_state_ref"] != expected_state_ref
                    ):
                        raise RecurringSeriesEditConflictError("Operation id was reused.")
                    return RecurringSeriesAccepted(
                        source_ref=prior["source_native_ref"],
                        recurrence_state_ref=prior["recurrence_state_ref"],
                        superseded_count=prior["superseded_count"],
                        protected_count=prior["protected_count"],
                        replayed=True,
                    )
                prepared = await self.prepare_in_session(
                    session,
                    self_person_ref=self_person_ref,
                    selected_occurrence_ref=selected_occurrence_ref,
                    requested_scope=requested_scope,
                    expected_revision=expected_revision,
                    expected_state_ref=expected_state_ref,
                    effective_zone_id=effective_zone_id,
                    proposed_recurrence=proposed_recurrence,
                    proposed_structure=proposed_structure,
                    profile_patch=profile_patch,
                )
                if prepared.fingerprint != expected_fingerprint:
                    raise RecurringSeriesEditConflictError(
                        "Series preview changed before acceptance."
                    )
                if profile_patch:
                    await session.execute(
                        text(
                            "SELECT * FROM dante.accept_self_occurrence_profile_edit_previewed("
                            ":actor,:selected,:operation,:revision,:state,:scope,:zone,"
                            "CAST(:patch AS jsonb),:fingerprint)"
                        ),
                        {
                            "actor": self_person_ref,
                            "selected": selected_occurrence_ref,
                            "operation": _child_operation(operation_id, "profile"),
                            "revision": expected_revision,
                            "state": expected_state_ref,
                            "scope": requested_scope,
                            "zone": effective_zone_id,
                            "patch": json.dumps(profile_patch, sort_keys=True),
                            "fingerprint": prepared.source_fingerprint,
                        },
                    )
                replacement = await self._recurrences.replace_in_session(
                    session,
                    owner=prepared.owner,
                    self_person_ref=self_person_ref,
                    owner_ref=prepared.source_ref,
                    operation_id=_child_operation(operation_id, "recurrence"),
                    expected_material_state_ref=expected_state_ref,
                    recurrence=proposed_recurrence,
                )
                new_state = replacement.recurrence.material_state_ref
                for index, ref in enumerate(prepared.scope.target_occurrence_refs):
                    await self._policies.supersede_clean_in_session(
                        session,
                        self_person_ref=self_person_ref,
                        occurrence_ref=ref,
                        source_ref=prepared.source_ref,
                        replacement_state_ref=new_state,
                        operation_id=_child_operation(operation_id, f"supersede:{index}"),
                        effective_zone_id=effective_zone_id,
                    )
                for index, coordinate in enumerate(
                    prepared.reconciliation.protected_matching_coordinates
                ):
                    await self._occurrences.exclude_in_session(
                        session,
                        owner=prepared.owner,
                        self_person_ref=self_person_ref,
                        source_ref=prepared.source_ref,
                        governing_recurrence_state_ref=new_state,
                        operation_id=_child_operation(operation_id, f"exception:{index}"),
                        coordinate=coordinate,
                    )
                await self._policies.replace_in_session(
                    session,
                    self_person_ref=self_person_ref,
                    owner=prepared.owner,
                    source_ref=prepared.source_ref,
                    previous_state_ref=expected_state_ref,
                    recurrence_state_ref=new_state,
                    operation_id=operation_id,
                    structure_snapshot=proposed_structure,
                    request_hash=request_hash,
                    preview_fingerprint=expected_fingerprint,
                    superseded_count=len(prepared.scope.target_occurrence_refs),
                    protected_count=len(prepared.scope.protected_future_occurrence_refs),
                )
                return RecurringSeriesAccepted(
                    source_ref=prepared.source_ref,
                    recurrence_state_ref=new_state,
                    superseded_count=len(prepared.scope.target_occurrence_refs),
                    protected_count=len(prepared.scope.protected_future_occurrence_refs),
                )
        except SQLAlchemyError as exc:
            raise RecurringSeriesEditConflictError("Series changed during acceptance.") from exc

    async def prepare_in_session(
        self,
        session: AsyncSession,
        *,
        self_person_ref: NativeRef,
        selected_occurrence_ref: UUID,
        requested_scope: SeriesScope,
        expected_revision: int,
        expected_state_ref: UUID,
        effective_zone_id: str,
        proposed_recurrence: CalendarRecurrence,
        proposed_structure: dict[str, object],
        profile_patch: dict[str, str | None] | None = None,
    ) -> RecurringSeriesPrepared:
        """Re-read every materialized source instance under one admission lock.

        The caller opens a transaction and repeats this preparation on accept.
        It must retain the same session until all canonical writes commit.
        """
        selected_row = (
            (
                await session.execute(
                    text("SELECT * FROM dante.get_self_occurrence(:actor,:selected)"),
                    {"actor": self_person_ref, "selected": selected_occurrence_ref},
                )
            )
            .mappings()
            .one_or_none()
        )
        if selected_row is None:
            raise RecurringSeriesEditConflictError("Selected instance is no longer available.")
        selected = _occurrence(selected_row)
        source_ref = selected.source_native_ref
        await session.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:key,0))"),
            {"key": f"dante:recurrence-materialization:{source_ref}"},
        )
        routine_owned = await session.scalar(
            text(
                "SELECT EXISTS(SELECT 1 FROM dante.list_self_routines(:actor) "
                "WHERE routine_ref=:source)"
            ),
            {"actor": self_person_ref, "source": source_ref},
        )
        owner: SeriesOwner = "routine" if routine_owned else "event"
        _validate_structure(owner, proposed_recurrence, proposed_structure)
        inventory = await self._inventories.read_in_session(
            session,
            self_person_ref=self_person_ref,
            selected_occurrence_ref=selected_occurrence_ref,
        )
        by_ref: dict[UUID, CalendarCoordinate] = {}
        for item in inventory.occurrences:
            if item.origin_code != "recurrence_generated":
                continue
            if not isinstance(item.coordinate, CalendarCoordinate):
                raise SeriesReconciliationError("Only calendar series can use this editor.")
            by_ref[item.occurrence_ref] = item.coordinate
        if not by_ref:
            raise SeriesReconciliationError("No generated calendar instances are available.")
        selected_coordinate = by_ref.get(selected_occurrence_ref)
        if selected_coordinate is None:
            raise RecurringSeriesEditConflictError("Selected instance has no calendar coordinate.")
        if proposed_recurrence.effective_from < selected_coordinate.generated_date:
            raise SeriesReconciliationError("Revised cadence begins before the selected boundary.")
        if (
            requested_scope == "from_next"
            and proposed_recurrence.effective_from <= selected_coordinate.generated_date
        ):
            raise SeriesReconciliationError("From-next cadence must begin after the selected day.")
        earliest = min(item.generated_date for item in by_ref.values())
        latest = max(item.generated_date for item in by_ref.values())
        try:
            window = SeriesReconciliationWindow(earliest, latest + timedelta(days=1))
        except OverflowError as exc:
            raise SeriesReconciliationError(
                "Materialized horizon exceeds calendar bounds."
            ) from exc
        preview = await self._previews.preview_in_session(
            session,
            self_person_ref=self_person_ref,
            selected_occurrence_ref=selected_occurrence_ref,
            scope_code=requested_scope,
            proposed_recurrence=proposed_recurrence,
            window=window,
            effective_zone_id=effective_zone_id,
        )
        if (
            preview.source_native_ref != source_ref
            or preview.profile_edit_revision != expected_revision
            or preview.recurrence_state_ref != expected_state_ref
        ):
            raise RecurringSeriesEditConflictError("Series preview has changed.")
        protected_detail: tuple[tuple[UUID, ProtectionReason, datetime], ...] = tuple(
            (
                UUID(str(entry["occurrence_ref"])),
                _protection_reason(str(entry["reason"])),
                datetime.fromisoformat(str(entry["expected_at"])),
            )
            for entry in preview.protected_occurrences
        )
        protected = tuple((ref, reason) for ref, reason, _ in protected_detail)
        scope = preview.scope_plan
        if set(scope.target_occurrence_refs) & set(scope.protected_future_occurrence_refs):
            raise RecurringSeriesEditConflictError("Future target and exception sets overlap.")
        reconciliation = preview.reconciliation
        intent = {
            "source": str(source_ref),
            "selected": str(selected_occurrence_ref),
            "scope": requested_scope,
            "source_fingerprint": preview.source_preview_fingerprint,
            "structural_fingerprint": preview.proposed_preview_fingerprint,
            "recurrence": asdict(proposed_recurrence),
            "structure": proposed_structure,
            "profile_patch": profile_patch,
            "reconciled_targets": [str(ref) for ref in scope.target_occurrence_refs],
            "protected": [(str(ref), reason) for ref, reason in protected],
        }
        fingerprint = hashlib.sha256(
            json.dumps(intent, sort_keys=True, default=str, separators=(",", ":")).encode()
        ).hexdigest()
        return RecurringSeriesPrepared(
            source_ref=source_ref,
            owner=owner,
            selected_ref=selected_occurrence_ref,
            prior_state_ref=expected_state_ref,
            scope=scope,
            reconciliation=reconciliation,
            fingerprint=fingerprint,
            source_fingerprint=preview.source_preview_fingerprint,
            protected_occurrences=protected_detail,
        )
