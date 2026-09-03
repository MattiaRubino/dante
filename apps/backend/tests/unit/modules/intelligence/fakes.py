"""Deterministic Intelligence fakes used only by unit acceptance tests."""

from __future__ import annotations

from collections.abc import Mapping
from uuid import UUID

from dante.modules.intelligence.contracts.references import (
    ReferenceBindingRequirement,
    ReferenceCandidateMatch,
    ReferenceResolutionRequest,
    ReferenceResolutionResult,
    ReferenceResolutionStatus,
)
from dante.modules.intelligence.contracts.retrieval import (
    CandidateValidationResult,
    RetrievalBatch,
    RetrievalCandidate,
    RetrievalPlan,
)
from dante.modules.intelligence.contracts.semantic_query import (
    SemanticQueryOutcome,
    SemanticQueryRequest,
    SemanticQueryStatus,
)


class EligibleUniverseReferenceResolverFake:
    """Resolve only within candidates already admitted by the caller."""

    def __init__(self) -> None:
        self.requests: list[ReferenceResolutionRequest] = []

    async def resolve(
        self,
        request: ReferenceResolutionRequest,
    ) -> ReferenceResolutionResult:
        self.requests.append(request)
        if request.required_binding is ReferenceBindingRequirement.EXACT_CANONICAL:
            accepted_matches = tuple(
                candidate
                for candidate in request.eligible_candidates
                if candidate.match is ReferenceCandidateMatch.EXACT
            )
        else:
            accepted_matches = request.eligible_candidates

        if len(accepted_matches) == 1:
            achieved_binding = (
                ReferenceBindingRequirement.EXACT_CANONICAL
                if accepted_matches[0].match is ReferenceCandidateMatch.EXACT
                else ReferenceBindingRequirement.UNIQUE_IN_SCOPE
            )
            return ReferenceResolutionResult(
                request_id=request.request_id,
                status=ReferenceResolutionStatus.RESOLVED,
                declared_bounded_universe_id=request.declared_bounded_universe_id,
                resolved_target=accepted_matches[0].target,
                achieved_binding=achieved_binding,
            )
        if len(accepted_matches) > 1:
            return ReferenceResolutionResult(
                request_id=request.request_id,
                status=ReferenceResolutionStatus.AMBIGUOUS,
                declared_bounded_universe_id=request.declared_bounded_universe_id,
                eligible_candidates=accepted_matches,
            )
        if request.eligible_candidates:
            return ReferenceResolutionResult(
                request_id=request.request_id,
                status=ReferenceResolutionStatus.UNRESOLVED,
                declared_bounded_universe_id=request.declared_bounded_universe_id,
            )
        return ReferenceResolutionResult(
            request_id=request.request_id,
            status=ReferenceResolutionStatus.NOT_FOUND_IN_DECLARED_BOUNDED_UNIVERSE,
            declared_bounded_universe_id=request.declared_bounded_universe_id,
        )


class ScriptedSemanticQueryGateway:
    """Return immutable outcomes by query identity and record every request."""

    def __init__(self, outcomes: Mapping[UUID, SemanticQueryOutcome]) -> None:
        self._outcomes = dict(outcomes)
        self.requests: list[SemanticQueryRequest] = []

    async def execute(self, request: SemanticQueryRequest) -> SemanticQueryOutcome:
        self.requests.append(request)
        outcome = self._outcomes.get(request.query_id)
        if outcome is not None:
            return outcome
        return SemanticQueryOutcome(
            query_id=request.query_id,
            status=SemanticQueryStatus.NOT_INTEGRATION_READY,
            limitations=("deterministic fake has no scripted capability seam",),
        )


class ScriptedRetrievalGateway:
    """Return predeclared candidate batches/validation outcomes without hidden I/O."""

    def __init__(
        self,
        *,
        batches: Mapping[UUID, RetrievalBatch],
        validations: Mapping[UUID, CandidateValidationResult],
    ) -> None:
        self._batches = dict(batches)
        self._validations = dict(validations)
        self.retrieve_requests: list[RetrievalPlan] = []
        self.validation_requests: list[RetrievalCandidate] = []

    async def retrieve(self, plan: RetrievalPlan) -> RetrievalBatch:
        self.retrieve_requests.append(plan)
        try:
            return self._batches[plan.plan_id]
        except KeyError as exc:
            raise LookupError("deterministic fake has no scripted retrieval batch") from exc

    async def validate(
        self,
        candidate: RetrievalCandidate,
    ) -> CandidateValidationResult:
        self.validation_requests.append(candidate)
        try:
            return self._validations[candidate.candidate_id]
        except KeyError as exc:
            raise LookupError("deterministic fake has no scripted validation") from exc
