"""Private provider-adapter port for one already-bound model invocation attempt."""

from __future__ import annotations

from typing import Protocol

from dante.modules.intelligence.contracts.model_access import (
    ProviderAttemptResult,
    ProviderInvocationRequest,
)


class ProviderAdapter(Protocol):
    """Provider protocol mechanics only; routing/policy/effects remain outside this port."""

    async def invoke(self, request: ProviderInvocationRequest) -> ProviderAttemptResult: ...
