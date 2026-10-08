"""B14-M3: optional primary Life Area and stable planned Session labels."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.life_area_assignment import (
    LifeAreaAssignmentApplication,
    LifeAreaAssignmentConflictError,
    LifeAreaAssignmentNotFoundError,
    LifeAreaAssignmentOperationIdReuseError,
)
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import (
    _legacy_activity,
    _legacy_event,
    _seed_self,
)

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_primary_life_area_null_is_versioned_and_replayable(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    activity = _legacy_activity(migrated_database, actor, "Area opzionale")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    app = LifeAreaAssignmentApplication(runtime.session_factory)
    area_app = LifeAreaApplication(runtime.session_factory)
    try:
        area = (await area_app.create(
            self_person_ref=actor, operation_id="m3:area", name="Personale",
        )).area
        assigned = await app.assign(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=activity, life_area_ref=area.life_area_ref,
            expected_assignment_revision=0, operation_id="m3:assign",
        )
        assert assigned.assignment_revision == 1

        removed = await app.assign(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=activity, life_area_ref=None,
            expected_assignment_revision=1, operation_id="m3:unassign",
        )
        assert removed.life_area_ref is None
        assert removed.assignment_revision == 2
        assert not removed.replayed

        replay = await app.assign(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=activity, life_area_ref=None,
            expected_assignment_revision=1, operation_id="m3:unassign",
        )
        assert replay.replayed
        assert replay.assignment_revision == 2
        assert any(row.subject_native_ref == activity for row in
                   await app.list_unassigned(self_person_ref=actor))
        values = await app.list_assignments(self_person_ref=actor)
        assert any(row.subject_native_ref == activity and
                   row.life_area_ref is None and row.assignment_revision == 2
                   for row in values)

        with pytest.raises(LifeAreaAssignmentOperationIdReuseError):
            await app.assign(
                self_person_ref=actor, subject_kind="activity",
                subject_native_ref=activity, life_area_ref=area.life_area_ref,
                expected_assignment_revision=1, operation_id="m3:unassign",
            )
        with pytest.raises(LifeAreaAssignmentConflictError):
            await app.assign(
                self_person_ref=actor, subject_kind="activity",
                subject_native_ref=activity, life_area_ref=area.life_area_ref,
                expected_assignment_revision=1, operation_id="m3:stale",
            )
        with pytest.raises(LifeAreaAssignmentNotFoundError):
            await app.assign(
                self_person_ref=other, subject_kind="activity",
                subject_native_ref=activity, life_area_ref=None,
                expected_assignment_revision=2, operation_id="m3:other",
            )
        back = await app.assign(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=activity, life_area_ref=area.life_area_ref,
            expected_assignment_revision=2, operation_id="m3:restore",
        )
        assert back.assignment_revision == 3
        assert not any(row.subject_native_ref == activity for row in
                       await app.list_unassigned(self_person_ref=actor))
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_planned_session_rename_keeps_schedule_identity_and_owner(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    window = NamedZoneLocalIntervalPlacement(
        starts_local_at=datetime(2026, 10, 9, 9),  # noqa: DTZ001
        ends_local_at=datetime(2026, 10, 9, 11),  # noqa: DTZ001
        zone_id="Europe/Rome",
    )
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="m3:planned", title="Studio",
            placement=window, activity_intervals=(window,),
            planned_slices=(window,), planned_slice_names=("Lettura",),
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            role = (await session.execute(text("""
                SELECT * FROM dante.get_self_activity_schedule_roles(
                    :actor,CAST(ARRAY[:activity] AS uuid[]))
                WHERE role_code='planned'
            """), {"actor": actor, "activity": activity})).mappings().one()
        schedule = role["schedule_ref"]
        async with runtime.session_factory() as session, session.begin():
            sql = text("""
                SELECT * FROM dante.revise_self_planned_session_name(
                    :actor,:activity,:schedule,:expected,:next)
            """)
            args = {"actor": actor, "activity": activity,
                    "schedule": schedule, "expected": "Lettura", "next": "Ripasso"}
            changed = (await session.execute(sql, args)).mappings().one()
            assert changed["schedule_ref"] == schedule
            assert changed["display_name"] == "Ripasso"
            assert not changed["replayed"]
            replay = (await session.execute(sql, args)).mappings().one()
            assert replay["replayed"]
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(sql, {**args, "expected": "Lettura", "next": "Errato"})
        # The rejected command runs in a separate transaction and cannot undo the accepted label.
        async with runtime.session_factory() as session, session.begin():
            current = (await session.execute(text("""
                SELECT * FROM dante.get_self_activity_schedule_roles(
                    :actor,CAST(ARRAY[:activity] AS uuid[]))
                WHERE role_code='planned'
            """), {"actor": actor, "activity": activity})).mappings().one()
            assert current["schedule_ref"] == schedule
            assert current["display_name"] == "Ripasso"
            assert (await session.execute(text("""
                SELECT * FROM dante.get_self_activity_schedule_roles(
                    :actor,CAST(ARRAY[:activity] AS uuid[]))
                WHERE role_code='planned'
            """), {"actor": other, "activity": activity})).first() is None
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_event_unassignment_has_the_same_cas_and_replay_policy(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, actor, "Evento da classificare")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    app = LifeAreaAssignmentApplication(runtime.session_factory)
    try:
        area = (await LifeAreaApplication(runtime.session_factory).create(
            self_person_ref=actor, operation_id="m3:event:area", name="Evento",
        )).area
        first = await app.assign(
            self_person_ref=actor, subject_kind="event", subject_native_ref=event,
            life_area_ref=area.life_area_ref,
            expected_assignment_revision=0, operation_id="m3:event:assigned",
        )
        assert first.assignment_revision == 1
        removed = await app.assign(
            self_person_ref=actor, subject_kind="event", subject_native_ref=event,
            life_area_ref=None, expected_assignment_revision=1,
            operation_id="m3:event:unassigned",
        )
        assert removed.life_area_ref is None
        assert removed.assignment_revision == 2
        assert (await app.assign(
            self_person_ref=actor, subject_kind="event", subject_native_ref=event,
            life_area_ref=None, expected_assignment_revision=1,
            operation_id="m3:event:unassigned",
        )).replayed
        assert any(row.subject_native_ref == event for row in
                   await app.list_unassigned(self_person_ref=actor))
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_retirement_rejects_recorded_past_execution_without_erasing_it(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    activity = _legacy_activity(migrated_database, actor, "Lavoro svolto")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    sessions = SessionApplication(runtime.session_factory)
    end = datetime.now(UTC) - timedelta(hours=2)
    start = end - timedelta(minutes=30)
    try:
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_runtime", migrated_database.cluster.runtime_password,
        )) as connection:
            connection.execute(
                "SELECT * FROM dante.set_self_activity_execution_policy(%s,%s,%s,%s,%s,%s,%s)",
                (actor, "m3:record-policy", hashlib.sha256(b"m3:record-policy").hexdigest(),
                 activity, uuid7(), "record", None),
            )
        recorded = await sessions.record_manual(
            self_person_ref=actor, operation_id="m3:manual",
            activity_ref=activity, started_at=start, ended_at=end,
        )
        with pytest.raises(DBAPIError) as failure:
            async with runtime.session_factory() as session, session.begin():
                await session.scalar(text(
                    "SELECT dante.retire_self_activity(:actor,:activity,:operation)"
                ), {"actor": actor, "activity": activity, "operation": "m3:retire"})
        assert getattr(failure.value.orig.diag, "constraint_name", None) == (
            "activity_profile_recorded_truth"
        )
        assert [row.session_ref for row in await sessions.list_for_subject(
            self_person_ref=actor, subject_native_ref=activity,
        )] == [recorded.session_ref]
    finally:
        await runtime.dispose()
