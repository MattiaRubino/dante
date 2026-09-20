"""Real PostgreSQL proof for B02-D unschedule and guarded Undo."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from b05_legacy_test_support import ensure_test_life_area

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.application import TemporalTimelineApplication
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    ScheduleNotFoundError,
    ScheduleOperationIdReuseError,
    ScheduleUndoConflictError,
    ScheduleUnscheduleConflictError,
    TemporalScheduleApplication,
    UnscheduledScheduleView,
)
from dante.platform.database.references import NativeRef
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


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_unschedule_returns_activity_to_tray_and_undo_is_monotonic(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    timeline = TemporalTimelineApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 13, 15),
        ends_local_at=_floating_local(2026, 9, 9, 14, 45),
    )

    try:
        created = await activities.create_activity_with_floating_schedule(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-d:create",
            title="Activity da rimuovere e ripristinare",
            placement=placement,
        )
        unscheduled = await schedules.unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:unschedule",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=created.schedule.material_state_ref,
        )
        replayed_unschedule = await schedules.unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:unschedule",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=created.schedule.material_state_ref,
        )

        assert unscheduled.replayed is False
        assert replayed_unschedule == UnscheduledScheduleView(
            schedule_ref=unscheduled.schedule_ref,
            previous_material_state_ref=unscheduled.previous_material_state_ref,
            unschedule_operation_id=unscheduled.unschedule_operation_id,
            created_at=unscheduled.created_at,
            replayed=True,
        )
        unplaced = await activities.list_unplaced(self_person_ref=self_person_ref)
        assert [item.activity_ref for item in unplaced] == [created.activity.activity_ref]
        absent_window = await timeline.read_window(
            context=_context(self_person_ref),
            query=TimelineWindowQuery(
                start_date=date(2026, 9, 9),
                end_date_exclusive=date(2026, 9, 10),
            ),
        )
        assert absent_window.items == ()

        restored = await schedules.undo_unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:undo",
            schedule_ref=created.schedule.schedule_ref,
            unschedule_operation_id=unscheduled.unschedule_operation_id,
        )
        replayed_restore = await schedules.undo_unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:undo",
            schedule_ref=created.schedule.schedule_ref,
            unschedule_operation_id=unscheduled.unschedule_operation_id,
        )
        assert restored.material_state_ref != created.schedule.material_state_ref
        assert restored.restored_from_material_state_ref == (created.schedule.material_state_ref)
        assert restored.placement == placement
        assert replayed_restore.material_state_ref == restored.material_state_ref
        assert replayed_restore.replayed is True
        assert await activities.list_unplaced(self_person_ref=self_person_ref) == ()

        restored_window = await timeline.read_window(
            context=_context(self_person_ref),
            query=TimelineWindowQuery(
                start_date=date(2026, 9, 9),
                end_date_exclusive=date(2026, 9, 10),
            ),
        )
        assert len(restored_window.items) == 1
        assert restored_window.items[0].placement_material_state_ref == restored.material_state_ref
    finally:
        await runtime.dispose()

    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        ),
        autocommit=True,
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        facts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.activity_intention
                WHERE activity_ref=%s),
              (SELECT count(*) FROM dante.schedule
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_state
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s AND current_until_at IS NULL),
              (SELECT count(*) FROM dante.scoped_current_material_state
                WHERE scoped_owner_ref=%s
                  AND facet_code='schedule.placement'),
              (SELECT count(*) FROM dante.schedule_unschedule_operation
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_unschedule_undo_operation
                WHERE schedule_ref=%s)
            """,
            (
                created.activity.activity_ref,
                created.schedule.schedule_ref,
                created.schedule.schedule_ref,
                created.schedule.schedule_ref,
                created.schedule.schedule_ref,
                created.schedule.schedule_ref,
                created.schedule.schedule_ref,
                created.schedule.schedule_ref,
            ),
        ).fetchone()
    assert facts == (1, 1, 2, 2, 1, 1, 1, 1)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_unschedule_and_undo_reject_stale_or_reused_intent(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    other_self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 9, 0),
        ends_local_at=_floating_local(2026, 9, 9, 10, 0),
    )

    try:
        created = await activities.create_activity_with_floating_schedule(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-d:conflict:create",
            title="Activity concorrente",
            placement=placement,
        )
        with pytest.raises(ScheduleNotFoundError):
            await schedules.unschedule(
                self_person_ref=other_self_person_ref,
                operation_id="operation:b02-d:cross-self-unschedule",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
            )

        revised = await schedules.revise_floating_schedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:conflict:revise",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=created.schedule.material_state_ref,
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=_floating_local(2026, 9, 9, 10, 0),
                ends_local_at=_floating_local(2026, 9, 9, 11, 0),
            ),
        )
        with pytest.raises(ScheduleUnscheduleConflictError):
            await schedules.unschedule(
                self_person_ref=self_person_ref,
                operation_id="operation:b02-d:conflict:stale",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
            )

        unscheduled = await schedules.unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:conflict:unschedule",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=revised.material_state_ref,
        )
        with pytest.raises(ScheduleOperationIdReuseError):
            await schedules.unschedule(
                self_person_ref=self_person_ref,
                operation_id="operation:b02-d:conflict:unschedule",
                schedule_ref=created.schedule.schedule_ref,
                expected_material_state_ref=created.schedule.material_state_ref,
            )

        with pytest.raises(ScheduleNotFoundError):
            await schedules.undo_unschedule(
                self_person_ref=other_self_person_ref,
                operation_id="operation:b02-d:cross-self-undo",
                schedule_ref=created.schedule.schedule_ref,
                unschedule_operation_id=unscheduled.unschedule_operation_id,
            )

        restored = await schedules.undo_unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:conflict:undo",
            schedule_ref=created.schedule.schedule_ref,
            unschedule_operation_id=unscheduled.unschedule_operation_id,
        )
        second_unschedule = await schedules.unschedule(
            self_person_ref=self_person_ref,
            operation_id="operation:b02-d:conflict:unschedule-2",
            schedule_ref=created.schedule.schedule_ref,
            expected_material_state_ref=restored.material_state_ref,
        )
        assert second_unschedule.previous_material_state_ref == (restored.material_state_ref)

        with pytest.raises(ScheduleUndoConflictError):
            await schedules.undo_unschedule(
                self_person_ref=self_person_ref,
                operation_id="operation:b02-d:conflict:stale-undo",
                schedule_ref=created.schedule.schedule_ref,
                unschedule_operation_id=unscheduled.unschedule_operation_id,
            )
    finally:
        await runtime.dispose()
