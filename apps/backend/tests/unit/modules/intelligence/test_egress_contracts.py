"""Unit acceptance for request-local egress/exposure contracts."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.context import ExposureState
from dante.modules.intelligence.contracts.egress import (
    EgressAcceptanceCertainty,
    EgressAttempt,
    EgressOutcomeState,
    EgressSendState,
)
from dante.modules.intelligence.contracts.policy import PolicyBoundary, PolicyDecisionOutcome
from dante.modules.intelligence.contracts.resource import ResourceAdmissionOutcome


def _attempt(
    *,
    send_state: EgressSendState,
    acceptance: EgressAcceptanceCertainty,
    exposure: ExposureState,
    outcome: EgressOutcomeState,
    policy_boundary: PolicyBoundary = PolicyBoundary.MODEL_EGRESS,
    policy_outcome: PolicyDecisionOutcome = PolicyDecisionOutcome.ALLOW,
    resource_admission_outcome: ResourceAdmissionOutcome | None = (
        ResourceAdmissionOutcome.ADMITTED
    ),
) -> EgressAttempt:
    resource_admission_id = uuid7() if resource_admission_outcome is not None else None
    return EgressAttempt(
        egress_attempt_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        recipient_binding="provider:test",
        purpose="ask_dante",
        consumer_context_id=uuid7(),
        projection_ref="projection:v1",
        policy_decision_id=uuid7(),
        policy_boundary=policy_boundary,
        policy_outcome=policy_outcome,
        send_state=send_state,
        acceptance_certainty=acceptance,
        exposure_state=exposure,
        outcome_state=outcome,
        created_at=datetime.now(UTC),
        resource_admission_id=resource_admission_id,
        resource_admission_outcome=resource_admission_outcome,
    )


def test_timeout_after_dispatch_preserves_possible_exposure() -> None:
    attempt = _attempt(
        send_state=EgressSendState.DISPATCHED,
        acceptance=EgressAcceptanceCertainty.POSSIBLE,
        exposure=ExposureState.POSSIBLE,
        outcome=EgressOutcomeState.TIMED_OUT,
    )
    assert attempt.exposure_state is ExposureState.POSSIBLE
    assert attempt.outcome_state is EgressOutcomeState.TIMED_OUT


def test_pre_send_failure_cannot_claim_external_exposure() -> None:
    with pytest.raises(ValueError, match="NOT_SENT"):
        _attempt(
            send_state=EgressSendState.FAILED_BEFORE_SEND,
            acceptance=EgressAcceptanceCertainty.NOT_APPLICABLE,
            exposure=ExposureState.POSSIBLE,
            outcome=EgressOutcomeState.NOT_DISPATCHED,
        )


def test_confirmed_send_requires_established_exposure_and_acceptance() -> None:
    with pytest.raises(ValueError, match="ESTABLISHED exposure"):
        _attempt(
            send_state=EgressSendState.CONFIRMED_SENT,
            acceptance=EgressAcceptanceCertainty.ESTABLISHED,
            exposure=ExposureState.POSSIBLE,
            outcome=EgressOutcomeState.COMPLETED,
        )


def test_dispatched_egress_requires_model_egress_allow() -> None:
    with pytest.raises(ValueError, match="MODEL_EGRESS"):
        _attempt(
            send_state=EgressSendState.DISPATCHED,
            acceptance=EgressAcceptanceCertainty.POSSIBLE,
            exposure=ExposureState.POSSIBLE,
            outcome=EgressOutcomeState.UNKNOWN,
            policy_boundary=PolicyBoundary.PUBLICATION,
        )

    with pytest.raises(ValueError, match="ALLOW"):
        _attempt(
            send_state=EgressSendState.DISPATCHED,
            acceptance=EgressAcceptanceCertainty.POSSIBLE,
            exposure=ExposureState.POSSIBLE,
            outcome=EgressOutcomeState.UNKNOWN,
            policy_outcome=PolicyDecisionOutcome.DENY,
        )


def test_dispatched_egress_requires_admitted_resource_decision() -> None:
    with pytest.raises(ValueError, match="current ResourceAdmission"):
        _attempt(
            send_state=EgressSendState.DISPATCHED,
            acceptance=EgressAcceptanceCertainty.POSSIBLE,
            exposure=ExposureState.POSSIBLE,
            outcome=EgressOutcomeState.UNKNOWN,
            resource_admission_outcome=None,
        )

    with pytest.raises(ValueError, match="ADMITTED"):
        _attempt(
            send_state=EgressSendState.DISPATCHED,
            acceptance=EgressAcceptanceCertainty.POSSIBLE,
            exposure=ExposureState.POSSIBLE,
            outcome=EgressOutcomeState.UNKNOWN,
            resource_admission_outcome=ResourceAdmissionOutcome.DENIED,
        )
