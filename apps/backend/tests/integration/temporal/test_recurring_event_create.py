"""B14 recurring Event Create: policy, Occurrence Schedule and Reminder proof."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, time
from typing import Any

import pytest
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_schedule_place import _context

from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineScheduledOccurrenceItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.recurring_series_edit import RecurringSeriesEditApplication
from dante.modules.temporal.recurring_structure_policy import RecurringStructurePolicyApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.modules.temporal.schedule_reminder import ScheduleReminderApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_series_accept_replaces_one_clean_future_event_without_duplicate(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    series = RecurringSeriesEditApplication(runtime.session_factory)
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
        proposed = replace(original, effective_from=date(2027, 1, 2), wall_times=(time(11),))
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
            profile_patch=None,
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
            profile_patch=None,
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
            profile_patch=None,
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
        assert current[0].placement.starts_local_at.time() == time(11)
        assert current[0].placement.ends_local_at.time() == time(13)
        revised_source = await series.source(
            self_person_ref=alice, selected_occurrence_ref=current[0].occurrence_ref
        )
        assert revised_source.structure_snapshot["agenda_parts"] == ["Presentazione"]
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
    try:
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
        )
        assert not policy.replayed
        assert policy.duration_minutes == 60
        assert policy.reminder_lead_minutes == 15

        replay = await policies.set(
            self_person_ref=alice,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=60,
            duration_days=None,
            reminder_lead_minutes=15,
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
        assert isinstance(item.placement, NamedZoneLocalIntervalPlacement)
        assert item.placement.starts_local_at.time() == time(10)
        assert item.placement.ends_local_at.time() == time(11)
        assert item.placement.zone_id == "Europe/Rome"

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
    finally:
        await runtime.dispose()
