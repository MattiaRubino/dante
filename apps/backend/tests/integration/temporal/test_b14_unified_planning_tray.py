"""B14 product proof for one canonical Activity/Event `Da collocare` tray."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.planning_tray import TemporalPlanningTrayApplication
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    TemporalScheduleApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _seed_self(database: Any) -> NativeRef:
    person_ref = NativeRef(uuid7())
    account_ref = uuid7()
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (person_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at) "
            "VALUES (%s,'active',%s,NULL)",
            (account_ref, datetime.now(UTC)),
        )
        connection.execute(
            "INSERT INTO dante.account_application_context("
            "account_ref,self_person_ref,timezone_mode,fixed_zone_id) "
            "VALUES (%s,%s,'follow_device',NULL)",
            (account_ref, person_ref),
        )
    return person_ref


def _placement(hour: int) -> FloatingLocalIntervalPlacement:
    return FloatingLocalIntervalPlacement(
        starts_local_at=datetime(2026, 10, 2, hour, 0),
        ends_local_at=datetime(2026, 10, 2, hour + 1, 0),
    )


@pytest.mark.asyncio
async def test_unified_tray_lists_and_places_activity_and_event(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = TemporalAuthoringApplication(runtime.session_factory)
    tray = TemporalPlanningTrayApplication(runtime.session_factory)
    try:
        activity = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="b14-tray:activity:create",
            title="Preparare documenti",
        )
        event = await authoring.create_event(
            self_person_ref=actor,
            operation_id="b14-tray:event:create",
            title="Cena con Marco",
        )

        items = await tray.list_items(self_person_ref=actor)
        assert {(item.kind, item.state, item.subject_ref) for item in items} == {
            ("activity", "unplaced", activity.item.subject_native_ref),
            ("event", "unplaced", event.item.subject_native_ref),
        }

        placed = await tray.place_item(
            self_person_ref=actor,
            kind="event",
            subject_ref=event.item.subject_native_ref,
            operation_id="b14-tray:event:place",
            placement=_placement(19),
        )
        assert placed.kind == "event"
        assert placed.subject_ref == event.item.subject_native_ref

        remaining = await tray.list_items(self_person_ref=actor)
        assert [(item.kind, item.subject_ref) for item in remaining] == [
            ("activity", activity.item.subject_native_ref)
        ]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_postponed_event_reuses_retained_schedule_from_same_tray(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = TemporalAuthoringApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    tray = TemporalPlanningTrayApplication(runtime.session_factory)
    try:
        event = await authoring.create_event(
            self_person_ref=actor,
            operation_id="b14-tray:postponed:create",
            title="Visita medica",
            placement=_placement(9),
        )
        assert event.schedule is not None
        original_schedule_ref = event.schedule.schedule_ref

        await schedules.unschedule(
            self_person_ref=actor,
            operation_id="b14-tray:postponed:unschedule",
            schedule_ref=event.schedule.schedule_ref,
            expected_material_state_ref=event.schedule.material_state_ref,
        )

        items = await tray.list_items(self_person_ref=actor)
        assert len(items) == 1
        postponed = items[0]
        assert postponed is not None
        assert postponed.kind == "event"
        assert postponed.state == "postponed"
        assert postponed.subject_ref == event.item.subject_native_ref
        assert postponed.schedule_ref == original_schedule_ref

        replanned = await tray.place_item(
            self_person_ref=actor,
            kind="event",
            subject_ref=event.item.subject_native_ref,
            operation_id="b14-tray:postponed:replan",
            placement=_placement(11),
        )
        assert replanned.schedule_ref == original_schedule_ref
        assert await tray.list_items(self_person_ref=actor) == ()
    finally:
        await runtime.dispose()
