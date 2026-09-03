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
class SearchFamilyExecutionScope:
    """Family projection admitted for one Search execution."""

    family_id: SearchFamilyId
    query_implementation_id: str
    source_scopes: frozenset[str]
    projection_fields: frozenset[str]
    source_lifecycle_exclusions: frozenset[str]
    excluded_scopes: frozenset[str]
    sensitivity_ceiling: str | None
    revalidation_requirement: str
    include_snippets: bool


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
    include_facets: bool
    include_count: bool
    purpose: str
    surface: str
    interpretation_frame: SearchInterpretationFrame | None


@dataclass(frozen=True, slots=True)
class SearchNavigationExecution:
    """Already-eligible navigation request handed to the outbound Search adapter."""

    family: SearchFamilyExecutionScope
    target: SearchTargetRef
    purpose: str
    surface: str


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
