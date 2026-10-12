"""Real PostgreSQL proof for governed B02-C Schedule placement revision."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any, cast
from uuid import uuid7

import psycopg
import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineFloatingLocalActivityItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    ScheduleRevisionConflictError,
    TemporalScheduleApplication,
)
from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
)
from dante.platform.database.runtime import create_database_runtime
from dante.platform.time import TimeZoneMode, TimeZonePolicy


def _floating_local(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
) -> datetime:
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


def _context(self_person_ref: NativeRef) -> DanteContext:
    now = datetime.now(UTC)
    return DanteContext(
        principal=Principal(
            account_ref=uuid7(),
            auth_session_ref=uuid7(),
            authenticated_at=now,
            recent_auth_at=now,
        ),
        self_person_ref=self_person_ref,
        timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
        effective_zone_id="Europe/Rome",
    )


def _revision_facts(
    database: Any,
    *,
    activity_ref: NativeRef,
    schedule_ref: ScopedRecordRef,
    old_state_ref: MaterialStateRef,
    new_state_ref: MaterialStateRef,
) -> tuple[int, int, int, int, int, int, int]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        row = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.activity_intention
                WHERE activity_ref=%s),
              (SELECT count(*) FROM dante.schedule
                WHERE schedule_ref=%s AND subject_native_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s AND material_state_ref=%s
                  AND current_until_at IS NOT NULL),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s AND material_state_ref=%s
                  AND current_until_at IS NULL),
              (SELECT count(*) FROM dante.scoped_current_material_state
                WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
                  AND material_state_ref=%s),
              (SELECT count(*) FROM dante.schedule_revision_operation
                WHERE schedule_ref=%s AND material_state_ref=%s)
            """,
            (
                activity_ref,
                schedule_ref,
                activity_ref,
                schedule_ref,
                schedule_ref,
                old_state_ref,
                schedule_ref,
                new_state_ref,
                schedule_ref,
                new_state_ref,
                schedule_ref,
                new_state_ref,
            ),
        ).fetchone()
        assert row is not None
        return cast(tuple[int, int, int, int, int, int, int], row)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_revision_retains_history_moves_current_and_replays_exact_intent(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    initial = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 10, 0),
        ends_local_at=_floating_local(2026, 9, 9, 11, 0),
    )
    revised = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 13, 15),
        ends_local_at=_floating_local(2026, 9, 9, 14, 45),
    )

    try:
        created = await activities.create_activity_with_floating_schedule(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-c:create",
            title="Activity con revisione",
            placement=initial,
        )
        result = await schedules.revise_floating_schedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-c:revise",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=created.schedule.material_state_ref,
            placement=revised,
        )
        assert result.replayed is False
        assert result.schedule_ref == created.schedule.schedule_ref
        assert result.previous_material_state_ref == created.schedule.material_state_ref
        assert result.material_state_ref.version == 7
        assert result.material_state_ref != created.schedule.material_state_ref

        replay = await schedules.revise_floating_schedule(
            self_person_ref=self_person_ref,
            operation_id=" operation:b02-c:revise ",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=created.schedule.material_state_ref,
            placement=revised,
        )
        assert replay.replayed is True
        assert replay.schedule_ref == result.schedule_ref
        assert replay.previous_material_state_ref == result.previous_material_state_ref
        assert replay.material_state_ref == result.material_state_ref
        assert replay.placement == result.placement

        with pytest.raises(ScheduleOperationIdReuseError):
            await schedules.revise_floating_schedule(
                self_person_ref=self_person_ref,
                operation_id="operation:b02-c:revise",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=_floating_local(2026, 9, 9, 15, 0),
                    ends_local_at=_floating_local(2026, 9, 9, 16, 0),
                ),
            )

        with pytest.raises(ScheduleRevisionConflictError):
            await schedules.revise_floating_schedule(
                self_person_ref=self_person_ref,
                operation_id="operation:b02-c:stale",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=_floating_local(2026, 9, 9, 16, 0),
                    ends_local_at=_floating_local(2026, 9, 9, 17, 0),
                ),
            )

        window = await timeline.read_window(
            query=TimelineWindowQuery(
                start_date=date(2026, 9, 9),
                end_date_exclusive=date(2026, 9, 10),
            ),
            context=_context(self_person_ref),
        )
        assert len(window.items) == 1
        item = window.items[0]
        assert isinstance(item, TimelineFloatingLocalActivityItem)
        assert item.activity_ref == created.activity.activity_ref
        assert item.schedule_ref == created.schedule.schedule_ref
        assert item.placement_material_state_ref == result.material_state_ref
        assert item.starts_local_at == revised.starts_local_at
        assert item.ends_local_at == revised.ends_local_at
    finally:
        await runtime.dispose()

    assert _revision_facts(
        migrated_database,
        activity_ref=created.activity.activity_ref,
        schedule_ref=created.schedule.schedule_ref,
        old_state_ref=created.schedule.material_state_ref,
        new_state_ref=result.material_state_ref,
    ) == (1, 1, 2, 1, 1, 1, 1)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_missing_and_cross_self_schedule_revision_are_indistinguishable(
    migrated_database: Any,
) -> None:
    owner_ref = _seed_self_person(migrated_database)
    other_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 9, 0),
        ends_local_at=_floating_local(2026, 9, 9, 10, 0),
    )

    try:
        created = await activities.create_activity_with_floating_schedule(
            self_person_ref=owner_ref,
            life_area_ref=ensure_test_life_area(migrated_database, owner_ref),
            operation_id="operation:b02-c:private-create",
            title="Schedule privata",
            placement=placement,
        )
        for self_ref, schedule_ref in (
            (other_ref, created.schedule.schedule_ref),
            (owner_ref, ScopedRecordRef(uuid7())),
        ):
            with pytest.raises(ScheduleNotFoundError):
                await schedules.revise_floating_schedule(
                    self_person_ref=self_ref,
                    operation_id=f"operation:b02-c:denied:{schedule_ref}",
                    schedule_ref=schedule_ref,
                    expected_material_state_ref=created.schedule.material_state_ref,
                    placement=FloatingLocalIntervalPlacement(
                        starts_local_at=_floating_local(2026, 9, 9, 11, 0),
                        ends_local_at=_floating_local(2026, 9, 9, 12, 0),
                    ),
                )
    finally:
        await runtime.dispose()

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        facts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.schedule_revision_operation
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s)
            """,
            (created.schedule.schedule_ref, created.schedule.schedule_ref),
        ).fetchone()
    assert facts == (0, 1)
