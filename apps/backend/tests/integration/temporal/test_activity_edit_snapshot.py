"""The edit read is bounded to one Activity and uses one database statement."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self
from tests.integration.temporal.test_schedule_create import _context

from dante.modules.temporal.activity_edit_snapshot_api import (
    _SNAPSHOT,
    ActivityCoreEditCommand,
    ActivityEditSnapshot,
    EditPolicyChange,
    EditProfileChange,
    EditReminderChange,
    revise_activity_core,
)
from dante.modules.temporal.activity_inspector_api import get_self_activity_session_impact
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
)
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _request(runtime: Any) -> Request:
    return Request(
        {
            "type": "http",
            "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
        }
    )


@pytest.mark.asyncio
async def test_delete_session_choice_rolls_back_with_stale_profile_then_commits_atomically(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="core-lifecycle:create",
            title="Prima",
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        started = await SessionApplication(runtime.session_factory).start(
            self_person_ref=actor,
            operation_id="core-lifecycle:start",
            subject_kind="activity",
            subject_native_ref=activity,
        )
        context = _context(actor)
        request = _request(runtime)
        impact = await get_self_activity_session_impact(activity, context, request, Response())
        with pytest.raises(ProblemError) as stale:
            await revise_activity_core(
                activity,
                ActivityCoreEditCommand(
                    operation_id="core-lifecycle:stale",
                    profile=EditProfileChange(expected_revision=9, title="Dopo"),
                    session_disposition="delete",
                    expected_session_fingerprint=impact.fingerprint,
                ),
                context,
                request,
                Response(),
            )
        assert stale.value.status == 409
        after_rollback = await get_self_activity_session_impact(
            activity, context, request, Response()
        )
        assert after_rollback.fingerprint == impact.fingerprint
        assert [row.session_ref for row in after_rollback.attempts] == [started.session_ref]
        changed = await revise_activity_core(
            activity,
            ActivityCoreEditCommand(
                operation_id="core-lifecycle:valid",
                profile=EditProfileChange(expected_revision=0, title="Dopo"),
                session_disposition="delete",
                expected_session_fingerprint=impact.fingerprint,
            ),
            context,
            request,
            Response(),
        )
        assert changed.profile.title == "Dopo"
        assert (
            await get_self_activity_session_impact(activity, context, request, Response())
        ).attempts == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_activity_edit_snapshot_is_scoped_and_contains_current_settings(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        # Floating-local Schedule values intentionally have no timezone offset.
        window = FloatingLocalIntervalPlacement(
            starts_local_at=datetime(2026, 10, 9, 9),  # noqa: DTZ001
            ends_local_at=datetime(2026, 10, 9, 12),  # noqa: DTZ001
        )
        planned = FloatingLocalIntervalPlacement(
            starts_local_at=datetime(2026, 10, 9, 10),  # noqa: DTZ001
            ends_local_at=datetime(2026, 10, 9, 11),  # noqa: DTZ001
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
            assert (
                await session.scalar(
                    text(
                        "SELECT count(*) FROM dante.activity_intention WHERE activity_ref=:activity"
                    ),
                    {"activity": activity},
                )
                == 1
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_reminder_and_profile_edit_commit_together_and_stale_profile_rolls_back(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="reminder-edit:create",
            title="Prima",
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=datetime(2026, 10, 9, 9),  # noqa: DTZ001
                ends_local_at=datetime(2026, 10, 9, 10),  # noqa: DTZ001
                zone_id="Europe/Rome",
            ),
        )
        activity = created.item.subject_native_ref
        context = _context(actor)
        request = _request(runtime)
        async with runtime.session_factory() as session, session.begin():
            before = ActivityEditSnapshot.model_validate(
                await session.scalar(
                    _SNAPSHOT,
                    {"actor": actor, "activity": activity},
                )
            )
        envelope = next(s for s in before.schedules if s.role_code == "envelope")
        first = await revise_activity_core(
            activity,
            ActivityCoreEditCommand(
                operation_id="reminder-edit:first",
                profile=EditProfileChange(expected_revision=0, title="Dopo"),
                reminder=EditReminderChange(
                    schedule_ref=envelope.schedule_ref,
                    enabled=True,
                    lead_minutes=15,
                ),
            ),
            context,
            request,
            Response(),
        )
        assert first.profile.revision == 1
        assert first.reminder is not None
        assert first.reminder.enabled is True
        assert first.reminder.lead_minutes == 15
        with pytest.raises(ProblemError) as failure:
            await revise_activity_core(
                activity,
                ActivityCoreEditCommand(
                    operation_id="reminder-edit:stale",
                    profile=EditProfileChange(expected_revision=0, title="Conflitto"),
                    reminder=EditReminderChange(
                        schedule_ref=envelope.schedule_ref,
                        expected_state_ref=first.reminder.material_state_ref,
                        enabled=False,
                        lead_minutes=0,
                    ),
                ),
                context,
                request,
                Response(),
            )
        assert failure.value.status == 409
        async with runtime.session_factory() as session, session.begin():
            after = ActivityEditSnapshot.model_validate(
                await session.scalar(
                    _SNAPSHOT,
                    {"actor": actor, "activity": activity},
                )
            )
        assert after.reminder is not None
        assert after.reminder.material_state_ref == first.reminder.material_state_ref
        assert after.reminder.enabled is True
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
            self_person_ref=actor,
            operation_id="core-edit:created",
            title="Prima",
        )
        activity = created.item.subject_native_ref
        context = _context(actor)
        request = _request(runtime)
        accepted = await revise_activity_core(
            activity,
            ActivityCoreEditCommand(
                operation_id="core-edit:accepted",
                capture=EditPolicyChange(mode_code="record", expected_state_ref=None),
                profile=EditProfileChange(expected_revision=0, title="Accettata"),
            ),
            context,
            request,
            Response(),
        )
        assert accepted.profile.title == "Accettata"
        assert accepted.profile.revision == 1
        assert accepted.capture.mode_code == "record"
        with pytest.raises(ProblemError) as failure:
            await revise_activity_core(
                activity,
                ActivityCoreEditCommand(
                    operation_id="core-edit:stale",
                    capture=EditPolicyChange(
                        mode_code="live",
                        expected_state_ref=accepted.capture.state_ref,
                    ),
                    profile=EditProfileChange(expected_revision=9, title="Dopo"),
                ),
                context,
                request,
                Response(),
            )
        assert failure.value.status == 409
        async with runtime.session_factory() as session, session.begin():
            snapshot = ActivityEditSnapshot.model_validate(
                await session.scalar(
                    _SNAPSHOT,
                    {"actor": actor, "activity": activity},
                )
            )
            assert snapshot.execution_policy.mode_code == "record"
            assert snapshot.execution_policy.state_ref == accepted.capture.state_ref
    finally:
        await runtime.dispose()
