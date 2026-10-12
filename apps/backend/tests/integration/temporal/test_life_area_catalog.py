"""Real PostgreSQL proof for the initial LR-12 Life Area catalog boundary."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.life_area import (
    LifeAreaApplication,
    LifeAreaOperationIdReuseError,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _seed_self(database: Any) -> NativeRef:
    """Establish an existing Person and independent Account application context."""
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
async def test_life_area_catalog_replay_isolation_and_no_native_owner(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = LifeAreaApplication(runtime.session_factory)
    try:
        created = await application.create(
            self_person_ref=alice, operation_id="b05-a:create:palestra", name=" Palestra "
        )
        assert created.area.name == "Palestra"
        assert not created.replayed
        replay = await application.create(
            self_person_ref=alice, operation_id="b05-a:create:palestra", name="Palestra"
        )
        assert replay.replayed
        assert replay.area == created.area
        with pytest.raises(LifeAreaOperationIdReuseError):
            await application.create(
                self_person_ref=alice, operation_id="b05-a:create:palestra", name="Inglese"
            )

        second = await application.create(
            self_person_ref=bob, operation_id="b05-a:create:palestra", name="Palestra"
        )
        assert second.area.life_area_ref != created.area.life_area_ref
        assert await application.list(self_person_ref=alice) == (created.area,)
        assert await application.list(self_person_ref=bob) == (second.area,)

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.native_address WHERE native_ref=%s",
                (created.area.life_area_ref,),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.life_area_create_operation WHERE life_area_ref=%s",
                (created.area.life_area_ref,),
            ).fetchone() == (1,)
    finally:
        await runtime.dispose()


def test_life_area_runtime_has_no_raw_table_access(migrated_database: Any) -> None:
    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
    ) as connection:
        assert connection.execute(
            "SELECT has_table_privilege('dante_runtime','dante.life_area','SELECT'), "
            "has_table_privilege('dante_runtime','dante.life_area','INSERT'), "
            "has_table_privilege('dante_runtime','dante.life_area_create_operation','SELECT'), "
            "has_table_privilege('dante_runtime','dante.life_area_mutation_operation','SELECT'), "
            "has_function_privilege('dante_runtime',"
            "'dante.create_self_life_area(uuid,text,text,uuid,text)','EXECUTE'), "
            "has_function_privilege('dante_runtime',"
            "'dante.list_self_life_areas(uuid)','EXECUTE'), "
            "has_function_privilege('dante_runtime',"
            "'dante.mutate_self_life_area(uuid,text,text,uuid,bigint,text,text,boolean,text,text)','EXECUTE'), "
            "has_function_privilege('dante_runtime',"
            "'dante.reorder_self_life_areas(uuid,text,text,uuid[],bigint[])','EXECUTE')"
        ).fetchone() == (False, False, False, False, True, True, True, True)


@pytest.mark.asyncio
async def test_life_area_full_lifecycle_replay_order_and_actor_isolation(
    migrated_database: Any,
) -> None:
    from dante.modules.temporal.life_area import (
        LifeAreaNotFoundError,
        LifeAreaStateConflictError,
    )

    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    app = LifeAreaApplication(runtime.session_factory)
    try:
        first = (
            await app.create(self_person_ref=alice, operation_id="create:first", name="Work")
        ).area
        second = (
            await app.create(self_person_ref=alice, operation_id="create:second", name="Home")
        ).area
        assert (first.sort_order, second.sort_order) == (0, 1)
        assert first.revision == second.revision == 1
        with pytest.raises(LifeAreaNotFoundError):
            await app.mutate(
                self_person_ref=bob,
                operation_id="foreign",
                life_area_ref=first.life_area_ref,
                expected_revision=1,
                kind="rename",
                name="No",
            )
        renamed = await app.mutate(
            self_person_ref=alice,
            operation_id="rename",
            life_area_ref=first.life_area_ref,
            expected_revision=1,
            kind="rename",
            name=" Studio ",
        )
        assert renamed.accepted_revision == 2
        assert not renamed.replayed
        assert (
            await app.mutate(
                self_person_ref=alice,
                operation_id="rename",
                life_area_ref=first.life_area_ref,
                expected_revision=1,
                kind="rename",
                name="Studio",
            )
        ).replayed
        with pytest.raises(LifeAreaOperationIdReuseError):
            await app.mutate(
                self_person_ref=alice,
                operation_id="rename",
                life_area_ref=first.life_area_ref,
                expected_revision=1,
                kind="rename",
                name="Other",
            )
        with pytest.raises(LifeAreaStateConflictError):
            await app.mutate(
                self_person_ref=alice,
                operation_id="stale",
                life_area_ref=first.life_area_ref,
                expected_revision=1,
                kind="visibility",
                hidden=True,
            )
        hidden = await app.mutate(
            self_person_ref=alice,
            operation_id="hide",
            life_area_ref=first.life_area_ref,
            expected_revision=2,
            kind="visibility",
            hidden=True,
        )
        assert hidden.accepted_revision == 3
        shown = await app.mutate(
            self_person_ref=alice,
            operation_id="show",
            life_area_ref=first.life_area_ref,
            expected_revision=3,
            kind="visibility",
            hidden=False,
        )
        assert shown.accepted_revision == 4
        styled = await app.mutate(
            self_person_ref=alice,
            operation_id="style",
            life_area_ref=first.life_area_ref,
            expected_revision=4,
            kind="appearance",
            icon_code="star",
            color_code="#aa33cc",
        )
        assert styled.accepted_revision == 5
        removed_style = await app.mutate(
            self_person_ref=alice,
            operation_id="clear-style",
            life_area_ref=first.life_area_ref,
            expected_revision=5,
            kind="appearance",
        )
        assert removed_style.accepted_revision == 6
        archived = await app.mutate(
            self_person_ref=alice,
            operation_id="archive",
            life_area_ref=first.life_area_ref,
            expected_revision=6,
            kind="archive",
        )
        assert archived.accepted_revision == 7
        with pytest.raises(LifeAreaStateConflictError):
            await app.mutate(
                self_person_ref=alice,
                operation_id="archive-again",
                life_area_ref=first.life_area_ref,
                expected_revision=7,
                kind="archive",
            )
        with pytest.raises(LifeAreaStateConflictError):
            await app.reorder(
                self_person_ref=alice, operation_id="missing", entries=((second.life_area_ref, 1),)
            )
        with pytest.raises(LifeAreaStateConflictError):
            await app.reorder(
                self_person_ref=alice,
                operation_id="duplicate",
                entries=((first.life_area_ref, 6), (second.life_area_ref, 1)),
            )
        reordered = await app.reorder(
            self_person_ref=alice,
            operation_id="reorder",
            entries=((second.life_area_ref, 1), (first.life_area_ref, 7)),
        )
        assert reordered.affected_count == 2
        assert not reordered.replayed
        assert (
            await app.reorder(
                self_person_ref=alice,
                operation_id="reorder",
                entries=((second.life_area_ref, 1), (first.life_area_ref, 7)),
            )
        ).replayed
        with pytest.raises(LifeAreaOperationIdReuseError):
            await app.reorder(
                self_person_ref=alice,
                operation_id="reorder",
                entries=((first.life_area_ref, 7), (second.life_area_ref, 1)),
            )
        areas = await app.list(self_person_ref=alice)
        assert [a.life_area_ref for a in areas] == [second.life_area_ref, first.life_area_ref]
        assert [(a.sort_order, a.revision) for a in areas] == [(0, 2), (1, 8)]
        assert areas[1].archived
        assert not areas[1].hidden
        assert areas[1].icon_code is None
        assert areas[1].color_code is None
        assert await app.list(self_person_ref=bob) == ()
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_life_area_same_key_concurrent_create_and_mutation_are_single_acceptance(
    migrated_database: Any,
) -> None:
    import asyncio

    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    app = LifeAreaApplication(runtime.session_factory)
    try:
        first, replay = await asyncio.gather(
            app.create(self_person_ref=alice, operation_id="parallel:create", name="Shared"),
            app.create(self_person_ref=alice, operation_id="parallel:create", name="Shared"),
        )
        assert first.area.life_area_ref == replay.area.life_area_ref
        assert {first.replayed, replay.replayed} == {False, True}
        accepted, retried = await asyncio.gather(
            app.mutate(
                self_person_ref=alice,
                operation_id="parallel:hide",
                life_area_ref=first.area.life_area_ref,
                expected_revision=1,
                kind="visibility",
                hidden=True,
            ),
            app.mutate(
                self_person_ref=alice,
                operation_id="parallel:hide",
                life_area_ref=first.area.life_area_ref,
                expected_revision=1,
                kind="visibility",
                hidden=True,
            ),
        )
        assert {accepted.replayed, retried.replayed} == {False, True}
        assert accepted.accepted_revision == retried.accepted_revision == 2
        assert (await app.list(self_person_ref=alice))[0].revision == 2
    finally:
        await runtime.dispose()
