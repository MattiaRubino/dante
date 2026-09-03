"""Provider-neutral route configuration identity and immutable snapshot contracts."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

_SCHEMA_VERSION = 1
_HEX_DIGITS = frozenset("0123456789abcdef")


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_unique_texts(values: tuple[str, ...], *, name: str) -> None:
    for value in values:
        _require_text(value, name=name)
    if len(values) != len(set(values)):
        raise ValueError(f"{name} entries must be unique")


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

    def __post_init__(self) -> None:
        if self.schema_version != _SCHEMA_VERSION:
            raise ValueError(f"unsupported route config schema_version: {self.schema_version}")
        _require_text(self.revision, name="revision")

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


@dataclass(frozen=True, slots=True)
class RouteConfigIdentity:
    """Material identity of one exact behavior-bearing route config artifact."""

    revision: str
    content_sha256: str

    def __post_init__(self) -> None:
        _require_text(self.revision, name="revision")
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
            raise ValueError("artifact_bytes do not match RouteConfigIdentity content digest")
