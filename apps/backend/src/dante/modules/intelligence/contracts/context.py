"""Full request-local Context contracts accepted by DANTE AI-03A/03C."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID

from dante.modules.intelligence.contracts.references import (
    ReferenceBindingRequirement,
    TargetRef,
)


class RealityScopeKind(StrEnum):
    """Reality frame carried by context and source material."""

    CANONICAL_CURRENT = "canonical_current"
    MATERIAL_HISTORICAL = "material_historical"
    SCENARIO = "scenario"
    OPEN_WORLD_ASSERTION = "open_world_assertion"
    MIXED = "mixed"


class InformationNeedOrigin(StrEnum):
    """Accepted origin of an explicit InformationNeed."""

    USER_EXPLICIT = "user_explicit"
    WORK_CONTRACT = "work_contract"
    POLICY_REQUIRED = "policy_required"
    CAPABILITY_REQUIRED = "capability_required"
    MODEL_DISCOVERED = "model_discovered"
    SOLVER_REQUIRED = "solver_required"
    VERIFIER_REQUIRED = "verifier_required"


class NeedCriticality(StrEnum):
    """How strongly one InformationNeed gates legitimate work."""

    REQUIRED = "required"
    USEFUL = "useful"
    OPTIONAL = "optional"


class CoverageRequirement(StrEnum):
    """Coverage required by an InformationNeed."""

    COMPLETE_REQUIRED = "complete_required"
    BOUNDED_COMPLETE = "bounded_complete"
    BEST_EFFORT = "best_effort"
    SAMPLE_ACCEPTABLE = "sample_acceptable"


class InformationGuarantee(StrEnum):
    """Truthful acquisition/result guarantee independent of result count."""

    EXACT = "exact"
    BOUNDED_COMPLETE = "bounded_complete"
    BEST_EFFORT = "best_effort"
    APPROXIMATE = "approximate"
    SAMPLED = "sampled"


class InformationNeedStatus(StrEnum):
    """Detailed readiness status for one InformationNeed."""

    SATISFIED = "satisfied"
    PARTIAL = "partial"
    MISSING = "missing"
    CONFLICTED = "conflicted"
    STALE = "stale"
    POLICY_BLOCKED = "policy_blocked"
    SOURCE_UNAVAILABLE = "source_unavailable"
    SOURCE_RETIRED = "source_retired"
    AMBIGUOUS_TARGET = "ambiguous_target"
    AMBIGUOUS_INTERPRETATION = "ambiguous_interpretation"


class ContextStrategyKind(StrEnum):
    """Accepted strategy families; availability remains integration-gated."""

    STRUCTURED_CURRENT_QUERY = "structured_current_query"
    MATERIAL_HISTORY_QUERY = "material_history_query"
    RELATION_TRAVERSAL = "relation_traversal"
    DERIVED_PROJECTION = "derived_projection"
    DETERMINISTIC_AGGREGATION = "deterministic_aggregation"
    SEARCH_DISCOVERY = "search_discovery"
    DIRECT_SOURCE_READ = "direct_source_read"
    LEXICAL_FUZZY = "lexical_fuzzy"
    SEMANTIC_HYBRID = "semantic_hybrid"
    DIRECT_LONG_CONTEXT = "direct_long_context"
    INTERACTION_RUN_CONTEXT = "interaction_run_context"
    SCENARIO_CONTEXT = "scenario_context"
    OPEN_WORLD_JIT = "open_world_jit"


class ContextReadinessState(StrEnum):
    """Final implementation-facing Context readiness classification."""

    READY = "ready"
    PARTIAL_WITH_DECLARED_LIMITATION = "partial_with_declared_limitation"
    NEEDS_ACQUISITION = "needs_acquisition"
    NEEDS_CLARIFICATION = "needs_clarification"
    CONFLICTED = "conflicted"
    STALE = "stale"
    POLICY_BLOCKED = "policy_blocked"
    INSUFFICIENT = "insufficient"


class ContextExclusionKind(StrEnum):
    """Negative ContextPlan requirements that relevance may not override."""

    SOURCE = "source"
    DATA_CLASS = "data_class"
    PURPOSE = "purpose"
    PROVIDER_EXPOSURE = "provider_exposure"
    DERIVATION_USE = "derivation_use"


class InstructionProvenance(StrEnum):
    """Instruction provenance kept distinct from source-content relevance."""

    DATA = "data"
    SOURCE_CONTENT = "source_content"
    CURRENT_USER_INSTRUCTION = "current_user_instruction"
    TRUSTED_SYSTEM_INSTRUCTION = "trusted_system_instruction"
    TOOL_OUTPUT = "tool_output"


class SourceRealityClass(StrEnum):
    """Runtime source class; none of these creates canonical ownership."""

    CANONICAL_CURRENT = "canonical_current"
    MATERIAL_HISTORICAL = "material_historical"
    DERIVED_PROJECTION = "derived_projection"
    EXTERNAL_PROVIDER = "external_provider"
    UNRESOLVED_CANDIDATE = "unresolved_candidate"
    INTERACTION_SESSION = "interaction_session"
    RUN_WORKING = "run_working"
    SCENARIO = "scenario"
    ARTIFACT_REPRESENTATION = "artifact_representation"
    OPEN_WORLD = "open_world"


class ReferenceBindingState(StrEnum):
    """Reference certainty carried by Context material."""

    EXACT = "exact"
    UNIQUE_IN_SCOPE = "unique_in_scope"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"


class SourceCurrentness(StrEnum):
    """Truthful currentness classification for runtime source material."""

    CURRENT = "current"
    HISTORICAL = "historical"
    STALE = "stale"
    UNKNOWN = "unknown"


class ExposureState(StrEnum):
    """What DANTE can establish about material consumer exposure."""

    NOT_SENT = "not_sent"
    POSSIBLE = "possible"
    ESTABLISHED = "established"


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
class RealityScope:
    """Explicit reality frame; current, history, scenario and open-world never collapse."""

    kind: RealityScopeKind
    as_of: datetime | None = None
    scenario_ref: str | None = None

    def __post_init__(self) -> None:
        if self.as_of is not None:
            _require_aware(self.as_of, name="as_of")
        if self.scenario_ref is not None:
            _require_text(self.scenario_ref, name="scenario_ref")

        if self.kind is RealityScopeKind.CANONICAL_CURRENT:
            if self.as_of is not None or self.scenario_ref is not None:
                raise ValueError("CANONICAL_CURRENT must not carry as_of/scenario_ref")
        elif self.kind is RealityScopeKind.MATERIAL_HISTORICAL:
            if self.as_of is None or self.scenario_ref is not None:
                raise ValueError("MATERIAL_HISTORICAL requires only an as_of instant")
        elif self.kind is RealityScopeKind.SCENARIO and self.scenario_ref is None:
            raise ValueError("SCENARIO requires scenario_ref")


@dataclass(frozen=True, slots=True)
class RuntimeInterpretationFrame:
    """Runtime temporal/spatial/locale frame used when meaning depends on it."""

    reference_instant: datetime
    timezone: str
    locale: str
    calendar: str | None = None
    day_boundary: str | None = None
    dst_resolution: str | None = None
    units_system: str | None = None
    spatial_anchor: str | None = None

    def __post_init__(self) -> None:
        _require_aware(self.reference_instant, name="reference_instant")
        _require_text(self.timezone, name="timezone")
        _require_text(self.locale, name="locale")
        for name, value in (
            ("calendar", self.calendar),
            ("day_boundary", self.day_boundary),
            ("dst_resolution", self.dst_resolution),
            ("units_system", self.units_system),
            ("spatial_anchor", self.spatial_anchor),
        ):
            if value is not None:
                _require_text(value, name=name)


@dataclass(frozen=True, slots=True)
class ContextExclusion:
    """Explicit negative context/acquisition requirement."""

    kind: ContextExclusionKind
    value: str
    basis_ref: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.value, name="exclusion value")
        if self.basis_ref is not None:
            _require_text(self.basis_ref, name="basis_ref")


@dataclass(frozen=True, slots=True)
class ContextResourceConstraints:
    """Bounded request-local acquisition/context packing limits."""

    max_fragments: int
    max_bytes: int
    max_estimated_tokens: int
    max_refinements: int

    def __post_init__(self) -> None:
        if self.max_fragments <= 0:
            raise ValueError("max_fragments must be positive")
        if self.max_bytes <= 0:
            raise ValueError("max_bytes must be positive")
        if self.max_estimated_tokens <= 0:
            raise ValueError("max_estimated_tokens must be positive")
        if self.max_refinements < 0:
            raise ValueError("max_refinements must not be negative")


@dataclass(frozen=True, slots=True)
class InformationNeed:
    """One explicit requirement used to evaluate context sufficiency."""

    need_id: UUID
    revision: int
    requirement: str
    origin: InformationNeedOrigin
    purpose: str
    reality_scope: RealityScope
    reference_requirement: ReferenceBindingRequirement
    criticality: NeedCriticality
    coverage_requirement: CoverageRequirement
    acceptable_source_semantics: tuple[str, ...]
    freshness_requirement: str
    coherence_requirement: str
    fidelity_requirement: str
    status: InformationNeedStatus
    target_bindings: tuple[TargetRef, ...] = ()
    subject_bindings: tuple[str, ...] = ()
    temporal_scope_ref: str | None = None
    interpretation_frame: RuntimeInterpretationFrame | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.need_id, name="need_id")
        if self.revision <= 0:
            raise ValueError("revision must be positive")
        _require_text(self.requirement, name="requirement")
        _require_text(self.purpose, name="purpose")
        _require_texts(
            self.acceptable_source_semantics,
            name="acceptable_source_semantics",
        )
        _require_text(self.freshness_requirement, name="freshness_requirement")
        _require_text(self.coherence_requirement, name="coherence_requirement")
        _require_text(self.fidelity_requirement, name="fidelity_requirement")
        _require_texts(self.subject_bindings, name="subject_bindings")
        if not self.acceptable_source_semantics:
            raise ValueError("acceptable_source_semantics must not be empty")
        if len(self.target_bindings) != len(set(self.target_bindings)):
            raise ValueError("target_bindings must not contain duplicates")
        if self.temporal_scope_ref is not None:
            _require_text(self.temporal_scope_ref, name="temporal_scope_ref")


@dataclass(frozen=True, slots=True)
class ContextPlan:
    """Bounded plan constraining the complete acquisition/exposure cycle."""

    plan_id: UUID
    revision: int
    work_id: UUID
    work_revision: int
    objective: str
    purpose: str
    principal_binding: str
    reality_scope: RealityScope
    privacy_compartment: str
    resource_constraints: ContextResourceConstraints
    information_need_ids: tuple[UUID, ...]
    known_targets: tuple[TargetRef, ...] = ()
    unresolved_reference_need_ids: tuple[UUID, ...] = ()
    protected_need_ids: tuple[UUID, ...] = ()
    exclusions: tuple[ContextExclusion, ...] = ()
    actor_binding: str | None = None
    represented_party_binding: str | None = None
    interpretation_frame: RuntimeInterpretationFrame | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.plan_id, name="plan_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.revision <= 0 or self.work_revision <= 0:
            raise ValueError("plan/work revisions must be positive")
        _require_text(self.objective, name="objective")
        _require_text(self.purpose, name="purpose")
        _require_text(self.principal_binding, name="principal_binding")
        _require_text(self.privacy_compartment, name="privacy_compartment")
        _require_uuid7s(self.information_need_ids, name="information_need_ids")
        _require_uuid7s(
            self.unresolved_reference_need_ids,
            name="unresolved_reference_need_ids",
        )
        _require_uuid7s(self.protected_need_ids, name="protected_need_ids")
        if not self.information_need_ids:
            raise ValueError("information_need_ids must not be empty")
        known_need_ids = set(self.information_need_ids)
        if not set(self.unresolved_reference_need_ids).issubset(known_need_ids):
            raise ValueError("unresolved reference needs must belong to the plan")
        if not set(self.protected_need_ids).issubset(known_need_ids):
            raise ValueError("protected needs must belong to the plan")
        if len(self.known_targets) != len(set(self.known_targets)):
            raise ValueError("known_targets must not contain duplicates")
        if self.actor_binding is not None:
            _require_text(self.actor_binding, name="actor_binding")
        if self.represented_party_binding is not None:
            _require_text(
                self.represented_party_binding,
                name="represented_party_binding",
            )


@dataclass(frozen=True, slots=True)
class ContextStrategy:
    """One bounded acquisition strategy for one InformationNeed."""

    strategy_id: UUID
    need_id: UUID
    kind: ContextStrategyKind
    purpose: str
    reality_scope: RealityScope
    required_guarantee: InformationGuarantee
    source_classes: tuple[str, ...]
    permitted_transformations: tuple[str, ...]
    exclusions: tuple[ContextExclusion, ...]
    max_refinements: int

    def __post_init__(self) -> None:
        _require_uuid7(self.strategy_id, name="strategy_id")
        _require_uuid7(self.need_id, name="need_id")
        _require_text(self.purpose, name="purpose")
        _require_texts(self.source_classes, name="source_classes")
        _require_texts(
            self.permitted_transformations,
            name="permitted_transformations",
        )
        if not self.source_classes:
            raise ValueError("source_classes must not be empty")
        if self.max_refinements < 0:
            raise ValueError("max_refinements must not be negative")


type ContextScalar = str | int | float | bool | UUID | datetime


@dataclass(frozen=True, slots=True)
class TextContextRepresentation:
    """Text representation without promoting text to canonical truth."""

    text: str
    kind: Literal["text"] = "text"

    def __post_init__(self) -> None:
        _require_text(self.text, name="text")


@dataclass(frozen=True, slots=True)
class ContextField:
    """One typed scalar field in a structured Context representation."""

    name: str
    value: ContextScalar

    def __post_init__(self) -> None:
        _require_text(self.name, name="field name")
        if isinstance(self.value, str):
            _require_text(self.value, name="field value")
        elif isinstance(self.value, datetime):
            _require_aware(self.value, name="field datetime")


@dataclass(frozen=True, slots=True)
class RecordContextRepresentation:
    """Structured record projection without a generic JSON semantic escape hatch."""

    fields: tuple[ContextField, ...]
    kind: Literal["record"] = "record"

    def __post_init__(self) -> None:
        if not self.fields:
            raise ValueError("record fields must not be empty")
        names = tuple(field.name for field in self.fields)
        if len(names) != len(set(names)):
            raise ValueError("record fields must not contain duplicate names")


@dataclass(frozen=True, slots=True)
class AggregateContextRepresentation:
    """Typed deterministic aggregate representation."""

    metric: str
    value: ContextScalar
    unit: str | None = None
    kind: Literal["aggregate"] = "aggregate"

    def __post_init__(self) -> None:
        _require_text(self.metric, name="metric")
        if isinstance(self.value, str):
            _require_text(self.value, name="aggregate value")
        elif isinstance(self.value, datetime):
            _require_aware(self.value, name="aggregate datetime")
        if self.unit is not None:
            _require_text(self.unit, name="unit")


type ContextRepresentation = (
    TextContextRepresentation | RecordContextRepresentation | AggregateContextRepresentation
)


@dataclass(frozen=True, slots=True)
class ContextFragment:
    """Validated runtime source-linked material eligible for Context construction."""

    fragment_id: UUID
    need_ids: tuple[UUID, ...]
    source_binding: TargetRef
    source_class: SourceRealityClass
    reality_scope: RealityScope
    reference_binding: ReferenceBindingState
    source_standing: str
    sensitivity: str
    instruction_provenance: InstructionProvenance
    retrieved_at: datetime
    currentness: SourceCurrentness
    representation: ContextRepresentation
    provenance_refs: tuple[str, ...] = ()
    transformation_lineage: tuple[str, ...] = ()
    derived_sensitivity: str | None = None
    contradiction_group_ref: str | None = None
    source_version_ref: str | None = None
    purpose_restrictions: tuple[str, ...] = ()
    valid_until: datetime | None = None
    interpretation_frame: RuntimeInterpretationFrame | None = None
    estimated_tokens: int | None = None
    size_bytes: int | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.fragment_id, name="fragment_id")
        _require_uuid7s(self.need_ids, name="need_ids")
        if not self.need_ids:
            raise ValueError("need_ids must not be empty")
        _require_text(self.source_standing, name="source_standing")
        _require_text(self.sensitivity, name="sensitivity")
        _require_aware(self.retrieved_at, name="retrieved_at")
        _require_texts(self.provenance_refs, name="provenance_refs")
        _require_texts(self.transformation_lineage, name="transformation_lineage")
        _require_texts(self.purpose_restrictions, name="purpose_restrictions")
        for name, value in (
            ("derived_sensitivity", self.derived_sensitivity),
            ("contradiction_group_ref", self.contradiction_group_ref),
            ("source_version_ref", self.source_version_ref),
        ):
            if value is not None:
                _require_text(value, name=name)
        if self.valid_until is not None:
            _require_aware(self.valid_until, name="valid_until")
            if self.valid_until < self.retrieved_at:
                raise ValueError("valid_until must not precede retrieved_at")
        if self.estimated_tokens is not None and self.estimated_tokens < 0:
            raise ValueError("estimated_tokens must not be negative")
        if self.size_bytes is not None and self.size_bytes < 0:
            raise ValueError("size_bytes must not be negative")


@dataclass(frozen=True, slots=True)
class NeedReadiness:
    """Current detailed status for one InformationNeed."""

    need_id: UUID
    status: InformationNeedStatus

    def __post_init__(self) -> None:
        _require_uuid7(self.need_id, name="need_id")


@dataclass(frozen=True, slots=True)
class ContextReadiness:
    """Consumer-/step-specific context readiness evaluation."""

    readiness_id: UUID
    plan_id: UUID
    plan_revision: int
    state: ContextReadinessState
    need_states: tuple[NeedReadiness, ...]
    evaluated_at: datetime
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.readiness_id, name="readiness_id")
        _require_uuid7(self.plan_id, name="plan_id")
        if self.plan_revision <= 0:
            raise ValueError("plan_revision must be positive")
        _require_aware(self.evaluated_at, name="evaluated_at")
        _require_texts(self.limitations, name="limitations")
        need_ids = tuple(state.need_id for state in self.need_states)
        if len(need_ids) != len(set(need_ids)):
            raise ValueError("need_states must not contain duplicate need_id values")
        if (
            self.state is ContextReadinessState.PARTIAL_WITH_DECLARED_LIMITATION
            and not self.limitations
        ):
            raise ValueError("partial readiness requires declared limitations")


@dataclass(frozen=True, slots=True)
class ConsumerContext:
    """Exact minimized runtime context surface for one consumer invocation."""

    context_id: UUID
    work_id: UUID
    work_revision: int
    plan_id: UUID
    plan_revision: int
    consumer_id: str
    purpose: str
    privacy_compartment: str
    fragment_ids: tuple[UUID, ...]
    current_user_instruction: str | None = None
    instruction_profile_ref: str | None = None
    capability_projection_refs: tuple[str, ...] = ()
    continuity_state_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.context_id, name="context_id")
        _require_uuid7(self.work_id, name="work_id")
        _require_uuid7(self.plan_id, name="plan_id")
        if self.work_revision <= 0 or self.plan_revision <= 0:
            raise ValueError("work/plan revisions must be positive")
        _require_text(self.consumer_id, name="consumer_id")
        _require_text(self.purpose, name="purpose")
        _require_text(self.privacy_compartment, name="privacy_compartment")
        _require_uuid7s(self.fragment_ids, name="fragment_ids")
        _require_texts(
            self.capability_projection_refs,
            name="capability_projection_refs",
        )
        _require_texts(self.continuity_state_refs, name="continuity_state_refs")
        _require_texts(self.limitations, name="limitations")
        if self.current_user_instruction is not None:
            _require_text(self.current_user_instruction, name="current_user_instruction")
        if self.instruction_profile_ref is not None:
            _require_text(self.instruction_profile_ref, name="instruction_profile_ref")


@dataclass(frozen=True, slots=True)
class ContextManifest:
    """Immutable consumer exposure receipt; not a causal-use or basis claim."""

    manifest_id: UUID
    consumer_context_id: UUID
    work_id: UUID
    work_revision: int
    plan_id: UUID
    plan_revision: int
    information_need_ids: tuple[UUID, ...]
    exposed_fragment_ids: tuple[UUID, ...]
    source_bindings: tuple[TargetRef, ...]
    reality_scope: RealityScope
    exposure_state: ExposureState
    consumer_binding: str
    created_at: datetime
    interpretation_frame: RuntimeInterpretationFrame | None = None
    representation_transform_refs: tuple[str, ...] = ()
    instruction_profile_ref: str | None = None
    capability_projection_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("manifest_id", self.manifest_id),
            ("consumer_context_id", self.consumer_context_id),
            ("work_id", self.work_id),
            ("plan_id", self.plan_id),
        ):
            _require_uuid7(value, name=name)
        if self.work_revision <= 0 or self.plan_revision <= 0:
            raise ValueError("work/plan revisions must be positive")
        _require_uuid7s(self.information_need_ids, name="information_need_ids")
        _require_uuid7s(self.exposed_fragment_ids, name="exposed_fragment_ids")
        _require_text(self.consumer_binding, name="consumer_binding")
        _require_aware(self.created_at, name="created_at")
        _require_texts(
            self.representation_transform_refs,
            name="representation_transform_refs",
        )
        _require_texts(
            self.capability_projection_refs,
            name="capability_projection_refs",
        )
        _require_texts(self.limitations, name="limitations")
        if len(self.source_bindings) != len(set(self.source_bindings)):
            raise ValueError("source_bindings must not contain duplicates")
        if self.instruction_profile_ref is not None:
            _require_text(self.instruction_profile_ref, name="instruction_profile_ref")
        if self.exposure_state is ExposureState.NOT_SENT and self.exposed_fragment_ids:
            raise ValueError("NOT_SENT manifest must not claim exposed fragments")


@dataclass(frozen=True, slots=True)
class BasisManifest:
    """Material dependency/currentness/coherence basis for a runtime result."""

    basis_id: UUID
    work_id: UUID
    work_revision: int
    source_bindings: tuple[TargetRef, ...]
    dependency_refs: tuple[str, ...]
    reality_scope: RealityScope
    basis_valid_at: datetime
    coherence_requirement: str
    currentness_requirement: str
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.basis_id, name="basis_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        if len(self.source_bindings) != len(set(self.source_bindings)):
            raise ValueError("source_bindings must not contain duplicates")
        _require_texts(self.dependency_refs, name="dependency_refs")
        _require_aware(self.basis_valid_at, name="basis_valid_at")
        _require_text(self.coherence_requirement, name="coherence_requirement")
        _require_text(self.currentness_requirement, name="currentness_requirement")
        _require_texts(self.limitations, name="limitations")
