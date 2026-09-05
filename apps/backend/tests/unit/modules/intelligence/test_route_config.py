"""Unit acceptance for immutable route-config identity and loading semantics."""

import json
from hashlib import sha256
from pathlib import Path

import pytest

from dante.modules.intelligence.contracts.route_config import (
    ProviderBindingState,
    ReasoningLevel,
    RouteConfigIdentity,
    RouteConfigSnapshot,
    RouteTargetState,
)
from dante.modules.intelligence.route_config import RouteConfigLoadError, load_route_config

_BACKEND_ROOT = Path(__file__).resolve().parents[4]
_REVISIONS_ROOT = _BACKEND_ROOT / "config" / "intelligence" / "revisions"


def _artifact(revision: str = "test-v1") -> dict[str, object]:
    return {
        "schema_version": 1,
        "revision": revision,
        "model_targets": [],
        "harness_profiles": [],
        "provider_bindings": [],
        "route_policies": [],
        "feature_modes": ["ask_dante:disabled"],
        "qualification_requirements": [],
        "control_profiles": [],
        "retry_profiles": [],
        "fallback_profiles": [],
        "resource_profiles": [],
        "security_profiles": [],
        "rollout_profiles": [],
    }


def _write_artifact(root: Path, revision: str, document: dict[str, object]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"{revision}.json"
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return path


def test_repository_revision_is_disabled_and_exact_byte_bound() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "pre-provider-v1")
    artifact_path = _REVISIONS_ROOT / "pre-provider-v1.json"
    artifact_bytes = artifact_path.read_bytes()

    assert snapshot.identity.revision == "pre-provider-v1"
    assert snapshot.identity.content_sha256 == sha256(artifact_bytes).hexdigest()
    assert snapshot.artifact_bytes == artifact_bytes
    assert snapshot.document.model_targets == ()
    assert snapshot.document.provider_bindings == ()
    assert snapshot.document.feature_modes == ("ask_dante:disabled",)


def test_openai_candidate_revision_is_inactive_and_qualification_only() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "openai-terra-candidate-v1")

    assert snapshot.document.model_targets == ("ask-readonly-terra-v1",)
    assert snapshot.document.provider_bindings == ("openai-responses-terra-candidate-v1",)
    assert "ask_dante:disabled" in snapshot.document.feature_modes
    assert "binding:inactive" in snapshot.document.rollout_profiles
    assert "production:off" in snapshot.document.rollout_profiles
    assert "private-data:ineligible" in snapshot.document.security_profiles
    assert "store:false" in snapshot.document.security_profiles
    assert "provider-sdk:auto-retry-off" in snapshot.document.retry_profiles
    assert "provider-fallback:off" in snapshot.document.fallback_profiles


def test_historical_gemini_schema_v2_remains_loadable() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v1")

    assert snapshot.document.schema_version == 2
    binding = snapshot.document.provider_binding_definitions[0]
    assert binding.ref == "google-gemini-interactions-flash-v1"
    assert binding.api_revision is None
    assert binding.service_tier is None


def test_gemini_schema_v3_materializes_exact_development_binding() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "gemini-flash-dev-v2")

    assert snapshot.document.schema_version == 3
    routes = {route.target_ref: route for route in snapshot.document.target_routes}
    assert routes["structured_interpretation"].state is RouteTargetState.ACTIVE
    assert routes["general_reasoning"].state is RouteTargetState.ACTIVE
    assert routes["deep_reasoning"].state is RouteTargetState.DORMANT
    assert routes["deep_reasoning"].champion_binding_ref is None

    harness = snapshot.document.harness_definitions[0]
    assert harness.reasoning_level is ReasoningLevel.LOW
    assert harness.timeout_seconds == 30

    binding = snapshot.document.provider_binding_definitions[0]
    assert binding.ref == "google-gemini-interactions-flash-v2"
    assert binding.model == "gemini-3.8-flash"
    assert binding.protocol_family == "gemini-interactions-v1beta"
    assert binding.api_revision == "2026-05-20"
    assert binding.service_tier == "standard"
    assert binding.versioning_posture == "stable-model-id-no-snapshot"
    assert binding.data_zone == "global"
    assert binding.retention_mode == "store-false"
    assert binding.state is ProviderBindingState.DEVELOPMENT
    assert "private-data:ineligible" in binding.security_profiles
    assert "production:off" in snapshot.document.rollout_profiles


def test_schema_v3_rejects_missing_exact_binding_identity(tmp_path: Path) -> None:
    source = json.loads(
        (_REVISIONS_ROOT / "gemini-flash-dev-v2.json").read_text(encoding="utf-8")
    )
    assert isinstance(source, dict)
    source["revision"] = "broken-v3"
    bindings = source["provider_binding_definitions"]
    assert isinstance(bindings, list)
    binding = bindings[0]
    assert isinstance(binding, dict)
    del binding["service_tier"]
    root = tmp_path / "revisions"
    _write_artifact(root, "broken-v3", source)

    with pytest.raises(RouteConfigLoadError, match="missing required fields"):
        load_route_config(root, "broken-v3")


def test_equal_json_with_different_bytes_has_different_identity(tmp_path: Path) -> None:
    root = tmp_path / "revisions"
    root.mkdir()
    path = root / "test-v1.json"
    document = _artifact()

    path.write_text(
        json.dumps(document, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    first = load_route_config(root, "test-v1")

    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    second = load_route_config(root, "test-v1")

    assert first.document == second.document
    assert first.identity.content_sha256 != second.identity.content_sha256
    assert first.artifact_bytes != second.artifact_bytes


def test_unsafe_revision_is_rejected_before_path_resolution(tmp_path: Path) -> None:
    with pytest.raises(RouteConfigLoadError, match="invalid route-config identifier"):
        load_route_config(tmp_path, "../escape")


def test_identity_rejects_unsafe_revision() -> None:
    with pytest.raises(ValueError, match="invalid route-config identifier"):
        RouteConfigIdentity(revision="../escape", content_sha256="0" * 64)


def test_loader_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    root = tmp_path / "revisions"
    path = _write_artifact(root, "test-v1", _artifact())
    text = path.read_text(encoding="utf-8")
    duplicate = text.replace(
        '"schema_version": 1,',
        '"schema_version": 1,\n  "schema_version": 1,',
        1,
    )
    path.write_text(duplicate, encoding="utf-8")

    with pytest.raises(RouteConfigLoadError, match="duplicate JSON key"):
        load_route_config(root, "test-v1")


def test_loader_rejects_unknown_behavior_fields(tmp_path: Path) -> None:
    root = tmp_path / "revisions"
    document = _artifact()
    document["undeclared_behavior"] = "forbidden"
    _write_artifact(root, "test-v1", document)

    with pytest.raises(RouteConfigLoadError, match="unknown fields"):
        load_route_config(root, "test-v1")


def test_loader_rejects_artifact_revision_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "revisions"
    _write_artifact(root, "selected-v1", _artifact(revision="different-v1"))

    with pytest.raises(RouteConfigLoadError, match="must match the selected logical revision"):
        load_route_config(root, "selected-v1")


def test_snapshot_rejects_identity_not_bound_to_artifact_bytes() -> None:
    loaded = load_route_config(_REVISIONS_ROOT, "pre-provider-v1")
    wrong_identity = RouteConfigIdentity(
        revision=loaded.identity.revision,
        content_sha256="0" * 64,
    )

    with pytest.raises(ValueError, match="do not match RouteConfigIdentity"):
        RouteConfigSnapshot(
            identity=wrong_identity,
            document=loaded.document,
            artifact_bytes=loaded.artifact_bytes,
        )
