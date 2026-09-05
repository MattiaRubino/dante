"""Provider-neutral route configuration identity and immutable snapshot contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from urllib.parse import urlparse

_SUPPORTED_SCHEMA_VERSIONS = frozenset({1, 2, 3})
_HEX_DIGITS = frozenset("0123456789abcdef")
_REVISION_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


class RouteTargetState(StrEnum):
    ACTIVE = "active"
    DORMANT = "dormant"
    DISABLED = "disabled"


class ProviderBindingState(StrEnum):
    DEVELOPMENT = "development"
    INACTIVE = "inactive"
    ACTIVE = "active"


class ReasoningLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_revision(value: str) -> None:
    _require_text(value, name="revision")
    if _REVISION_PATTERN.fullmatch(value) is None:
        raise ValueError("revision has an invalid route-config identifier")


def _require_unique_texts(values: tuple[str, ...], *, name: str) -> None:
    for value in values:
        _require_text(value, name=name)
    if len(values) != len(set(values)):
        raise ValueError(f"{name} entries must be unique")


@dataclass(frozen=True, slots=True)
class TargetRouteDefinition:
    """Deterministic route for one logical ModelTarget in one revision."""

    target_ref: str
    state: RouteTargetState
    champion_binding_ref: str | None = None
    harness_profile_ref: str | None = None
    challenger_binding_refs: tuple[str, ...] = ()
    fallback_binding_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.target_ref, name="target_ref")
        _require_unique_texts(
            self.challenger_binding_refs, name="challenger_binding_refs"
        )
        _require_unique_texts(self.fallback_binding_refs, name="fallback_binding_refs")
        if self.state is RouteTargetState.ACTIVE:
            if self.champion_binding_ref is None or self.harness_profile_ref is None:
                raise ValueError("active target route requires champion binding and harness")
            _require_text(self.champion_binding_ref, name="champion_binding_ref")
            _require_text(self.harness_profile_ref, name="harness_profile_ref")
            if self.champion_binding_ref in self.challenger_binding_refs:
                raise ValueError("champion binding cannot also be a challenger")
            if self.champion_binding_ref in self.fallback_binding_refs:
                raise ValueError("champion binding cannot also be a fallback")
            return
        if self.champion_binding_ref is not None or self.harness_profile_ref is not None:
            raise ValueError("dormant/disabled target route cannot select champion/harness")
        if self.challenger_binding_refs or self.fallback_binding_refs:
            raise ValueError("dormant/disabled target route cannot select challengers/fallbacks")


@dataclass(frozen=True, slots=True)
class HarnessProfileDefinition:
    """Behavior-bearing provider-neutral model harness profile."""

    ref: str
    reasoning_level: ReasoningLevel
    max_output_tokens: int
    timeout_seconds: float
    feature_modes: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.ref, name="harness ref")
        if self.max_output_tokens <= 0:
            raise ValueError("harness max_output_tokens must be positive")
        if self.timeout_seconds <= 0 or self.timeout_seconds > 300:
            raise ValueError("harness timeout_seconds must be >0 and <=300")
        _require_unique_texts(self.feature_modes, name="harness feature_modes")


@dataclass(frozen=True, slots=True)
class ProviderBindingDefinition:
    """Exact provider/model/protocol identity eligible for deterministic routing."""

    ref: str
    provider: str
    serving_platform: str
    protocol_family: str
    endpoint: str
    model: str
    region: str
    state: ProviderBindingState
    capabilities: tuple[str, ...]
    security_profiles: tuple[str, ...]
    api_revision: str | None = None
    service_tier: str | None = None
    model_version: str | None = None
    versioning_posture: str | None = None
    data_zone: str | None = None
    retention_mode: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("binding ref", self.ref),
            ("provider", self.provider),
            ("serving_platform", self.serving_platform),
            ("protocol_family", self.protocol_family),
            ("endpoint", self.endpoint),
            ("model", self.model),
            ("region", self.region),
        ):
            _require_text(value, name=name)
        parsed = urlparse(self.endpoint)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("provider binding endpoint must be an absolute HTTPS URL")
        _require_unique_texts(self.capabilities, name="binding capabilities")
        _require_unique_texts(self.security_profiles, name="binding security_profiles")
        for name, optional_value in (
            ("api_revision", self.api_revision),
            ("service_tier", self.service_tier),
            ("model_version", self.model_version),
            ("versioning_posture", self.versioning_posture),
            ("data_zone", self.data_zone),
            ("retention_mode", self.retention_mode),
        ):
            if optional_value is not None:
                _require_text(optional_value, name=name)


@dataclass(frozen=True, slots=True)
class RouteConfigDocument:
    """Typed behavior-bearing route configuration document for one logical revision."""

    schema_version: int
    revision: str
    model_targets: tuple[str, ...]
    harness_profiles: tuple[str, ...]
    provider_bindings: tuple[str, ...]
    route_policies: tuple[str, ...]
    feature_modes: tuple[str, ...]
    qualification_requirements: tuple[str, ...]
    control_profiles: tuple[str, ...]
    retry_profiles: tuple[str, ...]
    fallback_profiles: tuple[str, ...]
    resource_profiles: tuple[str, ...]
    security_profiles: tuple[str, ...]
    rollout_profiles: tuple[str, ...]
    target_routes: tuple[TargetRouteDefinition, ...] = ()
    harness_definitions: tuple[HarnessProfileDefinition, ...] = ()
    provider_binding_definitions: tuple[ProviderBindingDefinition, ...] = ()

    def __post_init__(self) -> None:
        if self.schema_version not in _SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(
                f"unsupported route config schema_version: {self.schema_version}"
            )
        _require_revision(self.revision)

        for name, values in (
            ("model_targets", self.model_targets),
            ("harness_profiles", self.harness_profiles),
            ("provider_bindings", self.provider_bindings),
            ("route_policies", self.route_policies),
            ("feature_modes", self.feature_modes),
            ("qualification_requirements", self.qualification_requirements),
            ("control_profiles", self.control_profiles),
            ("retry_profiles", self.retry_profiles),
            ("fallback_profiles", self.fallback_profiles),
            ("resource_profiles", self.resource_profiles),
            ("security_profiles", self.security_profiles),
            ("rollout_profiles", self.rollout_profiles),
        ):
            _require_unique_texts(values, name=name)

        if self.schema_version == 1:
            if (
                self.target_routes
                or self.harness_definitions
                or self.provider_binding_definitions
            ):
                raise ValueError("schema v1 cannot contain typed route definitions")
            return

        target_refs = tuple(route.target_ref for route in self.target_routes)
        harness_refs = tuple(profile.ref for profile in self.harness_definitions)
        binding_refs = tuple(
            binding.ref for binding in self.provider_binding_definitions
        )
        for name, values in (
            ("target route refs", target_refs),
            ("harness definition refs", harness_refs),
            ("provider binding definition refs", binding_refs),
        ):
            _require_unique_texts(values, name=name)

        if set(target_refs) != set(self.model_targets):
            raise ValueError("typed target_routes must exactly cover model_targets")
        if set(harness_refs) != set(self.harness_profiles):
            raise ValueError("typed harness_definitions must exactly cover harness_profiles")
        if set(binding_refs) != set(self.provider_bindings):
            raise ValueError(
                "typed provider_binding_definitions must exactly cover provider_bindings"
            )

        known_harnesses = set(harness_refs)
        known_bindings = set(binding_refs)
        global_feature_modes = set(self.feature_modes)
        global_security_profiles = set(self.security_profiles)
        for profile in self.harness_definitions:
            if not set(profile.feature_modes).issubset(global_feature_modes):
                raise ValueError("harness feature_modes must be declared by route config")
        for binding in self.provider_binding_definitions:
            if not set(binding.security_profiles).issubset(global_security_profiles):
                raise ValueError("binding security_profiles must be declared by route config")
            if self.schema_version >= 3:
                required_exact_identity = (
                    binding.api_revision,
                    binding.service_tier,
                    binding.versioning_posture,
                    binding.data_zone,
                    binding.retention_mode,
                )
                if any(value is None for value in required_exact_identity):
                    raise ValueError(
                        "schema v3 provider binding requires api_revision, service_tier, "
                        "versioning_posture, data_zone and retention_mode"
                    )
        for route in self.target_routes:
            if route.state is not RouteTargetState.ACTIVE:
                continue
            champion_binding_ref = route.champion_binding_ref
            harness_profile_ref = route.harness_profile_ref
            if champion_binding_ref is None or harness_profile_ref is None:
                raise ValueError("active target route requires champion binding and harness")
            if champion_binding_ref not in known_bindings:
                raise ValueError("target route references unknown champion binding")
            if harness_profile_ref not in known_harnesses:
                raise ValueError("target route references unknown harness profile")
            if any(
                ref not in known_bindings for ref in route.challenger_binding_refs
            ):
                raise ValueError("target route references unknown challenger binding")
            if any(ref not in known_bindings for ref in route.fallback_binding_refs):
                raise ValueError("target route references unknown fallback binding")


@dataclass(frozen=True, slots=True)
class RouteConfigIdentity:
    """Material identity of one exact behavior-bearing route config artifact."""

    revision: str
    content_sha256: str

    def __post_init__(self) -> None:
        _require_revision(self.revision)
        if len(self.content_sha256) != 64 or any(
            character not in _HEX_DIGITS for character in self.content_sha256
        ):
            raise ValueError("content_sha256 must be a lowercase SHA-256 hex digest")


@dataclass(frozen=True, slots=True)
class RouteConfigSnapshot:
    """Immutable loaded snapshot bound to the exact validated artifact bytes."""

    identity: RouteConfigIdentity
    document: RouteConfigDocument
    artifact_bytes: bytes

    def __post_init__(self) -> None:
        if self.document.revision != self.identity.revision:
            raise ValueError("document revision must match RouteConfigIdentity revision")
        observed_digest = sha256(self.artifact_bytes).hexdigest()
        if observed_digest != self.identity.content_sha256:
            raise ValueError(
                "artifact_bytes do not match RouteConfigIdentity content digest"
            )
