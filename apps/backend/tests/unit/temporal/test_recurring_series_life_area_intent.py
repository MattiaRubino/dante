"""Unit validation for exact recurring Life Area authoring contracts."""

from __future__ import annotations

from typing import Literal

import pytest

from dante.modules.temporal.recurring_series_edit import _validate_series_area_intent
from dante.modules.temporal.recurring_series_reconciliation import SeriesReconciliationError


@pytest.mark.parametrize("owner", ["event", "routine"])
def test_series_life_area_authoring_validation(
    owner: Literal["event", "routine"],
) -> None:
    event = {
        "life_area_ref": None,
        "new_life_area": {"name": "Nuova", "color_code": "#4285F4"},
    }
    routine = {
        "activity_template": {"life_area_ref": None},
        "new_life_area": {"name": "Nuova", "color_code": "#4285F4"},
    }
    structure = routine if owner == "routine" else event
    _validate_series_area_intent(owner, structure)
    for invalid in (
        {"name": "", "color_code": "#4285F4"},
        {"name": "  nuova  ", "color_code": "#4285F4"},
        {"name": "Nuova", "color_code": "blue"},
        {"name": "Nuova", "color_code": "#4285f4"},
    ):
        with pytest.raises(SeriesReconciliationError):
            _validate_series_area_intent(owner, {**structure, "new_life_area": invalid})
    with pytest.raises(SeriesReconciliationError):
        _validate_series_area_intent(
            owner,
            {
                **structure,
                "area_color_change": {
                    "life_area_ref": "00000000-0000-0000-0000-000000000001",
                    "expected_revision": 1,
                    "color_code": "#FFD600",
                },
            },
        )
