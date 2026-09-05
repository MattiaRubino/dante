"""Application-owned ModelAccess port; provider SDK/protocols stay behind adapters."""

from typing import Protocol

from dante.modules.intelligence.contracts.model_access import (
    ModelInvocationRequest,
    ModelInvocationResult,
)


class ModelAccessPort(Protocol):
    """Execute one logical cognition request through DANTE-owned routing."""

    async def invoke(self, request: ModelInvocationRequest) -> ModelInvocationResult: ...
