"""Self-scoped Activity Inspector profile and removal persistence."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest
from sqlalchemy import text
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_profile_revision_and_retirement_are_guarded_and_replayable(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="inspector:created",
            title="Prima",
            description="Note",
            location="Casa",
            item_color_code="#EA5C12",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            initial = (await session.execute(
                text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": actor, "activity": activity},
            )).mappings().one()
            assert initial["revision"] == 0
            assert initial["title"] == "Prima"
            assert (await session.execute(
                text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": other, "activity": activity},
            )).first() is None

        async with runtime.session_factory() as session, session.begin():
            params = {
                "actor": actor,
                "activity": activity,
                "operation": "inspector:edit",
                "revision": 0,
                "title": "Dopo",
                "description": "Nuove note",
                "location": None,
                "color": "#AABBCC",
            }
            sql = text("SELECT * FROM dante.revise_self_activity_profile("
                       ":actor,:activity,:operation,:revision,:title,:description,:location,:color)")
            first = (await session.execute(sql, params)).mappings().one()
            second = (await session.execute(sql, params)).mappings().one()
            assert first["revision"] == 1
            assert first["replayed"] is False
            assert second["replayed"] is True
            assert second["color_code"] == "#AABBCC"

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password,
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            previous, current = connection.execute(
                "SELECT previous_profile,current_profile "
                "FROM dante.activity_profile_revision WHERE activity_ref=%s",
                (activity,),
            ).fetchone()
            assert previous["title"] == "Prima"
            assert current["title"] == "Dopo"

        async with runtime.session_factory() as session, session.begin():
            assert await session.scalar(
                text("SELECT dante.retire_self_activity(:actor,:activity,:operation)"),
                {"actor": actor, "activity": activity, "operation": "inspector:retire"},
            ) is False
            assert await session.scalar(
                text("SELECT dante.retire_self_activity(:actor,:activity,:operation)"),
                {"actor": actor, "activity": activity, "operation": "inspector:retire"},
            ) is True
            assert (await session.execute(
                text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                {"actor": actor, "activity": activity},
            )).first() is None
    finally:
        await runtime.dispose()
