"""Real PostgreSQL proof for the B02-A Activity + Schedule atomic authoring slice."""

from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.activity import (
    ActivityOperationIdReuseError,
    CreateScheduledActivityResult,
    TemporalActivityApplication,
)
from dante.modules.temporal.application import (
    TemporalTimelineApplication,
    TimelineFloatingLocalActivityItem,
)
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.schedule import FloatingLocalIntervalPlacement
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.time import TimeZoneMode, TimeZonePolicy


def _floating_local(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    # A floating-local Schedule value intentionally has no timezone/offset.
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


def _canonical_rows(database: Any, self_person_ref: NativeRef) -> list[tuple[object, ...]]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return connection.execute(
            """
            SELECT intention.activity_ref,
                   schedule.schedule_ref,
                   current.material_state_ref,
                   payload.starts_local_at,
                   payload.ends_local_at,
                   history.current_from_at,
                   history.current_until_at,
                   receipt.operation_id,
                   receipt.intent_fingerprint
            FROM dante.activity_intention AS intention
            JOIN dante.schedule AS schedule
              ON schedule.subject_native_ref=intention.activity_ref
            JOIN dante.schedule_current_placement AS current
              ON current.scoped_owner_ref=schedule.schedule_ref
            JOIN dante.schedule_placement_floating_local_state AS payload
              ON payload.material_state_ref=current.material_state_ref
            JOIN dante.schedule_placement_current_history AS history
              ON history.schedule_ref=schedule.schedule_ref
             AND history.material_state_ref=current.material_state_ref
             AND history.current_until_at IS NULL
            JOIN dante.schedule_establish_operation AS receipt
              ON receipt.schedule_ref=schedule.schedule_ref
             AND receipt.material_state_ref=current.material_state_ref
            WHERE intention.self_person_ref=%s
            ORDER BY intention.created_at, schedule.schedule_ref
            """,
            (self_person_ref,),
        ).fetchall()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_scheduled_activity_create_is_atomic_idempotent_and_timeline_visible(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activity_application = TemporalActivityApplication(runtime.session_factory)
    timeline_application = TemporalTimelineApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 9, 15),
        ends_local_at=_floating_local(2026, 9, 9, 10, 45),
    )

    try:
        created = await activity_application.create_activity_with_floating_schedule(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-a:create-1",
            title="Deep work reale",
            placement=placement,
        )
        assert created.replayed is False
        assert created.activity.activity_ref.version == 7
        assert created.schedule.schedule_ref.version == 7
        assert created.schedule.material_state_ref.version == 7
        assert created.schedule.subject_native_ref == created.activity.activity_ref
        assert created.schedule.placement == placement

        replay = await activity_application.create_activity_with_floating_schedule(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id=" operation:b02-a:create-1 ",
            title=" Deep work reale ",
            placement=placement,
        )
        assert replay.replayed is True
        assert replay.activity.activity_ref == created.activity.activity_ref
        assert replay.schedule.schedule_ref == created.schedule.schedule_ref
        assert replay.schedule.material_state_ref == created.schedule.material_state_ref

        with pytest.raises(ActivityOperationIdReuseError):
            await activity_application.create_activity_with_floating_schedule(
                self_person_ref=self_person_ref,
                life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
                operation_id="operation:b02-a:create-1",
                title="Deep work reale",
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=_floating_local(2026, 9, 9, 9, 30),
                    ends_local_at=_floating_local(2026, 9, 9, 11, 0),
                ),
            )

        unplaced = await activity_application.list_unplaced(
            self_person_ref=self_person_ref,
        )
        assert unplaced == ()

        window = await timeline_application.read_window(
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
        assert item.placement_material_state_ref == created.schedule.material_state_ref
        assert item.starts_local_at == placement.starts_local_at
        assert item.ends_local_at == placement.ends_local_at
    finally:
        await runtime.dispose()

    rows = _canonical_rows(migrated_database, self_person_ref)
    assert len(rows) == 1
    assert UUID(str(rows[0][0])) == created.activity.activity_ref
    assert UUID(str(rows[0][1])) == created.schedule.schedule_ref
    assert UUID(str(rows[0][2])) == created.schedule.material_state_ref
    assert rows[0][3] == placement.starts_local_at
    assert rows[0][4] == placement.ends_local_at
    assert rows[0][6] is None
    assert rows[0][7] == "operation:b02-a:create-1"
    assert isinstance(rows[0][8], str)
    assert len(rows[0][8]) == 64


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_concurrent_same_scheduled_create_serializes_to_one_canonical_identity(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalActivityApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 14, 0),
        ends_local_at=_floating_local(2026, 9, 9, 14, 45),
    )

    async def create_once() -> CreateScheduledActivityResult:
        return await application.create_activity_with_floating_schedule(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-a:race",
            title="Concorrenza controllata",
            placement=placement,
        )

    try:
        left, right = await asyncio.gather(create_once(), create_once())
        assert left.activity.activity_ref == right.activity.activity_ref
        assert left.schedule.schedule_ref == right.schedule.schedule_ref
        assert left.schedule.material_state_ref == right.schedule.material_state_ref
        assert sorted([left.replayed, right.replayed]) == [False, True]
    finally:
        await runtime.dispose()

    assert len(_canonical_rows(migrated_database, self_person_ref)) == 1


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_prior_unplaced_command_id_cannot_be_reinterpreted_as_scheduled_create(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalActivityApplication(runtime.session_factory)

    try:
        unplaced = await application.create_activity(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-a:historical-unplaced",
            title="Intento già fissato",
        )
        assert unplaced.replayed is False

        with pytest.raises(ActivityOperationIdReuseError):
            await application.create_activity_with_floating_schedule(
                self_person_ref=self_person_ref,
                life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
                operation_id="operation:b02-a:historical-unplaced",
                title="Intento già fissato",
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=_floating_local(2026, 9, 9, 16, 0),
                    ends_local_at=_floating_local(2026, 9, 9, 17, 0),
                ),
            )
    finally:
        await runtime.dispose()

    assert _canonical_rows(migrated_database, self_person_ref) == []
