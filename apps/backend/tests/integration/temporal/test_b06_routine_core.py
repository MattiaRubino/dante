"""B06-A PostgreSQL proof: Routine source is not recurrence, occurrence or Schedule."""

from __future__ import annotations

from datetime import date, time
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.product_tag import ProductTagApplication
from dante.modules.temporal.routine import (
    RoutineApplication,
    RoutineOperationReuseError,
    RoutineStateConflictError,
)
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_routine_source_lifecycle_primary_area_tags_and_replay(migrated_database: Any) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    tags = ProductTagApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    try:
        studio = (await areas.create(self_person_ref=alice, operation_id="area:studio", name="Studio")).area
        health = (await areas.create(self_person_ref=alice, operation_id="area:health", name="Salute")).area
        tag, _ = await tags.create(self_person_ref=alice, operation_id="tag:focus", name="Focus")
        created = await routines.create(
            self_person_ref=alice, operation_id="routine:create", title=" Allenamento ",
            life_area_ref=studio.life_area_ref, starts_on=date(2026, 9, 21),
            wall_time=time(7, 30), tag_refs=(tag.tag_ref,),
        )
        assert created.title == "Allenamento"
        assert created.lifecycle_state == "active"
        assert created.source_revision == 1
        assert created.life_area_ref == studio.life_area_ref
        assert created.tag_refs == (tag.tag_ref,)
        replay = await routines.create(
            self_person_ref=alice, operation_id="routine:create", title="Allenamento",
            life_area_ref=studio.life_area_ref, starts_on=date(2026, 9, 21),
            wall_time=time(7, 30), tag_refs=(tag.tag_ref,),
        )
        assert replay.replayed and replay.routine_ref == created.routine_ref
        with pytest.raises(RoutineOperationReuseError):
            await routines.create(self_person_ref=alice, operation_id="routine:create", title="Altro", life_area_ref=studio.life_area_ref, starts_on=date(2026, 9, 21))

        paused = await routines.mutate(self_person_ref=alice, operation_id="routine:pause", routine_ref=created.routine_ref, expected_source_revision=1, kind="pause")
        assert paused.lifecycle_state == "paused" and paused.source_revision == 2
        resumed = await routines.mutate(self_person_ref=alice, operation_id="routine:resume", routine_ref=created.routine_ref, expected_source_revision=2, kind="resume")
        assert resumed.lifecycle_state == "active" and resumed.source_revision == 3
        renamed = await routines.mutate(self_person_ref=alice, operation_id="routine:rename", routine_ref=created.routine_ref, expected_source_revision=3, kind="rename", title="Allenamento leggero")
        assert renamed.source_revision == 4
        with pytest.raises(RoutineStateConflictError):
            await routines.mutate(self_person_ref=alice, operation_id="routine:stale", routine_ref=created.routine_ref, expected_source_revision=3, kind="end")

        moved = await routines.assign_life_area(self_person_ref=alice, operation_id="routine:area", routine_ref=created.routine_ref, life_area_ref=health.life_area_ref, expected_assignment_revision=1)
        assert moved.assignment_revision == 2 and moved.life_area_ref == health.life_area_ref
        detached = await routines.set_tag(self_person_ref=alice, operation_id="routine:tag:detach", routine_ref=created.routine_ref, tag_ref=tag.tag_ref, attached=False)
        assert not detached.attached
        visible = await routines.list(self_person_ref=alice)
        assert len(visible) == 1 and visible[0].tag_refs == () and visible[0].life_area_ref == health.life_area_ref
        assert await routines.list(self_person_ref=bob) == ()

        with psycopg.connect(**migrated_database.connection_kwargs("dante_migrator", migrated_database.cluster.migrator_password)) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute("SELECT count(*) FROM dante.occurrence").fetchone() == (0,)
            assert connection.execute("SELECT count(*) FROM dante.schedule").fetchone() == (0,)
            assert connection.execute("SELECT count(*) FROM dante.routine_recurrence_state WHERE routine_ref=%s", (created.routine_ref,)).fetchone() == (1,)
            assert connection.execute("SELECT count(*) FROM dante.routine_operation WHERE routine_ref=%s", (created.routine_ref,)).fetchone() == (4,)
    finally:
        await runtime.dispose()


def test_routine_runtime_has_execute_only_capabilities(migrated_database: Any) -> None:
    with psycopg.connect(host=migrated_database.cluster.host, port=migrated_database.cluster.port, dbname=migrated_database.name, user=migrated_database.cluster.admin_user, password=migrated_database.cluster.admin_password) as connection:
        assert connection.execute("SELECT has_table_privilege('dante_runtime','dante.routine_intention','SELECT'), has_table_privilege('dante_runtime','dante.routine_operation','INSERT'), has_function_privilege('dante_runtime','dante.create_self_routine(uuid,text,text,uuid,text,uuid,uuid[],date,time)','EXECUTE'), has_function_privilege('dante_runtime','dante.list_self_routines(uuid)','EXECUTE')").fetchone() == (False, False, True, True)
