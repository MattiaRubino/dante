"""Self-scoped Activity Inspector profile and removal persistence."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import psycopg
import pytest
from fastapi import Request, Response
from psycopg import sql
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.activity_inspector_api import (
    ActivityHardDeleteCommand,
    ActivitySessionAttemptDeleteCommand,
    delete_self_activity_hard,
    delete_self_activity_session_attempt,
    get_self_activity_session_impact,
)
from dante.modules.temporal.authoring import ActivityChildIntent, TemporalAuthoringApplication
from dante.modules.temporal.reality_objective_api import (
    ObjectiveCreateCommand,
    create_activity_objective,
)
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.references import ScopedRecordRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_single_attempt_delete_preserves_sibling_and_named_configuration(
    migrated_database: Any,
) -> None:
    actor, other = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="inspector:single:create",
            title="Studio",
            planned_slices=(None,),
            planned_slice_names=("Ripasso",),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity})
            )
        named = next(row for row in snapshot.schedules if row.role_code == "planned")
        sessions = SessionApplication(runtime.session_factory)
        main = await sessions.start(
            self_person_ref=actor,
            operation_id="inspector:single:main",
            subject_kind="activity",
            subject_native_ref=activity,
        )
        child = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="inspector:single:child",
            activity_ref=activity,
            schedule_ref=ScopedRecordRef(named.schedule_ref),
        )
        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
        other_context = cast(DanteContext, SimpleNamespace(self_person_ref=other))
        impact = await get_self_activity_session_impact(activity, context, request, Response())
        command = ActivitySessionAttemptDeleteCommand(
            expected_session_fingerprint=impact.fingerprint
        )
        with pytest.raises(ProblemError) as foreign:
            await delete_self_activity_session_attempt(
                activity, child.session_ref, command, other_context, request, Response()
            )
        assert foreign.value.status == 404
        await delete_self_activity_session_attempt(
            activity, child.session_ref, command, context, request, Response()
        )
        remaining = await get_self_activity_session_impact(activity, context, request, Response())
        assert [row.session_ref for row in remaining.attempts] == [main.session_ref]
        async with runtime.session_factory() as session, session.begin():
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity})
            )
        assert any(row.schedule_ref == named.schedule_ref for row in snapshot.schedules)
        with pytest.raises(ProblemError) as stale:
            await delete_self_activity_session_attempt(
                activity, main.session_ref, command, context, request, Response()
            )
        assert stale.value.status == 409
        await delete_self_activity_session_attempt(
            activity,
            main.session_ref,
            ActivitySessionAttemptDeleteCommand(expected_session_fingerprint=remaining.fingerprint),
            context,
            request,
            Response(),
        )
        assert (
            await get_self_activity_session_impact(activity, context, request, Response())
        ).attempts == []
    finally:
        await runtime.dispose()


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
        initial = await get_self_activity_session_impact(activity, context, request, Response())
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
        active = await get_self_activity_session_impact(activity, context, request, Response())
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
        with pytest.raises(ProblemError) as error:
            await get_self_activity_session_impact(activity, other_context, request, Response())
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


@pytest.mark.asyncio
async def test_hard_delete_requires_fresh_owner_confirmation_and_removes_execution_graph(
    migrated_database: Any,
) -> None:
    actor, other = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authoring = TemporalAuthoringApplication(runtime.session_factory)
        created = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="hard-delete:created",
            title="Da eliminare",
            session_capture_mode="live",
            planned_slices=(None,),
            planned_slice_names=("Fase interna",),
        )
        retained = await authoring.create_activity(
            self_person_ref=other,
            operation_id="hard-delete:retained",
            title="Di un'altra persona",
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            planned_schedule_ref = await session.scalar(
                text(
                    "SELECT schedule_ref FROM dante.get_self_activity_schedule_roles("
                    ":actor, CAST(ARRAY[:activity] AS uuid[])) WHERE role_code='planned'"
                ),
                {"actor": actor, "activity": activity},
            )
        assert planned_schedule_ref is not None
        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
        other_context = cast(DanteContext, SimpleNamespace(self_person_ref=other))
        before = await get_self_activity_session_impact(activity, context, request, Response())
        sessions = SessionApplication(runtime.session_factory)
        main = await sessions.start(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=activity,
            operation_id="hard-delete:main",
        )
        named = await sessions.start_planned(
            self_person_ref=actor,
            operation_id="hard-delete:named",
            activity_ref=activity,
            schedule_ref=ScopedRecordRef(planned_schedule_ref),
        )
        impact = await get_self_activity_session_impact(activity, context, request, Response())
        assert {row.session_ref for row in impact.attempts} == {main.session_ref, named.session_ref}
        with pytest.raises(ProblemError) as stale:
            await delete_self_activity_hard(
                activity,
                ActivityHardDeleteCommand(expected_session_fingerprint=before.fingerprint),
                context,
                request,
                Response(),
            )
        assert stale.value.status == 409
        with pytest.raises(ProblemError) as unauthorized:
            await delete_self_activity_hard(
                activity,
                ActivityHardDeleteCommand(expected_session_fingerprint=impact.fingerprint),
                other_context,
                request,
                Response(),
            )
        assert unauthorized.value.status == 404
        result = await delete_self_activity_hard(
            activity,
            ActivityHardDeleteCommand(expected_session_fingerprint=impact.fingerprint),
            context,
            request,
            Response(),
        )
        assert result.deleted_rows > 0
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator",
                migrated_database.cluster.migrator_password,
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            for table, ref_column, ref in (
                ("activity", "activity_ref", activity),
                ("native_address", "native_ref", activity),
                ("session", "session_ref", main.session_ref),
                ("session", "session_ref", named.session_ref),
                ("schedule", "schedule_ref", planned_schedule_ref),
            ):
                assert connection.execute(
                    sql.SQL("SELECT count(*) FROM {} WHERE {}=%s").format(
                        sql.Identifier("dante", table), sql.Identifier(ref_column)
                    ),
                    (ref,),
                ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity WHERE activity_ref=%s",
                (retained.item.subject_native_ref,),
            ).fetchone() == (1,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_hard_delete_includes_polymorphically_owned_objectives(
    migrated_database: Any,
) -> None:
    actor, other = _seed_self(migrated_database), _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authoring = TemporalAuthoringApplication(runtime.session_factory)
        selected = await authoring.create_activity(
            self_person_ref=actor,
            operation_id="hard-delete:objective:selected",
            title="Activity con obiettivo",
        )
        retained = await authoring.create_activity(
            self_person_ref=other,
            operation_id="hard-delete:objective:other",
            title="Activity di altro utente",
        )
        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
        other_context = cast(DanteContext, SimpleNamespace(self_person_ref=other))
        first = await create_activity_objective(
            selected.item.subject_native_ref,
            ObjectiveCreateCommand(
                operation_id="hard-delete:objective:selected-create",
                label="Verifica completamento",
                result_kind="boolean",
                presentation_order=0,
            ),
            context,
            request,
            Response(),
        )
        second = await create_activity_objective(
            retained.item.subject_native_ref,
            ObjectiveCreateCommand(
                operation_id="hard-delete:objective:other-create",
                label="Obiettivo di altro utente",
                result_kind="boolean",
                presentation_order=0,
            ),
            other_context,
            request,
            Response(),
        )
        impact = await get_self_activity_session_impact(
            selected.item.subject_native_ref, context, request, Response()
        )
        deleted = await delete_self_activity_hard(
            selected.item.subject_native_ref,
            ActivityHardDeleteCommand(expected_session_fingerprint=impact.fingerprint),
            context,
            request,
            Response(),
        )
        assert deleted.deleted_rows > 0
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.temporal_objective WHERE objective_ref=%s",
                (first.objective_ref,),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.temporal_objective WHERE objective_ref=%s",
                (second.objective_ref,),
            ).fetchone() == (1,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_intention WHERE activity_ref=%s",
                (retained.item.subject_native_ref,),
            ).fetchone() == (1,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_activity_hard_delete_removes_child_native_identities(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="hard:activity:subtree",
            title="Activity principale",
            children=(
                ActivityChildIntent(
                    title="Figlia da eliminare",
                    requirement_code="required",
                    presentation_order=1,
                ),
            ),
        )
        root = created.item.subject_native_ref
        assert len(created.children) == 1
        child = created.children[0].item.subject_native_ref
        context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        impact = await get_self_activity_session_impact(root, context, request, Response())
        deleted = await delete_self_activity_hard(
            root,
            ActivityHardDeleteCommand(expected_session_fingerprint=impact.fingerprint),
            context,
            request,
            Response(),
        )
        assert deleted.deleted_rows > 0
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            for ref in (root, child):
                assert connection.execute(
                    "SELECT count(*) FROM dante.activity WHERE activity_ref=%s", (ref,)
                ).fetchone() == (0,)
                assert connection.execute(
                    "SELECT count(*) FROM dante.native_address WHERE native_ref=%s", (ref,)
                ).fetchone() == (0,)
    finally:
        await runtime.dispose()
