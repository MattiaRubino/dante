"""B02-E1 proof for typed Schedule forms, precision, DST, and generic mutation."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    CoarseLocalPeriodPlacement,
    DateSpanPlacement,
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    ScheduleInputError,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    SchedulePlacement,
    ScheduleRevisionConflictError,
    TemporalScheduleApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.time import AmbiguousLocalTimeError, NonexistentLocalTimeError


def _local(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour, minute)  # noqa: DTZ001


def _seed_self_person(database: Any) -> NativeRef:
    person_ref = uuid7()
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute(
            "INSERT INTO dante.person(person_ref) VALUES (%s)",
            (person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (person_ref,),
        )
        connection.commit()
    return NativeRef(person_ref)


def _placements() -> tuple[SchedulePlacement, ...]:
    return (
        DateSpanPlacement(
            start_date=date(2026, 9, 16),
            end_date_exclusive=date(2026, 9, 19),
        ),
        FloatingLocalIntervalPlacement(
            starts_local_at=_local(2026, 9, 16, 23, 30),
            ends_local_at=_local(2026, 9, 17, 1, 0),
        ),
        NamedZoneLocalIntervalPlacement(
            starts_local_at=_local(2026, 10, 25, 2, 10),
            ends_local_at=_local(2026, 10, 25, 2, 40),
            zone_id="Europe/Rome",
            disambiguation="later",
        ),
        AbsoluteIntervalPlacement(
            starts_at=datetime(2026, 9, 16, 8, 0, tzinfo=UTC),
            ends_at=datetime(2026, 9, 16, 9, 20, tzinfo=UTC),
        ),
        CoarseLocalPeriodPlacement(
            local_date=date(2026, 9, 16),
            period="afternoon",
        ),
    )


def test_coarse_period_is_bounded_without_fabricated_clock_values() -> None:
    placement = CoarseLocalPeriodPlacement(
        local_date=date(2026, 9, 16),
        period="morning",
    )

    assert placement.local_date == date(2026, 9, 16)
    assert not hasattr(placement, "starts_local_at")
    assert not hasattr(placement, "ends_local_at")
    with pytest.raises(ScheduleInputError):
        CoarseLocalPeriodPlacement(
            local_date=date(2026, 9, 16),
            period="night",  # type: ignore[arg-type]
        )


def test_named_zone_dst_requires_explicit_disambiguation_and_retains_resolution() -> None:
    with pytest.raises(ScheduleInputError) as gap_error:
        NamedZoneLocalIntervalPlacement(
            starts_local_at=_local(2026, 3, 29, 2, 10),
            ends_local_at=_local(2026, 3, 29, 3, 10),
            zone_id="Europe/Rome",
        )
    assert isinstance(gap_error.value.__cause__, NonexistentLocalTimeError)

    with pytest.raises(ScheduleInputError) as overlap_error:
        NamedZoneLocalIntervalPlacement(
            starts_local_at=_local(2026, 10, 25, 2, 10),
            ends_local_at=_local(2026, 10, 25, 2, 40),
            zone_id="Europe/Rome",
        )
    assert isinstance(overlap_error.value.__cause__, AmbiguousLocalTimeError)

    explicit_gap = NamedZoneLocalIntervalPlacement(
        starts_local_at=_local(2026, 3, 29, 1, 50),
        ends_local_at=_local(2026, 3, 29, 2, 10),
        zone_id="Europe/Rome",
        disambiguation="later",
    )
    assert explicit_gap.resolved_start_at == datetime(2026, 3, 29, 0, 50, tzinfo=UTC)
    assert explicit_gap.resolved_end_at == datetime(2026, 3, 29, 1, 10, tzinfo=UTC)

    earlier = NamedZoneLocalIntervalPlacement(
        starts_local_at=_local(2026, 10, 25, 2, 10),
        ends_local_at=_local(2026, 10, 25, 2, 40),
        zone_id="Europe/Rome",
        disambiguation="earlier",
    )
    later = NamedZoneLocalIntervalPlacement(
        starts_local_at=_local(2026, 10, 25, 2, 10),
        ends_local_at=_local(2026, 10, 25, 2, 40),
        zone_id="Europe/Rome",
        disambiguation="later",
    )

    assert earlier.resolved_start_at == datetime(2026, 10, 25, 0, 10, tzinfo=UTC)
    assert earlier.resolved_end_at == datetime(2026, 10, 25, 0, 40, tzinfo=UTC)
    assert later.resolved_start_at == datetime(2026, 10, 25, 1, 10, tzinfo=UTC)
    assert later.resolved_end_at == datetime(2026, 10, 25, 1, 40, tzinfo=UTC)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_all_forms_establish_revise_unschedule_and_undo_losslessly(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    other_self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    placements = _placements()
    schedule_refs: list[UUID] = []

    try:
        for index, placement in enumerate(placements):
            operation_prefix = f"operation:b02-e1:form-{index}"
            created = await activities.create_activity_with_schedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:create",
                title=f"E1 form {index}",
                placement=placement,
            )
            replayed_create = await activities.create_activity_with_schedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:create",
                title=f"E1 form {index}",
                placement=placement,
            )
            assert created.replayed is False
            assert replayed_create.replayed is True
            assert replayed_create.schedule.schedule_ref == created.schedule.schedule_ref
            assert replayed_create.schedule.material_state_ref == (
                created.schedule.material_state_ref
            )

            replacement = placements[(index + 1) % len(placements)]
            revised = await schedules.revise_schedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:revise",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
                placement=replacement,
            )
            replayed_revision = await schedules.revise_schedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:revise",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
                placement=replacement,
            )
            assert revised.placement == replacement
            assert replayed_revision.replayed is True
            assert replayed_revision.material_state_ref == revised.material_state_ref

            with pytest.raises(ScheduleOperationIdReuseError):
                await schedules.revise_schedule(
                    self_person_ref=self_person_ref,
                    operation_id=f"{operation_prefix}:revise",
                    schedule_ref=created.schedule.schedule_ref,
                    expected_material_state_ref=created.schedule.material_state_ref,
                    placement=placements[(index + 2) % len(placements)],
                )
            with pytest.raises(ScheduleRevisionConflictError):
                await schedules.revise_schedule(
                    self_person_ref=self_person_ref,
                    operation_id=f"{operation_prefix}:stale-revise",
                    schedule_ref=created.schedule.schedule_ref,
                    expected_material_state_ref=created.schedule.material_state_ref,
                    placement=replacement,
                )
            if index == 0:
                with pytest.raises(ScheduleNotFoundError):
                    await schedules.revise_schedule(
                        self_person_ref=other_self_person_ref,
                        operation_id=f"{operation_prefix}:cross-self",
                        schedule_ref=created.schedule.schedule_ref,
                        expected_material_state_ref=revised.material_state_ref,
                        placement=replacement,
                    )

            unscheduled = await schedules.unschedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:unschedule",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=revised.material_state_ref,
            )
            restored = await schedules.undo_unschedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:undo",
                schedule_ref=created.schedule.schedule_ref,
                unschedule_operation_id=unscheduled.unschedule_operation_id,
            )
            replayed_restore = await schedules.undo_unschedule(
                self_person_ref=self_person_ref,
                operation_id=f"{operation_prefix}:undo",
                schedule_ref=created.schedule.schedule_ref,
                unschedule_operation_id=unscheduled.unschedule_operation_id,
            )
            assert restored.placement == replacement
            assert restored.material_state_ref != revised.material_state_ref
            assert restored.restored_from_material_state_ref == revised.material_state_ref
            assert replayed_restore.replayed is True
            assert replayed_restore.material_state_ref == restored.material_state_ref
            assert replayed_restore.placement == replacement
            schedule_refs.append(UUID(str(created.schedule.schedule_ref)))
    finally:
        await runtime.dispose()

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        rows = connection.execute(
            """
            SELECT placement.schedule_ref,
                   placement.temporal_form_code,
                   (date_payload.material_state_ref IS NOT NULL)::int
                     + (floating_payload.material_state_ref IS NOT NULL)::int
                     + (named_payload.material_state_ref IS NOT NULL)::int
                     + (absolute_payload.material_state_ref IS NOT NULL)::int
                     + (coarse_payload.material_state_ref IS NOT NULL)::int AS payload_count,
                   (current.material_state_ref IS NOT NULL) AS is_current
              FROM dante.schedule_placement_state AS placement
              LEFT JOIN dante.schedule_placement_date_state AS date_payload
                USING (material_state_ref)
              LEFT JOIN dante.schedule_placement_floating_local_state AS floating_payload
                USING (material_state_ref)
              LEFT JOIN dante.schedule_placement_named_zone_state AS named_payload
                USING (material_state_ref)
              LEFT JOIN dante.schedule_placement_absolute_state AS absolute_payload
                USING (material_state_ref)
              LEFT JOIN dante.schedule_placement_coarse_local_period_state AS coarse_payload
                USING (material_state_ref)
              LEFT JOIN dante.scoped_current_material_state AS current
                ON current.scoped_owner_ref = placement.schedule_ref
               AND current.facet_code = 'schedule.placement'
               AND current.material_state_ref = placement.material_state_ref
             WHERE placement.schedule_ref = ANY(%s)
             ORDER BY placement.schedule_ref, placement.material_state_ref
            """,
            (schedule_refs,),
        ).fetchall()
        history = connection.execute(
            """
            SELECT schedule_ref,
                   count(*) AS episode_count,
                   count(*) FILTER (WHERE current_until_at IS NULL) AS current_count,
                   bool_and(current_until_at IS NULL OR current_until_at > current_from_at)
              FROM dante.schedule_placement_current_history
             WHERE schedule_ref = ANY(%s)
             GROUP BY schedule_ref
            """,
            (schedule_refs,),
        ).fetchall()

    assert len(rows) == 15
    assert all(row[2] == 1 for row in rows)
    assert sum(row[3] for row in rows) == 5
    assert {row[1] for row in rows} == {
        "date_span",
        "floating_local",
        "named_zone_local",
        "absolute",
        "coarse_local_period",
    }
    assert len(history) == 5
    assert all(row[1:] == (3, 1, True) for row in history)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_one_activity_can_own_multiple_independent_schedules(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)

    try:
        created = await activities.create_activity(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-e1:multi:create",
            title="Una Activity con più Schedule",
        )
        first = await activities.schedule_existing_activity_with_placement(
            self_person_ref=self_person_ref,
            activity_ref=created.activity.activity_ref,
            operation_id="operation:b02-e1:multi:first",
            placement=DateSpanPlacement(
                start_date=date(2026, 9, 20),
                end_date_exclusive=date(2026, 9, 21),
            ),
        )
        second = await activities.schedule_existing_activity_with_placement(
            self_person_ref=self_person_ref,
            activity_ref=created.activity.activity_ref,
            operation_id="operation:b02-e1:multi:second",
            placement=CoarseLocalPeriodPlacement(
                local_date=date(2026, 9, 22),
                period="evening",
            ),
        )
        assert first.schedule.schedule_ref != second.schedule.schedule_ref
        assert await activities.list_unplaced(self_person_ref=self_person_ref) == ()
    finally:
        await runtime.dispose()

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        count_row = connection.execute(
            """
            SELECT count(*)
              FROM dante.schedule AS schedule
              JOIN dante.scoped_current_material_state AS current
                ON current.scoped_owner_ref = schedule.schedule_ref
               AND current.facet_code = 'schedule.placement'
             WHERE schedule.subject_native_ref = %s
            """,
            (created.activity.activity_ref,),
        ).fetchone()

    assert count_row is not None
    assert count_row[0] == 2
