"""Bounded Search-specific read/query port.

Implementations must apply the supplied eligible family/source universe before rank,
count, facet, pagination or other observable semantics.
"""

from dataclasses import dataclass
from typing import Protocol

from dante.modules.search.contracts import (
    NavigationResult,
    SearchFamilyId,
    SearchFilter,
    SearchGuarantee,
    SearchInterpretationFrame,
    SearchPageRequest,
    SearchResult,
    SearchTargetRef,
    SearchTemporalIntent,
)


@dataclass(frozen=True, slots=True)
class SearchExecutionAccessContext:
    """Minimized current access/basis context needed for Search revalidation."""

    principal_binding: str
    represented_party_binding: str | None
    recipient: str
    authority_basis_refs: tuple[str, ...]
    authz_basis_refs: tuple[str, ...]
    visibility_basis_refs: tuple[str, ...]
    consent_basis_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SearchFamilyExecutionScope:
    """Family projection admitted for one Search execution."""

    family_id: SearchFamilyId
    owning_capability: str
    source_semantics: str
    query_implementation_id: str
    owner_scopes: frozenset[str]
    source_scopes: frozenset[str]
    filter_fields: frozenset[str]
    projection_fields: frozenset[str]
    facet_fields: frozenset[str]
    source_lifecycle_exclusions: frozenset[str]
    excluded_scopes: frozenset[str]
    sensitivity_ceiling: str | None
    revalidation_requirement: str
    supports_source_reread: bool
    maximum_guarantee: SearchGuarantee
    basis_mapping: str
    coherence_requirement: str
    snapshot_requirement: str
    currentness_rule: str
    publication_revalidation_requirement: str
    include_navigation: bool
    include_snippets: bool
    include_facets: bool


@dataclass(frozen=True, slots=True)
class SearchQueryExecution:
    """Already-eligible bounded query handed to the outbound Search adapter."""

    query: str
    filters: tuple[SearchFilter, ...]
    families: tuple[SearchFamilyExecutionScope, ...]
    temporal_intent: SearchTemporalIntent
    page: SearchPageRequest
    requested_guarantee: SearchGuarantee
    maximum_guarantee: SearchGuarantee
    include_count: bool
    purpose: str
    surface: str
    access: SearchExecutionAccessContext
    interpretation_frame: SearchInterpretationFrame | None


@dataclass(frozen=True, slots=True)
class SearchNavigationExecution:
    """Already-eligible navigation request handed to the outbound Search adapter."""

    family: SearchFamilyExecutionScope
    target: SearchTargetRef
    purpose: str
    surface: str
    access: SearchExecutionAccessContext


class SearchQueryPort(Protocol):
    """Search-specific outbound read port; not a generic repository."""

    async def search(self, request: SearchQueryExecution) -> SearchResult:
        """Return only permission-safe observable Search results."""
        ...

    async def resolve_navigation(
        self,
        request: SearchNavigationExecution,
    ) -> NavigationResult:
        """Resolve a target hint without bypassing owning-capability authorization."""
        ...
