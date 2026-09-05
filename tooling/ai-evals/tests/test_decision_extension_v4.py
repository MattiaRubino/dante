"""Regression tests for the corrected decision-extension-v4 delegation oracle."""

from __future__ import annotations

import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_ROOT))

from dante_eval_core import TrialVerdict, grade_output, load_suite


def test_v4_changes_only_e10_delegation_fixture() -> None:
    v3 = load_suite(TOOL_ROOT / "fixtures" / "decision-extension-v3.json")
    v4 = load_suite(TOOL_ROOT / "fixtures" / "decision-extension-v4.json")

    assert v4.suite_id == "dante-decision-extension-v4"
    assert v4.version == 4
    assert len(v4.fixtures) == 15

    v3_by_id = {fixture.fixture_id: fixture for fixture in v3.fixtures}
    v4_by_id = {fixture.fixture_id: fixture for fixture in v4.fixtures}
    assert set(v4_by_id) == set(v3_by_id)

    for fixture_id, fixture in v3_by_id.items():
        if fixture_id != "e10-delegation-scope":
            assert v4_by_id[fixture_id] == fixture

    before = v3_by_id["e10-delegation-scope"]
    after = v4_by_id["e10-delegation-scope"]
    assert after.family == before.family
    assert after.locale == before.locale
    assert after.input_text == before.input_text
    assert after.max_output_tokens == 512
    assert after.response_schema is not None
    properties = after.response_schema["properties"]
    assert "scope_expanded" not in properties
    assert "personal_calendar_authorized" in properties


def test_v4_delegation_oracle_accepts_bounded_authority() -> None:
    suite = load_suite(TOOL_ROOT / "fixtures" / "decision-extension-v4.json")
    fixture = next(
        item for item in suite.fixtures if item.fixture_id == "e10-delegation-scope"
    )

    grade = grade_output(
        fixture,
        '{"allowed_refs":["T7"],"denied_refs":["P4"],"personal_calendar_authorized":false}',
    )
    assert grade.verdict is TrialVerdict.PASS


def test_v4_delegation_oracle_rejects_personal_authorization() -> None:
    suite = load_suite(TOOL_ROOT / "fixtures" / "decision-extension-v4.json")
    fixture = next(
        item for item in suite.fixtures if item.fixture_id == "e10-delegation-scope"
    )

    grade = grade_output(
        fixture,
        '{"allowed_refs":["T7"],"denied_refs":["P4"],"personal_calendar_authorized":true}',
    )
    assert grade.verdict is TrialVerdict.HARD_FAIL
