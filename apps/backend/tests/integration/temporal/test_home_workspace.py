"""B14: truthful Home finished-work and pending Objective lists, actor isolated."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast
from zoneinfo import ZoneInfo

import pytest
from fastapi import Request, Response
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.activity_replan_api import (
    ActivityReplanCommand,
    ReplanRow,
    RetainedPlannedRow,
    apply_activity_replan,
)
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.outcome_review_policy_api import (
    OutcomeReviewPolicyCommand,
    set_outcome_review_policy,
)
from dante.modules.temporal.reality_objective_api import (
    ObjectiveCreateCommand,
    create_activity_objective,
)
from dante.modules.temporal.resolution_queue_api import (
    list_home_finished_work,
    list_home_objective_work,
    list_resolution_queue,
)
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
)
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _fake_context(actor: object, zone_id: str = "Europe/Rome") -> DanteContext:
    """Only identity/zone attributes are accessed by these direct route calls."""
    return cast(
        DanteContext,
        SimpleNamespace(self_person_ref=actor, effective_zone_id=zone_id),
    )


def _fake_request(runtime: Any) -> Request:
    """Use a bounded ASGI app-state double rather than a running web server."""
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


@pytest.mark.asyncio
async def test_home_history_has_real_session_stop_but_no_inferred_activity_completion(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = _fake_request(runtime)
    context = _fake_context(actor)
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="home-workspace:create",
            title="Studio inglese",
            placement=AbsoluteIntervalPlacement(
                starts_at=now - timedelta(minutes=15),
                ends_at=now + timedelta(hours=1),
            ),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        assert await list_home_finished_work(request, context, Response()) == []
        sessions = SessionApplication(runtime.session_factory)
        started = await sessions.start(
            self_person_ref=actor,
            operation_id="home-workspace:start",
            subject_kind="activity",
            subject_native_ref=activity,
        )
        ended = await sessions.end(
            self_person_ref=actor,
            operation_id="home-workspace:end",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert not ended.open
        history = await list_home_finished_work(request, context, Response())
        assert len(history) == 1
        assert history[0].record_kind == "session_ended"
        assert history[0].title == "Studio inglese"
        assert history[0].subject_kind == "activity"
        assert await list_home_finished_work(request, _fake_context(stranger), Response()) == []

        objective = await create_activity_objective(
            activity,
            ObjectiveCreateCommand(
                operation_id="home-workspace:objective",
                label="15 vocaboli",
                result_kind="boolean",
                presentation_order=1,
            ),
            context,
            request,
            Response(),
        )
        pending = await list_home_objective_work(request, context, Response())
        assert len(pending) == 1
        assert pending[0].objective_ref == objective.objective_ref
        assert pending[0].subject_title == "Studio inglese"
        assert pending[0].draft_revision is None
        assert await list_home_objective_work(request, _fake_context(stranger), Response()) == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_past_unstarted_activity_requires_explicit_reality_review_and_shows_objectives(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = _fake_request(runtime)
    context = _fake_context(actor)
    now = datetime.now(UTC)
    try:
        activity = (
            await TemporalAuthoringApplication(runtime.session_factory).create_activity(
                self_person_ref=actor,
                operation_id="past-unstarted:create",
                title="Allenamento pianificato",
                placement=AbsoluteIntervalPlacement(
                    starts_at=now - timedelta(hours=3),
                    ends_at=now - timedelta(hours=2),
                ),
                session_capture_mode="record",
            )
        ).item.subject_native_ref
        await create_activity_objective(
            activity,
            ObjectiveCreateCommand(
                operation_id="past-unstarted:objective",
                label="Distanza",
                result_kind="boolean",
                presentation_order=1,
            ),
            context,
            request,
            Response(),
        )
        before = await list_resolution_queue(request, context)
        assert [item.reason_code for item in before.items] == ["objective_review"]
        await set_outcome_review_policy(
            activity,
            OutcomeReviewPolicyCommand(
                operation_id="past-unstarted:policy",
                mode_code="review_on_end",
            ),
            context,
            request,
            Response(),
        )
        after = await list_resolution_queue(request, context)
        assert after.count == 2
        review = next(item for item in after.items if item.reason_code == "realization_review")
        assert review.subject_ref == activity
        assert review.purpose_code == "activity.policy.past_unstarted"
        assert review.session_ref is None
        assert review.session_timing_material_state_ref is None
        automatic = (
            await TemporalAuthoringApplication(runtime.session_factory).create_activity(
                self_person_ref=actor,
                operation_id="past-unstarted:auto:create",
                title="Sessione automatica mai avviata",
                placement=AbsoluteIntervalPlacement(
                    starts_at=now - timedelta(hours=5),
                    ends_at=now - timedelta(hours=4),
                ),
                session_capture_mode="live",
            )
        ).item.subject_native_ref
        await set_outcome_review_policy(
            automatic,
            OutcomeReviewPolicyCommand(
                operation_id="past-unstarted:auto:policy",
                mode_code="auto_confirm_outcome",
            ),
            context,
            request,
            Response(),
        )
        auto_queue = await list_resolution_queue(request, context)
        assert auto_queue.count == 4
        assert any(
            item.subject_ref == automatic
            and item.reason_code == "session_unstarted"
            and item.planned_schedule_ref is None
            for item in auto_queue.items
        )
        assert any(
            item.subject_ref == automatic
            and item.reason_code == "realization_review"
            and item.session_ref is None
            for item in auto_queue.items
        )
        assert (
            await list_resolution_queue(
                request,
                _fake_context(stranger),
            )
        ).count == 0
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_unstarted_named_session_review_tracks_current_plan_and_real_attempts(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = _fake_request(runtime)
    context = _fake_context(actor)
    local_today = datetime.now(ZoneInfo("Europe/Rome")).date()
    past = datetime.combine(local_today - timedelta(days=2), datetime.min.time()).replace(hour=10)
    future = datetime.combine(local_today + timedelta(days=2), datetime.min.time()).replace(hour=10)

    async def snapshot(activity_ref: Any) -> ActivityEditSnapshot:
        async with runtime.session_factory() as session, session.begin():
            return ActivityEditSnapshot.model_validate(
                await session.scalar(_SNAPSHOT, {"actor": actor, "activity": activity_ref})
            )

    async def move(activity_ref: Any, start: datetime, operation: str) -> None:
        profile = await snapshot(activity_ref)
        envelope = next(row for row in profile.schedules if row.role_code == "envelope")
        planned = next(row for row in profile.schedules if row.role_code == "planned")
        assert envelope.placement_material_state_ref is not None
        await apply_activity_replan(
            activity_ref,
            ActivityReplanCommand(
                operation_id=operation,
                envelope=ReplanRow(
                    schedule_ref=envelope.schedule_ref,
                    expected_material_state_ref=envelope.placement_material_state_ref,
                    starts_local_at=start,
                    ends_local_at=start + timedelta(hours=1),
                ),
                planned_sessions=[
                    RetainedPlannedRow(
                        schedule_ref=planned.schedule_ref,
                        expected_material_state_ref=planned.placement_material_state_ref,
                    )
                ],
            ),
            context,
            request,
            Response(),
        )

    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="review-plan:create",
            title="Studio programmato",
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=past,
                ends_local_at=past + timedelta(hours=1),
                zone_id="Europe/Rome",
            ),
            planned_slices=(None,),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        initial = await list_resolution_queue(request, context)
        pending = [
            item
            for item in initial.items
            if item.subject_ref == activity and item.reason_code == "session_unstarted"
        ]
        assert len(pending) == 2
        assert {item.planned_schedule_ref for item in pending} == {
            None,
            next(
                row.schedule_ref
                for row in (await snapshot(activity)).schedules
                if row.role_code == "planned"
            ),
        }
        assert (await list_resolution_queue(request, _fake_context(stranger))).count == 0

        await move(activity, future, "review-plan:future-unstarted")
        assert not any(
            item.reason_code == "session_unstarted" and item.subject_ref == activity
            for item in (await list_resolution_queue(request, context)).items
        )
        await move(activity, past, "review-plan:past-unstarted")
        assert (
            sum(
                item.reason_code == "session_unstarted" and item.subject_ref == activity
                for item in (await list_resolution_queue(request, context)).items
            )
            == 2
        )

        sessions = SessionApplication(runtime.session_factory)
        started = await sessions.start(
            self_person_ref=actor,
            operation_id="review-plan:start-main",
            subject_kind="activity",
            subject_native_ref=activity,
        )
        await sessions.end(
            self_person_ref=actor,
            operation_id="review-plan:stop-main",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        remaining = [
            item
            for item in (await list_resolution_queue(request, context)).items
            if item.subject_ref == activity and item.reason_code == "session_unstarted"
        ]
        assert len(remaining) == 1
        assert remaining[0].planned_schedule_ref is not None

        with pytest.raises(ProblemError) as locked:
            await move(activity, future, "review-plan:future")
        assert locked.value.status == 409
        again = [
            item
            for item in (await list_resolution_queue(request, context)).items
            if item.subject_ref == activity and item.reason_code == "session_unstarted"
        ]
        assert len(again) == 1
        assert again[0].planned_schedule_ref == remaining[0].planned_schedule_ref
    finally:
        await runtime.dispose()
