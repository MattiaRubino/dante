"""Bounded CP-SAT selection keeps solver outcomes distinct."""

import pytest

from dante.modules.temporal.plan_candidate_solver import select_nearby_indices


def test_nearest_distinct_stable_tie_break() -> None:
    allowed = tuple(index for index in range(97) if index != 48)
    assert select_nearby_indices(allowed).indices == (47, 49, 46)
    assert select_nearby_indices(allowed).indices == (47, 49, 46)
    assert select_nearby_indices(allowed).status == "OPTIMAL"


def test_empty_model_is_infeasible_only_with_no_allowed_slot() -> None:
    assert select_nearby_indices(()).status == "INFEASIBLE"
    assert select_nearby_indices((52,)).indices == (52,)
    assert select_nearby_indices((52,)).status == "OPTIMAL"


@pytest.mark.parametrize("allowed", [(49, 48), (48, 48), (-1,), (97,)])
def test_reject_invalid_grid(allowed: tuple[int, ...]) -> None:
    with pytest.raises(ValueError, match="Candidate grid indices are invalid"):
        select_nearby_indices(allowed)
