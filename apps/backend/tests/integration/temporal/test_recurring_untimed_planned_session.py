"""A recurring Activity keeps each named untimed planned Session unplaced."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast
from zoneinfo import ZoneInfo

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
from dante.modules.temporal.recurrence import RecurrenceApplication
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
async def test_checkpoint_after_instance_profile_edit_preserves_bound_activity(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    day = datetime.now(ZoneInfo("Europe/Rome")).date() + timedelta(days=2)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        routine = await RecurringAuthoringApplication(
            runtime.session_factory
        ).create_routine(
            self_person_ref=actor,
            operation_id="recurring:profile-recheck:create",
            title="Raccolta",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=30,
            reminder_lead_minutes=None,
            activity_template={"version": 1},
        )
        state = await RecurrenceApplication(runtime.session_factory).get(
            owner="routine", self_person_ref=actor, owner_ref=routine.source_ref
        )
        assert state is not None
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="recurring:profile-recheck:first",
            start_date=day,
            end_date_exclusive=day + timedelta(days=1),
            effective_zone_id="Europe/Rome",
        )
        occurrences = await _read_checkpoint_refs(
            runtime,
            actor,
            routine.source_ref,
            owner="routine",
            operation="recurring:profile-recheck:first",
            start=day,
            end=day + timedelta(days=1),
        )
        assert len(occurrences) == 1
        occurrence = occurrences[0]
        async with runtime.session_factory() as session, session.begin():
            before = await session.scalar(
                text(
                    "SELECT activity_ref FROM "
                    "dante.list_self_routine_occurrence_activities("
                    ":actor, CAST(ARRAY[:occurrence] AS uuid[]))"
                ),
                {"actor": actor, "occurrence": occurrence},
            )
            assert before is not None
            await session.execute(
                text(
                    "SELECT * FROM dante.accept_self_occurrence_profile_edit("
                    ":actor,:occurrence,:operation,0,:state,'only_this',:zone,"
                    "CAST(:patch AS jsonb))"
                ),
                {
                    "actor": actor,
                    "occurrence": occurrence,
                    "operation": "recurring:profile-recheck:edit",
                    "state": state.material_state_ref,
                    "zone": "Europe/Rome",
                    "patch": '{"title":"Raccolta aggiornata"}',
                },
            )
        # A new window request rechecks the same already bound occurrence.
        # Create's immutable operation ID must not be replayed with the edited title.
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="recurring:profile-recheck:second",
            start_date=day,
            end_date_exclusive=day + timedelta(days=1),
            effective_zone_id="Europe/Rome",
        )
        async with runtime.session_factory() as session, session.begin():
            after = await session.scalar(
                text(
                    "SELECT activity_ref FROM "
                    "dante.list_self_routine_occurrence_activities("
                    ":actor, CAST(ARRAY[:occurrence] AS uuid[]))"
                ),
                {"actor": actor, "occurrence": occurrence},
            )
            patch = await session.scalar(
                text(
                    "SELECT dante.get_self_occurrence_profile_patch(:actor,:occurrence)"
                ),
                {"actor": actor, "occurrence": occurrence},
            )
        assert after == before
        assert patch == {"title": "Raccolta aggiornata"}
    finally:
        await runtime.dispose()
