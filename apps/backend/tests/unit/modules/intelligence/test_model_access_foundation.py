"""Foundation-level acceptance for ModelAccess cancellation and process composition."""

from __future__ import annotations

from pathlib import Path

import pytest

from dante.bootstrap.intelligence import create_development_model_access_runtime
from dante.modules.intelligence.adapters.outbound.model.gemini_interactions import (
    GEMINI_INTERACTIONS_BINDING_REF,
    GEMINI_INTERACTIONS_ROUTE_REVISION,
)
from dante.modules.intelligence.application.cancellation import ModelCancellationSignal

_BACKEND_ROOT = Path(__file__).resolve().parents[4]
_REVISIONS_ROOT = _BACKEND_ROOT / "config" / "intelligence" / "revisions"


@pytest.mark.asyncio
async def test_model_cancellation_signal_is_idempotent_and_waitable() -> None:
    signal = ModelCancellationSignal()

    assert signal.cancelled is False
    assert signal.cancel() is True
    assert signal.cancel() is False
    await signal.wait()
    assert signal.cancelled is True


@pytest.mark.asyncio
async def test_development_composition_uses_explicit_current_route_and_closes() -> None:
    resources = create_development_model_access_runtime(
        api_key="synthetic-not-used",
        revisions_root=_REVISIONS_ROOT,
        route_revision=GEMINI_INTERACTIONS_ROUTE_REVISION,
    )
    try:
        assert resources.runtime.route_config.identity.revision == GEMINI_INTERACTIONS_ROUTE_REVISION
        active_bindings = {
            route.champion_binding_ref
            for route in resources.runtime.route_config.document.target_routes
            if route.champion_binding_ref is not None
        }
        assert active_bindings == {GEMINI_INTERACTIONS_BINDING_REF}
    finally:
        await resources.close()


def test_development_composition_rejects_historical_route_binding() -> None:
    with pytest.raises(ValueError, match="schema v3|not supported"):
        create_development_model_access_runtime(
            api_key="synthetic-not-used",
            revisions_root=_REVISIONS_ROOT,
            route_revision="gemini-flash-dev-v1",
        )
