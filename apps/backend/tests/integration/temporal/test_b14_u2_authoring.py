"""B14-U2 PostgreSQL proof for optional organization and quick-authoring metadata."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.authoring import (
    AuthoringLifeAreaIntent,
    TemporalAuthoringApplication,
    TemporalAuthoringOperationIdReuseError,
)
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.schedule import FloatingLocalIntervalPlacement
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


@pytest.mark.asyncio
async def test_u2_unassigned_activity_metadata_multiday_schedule_and_replay(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = TemporalAuthoringApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=datetime(2026, 9, 30, 23, 30),
        ends_local_at=datetime(2026, 10, 2, 1, 0),
    )
    try:
        created = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="b14-u2:activity:unassigned",
            title="Camminata notturna",
            description="  Percorso lungo il fiume  ",
            location="  Lungofiume  ",
            item_color_code="#12abef",
            placement=placement,
        )
        assert created.item.life_area_ref is None
        assert created.item.life_area_assignment_revision is None
        assert created.item.description == "Percorso lungo il fiume"
        assert created.item.location == "Lungofiume"
        assert created.item.color_code == "#12ABEF"
        assert created.schedule is not None
        assert created.schedule.placement == placement
        assert not created.replayed

        replay = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="b14-u2:activity:unassigned",
            title="Camminata notturna",
            description="Percorso lungo il fiume",
            location="Lungofiume",
            item_color_code="#12ABEF",
            placement=placement,
        )
        assert replay.replayed
        assert replay.item.subject_native_ref == created.item.subject_native_ref
        assert replay.schedule is not None
        assert replay.schedule.schedule_ref == created.schedule.schedule_ref

        with pytest.raises(TemporalAuthoringOperationIdReuseError):
            await authoring.create_activity(
                self_person_ref=actor,
                operation_id="b14-u2:activity:unassigned",
                title="Camminata notturna",
                description="Percorso diverso",
                location="Lungofiume",
                item_color_code="#12ABEF",
                placement=placement,
            )

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            row = connection.execute(
                "SELECT description,location,color_code FROM dante.activity_intention "
                "WHERE activity_ref=%s",
                (created.item.subject_native_ref,),
            ).fetchone()
            assert row == ("Percorso lungo il fiume", "Lungofiume", "#12ABEF")
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_life_area_assignment "
                "WHERE activity_ref=%s",
                (created.item.subject_native_ref,),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_u2_event_can_create_life_area_with_color_atomically(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = TemporalAuthoringApplication(runtime.session_factory)
    try:
        created = await authoring.create_event(
            self_person_ref=actor,
            operation_id="b14-u2:event:new-area",
            title="Workshop",
            life_area_intent=AuthoringLifeAreaIntent(
                new_name="Studio",
                color_code="#8a4fff",
            ),
            description="Sessione di progettazione",
            location="Sala riunioni A",
            agenda_parts=("Revisione", "Decisioni"),
        )
        assert created.item.life_area_ref is not None
        assert created.item.life_area_assignment_revision == 1
        assert created.item.life_area_color_code == "#8A4FFF"
        assert created.item.life_area_revision == 2
        assert created.item.color_code is None
        assert created.item.description == "Sessione di progettazione"
        assert created.item.location == "Sala riunioni A"
        assert created.item.agenda_parts == ("Revisione", "Decisioni")

        replay = await authoring.create_event(
            self_person_ref=actor,
            operation_id="b14-u2:event:new-area",
            title="Workshop",
            life_area_intent=AuthoringLifeAreaIntent(
                new_name="Studio",
                color_code="#8A4FFF",
            ),
            description="Sessione di progettazione",
            location="Sala riunioni A",
            agenda_parts=("Revisione", "Decisioni"),
        )
        assert replay.replayed
        assert replay.item.subject_native_ref == created.item.subject_native_ref
        assert replay.item.life_area_ref == created.item.life_area_ref

        areas = await LifeAreaApplication(runtime.session_factory).list(self_person_ref=actor)
        assert [(area.name, area.color_code) for area in areas] == [("Studio", "#8A4FFF")]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_u2_existing_life_area_color_update_is_revision_guarded(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    authoring = TemporalAuthoringApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=actor,
                operation_id="b14-u2:area:existing",
                name="Corpo",
            )
        ).area
        created = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="b14-u2:activity:existing-area",
            title="Allenamento",
            life_area_intent=AuthoringLifeAreaIntent(
                life_area_ref=area.life_area_ref,
                expected_revision=area.revision,
                color_code="#00c896",
            ),
            location="Palestra",
        )
        assert created.item.life_area_ref == area.life_area_ref
        assert created.item.life_area_color_code == "#00C896"
        assert created.item.life_area_revision == 2
        assert created.item.color_code is None

        updated = await areas.list(self_person_ref=actor)
        assert len(updated) == 1
        assert updated[0].revision == 2
        assert updated[0].color_code == "#00C896"
    finally:
        await runtime.dispose()


def test_u2_authoring_acl_is_bounded(migrated_database: Any) -> None:
    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
    ) as connection:
        for signature in (
            "dante.create_self_activity_authoring(uuid,text,text,uuid,text,uuid,text,text,text)",
            "dante.create_self_event_authoring(uuid,text,text,uuid,text,text[],uuid,text,text,text)",
        ):
            assert connection.execute(
                "SELECT has_function_privilege('dante_runtime',%s,'EXECUTE')",
                (signature,),
            ).fetchone() == (True,)
        for table in ("activity_intention", "event_expectation"):
            assert connection.execute(
                "SELECT has_table_privilege('dante_runtime',%s,'SELECT'), "
                "has_table_privilege('dante_runtime',%s,'UPDATE')",
                (f"dante.{table}", f"dante.{table}"),
            ).fetchone() == (False, False)
