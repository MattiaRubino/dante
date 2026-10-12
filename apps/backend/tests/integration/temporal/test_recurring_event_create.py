"""B14 recurring Event Create: policy, Occurrence Schedule and Reminder proof."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import pytest
from tests.integration.temporal.test_b02_schedule_place import _context
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineScheduledOccurrenceItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.recurrence import CalendarRecurrence
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.modules.temporal.schedule_reminder import ScheduleReminderApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


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
        assert await policies.get(
            self_person_ref=bob,
            event_ref=created.source_ref,
        ) is None

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
