"""Application-owned ModelAccess port; provider SDK/protocols stay behind adapters."""

from typing import Protocol

from dante.modules.intelligence.contracts.model_access import (
    ModelInvocationRequest,
    ModelInvocationResult,
)


class CancellationSignal(Protocol):
    """Request-owned cancellation signal with no provider semantics."""

    @property
    def cancelled(self) -> bool: ...

    async def wait(self) -> None:
        """Return once cancellation has been requested."""
        ...


class ModelAccessPort(Protocol):
    """Execute one logical cognition request through DANTE-owned routing."""

    async def invoke(
        self,
        request: ModelInvocationRequest,
        cancellation: CancellationSignal | None = None,
    ) -> ModelInvocationResult: ...
