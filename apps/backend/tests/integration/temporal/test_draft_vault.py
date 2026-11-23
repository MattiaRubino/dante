"""B14 Draft Vault PostgreSQL: owner/CAS/replay and no operational writes."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.support.life_area import ensure_test_life_area
from tests.integration.temporal.test_schedule_create import _context

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.draft_vault_api import (
    DraftVaultMoveRequest,
    DraftVaultSaveRequest,
    delete_draft,
    list_drafts,
    move_self_item_to_draft,
    save_draft,
)
from dante.modules.temporal.event import TemporalEventApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

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
async def test_inert_drafts_are_owner_scoped_replay_safe_and_do_not_create_subjects(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    draft = uuid7()
    payload = json.dumps(
        {
            "version": 1,
            "fields": {"kind": "activity", "title": "Allenamento"},
            "advanced": {
                "activityStructure": {"plannedSlices": [{"title": "Corsa", "startTime": "17:00"}]}
            },
            "surface": "full",
        }
    )
    try:

        async def save(op: str, expected: int | None, title: str = "Allenamento") -> RowMapping:
            async with runtime.session_factory() as session, session.begin():
                return (
                    (
                        await session.execute(
                            text("""
                    SELECT * FROM dante.save_self_temporal_draft(
                        :actor,:draft,:op,:rev,'activity',:title,CAST(:data AS jsonb))
                """),
                            {
                                "actor": actor,
                                "draft": draft,
                                "op": op,
                                "rev": expected,
                                "title": title,
                                "data": payload,
                            },
                        )
                    )
                    .mappings()
                    .one()
                )

        before = await save("vault:create", None)
        assert before["revision"] == 1
        slices = before["payload"]["advanced"]["activityStructure"]["plannedSlices"]
        assert slices[0]["title"] == "Corsa"
        replay = await save("vault:create", None)
        assert replay["draft_ref"] == draft
        assert replay["revision"] == 1

        async with runtime.session_factory() as session, session.begin():
            own = (
                (
                    await session.execute(
                        text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """),
                        {"actor": actor},
                    )
                )
                .mappings()
                .all()
            )
            elsewhere = (
                (
                    await session.execute(
                        text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """),
                        {"actor": other},
                    )
                )
                .mappings()
                .all()
            )
        assert [row["draft_ref"] for row in own] == [draft]
        assert elsewhere == []

        with pytest.raises(DBAPIError):
            await save("vault:stale", None, "Stale")
        updated = await save("vault:revise", 1, "Allenamento completo")
        assert updated["revision"] == 2
        assert updated["title"] == "Allenamento completo"

        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text("""
                SELECT dante.retire_self_temporal_draft(:actor,:draft,:rev)
            """),
                {"actor": actor, "draft": draft, "rev": 2},
            )
        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.execute(
                    text("""
                SELECT * FROM dante.list_self_temporal_drafts(:actor)
            """),
                    {"actor": actor},
                )
            ).mappings().all() == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_draft_vault_http_capability_returns_saved_snapshot_and_cas_delete(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    draft_ref = uuid7()
    context = _context(actor)
    request = Request(
        {
            "type": "http",
            "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
        }
    )
    payload = {
        "version": 1,
        "fields": {"kind": "event", "title": "Visita"},
        "advanced": {"eventParticipants": []},
        "surface": "full",
    }
    try:
        saved = await save_draft(
            draft_ref,
            DraftVaultSaveRequest(
                draft_ref=draft_ref,
                operation_id="vault:event:save",
                expected_revision=None,
                subject_kind="event",
                title="Visita",
                payload=payload,
            ),
            context,
            request,
            Response(),
        )
        assert saved.payload == payload
        assert saved.subject_kind == "event"
        assert saved.revision == 1
        listed = await list_drafts(context, request, Response())
        assert [item.draft_ref for item in listed] == [draft_ref]
        await delete_draft(draft_ref, 1, context, request, Response())
        assert await list_drafts(context, request, Response()) == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_standalone_event_moves_atomically_to_an_inert_draft(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    area = ensure_test_life_area(migrated_database, actor)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    context = _context(actor)
    request = Request({
        "type": "http",
        "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
    })
    draft_ref = uuid7()
    try:
        created = await TemporalEventApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="move:event:create",
            title="Visita",
            life_area_ref=area,
        )
        event_ref = created.event.event_ref
        async with runtime.session_factory() as session, session.begin():
            fingerprint = await session.scalar(
                text(
                    "SELECT dante.get_self_temporal_hard_delete_fingerprint("
                    ":actor,:source,'event_once')"
                ),
                {"actor": actor, "source": event_ref},
            )
        assert fingerprint is not None
        snapshot = {
            "version": 1,
            "fields": {"kind": "event", "title": "Visita"},
            "advanced": {"eventParticipants": [], "objectives": []},
            "surface": "full",
        }
        request_body = DraftVaultMoveRequest(
            draft_ref=draft_ref,
            operation_id="move:event:commit",
            subject_kind="event",
            title="Visita",
            payload=snapshot,
            expected_fingerprint=fingerprint,
        )
        with pytest.raises(ProblemError) as stale:
            await move_self_item_to_draft(
                event_ref,
                request_body.model_copy(update={"expected_fingerprint": "0" * 64}),
                context,
                request,
                Response(),
            )
        assert stale.value.status == 409
        assert await list_drafts(context, request, Response()) == []

        moved = await move_self_item_to_draft(
            event_ref, request_body, context, request, Response()
        )
        assert moved.draft_ref == draft_ref
        assert moved.payload == snapshot
        assert [item.draft_ref for item in await list_drafts(context, request, Response())] == [
            draft_ref
        ]
        # Verify physical root deletion through the privileged test harness,
        # not by calling a preview function that raises for a missing Event.
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            remaining = connection.execute(
                "SELECT count(*) FROM dante.event_expectation "
                "WHERE event_ref=%s AND self_person_ref=%s",
                (event_ref, actor),
            ).fetchone()
        assert remaining is not None and remaining[0] == 0
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_standalone_activity_moves_atomically_without_leaving_product_identity(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    area = ensure_test_life_area(migrated_database, actor)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    context = _context(actor)
    request = Request({
        "type": "http",
        "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
    })
    draft_ref = uuid7()
    try:
        created = await TemporalActivityApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="move:activity:create",
            title="Allenamento",
            life_area_ref=area,
        )
        activity_ref = created.activity.activity_ref
        async with runtime.session_factory() as session, session.begin():
            original = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_activity_profile(:actor,:source)"),
                        {"actor": actor, "source": activity_ref},
                    )
                )
                .mappings()
                .one()
            )
            fingerprint = await session.scalar(
                text("SELECT dante.get_self_activity_session_impact_hash(:actor,:source)"),
                {"actor": actor, "source": activity_ref},
            )
        assert fingerprint is not None
        snapshot = {
            "version": 1,
            "fields": {"kind": "activity", "title": "Allenamento"},
            "advanced": {"activityStructure": {"plannedSlices": []}, "objectives": []},
            "surface": "full",
        }
        request_body = DraftVaultMoveRequest(
            draft_ref=draft_ref,
            operation_id="move:activity:commit",
            subject_kind="activity",
            title="Allenamento",
            payload=snapshot,
            expected_fingerprint=fingerprint,
            expected_profile_revision=original["revision"],
        )
        with pytest.raises(ProblemError) as stale:
            await move_self_item_to_draft(
                activity_ref,
                request_body.model_copy(update={"expected_profile_revision": original["revision"] + 1}),
                context,
                request,
                Response(),
            )
        assert stale.value.status == 409
        assert await list_drafts(context, request, Response()) == []

        moved = await move_self_item_to_draft(
            activity_ref, request_body, context, request, Response()
        )
        assert moved.draft_ref == draft_ref
        assert moved.payload == snapshot
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            existing = connection.execute(
                "SELECT count(*) FROM dante.activity_intention "
                "WHERE activity_ref=%s AND self_person_ref=%s",
                (activity_ref, actor),
            ).fetchone()
        assert existing is not None and existing[0] == 0
    finally:
        await runtime.dispose()
