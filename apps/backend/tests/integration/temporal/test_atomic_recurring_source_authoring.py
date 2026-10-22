"""B06-D PostgreSQL proof for atomic source + Recurrence + policy authoring."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import psycopg
import pytest
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self

from dante.modules.temporal.authoring import AuthoringLifeAreaIntent
from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.event_occurrence_policy import (
    EventOccurrencePolicyApplication,
    EventOccurrencePolicyConflictError,
    EventOccurrencePolicyInputError,
)
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    RecurrenceApplication,
    RecurrenceNotFoundError,
)
from dante.modules.temporal.recurring_authoring import (
    EventAuthoringPolicy,
    RecurringAuthoringApplication,
    RecurringAuthoringOperationReuseError,
    RoutineAuthoringPolicy,
)
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.routine_occurrence_policy import (
    RoutineOccurrencePolicyApplication,
    RoutineOccurrencePolicyConflictError,
    RoutineOccurrencePolicyInputError,
)
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
    policies = RoutineOccurrencePolicyApplication(runtime.session_factory)
    policy = RoutineAuthoringPolicy(
        duration_minutes=45,
        reminder_lead_minutes=10,
        activity_template={"version": 1, "planned_slices": []},
    )
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
            life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
            recurrence=requested,
            policy=policy,
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
        saved_policy = await policies.get(self_person_ref=alice, routine_ref=created.source_ref)
        assert saved_policy is not None
        assert saved_policy.activity_template == policy.activity_template
        async with runtime.session_factory() as session, session.begin():
            read_in_session = await policies.get_in_session(
                session, self_person_ref=alice, routine_ref=created.source_ref
            )
            assert read_in_session == saved_policy
        assert [item.routine_ref for item in await routines.list(self_person_ref=alice)] == [
            created.source_ref
        ]

        replay = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="b06-d:authoring:routine",
            title="Allenamento",
            life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
            recurrence=requested,
            policy=policy,
        )
        assert replay.replayed
        assert replay.source_ref == created.source_ref
        assert replay.recurrence_material_state_ref == created.recurrence_material_state_ref

        with pytest.raises(RoutineOccurrencePolicyConflictError):
            await authoring.create_routine(
                self_person_ref=alice,
                operation_id="b06-d:authoring:routine",
                title="Allenamento",
                life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
                recurrence=requested,
                policy=RoutineAuthoringPolicy(
                    duration_minutes=60,
                    reminder_lead_minutes=10,
                    activity_template=policy.activity_template,
                ),
            )

        with pytest.raises(RecurringAuthoringOperationReuseError):
            await authoring.create_routine(
                self_person_ref=alice,
                operation_id="b06-d:authoring:routine",
                title="Allenamento",
                life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
                recurrence=_weekly(2, 4),
            )

        with pytest.raises(RecurrenceNotFoundError):
            await recurrences.get(
                owner="routine",
                self_person_ref=bob,
                owner_ref=created.source_ref,
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_routine_authoring_creates_new_life_area_with_appearance_atomically(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    try:
        created = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="b06-d:authoring:routine:new-area",
            title="Allenamento",
            life_area_intent=AuthoringLifeAreaIntent(
                new_name="Corpo",
                color_code="#4285F4",
            ),
            recurrence=_weekly(1, 3, 5),
        )
        routine = next(
            item
            for item in await routines.list(self_person_ref=alice)
            if item.routine_ref == created.source_ref
        )
        assert routine.life_area_ref is not None

        area = next(
            item
            for item in await areas.list(self_person_ref=alice)
            if item.life_area_ref == routine.life_area_ref
        )
        assert area.name == "Corpo"
        assert area.color_code == "#4285F4"

        replay = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="b06-d:authoring:routine:new-area",
            title="Allenamento",
            life_area_intent=AuthoringLifeAreaIntent(
                new_name="Corpo",
                color_code="#4285F4",
            ),
            recurrence=_weekly(1, 3, 5),
        )
        assert replay.replayed
        assert replay.source_ref == created.source_ref

        assert (
            len([item for item in await areas.list(self_person_ref=alice) if item.name == "Corpo"])
            == 1
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
    policies = EventOccurrencePolicyApplication(runtime.session_factory)
    policy = EventAuthoringPolicy(
        placement_kind="timed",
        duration_minutes=30,
        duration_days=None,
        reminder_lead_minutes=5,
        reality_mode="manual",
        objectives=(),
    )
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
            life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
            agenda_parts=("Stato", "Blocchi"),
            recurrence=requested,
            policy=policy,
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
        saved_policy = await policies.get(self_person_ref=alice, event_ref=created.source_ref)
        assert saved_policy is not None
        assert saved_policy.duration_minutes == policy.duration_minutes
        async with runtime.session_factory() as session, session.begin():
            read_in_session = await policies.get_in_session(
                session, self_person_ref=alice, event_ref=created.source_ref
            )
            assert read_in_session == saved_policy

        replay = await authoring.create_event(
            self_person_ref=alice,
            operation_id="b06-d:authoring:event",
            title="Sync progetto",
            life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
            agenda_parts=("Stato", "Blocchi"),
            recurrence=requested,
            policy=policy,
        )
        assert replay.replayed
        assert replay.source_ref == created.source_ref

        with pytest.raises(EventOccurrencePolicyConflictError):
            await authoring.create_event(
                self_person_ref=alice,
                operation_id="b06-d:authoring:event",
                title="Sync progetto",
                life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
                agenda_parts=("Stato", "Blocchi"),
                recurrence=requested,
                policy=EventAuthoringPolicy(
                    placement_kind="timed",
                    duration_minutes=40,
                    duration_days=None,
                    reminder_lead_minutes=5,
                    reality_mode="manual",
                    objectives=(),
                ),
            )

        with pytest.raises(RecurringAuthoringOperationReuseError):
            await authoring.create_event(
                self_person_ref=alice,
                operation_id="b06-d:authoring:event",
                title="Sync progetto",
                life_area_intent=AuthoringLifeAreaIntent(life_area_ref=area.life_area_ref),
                agenda_parts=("Stato", "Blocchi"),
                recurrence=_weekly(1),
            )

        assert await events.get_event(self_person_ref=bob, event_ref=event_ref) is None
        with pytest.raises(RecurrenceNotFoundError):
            await recurrences.get(
                owner="event",
                self_person_ref=bob,
                owner_ref=created.source_ref,
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_routine_invalid_policy_rolls_back_source_and_recurrence(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    try:
        with pytest.raises(RoutineOccurrencePolicyInputError):
            await authoring.create_routine(
                self_person_ref=actor,
                operation_id="recurring:routine:invalid-policy",
                title="Allenamento",
                life_area_intent=None,
                recurrence=_weekly(1),
                policy=RoutineAuthoringPolicy(
                    duration_minutes=0,
                    reminder_lead_minutes=None,
                    activity_template={"version": 1},
                ),
            )
        assert not await routines.list(self_person_ref=actor)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_event_invalid_policy_rolls_back_source_agenda_and_recurrence(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    try:
        with pytest.raises(EventOccurrencePolicyInputError):
            await authoring.create_event(
                self_person_ref=actor,
                operation_id="recurring:event:invalid-policy",
                title="Sync",
                life_area_intent=None,
                agenda_parts=("Ordine del giorno",),
                recurrence=_weekly(2),
                policy=EventAuthoringPolicy(
                    placement_kind="timed",
                    duration_minutes=None,
                    duration_days=None,
                    reminder_lead_minutes=None,
                    reality_mode="manual",
                    objectives=(),
                ),
            )
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.event_expectation WHERE self_person_ref=%s",
                (actor,),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
