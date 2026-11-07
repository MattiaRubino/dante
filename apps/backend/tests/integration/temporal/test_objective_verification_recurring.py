"""Canonical Objective verification follows selected and future Routine Occurrences."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text
from tests.integration.temporal.test_objective_recurring_instance_scope import (
    ZONE,
    _apply,
    _objective_for_occurrence,
    _read_checkpoint_refs,
    _series_state,
)
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_profile_scoped_edit import _daily

from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import (
    RoutineOccurrencePolicyApplication,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


async def _mode(runtime: Any, owner: UUID, objective_ref: UUID) -> tuple[str, int] | None:
    async with runtime.session_factory() as session, session.begin():
        row = (
            await session.execute(
                text(
                    "SELECT * FROM dante.get_self_objective_verification("
                    ":actor,:objective)"
                ),
                {"actor": owner, "objective": objective_ref},
            )
        ).mappings().one_or_none()
        if row is None:
            return None
        return str(row["mode_code"]), int(row["verification_revision"])


@pytest.mark.asyncio
async def test_objective_verification_only_selected_and_following(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    today = datetime.now(ZoneInfo(ZONE)).date()
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policy = RoutineOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        created = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="objective-verify:routine",
            title="Allenamento",
            life_area_intent=None,
            recurrence=replace(
                _daily(today - timedelta(days=3)),
                clock_basis_code="named_zone",
                zone_id=ZONE,
                nonexistent_local_time_policy="skip_civil_candidate",
                ambiguous_local_time_policy="earlier",
            ),
        )
        await policy.set(
            self_person_ref=alice,
            routine_ref=created.source_ref,
            duration_minutes=45,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "objectives": [
                    {
                        "label": "Correre",
                        "result_kind": "boolean",
                        "presentation_order": 0,
                        "verification_mode": "none",
                    }
                ],
            },
        )
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="objective-verify:past",
            start_date=today - timedelta(days=3),
            end_date_exclusive=today - timedelta(days=1),
            effective_zone_id=ZONE,
        )
        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="objective-verify:future",
            start_date=today + timedelta(days=2),
            end_date_exclusive=today + timedelta(days=4),
            effective_zone_id=ZONE,
        )
        past = await _read_checkpoint_refs(
            runtime,
            alice,
            created.source_ref,
            owner="routine",
            operation="objective-verify:past",
            start=today - timedelta(days=3),
            end=today - timedelta(days=1),
        )
        future = await _read_checkpoint_refs(
            runtime,
            alice,
            created.source_ref,
            owner="routine",
            operation="objective-verify:future",
            start=today + timedelta(days=2),
            end=today + timedelta(days=4),
        )
        assert len(past) == len(future) == 2
        earlier, selected, *later = [
            await _objective_for_occurrence(runtime, alice, occurrence)
            for occurrence in (*past, *future)
        ]
        assert await _mode(runtime, alice, earlier) == ("none", 0)
        assert await _mode(runtime, alice, selected) == ("none", 0)
        assert await _mode(runtime, bob, selected) is None
        context = await _series_state(runtime, alice, selected)
        assert context is not None

        accepted = await _apply(
            runtime,
            alice,
            selected,
            operation="objective-verify:series",
            recurrence_state=context.recurrence_state_ref,
        )
        assert not accepted.replayed
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text(
                    "SELECT dante.apply_self_objective_verification_series("
                    ":actor,:objective,:operation,:mode)"
                ),
                {
                    "actor": alice,
                    "objective": selected,
                    "operation": "objective-verify:series",
                    "mode": "review_on_end",
                },
            )
        assert await _mode(runtime, alice, earlier) == ("none", 0)
        assert await _mode(runtime, alice, selected) == ("review_on_end", 0)
        for ref in later:
            assert await _mode(runtime, alice, ref) == ("review_on_end", 0)

        await materializer.checkpoint_window(
            self_person_ref=alice,
            operation_id="objective-verify:later",
            start_date=today + timedelta(days=4),
            end_date_exclusive=today + timedelta(days=5),
            effective_zone_id=ZONE,
        )
        (later_occurrence,) = await _read_checkpoint_refs(
            runtime,
            alice,
            created.source_ref,
            owner="routine",
            operation="objective-verify:later",
            start=today + timedelta(days=4),
            end=today + timedelta(days=5),
        )
        new_objective = await _objective_for_occurrence(
            runtime, alice, later_occurrence
        )
        assert await _mode(runtime, alice, new_objective) == ("review_on_end", 0)
    finally:
        await runtime.dispose()
