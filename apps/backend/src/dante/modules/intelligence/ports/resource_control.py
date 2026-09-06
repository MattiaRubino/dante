"""Request-local resource-control consumer port for DANTE Intelligence."""

from typing import Protocol

from dante.modules.intelligence.contracts.resource import (
    ResourceAdmission,
    ResourceAdmissionRequest,
    ResourceEstimate,
    ResourceEstimateRequest,
    ResourceSettlement,
    ResourceSettlementRequest,
)


class ResourceControlPort(Protocol):
    """Estimate, admit and settle bounded request-local resource use."""

    async def estimate(self, request: ResourceEstimateRequest) -> ResourceEstimate: ...

    async def admit(self, request: ResourceAdmissionRequest) -> ResourceAdmission: ...

    async def settle(self, request: ResourceSettlementRequest) -> ResourceSettlement: ...
