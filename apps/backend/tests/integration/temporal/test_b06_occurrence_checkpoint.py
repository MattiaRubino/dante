"""B06-C PostgreSQL proof for canonical Occurrence checkpoint and scopes."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import psycopg
import pytest
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    OccurrenceApplication,
    OccurrenceMaterializedConflictError,
    OccurrenceOperationReuseError,
    OccurrenceSourceInactiveError,
    OccurrenceSourceNotFoundError,
)
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _daily(*, starts_on: date, wall_time: time) -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=starts_on,
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="floating_local",
        zone_id=None,
        pattern_anchor_date=None,
        wall_times=(wall_time,),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy=None,
        ambiguous_local_time_policy=None,
    )


@pytest.mark.asyncio
async def test_checkpoint_replay_revision_extra_skip_exclusion_and_event_reuse(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    try:
        area = (await areas.create(self_person_ref=alice, operation_id="area", name="Casa")).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="routine",
            title="Farmaco",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        initial = await recurrences.get(
            owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref
        )
        assert initial is not None

        first = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:first",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 4),
            effective_zone_id="Europe/Rome",
        )
        assert len(first.occurrences) == 3
        assert not first.replayed
        assert (
            await occurrences.checkpoint(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="checkpoint:first",
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 4),
                effective_zone_id="Europe/Rome",
            )
        ).replayed
        with pytest.raises(OccurrenceOperationReuseError):
            await occurrences.checkpoint(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="checkpoint:first",
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 5),
                effective_zone_id="Europe/Rome",
            )

        empty = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:empty",
            start_date=date(2026, 9, 1),
            end_date_exclusive=date(2026, 9, 2),
            effective_zone_id="Europe/Rome",
        )
        assert empty.occurrences == ()
        assert (
            await occurrences.checkpoint(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="checkpoint:empty",
                start_date=date(2026, 9, 1),
                end_date_exclusive=date(2026, 9, 2),
                effective_zone_id="Europe/Rome",
            )
        ).replayed

        revised = await recurrences.replace(
            owner="routine",
            self_person_ref=alice,
            owner_ref=routine.routine_ref,
            operation_id="recurrence:future",
            expected_material_state_ref=initial.material_state_ref,
            recurrence=_daily(starts_on=date(2026, 10, 3), wall_time=time(9)),
        )
        reconciled = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:revised",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 5),
            effective_zone_id="Europe/Rome",
        )
        assert [
            item.coordinate.generated_wall_time
            for item in reconciled.occurrences
            if isinstance(item.coordinate, CalendarCoordinate)
        ] == [time(8), time(8), time(9), time(9)]

        old_third = first.occurrences[2]
        skipped = await occurrences.skip(
            self_person_ref=alice,
            occurrence_ref=old_third.occurrence_ref,
            operation_id="skip:old-third",
            reason="Series changed after this materialized expectation",
        )
        assert skipped.occurrence.skipped
        assert (
            await occurrences.get(self_person_ref=alice, occurrence_ref=old_third.occurrence_ref)
        ).skipped

        exclusion_coordinate = CalendarCoordinate(
            family_code="calendar_wall_clock",
            generated_date=date(2026, 10, 5),
            generated_wall_time=time(9),
            clock_basis_code="floating_local",
            zone_id=None,
            resolved_at=None,
        )
        exclusion = await occurrences.exclude(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=revised.recurrence.material_state_ref,
            operation_id="exclude:oct-5",
            coordinate=exclusion_coordinate,
        )
        assert not exclusion.replayed
        excluded_checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:excluded",
            start_date=date(2026, 10, 5),
            end_date_exclusive=date(2026, 10, 6),
            effective_zone_id="Europe/Rome",
        )
        assert excluded_checkpoint.occurrences == ()
        with pytest.raises(OccurrenceMaterializedConflictError):
            await occurrences.exclude(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                governing_recurrence_state_ref=revised.recurrence.material_state_ref,
                operation_id="exclude:materialized",
                coordinate=CalendarCoordinate(
                    family_code="calendar_wall_clock",
                    generated_date=date(2026, 10, 4),
                    generated_wall_time=time(9),
                    clock_basis_code="floating_local",
                    zone_id=None,
                    resolved_at=None,
                ),
            )

        extra = await occurrences.create_extra(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="extra:one",
        )
        assert extra.occurrence.origin_code == "explicit_extra"
        assert extra.occurrence.governing_recurrence_state_ref is None
        assert extra.occurrence.coordinate is None

        paused = await routines.mutate(
            self_person_ref=alice,
            operation_id="routine:pause",
            routine_ref=routine.routine_ref,
            expected_source_revision=routine.source_revision,
            kind="pause",
        )
        assert paused.lifecycle_state == "paused"
        assert (
            await occurrences.checkpoint(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="checkpoint:first",
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 4),
                effective_zone_id="Europe/Rome",
            )
        ).replayed
        with pytest.raises(OccurrenceSourceInactiveError):
            await occurrences.checkpoint(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="checkpoint:paused",
                start_date=date(2026, 10, 6),
                end_date_exclusive=date(2026, 10, 7),
                effective_zone_id="Europe/Rome",
            )
        with pytest.raises(OccurrenceSourceInactiveError):
            await occurrences.create_extra(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="extra:paused",
            )
        resumed = await routines.mutate(
            self_person_ref=alice,
            operation_id="routine:resume",
            routine_ref=routine.routine_ref,
            expected_source_revision=paused.source_revision,
            kind="resume",
        )
        assert resumed.lifecycle_state == "active"

        event = (
            await events.create_event(
                self_person_ref=alice,
                operation_id="event",
                title="Standup",
                life_area_ref=area.life_area_ref,
            )
        ).event
        await recurrences.replace(
            owner="event",
            self_person_ref=alice,
            owner_ref=event.event_ref,
            operation_id="event:recurrence",
            expected_material_state_ref=None,
            recurrence=_daily(starts_on=date(2026, 10, 1), wall_time=time(10)),
        )
        event_checkpoint = await occurrences.checkpoint(
            owner="event",
            self_person_ref=alice,
            source_ref=event.event_ref,
            operation_id="event:checkpoint",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        assert len(event_checkpoint.occurrences) == 1
        with pytest.raises(OccurrenceSourceNotFoundError):
            await occurrences.get(
                self_person_ref=bob,
                occurrence_ref=event_checkpoint.occurrences[0].occurrence_ref,
            )

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.occurrence_generation "
                "WHERE source_native_ref=%s AND governing_recurrence_state_ref=%s",
                (routine.routine_ref, initial.material_state_ref),
            ).fetchone() == (3,)
    finally:
        await runtime.dispose()


def test_occurrence_runtime_surface_is_execute_only(migrated_database: Any) -> None:
    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
    ) as connection:
        assert connection.execute(
            "SELECT "
            "has_table_privilege('dante_runtime','dante.occurrence_checkpoint_operation','INSERT'),"
            "has_table_privilege('dante_runtime','dante.occurrence_skip','SELECT'),"
            "has_table_privilege('dante_runtime','dante.occurrence_generation','SELECT'),"
            "has_table_privilege('dante_runtime','dante.occurrence_generation','INSERT'),"
            "has_table_privilege('dante_runtime','dante.occurrence_generation_calendar','INSERT'),"
            "has_function_privilege('dante_runtime','dante.begin_self_routine_occurrence_checkpoint(uuid,text,text,uuid,date,date,text)','EXECUTE'),"
            "has_function_privilege('dante_runtime','dante.materialize_self_event_occurrence_candidate(uuid,text,uuid,uuid,text,date,time,text,text,timestamptz,timestamptz,date,date,text,text,integer)','EXECUTE'),"
            "has_function_privilege('dante_runtime','dante.skip_self_occurrence(uuid,text,text,uuid,text)','EXECUTE')"
        ).fetchone() == (False, False, False, False, False, True, True, True)
