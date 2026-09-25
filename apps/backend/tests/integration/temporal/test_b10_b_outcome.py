"""B10-B PostgreSQL proof for contextual Outcome authoring and current/history truth."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.outcome_runtime import (
    OutcomeApplication,
    OutcomeCurrentConflictError,
    OutcomeNotFoundError,
    OutcomeOperationReuseError,
)
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


@pytest.mark.asyncio
async def test_b10_b_outcome_is_contextual_append_only_idempotent_and_actual_is_unchanged(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    outcomes = OutcomeApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-b:area",
                name="Outcome proof",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b10-b:activity",
                title="Contextual result",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-b:actual",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
        )

        with pytest.raises(OutcomeNotFoundError):
            await outcomes.get_for_actual(
                self_person_ref=alice,
                actual_ref=actual.actual_ref,
                vocabulary_code="work.execution",
            )

        first = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:first",
            actual_ref=actual.actual_ref,
            vocabulary_code="work.execution",
            expected_material_state_ref=None,
            result_code="completed",
            note="Initial accepted result",
        )
        assert first.actual_ref == actual.actual_ref
        assert first.vocabulary_code == "work.execution"
        assert first.result_code == "completed"
        assert first.note == "Initial accepted result"
        assert not first.replayed

        replay = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:first",
            actual_ref=actual.actual_ref,
            vocabulary_code="work.execution",
            expected_material_state_ref=None,
            result_code="completed",
            note="Initial accepted result",
        )
        assert replay.replayed
        assert replay.outcome_ref == first.outcome_ref
        assert replay.material_state_ref == first.material_state_ref

        with pytest.raises(OutcomeOperationReuseError):
            await outcomes.record(
                self_person_ref=alice,
                operation_id="b10-b:outcome:first",
                actual_ref=actual.actual_ref,
                vocabulary_code="work.execution",
                expected_material_state_ref=first.material_state_ref,
                result_code="partial",
                note=None,
            )

        corrected = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:correct",
            actual_ref=actual.actual_ref,
            vocabulary_code="work.execution",
            expected_material_state_ref=first.material_state_ref,
            result_code="partial",
            note="Corrected result",
        )
        assert corrected.outcome_ref == first.outcome_ref
        assert corrected.material_state_ref != first.material_state_ref
        assert corrected.result_code == "partial"

        current = await outcomes.get_for_actual(
            self_person_ref=alice,
            actual_ref=actual.actual_ref,
            vocabulary_code="work.execution",
        )
        assert current.material_state_ref == corrected.material_state_ref
        assert current.result_code == "partial"

        history = await outcomes.history(
            self_person_ref=alice,
            outcome_ref=first.outcome_ref,
        )
        assert [item.material_state_ref for item in history] == [
            first.material_state_ref,
            corrected.material_state_ref,
        ]
        assert history[0].current_until_at is not None
        assert history[1].current_until_at is None

        with pytest.raises(OutcomeCurrentConflictError):
            await outcomes.record(
                self_person_ref=alice,
                operation_id="b10-b:outcome:stale",
                actual_ref=actual.actual_ref,
                vocabulary_code="work.execution",
                expected_material_state_ref=first.material_state_ref,
                result_code="completed",
                note=None,
            )

        with pytest.raises(OutcomeNotFoundError):
            await outcomes.get_for_actual(
                self_person_ref=bob,
                actual_ref=actual.actual_ref,
                vocabulary_code="work.execution",
            )

        other_vocabulary = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:quality",
            actual_ref=actual.actual_ref,
            vocabulary_code="work.quality",
            expected_material_state_ref=None,
            result_code="accepted",
            note=None,
        )
        assert other_vocabulary.outcome_ref != first.outcome_ref

        actual_after = await actuals.get_for_subject(
            self_person_ref=alice,
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert actual_after.material_state_ref == actual.material_state_ref
        assert actual_after.realization_occurred is True

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.outcome WHERE actual_ref=%s),
                  (SELECT count(*) FROM dante.outcome_result_state WHERE outcome_ref=%s),
                  (SELECT count(*) FROM dante.outcome_result_current_history WHERE outcome_ref=%s),
                  (SELECT material_state_ref
                     FROM dante.scoped_current_material_state
                    WHERE scoped_owner_ref=%s AND facet_code='outcome.result'),
                  (SELECT count(*) FROM dante.actual_realization_state WHERE actual_ref=%s)
                """,
                (
                    actual.actual_ref,
                    first.outcome_ref,
                    first.outcome_ref,
                    first.outcome_ref,
                    actual.actual_ref,
                ),
            ).fetchone()
        assert proof == (2, 2, 2, corrected.material_state_ref, 1)
    finally:
        await runtime.dispose()
