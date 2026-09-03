"""Deterministic Search registry and application shell."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from types import MappingProxyType

from dante.modules.search.contracts import (
    NavigationExecutionRequest,
    NavigationResult,
    NavigationStatus,
    SearchExecutionRequest,
    SearchFamilyActivationState,
    SearchFamilyEligibility,
    SearchFamilyId,
    SearchFamilyRegistration,
    SearchGuarantee,
    SearchLimitation,
    SearchLimitationCode,
    SearchResult,
    SearchTemporalIntent,
)
from dante.modules.search.ports.query import (
    SearchFamilyExecutionScope,
    SearchNavigationExecution,
    SearchQueryExecution,
    SearchQueryPort,
)

_GUARANTEE_STRENGTH: Mapping[SearchGuarantee, int] = MappingProxyType(
    {
        SearchGuarantee.SAMPLED: 1,
        SearchGuarantee.APPROXIMATE: 2,
        SearchGuarantee.BEST_EFFORT: 3,
        SearchGuarantee.BOUNDED_COMPLETE: 4,
        SearchGuarantee.EXACT: 5,
    }
)


class SearchContractViolation(RuntimeError):
    """Raised when a Search adapter violates the admitted observable contract."""


class SearchFamilyRegistry:
    """Immutable Search-family registry with explicit activation metadata."""

    __slots__ = ("_by_id", "_registrations")

    def __init__(self, registrations: tuple[SearchFamilyRegistration, ...]) -> None:
        by_id = {registration.family_id: registration for registration in registrations}
        if len(by_id) != len(registrations):
            raise ValueError("SearchFamilyRegistry contains duplicate family_id values")
        self._registrations = registrations
        self._by_id: Mapping[SearchFamilyId, SearchFamilyRegistration] = MappingProxyType(
            by_id
        )

    @property
    def registrations(self) -> tuple[SearchFamilyRegistration, ...]:
        """Return immutable registry entries in declared order."""
        return self._registrations

    def active(self, family_id: SearchFamilyId) -> SearchFamilyRegistration | None:
        """Return one active registration without exposing inactive state to callers."""
        registration = self._by_id.get(family_id)
        if (
            registration is None
            or registration.activation_state is not SearchFamilyActivationState.ACTIVE
        ):
            return None
        return registration


class SearchApplication:
    """Deterministic application shell enforcing registry/eligibility before query I/O."""

    __slots__ = ("_max_page_size", "_query_port", "_registry")

    def __init__(
        self,
        *,
        registry: SearchFamilyRegistry,
        query_port: SearchQueryPort,
        max_page_size: int,
    ) -> None:
        if max_page_size <= 0:
            raise ValueError("max_page_size must be positive")
        self._registry = registry
        self._query_port = query_port
        self._max_page_size = max_page_size

    async def search(self, request: SearchExecutionRequest) -> SearchResult:
        """Execute Search only across the current active+eligible family intersection."""
        if request.page.limit > self._max_page_size:
            raise ValueError("requested page exceeds configured Search bound")

        family_pairs = self._eligible_family_pairs(request)
        if not family_pairs:
            return SearchResult.no_eligible_source()

        maximum_guarantee = _weakest_guarantee(
            tuple(registration.maximum_guarantee for registration, _ in family_pairs)
        )
        admitted_guarantee = _weaker_guarantee(
            request.requested_guarantee,
            maximum_guarantee,
        )
        scopes = tuple(
            _execution_scope(
                registration,
                eligibility,
                include_snippets=request.presentation.include_snippets,
            )
            for registration, eligibility in family_pairs
        )

        include_facets = request.presentation.include_facets and all(
            eligibility.allow_facets for _, eligibility in family_pairs
        )
        include_count = request.presentation.include_count and all(
            eligibility.allow_counts for _, eligibility in family_pairs
        )

        execution = SearchQueryExecution(
            query=request.query,
            filters=request.filters,
            families=scopes,
            temporal_intent=request.temporal_intent,
            page=request.page,
            requested_guarantee=admitted_guarantee,
            maximum_guarantee=maximum_guarantee,
            include_facets=include_facets,
            include_count=include_count,
            purpose=request.purpose,
            surface=request.surface,
            interpretation_frame=request.interpretation_frame,
        )
        result = await self._query_port.search(execution)
        _validate_search_result(result, execution)

        if admitted_guarantee is request.requested_guarantee:
            return result
        return replace(
            result,
            limitations=(
                *result.limitations,
                SearchLimitation(code=SearchLimitationCode.GUARANTEE_DOWNGRADED),
            ),
        )

    async def resolve_navigation(
        self,
        request: NavigationExecutionRequest,
    ) -> NavigationResult:
        """Resolve navigation only for an active and currently eligible family."""
        registration = self._registry.active(request.family_id)
        eligibility = request.eligibility.for_family(request.family_id)
        if registration is None or eligibility is None or not eligibility.source_scopes:
            return NavigationResult.unavailable()

        scope = _execution_scope(
            registration,
            eligibility,
            include_snippets=False,
        )
        if not scope.projection_fields:
            return NavigationResult.unavailable()

        result = await self._query_port.resolve_navigation(
            SearchNavigationExecution(
                family=scope,
                target=request.target,
                purpose=request.purpose,
                surface=request.surface,
            )
        )
        if result.status is NavigationStatus.UNAVAILABLE:
            return result
        if (
            result.family_id != request.family_id
            or result.owning_capability != registration.owning_capability
        ):
            raise SearchContractViolation(
                "navigation adapter escaped admitted Search family/owner"
            )
        return result

    def _eligible_family_pairs(
        self,
        request: SearchExecutionRequest,
    ) -> tuple[tuple[SearchFamilyRegistration, SearchFamilyEligibility], ...]:
        pairs: list[tuple[SearchFamilyRegistration, SearchFamilyEligibility]] = []
        for family_id in request.requested_family_ids:
            registration = self._registry.active(family_id)
            eligibility = request.eligibility.for_family(family_id)
            if registration is None or eligibility is None:
                continue
            if not eligibility.source_scopes:
                continue
            if not _temporal_allowed(
                request.temporal_intent,
                registration=registration,
                eligibility=eligibility,
            ):
                continue
            if not registration.safe_projection_fields.intersection(
                eligibility.projection_fields
            ):
                continue
            pairs.append((registration, eligibility))
        return tuple(pairs)


def _temporal_allowed(
    intent: SearchTemporalIntent,
    *,
    registration: SearchFamilyRegistration,
    eligibility: SearchFamilyEligibility,
) -> bool:
    if intent is SearchTemporalIntent.CURRENT:
        return registration.supports_current and eligibility.allow_current
    return registration.supports_history and eligibility.allow_history


def _execution_scope(
    registration: SearchFamilyRegistration,
    eligibility: SearchFamilyEligibility,
    *,
    include_snippets: bool,
) -> SearchFamilyExecutionScope:
    return SearchFamilyExecutionScope(
        family_id=registration.family_id,
        query_implementation_id=registration.query_implementation_id,
        source_scopes=eligibility.source_scopes,
        projection_fields=frozenset(
            registration.safe_projection_fields.intersection(
                eligibility.projection_fields
            )
        ),
        source_lifecycle_exclusions=eligibility.source_lifecycle_exclusions,
        excluded_scopes=eligibility.excluded_scopes,
        sensitivity_ceiling=eligibility.sensitivity_ceiling,
        revalidation_requirement=eligibility.revalidation_requirement,
        include_snippets=include_snippets and eligibility.allow_snippets,
    )


def _weakest_guarantee(values: tuple[SearchGuarantee, ...]) -> SearchGuarantee:
    if not values:
        raise ValueError("guarantee calculation requires at least one value")
    return min(values, key=_GUARANTEE_STRENGTH.__getitem__)


def _weaker_guarantee(
    left: SearchGuarantee,
    right: SearchGuarantee,
) -> SearchGuarantee:
    return min((left, right), key=_GUARANTEE_STRENGTH.__getitem__)


def _validate_search_result(
    result: SearchResult,
    execution: SearchQueryExecution,
) -> None:
    scopes = {scope.family_id: scope for scope in execution.families}

    for hit in result.hits:
        scope = scopes.get(hit.family_id)
        if scope is None:
            raise SearchContractViolation("Search adapter returned an unadmitted family")
        if hit.snippet is not None and not scope.include_snippets:
            raise SearchContractViolation("Search adapter returned a disallowed snippet")

    if result.facets and not execution.include_facets:
        raise SearchContractViolation("Search adapter returned disallowed facets")
    if any(facet.family_id not in scopes for facet in result.facets):
        raise SearchContractViolation("Search adapter returned facet for unadmitted family")
    if result.total_count is not None and not execution.include_count:
        raise SearchContractViolation("Search adapter returned a disallowed count")

    if (
        result.achieved_guarantee is not None
        and _GUARANTEE_STRENGTH[result.achieved_guarantee]
        > _GUARANTEE_STRENGTH[execution.maximum_guarantee]
    ):
        raise SearchContractViolation(
            "Search adapter claimed a guarantee above family registration"
        )
