"""Unit proof for deterministic product-independent pre-vertical personas."""

from tooling.pre_vertical_foundation.personas import (
    HISTORICAL,
    NORMAL,
    PERSONAS,
    TEMPORAL_EDGE,
    TemporalExpectation,
    deterministic_uuid7,
)

from dante.platform.time import classify_local_time


def test_persona_uuidv7_refs_are_stable_valid_and_unique() -> None:
    assert deterministic_uuid7("normal:account") == NORMAL.account_ref
    assert deterministic_uuid7("normal:self-person") == NORMAL.self_person_ref

    refs = [ref for persona in PERSONAS for ref in (persona.account_ref, persona.self_person_ref)]
    assert len(refs) == len(set(refs))
    assert all(ref.version == 7 for ref in refs)


def test_normal_persona_follows_current_device_zone() -> None:
    assert NORMAL.timezone_policy.resolve(device_zone_id=NORMAL.device_zone_id) == "Europe/Rome"
    anchor = NORMAL.temporal_anchors[0]
    assert anchor.local_datetime is not None
    assert classify_local_time(anchor.local_datetime, anchor.zone_id).kind == "unique"


def test_temporal_edge_persona_proves_gap_overlap_and_fixed_zone_independence() -> None:
    assert (
        TEMPORAL_EDGE.timezone_policy.resolve(device_zone_id=TEMPORAL_EDGE.device_zone_id)
        == "America/New_York"
    )

    expectations = {
        anchor.expectation: classify_local_time(anchor.local_datetime, anchor.zone_id).kind
        for anchor in TEMPORAL_EDGE.temporal_anchors
        if anchor.local_datetime is not None
    }
    assert expectations[TemporalExpectation.NONEXISTENT_LOCAL] == "nonexistent"
    assert expectations[TemporalExpectation.AMBIGUOUS_LOCAL] == "ambiguous"


def test_historical_persona_uses_explicit_instants_not_identifier_order() -> None:
    history_start = HISTORICAL.temporal_anchors[0].instant
    history_as_of = HISTORICAL.temporal_anchors[1].instant
    assert history_start is not None
    assert history_as_of is not None
    assert history_start < history_as_of


def test_persona_slugs_and_emails_are_stable_and_distinct() -> None:
    assert [persona.slug for persona in PERSONAS] == ["normal", "temporal_edge", "historical"]
    assert len({persona.email for persona in PERSONAS}) == len(PERSONAS)
