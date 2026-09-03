"""Unit tests for immutable Search contracts."""

from datetime import UTC, datetime
from uuid import uuid4, uuid7

import pytest

from dante.modules.search.contracts import (
    MaterialStateSearchTargetRef,
    NativeSearchTargetRef,
    NavigationResult,
    NavigationStatus,
    SearchEligibilityEnvelope,
    SearchExecutionRequest,
    SearchFamilyEligibility,
    SearchFamilyId,
    SearchFilter,
    SearchFilterOperator,
    SearchGuarantee,
    SearchInterpretationFrame,
    SearchPageRequest,
    SearchPresentationRequest,
    SearchTemporalIntent,
)


def _eligibility() -> SearchEligibilityEnvelope:
    family_id = SearchFamilyId("schedule")
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
        families=(
            SearchFamilyEligibility(
                family_id=family_id,
                owner_scopes=frozenset({"owner:self"}),
                source_scopes=frozenset({"schedule:current"}),
                projection_fields=frozenset({"title", "starts_at"}),
                permitted_filter_fields=frozenset({"status"}),
                permitted_facet_fields=frozenset({"status"}),
                allow_current=True,
                allow_history=False,
                allow_navigation=True,
                allow_snippets=True,
                allow_facets=False,
                allow_counts=False,
                sensitivity_ceiling="private",
                source_lifecycle_exclusions=frozenset({"retired"}),
                excluded_scopes=frozenset(),
                revalidation_requirement="before_publication",
            ),
        ),
    )


def test_search_reference_projections_require_uuid7() -> None:
    with pytest.raises(ValueError, match="UUIDv7"):
        NativeSearchTargetRef(native_ref=uuid4())
    assert MaterialStateSearchTargetRef(material_state_ref=uuid7()).kind == "material_state"


def test_structured_filter_operator_shape_is_explicit() -> None:
    with pytest.raises(ValueError, match="non-empty tuple"):
        SearchFilter(field="status", operator=SearchFilterOperator.IN, value=())
    with pytest.raises(ValueError, match="only IN/NOT_IN"):
        SearchFilter(
            field="status",
            operator=SearchFilterOperator.EQ,
            value=("open", "done"),
        )


def test_trusted_request_requires_query_or_filter_and_route_coherence() -> None:
    eligibility = _eligibility()
    with pytest.raises(ValueError, match="query or at least one"):
        SearchExecutionRequest(
            query=" ",
            filters=(),
            eligibility=eligibility,
            requested_family_ids=(SearchFamilyId("schedule"),),
            temporal_intent=SearchTemporalIntent.CURRENT,
            page=SearchPageRequest(limit=20),
            requested_guarantee=SearchGuarantee.BEST_EFFORT,
            presentation=SearchPresentationRequest(),
            purpose="global_search",
            surface="web",
        )
    with pytest.raises(ValueError, match="purpose"):
        SearchExecutionRequest(
            query="dentist",
            filters=(),
            eligibility=eligibility,
            requested_family_ids=(SearchFamilyId("schedule"),),
            temporal_intent=SearchTemporalIntent.CURRENT,
            page=SearchPageRequest(limit=20),
            requested_guarantee=SearchGuarantee.BEST_EFFORT,
            presentation=SearchPresentationRequest(),
            purpose="other",
            surface="web",
        )


def test_interpretation_frame_requires_timezone_aware_reference() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        SearchInterpretationFrame(
            reference_instant=datetime.fromisoformat("2026-09-03T10:00:00"),
            timezone="Europe/Rome",
            locale="it-IT",
        )
    frame = SearchInterpretationFrame(
        reference_instant=datetime.now(UTC),
        timezone="Europe/Rome",
        locale="it-IT",
    )
    assert frame.reference_instant.utcoffset() is not None


def test_navigation_unavailable_never_exposes_target_metadata() -> None:
    with pytest.raises(ValueError, match="must not expose"):
        NavigationResult(
            status=NavigationStatus.UNAVAILABLE,
            family_id=SearchFamilyId("schedule"),
        )
    assert NavigationResult.unavailable().family_id is None
