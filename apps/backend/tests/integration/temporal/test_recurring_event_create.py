"""B14 recurring Event Create: policy, Occurrence Schedule and Reminder proof."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import date, time
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_schedule_place import _context

from dante.context.contracts import DanteContext
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineScheduledOccurrenceItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.event import _read_event_in_session
from dante.modules.temporal.event_occurrence_policy import (
    EventOccurrencePolicyApplication,
    EventOccurrencePolicyConflictError,
)
from dante.modules.temporal.occurrence_api import (
    EventOccurrenceLocalEditCommand,
    accept_event_occurrence_local_edit,
    get_recurring_event_occurrence_detail,
    get_recurring_event_occurrence_expected_participation,
)
from dante.modules.temporal.placement_lock import (
    PlacementLockApplication,
    PlacementLockNotFoundError,
)
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication
from dante.modules.temporal.recurring_authoring import (
    EventAuthoringPolicy,
    RecurringAuthoringApplication,
)
from dante.modules.temporal.recurring_series_edit import RecurringSeriesEditApplication
from dante.modules.temporal.recurring_structure_policy import RecurringStructurePolicyApplication
from dante.modules.temporal.responsibility_participation import (
    ResponsibilityParticipationApplication,
)
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.modules.temporal.schedule_reminder import ScheduleReminderApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_event_occurrence_local_structure_is_versioned_and_does_not_mutate_source(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    try:
        created = await authoring.create_event(
            self_person_ref=alice,
            operation_id="event:local:create",
            title="Event source",
            life_area_intent=None,
            agenda_parts=("Originale",),
            description=None,
            location=None,
            item_color_code=None,
            recurrence=_daily_named_zone(),
        )
        await policies.set(
            self_person_ref=alice,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=None,
        )
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="event:local:window",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 4),
            effective_zone_id="Europe/Rome",
        )
        window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2), end_date_exclusive=date(2027, 1, 4)
            ),
            context=_context(alice),
        )
        occurrences = [
            item.occurrence_ref
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert len(occurrences) == 2
        selected, other = occurrences
        scheduled = {
            item.occurrence_ref: item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        }
        async with runtime.session_factory() as session, session.begin():
            schedule_identity = text(
                "SELECT dante.is_self_event_occurrence_schedule(:actor,:occurrence,:schedule)"
            )
            assert (
                await session.scalar(
                    schedule_identity,
                    {
                        "actor": alice,
                        "occurrence": selected,
                        "schedule": scheduled[selected].schedule_ref,
                    },
                )
                is True
            )
            assert (
                await session.scalar(
                    schedule_identity,
                    {
                        "actor": alice,
                        "occurrence": selected,
                        "schedule": scheduled[other].schedule_ref,
                    },
                )
                is False
            )
            assert (
                await session.scalar(
                    schedule_identity,
                    {
                        "actor": uuid4(),
                        "occurrence": selected,
                        "schedule": scheduled[selected].schedule_ref,
                    },
                )
                is False
            )
        patch = json.dumps(
            {
                "title": "Event locale",
                "event_local": {
                    "agenda_parts": ["Punto locale"],
                    "life_area_ref": None,
                    "expected_participants": [
                        {"person_ref": "self", "requirement_code": "required"}
                    ],
                },
            }
        )
        async with runtime.session_factory() as session, session.begin():
            params = {
                "actor": alice,
                "selected": selected,
                "operation": "event:local:edit",
                "expected": 0,
                "recurrence": created.recurrence_material_state_ref,
                "zone": "Europe/Rome",
                "patch": patch,
            }
            sql = text(
                "SELECT * FROM dante.accept_self_occurrence_profile_edit("
                ":actor,:selected,:operation,:expected,:recurrence,'only_this',"
                ":zone,CAST(:patch AS jsonb))"
            )
            accepted = (await session.execute(sql, params)).mappings().one()
            assert accepted["revision"] == 1
            assert not accepted["replayed"]
            replay = (await session.execute(sql, params)).mappings().one()
            assert replay["replayed"]
            selected_patch = await session.scalar(
                text("SELECT dante.get_self_occurrence_profile_patch(:actor,:occurrence)"),
                {"actor": alice, "occurrence": selected},
            )
            other_patch = await session.scalar(
                text("SELECT dante.get_self_occurrence_profile_patch(:actor,:occurrence)"),
                {"actor": alice, "occurrence": other},
            )
            assert selected_patch == json.loads(patch)
            assert other_patch == {}
            source_event = await _read_event_in_session(
                session, self_person_ref=alice, event_ref=NativeRef(created.source_ref)
            )
            assert source_event is not None
            assert source_event.agenda_parts == ("Originale",)
        context = cast(
            DanteContext,
            SimpleNamespace(self_person_ref=alice, effective_zone_id="Europe/Rome"),
        )
        request = Request(
            {
                "type": "http",
                "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
            }
        )
        payload: dict[str, Any] = {
            "operation_id": "event:local:aggregate",
            "expected_revision": 1,
            "expected_recurrence_state_ref": created.recurrence_material_state_ref,
            "profile_patch": {"title": "Event aggiornato"},
            "structure": {
                "agenda_parts": ["Punto locale aggiornato"],
                "life_area_ref": None,
                "expected_participants": [{"person_ref": "self", "requirement_code": "required"}],
            },
            "schedule": {
                "schedule_ref": scheduled[selected].schedule_ref,
                "expected_material_state_ref": scheduled[selected].placement_material_state_ref,
                "placement": {
                    "kind": "named_zone_local_interval",
                    "starts_local_at": "2027-01-02T12:00:00",
                    "ends_local_at": "2027-01-02T13:00:00",
                    "zone_id": "Europe/Rome",
                },
            },
            "objectives": {
                "add": [
                    {
                        "operation_id": "event:local:objective",
                        "label": "Esito locale",
                        "result_kind": "boolean",
                        "presentation_order": 0,
                    }
                ]
            },
        }
        with pytest.raises(ProblemError):
            await accept_event_occurrence_local_edit(
                selected,
                EventOccurrenceLocalEditCommand.model_validate(
                    {
                        **payload,
                        "schedule": {
                            **payload["schedule"],
                            "schedule_ref": scheduled[other].schedule_ref,
                        },
                    }
                ),
                context,
                request,
                Response(),
            )
        async with runtime.session_factory() as session, session.begin():
            revision_after_refusal = await session.scalar(
                text(
                    "SELECT edit_revision FROM dante.get_self_occurrence_edit_revision("
                    ":actor,:occurrence)"
                ),
                {"actor": alice, "occurrence": selected},
            )
            assert revision_after_refusal == 1
            assert (
                await session.scalar(
                    text(
                        "SELECT count(*) FROM dante.list_self_temporal_objectives("
                        ":actor,'occurrence',:occurrence)"
                    ),
                    {"actor": alice, "occurrence": selected},
                )
                == 0
            )
        local_accepted = await accept_event_occurrence_local_edit(
            selected,
            EventOccurrenceLocalEditCommand.model_validate(payload),
            context,
            request,
            Response(),
        )
        assert local_accepted.revision == 2
        local_replay = await accept_event_occurrence_local_edit(
            selected,
            EventOccurrenceLocalEditCommand.model_validate(payload),
            context,
            request,
            Response(),
        )
        assert local_replay.replayed
        assert local_replay.revision == local_accepted.revision
        detail = await get_recurring_event_occurrence_detail(selected, context, request, Response())
        assert detail.title == "Event aggiornato"
        assert detail.agenda_parts == ["Punto locale aggiornato"]
        participants = await get_recurring_event_occurrence_expected_participation(
            selected, context, request, Response()
        )
        assert len(participants) == 1
        assert participants[0].participant_is_self
        assert participants[0].requirement_code == "required"
        untouched = await get_recurring_event_occurrence_detail(other, context, request, Response())
        assert untouched.title == "Event source"
        assert untouched.agenda_parts == ["Originale"]
        async with runtime.session_factory() as session, session.begin():
            objective_count = await session.scalar(
                text(
                    "SELECT count(*) FROM dante.list_self_temporal_objectives("
                    ":actor,'occurrence',:occurrence)"
                ),
                {"actor": alice, "occurrence": selected},
            )
            assert objective_count == 1
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "new_clock", [time(8), time(11)], ids=["earlier_selected", "later_selected"]
)
async def test_series_accept_replaces_one_clean_future_event_without_duplicate(
    migrated_database: Any,
    new_clock: time,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    series = RecurringSeriesEditApplication(runtime.session_factory)
    participation = ResponsibilityParticipationApplication(runtime.session_factory)
    try:
        original = _daily_named_zone()
        created = await authoring.create_event(
            self_person_ref=alice,
            operation_id="structure:accept:create",
            title="Lezione ricorrente",
            life_area_intent=None,
            agenda_parts=(),
            description=None,
            location=None,
            item_color_code=None,
            recurrence=original,
        )
        await policies.set(
            self_person_ref=alice,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=None,
        )
        await participation.set_expected_participation(
            self_person_ref=alice,
            operation_id="structure:accept:participant",
            event_ref=NativeRef(created.source_ref),
            participant_person_ref=alice,
            requirement_code="required",
            expected_requirement_code=None,
        )
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="structure:accept:old",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 3),
            effective_zone_id="Europe/Rome",
        )
        query = TimelineWindowQuery(
            start_date=date(2027, 1, 2), end_date_exclusive=date(2027, 1, 3)
        )
        before = await timeline.read_window(query=query, context=_context(alice))
        old_items = [
            item
            for item in before.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert len(old_items) == 1
        loaded = await series.source(
            self_person_ref=alice,
            selected_occurrence_ref=old_items[0].occurrence_ref,
        )
        assert loaded.source_ref == created.source_ref
        assert loaded.recurrence_state_ref == created.recurrence_material_state_ref
        assert loaded.structure_snapshot["duration_minutes"] == 60
        assert loaded.structure_snapshot["agenda_parts"] == []
        assert loaded.structure_snapshot["life_area_ref"] is None
        assert loaded.structure_snapshot["expected_participants"] == [
            {"person_ref": "self", "requirement_code": "required"}
        ]
        proposed = replace(original, effective_from=date(2027, 1, 2), wall_times=(new_clock,))
        structure = {
            "version": 1,
            "placement_kind": "timed",
            "duration_minutes": 120,
            "duration_days": None,
            "reminder_lead_minutes": None,
            "reality_mode": "manual",
            "objectives": [],
            "agenda_parts": ["Presentazione"],
            "life_area_ref": None,
            "expected_participants": [],
        }
        preview = await series.preview(
            self_person_ref=alice,
            selected_occurrence_ref=old_items[0].occurrence_ref,
            requested_scope="this_and_following",
            expected_revision=0,
            expected_state_ref=created.recurrence_material_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposed,
            proposed_structure=structure,
            profile_patch={"title": "Lezione della serie aggiornata"},
        )
        assert preview.scope.target_occurrence_refs == (old_items[0].occurrence_ref,)
        accepted = await series.accept(
            self_person_ref=alice,
            selected_occurrence_ref=old_items[0].occurrence_ref,
            requested_scope="this_and_following",
            expected_revision=0,
            expected_state_ref=created.recurrence_material_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposed,
            proposed_structure=structure,
            profile_patch={"title": "Lezione della serie aggiornata"},
            expected_fingerprint=preview.fingerprint,
            operation_id="structure:accept:operation",
        )
        assert accepted.superseded_count == 1
        replay = await series.accept(
            self_person_ref=alice,
            selected_occurrence_ref=old_items[0].occurrence_ref,
            requested_scope="this_and_following",
            expected_revision=0,
            expected_state_ref=created.recurrence_material_state_ref,
            effective_zone_id="Europe/Rome",
            proposed_recurrence=proposed,
            proposed_structure=structure,
            profile_patch={"title": "Lezione della serie aggiornata"},
            expected_fingerprint=preview.fingerprint,
            operation_id="structure:accept:operation",
        )
        assert replay.replayed
        assert replay.recurrence_state_ref == accepted.recurrence_state_ref
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="structure:accept:new",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 3),
            effective_zone_id="Europe/Rome",
        )
        after = await timeline.read_window(query=query, context=_context(alice))
        current = [
            item
            for item in after.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert len(current) == 1
        assert current[0].occurrence_ref != old_items[0].occurrence_ref
        assert isinstance(current[0].placement, NamedZoneLocalIntervalPlacement)
        assert current[0].placement.starts_local_at.time() == new_clock
        assert current[0].placement.ends_local_at.time() == time(new_clock.hour + 2)
        # A replaced selected Occurrence must inherit its own accepted title,
        # even if the revised start clock moved *before* the prior anchor.
        assert current[0].title == "Lezione della serie aggiornata"
        revised_source = await series.source(
            self_person_ref=alice, selected_occurrence_ref=current[0].occurrence_ref
        )
        assert revised_source.structure_snapshot["agenda_parts"] == ["Presentazione"]
        assert revised_source.structure_snapshot["expected_participants"] == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_revised_event_structure_follows_governing_recurrence_state(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    locks = PlacementLockApplication(runtime.session_factory)
    revisions = RecurringStructurePolicyApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    try:
        initial = _daily_named_zone()
        created = await authoring.create_event(
            self_person_ref=alice,
            operation_id="structure:event:create",
            title="Lezione ricorrente",
            life_area_intent=None,
            agenda_parts=("Introduzione",),
            description=None,
            location=None,
            item_color_code=None,
            recurrence=initial,
        )
        await policies.set(
            self_person_ref=alice,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=None,
        )
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="structure:event:old-window",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 3),
            effective_zone_id="Europe/Rome",
        )
        before = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2), end_date_exclusive=date(2027, 1, 3)
            ),
            context=_context(alice),
        )
        previous = [
            item
            for item in before.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert len(previous) == 1
        assert isinstance(previous[0].placement, NamedZoneLocalIntervalPlacement)
        assert previous[0].placement.ends_local_at.time() == time(11)
        old_state = created.recurrence_material_state_ref
        snapshot = {
            "version": 1,
            "placement_kind": "timed",
            "duration_minutes": 120,
            "duration_days": None,
            "reminder_lead_minutes": None,
            "reality_mode": "manual",
            "objectives": [],
            "placement_protected": True,
        }
        async with runtime.session_factory() as session, session.begin():
            changed = await recurrences.replace_in_session(
                session,
                owner="event",
                self_person_ref=alice,
                owner_ref=created.source_ref,
                operation_id="structure:event:recurrence",
                expected_material_state_ref=old_state,
                recurrence=replace(initial, effective_from=date(2027, 1, 2)),
            )
            accepted = await revisions.replace_in_session(
                session,
                self_person_ref=alice,
                owner="event",
                source_ref=created.source_ref,
                previous_state_ref=old_state,
                recurrence_state_ref=changed.recurrence.material_state_ref,
                operation_id="structure:event:policy",
                structure_snapshot=snapshot,
                request_hash="0" * 64,
                preview_fingerprint="1" * 64,
                superseded_count=1,
                protected_count=0,
            )
            assert not accepted.replayed
            retired = await revisions.supersede_clean_in_session(
                session,
                self_person_ref=alice,
                occurrence_ref=previous[0].occurrence_ref,
                source_ref=created.source_ref,
                replacement_state_ref=changed.recurrence.material_state_ref,
                operation_id="structure:event:supersede",
                effective_zone_id="Europe/Rome",
            )
            assert not retired.replayed
        assert (
            await revisions.event(
                self_person_ref=bob,
                event_ref=created.source_ref,
                recurrence_state_ref=changed.recurrence.material_state_ref,
            )
            is None
        )
        assert (
            await revisions.event(
                self_person_ref=alice,
                event_ref=created.source_ref,
                recurrence_state_ref=old_state,
            )
            is None
        )
        policy = await revisions.event(
            self_person_ref=alice,
            event_ref=created.source_ref,
            recurrence_state_ref=changed.recurrence.material_state_ref,
        )
        assert policy is not None
        assert policy.duration_minutes == 120
        assert policy.placement_protected is True
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="structure:event:window",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 3),
            effective_zone_id="Europe/Rome",
        )
        window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2), end_date_exclusive=date(2027, 1, 3)
            ),
            context=_context(alice),
        )
        items = [
            item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert len(items) == 1
        assert items[0].occurrence_ref != previous[0].occurrence_ref
        assert isinstance(items[0].placement, NamedZoneLocalIntervalPlacement)
        assert items[0].placement.starts_local_at.time() == time(10)
        assert items[0].placement.ends_local_at.time() == time(12)
        revised_lock = await locks.get(self_person_ref=alice, schedule_ref=items[0].schedule_ref)
        assert revised_lock.locked is True
        assert revised_lock.revision > 0
    finally:
        await runtime.dispose()

@pytest.mark.asyncio
async def test_protected_recurring_event_create_replay_and_manual_unlock_are_preserved(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    locks = PlacementLockApplication(runtime.session_factory)
    policy = EventAuthoringPolicy(
        placement_kind="timed",
        duration_minutes=45,
        duration_days=None,
        reminder_lead_minutes=None,
        reality_mode="manual",
        objectives=(),
        placement_protected=True,
    )
    try:
        created = await authoring.create_event(
            self_person_ref=alice,
            operation_id="event:protected:create",
            title="Evento protetto",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
            policy=policy,
        )
        assert created.replayed is False
        replay = await authoring.create_event(
            self_person_ref=alice,
            operation_id="event:protected:create",
            title="Evento protetto",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
            policy=policy,
        )
        assert replay.replayed is True
        assert replay.source_ref == created.source_ref

        saved = await policies.get(self_person_ref=alice, event_ref=created.source_ref)
        assert saved is not None
        assert saved.placement_protected is True
        assert await policies.get(self_person_ref=bob, event_ref=created.source_ref) is None
        with pytest.raises(EventOccurrencePolicyConflictError):
            await policies.set(
                self_person_ref=alice,
                event_ref=created.source_ref,
                placement_kind="timed",
                duration_minutes=45,
                duration_days=None,
                reminder_lead_minutes=None,
                placement_protected=False,
            )

        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="event:protected:window-initial",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 3),
            effective_zone_id="Europe/Rome",
        )
        before = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2027, 1, 2),
                end_date_exclusive=date(2027, 1, 3),
            ),
            context=_context(alice),
        )
        event_items = [
            item
            for item in before.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_native_ref == created.source_ref
        ]
        assert len(event_items) == 1
        schedule_ref = event_items[0].schedule_ref
        initially_locked = await locks.get(self_person_ref=alice, schedule_ref=schedule_ref)
        assert initially_locked.locked is True
        assert initially_locked.revision >= 1
        with pytest.raises(PlacementLockNotFoundError):
            await locks.get(self_person_ref=bob, schedule_ref=schedule_ref)

        manually_unlocked = await locks.set(
            self_person_ref=alice,
            schedule_ref=schedule_ref,
            locked=False,
            expected_revision=initially_locked.revision,
        )
        assert manually_unlocked.locked is False
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="event:protected:window-recheck",
            start_date=date(2027, 1, 2),
            end_date_exclusive=date(2027, 1, 3),
            effective_zone_id="Europe/Rome",
        )
        preserved = await locks.get(self_person_ref=alice, schedule_ref=schedule_ref)
        assert preserved.locked is False
        assert preserved.revision == manually_unlocked.revision
    finally:
        await runtime.dispose()

def _daily_named_zone() -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 10, 6),
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="named_zone",
        zone_id="Europe/Rome",
        pattern_anchor_date=None,
        wall_times=(time(10),),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy="skip_civil_candidate",
        ambiguous_local_time_policy="earlier",
        step_unit_code=None,
    )


@pytest.mark.asyncio
async def test_recurring_event_policy_materializes_schedule_and_reminder(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    reminders = ScheduleReminderApplication(runtime.session_factory)
    locks = PlacementLockApplication(runtime.session_factory)
    try:
        objectives = (
            {
                "label": "Conferma",
                "result_kind": "boolean",
                "comparator_code": None,
                "target_value": None,
                "target_min": None,
                "target_max": None,
                "unit_code": None,
                "presentation_order": 0,
            },
            {
                "label": "Pezzi",
                "result_kind": "quantity",
                "comparator_code": "gte",
                "target_value": 4,
                "target_min": None,
                "target_max": None,
                "unit_code": "mle",
                "presentation_order": 1,
            },
        )
        created = await authoring.create_event(
            self_person_ref=alice,
            operation_id="b14:event:create",
            title="Sync ricorrente",
            life_area_intent=None,
            agenda_parts=("Stato", "Decisioni"),
            description="Allineamento",
            location="Sala A",
            item_color_code="#EA5C12",
            recurrence=_daily_named_zone(),
        )
        policy = await policies.set(
            self_person_ref=alice,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=15,
            objectives=objectives,
        )
        assert not policy.replayed
        assert policy.duration_minutes == 60
        assert policy.reminder_lead_minutes == 15
        assert policy.placement_protected is False

        replay = await policies.set(
            self_person_ref=alice,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=15,
            objectives=objectives,
        )
        assert replay.replayed
        assert (
            await policies.get(
                self_person_ref=bob,
                event_ref=created.source_ref,
            )
            is None
        )

        checkpoint = await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="b14:event:window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 7),
            effective_zone_id="Europe/Rome",
        )
        assert checkpoint.source_count >= 1
        assert checkpoint.occurrence_count >= 1

        window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2026, 10, 6),
                end_date_exclusive=date(2026, 10, 7),
            ),
            context=_context(alice),
        )
        event_items = [
            item
            for item in window.items
            if isinstance(item, TimelineScheduledOccurrenceItem)
            and item.source_kind == "event"
            and item.source_native_ref == created.source_ref
        ]
        assert len(event_items) == 1
        item = event_items[0]
        lock_state = await locks.get(self_person_ref=alice, schedule_ref=item.schedule_ref)
        assert not lock_state.locked
        with pytest.raises(PlacementLockNotFoundError):
            await locks.get(self_person_ref=bob, schedule_ref=item.schedule_ref)
        locked = await locks.set(
            self_person_ref=alice,
            schedule_ref=item.schedule_ref,
            locked=True,
            expected_revision=None,
        )
        assert locked.locked
        assert locked.revision == 1
        assert isinstance(item.placement, NamedZoneLocalIntervalPlacement)
        assert item.placement.starts_local_at.time() == time(10)
        assert item.placement.ends_local_at.time() == time(11)
        assert item.placement.zone_id == "Europe/Rome"
        async with runtime.session_factory() as session, session.begin():
            objective_count = await session.scalar(
                text(
                    "SELECT count(*) FROM dante.list_self_temporal_objectives("
                    ":actor,'occurrence',:occurrence)"
                ),
                {"actor": alice, "occurrence": item.occurrence_ref},
            )
        assert objective_count == 2

        reminder = await reminders.get(
            self_person_ref=alice,
            schedule_ref=item.schedule_ref,
        )
        assert reminder is not None
        assert reminder.enabled
        assert reminder.lead_minutes == 15

        replay_checkpoint = await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="b14:event:window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 7),
            effective_zone_id="Europe/Rome",
        )
        assert replay_checkpoint.replayed_source_count >= 1
        replay_window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2026, 10, 6),
                end_date_exclusive=date(2026, 10, 7),
            ),
            context=_context(alice),
        )
        replay_event_items = [
            candidate
            for candidate in replay_window.items
            if isinstance(candidate, TimelineScheduledOccurrenceItem)
            and candidate.source_kind == "event"
            and candidate.source_native_ref == created.source_ref
        ]
        assert len(replay_event_items) == 1
        assert replay_event_items[0].schedule_ref == item.schedule_ref

        five_day_checkpoint = await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="b14:event:five-day-window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 11),
            effective_zone_id="Europe/Rome",
        )
        assert five_day_checkpoint.occurrence_count >= 5
        five_day_window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2026, 10, 6),
                end_date_exclusive=date(2026, 10, 11),
            ),
            context=_context(alice),
        )
        assert (
            sum(
                isinstance(candidate, TimelineScheduledOccurrenceItem)
                and candidate.source_native_ref == created.source_ref
                for candidate in five_day_window.items
            )
            == 5
        )
    finally:
        await runtime.dispose()
