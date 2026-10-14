"""Self-scoped Activity Inspector profile and removal persistence."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_inspector_api import get_self_activity_session_impact
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres



@pytest.mark.asyncio
async def test_session_impact_lists_only_owned_attempts_and_changes_token_on_transition(
    migrated_database: Any,
) -> None:
    actor, other = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="inspector:impact:create",
            title="Conserva esecuzioni",
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
        other_context = cast(DanteContext, SimpleNamespace(self_person_ref=other))
        initial = await get_self_activity_session_impact(
            activity, context, request, Response()
        )
        assert initial.activity_ref == activity
        assert initial.attempts == []
        assert len(initial.fingerprint) == 64

        sessions = SessionApplication(runtime.session_factory)
        started = await sessions.start(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=activity,
            operation_id="inspector:impact:start",
        )
        active = await get_self_activity_session_impact(
            activity, context, request, Response()
        )
        assert active.fingerprint != initial.fingerprint
        assert len(active.attempts) == 1
        assert active.attempts[0].session_ref == started.session_ref
        assert active.attempts[0].status == "in corso"
        paused = await sessions.pause(
            self_person_ref=actor,
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
            operation_id="inspector:impact:pause",
        )
        pause_impact = await get_self_activity_session_impact(
            activity, context, request, Response()
        )
        assert pause_impact.fingerprint != active.fingerprint
        assert pause_impact.attempts[0].status == "in pausa"
        assert pause_impact.attempts[0].timing_material_state_ref == (
            paused.timing_material_state_ref
        )
        with pytest.raises(Exception) as error:
            await get_self_activity_session_impact(
                activity, other_context, request, Response()
            )
        assert getattr(error.value, "status", None) == 404
    finally:
        await runtime.dispose()


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
            initial = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                        {"actor": actor, "activity": activity},
                    )
                )
                .mappings()
                .one()
            )
            assert initial["revision"] == 0
            assert initial["title"] == "Prima"
            assert (
                await session.execute(
                    text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                    {"actor": other, "activity": activity},
                )
            ).first() is None

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
            sql = text(
                "SELECT * FROM dante.revise_self_activity_profile("
                ":actor,:activity,:operation,:revision,:title,:description,:location,:color)"
            )
            first = (await session.execute(sql, params)).mappings().one()
            second = (await session.execute(sql, params)).mappings().one()
            assert first["revision"] == 1
            assert first["replayed"] is False
            assert second["replayed"] is True
            assert second["color_code"] == "#AABBCC"

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator",
                migrated_database.cluster.migrator_password,
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            fetched_row = connection.execute(
                "SELECT previous_profile,current_profile "
                "FROM dante.activity_profile_revision WHERE activity_ref=%s",
                (activity,),
            ).fetchone()
            assert fetched_row is not None
            previous, current = fetched_row
            assert previous["title"] == "Prima"
            assert current["title"] == "Dopo"

        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.scalar(
                    text("SELECT dante.retire_self_activity(:actor,:activity,:operation)"),
                    {"actor": actor, "activity": activity, "operation": "inspector:retire"},
                )
                is False
            )
            assert (
                await session.scalar(
                    text("SELECT dante.retire_self_activity(:actor,:activity,:operation)"),
                    {"actor": actor, "activity": activity, "operation": "inspector:retire"},
                )
                is True
            )
            assert (
                await session.execute(
                    text("SELECT * FROM dante.get_self_activity_profile(:actor,:activity)"),
                    {"actor": actor, "activity": activity},
                )
            ).first() is None
    finally:
        await runtime.dispose()
