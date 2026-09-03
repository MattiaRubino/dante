"""Typed reference-resolution contracts for request-local Intelligence work."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, Protocol
from uuid import UUID


class ReferenceBindingRequirement(StrEnum):
    """Binding strength required before a material referent is treated as resolved."""

    EXACT_CANONICAL = "exact_canonical"
    UNIQUE_IN_SCOPE = "unique_in_scope"


class ReferenceCandidateMatch(StrEnum):
    """Candidate evidence class; never model confidence or a resolution outcome."""

    EXACT = "exact"
    POSSIBLE = "possible"


class ReferenceResolutionStatus(StrEnum):
    """Accepted request-local reference-resolution outcomes."""

    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    NOT_FOUND_IN_DECLARED_BOUNDED_UNIVERSE = "not_found_in_declared_bounded_universe"
    POLICY_BLOCKED = "policy_blocked"
    SOURCE_UNAVAILABLE = "source_unavailable"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


@dataclass(frozen=True, slots=True)
class NativeRefBinding:
    """Reference binding to an accepted DANTE NativeRef."""

    native_ref: UUID
    kind: Literal["native"] = "native"

    def __post_init__(self) -> None:
        _require_uuid7(self.native_ref, name="native_ref")


@dataclass(frozen=True, slots=True)
class ScopedRecordRefBinding:
    """Reference binding to an accepted DANTE ScopedRecordRef."""

    scoped_record_ref: UUID
    kind: Literal["scoped_record"] = "scoped_record"

    def __post_init__(self) -> None:
        _require_uuid7(self.scoped_record_ref, name="scoped_record_ref")


@dataclass(frozen=True, slots=True)
class MaterialStateRefBinding:
    """Reference binding to an accepted DANTE MaterialStateRef."""

    material_state_ref: UUID
    kind: Literal["material_state"] = "material_state"

    def __post_init__(self) -> None:
        _require_uuid7(self.material_state_ref, name="material_state_ref")


@dataclass(frozen=True, slots=True)
class ExternalRefBinding:
    """Reference binding to an explicit external/source identity."""

    system: str
    external_ref: str
    revision_ref: str | None = None
    kind: Literal["external"] = "external"

    def __post_init__(self) -> None:
        _require_text(self.system, name="external system")
        _require_text(self.external_ref, name="external_ref")
        if self.revision_ref is not None:
            _require_text(self.revision_ref, name="revision_ref")


type TargetRef = (
    NativeRefBinding | ScopedRecordRefBinding | MaterialStateRefBinding | ExternalRefBinding
)


@dataclass(frozen=True, slots=True)
class ReferenceCandidate:
    """One already-eligible candidate inside the declared bounded universe."""

    target: TargetRef
    display_label: str
    source_scope: str
    match: ReferenceCandidateMatch
    basis_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.display_label, name="display_label")
        _require_text(self.source_scope, name="source_scope")
        if any(not value or not value.strip() for value in self.basis_refs):
            raise ValueError("basis_refs entries must be non-empty")


@dataclass(frozen=True, slots=True)
class ReferenceResolutionRequest:
    """Resolution input over a pre-filtered eligible candidate universe."""

    request_id: UUID
    work_id: UUID
    work_revision: int
    reference_text: str
    purpose: str
    required_binding: ReferenceBindingRequirement
    declared_bounded_universe_id: str
    eligible_candidates: tuple[ReferenceCandidate, ...]
    interpretation_frame_ref: str | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.request_id, name="request_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.reference_text, name="reference_text")
        _require_text(self.purpose, name="purpose")
        _require_text(
            self.declared_bounded_universe_id,
            name="declared_bounded_universe_id",
        )
        if self.interpretation_frame_ref is not None:
            _require_text(self.interpretation_frame_ref, name="interpretation_frame_ref")
        targets = tuple(candidate.target for candidate in self.eligible_candidates)
        if len(targets) != len(set(targets)):
            raise ValueError("eligible_candidates must not contain duplicate targets")


@dataclass(frozen=True, slots=True)
class ReferenceResolutionResult:
    """Immutable resolution outcome carrying target plus achieved binding proof."""

    request_id: UUID
    status: ReferenceResolutionStatus
    declared_bounded_universe_id: str
    resolved_target: TargetRef | None = None
    achieved_binding: ReferenceBindingRequirement | None = None
    eligible_candidates: tuple[ReferenceCandidate, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.request_id, name="request_id")
        _require_text(
            self.declared_bounded_universe_id,
            name="declared_bounded_universe_id",
        )
        if any(not value or not value.strip() for value in self.limitations):
            raise ValueError("limitations entries must be non-empty")

        if self.status is ReferenceResolutionStatus.RESOLVED:
            if self.resolved_target is None or self.achieved_binding is None:
                raise ValueError("RESOLVED requires resolved_target and achieved_binding")
            if self.eligible_candidates:
                raise ValueError("RESOLVED must not carry ambiguity candidates")
            return

        if self.resolved_target is not None or self.achieved_binding is not None:
            raise ValueError(
                "non-RESOLVED result must not carry resolved_target/achieved_binding"
            )

        if self.status is ReferenceResolutionStatus.AMBIGUOUS:
            if len(self.eligible_candidates) < 2:
                raise ValueError("AMBIGUOUS requires at least two eligible candidates")
        elif self.eligible_candidates:
            raise ValueError("only AMBIGUOUS may expose eligible candidate alternatives")


class ReferenceResolver(Protocol):
    """Application-owned resolution seam independent of model/provider identity."""

    async def resolve(
        self,
        request: ReferenceResolutionRequest,
    ) -> ReferenceResolutionResult: ...
