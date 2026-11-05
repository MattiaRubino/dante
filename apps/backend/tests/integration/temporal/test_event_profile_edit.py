"""M4 Event Inspector metadata: self ownership, CAS, replay and immutable audit."""

from __future__ import annotations

from typing import Any
from uuid import uuid7

import psycopg
import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.test_primary_life_area_assignment import (
    _legacy_event,
    _seed_self,
)

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.reality_objective_api import (
    ActivityObjectiveBatchCommand,
    apply_event_objective_edits_in_session,
)
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres

_EDIT = text("""
    SELECT * FROM dante.revise_self_event_profile(
        :actor,:event,:operation,:expected,:title,:description,:location,:color
    )
""")

_CREATE_OBJECTIVE = text("""
    SELECT * FROM dante.create_self_temporal_objective(
        :actor,:operation,:fingerprint,:objective,'event',:event,
        :label,'boolean',NULL,NULL,NULL,NULL,NULL,0
    )
""")
_RETIRE_OBJECTIVE = text("""
    SELECT * FROM dante.retire_self_temporal_objective(
        :actor,:objective,:operation,:fingerprint,:expected
    )
""")


@pytest.mark.asyncio
async def test_one_off_event_objective_batch_rolls_back_revision_when_retirement_is_stale(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "One-off")
    revised, removed = uuid7(), uuid7()
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.session_factory() as session, session.begin():
            for index, objective in enumerate((revised, removed)):
                await session.execute(
                    _CREATE_OBJECTIVE,
                    {
                        "actor": owner,
                        "operation": f"event:batch:create:{index}",
                        "fingerprint": f"{index + 1}" * 64,
                        "objective": objective,
                        "event": event,
                        "label": f"Original {index}",
                    },
                )
        command = {
            "add": [
                {
                    "operation_id": "event:batch:add",
                    "label": "Nuovo",
                    "result_kind": "boolean",
                    "presentation_order": 2,
                }
            ],
            "revise": [
                {
                    "objective_ref": revised,
                    "change": {
                        "operation_id": "event:batch:revise",
                        "expected_revision": 0,
                        "label": "Aggiornato",
                        "result_kind": "boolean",
                        "presentation_order": 0,
                    },
                }
            ],
            "retire": [
                {
                    "objective_ref": removed,
                    "operation_id": "event:batch:retire",
                    "expected_revision": 1,
                }
            ],
        }

        async def reject_stale_batch() -> None:
            async with runtime.session_factory() as session, session.begin():
                await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                await apply_event_objective_edits_in_session(
                    session,
                    actor=owner,
                    subject_ref=event,
                    payload=ActivityObjectiveBatchCommand.model_validate(command),
                    effective_zone_id="Europe/Rome",
                )

        with pytest.raises(DBAPIError):
            await reject_stale_batch()

        async with runtime.session_factory() as session, session.begin():
            before = (
                await session.execute(
                    text("SELECT * FROM dante.list_self_temporal_objectives(:actor,'event',:event)"),
                    {"actor": owner, "event": event},
                )
            ).mappings().all()
        assert {row["label"] for row in before} == {"Original 0", "Original 1"}

        command["retire"][0]["expected_revision"] = 0
        async with runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            after = await apply_event_objective_edits_in_session(
                session,
                actor=owner,
                subject_ref=event,
                payload=ActivityObjectiveBatchCommand.model_validate(command),
                effective_zone_id="Europe/Rome",
            )
        assert {row.label for row in after} == {"Aggiornato", "Nuovo"}

        command["revise"][0]["change"]["scope_code"] = "this_and_following"
        with pytest.raises(ProblemError):
            async with runtime.session_factory() as session, session.begin():
                await apply_event_objective_edits_in_session(
                    session,
                    actor=owner,
                    subject_ref=event,
                    payload=ActivityObjectiveBatchCommand.model_validate(command),
                    effective_zone_id="Europe/Rome",
                )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_event_objective_retirement_is_owner_scoped_replayable_and_revision_guarded(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "One-off")
    objective = uuid7()
    runtime = create_database_runtime(migrated_database.runtime_settings())
    command = {
        "actor": owner,
        "objective": objective,
        "operation": "event:objective:retire",
        "fingerprint": "b" * 64,
        "expected": 0,
    }
    try:
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                _CREATE_OBJECTIVE,
                {
                    "actor": owner,
                    "operation": "event:objective:create",
                    "fingerprint": "a" * 64,
                    "objective": objective,
                    "event": event,
                    "label": "Arrivare",
                },
            )

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _RETIRE_OBJECTIVE,
                    {**command, "actor": stranger, "operation": "event:foreign"},
                )
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _RETIRE_OBJECTIVE,
                    {**command, "operation": "event:stale", "expected": 1},
                )

        async with runtime.session_factory() as session, session.begin():
            applied = (await session.execute(_RETIRE_OBJECTIVE, command)).mappings().one()
            replay = (await session.execute(_RETIRE_OBJECTIVE, command)).mappings().one()
        assert applied["objective_ref"] == objective
        assert applied["replayed"] is False
        assert replay["replayed"] is True

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _RETIRE_OBJECTIVE,
                    {**command, "operation": "event:reused", "fingerprint": "c" * 64},
                )

        async with runtime.session_factory() as session, session.begin():
            current = (
                await session.execute(
                    text("SELECT * FROM dante.list_self_temporal_objectives(:actor,'event',:event)"),
                    {"actor": owner, "event": event},
                )
            ).all()
        assert current == []
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as db:
            db.execute("SET ROLE dante_owner")
            tombstone = db.execute(
                "SELECT retired_at,retirement_operation_id FROM dante.temporal_objective "
                "WHERE objective_ref=%s",
                (objective,),
            ).fetchone()
        assert tombstone is not None
        assert tombstone[0] is not None
        assert tombstone[1] == command["operation"]
    finally:
        await runtime.dispose()


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
            self_person_ref=owner,
            event_ref=event,
        )
        assert canonical is not None
        assert canonical.title == "Modificato"
        assert canonical.description == "Descrizione"
        assert canonical.location == "Sala A"
        assert canonical.color_code == "#ABCDEF"
        assert canonical.profile_revision == 1

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator",
                migrated_database.cluster.migrator_password,
            )
        ) as db:
            db.execute("SET ROLE dante_owner")
            fetched_row = db.execute(
                "SELECT previous_profile,current_profile FROM dante.event_profile_revision "
                "WHERE event_ref=%s AND revision=1",
                (event,),
            ).fetchone()
            assert fetched_row is not None
            before, after = fetched_row
        assert before["title"] == "Original"
        assert after["title"] == "Modificato"

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(_EDIT, {**command, "operation": "m4:stale"})
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _EDIT,
                    {
                        **command,
                        "actor": stranger,
                        "operation": "m4:foreign",
                    },
                )
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _EDIT,
                    {
                        **command,
                        "title": "Reused with different intent",
                    },
                )

        canonical_after = await TemporalEventApplication(runtime.session_factory).get_event(
            self_person_ref=owner,
            event_ref=event,
        )
        assert canonical_after is not None
        assert canonical_after.title == "Modificato"
        assert canonical_after.profile_revision == 1
    finally:
        await runtime.dispose()
