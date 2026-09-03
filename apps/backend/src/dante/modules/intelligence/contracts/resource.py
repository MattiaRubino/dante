"""Request-local resource estimation, admission and settlement contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class ResourceUsageCertainty(StrEnum):
    """Whether one usage amount is known, estimated or genuinely unknown."""

    KNOWN = "known"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"


class ResourceAdmissionOutcome(StrEnum):
    """Request-local admission result; not commercial entitlement truth."""

    ADMITTED = "admitted"
    DENIED = "denied"


class ResourceSettlementStatus(StrEnum):
    """How completely request-local usage could be settled from available evidence."""

    SETTLED = "settled"
    PARTIAL = "partial"
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
class ResourceMeasure:
    """One typed resource quantity; UNKNOWN usage carries no fabricated numeric zero."""

    dimension: str
    unit: str
    certainty: ResourceUsageCertainty
    amount: int | None

    def __post_init__(self) -> None:
        _require_text(self.dimension, name="dimension")
        _require_text(self.unit, name="unit")
        if self.certainty is ResourceUsageCertainty.UNKNOWN:
            if self.amount is not None:
                raise ValueError("UNKNOWN resource usage must not carry a numeric amount")
            return
        if self.amount is None:
            raise ValueError("known/estimated resource usage requires an amount")
        if self.amount < 0:
            raise ValueError("resource amount must not be negative")


@dataclass(frozen=True, slots=True)
class ResourceEstimateRequest:
    """Request for a bounded pre-admission resource estimate."""

    request_id: UUID
    work_id: UUID
    work_revision: int
    route_candidate_ref: str
    requested_measures: tuple[ResourceMeasure, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        _require_uuid7(self.request_id, name="request_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.route_candidate_ref, name="route_candidate_ref")
        if not self.requested_measures:
            raise ValueError("requested_measures must not be empty")
        _require_aware(self.created_at, name="created_at")


@dataclass(frozen=True, slots=True)
class ResourceEstimate:
    """Immutable estimate evidence; never final cost or a reservation."""

    estimate_id: UUID
    request_id: UUID
    measures: tuple[ResourceMeasure, ...]
    basis_refs: tuple[str, ...]
    evaluated_at: datetime

    def __post_init__(self) -> None:
        _require_uuid7(self.estimate_id, name="estimate_id")
        _require_uuid7(self.request_id, name="request_id")
        if not self.measures:
            raise ValueError("estimate measures must not be empty")
        if any(measure.certainty is ResourceUsageCertainty.KNOWN for measure in self.measures):
            raise ValueError("pre-admission estimate must not claim KNOWN final usage")
        if not self.basis_refs:
            raise ValueError("ResourceEstimate requires basis_refs")
        _require_texts(self.basis_refs, name="basis_refs")
        _require_aware(self.evaluated_at, name="evaluated_at")


@dataclass(frozen=True, slots=True)
class ResourceAdmissionRequest:
    """Request-local admission request for one concrete route/attempt boundary."""

    request_id: UUID
    work_id: UUID
    work_revision: int
    estimate_id: UUID
    route_ref: str
    limit_refs: tuple[str, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("work_id", self.work_id),
            ("estimate_id", self.estimate_id),
        ):
            _require_uuid7(value, name=name)
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.route_ref, name="route_ref")
        _require_texts(self.limit_refs, name="limit_refs")
        _require_aware(self.created_at, name="created_at")


@dataclass(frozen=True, slots=True)
class ResourceAdmission:
    """Immutable request-local resource admission; not shared/commercial ledger state."""

    admission_id: UUID
    request_id: UUID
    outcome: ResourceAdmissionOutcome
    basis_refs: tuple[str, ...]
    evaluated_at: datetime
    admitted_limit_refs: tuple[str, ...] = ()
    internal_reason_code: str | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.admission_id, name="admission_id")
        _require_uuid7(self.request_id, name="request_id")
        if not self.basis_refs:
            raise ValueError("ResourceAdmission requires basis_refs")
        _require_texts(self.basis_refs, name="basis_refs")
        _require_texts(self.admitted_limit_refs, name="admitted_limit_refs")
        _require_aware(self.evaluated_at, name="evaluated_at")
        if self.internal_reason_code is not None:
            _require_text(self.internal_reason_code, name="internal_reason_code")
        if self.outcome is ResourceAdmissionOutcome.DENIED and self.admitted_limit_refs:
            raise ValueError("denied admission must not carry admitted limits")


@dataclass(frozen=True, slots=True)
class ResourceSettlementRequest:
    """Settlement request using actual/late/unknown usage evidence for one admission."""

    request_id: UUID
    admission_id: UUID
    observed_measures: tuple[ResourceMeasure, ...]
    usage_evidence_refs: tuple[str, ...]
    created_at: datetime

    def __post_init__(self) -> None:
        _require_uuid7(self.request_id, name="request_id")
        _require_uuid7(self.admission_id, name="admission_id")
        if not self.observed_measures:
            raise ValueError("observed_measures must not be empty")
        _require_texts(self.usage_evidence_refs, name="usage_evidence_refs")
        _require_aware(self.created_at, name="created_at")


@dataclass(frozen=True, slots=True)
class ResourceSettlement:
    """Request-local settlement evidence, deliberately separate from commercial accounting."""

    settlement_id: UUID
    request_id: UUID
    admission_id: UUID
    status: ResourceSettlementStatus
    measures: tuple[ResourceMeasure, ...]
    evidence_refs: tuple[str, ...]
    settled_at: datetime

    def __post_init__(self) -> None:
        for name, value in (
            ("settlement_id", self.settlement_id),
            ("request_id", self.request_id),
            ("admission_id", self.admission_id),
        ):
            _require_uuid7(value, name=name)
        if not self.measures:
            raise ValueError("settlement measures must not be empty")
        _require_texts(self.evidence_refs, name="evidence_refs")
        _require_aware(self.settled_at, name="settled_at")
        has_unknown = any(
            measure.certainty is ResourceUsageCertainty.UNKNOWN for measure in self.measures
        )
        if self.status is ResourceSettlementStatus.SETTLED and has_unknown:
            raise ValueError("SETTLED resource usage must not contain UNKNOWN measures")
        if self.status is ResourceSettlementStatus.UNKNOWN and not has_unknown:
            raise ValueError("UNKNOWN settlement requires at least one UNKNOWN measure")
