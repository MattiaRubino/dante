"""B14 Draft Vault PostgreSQL: owner/CAS/replay and no operational writes."""

from __future__ import annotations

import json
from typing import Any
from uuid import uuid7

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_inert_drafts_are_owner_scoped_replay_safe_and_do_not_create_subjects(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    draft = uuid7()
    payload = json.dumps({
        "version": 1,
        "fields": {"kind": "activity", "title": "Allenamento"},
        "advanced": {"activityStructure": {"plannedSlices": [
            {"title": "Corsa", "startTime": "17:00"}
        ]}},
        "surface": "full",
    })
    try:
        async def save(op: str, expected: int | None, title: str = "Allenamento"):
            async with runtime.session_factory() as session, session.begin():
                return (await session.execute(text("""
                    SELECT * FROM dante.save_self_temporal_draft(
                        :actor,:draft,:op,:rev,'activity',:title,CAST(:data AS jsonb))
                """), {"actor": actor, "draft": draft, "op": op,
                       "rev": expected, "title": title,
                       "data": payload})).mappings().one()

        before = await save("vault:create", None)
        assert before["revision"] == 1
        slices = before["payload"]["advanced"]["activityStructure"]["plannedSlices"]
        assert slices[0]["title"] == "Corsa"
        replay = await save("vault:create", None)
        assert replay["draft_ref"] == draft
        assert replay["revision"] == 1

        async with runtime.session_factory() as session:
            own = (await session.execute(text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """), {"actor": actor})).mappings().all()
            elsewhere = (await session.execute(text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """), {"actor": other})).mappings().all()
        assert [row["draft_ref"] for row in own] == [draft]
        assert elsewhere == []

        with pytest.raises(DBAPIError):
            await save("vault:stale", None, "Stale")
        updated = await save("vault:revise", 1, "Allenamento completo")
        assert updated["revision"] == 2
        assert updated["title"] == "Allenamento completo"

        async with runtime.session_factory() as session, session.begin():
            await session.execute(text("""
                SELECT dante.retire_self_temporal_draft(:actor,:draft,:rev)
            """), {"actor": actor, "draft": draft, "rev": 2})
        async with runtime.session_factory() as session:
            assert (await session.execute(text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """), {"actor": actor})).mappings().all() == []
    finally:
        await runtime.dispose()
