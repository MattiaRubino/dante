"""B10-D PostgreSQL proof for owner-scoped reconciliation over exact Confirmation states."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.confirmation_runtime import ConfirmationApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.outcome_runtime import OutcomeApplication
from dante.modules.temporal.reconciliation_runtime import (
    ReconciliationApplication,
    ReconciliationCurrentConflictError,
    ReconciliationEvidence,
    ReconciliationInputError,
    ReconciliationNotFoundError,
    ReconciliationOperationReuseError,
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
async def test_b10_d_reconciliation_is_owner_scoped_versioned_and_evidence_pinned(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    outcomes = OutcomeApplication(runtime.session_factory)
    confirmations = ConfirmationApplication(runtime.session_factory)
    reconciliations = ReconciliationApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-d:area",
                name="Reconciliation proof",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b10-d:activity",
                title="Resolve contextual evidence",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-d:actual",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
        )
        outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-d:outcome",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=None,
            disposition_code="work.completed",
        )

        alice_confirmation = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-d:alice-confirmation",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="attested",
        )
        bob_confirmation = await confirmations.record(
            self_person_ref=bob,
            operation_id="b10-d:bob-confirmation",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="disputed",
        )

        assert await reconciliations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        ) == ()
        assert (
            await reconciliations.list_for_outcome(
                self_person_ref=bob,
                outcome_ref=outcome.outcome_ref,
            )
            is None
        )

        with pytest.raises(ReconciliationNotFoundError):
            await reconciliations.record(
                self_person_ref=bob,
                operation_id="b10-d:bob-cannot-resolve",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=None,
                purpose_code="review.personal",
                action_code="unresolved",
                evidence=(),
            )

        alice_evidence = ReconciliationEvidence(
            confirmation_ref=alice_confirmation.confirmation_ref,
            confirmation_attestation_material_state_ref=alice_confirmation.material_state_ref,
            role_code="selected",
        )
        bob_considered = ReconciliationEvidence(
            confirmation_ref=bob_confirmation.confirmation_ref,
            confirmation_attestation_material_state_ref=bob_confirmation.material_state_ref,
            role_code="considered",
        )
        first = await reconciliations.record(
            self_person_ref=alice,
            operation_id="b10-d:first",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            action_code="select",
            evidence=(bob_considered, alice_evidence),
        )
        assert first.outcome_ref == outcome.outcome_ref
        assert first.outcome_disposition_material_state_ref == outcome.material_state_ref
        assert first.resolved_by_person_ref == alice
        assert first.action_code == "select"
        assert [item.role_code for item in first.evidence] == ["selected", "considered"]
        assert not first.replayed

        replay = await reconciliations.record(
            self_person_ref=alice,
            operation_id="b10-d:first",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            action_code="select",
            evidence=(alice_evidence, bob_considered),
        )
        assert replay.replayed
        assert replay.reconciliation_ref == first.reconciliation_ref
        assert replay.material_state_ref == first.material_state_ref

        with pytest.raises(ReconciliationOperationReuseError):
            await reconciliations.record(
                self_person_ref=alice,
                operation_id="b10-d:first",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=first.material_state_ref,
                purpose_code="review.personal",
                action_code="unresolved",
                evidence=(),
            )

        bob_selected = ReconciliationEvidence(
            confirmation_ref=bob_confirmation.confirmation_ref,
            confirmation_attestation_material_state_ref=bob_confirmation.material_state_ref,
            role_code="selected",
        )
        corrected = await reconciliations.record(
            self_person_ref=alice,
            operation_id="b10-d:correct",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=first.material_state_ref,
            purpose_code="review.personal",
            action_code="accept_multiple",
            evidence=(alice_evidence, bob_selected),
        )
        assert corrected.reconciliation_ref == first.reconciliation_ref
        assert corrected.material_state_ref != first.material_state_ref
        assert corrected.action_code == "accept_multiple"
        assert {item.role_code for item in corrected.evidence} == {"selected"}

        with pytest.raises(ReconciliationCurrentConflictError):
            await reconciliations.record(
                self_person_ref=alice,
                operation_id="b10-d:stale",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=first.material_state_ref,
                purpose_code="review.personal",
                action_code="unresolved",
                evidence=(),
            )

        history = await reconciliations.history(
            self_person_ref=alice,
            reconciliation_ref=first.reconciliation_ref,
        )
        assert [item.material_state_ref for item in history] == [
            first.material_state_ref,
            corrected.material_state_ref,
        ]
        assert history[0].current_until_at is not None
        assert history[1].current_until_at is None
        with pytest.raises(ReconciliationNotFoundError):
            await reconciliations.history(
                self_person_ref=bob,
                reconciliation_ref=first.reconciliation_ref,
            )

        corrected_alice_confirmation = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-d:alice-confirmation-correct",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=alice_confirmation.material_state_ref,
            purpose_code="review.personal",
            stance_code="retracted",
        )
        pinned_history = await reconciliations.history(
            self_person_ref=alice,
            reconciliation_ref=first.reconciliation_ref,
        )
        assert pinned_history[0].evidence[0].confirmation_attestation_material_state_ref == (
            alice_confirmation.material_state_ref
        )
        assert corrected_alice_confirmation.material_state_ref != alice_confirmation.material_state_ref

        with pytest.raises(ReconciliationInputError):
            await reconciliations.record(
                self_person_ref=alice,
                operation_id="b10-d:bad-select",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=corrected.material_state_ref,
                purpose_code="review.personal",
                action_code="select",
                evidence=(bob_considered,),
            )
        with pytest.raises(ReconciliationInputError):
            await reconciliations.record(
                self_person_ref=alice,
                operation_id="b10-d:bad-multiple",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=corrected.material_state_ref,
                purpose_code="review.personal",
                action_code="accept_multiple",
                evidence=(bob_selected,),
            )

        corrected_outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-d:outcome-correct",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=outcome.material_state_ref,
            disposition_code="work.partial",
        )
        on_new_outcome_state = await reconciliations.record(
            self_person_ref=alice,
            operation_id="b10-d:new-outcome-state",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=corrected_outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            action_code="unresolved",
            evidence=(),
        )
        assert on_new_outcome_state.reconciliation_ref != first.reconciliation_ref
        assert on_new_outcome_state.outcome_disposition_material_state_ref == (
            corrected_outcome.material_state_ref
        )

        with pytest.raises(ReconciliationInputError):
            await reconciliations.record(
                self_person_ref=alice,
                operation_id="b10-d:wrong-target-evidence",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=corrected_outcome.material_state_ref,
                expected_material_state_ref=on_new_outcome_state.material_state_ref,
                purpose_code="review.personal",
                action_code="select",
                evidence=(alice_evidence,),
            )

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.outcome_reconciliation
                    WHERE outcome_ref=%s),
                  (SELECT count(*) FROM dante.outcome_reconciliation_state
                    WHERE reconciliation_ref=%s),
                  (SELECT count(*) FROM dante.outcome_reconciliation_evidence
                    WHERE reconciliation_ref=%s),
                  (SELECT material_state_ref
                     FROM dante.scoped_current_material_state
                    WHERE scoped_owner_ref=%s AND facet_code='outcome.reconciliation')
                """,
                (
                    outcome.outcome_ref,
                    first.reconciliation_ref,
                    first.reconciliation_ref,
                    first.reconciliation_ref,
                ),
            ).fetchone()
        assert proof == (2, 2, 4, corrected.material_state_ref)
    finally:
        await runtime.dispose()
