"""Request-local egress exposure contracts for governed external data sends."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from dante.modules.intelligence.contracts.context import ExposureState


class EgressSendState(StrEnum):
    """What DANTE can establish about the outbound send boundary."""

    NOT_STARTED = "not_started"
    FAILED_BEFORE_SEND = "failed_before_send"
    DISPATCHED = "dispatched"
    CONFIRMED_SENT = "confirmed_sent"


class EgressAcceptanceCertainty(StrEnum):
    """Knowledge about external acceptance after a material send attempt."""

    NOT_APPLICABLE = "not_applicable"
    NOT_ACCEPTED = "not_accepted"
    POSSIBLE = "possible"
    ESTABLISHED = "established"


class EgressOutcomeState(StrEnum):
    """Normalized external outcome independent of exposure occurrence."""

    NOT_DISPATCHED = "not_dispatched"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    REFUSED = "refused"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_texts(values: tuple[str, ...], *, name: str) -> None:
    if any(not value or not value.strip() for value in values):
        raise ValueError(f"{name} entries must be non-empty")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


def _require_aware(value: datetime, *, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class EgressAttempt:
    """Immutable request-local exposure record for one material recipient attempt."""

    egress_attempt_id: UUID
    work_id: UUID
    work_revision: int
    recipient_binding: str
    purpose: str
    consumer_context_id: UUID
    projection_ref: str
    policy_decision_id: UUID
    send_state: EgressSendState
    acceptance_certainty: EgressAcceptanceCertainty
    exposure_state: ExposureState
    outcome_state: EgressOutcomeState
    created_at: datetime
    invocation_ref: str | None = None
    provider_attempt_ref: str | None = None
    prior_egress_attempt_refs: tuple[str, ...] = ()
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("egress_attempt_id", self.egress_attempt_id),
            ("work_id", self.work_id),
            ("consumer_context_id", self.consumer_context_id),
            ("policy_decision_id", self.policy_decision_id),
        ):
            _require_uuid7(value, name=name)
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.recipient_binding, name="recipient_binding")
        _require_text(self.purpose, name="purpose")
        _require_text(self.projection_ref, name="projection_ref")
        _require_texts(self.prior_egress_attempt_refs, name="prior_egress_attempt_refs")
        _require_aware(self.created_at, name="created_at")
        for name, value in (
            ("invocation_ref", self.invocation_ref),
            ("provider_attempt_ref", self.provider_attempt_ref),
        ):
            if value is not None:
                _require_text(value, name=name)
        if self.completed_at is not None:
            _require_aware(self.completed_at, name="completed_at")
            if self.completed_at < self.created_at:
                raise ValueError("completed_at must not precede created_at")

        pre_send = self.send_state in {
            EgressSendState.NOT_STARTED,
            EgressSendState.FAILED_BEFORE_SEND,
        }
        if pre_send:
            if self.exposure_state is not ExposureState.NOT_SENT:
                raise ValueError("pre-send egress state must have NOT_SENT exposure")
            if self.acceptance_certainty is not EgressAcceptanceCertainty.NOT_APPLICABLE:
                raise ValueError("pre-send egress state has no external acceptance")
            if self.outcome_state is not EgressOutcomeState.NOT_DISPATCHED:
                raise ValueError("pre-send egress state must be NOT_DISPATCHED")
            return

        if self.exposure_state is ExposureState.NOT_SENT:
            raise ValueError("dispatched egress cannot claim NOT_SENT exposure")
        if self.outcome_state is EgressOutcomeState.NOT_DISPATCHED:
            raise ValueError("dispatched egress cannot have NOT_DISPATCHED outcome")
        if self.acceptance_certainty is EgressAcceptanceCertainty.NOT_APPLICABLE:
            raise ValueError("dispatched egress requires external acceptance certainty")
        if self.send_state is EgressSendState.CONFIRMED_SENT:
            if self.exposure_state is not ExposureState.ESTABLISHED:
                raise ValueError("CONFIRMED_SENT requires ESTABLISHED exposure")
            if self.acceptance_certainty is not EgressAcceptanceCertainty.ESTABLISHED:
                raise ValueError("CONFIRMED_SENT requires ESTABLISHED acceptance")
