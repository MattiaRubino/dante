"""Public application protocol for DANTE Global Search."""

from typing import Protocol

from dante.modules.search.contracts import (
    NavigationExecutionRequest,
    NavigationResult,
    SearchExecutionRequest,
    SearchResult,
)


class SearchService(Protocol):
    """Application-owned Search surface consumed by inbound adapters/Intelligence."""

    async def search(self, request: SearchExecutionRequest) -> SearchResult:
        """Execute permission-safe Global Search."""
        ...

    async def resolve_navigation(
        self,
        request: NavigationExecutionRequest,
    ) -> NavigationResult:
        """Resolve an eligible Search target to an owner-routable reference."""
        ...
