"""B14: truthful Home finished-work and pending Objective lists, actor isolated."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import Response
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

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
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_home_history_has_real_session_stop_but_no_inferred_activity_completion(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)))
    context = SimpleNamespace(self_person_ref=actor)
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="home-workspace:create",
            title="Studio inglese",
            placement=AbsoluteIntervalPlacement(
                starts_at=now-timedelta(minutes=15),
                ends_at=now+timedelta(hours=1),
            ),
            session_capture_mode="live",
        )
        activity = created.item.subject_native_ref
        assert await list_home_finished_work(request, context, Response()) == []
        sessions = SessionApplication(runtime.session_factory)
        started = await sessions.start(
            self_person_ref=actor, operation_id="home-workspace:start",
            subject_kind="activity", subject_native_ref=activity,
        )
        ended = await sessions.end(
            self_person_ref=actor, operation_id="home-workspace:end",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert not ended.open
        history = await list_home_finished_work(request, context, Response())
        assert len(history) == 1
        assert history[0].record_kind == "session_ended"
        assert history[0].title == "Studio inglese"
        assert history[0].subject_kind == "activity"
        assert await list_home_finished_work(
            request, SimpleNamespace(self_person_ref=stranger), Response()
        ) == []

        objective = await create_activity_objective(
            activity, ObjectiveCreateCommand(
                operation_id="home-workspace:objective", label="15 vocaboli",
                result_kind="boolean", presentation_order=1,
            ), context, request, Response(),
        )
        pending = await list_home_objective_work(request, context, Response())
        assert len(pending) == 1
        assert pending[0].objective_ref == objective.objective_ref
        assert pending[0].subject_title == "Studio inglese"
        assert pending[0].draft_revision is None
        assert await list_home_objective_work(
            request, SimpleNamespace(self_person_ref=stranger), Response()
        ) == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_past_unstarted_activity_requires_explicit_reality_review_and_shows_objectives(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)))
    context = SimpleNamespace(self_person_ref=actor, effective_zone_id="Europe/Rome")
    now = datetime.now(UTC)
    try:
        activity = (await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="past-unstarted:create",
            title="Allenamento pianificato",
            placement=AbsoluteIntervalPlacement(
                starts_at=now-timedelta(hours=3), ends_at=now-timedelta(hours=2),
            ),
            session_capture_mode="record",
        )).item.subject_native_ref
        await create_activity_objective(
            activity, ObjectiveCreateCommand(
                operation_id="past-unstarted:objective", label="Distanza",
                result_kind="boolean", presentation_order=1,
            ), context, request, Response(),
        )
        before = await list_resolution_queue(request, context)
        assert [item.reason_code for item in before.items] == ["objective_review"]
        await set_outcome_review_policy(
            activity, OutcomeReviewPolicyCommand(
                operation_id="past-unstarted:policy", mode_code="review_on_end",
            ), context, request, Response(),
        )
        after = await list_resolution_queue(request, context)
        assert after.count == 2
        review = next(item for item in after.items if item.reason_code == "realization_review")
        assert review.subject_ref == activity
        assert review.purpose_code == "activity.policy.past_unstarted"
        assert review.session_ref is None
        assert review.session_timing_material_state_ref is None
        automatic = (await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor, operation_id="past-unstarted:auto:create",
            title="Sessione automatica mai avviata",
            placement=AbsoluteIntervalPlacement(
                starts_at=now-timedelta(hours=5), ends_at=now-timedelta(hours=4),
            ),
            session_capture_mode="live",
        )).item.subject_native_ref
        await set_outcome_review_policy(
            automatic, OutcomeReviewPolicyCommand(
                operation_id="past-unstarted:auto:policy", mode_code="auto_confirm_outcome",
            ), context, request, Response(),
        )
        auto_queue = await list_resolution_queue(request, context)
        assert auto_queue.count == 3
        assert any(item.subject_ref == automatic and item.reason_code == "realization_review"
                   and item.session_ref is None for item in auto_queue.items)
        assert (await list_resolution_queue(
            request, SimpleNamespace(self_person_ref=stranger, effective_zone_id="Europe/Rome"),
        )).count == 0
    finally:
        await runtime.dispose()
