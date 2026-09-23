"""B06-D PostgreSQL proof for atomic source + Recurrence authoring."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import pytest
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication
from dante.modules.temporal.recurring_authoring import (
    RecurringAuthoringApplication,
    RecurringAuthoringOperationReuseError,
)
from dante.modules.temporal.routine import RoutineApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _weekly(*weekdays: int) -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 10, 1),
        effective_until=None,
        pattern_code="weekly_weekdays",
        interval_count=1,
        clock_basis_code="floating_local",
        zone_id=None,
        pattern_anchor_date=None,
        wall_times=(time(8),),
        weekdays=weekdays,
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy=None,
        ambiguous_local_time_policy=None,
        step_unit_code=None,
    )


@pytest.mark.asyncio
async def test_recurring_routine_authoring_is_atomic_replayable_and_self_scoped(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b06-d:authoring:routine:area",
                name="Salute",
            )
        ).area
        requested = _weekly(1, 3, 5)
        created = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="b06-d:authoring:routine",
            title="Allenamento",
            life_area_ref=area.life_area_ref,
            recurrence=requested,
        )
        assert created.owner_kind == "routine"
        assert not created.replayed

        current = await recurrences.get(
            owner="routine",
            self_person_ref=alice,
            owner_ref=created.source_ref,
        )
        assert current is not None
        assert current.material_state_ref == created.recurrence_material_state_ref
        assert current.recurrence == requested
        assert [item.routine_ref for item in await routines.list(self_person_ref=alice)] == [
            created.source_ref
        ]

        replay = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="b06-d:authoring:routine",
            title="Allenamento",
            life_area_ref=area.life_area_ref,
            recurrence=requested,
        )
        assert replay.replayed
        assert replay.source_ref == created.source_ref
        assert replay.recurrence_material_state_ref == created.recurrence_material_state_ref

        with pytest.raises(RecurringAuthoringOperationReuseError):
            await authoring.create_routine(
                self_person_ref=alice,
                operation_id="b06-d:authoring:routine",
                title="Allenamento",
                life_area_ref=area.life_area_ref,
                recurrence=_weekly(2, 4),
            )

        assert (
            await recurrences.get(
                owner="routine",
                self_person_ref=bob,
                owner_ref=created.source_ref,
            )
            is None
        )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_event_authoring_commits_source_and_recurrence_together(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b06-d:authoring:event:area",
                name="Lavoro",
            )
        ).area
        requested = _weekly(2, 4)
        created = await authoring.create_event(
            self_person_ref=alice,
            operation_id="b06-d:authoring:event",
            title="Sync progetto",
            life_area_ref=area.life_area_ref,
            agenda_parts=("Stato", "Blocchi"),
            recurrence=requested,
        )
        assert created.owner_kind == "event"
        assert not created.replayed

        event_ref = NativeRef(created.source_ref)
        event = await events.get_event(self_person_ref=alice, event_ref=event_ref)
        assert event is not None
        assert event.title == "Sync progetto"
        assert event.agenda_parts == ("Stato", "Blocchi")
        current = await recurrences.get(
            owner="event",
            self_person_ref=alice,
            owner_ref=created.source_ref,
        )
        assert current is not None
        assert current.recurrence == requested
        assert current.material_state_ref == created.recurrence_material_state_ref

        replay = await authoring.create_event(
            self_person_ref=alice,
            operation_id="b06-d:authoring:event",
            title="Sync progetto",
            life_area_ref=area.life_area_ref,
            agenda_parts=("Stato", "Blocchi"),
            recurrence=requested,
        )
        assert replay.replayed
        assert replay.source_ref == created.source_ref

        with pytest.raises(RecurringAuthoringOperationReuseError):
            await authoring.create_event(
                self_person_ref=alice,
                operation_id="b06-d:authoring:event",
                title="Sync progetto",
                life_area_ref=area.life_area_ref,
                agenda_parts=("Stato", "Blocchi"),
                recurrence=_weekly(1),
            )

        assert await events.get_event(self_person_ref=bob, event_ref=event_ref) is None
        assert (
            await recurrences.get(
                owner="event",
                self_person_ref=bob,
                owner_ref=created.source_ref,
            )
            is None
        )
    finally:
        await runtime.dispose()
