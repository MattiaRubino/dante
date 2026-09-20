"""B05-B direct PostgreSQL proof of typed self organization and legacy transition."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, date, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.activity import (
    ActivityLifeAreaUnavailableError,
    ActivityOperationIdReuseError,
    TemporalActivityApplication,
)
from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.life_area_assignment import (
    LifeAreaAssignmentApplication,
    LifeAreaAssignmentConflictError,
    LifeAreaAssignmentNotFoundError,
    LifeAreaAssignmentOperationIdReuseError,
)
from dante.modules.temporal.schedule import DateSpanPlacement
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


def _legacy_activity(database: Any, actor: NativeRef, title: str) -> NativeRef:
    """Simulate pre-B05 accepted data with the retained owner-only legacy helper."""
    fingerprint = hashlib.sha256(
        json.dumps(
            {"title": title}, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode()
    ).hexdigest()
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return NativeRef(
            connection.execute(
                "SELECT activity_ref FROM dante.create_self_activity(%s,%s,%s,%s,%s)",
                (actor, f"legacy:{uuid7()}", fingerprint, uuid7(), title),
            ).fetchone()[0]
        )


def _legacy_event(database: Any, actor: NativeRef, title: str) -> NativeRef:
    fingerprint = hashlib.sha256(
        json.dumps(
            {"title": title}, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode()
    ).hexdigest()
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return NativeRef(
            connection.execute(
                "SELECT event_ref FROM dante.create_self_event(%s,%s,%s,%s,%s)",
                (actor, f"legacy-event:{uuid7()}", fingerprint, uuid7(), title),
            ).fetchone()[0]
        )


@pytest.mark.asyncio
async def test_primary_assignment_create_reassign_archive_legacy_and_isolation(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    assignments = LifeAreaAssignmentApplication(runtime.session_factory)
    try:
        first = (
            await areas.create(self_person_ref=alice, operation_id="b05b:area:first", name="Studio")
        ).area
        second = (
            await areas.create(self_person_ref=alice, operation_id="b05b:area:second", name="Casa")
        ).area
        bob_area = (
            await areas.create(self_person_ref=bob, operation_id="b05b:bob:area", name="Casa")
        ).area
        created = await activities.create_activity(
            self_person_ref=alice,
            operation_id="b05b:activity",
            title="Leggere",
            life_area_ref=first.life_area_ref,
        )
        assert created.activity.life_area_ref == first.life_area_ref
        assert created.activity.life_area_assignment_revision == 1
        assert not created.replayed
        replay = await activities.create_activity(
            self_person_ref=alice,
            operation_id="b05b:activity",
            title="Leggere",
            life_area_ref=first.life_area_ref,
        )
        assert replay.replayed
        assert replay.activity.activity_ref == created.activity.activity_ref
        with pytest.raises(ActivityOperationIdReuseError):
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b05b:activity",
                title="Leggere",
                life_area_ref=second.life_area_ref,
            )

        scheduled = await events.create_event_with_schedule(
            self_person_ref=alice,
            operation_id="b05b:event",
            title="Viaggio",
            life_area_ref=first.life_area_ref,
            agenda_parts=("Preparare",),
            placement=DateSpanPlacement(
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 2),
            ),
        )
        assert scheduled.event.life_area_ref == first.life_area_ref
        assert scheduled.event.life_area_assignment_revision == 1
        assert scheduled.schedule.schedule_ref is not None
        event_replay = await events.create_event_with_schedule(
            self_person_ref=alice,
            operation_id="b05b:event",
            title="Viaggio",
            life_area_ref=first.life_area_ref,
            agenda_parts=("Preparare",),
            placement=DateSpanPlacement(
                start_date=date(2026, 10, 1),
                end_date_exclusive=date(2026, 10, 2),
            ),
        )
        assert event_replay.replayed
        assert event_replay.event.event_ref == scheduled.event.event_ref
        assert event_replay.schedule.schedule_ref == scheduled.schedule.schedule_ref

        moved = await assignments.assign(
            self_person_ref=alice,
            subject_kind="activity",
            subject_native_ref=created.activity.activity_ref,
            life_area_ref=second.life_area_ref,
            expected_assignment_revision=1,
            operation_id="b05b:move",
        )
        assert (moved.life_area_ref, moved.assignment_revision, moved.replayed) == (
            second.life_area_ref,
            2,
            False,
        )
        assert (
            await assignments.assign(
                self_person_ref=alice,
                subject_kind="activity",
                subject_native_ref=created.activity.activity_ref,
                life_area_ref=second.life_area_ref,
                expected_assignment_revision=1,
                operation_id="b05b:move",
            )
        ).replayed
        with pytest.raises(LifeAreaAssignmentOperationIdReuseError):
            await assignments.assign(
                self_person_ref=alice,
                subject_kind="activity",
                subject_native_ref=created.activity.activity_ref,
                life_area_ref=first.life_area_ref,
                expected_assignment_revision=1,
                operation_id="b05b:move",
            )
        with pytest.raises(LifeAreaAssignmentConflictError):
            await assignments.assign(
                self_person_ref=alice,
                subject_kind="activity",
                subject_native_ref=created.activity.activity_ref,
                life_area_ref=first.life_area_ref,
                expected_assignment_revision=1,
                operation_id="b05b:stale",
            )
        with pytest.raises(LifeAreaAssignmentNotFoundError):
            await assignments.assign(
                self_person_ref=bob,
                subject_kind="activity",
                subject_native_ref=created.activity.activity_ref,
                life_area_ref=bob_area.life_area_ref,
                expected_assignment_revision=0,
                operation_id="b05b:foreign",
            )
        legacy = _legacy_activity(migrated_database, alice, "Legacy senza area")
        legacy_event = _legacy_event(migrated_database, alice, "Legacy Event senza area")
        assert [
            (item.subject_kind, item.subject_native_ref)
            for item in await assignments.list_unassigned(self_person_ref=alice)
        ] == [("activity", legacy), ("event", legacy_event)]
        assigned_legacy = await assignments.assign(
            self_person_ref=alice,
            subject_kind="activity",
            subject_native_ref=legacy,
            life_area_ref=second.life_area_ref,
            expected_assignment_revision=0,
            operation_id="b05b:legacy",
        )
        assert assigned_legacy.assignment_revision == 1
        assert (
            await assignments.assign(
                self_person_ref=alice,
                subject_kind="event",
                subject_native_ref=legacy_event,
                life_area_ref=first.life_area_ref,
                expected_assignment_revision=0,
                operation_id="b05b:legacy-event",
            )
        ).assignment_revision == 1
        assert await assignments.list_unassigned(self_person_ref=alice) == ()

        await areas.mutate(
            self_person_ref=alice,
            operation_id="b05b:archive",
            life_area_ref=second.life_area_ref,
            expected_revision=1,
            kind="archive",
        )
        assert {
            entry.subject_native_ref: entry.life_area_ref
            for entry in await assignments.list_assignments(self_person_ref=alice)
        }[legacy] == second.life_area_ref
        assert (await assignments.list_assignments(self_person_ref=bob)) == ()
        with pytest.raises(LifeAreaAssignmentNotFoundError):
            await assignments.assign(
                self_person_ref=alice,
                subject_kind="event",
                subject_native_ref=scheduled.event.event_ref,
                life_area_ref=second.life_area_ref,
                expected_assignment_revision=1,
                operation_id="b05b:archived",
            )
        with pytest.raises(ActivityLifeAreaUnavailableError):
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b05b:invalid-new",
                title="Non deve esistere",
                life_area_ref=second.life_area_ref,
            )
        assert await activities.get_activity(self_person_ref=alice, activity_ref=legacy) is not None
        assert (
            await activities.get_activity(
                self_person_ref=alice, activity_ref=created.activity.activity_ref
            )
        ).life_area_ref == second.life_area_ref
        assert (
            await events.get_event(self_person_ref=alice, event_ref=scheduled.event.event_ref)
        ).life_area_ref == first.life_area_ref
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_intention WHERE title=%s",
                ("Non deve esistere",),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_life_area_assignment_operation "
                "WHERE self_person_ref=%s AND activity_ref=%s",
                (alice, created.activity.activity_ref),
            ).fetchone() == (2,)
    finally:
        await runtime.dispose()


def test_primary_assignment_acl_only_bounded_functions(migrated_database: Any) -> None:
    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
    ) as connection:
        for table in (
            "activity_life_area_assignment",
            "event_life_area_assignment",
            "activity_life_area_assignment_operation",
            "event_life_area_assignment_operation",
        ):
            assert connection.execute(
                "SELECT has_table_privilege('dante_runtime',%s,'SELECT'), "
                "has_table_privilege('dante_runtime',%s,'INSERT')",
                (f"dante.{table}", f"dante.{table}"),
            ).fetchone() == (False, False)
        for signature in (
            "dante.assign_self_activity_life_area(uuid,text,text,uuid,uuid,bigint)",
            "dante.assign_self_event_life_area(uuid,text,text,uuid,uuid,bigint)",
            "dante.create_self_activity_in_life_area(uuid,text,text,uuid,text,uuid)",
            "dante.create_self_event_with_agenda_in_life_area(uuid,text,text,uuid,text,text[],uuid)",
            "dante.list_self_life_area_assignments(uuid)",
            "dante.list_self_unassigned_life_area_items(uuid)",
        ):
            assert connection.execute(
                "SELECT has_function_privilege('dante_runtime',%s,'EXECUTE')",
                (signature,),
            ).fetchone() == (True,)
        for signature in (
            "dante.create_self_activity(uuid,text,text,uuid,text)",
            "dante.create_self_event(uuid,text,text,uuid,text)",
            "dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[])",
        ):
            assert connection.execute(
                "SELECT has_function_privilege('dante_runtime',%s,'EXECUTE')",
                (signature,),
            ).fetchone() == (False,)
