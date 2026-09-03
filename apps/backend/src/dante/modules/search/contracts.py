"""Immutable public and application contracts for permission-safe Global Search."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Literal, NewType
from uuid import UUID

SearchFamilyId = NewType("SearchFamilyId", str)

type SearchScalar = str | int | float | bool | UUID
type SearchFilterValue = SearchScalar | tuple[SearchScalar, ...]


class SearchTemporalIntent(StrEnum):
    """Requested current/history discovery semantics."""

    CURRENT = "current"
    HISTORY = "history"


class SearchQueryMode(StrEnum):
    """Public query modes a Search family may truthfully support."""

    KEYWORD = "keyword"
    STRUCTURED_FILTER = "structured_filter"


class SearchFilterOperator(StrEnum):
    """Bounded structured-filter operators owned by Search."""

    EQ = "eq"
    NE = "ne"
    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"
    IN = "in"
    NOT_IN = "not_in"


class SearchGuarantee(StrEnum):
    """Truthful coverage guarantees, ordered separately by application policy."""

    EXACT = "exact"
    BOUNDED_COMPLETE = "bounded_complete"
    BEST_EFFORT = "best_effort"
    APPROXIMATE = "approximate"
    SAMPLED = "sampled"


class SearchFamilyActivationState(StrEnum):
    """Build-time Search-family activation posture."""

    INACTIVE = "inactive"
    ACTIVE = "active"


class SearchCurrentness(StrEnum):
    """Safe currentness classification exposed with a hit."""

    CURRENT = "current"
    HISTORICAL = "historical"
    UNKNOWN = "unknown"


class SearchLimitationCode(StrEnum):
    """Recipient-safe result limitation classes."""

    NO_ELIGIBLE_RESULT_SOURCE = "no_eligible_result_source"
    GUARANTEE_DOWNGRADED = "guarantee_downgraded"
    SOURCE_UNAVAILABLE = "source_unavailable"
    CURRENTNESS_LIMITED = "currentness_limited"


class NavigationStatus(StrEnum):
    """Safe navigation-resolution result."""

    RESOLVED = "resolved"
    UNAVAILABLE = "unavailable"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_texts(values: tuple[str, ...] | frozenset[str], *, name: str) -> None:
    if any(not value or not value.strip() for value in values):
        raise ValueError(f"{name} entries must be non-empty")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


@dataclass(frozen=True, slots=True)
class SearchFilter:
    """One bounded structured discovery predicate."""

    field: str
    operator: SearchFilterOperator
    value: SearchFilterValue

    def __post_init__(self) -> None:
        _require_text(self.field, name="filter field")
        is_collection = isinstance(self.value, tuple)
        if self.operator in {SearchFilterOperator.IN, SearchFilterOperator.NOT_IN}:
            if not is_collection or not self.value:
                raise ValueError("IN/NOT_IN filters require a non-empty tuple")
        elif is_collection:
            raise ValueError("only IN/NOT_IN filters accept tuple values")


@dataclass(frozen=True, slots=True)
class SearchInterpretationFrame:
    """Runtime interpretation needed when query meaning depends on time/locale."""

    reference_instant: datetime
    timezone: str
    locale: str
    units_system: str | None = None
    spatial_anchor: str | None = None

    def __post_init__(self) -> None:
        if self.reference_instant.tzinfo is None or self.reference_instant.utcoffset() is None:
            raise ValueError("reference_instant must be timezone-aware")
        _require_text(self.timezone, name="timezone")
        _require_text(self.locale, name="locale")
        if self.units_system is not None:
            _require_text(self.units_system, name="units_system")
        if self.spatial_anchor is not None:
            _require_text(self.spatial_anchor, name="spatial_anchor")


@dataclass(frozen=True, slots=True)
class SearchPageRequest:
    """Opaque-cursor pagination requested by the trusted route."""

    limit: int
    cursor: str | None = None

    def __post_init__(self) -> None:
        if self.limit <= 0:
            raise ValueError("page limit must be positive")
        if self.cursor is not None:
            _require_text(self.cursor, name="cursor")


@dataclass(frozen=True, slots=True)
class SearchPresentationRequest:
    """Optional observable Search features requested by the route."""

    include_snippets: bool = True
    include_facets: bool = False
    include_count: bool = False


@dataclass(frozen=True, slots=True)
class NativeSearchTargetRef:
    """Search navigation projection of a canonical NativeRef."""

    native_ref: UUID
    kind: Literal["native"] = "native"

    def __post_init__(self) -> None:
        _require_uuid7(self.native_ref, name="native_ref")


@dataclass(frozen=True, slots=True)
class ScopedRecordSearchTargetRef:
    """Search navigation projection of a canonical ScopedRecordRef."""

    scoped_record_ref: UUID
    kind: Literal["scoped_record"] = "scoped_record"

    def __post_init__(self) -> None:
        _require_uuid7(self.scoped_record_ref, name="scoped_record_ref")


@dataclass(frozen=True, slots=True)
class MaterialStateSearchTargetRef:
    """Search navigation projection of a canonical MaterialStateRef."""

    material_state_ref: UUID
    kind: Literal["material_state"] = "material_state"

    def __post_init__(self) -> None:
        _require_uuid7(self.material_state_ref, name="material_state_ref")


@dataclass(frozen=True, slots=True)
class ExternalSearchTargetRef:
    """Search navigation projection of an external source identity."""

    system: str
    external_ref: str
    kind: Literal["external"] = "external"

    def __post_init__(self) -> None:
        _require_text(self.system, name="external system")
        _require_text(self.external_ref, name="external_ref")


type SearchTargetRef = (
    NativeSearchTargetRef
    | ScopedRecordSearchTargetRef
    | MaterialStateSearchTargetRef
    | ExternalSearchTargetRef
)


@dataclass(frozen=True, slots=True)
class SearchFamilyEligibility:
    """Request-scoped Search projection for one family after authority evaluation."""

    family_id: SearchFamilyId
    owner_scopes: frozenset[str]
    source_scopes: frozenset[str]
    projection_fields: frozenset[str]
    permitted_filter_fields: frozenset[str]
    permitted_facet_fields: frozenset[str]
    allow_current: bool
    allow_history: bool
    allow_navigation: bool
    allow_snippets: bool
    allow_facets: bool
    allow_counts: bool
    sensitivity_ceiling: str | None
    source_lifecycle_exclusions: frozenset[str]
    excluded_scopes: frozenset[str]
    revalidation_requirement: str

    def __post_init__(self) -> None:
        _require_text(str(self.family_id), name="family_id")
        _require_texts(self.owner_scopes, name="owner_scopes")
        _require_texts(self.source_scopes, name="source_scopes")
        _require_texts(self.projection_fields, name="projection_fields")
        _require_texts(self.permitted_filter_fields, name="permitted_filter_fields")
        _require_texts(self.permitted_facet_fields, name="permitted_facet_fields")
        _require_texts(self.source_lifecycle_exclusions, name="source_lifecycle_exclusions")
        _require_texts(self.excluded_scopes, name="excluded_scopes")
        _require_text(self.revalidation_requirement, name="revalidation_requirement")
        if self.sensitivity_ceiling is not None:
            _require_text(self.sensitivity_ceiling, name="sensitivity_ceiling")


@dataclass(frozen=True, slots=True)
class SearchEligibilityEnvelope:
    """Immutable trusted projection of current authoritative Search eligibility."""

    principal_binding: str
    represented_party_binding: str | None
    purpose: str
    recipient: str
    surface: str
    authority_basis_refs: tuple[str, ...]
    authz_basis_refs: tuple[str, ...]
    visibility_basis_refs: tuple[str, ...]
    consent_basis_refs: tuple[str, ...]
    families: tuple[SearchFamilyEligibility, ...]

    def __post_init__(self) -> None:
        _require_text(self.principal_binding, name="principal_binding")
        if self.represented_party_binding is not None:
            _require_text(self.represented_party_binding, name="represented_party_binding")
        _require_text(self.purpose, name="purpose")
        _require_text(self.recipient, name="recipient")
        _require_text(self.surface, name="surface")
        _require_texts(self.authority_basis_refs, name="authority_basis_refs")
        _require_texts(self.authz_basis_refs, name="authz_basis_refs")
        _require_texts(self.visibility_basis_refs, name="visibility_basis_refs")
        _require_texts(self.consent_basis_refs, name="consent_basis_refs")
        family_ids = tuple(family.family_id for family in self.families)
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("Search eligibility contains duplicate family_id values")

    def for_family(self, family_id: SearchFamilyId) -> SearchFamilyEligibility | None:
        """Return only the explicitly eligible projection for one Search family."""
        return next((family for family in self.families if family.family_id == family_id), None)


@dataclass(frozen=True, slots=True)
class SearchExecutionRequest:
    """Trusted Search request constructed after inbound authentication/policy projection."""

    query: str
    filters: tuple[SearchFilter, ...]
    eligibility: SearchEligibilityEnvelope
    requested_family_ids: tuple[SearchFamilyId, ...]
    temporal_intent: SearchTemporalIntent
    page: SearchPageRequest
    requested_guarantee: SearchGuarantee
    presentation: SearchPresentationRequest
    purpose: str
    surface: str
    interpretation_frame: SearchInterpretationFrame | None = None

    def __post_init__(self) -> None:
        if not self.query.strip() and not self.filters:
            raise ValueError("Search requires a query or at least one structured filter")
        if len(self.requested_family_ids) != len(set(self.requested_family_ids)):
            raise ValueError("requested_family_ids must not contain duplicates")
        _require_text(self.purpose, name="purpose")
        _require_text(self.surface, name="surface")
        if self.purpose != self.eligibility.purpose:
            raise ValueError("request purpose must match SearchEligibilityEnvelope purpose")
        if self.surface != self.eligibility.surface:
            raise ValueError("request surface must match SearchEligibilityEnvelope surface")


@dataclass(frozen=True, slots=True)
class NavigationExecutionRequest:
    """Trusted request to turn a Search target hint into an owner-routable reference."""

    family_id: SearchFamilyId
    target: SearchTargetRef
    eligibility: SearchEligibilityEnvelope
    purpose: str
    surface: str

    def __post_init__(self) -> None:
        _require_text(str(self.family_id), name="family_id")
        _require_text(self.purpose, name="purpose")
        _require_text(self.surface, name="surface")
        if self.purpose != self.eligibility.purpose:
            raise ValueError("request purpose must match SearchEligibilityEnvelope purpose")
        if self.surface != self.eligibility.surface:
            raise ValueError("request surface must match SearchEligibilityEnvelope surface")


@dataclass(frozen=True, slots=True)
class SearchHit:
    """One permission-safe Search hit."""

    family_id: SearchFamilyId
    target: SearchTargetRef
    title: str
    rank: int
    currentness: SearchCurrentness
    snippet: str | None = None
    basis_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(str(self.family_id), name="family_id")
        _require_text(self.title, name="title")
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        if self.snippet is not None:
            _require_text(self.snippet, name="snippet")
        _require_texts(self.basis_refs, name="basis_refs")


@dataclass(frozen=True, slots=True)
class SearchFacet:
    """One permission-safe family-scoped facet bucket."""

    family_id: SearchFamilyId
    field: str
    value: str
    count: int

    def __post_init__(self) -> None:
        _require_text(str(self.family_id), name="family_id")
        _require_text(self.field, name="facet field")
        _require_text(self.value, name="facet value")
        if self.count < 0:
            raise ValueError("facet count must not be negative")


@dataclass(frozen=True, slots=True)
class SearchLimitation:
    """Recipient-safe limitation attached to a Search result."""

    code: SearchLimitationCode


@dataclass(frozen=True, slots=True)
class SearchResult:
    """Permission-safe Search output after the Search query boundary."""

    hits: tuple[SearchHit, ...]
    facets: tuple[SearchFacet, ...]
    total_count: int | None
    next_cursor: str | None
    achieved_guarantee: SearchGuarantee | None
    limitations: tuple[SearchLimitation, ...] = ()

    def __post_init__(self) -> None:
        if self.total_count is not None and self.total_count < 0:
            raise ValueError("total_count must not be negative")
        if self.next_cursor is not None:
            _require_text(self.next_cursor, name="next_cursor")

    @classmethod
    def no_eligible_source(cls) -> SearchResult:
        """Return the uniform empty result for no active+eligible Search family."""
        return cls(
            hits=(),
            facets=(),
            total_count=None,
            next_cursor=None,
            achieved_guarantee=None,
            limitations=(
                SearchLimitation(code=SearchLimitationCode.NO_ELIGIBLE_RESULT_SOURCE),
            ),
        )


@dataclass(frozen=True, slots=True)
class NavigationResult:
    """Safe owner-routing result; the owning capability must reauthorize target access."""

    status: NavigationStatus
    family_id: SearchFamilyId | None = None
    owning_capability: str | None = None
    target: SearchTargetRef | None = None

    def __post_init__(self) -> None:
        if self.status is NavigationStatus.RESOLVED:
            if self.family_id is None or self.owning_capability is None or self.target is None:
                raise ValueError("resolved navigation requires family, owner and target")
            _require_text(str(self.family_id), name="family_id")
            _require_text(self.owning_capability, name="owning_capability")
        elif any(
            value is not None
            for value in (self.family_id, self.owning_capability, self.target)
        ):
            raise ValueError("unavailable navigation must not expose target metadata")

    @classmethod
    def unavailable(cls) -> NavigationResult:
        """Return a uniform non-oracular navigation miss."""
        return cls(status=NavigationStatus.UNAVAILABLE)


@dataclass(frozen=True, slots=True)
class SearchFamilyRegistration:
    """Immutable SearchFamilyRegistry entry; never a database catalog row."""

    family_id: SearchFamilyId
    owning_capability: str
    source_semantics: str
    query_modes: frozenset[SearchQueryMode]
    filter_fields: frozenset[str]
    safe_projection_fields: frozenset[str]
    safe_facet_fields: frozenset[str]
    supports_current: bool
    supports_history: bool
    supports_source_reread: bool
    maximum_guarantee: SearchGuarantee
    eligibility_requirement_codes: frozenset[str]
    query_implementation_id: str
    basis_mapping: str
    coherence_requirement: str
    snapshot_requirement: str
    currentness_rule: str
    publication_revalidation_requirement: str
    activation_evidence_ref: str | None
    direct_proof_ids: tuple[str, ...]
    activation_state: SearchFamilyActivationState

    def __post_init__(self) -> None:
        _require_text(str(self.family_id), name="family_id")
        _require_text(self.owning_capability, name="owning_capability")
        _require_text(self.source_semantics, name="source_semantics")
        if not self.query_modes:
            raise ValueError("query_modes must not be empty")
        _require_texts(self.filter_fields, name="filter_fields")
        _require_texts(self.safe_projection_fields, name="safe_projection_fields")
        _require_texts(self.safe_facet_fields, name="safe_facet_fields")
        _require_texts(
            self.eligibility_requirement_codes,
            name="eligibility_requirement_codes",
        )
        _require_text(self.query_implementation_id, name="query_implementation_id")
        _require_text(self.basis_mapping, name="basis_mapping")
        _require_text(self.coherence_requirement, name="coherence_requirement")
        _require_text(self.snapshot_requirement, name="snapshot_requirement")
        _require_text(self.currentness_rule, name="currentness_rule")
        _require_text(
            self.publication_revalidation_requirement,
            name="publication_revalidation_requirement",
        )
        if self.activation_evidence_ref is not None:
            _require_text(self.activation_evidence_ref, name="activation_evidence_ref")
        _require_texts(self.direct_proof_ids, name="direct_proof_ids")
        if (
            self.activation_state is SearchFamilyActivationState.ACTIVE
            and self.activation_evidence_ref is None
        ):
            raise ValueError("active Search family requires activation evidence")
