"""Fail-closed loader for immutable DANTE Intelligence route configuration revisions."""

from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path
from typing import Never, cast

from dante.modules.intelligence.contracts.route_config import (
    HarnessProfileDefinition,
    ProviderBindingDefinition,
    ProviderBindingState,
    ReasoningLevel,
    RouteConfigDocument,
    RouteConfigIdentity,
    RouteConfigSnapshot,
    RouteTargetState,
    TargetRouteDefinition,
)

_MAX_ARTIFACT_BYTES = 1024 * 1024
_REVISION_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_COMMON_FIELDS = frozenset(
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
_V2_FIELDS = _COMMON_FIELDS | frozenset(
    {"target_routes", "harness_definitions", "provider_binding_definitions"}
)
_TARGET_ROUTE_FIELDS = frozenset(
    {
        "target_ref",
        "state",
        "champion_binding_ref",
        "harness_profile_ref",
        "challenger_binding_refs",
        "fallback_binding_refs",
    }
)
_HARNESS_FIELDS = frozenset(
    {"ref", "reasoning_level", "max_output_tokens", "timeout_seconds", "feature_modes"}
)
_BINDING_FIELDS = frozenset(
    {
        "ref",
        "provider",
        "serving_platform",
        "protocol_family",
        "endpoint",
        "model",
        "region",
        "state",
        "capabilities",
        "security_profiles",
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


def _require_exact_fields(document: dict[str, object], expected: frozenset[str], *, name: str) -> None:
    actual = frozenset(document)
    missing = expected - actual
    unknown = actual - expected
    if missing:
        raise RouteConfigLoadError(f"{name} is missing required fields: {sorted(missing)}")
    if unknown:
        raise RouteConfigLoadError(f"{name} contains unknown fields: {sorted(unknown)}")


def _parse_text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RouteConfigLoadError(f"{field} must be a non-empty string")
    return value


def _parse_optional_text(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return _parse_text(value, field=field)


def _parse_text_list_value(value: object, *, field: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise RouteConfigLoadError(f"{field} must be a JSON array")
    parsed = tuple(_parse_text(item, field=f"{field} entry") for item in value)
    if len(parsed) != len(set(parsed)):
        raise RouteConfigLoadError(f"{field} entries must be unique")
    return parsed


def _parse_text_list(document: dict[str, object], *, field: str) -> tuple[str, ...]:
    return _parse_text_list_value(document[field], field=field)


def _parse_target_routes(value: object) -> tuple[TargetRouteDefinition, ...]:
    if not isinstance(value, list):
        raise RouteConfigLoadError("target_routes must be a JSON array")
    routes: list[TargetRouteDefinition] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise RouteConfigLoadError("target_routes entries must be JSON objects")
        document = cast(dict[str, object], item)
        _require_exact_fields(document, _TARGET_ROUTE_FIELDS, name=f"target_routes[{index}]")
        try:
            routes.append(
                TargetRouteDefinition(
                    target_ref=_parse_text(document["target_ref"], field="target_ref"),
                    state=RouteTargetState(_parse_text(document["state"], field="state")),
                    champion_binding_ref=_parse_optional_text(
                        document["champion_binding_ref"], field="champion_binding_ref"
                    ),
                    harness_profile_ref=_parse_optional_text(
                        document["harness_profile_ref"], field="harness_profile_ref"
                    ),
                    challenger_binding_refs=_parse_text_list_value(
                        document["challenger_binding_refs"], field="challenger_binding_refs"
                    ),
                    fallback_binding_refs=_parse_text_list_value(
                        document["fallback_binding_refs"], field="fallback_binding_refs"
                    ),
                )
            )
        except ValueError as exc:
            raise RouteConfigLoadError(str(exc)) from exc
    return tuple(routes)


def _parse_harness_definitions(value: object) -> tuple[HarnessProfileDefinition, ...]:
    if not isinstance(value, list):
        raise RouteConfigLoadError("harness_definitions must be a JSON array")
    profiles: list[HarnessProfileDefinition] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise RouteConfigLoadError("harness_definitions entries must be JSON objects")
        document = cast(dict[str, object], item)
        _require_exact_fields(document, _HARNESS_FIELDS, name=f"harness_definitions[{index}]")
        max_output_tokens = document["max_output_tokens"]
        timeout_seconds = document["timeout_seconds"]
        if isinstance(max_output_tokens, bool) or not isinstance(max_output_tokens, int):
            raise RouteConfigLoadError("harness max_output_tokens must be an integer")
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
            raise RouteConfigLoadError("harness timeout_seconds must be numeric")
        try:
            profiles.append(
                HarnessProfileDefinition(
                    ref=_parse_text(document["ref"], field="harness ref"),
                    reasoning_level=ReasoningLevel(
                        _parse_text(document["reasoning_level"], field="reasoning_level")
                    ),
                    max_output_tokens=max_output_tokens,
                    timeout_seconds=float(timeout_seconds),
                    feature_modes=_parse_text_list_value(
                        document["feature_modes"], field="harness feature_modes"
                    ),
                )
            )
        except ValueError as exc:
            raise RouteConfigLoadError(str(exc)) from exc
    return tuple(profiles)


def _parse_binding_definitions(value: object) -> tuple[ProviderBindingDefinition, ...]:
    if not isinstance(value, list):
        raise RouteConfigLoadError("provider_binding_definitions must be a JSON array")
    bindings: list[ProviderBindingDefinition] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise RouteConfigLoadError("provider_binding_definitions entries must be JSON objects")
        document = cast(dict[str, object], item)
        _require_exact_fields(
            document,
            _BINDING_FIELDS,
            name=f"provider_binding_definitions[{index}]",
        )
        try:
            bindings.append(
                ProviderBindingDefinition(
                    ref=_parse_text(document["ref"], field="binding ref"),
                    provider=_parse_text(document["provider"], field="provider"),
                    serving_platform=_parse_text(
                        document["serving_platform"], field="serving_platform"
                    ),
                    protocol_family=_parse_text(
                        document["protocol_family"], field="protocol_family"
                    ),
                    endpoint=_parse_text(document["endpoint"], field="endpoint"),
                    model=_parse_text(document["model"], field="model"),
                    region=_parse_text(document["region"], field="region"),
                    state=ProviderBindingState(
                        _parse_text(document["state"], field="binding state")
                    ),
                    capabilities=_parse_text_list_value(
                        document["capabilities"], field="binding capabilities"
                    ),
                    security_profiles=_parse_text_list_value(
                        document["security_profiles"], field="binding security_profiles"
                    ),
                )
            )
        except ValueError as exc:
            raise RouteConfigLoadError(str(exc)) from exc
    return tuple(bindings)


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

    schema_version = document.get("schema_version")
    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise RouteConfigLoadError("schema_version must be an integer")
    if schema_version == 1:
        expected_fields = _COMMON_FIELDS
    elif schema_version == 2:
        expected_fields = _V2_FIELDS
    else:
        raise RouteConfigLoadError(f"unsupported route config schema_version: {schema_version}")
    _require_exact_fields(document, expected_fields, name="route config")

    revision = _parse_text(document["revision"], field="revision")
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
            target_routes=(
                _parse_target_routes(document["target_routes"]) if schema_version == 2 else ()
            ),
            harness_definitions=(
                _parse_harness_definitions(document["harness_definitions"])
                if schema_version == 2
                else ()
            ),
            provider_binding_definitions=(
                _parse_binding_definitions(document["provider_binding_definitions"])
                if schema_version == 2
                else ()
            ),
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
