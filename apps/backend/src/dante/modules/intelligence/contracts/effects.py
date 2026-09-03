"""First-vertical Effect boundary contracts for read-only Intelligence work."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from dante.modules.intelligence.contracts.work import ConsequenceProfile


class EffectDisposition(StrEnum):
    """Future-compatible Effect outcome classification; C6 admits NO_EFFECT only."""

    NO_EFFECT = "no_effect"
    EXECUTED = "executed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


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
class EffectOutcome:
    """Immutable Effect-boundary result; no mutation adapter is materialized by C6."""

    outcome_id: UUID
    work_id: UUID
    work_revision: int
    consequence_profile: ConsequenceProfile
    disposition: EffectDisposition
    evaluated_at: datetime
    proposed_effect_refs: tuple[str, ...] = ()
    executed_effect_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.outcome_id, name="outcome_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_aware(self.evaluated_at, name="evaluated_at")
        _require_texts(self.proposed_effect_refs, name="proposed_effect_refs")
        _require_texts(self.executed_effect_refs, name="executed_effect_refs")
        _require_texts(self.limitations, name="limitations")

        if self.consequence_profile is ConsequenceProfile.READ_ONLY:
            if self.proposed_effect_refs or self.executed_effect_refs:
                raise ValueError("READ_ONLY work must not carry proposed or executed effects")
            if self.disposition is not EffectDisposition.NO_EFFECT:
                raise ValueError("READ_ONLY work requires EffectDisposition.NO_EFFECT")
