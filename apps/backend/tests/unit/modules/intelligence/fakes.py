"""Deterministic Intelligence fakes used only by unit acceptance tests."""

from __future__ import annotations

from collections.abc import Mapping
from uuid import UUID

from dante.modules.intelligence.contracts.evidence import RuntimeEvidenceEvent
from dante.modules.intelligence.contracts.policy import (
    ContextExposurePolicyRequest,
    EffectPolicyRequest,
    ModelEgressPolicyRequest,
    PolicyBoundary,
    PolicyDecision,
    PublicationPolicyRequest,
)
from dante.modules.intelligence.contracts.references import (
    ReferenceBindingRequirement,
    ReferenceCandidateMatch,
    ReferenceResolutionRequest,
    ReferenceResolutionResult,
    ReferenceResolutionStatus,
)
from dante.modules.intelligence.contracts.resource import (
    ResourceAdmission,
    ResourceAdmissionRequest,
    ResourceEstimate,
    ResourceEstimateRequest,
    ResourceSettlement,
    ResourceSettlementRequest,
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


class ScriptedPolicyPort:
    """Return explicit boundary decisions without inventing application authorization truth."""

    def __init__(self, decisions: Mapping[PolicyBoundary, PolicyDecision]) -> None:
        self._decisions = dict(decisions)
        self.context_exposure_requests: list[ContextExposurePolicyRequest] = []
        self.model_egress_requests: list[ModelEgressPolicyRequest] = []
        self.effect_requests: list[EffectPolicyRequest] = []
        self.publication_requests: list[PublicationPolicyRequest] = []

    def _decision(self, boundary: PolicyBoundary) -> PolicyDecision:
        try:
            decision = self._decisions[boundary]
        except KeyError as exc:
            raise LookupError("deterministic fake has no scripted policy decision") from exc
        if decision.boundary is not boundary:
            raise ValueError("scripted PolicyDecision does not match requested boundary")
        return decision

    async def authorize_context_exposure(
        self,
        request: ContextExposurePolicyRequest,
    ) -> PolicyDecision:
        self.context_exposure_requests.append(request)
        return self._decision(PolicyBoundary.CONTEXT_EXPOSURE)

    async def authorize_model_egress(
        self,
        request: ModelEgressPolicyRequest,
    ) -> PolicyDecision:
        self.model_egress_requests.append(request)
        return self._decision(PolicyBoundary.MODEL_EGRESS)

    async def authorize_effect(self, request: EffectPolicyRequest) -> PolicyDecision:
        self.effect_requests.append(request)
        return self._decision(PolicyBoundary.EFFECT)

    async def authorize_publication(
        self,
        request: PublicationPolicyRequest,
    ) -> PolicyDecision:
        self.publication_requests.append(request)
        return self._decision(PolicyBoundary.PUBLICATION)


class ScriptedResourceControl:
    """Return predeclared request-local resource decisions and record each phase."""

    def __init__(
        self,
        *,
        estimates: Mapping[UUID, ResourceEstimate],
        admissions: Mapping[UUID, ResourceAdmission],
        settlements: Mapping[UUID, ResourceSettlement],
    ) -> None:
        self._estimates = dict(estimates)
        self._admissions = dict(admissions)
        self._settlements = dict(settlements)
        self.estimate_requests: list[ResourceEstimateRequest] = []
        self.admission_requests: list[ResourceAdmissionRequest] = []
        self.settlement_requests: list[ResourceSettlementRequest] = []

    async def estimate(self, request: ResourceEstimateRequest) -> ResourceEstimate:
        self.estimate_requests.append(request)
        try:
            return self._estimates[request.request_id]
        except KeyError as exc:
            raise LookupError("deterministic fake has no scripted resource estimate") from exc

    async def admit(self, request: ResourceAdmissionRequest) -> ResourceAdmission:
        self.admission_requests.append(request)
        try:
            return self._admissions[request.request_id]
        except KeyError as exc:
            raise LookupError("deterministic fake has no scripted resource admission") from exc

    async def settle(self, request: ResourceSettlementRequest) -> ResourceSettlement:
        self.settlement_requests.append(request)
        try:
            return self._settlements[request.request_id]
        except KeyError as exc:
            raise LookupError("deterministic fake has no scripted resource settlement") from exc


class RecordingRuntimeEvidencePort:
    """Capture minimized runtime evidence without external I/O."""

    def __init__(self) -> None:
        self.events: list[RuntimeEvidenceEvent] = []

    async def emit(self, event: RuntimeEvidenceEvent) -> None:
        self.events.append(event)
