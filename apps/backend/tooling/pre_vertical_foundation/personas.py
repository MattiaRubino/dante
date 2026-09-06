"""Deterministic, product-independent personas for pre-vertical development and QA."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from uuid import UUID

from dante.platform.time import TimeZoneMode, TimeZonePolicy

_NAMESPACE = "dante.pre-vertical.persona.v1"
_SYNTHETIC_UUID_TIMESTAMP_MS = int(datetime(2026, 1, 1, tzinfo=UTC).timestamp() * 1000)


class TemporalExpectation(StrEnum):
    """Expected interpretation of one deterministic temporal anchor."""

    ORDINARY_LOCAL = "ordinary_local"
    NONEXISTENT_LOCAL = "nonexistent_local"
    AMBIGUOUS_LOCAL = "ambiguous_local"
    HISTORICAL_INSTANT = "historical_instant"


@dataclass(frozen=True, slots=True)
class TemporalAnchor:
    """One reusable local-time or absolute-time anchor with explicit expected semantics."""

    label: str
    zone_id: str
    expectation: TemporalExpectation
    local_datetime: datetime | None = None
    instant: datetime | None = None

    def __post_init__(self) -> None:
        if (self.local_datetime is None) == (self.instant is None):
            raise ValueError("TemporalAnchor requires exactly one local_datetime or instant")
        if self.local_datetime is not None and self.local_datetime.tzinfo is not None:
            raise ValueError("local_datetime anchors must be naive wall-clock values")
        if self.instant is not None and self.instant.tzinfo is None:
            raise ValueError("instant anchors must be timezone-aware")


@dataclass(frozen=True, slots=True)
class PersonaSpec:
    """Stable synthetic identity plus timezone/time scenarios, without product records."""

    slug: str
    email: str
    account_ref: UUID
    self_person_ref: UUID
    timezone_policy: TimeZonePolicy
    device_zone_id: str
    temporal_anchors: tuple[TemporalAnchor, ...]


def deterministic_uuid7(label: str) -> UUID:
    """Return one stable syntactically valid UUIDv7 for deterministic synthetic identity.

    The embedded UUIDv7 timestamp is a fixture-construction detail only. DANTE never derives
    semantic chronology/currentness from ordering these identifiers.
    """
    if not label or label.strip() != label:
        raise ValueError("deterministic UUID label must be non-blank and trimmed")

    digest = sha256(f"{_NAMESPACE}:{label}".encode()).digest()
    random_bits = int.from_bytes(digest[:10], "big") & ((1 << 74) - 1)
    rand_a = (random_bits >> 62) & ((1 << 12) - 1)
    rand_b = random_bits & ((1 << 62) - 1)

    value = (
        (_SYNTHETIC_UUID_TIMESTAMP_MS << 80) | (0x7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    )
    return UUID(int=value)


def _persona_ref(slug: str, family: str) -> UUID:
    return deterministic_uuid7(f"{slug}:{family}")


NORMAL = PersonaSpec(
    slug="normal",
    email="synthetic.normal@example.com",
    account_ref=_persona_ref("normal", "account"),
    self_person_ref=_persona_ref("normal", "self-person"),
    timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
    device_zone_id="Europe/Rome",
    temporal_anchors=(
        TemporalAnchor(
            label="ordinary-summer-local",
            zone_id="Europe/Rome",
            expectation=TemporalExpectation.ORDINARY_LOCAL,
            local_datetime=datetime(2026, 6, 15, 12, 0),  # noqa: DTZ001 - intentional naive local wall-clock
        ),
    ),
)

TEMPORAL_EDGE = PersonaSpec(
    slug="temporal_edge",
    email="synthetic.temporal-edge@example.com",
    account_ref=_persona_ref("temporal_edge", "account"),
    self_person_ref=_persona_ref("temporal_edge", "self-person"),
    timezone_policy=TimeZonePolicy(
        mode=TimeZoneMode.FIXED,
        fixed_zone_id="America/New_York",
    ),
    # Deliberately different from the fixed semantic/default policy to prove device movement does
    # not rewrite the persisted fixed policy.
    device_zone_id="Europe/Rome",
    temporal_anchors=(
        TemporalAnchor(
            label="new-york-spring-gap",
            zone_id="America/New_York",
            expectation=TemporalExpectation.NONEXISTENT_LOCAL,
            local_datetime=datetime(2026, 3, 8, 2, 30),  # noqa: DTZ001 - intentional naive local wall-clock
        ),
        TemporalAnchor(
            label="new-york-fall-overlap",
            zone_id="America/New_York",
            expectation=TemporalExpectation.AMBIGUOUS_LOCAL,
            local_datetime=datetime(2026, 11, 1, 1, 30),  # noqa: DTZ001 - intentional naive local wall-clock
        ),
    ),
)

HISTORICAL = PersonaSpec(
    slug="historical",
    email="synthetic.historical@example.com",
    account_ref=_persona_ref("historical", "account"),
    self_person_ref=_persona_ref("historical", "self-person"),
    timezone_policy=TimeZonePolicy(
        mode=TimeZoneMode.FIXED,
        fixed_zone_id="Europe/Rome",
    ),
    device_zone_id="America/Los_Angeles",
    temporal_anchors=(
        TemporalAnchor(
            label="history-start",
            zone_id="Europe/Rome",
            expectation=TemporalExpectation.HISTORICAL_INSTANT,
            instant=datetime(2016, 1, 1, tzinfo=UTC),
        ),
        TemporalAnchor(
            label="history-as-of",
            zone_id="Europe/Rome",
            expectation=TemporalExpectation.HISTORICAL_INSTANT,
            instant=datetime(2026, 1, 1, tzinfo=UTC),
        ),
    ),
)

PERSONAS: tuple[PersonaSpec, ...] = (NORMAL, TEMPORAL_EDGE, HISTORICAL)
PERSONAS_BY_SLUG = {persona.slug: persona for persona in PERSONAS}
