"""The edit read is bounded to one Activity and uses one database statement."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Response
from sqlalchemy import text

from dante.modules.temporal.activity_edit_snapshot_api import (
    ActivityCoreEditCommand,
    ActivityEditSnapshot,
    EditPolicyChange,
    EditProfileChange,
    _SNAPSHOT,
    revise_activity_core,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import FloatingLocalIntervalPlacement
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError
from tests.integration.temporal.test_b14_u2_authoring import _seed_self

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_activity_edit_snapshot_is_scoped_and_contains_current_settings(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        window = FloatingLocalIntervalPlacement(
            starts_local_at=datetime(2026, 10, 9, 9),
            ends_local_at=datetime(2026, 10, 9, 12),
        )
        planned = FloatingLocalIntervalPlacement(
            starts_local_at=datetime(2026, 10, 9, 10),
            ends_local_at=datetime(2026, 10, 9, 11),
        )
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="snapshot:created",
            title="Studio",
            description="Note",
            placement=window,
            planned_slices=(planned,),
            planned_slice_names=("Ripasso",),
        )
        activity = created.item.subject_native_ref
        async with runtime.session_factory() as session, session.begin():
            payload = await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity})
            assert payload is not None
            view = ActivityEditSnapshot.model_validate(payload)
            assert view.activity_ref == activity
            assert view.execution_policy.activity_ref == activity
            assert view.reality_policy.subject_native_ref == activity
            assert [schedule.role_code for schedule in view.schedules] == ["envelope", "planned"]
            assert view.schedules[1].display_name == "Ripasso"
            assert view.schedules[1].starts_local_at == planned.starts_local_at
            assert view.objectives == []
            assert view.placement_lock is not None
            assert view.placement_lock.schedule_ref == view.schedules[0].schedule_ref
            assert view.placement_lock.locked is False
            assert view.reminder is None
            assert await session.scalar(_SNAPSHOT, {"actor": other, "activity": activity}) is None
            assert await session.scalar(
                text("SELECT count(*) FROM dante.activity_intention WHERE activity_ref=:activity"),
                {"activity": activity},
            ) == 1
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_core_edit_rolls_back_policy_when_profile_revision_is_stale(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="core-edit:created", title="Prima",
        )
        activity = created.item.subject_native_ref
        context = SimpleNamespace(self_person_ref=actor)
        request = SimpleNamespace(app=SimpleNamespace(
            state=SimpleNamespace(database_runtime=runtime)))
        accepted = await revise_activity_core(
            activity, ActivityCoreEditCommand(
                operation_id="core-edit:accepted",
                capture=EditPolicyChange(mode_code="record", expected_state_ref=None),
                profile=EditProfileChange(expected_revision=0, title="Accettata"),
            ), context, request, Response(),
        )
        assert accepted.profile.title == "Accettata"
        assert accepted.profile.revision == 1
        assert accepted.capture.mode_code == "record"
        with pytest.raises(ProblemError) as failure:
            await revise_activity_core(
                activity, ActivityCoreEditCommand(
                    operation_id="core-edit:stale",
                    capture=EditPolicyChange(
                        mode_code="live", expected_state_ref=accepted.capture.state_ref,
                    ),
                    profile=EditProfileChange(expected_revision=9, title="Dopo"),
                ), context, request, Response(),
            )
        assert failure.value.status == 409
        async with runtime.session_factory() as session, session.begin():
            snapshot = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
            assert snapshot.execution_policy.mode_code == "record"
            assert snapshot.execution_policy.state_ref == accepted.capture.state_ref
    finally:
        await runtime.dispose()
