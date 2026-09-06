"""Policy consumer port; authoritative application policy remains outside Intelligence."""

from typing import Protocol

from dante.modules.intelligence.contracts.policy import (
    ContextExposurePolicyRequest,
    EffectPolicyRequest,
    ModelEgressPolicyRequest,
    PolicyDecision,
    PublicationPolicyRequest,
)


class IntelligencePolicyPort(Protocol):
    """Consume current policy decisions at each material Intelligence boundary."""

    async def authorize_context_exposure(
        self,
        request: ContextExposurePolicyRequest,
    ) -> PolicyDecision: ...

    async def authorize_model_egress(
        self,
        request: ModelEgressPolicyRequest,
    ) -> PolicyDecision: ...

    async def authorize_effect(
        self,
        request: EffectPolicyRequest,
    ) -> PolicyDecision: ...

    async def authorize_publication(
        self,
        request: PublicationPolicyRequest,
    ) -> PolicyDecision: ...
