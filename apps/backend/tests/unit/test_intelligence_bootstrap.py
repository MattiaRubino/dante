"""Unit acceptance for provider-specific ModelAccess bootstrap composition."""

from pathlib import Path

import pytest

from dante.bootstrap.intelligence import create_development_model_access_runtime
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
)

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_REVISIONS_ROOT = _BACKEND_ROOT / "config" / "intelligence" / "revisions"


@pytest.mark.asyncio
async def test_development_model_access_composition_loads_exact_route_without_network_io() -> None:
    resources = create_development_model_access_runtime(
        api_key="synthetic-secret-not-used",
        revisions_root=_REVISIONS_ROOT,
    )
    try:
        snapshot = resources.runtime.route_config
        assert snapshot.identity.revision == GEMINI_INTERACTIONS_ROUTE_REVISION
        assert {
            route.champion_binding_ref
            for route in snapshot.document.target_routes
            if route.champion_binding_ref is not None
        } == {GEMINI_INTERACTIONS_BINDING_REF}
    finally:
        await resources.close()


def test_development_model_access_composition_rejects_empty_secret() -> None:
    with pytest.raises(ValueError, match="Gemini API key must be non-empty"):
        create_development_model_access_runtime(
            api_key="",
            revisions_root=_REVISIONS_ROOT,
        )
