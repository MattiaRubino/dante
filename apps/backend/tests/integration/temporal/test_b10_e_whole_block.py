"""B10-E whole-block proof across Session → Actual → Outcome → Confirmation → Reconciliation."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import (
    ActualApplication,
    ActualNotFoundError,
    ActualSessionBasis,
)
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.confirmation_runtime import ConfirmationApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.outcome_runtime import OutcomeApplication, OutcomeNotFoundError
from dante.modules.temporal.reconciliation_runtime import (
    ReconciliationApplication,
    ReconciliationEvidence,
    ReconciliationNotFoundError,
)
from dante.modules.temporal.session_runtime import SessionApplication
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
async def test_b10_e_chain_is_explicit_layered_and_history_preserving(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    outcomes = OutcomeApplication(runtime.session_factory)
    confirmations = ConfirmationApplication(runtime.session_factory)
    reconciliations = ReconciliationApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-e:area",
                name="Whole B10 proof",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b10-e:activity",
                title="Explicit realized truth chain",
                life_area_ref=area.life_area_ref,
            )
        ).activity

        # Session execution remains evidence only. Ending it must not fabricate Actual.
        started = await sessions.start(
            self_person_ref=alice,
            operation_id="b10-e:session:start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        ended = await sessions.end(
            self_person_ref=alice,
            operation_id="b10-e:session:end",
            session_ref=started.session_ref,
            expected_material_state_ref=started.timing_material_state_ref,
        )
        assert not ended.open
        with pytest.raises(ActualNotFoundError):
            await actuals.get_for_subject(
                self_person_ref=alice,
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
            )

        # Actual is explicit and may pin the exact Session timing state as evidence.
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-e:actual",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
            session_bases=(
                ActualSessionBasis(
                    session_ref=ended.session_ref,
                    session_timing_material_state_ref=ended.timing_material_state_ref,
                ),
            ),
        )
        assert actual.session_bases[0].session_timing_material_state_ref == (
            ended.timing_material_state_ref
        )

        # Actual does not fabricate Outcome.
        with pytest.raises(OutcomeNotFoundError):
            await outcomes.get_for_actual(
                self_person_ref=alice,
                actual_ref=actual.actual_ref,
            )

        outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-e:outcome",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=None,
            disposition_code="work.completed",
        )

        # Outcome does not fabricate Confirmation or Reconciliation.
        assert await confirmations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        ) == ()
        assert await reconciliations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        ) == ()

        alice_confirmation = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-e:confirmation:alice",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="attested",
        )
        bob_confirmation = await confirmations.record(
            self_person_ref=bob,
            operation_id="b10-e:confirmation:bob",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="disputed",
        )

        # Confirmation participation does not grant resolver authority and does not auto-resolve.
        assert await reconciliations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        ) == ()
        with pytest.raises(ReconciliationNotFoundError):
            await reconciliations.record(
                self_person_ref=bob,
                operation_id="b10-e:reconciliation:bob-forbidden",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=None,
                purpose_code="review.personal",
                action_code="unresolved",
                evidence=(),
            )

        first_reconciliation = await reconciliations.record(
            self_person_ref=alice,
            operation_id="b10-e:reconciliation:first",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            action_code="select",
            evidence=(
                ReconciliationEvidence(
                    confirmation_ref=alice_confirmation.confirmation_ref,
                    confirmation_attestation_material_state_ref=(
                        alice_confirmation.material_state_ref
                    ),
                    role_code="selected",
                ),
                ReconciliationEvidence(
                    confirmation_ref=bob_confirmation.confirmation_ref,
                    confirmation_attestation_material_state_ref=bob_confirmation.material_state_ref,
                    role_code="considered",
                ),
            ),
        )
        assert first_reconciliation.resolved_by_person_ref == alice
        assert first_reconciliation.action_code == "select"

        # Correcting Confirmation must not rewrite the exact evidence already reconciled.
        corrected_confirmation = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-e:confirmation:alice-correct",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=alice_confirmation.material_state_ref,
            purpose_code="review.personal",
            stance_code="retracted",
        )
        assert corrected_confirmation.material_state_ref != alice_confirmation.material_state_ref

        reconciliation_history = await reconciliations.history(
            self_person_ref=alice,
            reconciliation_ref=first_reconciliation.reconciliation_ref,
        )
        assert len(reconciliation_history) == 1
        pinned_evidence = {
            item.confirmation_attestation_material_state_ref
            for item in reconciliation_history[0].evidence
        }
        assert alice_confirmation.material_state_ref in pinned_evidence
        assert corrected_confirmation.material_state_ref not in pinned_evidence

        # Correcting Outcome creates a new reconciliation target; nothing transfers implicitly.
        corrected_outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-e:outcome:correct",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=outcome.material_state_ref,
            disposition_code="work.partial",
        )
        assert corrected_outcome.material_state_ref != outcome.material_state_ref

        confirmations_after_outcome_correction = await confirmations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        )
        assert confirmations_after_outcome_correction is not None
        assert all(
            item.outcome_disposition_material_state_ref == outcome.material_state_ref
            for item in confirmations_after_outcome_correction
        )

        reconciliations_after_outcome_correction = await reconciliations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        )
        assert len(reconciliations_after_outcome_correction) == 1
        assert (
            reconciliations_after_outcome_correction[0].outcome_disposition_material_state_ref
            == outcome.material_state_ref
        )

        new_target_reconciliation = await reconciliations.record(
            self_person_ref=alice,
            operation_id="b10-e:reconciliation:new-outcome-state",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=corrected_outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            action_code="unresolved",
            evidence=(),
        )
        assert new_target_reconciliation.reconciliation_ref != (
            first_reconciliation.reconciliation_ref
        )

        with _admin(migrated_database) as connection:
            counts = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.session WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.outcome WHERE actual_ref=%s),
                  (SELECT count(*) FROM dante.confirmation WHERE outcome_ref=%s),
                  (SELECT count(*) FROM dante.outcome_reconciliation WHERE outcome_ref=%s)
                """,
                (
                    activity.activity_ref,
                    activity.activity_ref,
                    actual.actual_ref,
                    outcome.outcome_ref,
                    outcome.outcome_ref,
                ),
            ).fetchone()
        assert counts == (1, 1, 1, 2, 2)
    finally:
        await runtime.dispose()
