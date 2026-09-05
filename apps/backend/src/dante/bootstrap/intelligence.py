"""Process composition for the development ModelAccess runtime.

This is the only production-shaped composition root that knows which concrete provider adapter backs
the accepted development route. Application/domain code remains provider-neutral. The runtime is
not attached to FastAPI lifecycle until a real product integration seam is activated.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dante.modules.intelligence.adapters.outbound.model.gemini_http import (
    GeminiInteractionsHttpTransport,
)
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_BINDING_REF,
    GeminiInteractionsAdapter,
)
from dante.modules.intelligence.application.model_access import ModelAccessRuntime
from dante.modules.intelligence.contracts.route_config import ProviderBindingState
from dante.modules.intelligence.ports.runtime_evidence import RuntimeEvidencePort
from dante.modules.intelligence.route_config import load_route_config


@dataclass(slots=True)
class ModelAccessRuntimeResources:
    """Process-owned ModelAccess runtime plus concrete transport lifecycle."""

    runtime: ModelAccessRuntime
    _gemini_transport: GeminiInteractionsHttpTransport

    async def close(self) -> None:
        await self._gemini_transport.close()


def create_development_model_access_runtime(
    *,
    api_key: str,
    revisions_root: Path,
    route_revision: str,
    evidence: RuntimeEvidencePort | None = None,
) -> ModelAccessRuntimeResources:
    """Compose one explicitly selected development route without activating a product endpoint.

    The route revision is a deployment/composition selector. Provider/model behavior still comes
    from the immutable route artifact; unsupported or historical bindings fail closed here instead
    of silently falling back to hard-coded provider behavior.
    """
    snapshot = load_route_config(revisions_root, route_revision)
    if snapshot.document.schema_version < 3:
        raise ValueError("development ModelAccess composition requires route-config schema v3")

    active_binding_refs = {
        route.champion_binding_ref
        for route in snapshot.document.target_routes
        if route.champion_binding_ref is not None
    }
    if active_binding_refs != {GEMINI_INTERACTIONS_BINDING_REF}:
        raise ValueError("selected development route is not supported by this composition root")

    binding = next(
        definition
        for definition in snapshot.document.provider_binding_definitions
        if definition.ref == GEMINI_INTERACTIONS_BINDING_REF
    )
    if binding.state is not ProviderBindingState.DEVELOPMENT:
        raise ValueError("development composition requires a DEVELOPMENT provider binding")

    transport = GeminiInteractionsHttpTransport(api_key)
    adapter = GeminiInteractionsAdapter(transport)
    runtime = ModelAccessRuntime(
        snapshot,
        {GEMINI_INTERACTIONS_BINDING_REF: adapter},
        evidence=evidence,
    )
    return ModelAccessRuntimeResources(runtime=runtime, _gemini_transport=transport)
