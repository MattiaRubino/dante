"""Fail-closed loader for immutable DANTE Intelligence route configuration revisions."""

from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path
from typing import Never, cast

from dante.modules.intelligence.contracts.route_config import (
    RouteConfigDocument,
    RouteConfigIdentity,
    RouteConfigSnapshot,
)

_MAX_ARTIFACT_BYTES = 1024 * 1024
_REVISION_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_EXPECTED_FIELDS = frozenset(
    {
        "schema_version",
        "revision",
        "model_targets",
        "harness_profiles",
        "provider_bindings",
        "route_policies",
        "feature_modes",
        "qualification_requirements",
        "control_profiles",
        "retry_profiles",
        "fallback_profiles",
        "resource_profiles",
        "security_profiles",
        "rollout_profiles",
    }
)


class RouteConfigLoadError(ValueError):
    """Raised when a route configuration artifact cannot be safely materialized."""


def _reject_json_constant(value: str) -> Never:
    raise RouteConfigLoadError(f"non-standard JSON constant is forbidden: {value}")


def _reject_duplicate_object_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise RouteConfigLoadError(f"duplicate JSON key is forbidden: {key}")
        result[key] = value
    return result


def _parse_text_list(document: dict[str, object], *, field: str) -> tuple[str, ...]:
    value = document[field]
    if not isinstance(value, list):
        raise RouteConfigLoadError(f"{field} must be a JSON array")

    parsed: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise RouteConfigLoadError(f"{field} entries must be non-empty strings")
        parsed.append(item)
    if len(parsed) != len(set(parsed)):
        raise RouteConfigLoadError(f"{field} entries must be unique")
    return tuple(parsed)


def _parse_document(artifact_bytes: bytes) -> RouteConfigDocument:
    try:
        text = artifact_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RouteConfigLoadError("route config artifact must be UTF-8") from exc

    try:
        loaded = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_object_keys,
            parse_constant=_reject_json_constant,
        )
    except json.JSONDecodeError as exc:
        raise RouteConfigLoadError("route config artifact must be valid JSON") from exc

    if not isinstance(loaded, dict):
        raise RouteConfigLoadError("route config artifact root must be a JSON object")
    document = cast(dict[str, object], loaded)

    actual_fields = frozenset(document)
    missing_fields = _EXPECTED_FIELDS - actual_fields
    unknown_fields = actual_fields - _EXPECTED_FIELDS
    if missing_fields:
        raise RouteConfigLoadError(
            f"route config is missing required fields: {sorted(missing_fields)}"
        )
    if unknown_fields:
        raise RouteConfigLoadError(
            f"route config contains unknown fields: {sorted(unknown_fields)}"
        )

    schema_version = document["schema_version"]
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise RouteConfigLoadError("schema_version must be an integer")
    revision = document["revision"]
    if not isinstance(revision, str) or not revision.strip():
        raise RouteConfigLoadError("revision must be a non-empty string")

    try:
        return RouteConfigDocument(
            schema_version=schema_version,
            revision=revision,
            model_targets=_parse_text_list(document, field="model_targets"),
            harness_profiles=_parse_text_list(document, field="harness_profiles"),
            provider_bindings=_parse_text_list(document, field="provider_bindings"),
            route_policies=_parse_text_list(document, field="route_policies"),
            feature_modes=_parse_text_list(document, field="feature_modes"),
            qualification_requirements=_parse_text_list(
                document, field="qualification_requirements"
            ),
            control_profiles=_parse_text_list(document, field="control_profiles"),
            retry_profiles=_parse_text_list(document, field="retry_profiles"),
            fallback_profiles=_parse_text_list(document, field="fallback_profiles"),
            resource_profiles=_parse_text_list(document, field="resource_profiles"),
            security_profiles=_parse_text_list(document, field="security_profiles"),
            rollout_profiles=_parse_text_list(document, field="rollout_profiles"),
        )
    except (TypeError, ValueError) as exc:
        raise RouteConfigLoadError(str(exc)) from exc


def load_route_config(revisions_root: Path, revision: str) -> RouteConfigSnapshot:
    """Load one exact revision without allowing path escape or semantic rewriting."""
    if _REVISION_PATTERN.fullmatch(revision) is None:
        raise RouteConfigLoadError("revision has an invalid route-config identifier")

    try:
        root = revisions_root.resolve(strict=True)
        candidate = (root / f"{revision}.json").resolve(strict=True)
    except OSError as exc:
        raise RouteConfigLoadError("route config revision could not be resolved") from exc

    if not root.is_dir():
        raise RouteConfigLoadError("route config revisions root must be a directory")
    if candidate.parent != root or not candidate.is_file():
        raise RouteConfigLoadError("route config revision must resolve inside the revisions root")

    try:
        artifact_bytes = candidate.read_bytes()
    except OSError as exc:
        raise RouteConfigLoadError("route config revision could not be read") from exc

    if not artifact_bytes:
        raise RouteConfigLoadError("route config artifact must not be empty")
    if len(artifact_bytes) > _MAX_ARTIFACT_BYTES:
        raise RouteConfigLoadError("route config artifact exceeds the bounded size limit")

    document = _parse_document(artifact_bytes)
    if document.revision != revision:
        raise RouteConfigLoadError("artifact revision must match the selected logical revision")

    identity = RouteConfigIdentity(
        revision=revision,
        content_sha256=sha256(artifact_bytes).hexdigest(),
    )
    return RouteConfigSnapshot(
        identity=identity,
        document=document,
        artifact_bytes=artifact_bytes,
    )
