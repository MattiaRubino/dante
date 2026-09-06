"""Policy-consumer contracts for DANTE Intelligence enforcement boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class PolicyDecisionOutcome(StrEnum):
    """Result returned by an authoritative policy seam."""

    ALLOW = "allow"
    DENY = "deny"


class PolicyBoundary(StrEnum):
    """Material boundary at which current policy was evaluated."""

    CONTEXT_EXPOSURE = "context_exposure"
    MODEL_EGRESS = "model_egress"
    EFFECT = "effect"
    PUBLICATION = "publication"


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
class PolicyRequestContext:
    """Current authoritative access projection consumed by Intelligence, never owned by it."""

    work_id: UUID
    work_revision: int
    principal_binding: str
    recipient: str
    surface: str
    purpose: str
    authority_basis_refs: tuple[str, ...] = ()
    authz_basis_refs: tuple[str, ...] = ()
    visibility_basis_refs: tuple[str, ...] = ()
    consent_basis_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        for name, value in (
            ("principal_binding", self.principal_binding),
            ("recipient", self.recipient),
            ("surface", self.surface),
            ("purpose", self.purpose),
        ):
            _require_text(value, name=name)
        _require_texts(self.authority_basis_refs, name="authority_basis_refs")
        _require_texts(self.authz_basis_refs, name="authz_basis_refs")
        _require_texts(self.visibility_basis_refs, name="visibility_basis_refs")
        _require_texts(self.consent_basis_refs, name="consent_basis_refs")


@dataclass(frozen=True, slots=True)
class ContextExposurePolicyRequest:
    """Policy request for exposing minimized Context to one consumer."""

    context: PolicyRequestContext
    consumer_context_id: UUID
    sensitivity: str

    def __post_init__(self) -> None:
        _require_uuid7(self.consumer_context_id, name="consumer_context_id")
        _require_text(self.sensitivity, name="sensitivity")


@dataclass(frozen=True, slots=True)
class ModelEgressPolicyRequest:
    """Policy request evaluated immediately before material model/provider egress."""

    context: PolicyRequestContext
    consumer_context_id: UUID
    recipient_binding: str
    projection_ref: str
    prior_egress_attempt_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.consumer_context_id, name="consumer_context_id")
        _require_text(self.recipient_binding, name="recipient_binding")
        _require_text(self.projection_ref, name="projection_ref")
        _require_texts(self.prior_egress_attempt_refs, name="prior_egress_attempt_refs")


@dataclass(frozen=True, slots=True)
class EffectPolicyRequest:
    """Policy request for a bounded Effect proposal; C6 does not dispatch effects."""

    context: PolicyRequestContext
    effect_intent_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_texts(self.effect_intent_refs, name="effect_intent_refs")


@dataclass(frozen=True, slots=True)
class PublicationPolicyRequest:
    """Policy request for the exact final representation considered for publication."""

    context: PolicyRequestContext
    representation_ref: str
    verification_result_id: UUID
    basis_manifest_id: UUID
    egress_attempt_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.representation_ref, name="representation_ref")
        _require_uuid7(self.verification_result_id, name="verification_result_id")
        _require_uuid7(self.basis_manifest_id, name="basis_manifest_id")
        _require_texts(self.egress_attempt_refs, name="egress_attempt_refs")


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Immutable evidence returned by a policy owner; not Authority/AuthZ truth itself."""

    decision_id: UUID
    boundary: PolicyBoundary
    outcome: PolicyDecisionOutcome
    work_id: UUID
    work_revision: int
    principal_binding: str
    recipient: str
    surface: str
    purpose: str
    basis_refs: tuple[str, ...]
    revalidation_requirement: str
    internal_reason_code: str
    evaluated_at: datetime
    obligations: tuple[str, ...] = ()
    valid_until: datetime | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.decision_id, name="decision_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        for name, value in (
            ("principal_binding", self.principal_binding),
            ("recipient", self.recipient),
            ("surface", self.surface),
            ("purpose", self.purpose),
            ("revalidation_requirement", self.revalidation_requirement),
            ("internal_reason_code", self.internal_reason_code),
        ):
            _require_text(value, name=name)
        if not self.basis_refs:
            raise ValueError("PolicyDecision requires material basis_refs")
        _require_texts(self.basis_refs, name="basis_refs")
        _require_texts(self.obligations, name="obligations")
        _require_aware(self.evaluated_at, name="evaluated_at")
        if self.valid_until is not None:
            _require_aware(self.valid_until, name="valid_until")
            if self.valid_until < self.evaluated_at:
                raise ValueError("valid_until must not precede evaluated_at")
