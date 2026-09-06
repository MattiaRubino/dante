"""Deterministic, product-independent scale planning for PV-03 readiness QA."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from uuid import UUID

from tooling.pre_vertical_foundation.personas import PERSONAS, PersonaSpec, deterministic_uuid7


class ScaleProfile(StrEnum):
    """Bounded fixture cardinalities for pre-vertical readiness checks."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


SCALE_PROFILE_SIZES: dict[ScaleProfile, int] = {
    ScaleProfile.SMALL: 12,
    ScaleProfile.MEDIUM: 120,
    ScaleProfile.LARGE: 1_200,
}


class HistoryInputShape(StrEnum):
    """Synthetic input-shape labels only; they are not DANTE domain/state types."""

    METADATA_FREE = "metadata_free"
    INCOMPLETE = "incomplete"
    CORRECTED = "corrected"
    MIXED = "mixed"


HISTORY_INPUT_SHAPES: tuple[HistoryInputShape, ...] = (
    HistoryInputShape.METADATA_FREE,
    HistoryInputShape.INCOMPLETE,
    HistoryInputShape.CORRECTED,
    HistoryInputShape.MIXED,
)


@dataclass(frozen=True, slots=True)
class SyntheticHistoryInput:
    """Fixture-only explicit chronology for one synthetic history input shape.

    ``source_instants`` are test input metadata. They do not define a canonical Fact,
    Version, Event, Observation, state model or database persistence contract.
    """

    shape: HistoryInputShape
    source_instants: tuple[datetime, ...]

    def __post_init__(self) -> None:
        if any(instant.tzinfo is None for instant in self.source_instants):
            raise ValueError("synthetic history instants must be timezone-aware")
        if any(instant.utcoffset() != timedelta(0) for instant in self.source_instants):
            raise ValueError("synthetic history instants must be explicit UTC instants")
        if tuple(sorted(self.source_instants)) != self.source_instants:
            raise ValueError("synthetic history chronology must be explicit and ascending")
        if len(set(self.source_instants)) != len(self.source_instants):
            raise ValueError("synthetic history chronology must not contain duplicate instants")


@dataclass(frozen=True, slots=True)
class ScaleIdentityPlan:
    """One deterministic synthetic Account/self-Person fixture plan.

    This is a planning object only. Building a plan performs no database writes and creates no
    password credential, product vertical record or canonical history/state object.
    """

    slot: int
    persona: PersonaSpec
    history: SyntheticHistoryInput
    email: str
    account_ref: UUID
    self_person_ref: UUID


_PROFILE_CELL_COUNT = len(PERSONAS) * len(HISTORY_INPUT_SHAPES)
_HISTORY_BASE = datetime(2016, 1, 1, tzinfo=UTC)
_HISTORY_MIDDLE = datetime(2021, 1, 1, tzinfo=UTC)
_HISTORY_RECENT = datetime(2026, 1, 1, tzinfo=UTC)


def build_scale_plan(profile: ScaleProfile) -> tuple[ScaleIdentityPlan, ...]:
    """Build one stable balanced profile without materializing login-capable Accounts.

    Every block of 12 entries contains the full 3-persona x 4-history-shape matrix exactly once.
    The smaller plans are prefixes of the larger plans, so fixture identity remains stable when a
    test increases its scale profile.
    """
    size = SCALE_PROFILE_SIZES[profile]
    return tuple(_build_identity_plan(slot) for slot in range(size))


def _build_identity_plan(slot: int) -> ScaleIdentityPlan:
    if slot < 0:
        raise ValueError("scale fixture slot must be non-negative")

    cell = slot % _PROFILE_CELL_COUNT
    cycle = slot // _PROFILE_CELL_COUNT
    persona = PERSONAS[cell // len(HISTORY_INPUT_SHAPES)]
    history_shape = HISTORY_INPUT_SHAPES[cell % len(HISTORY_INPUT_SHAPES)]

    return ScaleIdentityPlan(
        slot=slot,
        persona=persona,
        history=_history_input(history_shape, cycle=cycle),
        email=(
            f"synthetic.scale.{slot:04d}.{persona.slug}.{history_shape.value}@example.com"
        ),
        account_ref=deterministic_uuid7(f"scale:{slot}:account"),
        self_person_ref=deterministic_uuid7(f"scale:{slot}:self-person"),
    )


def _history_input(shape: HistoryInputShape, *, cycle: int) -> SyntheticHistoryInput:
    """Return deterministic explicit source timestamps for one fixture input shape."""
    offset = timedelta(days=cycle)
    if shape is HistoryInputShape.METADATA_FREE:
        instants: tuple[datetime, ...] = ()
    elif shape is HistoryInputShape.INCOMPLETE:
        instants = (_HISTORY_MIDDLE + offset,)
    elif shape is HistoryInputShape.CORRECTED:
        instants = (
            _HISTORY_MIDDLE + offset,
            _HISTORY_RECENT + offset,
        )
    elif shape is HistoryInputShape.MIXED:
        instants = (
            _HISTORY_BASE + offset,
            _HISTORY_MIDDLE + offset,
            _HISTORY_RECENT + offset,
        )
    else:  # pragma: no cover - exhaustive StrEnum guard
        raise AssertionError(f"unsupported history input shape: {shape}")

    return SyntheticHistoryInput(shape=shape, source_instants=instants)
