"""B06-C PostgreSQL proof for canonical Occurrence checkpoint and scopes."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

import psycopg
import pytest
from sqlalchemy import text
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import (
    CalendarCoordinate,
    CyclicCoordinate,
    ElapsedCoordinate,
    OccurrenceApplication,
    OccurrenceCheckpoint,
    OccurrenceMaterializedConflictError,
    OccurrenceOperationReuseError,
    OccurrenceSourceInactiveError,
    OccurrenceSourceNotFoundError,
    QuotaCoordinate,
)
from dante.modules.temporal.open_recurrence_allowance import OpenRecurrenceAllowanceApplication
from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    CyclicRecurrence,
    ElapsedRecurrence,
    QuotaRecurrence,
    RecurrenceApplication,
)
from dante.modules.temporal.routine import RoutineApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_open_series_requires_explicit_renewal_after_730_expected_dates(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    routines = RoutineApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    areas = LifeAreaApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    renewals = OpenRecurrenceAllowanceApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    today = date(2026, 11, 22)
    first = today - timedelta(days=699)
    try:
        area = (
            await areas.create(self_person_ref=alice, operation_id="renewal:area", name="Studio")
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="renewal:routine",
            title="Studio quotidiano",
            life_area_ref=area.life_area_ref,
            starts_on=first,
            wall_time=time(8),
        )
        notices = await renewals.list_notices(
            actor=alice, today=today, effective_zone_id="Europe/Rome"
        )
        notice = next(item for item in notices if item.source_ref == routine.routine_ref)
        assert (notice.allowed_count, notice.remaining_count) == (730, 30)
        assert not await renewals.list_notices(
            actor=bob, today=today, effective_zone_id="Europe/Rome"
        )

        last_day = first + timedelta(days=729)
        bounded = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="renewal:bounded",
            start_date=last_day,
            end_date_exclusive=last_day + timedelta(days=2),
            effective_zone_id="Europe/Rome",
        )
        assert len(bounded.occurrences) == 1
        for _ in range(2):
            await renewals.decide(
                actor=alice,
                owner="routine",
                source_ref=routine.routine_ref,
                title=notice.title,
                today=today,
                effective_zone_id="Europe/Rome",
                expected_state_ref=notice.material_state_ref,
                expected_revision=notice.revision,
                operation_id="renewal:extend",
                decision="extend",
            )
        assert all(
            item.source_ref != routine.routine_ref
            for item in await renewals.list_notices(
                actor=alice, today=today, effective_zone_id="Europe/Rome"
            )
        )
        renewed = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="renewal:extended",
            start_date=last_day + timedelta(days=1),
            end_date_exclusive=last_day + timedelta(days=2),
            effective_zone_id="Europe/Rome",
        )
        assert len(renewed.occurrences) == 1

        declining = await routines.create(
            self_person_ref=alice,
            operation_id="renewal:declining",
            title="Serie che termina",
            life_area_ref=area.life_area_ref,
            starts_on=first,
            wall_time=time(9),
        )
        decline_notice = next(
            item
            for item in await renewals.list_notices(
                actor=alice, today=today, effective_zone_id="Europe/Rome"
            )
            if item.source_ref == declining.routine_ref
        )
        await renewals.decide(
            actor=alice,
            owner="routine",
            source_ref=declining.routine_ref,
            title=decline_notice.title,
            today=today,
            effective_zone_id="Europe/Rome",
            expected_state_ref=decline_notice.material_state_ref,
            expected_revision=decline_notice.revision,
            operation_id="renewal:decline",
            decision="decline",
        )
        assert all(
            item.source_ref != declining.routine_ref
            for item in await renewals.list_notices(
                actor=alice, today=today, effective_zone_id="Europe/Rome"
            )
        )
        stopped = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=declining.routine_ref,
            operation_id="renewal:stopped",
            start_date=last_day,
            end_date_exclusive=last_day + timedelta(days=2),
            effective_zone_id="Europe/Rome",
        )
        assert len(stopped.occurrences) == 1
        finite = await recurrences.replace(
            owner="routine",
            self_person_ref=alice,
            owner_ref=declining.routine_ref,
            operation_id="renewal:finite",
            expected_material_state_ref=decline_notice.material_state_ref,
            recurrence=replace(
                _daily(starts_on=today + timedelta(days=1), wall_time=time(9)),
                range_kind="expected_count",
                expected_occurrence_count=900,
            ),
        )
        assert all(
            item.source_ref != declining.routine_ref
            for item in await renewals.list_notices(
                actor=alice, today=today, effective_zone_id="Europe/Rome"
            )
        )
        await recurrences.replace(
            owner="routine",
            self_person_ref=alice,
            owner_ref=declining.routine_ref,
            operation_id="renewal:open-again",
            expected_material_state_ref=finite.recurrence.material_state_ref,
            recurrence=_daily(starts_on=today + timedelta(days=2), wall_time=time(9)),
        )
        async with runtime.session_factory() as session, session.begin():
            allowance = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_open_recurrence_allowance(:actor,:owner,:source)"
                        ),
                        {"actor": alice, "owner": "routine", "source": declining.routine_ref},
                    )
                )
                .mappings()
                .one()
            )
        assert (allowance["allowed_count"], allowance["declined"], allowance["revision"]) == (
            730,
            False,
            0,
        )

        event = (
            await events.create_event(
                self_person_ref=alice,
                operation_id="renewal:event",
                title="Evento quotidiano",
                life_area_ref=area.life_area_ref,
            )
        ).event
        await recurrences.replace(
            owner="event",
            self_person_ref=alice,
            owner_ref=event.event_ref,
            operation_id="renewal:event:recurrence",
            expected_material_state_ref=None,
            recurrence=_daily(starts_on=first, wall_time=time(10)),
        )
        event_notice = next(
            item
            for item in await renewals.list_notices(
                actor=alice, today=today, effective_zone_id="Europe/Rome"
            )
            if item.source_ref == event.event_ref
        )
        assert (event_notice.owner, event_notice.remaining_count) == ("event", 30)
        event_boundary = await occurrences.checkpoint(
            owner="event",
            self_person_ref=alice,
            source_ref=event.event_ref,
            operation_id="renewal:event:boundary",
            start_date=last_day,
            end_date_exclusive=last_day + timedelta(days=2),
            effective_zone_id="Europe/Rome",
        )
        assert len(event_boundary.occurrences) == 1
    finally:
        await runtime.dispose()


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
        skipped_replay = await occurrences.skip(
            self_person_ref=alice,
            occurrence_ref=old_third.occurrence_ref,
            operation_id="skip:old-third",
            reason="Series changed after this materialized expectation",
        )
        assert skipped_replay.replayed
        assert skipped_replay.occurrence.occurrence_ref == skipped.occurrence.occurrence_ref
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
        exclusion_replay = await occurrences.exclude(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=revised.recurrence.material_state_ref,
            operation_id="exclude:oct-5",
            coordinate=exclusion_coordinate,
        )
        assert exclusion_replay.replayed
        assert exclusion_replay.exclusion_ref == exclusion.exclusion_ref
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
        extra_replay = await occurrences.create_extra(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="extra:one",
        )
        assert extra_replay.replayed
        assert extra_replay.occurrence.occurrence_ref == extra.occurrence.occurrence_ref

        paused = await routines.mutate(
            self_person_ref=alice,
            operation_id="routine:pause",
            routine_ref=routine.routine_ref,
            expected_source_revision=routine.source_revision,
            kind="pause",
        )
        assert paused.lifecycle_state == "paused"
        assert (
            await occurrences.create_extra(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id="extra:one",
            )
        ).replayed
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

        elapsed = await recurrences.replace(
            owner="routine",
            self_person_ref=alice,
            owner_ref=routine.routine_ref,
            operation_id="recurrence:elapsed",
            expected_material_state_ref=revised.recurrence.material_state_ref,
            recurrence=ElapsedRecurrence(
                family_code="elapsed_interval",
                range_kind="until_boundary",
                expected_occurrence_count=None,
                effective_from=datetime(2026, 11, 1, tzinfo=UTC),
                effective_until=datetime(2026, 11, 2, tzinfo=UTC),
                elapsed_seconds=Decimal("21600"),
                anchor_mode_code="fixed_anchor",
                anchor_at=datetime(2026, 11, 1, tzinfo=UTC),
            ),
        )
        elapsed_checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:elapsed",
            start_date=date(2026, 11, 1),
            end_date_exclusive=date(2026, 11, 2),
            effective_zone_id="UTC",
        )
        assert [
            item.coordinate.expected_at
            for item in elapsed_checkpoint.occurrences
            if isinstance(item.coordinate, ElapsedCoordinate)
        ] == [
            datetime(2026, 11, 1, 6, tzinfo=UTC),
            datetime(2026, 11, 1, 12, tzinfo=UTC),
            datetime(2026, 11, 1, 18, tzinfo=UTC),
        ]

        quota = await recurrences.replace(
            owner="routine",
            self_person_ref=alice,
            owner_ref=routine.routine_ref,
            operation_id="recurrence:quota",
            expected_material_state_ref=elapsed.recurrence.material_state_ref,
            recurrence=QuotaRecurrence(
                family_code="quota_per_period",
                range_kind="open",
                expected_occurrence_count=None,
                effective_from=date(2026, 11, 2),
                effective_until=None,
                quota_count=2,
                period_unit_code="day",
                period_span=1,
                frame_code="floating_local",
                zone_id=None,
                week_start=None,
                pattern_anchor_date=None,
            ),
        )
        quota_checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:quota",
            start_date=date(2026, 11, 2),
            end_date_exclusive=date(2026, 11, 3),
            effective_zone_id="UTC",
        )
        assert (
            len(
                [
                    item
                    for item in quota_checkpoint.occurrences
                    if isinstance(item.coordinate, QuotaCoordinate)
                ]
            )
            == 2
        )

        cyclic = await recurrences.replace(
            owner="routine",
            self_person_ref=alice,
            owner_ref=routine.routine_ref,
            operation_id="recurrence:cyclic",
            expected_material_state_ref=quota.recurrence.material_state_ref,
            recurrence=CyclicRecurrence(
                family_code="cyclic_positional",
                range_kind="open",
                expected_occurrence_count=None,
                effective_from=date(2026, 11, 3),
                effective_until=None,
                cycle_length=2,
                position_unit_code="day",
                pattern_anchor_date=date(2026, 11, 3),
                generates_expected=(True, False),
            ),
        )
        cyclic_checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="checkpoint:cyclic",
            start_date=date(2026, 11, 3),
            end_date_exclusive=date(2026, 11, 7),
            effective_zone_id="UTC",
        )
        assert [
            item.coordinate.generated_date
            for item in cyclic_checkpoint.occurrences
            if isinstance(item.coordinate, CyclicCoordinate)
        ] == [date(2026, 11, 3), date(2026, 11, 5)]
        assert cyclic.recurrence.material_state_ref != quota.recurrence.material_state_ref

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
        event_reuse = await occurrences.checkpoint(
            owner="event",
            self_person_ref=alice,
            source_ref=event.event_ref,
            operation_id="event:checkpoint:reuse",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        assert not event_reuse.replayed
        assert (
            event_reuse.occurrences[0].occurrence_ref
            == event_checkpoint.occurrences[0].occurrence_ref
        )
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


@pytest.mark.asyncio
async def test_concurrent_checkpoints_reuse_the_same_canonical_occurrences(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="concurrent:area",
                name="Salute",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="concurrent:routine",
            title="Idratazione",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 12, 1),
            wall_time=time(9),
        )

        async def checkpoint(operation_id: str) -> OccurrenceCheckpoint:
            return await occurrences.checkpoint(
                owner="routine",
                self_person_ref=alice,
                source_ref=routine.routine_ref,
                operation_id=operation_id,
                start_date=date(2026, 12, 1),
                end_date_exclusive=date(2026, 12, 4),
                effective_zone_id="Europe/Rome",
            )

        first, second = await asyncio.gather(
            checkpoint("concurrent:checkpoint:a"),
            checkpoint("concurrent:checkpoint:b"),
        )

        first_refs = {item.occurrence_ref for item in first.occurrences}
        second_refs = {item.occurrence_ref for item in second.occurrences}
        assert len(first_refs) == 3
        assert first_refs == second_refs

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.occurrence_generation WHERE source_native_ref=%s",
                (routine.routine_ref,),
            ).fetchone() == (3,)
    finally:
        await runtime.dispose()
