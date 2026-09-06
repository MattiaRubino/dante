"""Unit proof for deterministic balanced PV-03 scale fixture planning."""

from collections import Counter

import pytest
from tooling.pre_vertical_foundation.scale import (
    HISTORY_INPUT_SHAPES,
    SCALE_PROFILE_SIZES,
    HistoryInputShape,
    ScaleProfile,
    build_scale_plan,
)


@pytest.mark.parametrize(
    ("profile", "expected_size"),
    [
        (ScaleProfile.SMALL, 12),
        (ScaleProfile.MEDIUM, 120),
        (ScaleProfile.LARGE, 1_200),
    ],
)
def test_scale_profiles_have_exact_balanced_cardinality(
    profile: ScaleProfile,
    expected_size: int,
) -> None:
    plan = build_scale_plan(profile)

    assert len(plan) == expected_size == SCALE_PROFILE_SIZES[profile]
    matrix = Counter((item.persona.slug, item.history.shape) for item in plan)
    assert set(matrix.values()) == {expected_size // 12}
    assert len(matrix) == 12


def test_scale_profiles_are_stable_prefixes_with_unique_uuidv7_identity() -> None:
    small = build_scale_plan(ScaleProfile.SMALL)
    medium = build_scale_plan(ScaleProfile.MEDIUM)
    large = build_scale_plan(ScaleProfile.LARGE)

    assert medium[: len(small)] == small
    assert large[: len(medium)] == medium

    account_refs = [item.account_ref for item in large]
    self_person_refs = [item.self_person_ref for item in large]
    emails = [item.email for item in large]

    assert len(set(account_refs)) == len(account_refs)
    assert len(set(self_person_refs)) == len(self_person_refs)
    assert len(set(account_refs + self_person_refs)) == (len(account_refs) + len(self_person_refs))
    assert len(set(emails)) == len(emails)
    assert all(ref.version == 7 for ref in account_refs + self_person_refs)


def test_history_shapes_are_fixture_only_explicit_timestamp_inputs() -> None:
    first_matrix = build_scale_plan(ScaleProfile.SMALL)
    by_shape = {item.history.shape: item.history for item in first_matrix[:4]}

    assert tuple(by_shape) == HISTORY_INPUT_SHAPES
    assert by_shape[HistoryInputShape.METADATA_FREE].source_instants == ()
    assert len(by_shape[HistoryInputShape.INCOMPLETE].source_instants) == 1
    assert len(by_shape[HistoryInputShape.CORRECTED].source_instants) == 2
    assert len(by_shape[HistoryInputShape.MIXED].source_instants) == 3

    for history in by_shape.values():
        assert tuple(sorted(history.source_instants)) == history.source_instants
        assert all(instant.utcoffset() is not None for instant in history.source_instants)


def test_large_profile_is_planning_data_not_auth_or_product_materialization() -> None:
    plan = build_scale_plan(ScaleProfile.LARGE)

    assert len(plan) == 1_200
    assert not hasattr(plan[0], "password")
    assert not hasattr(plan[0], "verifier")
    assert not hasattr(plan[0], "activity")
    assert not hasattr(plan[0], "event")
    assert not hasattr(plan[0], "routine")
