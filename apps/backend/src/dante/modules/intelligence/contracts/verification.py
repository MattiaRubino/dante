"""Verification contracts separating evidence-backed truth checks from publication."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class VerificationStatus(StrEnum):
    """Accepted first-vertical verification outcomes."""

    VERIFIED = "verified"
    LIMITED = "limited"
    CONFLICTED = "conflicted"
    STALE = "stale"
    REJECTED = "rejected"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    NEEDS_REREAD = "needs_reread"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_texts(values: tuple[str, ...], *, name: str) -> None:
    if any(not value or not value.strip() for value in values):
        raise ValueError(f"{name} entries must be non-empty")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


def _require_aware(value: datetime, *, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """Immutable verification result for one exact runtime representation."""

    verification_id: UUID
    work_id: UUID
    work_revision: int
    representation_ref: str
    basis_manifest_id: UUID
    status: VerificationStatus
    evaluated_at: datetime
    evidence_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, value in (
            ("verification_id", self.verification_id),
            ("work_id", self.work_id),
            ("basis_manifest_id", self.basis_manifest_id),
        ):
            _require_uuid7(value, name=name)
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.representation_ref, name="representation_ref")
        _require_aware(self.evaluated_at, name="evaluated_at")
        _require_texts(self.evidence_refs, name="evidence_refs")
        _require_texts(self.limitations, name="limitations")

        if self.status is VerificationStatus.VERIFIED:
            if not self.evidence_refs:
                raise ValueError("VERIFIED result requires evidence_refs")
            if self.limitations:
                raise ValueError("VERIFIED result must not carry unresolved limitations")
        if self.status is VerificationStatus.LIMITED and not self.limitations:
            raise ValueError("LIMITED result requires declared limitations")
        if self.status in {VerificationStatus.STALE, VerificationStatus.NEEDS_REREAD} and not self.limitations:
            raise ValueError("stale/reread verification requires a declared limitation")
