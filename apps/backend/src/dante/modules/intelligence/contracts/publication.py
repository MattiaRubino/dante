"""Safe-publication decision/result contracts for DANTE Intelligence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from dante.modules.intelligence.contracts.policy import PolicyBoundary, PolicyDecisionOutcome
from dante.modules.intelligence.contracts.verification import VerificationStatus
from dante.modules.intelligence.contracts.work import ResultMaturity


class PublicationDecisionStatus(StrEnum):
    """Decision for the exact final representation at the publication boundary."""

    PUBLISH = "publish"
    PUBLISH_WITH_LIMITATIONS = "publish_with_limitations"
    DENY = "deny"
    NEEDS_REREAD = "needs_reread"


class PublicationResultStatus(StrEnum):
    """Observed result of applying one PublicationDecision."""

    PUBLISHED = "published"
    WITHHELD = "withheld"


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
class PublicationDecision:
    """Immutable final publication gate after verification and current-state rechecks."""

    decision_id: UUID
    work_id: UUID
    work_revision: int
    representation_ref: str
    recipient: str
    surface: str
    status: PublicationDecisionStatus
    result_maturity: ResultMaturity
    verification_result_id: UUID
    verification_status: VerificationStatus
    basis_manifest_id: UUID
    policy_decision_id: UUID
    policy_boundary: PolicyBoundary
    policy_outcome: PolicyDecisionOutcome
    work_current: bool
    access_current: bool
    basis_current: bool
    emergency_denied: bool
    final_transform_rechecked: bool
    cumulative_disclosure_rechecked: bool
    evaluated_at: datetime
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for uuid_name, uuid_value in (
            ("decision_id", self.decision_id),
            ("work_id", self.work_id),
            ("verification_result_id", self.verification_result_id),
            ("basis_manifest_id", self.basis_manifest_id),
            ("policy_decision_id", self.policy_decision_id),
        ):
            _require_uuid7(uuid_value, name=uuid_name)
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        for text_name, text_value in (
            ("representation_ref", self.representation_ref),
            ("recipient", self.recipient),
            ("surface", self.surface),
        ):
            _require_text(text_value, name=text_name)
        _require_aware(self.evaluated_at, name="evaluated_at")
        _require_texts(self.limitations, name="limitations")
        if self.policy_boundary is not PolicyBoundary.PUBLICATION:
            raise ValueError("PublicationDecision requires PUBLICATION policy boundary")

        publishable = self.status in {
            PublicationDecisionStatus.PUBLISH,
            PublicationDecisionStatus.PUBLISH_WITH_LIMITATIONS,
        }
        if publishable:
            if self.policy_outcome is not PolicyDecisionOutcome.ALLOW:
                raise ValueError("publication requires an ALLOW policy decision")
            if self.result_maturity is not ResultMaturity.PUBLISHABLE:
                raise ValueError("publication requires PUBLISHABLE result maturity")
            if self.verification_status not in {
                VerificationStatus.VERIFIED,
                VerificationStatus.LIMITED,
            }:
                raise ValueError("publication requires VERIFIED or LIMITED verification")
            if not all(
                (
                    self.work_current,
                    self.access_current,
                    self.basis_current,
                    self.final_transform_rechecked,
                    self.cumulative_disclosure_rechecked,
                )
            ):
                raise ValueError("publication requires all currentness/disclosure rechecks")
            if self.emergency_denied:
                raise ValueError("emergency deny blocks publication")

        if self.status is PublicationDecisionStatus.PUBLISH:
            if self.verification_status is not VerificationStatus.VERIFIED:
                raise ValueError("unlimited publication requires VERIFIED status")
            if self.limitations:
                raise ValueError("PUBLISH must not carry limitations")
        if (
            self.status is PublicationDecisionStatus.PUBLISH_WITH_LIMITATIONS
            and not self.limitations
        ):
            raise ValueError("limited publication requires declared limitations")


@dataclass(frozen=True, slots=True)
class PublicationResult:
    """Recipient-facing publication occurrence without carrying response content itself."""

    result_id: UUID
    decision_id: UUID
    status: PublicationResultStatus
    representation_ref: str | None = None
    published_at: datetime | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.result_id, name="result_id")
        _require_uuid7(self.decision_id, name="decision_id")
        if self.status is PublicationResultStatus.PUBLISHED:
            if self.representation_ref is None or self.published_at is None:
                raise ValueError("PUBLISHED result requires representation_ref and published_at")
            _require_text(self.representation_ref, name="representation_ref")
            _require_aware(self.published_at, name="published_at")
            return
        if self.representation_ref is not None or self.published_at is not None:
            raise ValueError("WITHHELD result must not claim recipient externalization")
