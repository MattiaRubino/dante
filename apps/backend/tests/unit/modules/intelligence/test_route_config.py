"""Unit acceptance for immutable route-config identity and loading semantics."""

import json
from hashlib import sha256
from pathlib import Path

import pytest

from dante.modules.intelligence.contracts.route_config import (
    RouteConfigIdentity,
    RouteConfigSnapshot,
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


def test_repository_pre_provider_revision_is_disabled_and_bound_to_exact_bytes() -> None:
    snapshot = load_route_config(_REVISIONS_ROOT, "pre-provider-v1")
    artifact_path = _REVISIONS_ROOT / "pre-provider-v1.json"
    artifact_bytes = artifact_path.read_bytes()

    assert snapshot.identity.revision == "pre-provider-v1"
    assert snapshot.identity.content_sha256 == sha256(artifact_bytes).hexdigest()
    assert snapshot.artifact_bytes == artifact_bytes
    assert snapshot.document.model_targets == ()
    assert snapshot.document.provider_bindings == ()
    assert snapshot.document.feature_modes == ("ask_dante:disabled",)


def test_semantically_equal_json_with_different_bytes_has_different_identity(tmp_path: Path) -> None:
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


def test_loader_rejects_unsafe_revision_before_path_resolution(tmp_path: Path) -> None:
    with pytest.raises(RouteConfigLoadError, match="invalid route-config identifier"):
        load_route_config(tmp_path, "../escape")


def test_loader_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    root = tmp_path / "revisions"
    path = _write_artifact(root, "test-v1", _artifact())
    text = path.read_text(encoding="utf-8")
    duplicate = text.replace(
        "\"schema_version\": 1,",
        "\"schema_version\": 1,\n  \"schema_version\": 1,",
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
