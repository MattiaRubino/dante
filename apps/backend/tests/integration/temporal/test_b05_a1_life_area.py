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
            self_person_ref=alice, operation_id="b05-a1:create:palestra", name=" Palestra "
        )
        assert created.area.name == "Palestra"
        assert not created.replayed
        replay = await application.create(
            self_person_ref=alice, operation_id="b05-a1:create:palestra", name="Palestra"
        )
        assert replay.replayed
        assert replay.area == created.area
        with pytest.raises(LifeAreaOperationIdReuseError):
            await application.create(
                self_person_ref=alice, operation_id="b05-a1:create:palestra", name="Inglese"
            )

        second = await application.create(
            self_person_ref=bob, operation_id="b05-a1:create:palestra", name="Palestra"
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
        **migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password
        )
    ) as connection:
        assert connection.execute(
            "SELECT has_table_privilege('dante_runtime','dante.life_area','SELECT'), "
            "has_table_privilege('dante_runtime','dante.life_area','INSERT'), "
            "has_table_privilege('dante_runtime','dante.life_area_create_operation','SELECT'), "
            "has_function_privilege('dante_runtime',"
            "'dante.create_self_life_area(uuid,text,text,uuid,text)','EXECUTE'), "
            "has_function_privilege('dante_runtime',"
            "'dante.list_self_life_areas(uuid)','EXECUTE')"
        ).fetchone() == (False, False, False, True, True)
