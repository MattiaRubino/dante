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


def _attempt(
    *,
    send_state: EgressSendState,
    acceptance: EgressAcceptanceCertainty,
    exposure: ExposureState,
    outcome: EgressOutcomeState,
) -> EgressAttempt:
    return EgressAttempt(
        egress_attempt_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        recipient_binding="provider:test",
        purpose="ask_dante",
        consumer_context_id=uuid7(),
        projection_ref="projection:v1",
        policy_decision_id=uuid7(),
        send_state=send_state,
        acceptance_certainty=acceptance,
        exposure_state=exposure,
        outcome_state=outcome,
        created_at=datetime.now(UTC),
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
