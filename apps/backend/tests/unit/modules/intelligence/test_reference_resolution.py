"""Unit acceptance for eligible-universe reference-resolution semantics."""

from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.references import (
    NativeRefBinding,
    ReferenceBindingRequirement,
    ReferenceCandidate,
    ReferenceCandidateMatch,
    ReferenceResolutionRequest,
    ReferenceResolutionResult,
    ReferenceResolutionStatus,
)
from tests.unit.modules.intelligence.fakes import EligibleUniverseReferenceResolverFake


def _candidate(
    label: str,
    match: ReferenceCandidateMatch,
) -> ReferenceCandidate:
    return ReferenceCandidate(
        target=NativeRefBinding(native_ref=uuid7()),
        display_label=label,
        source_scope="schedule:visible",
        match=match,
        basis_refs=("visibility:current",),
    )


def _request(
    candidates: tuple[ReferenceCandidate, ...],
    *,
    requirement: ReferenceBindingRequirement = ReferenceBindingRequirement.UNIQUE_IN_SCOPE,
) -> ReferenceResolutionRequest:
    return ReferenceResolutionRequest(
        request_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        reference_text="dentist appointment",
        purpose="ask_dante",
        required_binding=requirement,
        declared_bounded_universe_id="eligible:schedule:self",
        eligible_candidates=candidates,
    )


@pytest.mark.asyncio
async def test_single_eligible_candidate_resolves_without_hidden_ambiguity() -> None:
    resolver = EligibleUniverseReferenceResolverFake()
    visible = _candidate("Dentist appointment", ReferenceCandidateMatch.POSSIBLE)

    result = await resolver.resolve(_request((visible,)))

    assert result.status is ReferenceResolutionStatus.RESOLVED
    assert result.resolved_target == visible.target
    assert result.achieved_binding is ReferenceBindingRequirement.UNIQUE_IN_SCOPE
    assert resolver.requests[0].eligible_candidates == (visible,)


@pytest.mark.asyncio
async def test_exact_candidate_preserves_stronger_resolution_proof() -> None:
    resolver = EligibleUniverseReferenceResolverFake()
    exact = _candidate("Dentist appointment", ReferenceCandidateMatch.EXACT)

    result = await resolver.resolve(_request((exact,)))

    assert result.status is ReferenceResolutionStatus.RESOLVED
    assert result.achieved_binding is ReferenceBindingRequirement.EXACT_CANONICAL


@pytest.mark.asyncio
async def test_multiple_eligible_matches_are_ambiguous() -> None:
    resolver = EligibleUniverseReferenceResolverFake()
    first = _candidate("Dentist A", ReferenceCandidateMatch.POSSIBLE)
    second = _candidate("Dentist B", ReferenceCandidateMatch.EXACT)

    result = await resolver.resolve(_request((first, second)))

    assert result.status is ReferenceResolutionStatus.AMBIGUOUS
    assert result.eligible_candidates == (first, second)
    assert result.resolved_target is None
    assert result.achieved_binding is None


@pytest.mark.asyncio
async def test_exact_requirement_does_not_promote_possible_candidate() -> None:
    resolver = EligibleUniverseReferenceResolverFake()
    candidate = _candidate("Dentist", ReferenceCandidateMatch.POSSIBLE)

    result = await resolver.resolve(
        _request(
            (candidate,),
            requirement=ReferenceBindingRequirement.EXACT_CANONICAL,
        )
    )

    assert result.status is ReferenceResolutionStatus.UNRESOLVED
    assert result.resolved_target is None
    assert result.achieved_binding is None


@pytest.mark.asyncio
async def test_empty_declared_universe_has_bounded_not_found_semantics() -> None:
    resolver = EligibleUniverseReferenceResolverFake()

    result = await resolver.resolve(_request(()))

    assert (
        result.status
        is ReferenceResolutionStatus.NOT_FOUND_IN_DECLARED_BOUNDED_UNIVERSE
    )


def test_non_resolved_outcome_cannot_smuggle_resolved_target() -> None:
    target = NativeRefBinding(native_ref=uuid7())
    with pytest.raises(ValueError, match="non-RESOLVED"):
        ReferenceResolutionResult(
            request_id=uuid7(),
            status=ReferenceResolutionStatus.UNRESOLVED,
            declared_bounded_universe_id="eligible:schedule:self",
            resolved_target=target,
            achieved_binding=ReferenceBindingRequirement.EXACT_CANONICAL,
        )
