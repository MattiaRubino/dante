"""A recurring Activity keeps each named untimed planned Session unplaced."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from typing import Any, cast

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_objective_recurring_instance_scope import _read_checkpoint_refs
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.activity_inspector_api import (
    ActivityHardDeleteCommand,
    delete_self_activity_hard,
    get_self_activity_session_impact,
)
from dante.modules.temporal.occurrence import OccurrencePersistenceError
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_recurring_activity_keeps_untimed_planned_session(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="recurring:untimed:create",
            title="Raccolta",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=30,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [{"name": "Cernita", "time_enabled": False}],
            },
        )
        await RoutineOccurrenceMaterializationApplication(
            runtime.session_factory
        ).checkpoint_window(
            self_person_ref=actor,
            operation_id="recurring:untimed:window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 7),
            effective_zone_id="Europe/Rome",
        )
        occurrences = await _read_checkpoint_refs(
            runtime,
            actor,
            routine.source_ref,
            owner="routine",
            operation="recurring:untimed:window",
            start=date(2026, 10, 6),
            end=date(2026, 10, 7),
        )
        assert len(occurrences) == 1
        async with runtime.session_factory() as session, session.begin():
            activity = (
                await session.execute(
                    text("""
                SELECT activity_ref FROM dante.list_self_routine_occurrence_activities(
                    :actor, CAST(ARRAY[:occurrence] AS uuid[])
                )
            """),
                    {
                        "actor": actor,
                        "occurrence": occurrences[0],
                    },
                )
            ).scalar_one()
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(
                    _SNAPSHOT,
                    {"actor": actor, "activity": activity},
                )
            )
        planned = [row for row in snapshot.schedules if row.role_code == "planned"]
        assert len(planned) == 1
        assert planned[0].display_name == "Cernita"
        assert planned[0].placement_material_state_ref is None
        request = cast(
            Request,
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
        )
        context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
        impact = await get_self_activity_session_impact(activity, context, request, Response())
        with pytest.raises(ProblemError) as recurring_scope:
            await delete_self_activity_hard(
                activity,
                ActivityHardDeleteCommand(expected_session_fingerprint=impact.fingerprint),
                context,
                request,
                Response(),
            )
        assert recurring_scope.value.status == 409
        assert recurring_scope.value.code == "temporal.activity_lifecycle.recurring_scope_required"
        async with runtime.session_factory() as session, session.begin():
            assert (
                await session.scalar(
                    text(
                        "SELECT activity_ref FROM dante.get_self_activity_profile(:actor,:activity)"
                    ),
                    {"actor": actor, "activity": activity},
                )
                == activity
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_activity_retry_after_binding_failure_creates_one_complete_instance(
    migrated_database: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="recurring:rollback:create",
            title="Raccolta",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=90,
            reminder_lead_minutes=10,
            activity_template={
                "version": 1,
                "root_window": {"start_offset_minutes": 0, "duration_minutes": 90},
                "activity_intervals": [
                    {"start_offset_minutes": 0, "duration_minutes": 30},
                    {"start_offset_minutes": 60, "duration_minutes": 30},
                ],
                "planned_slices": [{"name": "Cernita", "time_enabled": False}],
                "objectives": [
                    {"label": "Completato", "result_kind": "boolean", "presentation_order": 0}
                ],
            },
        )
        materialization = RoutineOccurrenceMaterializationApplication(runtime.session_factory)

        async def fail_binding(**_kwargs: Any) -> None:
            raise OccurrencePersistenceError("Injected failure after Activity authoring")

        original_bind = materialization._bind_activity
        monkeypatch.setattr(materialization, "_bind_activity", fail_binding)

        async def checkpoint() -> None:
            await materialization.checkpoint_window(
                self_person_ref=actor,
                operation_id="recurring:rollback:window",
                start_date=date(2026, 10, 6),
                end_date_exclusive=date(2026, 10, 7),
                effective_zone_id="Europe/Rome",
            )

        with pytest.raises(OccurrencePersistenceError, match="Injected failure"):
            await checkpoint()
        occurrences = await _read_checkpoint_refs(
            runtime,
            actor,
            routine.source_ref,
            owner="routine",
            operation="recurring:rollback:window",
            start=date(2026, 10, 6),
            end=date(2026, 10, 7),
        )
        assert len(occurrences) == 1
        operation = f"b14:occurrence-activity:{occurrences[0]}"
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_create_operation "
                "WHERE self_person_ref=%s AND operation_id=%s",
                (actor, operation),
            ).fetchone() == (0,)
        monkeypatch.setattr(materialization, "_bind_activity", original_bind)
        await checkpoint()
        async with runtime.session_factory() as session, session.begin():
            bindings = (
                (
                    await session.execute(
                        text(
                            "SELECT activity_ref FROM dante.list_self_routine_occurrence_activities("
                            ":actor, CAST(ARRAY[:occurrence] AS uuid[]))"
                        ),
                        {"actor": actor, "occurrence": occurrences[0]},
                    )
                )
                .scalars()
                .all()
            )
            assert len(bindings) == 1
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(_SNAPSHOT, {"actor": actor, "activity": bindings[0]})
            )
        assert any(
            row.role_code == "envelope" and row.placement_material_state_ref
            for row in snapshot.schedules
        )
        assert any(
            row.role_code == "planned" and row.display_name == "Cernita"
            for row in snapshot.schedules
        )
        assert sum(row.role_code == "interval" for row in snapshot.schedules) == 2
    finally:
        await runtime.dispose()
