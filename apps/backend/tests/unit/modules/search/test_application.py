"""Unit acceptance for Search registry/eligibility/application-shell semantics."""

from uuid import uuid7

import pytest

from dante.modules.search.application import (
    SearchApplication,
    SearchContractViolation,
    SearchFamilyRegistry,
)
from dante.modules.search.contracts import (
    NativeSearchTargetRef,
    NavigationExecutionRequest,
    NavigationResult,
    NavigationStatus,
    SearchCurrentness,
    SearchEligibilityEnvelope,
    SearchExecutionRequest,
    SearchFacet,
    SearchFamilyActivationState,
    SearchFamilyEligibility,
    SearchFamilyId,
    SearchFamilyRegistration,
    SearchFilter,
    SearchFilterOperator,
    SearchGuarantee,
    SearchHit,
    SearchPageRequest,
    SearchPresentationRequest,
    SearchQueryMode,
    SearchResult,
    SearchTemporalIntent,
)
from dante.modules.search.ports.query import (
    SearchNavigationExecution,
    SearchQueryExecution,
)


class RecordingQueryPort:
    """Deterministic fake used only to inspect the admitted Search boundary."""

    def __init__(self, result: SearchResult) -> None:
        self.result = result
        self.search_requests: list[SearchQueryExecution] = []
        self.navigation_requests: list[SearchNavigationExecution] = []

    async def search(self, request: SearchQueryExecution) -> SearchResult:
        self.search_requests.append(request)
        return self.result

    async def resolve_navigation(
        self,
        request: SearchNavigationExecution,
    ) -> NavigationResult:
        self.navigation_requests.append(request)
        return NavigationResult(
            status=NavigationStatus.RESOLVED,
            family_id=request.family.family_id,
            owning_capability="schedule",
            target=request.target,
        )


def _registration(
    family: str,
    *,
    owner: str = "schedule",
    state: SearchFamilyActivationState = SearchFamilyActivationState.ACTIVE,
    maximum_guarantee: SearchGuarantee = SearchGuarantee.EXACT,
) -> SearchFamilyRegistration:
    return SearchFamilyRegistration(
        family_id=SearchFamilyId(family),
        owning_capability=owner,
        source_semantics="canonical_schedule",
        query_modes=frozenset({SearchQueryMode.KEYWORD, SearchQueryMode.STRUCTURED_FILTER}),
        filter_fields=frozenset({"status"}),
        safe_projection_fields=frozenset({"title", "starts_at"}),
        safe_facet_fields=frozenset({"status"}),
        supports_current=True,
        supports_history=False,
        supports_source_reread=True,
        maximum_guarantee=maximum_guarantee,
        eligibility_requirement_codes=frozenset({"current_access"}),
        query_implementation_id=f"{family}:query:v1",
        basis_mapping="source_row_revision",
        coherence_requirement="single_statement",
        snapshot_requirement="statement_snapshot",
        currentness_rule="reread_before_publication",
        publication_revalidation_requirement="current_access_and_source",
        activation_evidence_ref=(
            f"synthetic:{family}" if state is SearchFamilyActivationState.ACTIVE else None
        ),
        direct_proof_ids=(),
        activation_state=state,
    )


def _family_eligibility(
    family: str,
    *,
    allow_navigation: bool = True,
    allow_snippets: bool = True,
    allow_facets: bool = True,
    allow_counts: bool = True,
    permitted_filter_fields: frozenset[str] = frozenset({"status"}),
    permitted_facet_fields: frozenset[str] = frozenset({"status"}),
) -> SearchFamilyEligibility:
    return SearchFamilyEligibility(
        family_id=SearchFamilyId(family),
        owner_scopes=frozenset({"owner:self"}),
        source_scopes=frozenset({f"{family}:current"}),
        projection_fields=frozenset({"title"}),
        permitted_filter_fields=permitted_filter_fields,
        permitted_facet_fields=permitted_facet_fields,
        allow_current=True,
        allow_history=False,
        allow_navigation=allow_navigation,
        allow_snippets=allow_snippets,
        allow_facets=allow_facets,
        allow_counts=allow_counts,
        sensitivity_ceiling="private",
        source_lifecycle_exclusions=frozenset({"retired"}),
        excluded_scopes=frozenset(),
        revalidation_requirement="before_publication",
    )


def _envelope(*families: SearchFamilyEligibility) -> SearchEligibilityEnvelope:
    return SearchEligibilityEnvelope(
        principal_binding="principal:self",
        represented_party_binding=None,
        purpose="global_search",
        recipient="self",
        surface="web",
        authority_basis_refs=("authority:1",),
        authz_basis_refs=("authz:1",),
        visibility_basis_refs=("visibility:1",),
        consent_basis_refs=(),
        families=tuple(families),
    )


def _request(
    eligibility: SearchEligibilityEnvelope,
    *families: str,
    filters: tuple[SearchFilter, ...] = (),
    requested_guarantee: SearchGuarantee = SearchGuarantee.EXACT,
    include_snippets: bool = True,
    include_facets: bool = True,
    include_count: bool = True,
    page_size: int = 20,
) -> SearchExecutionRequest:
    return SearchExecutionRequest(
        query="dentist",
        filters=filters,
        eligibility=eligibility,
        requested_family_ids=tuple(SearchFamilyId(family) for family in families),
        temporal_intent=SearchTemporalIntent.CURRENT,
        page=SearchPageRequest(limit=page_size),
        requested_guarantee=requested_guarantee,
        presentation=SearchPresentationRequest(
            include_snippets=include_snippets,
            include_facets=include_facets,
            include_count=include_count,
        ),
        purpose="global_search",
        surface="web",
    )


def _empty_result(
    guarantee: SearchGuarantee | None = SearchGuarantee.BEST_EFFORT,
) -> SearchResult:
    return SearchResult(
        hits=(),
        facets=(),
        total_count=None,
        next_cursor=None,
        achieved_guarantee=guarantee,
    )


def test_registry_rejects_duplicate_family_ids() -> None:
    registration = _registration("schedule")
    with pytest.raises(ValueError, match="duplicate family_id"):
        SearchFamilyRegistry((registration, registration))


@pytest.mark.asyncio
async def test_ineligible_or_inactive_families_never_reach_query_port() -> None:
    port = RecordingQueryPort(_empty_result())
    app = SearchApplication(
        registry=SearchFamilyRegistry(
            (
                _registration("schedule"),
                _registration("hidden_notes", owner="notes"),
                _registration(
                    "inactive",
                    state=SearchFamilyActivationState.INACTIVE,
                ),
            )
        ),
        query_port=port,
        max_page_size=50,
    )
    eligibility = _envelope(_family_eligibility("schedule"))

    result = await app.search(
        _request(eligibility, "schedule", "hidden_notes", "inactive", "unknown")
    )

    assert tuple(scope.family_id for scope in port.search_requests[0].families) == (
        SearchFamilyId("schedule"),
    )
    assert result == _empty_result()


@pytest.mark.asyncio
async def test_hidden_family_presence_does_not_change_no_eligible_result() -> None:
    eligibility = _envelope()
    request = _request(eligibility, "hidden_notes")

    with_hidden_port = RecordingQueryPort(_empty_result())
    with_hidden = SearchApplication(
        registry=SearchFamilyRegistry((_registration("hidden_notes", owner="notes"),)),
        query_port=with_hidden_port,
        max_page_size=50,
    )
    without_hidden_port = RecordingQueryPort(_empty_result())
    without_hidden = SearchApplication(
        registry=SearchFamilyRegistry(()),
        query_port=without_hidden_port,
        max_page_size=50,
    )

    assert await with_hidden.search(request) == await without_hidden.search(request)
    assert with_hidden_port.search_requests == []
    assert without_hidden_port.search_requests == []


@pytest.mark.asyncio
async def test_access_basis_and_observable_scopes_are_minimized_before_query() -> None:
    port = RecordingQueryPort(_empty_result())
    app = SearchApplication(
        registry=SearchFamilyRegistry(
            (_registration("schedule"), _registration("notes", owner="notes"))
        ),
        query_port=port,
        max_page_size=50,
    )
    eligibility = _envelope(
        _family_eligibility("schedule"),
        _family_eligibility(
            "notes",
            allow_snippets=False,
            allow_facets=False,
            allow_counts=False,
        ),
    )

    await app.search(_request(eligibility, "schedule", "notes"))

    execution = port.search_requests[0]
    assert execution.access.principal_binding == "principal:self"
    assert execution.access.authority_basis_refs == ("authority:1",)
    assert execution.include_count is False
    assert execution.families[0].include_snippets is True
    assert execution.families[0].include_facets is True
    assert execution.families[1].include_snippets is False
    assert execution.families[1].include_facets is False


@pytest.mark.asyncio
async def test_disallowed_filter_excludes_family_before_query_observables() -> None:
    port = RecordingQueryPort(_empty_result())
    app = SearchApplication(
        registry=SearchFamilyRegistry((_registration("schedule"),)),
        query_port=port,
        max_page_size=50,
    )
    eligibility = _envelope(
        _family_eligibility(
            "schedule",
            permitted_filter_fields=frozenset(),
        )
    )
    private_filter = SearchFilter(
        field="status",
        operator=SearchFilterOperator.EQ,
        value="private",
    )

    result = await app.search(_request(eligibility, "schedule", filters=(private_filter,)))

    assert result == SearchResult.no_eligible_source()
    assert port.search_requests == []


@pytest.mark.asyncio
async def test_family_maximum_guarantee_downgrades_request_explicitly() -> None:
    port = RecordingQueryPort(_empty_result(SearchGuarantee.BEST_EFFORT))
    app = SearchApplication(
        registry=SearchFamilyRegistry(
            (
                _registration(
                    "schedule",
                    maximum_guarantee=SearchGuarantee.BEST_EFFORT,
                ),
            )
        ),
        query_port=port,
        max_page_size=50,
    )

    result = await app.search(_request(_envelope(_family_eligibility("schedule")), "schedule"))

    assert port.search_requests[0].requested_guarantee is SearchGuarantee.BEST_EFFORT
    assert tuple(limitation.code.value for limitation in result.limitations) == (
        "guarantee_downgraded",
    )


@pytest.mark.asyncio
async def test_page_bound_is_application_owned_and_checked_before_query() -> None:
    port = RecordingQueryPort(_empty_result())
    app = SearchApplication(
        registry=SearchFamilyRegistry((_registration("schedule"),)),
        query_port=port,
        max_page_size=25,
    )

    with pytest.raises(ValueError, match="page exceeds"):
        await app.search(
            _request(
                _envelope(_family_eligibility("schedule")),
                "schedule",
                page_size=26,
            )
        )
    assert port.search_requests == []


@pytest.mark.asyncio
async def test_adapter_cannot_return_hit_from_unadmitted_family() -> None:
    hidden_hit = SearchHit(
        family_id=SearchFamilyId("hidden_notes"),
        target=NativeSearchTargetRef(native_ref=uuid7()),
        title="hidden",
        rank=1,
        currentness=SearchCurrentness.CURRENT,
    )
    port = RecordingQueryPort(
        SearchResult(
            hits=(hidden_hit,),
            facets=(),
            total_count=None,
            next_cursor=None,
            achieved_guarantee=SearchGuarantee.EXACT,
        )
    )
    app = SearchApplication(
        registry=SearchFamilyRegistry((_registration("schedule"),)),
        query_port=port,
        max_page_size=50,
    )

    with pytest.raises(SearchContractViolation, match="unadmitted family"):
        await app.search(_request(_envelope(_family_eligibility("schedule")), "schedule"))


@pytest.mark.asyncio
async def test_adapter_cannot_publish_disallowed_snippet_or_count() -> None:
    hit = SearchHit(
        family_id=SearchFamilyId("schedule"),
        target=NativeSearchTargetRef(native_ref=uuid7()),
        title="Dentist",
        rank=1,
        currentness=SearchCurrentness.CURRENT,
        snippet="private detail",
    )
    port = RecordingQueryPort(
        SearchResult(
            hits=(hit,),
            facets=(),
            total_count=1,
            next_cursor=None,
            achieved_guarantee=SearchGuarantee.EXACT,
        )
    )
    app = SearchApplication(
        registry=SearchFamilyRegistry((_registration("schedule"),)),
        query_port=port,
        max_page_size=50,
    )

    with pytest.raises(SearchContractViolation, match="disallowed snippet"):
        await app.search(
            _request(
                _envelope(
                    _family_eligibility(
                        "schedule",
                        allow_snippets=False,
                        allow_counts=False,
                    )
                ),
                "schedule",
            )
        )


@pytest.mark.asyncio
async def test_adapter_cannot_publish_unadmitted_facet_field() -> None:
    port = RecordingQueryPort(
        SearchResult(
            hits=(),
            facets=(
                SearchFacet(
                    family_id=SearchFamilyId("schedule"),
                    field="private_category",
                    value="secret",
                    count=1,
                ),
            ),
            total_count=None,
            next_cursor=None,
            achieved_guarantee=SearchGuarantee.EXACT,
        )
    )
    app = SearchApplication(
        registry=SearchFamilyRegistry((_registration("schedule"),)),
        query_port=port,
        max_page_size=50,
    )

    with pytest.raises(SearchContractViolation, match="disallowed facet"):
        await app.search(_request(_envelope(_family_eligibility("schedule")), "schedule"))


@pytest.mark.asyncio
async def test_navigation_uses_same_active_eligible_intersection() -> None:
    port = RecordingQueryPort(_empty_result())
    app = SearchApplication(
        registry=SearchFamilyRegistry((_registration("schedule"),)),
        query_port=port,
        max_page_size=50,
    )
    target = NativeSearchTargetRef(native_ref=uuid7())

    unavailable = await app.resolve_navigation(
        NavigationExecutionRequest(
            family_id=SearchFamilyId("schedule"),
            target=target,
            eligibility=_envelope(_family_eligibility("schedule", allow_navigation=False)),
            purpose="global_search",
            surface="web",
        )
    )
    assert unavailable.status is NavigationStatus.UNAVAILABLE
    assert port.navigation_requests == []

    resolved = await app.resolve_navigation(
        NavigationExecutionRequest(
            family_id=SearchFamilyId("schedule"),
            target=target,
            eligibility=_envelope(_family_eligibility("schedule")),
            purpose="global_search",
            surface="web",
        )
    )
    assert resolved.status is NavigationStatus.RESOLVED
    assert port.navigation_requests[0].family.family_id == SearchFamilyId("schedule")
    assert port.navigation_requests[0].access.recipient == "self"
