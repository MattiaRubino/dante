"""PostgreSQL integration: irreversible Event and recurring Activity deletion scopes."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from typing import Any, cast

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone

from dante.context.contracts import DanteContext
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.reality_objective_api import (
    TemporalHardDeleteCommand,
    apply_temporal_hard_deletion,
    preview_temporal_hard_deletion,
)
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _request(runtime: Any) -> Request:
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


def _context(actor: Any) -> DanteContext:
    return cast(DanteContext, SimpleNamespace(self_person_ref=actor))


async def _preview(runtime: Any, actor: Any, ref: Any, scope: str) -> str:
    result = await preview_temporal_hard_deletion(
        ref, scope, _context(actor), _request(runtime), Response()
    )
    assert result.scope == scope
    assert len(result.fingerprint) == 64
    return result.fingerprint


async def _delete(runtime: Any, actor: Any, ref: Any, scope: str, fingerprint: str) -> int:
    result = await apply_temporal_hard_deletion(
        ref,
        TemporalHardDeleteCommand(scope=scope, expected_fingerprint=fingerprint),
        _context(actor),
        _request(runtime),
        Response(),
    )
    assert result.requested_ref == ref
    assert result.deleted_rows > 0
    return result.deleted_rows


def _owner_sql(database: Any, sql_text: str, args: tuple[Any, ...]) -> list[tuple[Any, ...]]:
    # Introspection is exclusively for the test owner role, never runtime DML.
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator", database.cluster.migrator_password
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return list(connection.execute(sql_text, args).fetchall())


def _occurrences(database: Any, source: Any) -> list[Any]:
    return [
        row[0]
        for row in _owner_sql(
            database,
            "SELECT occurrence_ref FROM dante.occurrence_generation "
            "WHERE source_native_ref=%s ORDER BY occurrence_ref",
            (source,),
        )
    ]


def _exists(database: Any, sql_text: str, ref: Any) -> bool:
    return bool(_owner_sql(database, sql_text, (ref,))[0][0])


async def _activity_for(runtime: Any, actor: Any, occurrence: Any) -> Any:
    async with runtime.session_factory() as session, session.begin():
        return await session.scalar(
            text(
                "SELECT activity_ref FROM dante.list_self_routine_occurrence_activities("
                ":actor,CAST(ARRAY[:occurrence] AS uuid[]))"
            ),
            {"actor": actor, "occurrence": occurrence},
        )


@pytest.mark.asyncio
async def test_recurring_activity_instance_skip_and_whole_series_no_regeneration(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="hard:activity:routine",
            title="Ricorrenza da eliminare",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=45,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [{"name": "Fase", "time_enabled": False}],
            },
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:activity:window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        occurrences = _occurrences(migrated_database, routine.source_ref)
        assert len(occurrences) == 2
        first, second = occurrences
        first_activity = await _activity_for(runtime, actor, first)
        second_activity = await _activity_for(runtime, actor, second)
        assert first_activity is not None and second_activity is not None

        with pytest.raises(ProblemError) as foreign:
            await _preview(runtime, stranger, first_activity, "activity_instance")
        assert foreign.value.status == 404

        fingerprint = await _preview(runtime, actor, first_activity, "activity_instance")
        await _delete(runtime, actor, first_activity, "activity_instance", fingerprint)
        assert await _activity_for(runtime, actor, first) is None
        assert await _activity_for(runtime, actor, second) == second_activity

        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.routine_intention WHERE routine_ref=%s)",
            routine.source_ref,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:activity:replay",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert await _activity_for(runtime, actor, first) is None

        series = await _preview(runtime, actor, second_activity, "activity_series")
        await _delete(runtime, actor, second_activity, "activity_series", series)
        assert _occurrences(migrated_database, routine.source_ref) == []
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.routine WHERE routine_ref=%s",
                (routine.source_ref,),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity WHERE activity_ref IN (%s,%s)",
                (first_activity, second_activity),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_event_single_occurrence_then_full_series(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        created = await RecurringAuthoringApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="hard:event:create",
            title="Eventi ricorrenti",
            agenda_parts=("Agenda",),
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await EventOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=40,
            duration_days=None,
            reminder_lead_minutes=10,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:event:checkpoint",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        first, second = _occurrences(migrated_database, created.source_ref)
        fingerprint = await _preview(runtime, actor, first, "event_instance")
        await _delete(runtime, actor, first, "event_instance", fingerprint)
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
            first,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
            second,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:event:after-single",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
            first,
        )

        series = await _preview(runtime, actor, second, "event_series")
        await _delete(runtime, actor, second, "event_series", series)
        assert _occurrences(migrated_database, created.source_ref) == []
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            created.source_ref,
        )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_single_event_delete_keeps_unrelated_actors(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authoring = TemporalAuthoringApplication(runtime.session_factory)
        selected = await authoring.create_event(
            self_person_ref=actor,
            operation_id="hard:oneoff:owner",
            title="Evento singolo",
        )
        retained = await authoring.create_event(
            self_person_ref=stranger,
            operation_id="hard:oneoff:other",
            title="Evento estraneo",
        )
        ref = selected.item.subject_native_ref
        impact = await _preview(runtime, actor, ref, "event_once")
        await _delete(runtime, actor, ref, "event_once", impact)
        assert not _exists(
            migrated_database, "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            ref,
        )
        assert _exists(
            migrated_database, "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            retained.item.subject_native_ref,
        )
    finally:
        await runtime.dispose()
