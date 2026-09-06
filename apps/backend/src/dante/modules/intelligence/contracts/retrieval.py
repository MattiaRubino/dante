"""Governed Retrieval contracts for request-local DANTE Intelligence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import isfinite
from typing import Protocol
from uuid import UUID

from dante.modules.intelligence.contracts.context import (
    ContextFragment,
    InformationGuarantee,
    RealityScope,
    RuntimeInterpretationFrame,
    SourceCurrentness,
)
from dante.modules.intelligence.contracts.references import (
    ReferenceBindingRequirement,
    TargetRef,
)


class RetrievalMechanism(StrEnum):
    """Candidate-discovery mechanism; mechanism never establishes truth by itself."""

    STRUCTURED_EXACT = "structured_exact"
    MATERIAL_HISTORY = "material_history"
    RELATION_TRAVERSAL = "relation_traversal"
    LEXICAL = "lexical"
    FUZZY = "fuzzy"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"
    HIERARCHICAL_DOCUMENT = "hierarchical_document"
    DIRECT_LONG_CONTEXT = "direct_long_context"
    INTERACTION_RUN = "interaction_run"
    FEDERATED_PROVIDER = "federated_provider"
    OPEN_WORLD_JIT = "open_world_jit"


class SourceLifecycleHint(StrEnum):
    """Non-authoritative lifecycle hint carried by a retrieval candidate."""

    ACTIVE = "active"
    HISTORICAL = "historical"
    RETIRED = "retired"
    REDACTED = "redacted"
    UNKNOWN = "unknown"


class CandidateValidationStatus(StrEnum):
    """Validation outcome before candidate material may become Context."""

    ELIGIBLE_CURRENT = "eligible_current"
    ELIGIBLE_HISTORICAL = "eligible_historical"
    ELIGIBLE_WITH_LIMITATION = "eligible_with_limitation"
    STALE = "stale"
    CONFLICTED = "conflicted"
    SOURCE_RETIRED = "source_retired"
    SOURCE_REDACTED = "source_redacted"
    POLICY_BLOCKED = "policy_blocked"
    NOT_CURRENTLY_VISIBLE = "not_currently_visible"
    SOURCE_UNAVAILABLE = "source_unavailable"
    AMBIGUOUS_TARGET = "ambiguous_target"
    AMBIGUOUS_INTERPRETATION = "ambiguous_interpretation"
    INVALID_DERIVATIVE = "invalid_derivative"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_texts(values: tuple[str, ...], *, name: str) -> None:
    if any(not value or not value.strip() for value in values):
        raise ValueError(f"{name} entries must be non-empty")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


def _require_uuid7s(values: tuple[UUID, ...], *, name: str) -> None:
    for value in values:
        _require_uuid7(value, name=name)
    if len(values) != len(set(values)):
        raise ValueError(f"{name} must not contain duplicates")


def _require_aware(value: datetime, *, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class RetrievalPlan:
    """Bounded execution projection for accepted InformationNeeds."""

    plan_id: UUID
    work_id: UUID
    work_revision: int
    context_plan_id: UUID
    context_plan_revision: int
    information_need_ids: tuple[UUID, ...]
    strategy_ids: tuple[UUID, ...]
    purpose: str
    reality_scope: RealityScope
    reference_requirement: ReferenceBindingRequirement
    eligible_source_classes: tuple[str, ...]
    excluded_source_classes: tuple[str, ...]
    required_guarantee: InformationGuarantee
    freshness_requirement: str
    coherence_requirement: str
    fidelity_requirement: str
    permitted_transformations: tuple[str, ...]
    max_candidates: int
    max_refinements: int
    budget_units: int

    def __post_init__(self) -> None:
        for name, value in (
            ("plan_id", self.plan_id),
            ("work_id", self.work_id),
            ("context_plan_id", self.context_plan_id),
        ):
            _require_uuid7(value, name=name)
        if self.work_revision <= 0 or self.context_plan_revision <= 0:
            raise ValueError("work/context plan revisions must be positive")
        _require_uuid7s(self.information_need_ids, name="information_need_ids")
        _require_uuid7s(self.strategy_ids, name="strategy_ids")
        if not self.information_need_ids:
            raise ValueError("information_need_ids must not be empty")
        if not self.strategy_ids:
            raise ValueError("strategy_ids must not be empty")
        _require_text(self.purpose, name="purpose")
        _require_texts(self.eligible_source_classes, name="eligible_source_classes")
        _require_texts(self.excluded_source_classes, name="excluded_source_classes")
        _require_text(self.freshness_requirement, name="freshness_requirement")
        _require_text(self.coherence_requirement, name="coherence_requirement")
        _require_text(self.fidelity_requirement, name="fidelity_requirement")
        _require_texts(
            self.permitted_transformations,
            name="permitted_transformations",
        )
        if not self.eligible_source_classes:
            raise ValueError("eligible_source_classes must not be empty")
        if set(self.eligible_source_classes).intersection(self.excluded_source_classes):
            raise ValueError("source class cannot be both eligible and excluded")
        if self.max_candidates <= 0:
            raise ValueError("max_candidates must be positive")
        if self.max_refinements < 0:
            raise ValueError("max_refinements must not be negative")
        if self.budget_units < 0:
            raise ValueError("budget_units must not be negative")


@dataclass(frozen=True, slots=True)
class RetrievalCandidate:
    """Runtime discovery candidate; rank/score are retrieval evidence only."""

    candidate_id: UUID
    plan_id: UUID
    information_need_id: UUID
    source_binding: TargetRef
    source_class: str
    mechanism: RetrievalMechanism
    retrieved_at: datetime
    reality_scope: RealityScope
    currentness_hint: SourceCurrentness
    source_lifecycle_hint: SourceLifecycleHint
    purpose_scope: str
    lineage_refs: tuple[str, ...]
    cost_units: int
    rank: int | None = None
    score: float | None = None
    interpretation_frame: RuntimeInterpretationFrame | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.candidate_id, name="candidate_id")
        _require_uuid7(self.plan_id, name="plan_id")
        _require_uuid7(self.information_need_id, name="information_need_id")
        _require_text(self.source_class, name="source_class")
        _require_aware(self.retrieved_at, name="retrieved_at")
        _require_text(self.purpose_scope, name="purpose_scope")
        _require_texts(self.lineage_refs, name="lineage_refs")
        if self.cost_units < 0:
            raise ValueError("cost_units must not be negative")
        if self.rank is not None and self.rank <= 0:
            raise ValueError("rank must be positive when present")
        if self.score is not None and not isfinite(self.score):
            raise ValueError("score must be finite when present")


@dataclass(frozen=True, slots=True)
class RetrievalBatch:
    """One bounded candidate batch with an explicit achieved guarantee."""

    plan_id: UUID
    candidates: tuple[RetrievalCandidate, ...]
    achieved_guarantee: InformationGuarantee
    exhausted: bool
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.plan_id, name="plan_id")
        _require_texts(self.limitations, name="limitations")
        candidate_ids = tuple(candidate.candidate_id for candidate in self.candidates)
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidates must not contain duplicate candidate_id values")
        if any(candidate.plan_id != self.plan_id for candidate in self.candidates):
            raise ValueError("every candidate must belong to the RetrievalBatch plan")


@dataclass(frozen=True, slots=True)
class CandidateValidationResult:
    """Immutable validation result controlling promotion to ContextFragment."""

    candidate_id: UUID
    status: CandidateValidationStatus
    fragment: ContextFragment | None = None
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.candidate_id, name="candidate_id")
        _require_texts(self.limitations, name="limitations")
        eligible_statuses = {
            CandidateValidationStatus.ELIGIBLE_CURRENT,
            CandidateValidationStatus.ELIGIBLE_HISTORICAL,
            CandidateValidationStatus.ELIGIBLE_WITH_LIMITATION,
        }
        if self.status in eligible_statuses:
            if self.fragment is None:
                raise ValueError("eligible validation status requires ContextFragment")
            return
        if self.fragment is not None:
            raise ValueError("ineligible validation status must not carry ContextFragment")


class RetrievalGateway(Protocol):
    """Application-owned retrieval seam independent of provider/index technology."""

    async def retrieve(self, plan: RetrievalPlan) -> RetrievalBatch: ...

    async def validate(
        self,
        candidate: RetrievalCandidate,
    ) -> CandidateValidationResult: ...
