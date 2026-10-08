"""M4 Event Inspector metadata: self ownership, CAS, replay and immutable audit."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from tests.integration.temporal.test_b05_primary_life_area_assignment import (
    _legacy_event,
    _seed_self,
)

from dante.modules.temporal.event import TemporalEventApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres

_EDIT = text("""
    SELECT * FROM dante.revise_self_event_profile(
        :actor,:event,:operation,:expected,:title,:description,:location,:color
    )
""")


@pytest.mark.asyncio
async def test_event_profile_is_guarded_and_current_read_tracks_append_only_edits(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Original")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    command = {
        "actor": owner,
        "event": event,
        "operation": "m4:metadata:edit",
        "expected": 0,
        "title": "Modificato",
        "description": "Descrizione",
        "location": "Sala A",
        "color": "#ABCDEF",
    }
    try:
        async with runtime.session_factory() as session, session.begin():
            first = (await session.execute(_EDIT, command)).mappings().one()
            replay = (await session.execute(_EDIT, command)).mappings().one()
        assert first["event_ref"] == event
        assert first["revision"] == 1
        assert first["replayed"] is False
        assert replay["revision"] == 1
        assert replay["replayed"] is True

        canonical = await TemporalEventApplication(runtime.session_factory).get_event(
            self_person_ref=owner, event_ref=event,
        )
        assert canonical is not None
        assert canonical.title == "Modificato"
        assert canonical.description == "Descrizione"
        assert canonical.location == "Sala A"
        assert canonical.color_code == "#ABCDEF"
        assert canonical.profile_revision == 1

        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password,
        )) as db:
            db.execute("SET ROLE dante_owner")
            before, after = db.execute(
                "SELECT previous_profile,current_profile FROM dante.event_profile_revision "
                "WHERE event_ref=%s AND revision=1",
                (event,),
            ).fetchone()
        assert before["title"] == "Original"
        assert after["title"] == "Modificato"

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(_EDIT, {**command, "operation": "m4:stale"})
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(_EDIT, {
                    **command, "actor": stranger, "operation": "m4:foreign",
                })
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(_EDIT, {
                    **command, "title": "Reused with different intent",
                })

        canonical_after = await TemporalEventApplication(runtime.session_factory).get_event(
            self_person_ref=owner, event_ref=event,
        )
        assert canonical_after is not None
        assert canonical_after.title == "Modificato"
        assert canonical_after.profile_revision == 1
    finally:
        await runtime.dispose()
