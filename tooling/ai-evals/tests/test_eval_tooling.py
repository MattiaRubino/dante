"""Deterministic tests for the isolated DANTE eval tooling."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

TOOL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_ROOT))

from azure_candidate_config import normalize_azure_responses_base_url
from dante_eval_core import (
    AssertionSeverity,
    AssertionSpec,
    BudgetGuard,
    EvalFixture,
    Pricing,
    TrialVerdict,
    grade_output,
    load_suite,
)
from gemini_candidate_config import GeminiCandidateConfig


class SuiteLoadingTests(unittest.TestCase):
    def test_current_mini_suite_loads_and_is_bounded(self) -> None:
        suite = load_suite(TOOL_ROOT / "fixtures" / "mini-baseline-v1.json")
        self.assertEqual(suite.suite_id, "dante-mini-baseline-v1")
        self.assertEqual(len(suite.fixtures), 14)
        self.assertEqual(sum(f.requires_model for f in suite.fixtures), 13)

    def test_unknown_family_is_rejected(self) -> None:
        document = {
            "suite_id": "bad",
            "version": 1,
            "description": "bad fixture",
            "fixtures": [
                {
                    "id": "x",
                    "family": "DANTE-E99",
                    "locale": "it-IT",
                    "description": "invalid",
                    "requires_model": False,
                    "input": "",
                    "instructions": "",
                    "max_output_tokens": 1,
                    "response_schema": None,
                    "assertions": [],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "suite.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown workload family"):
                load_suite(path)


class GradingTests(unittest.TestCase):
    def _fixture(self, assertions: tuple[AssertionSpec, ...]) -> EvalFixture:
        return EvalFixture(
            fixture_id="x",
            family="DANTE-E02",
            locale="it-IT",
            description="test",
            requires_model=True,
            input_text="x",
            instructions="x",
            max_output_tokens=32,
            response_schema={"type": "object"},
            assertions=assertions,
        )

    def test_hard_failure_outranks_quality(self) -> None:
        fixture = self._fixture(
            (
                AssertionSpec("equals", "safe", True, AssertionSeverity.HARD),
                AssertionSpec("equals", "label", "ok", AssertionSeverity.QUALITY),
            )
        )
        grade = grade_output(fixture, '{"safe":false,"label":"wrong"}')
        self.assertEqual(grade.verdict, TrialVerdict.HARD_FAIL)

    def test_set_equals_is_order_independent(self) -> None:
        fixture = self._fixture(
            (
                AssertionSpec(
                    "set_equals",
                    "refs",
                    ["A", "B"],
                    AssertionSeverity.HARD,
                ),
            )
        )
        grade = grade_output(fixture, '{"refs":["B","A"]}')
        self.assertEqual(grade.verdict, TrialVerdict.PASS)


class BudgetTests(unittest.TestCase):
    def test_call_cap_blocks_next_dispatch(self) -> None:
        fixture = EvalFixture(
            fixture_id="x",
            family="DANTE-E02",
            locale="it-IT",
            description="test",
            requires_model=True,
            input_text="small",
            instructions="small",
            max_output_tokens=32,
            response_schema={"type": "object"},
            assertions=(),
        )
        guard = BudgetGuard(max_calls=1, max_cost_eur=None, pricing=None)
        guard.calls_used = 1
        with self.assertRaisesRegex(RuntimeError, "call_budget_exhausted"):
            guard.assert_can_dispatch(fixture)

    def test_cost_guard_is_conservative_pre_dispatch(self) -> None:
        fixture = EvalFixture(
            fixture_id="x",
            family="DANTE-E02",
            locale="it-IT",
            description="test",
            requires_model=True,
            input_text="x" * 3000,
            instructions="x" * 3000,
            max_output_tokens=512,
            response_schema={"type": "object"},
            assertions=(),
        )
        guard = BudgetGuard(
            max_calls=1,
            max_cost_eur=0.000001,
            pricing=Pricing(input_eur_per_million=1, output_eur_per_million=1),
        )
        with self.assertRaisesRegex(RuntimeError, "estimated_cost_budget"):
            guard.assert_can_dispatch(fixture)


class AzureEndpointTests(unittest.TestCase):
    def test_resource_root_normalizes_to_v1(self) -> None:
        self.assertEqual(
            normalize_azure_responses_base_url(
                "https://example.openai.azure.com/"
            ),
            "https://example.openai.azure.com/openai/v1/",
        )

    def test_non_azure_host_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Azure OpenAI"):
            normalize_azure_responses_base_url("https://example.com/")


class GeminiCandidateConfigTests(unittest.TestCase):
    def test_defaults_to_gemini_38_flash_low(self) -> None:
        with patch.dict(
            "os.environ",
            {"DANTE_EVAL_GEMINI_API_KEY": "secret"},
            clear=True,
        ):
            config = GeminiCandidateConfig.from_environment()

        self.assertEqual(config.api_key, "secret")
        self.assertEqual(config.model, "gemini-3.8-flash")
        self.assertEqual(config.reasoning_effort, "low")

    def test_rejects_unsupported_reasoning_effort(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "DANTE_EVAL_GEMINI_API_KEY": "secret",
                "DANTE_EVAL_GEMINI_REASONING_EFFORT": "minimal",
            },
            clear=True,
        ):
            with self.assertRaisesRegex(ValueError, "REASONING_EFFORT"):
                GeminiCandidateConfig.from_environment()


if __name__ == "__main__":
    unittest.main()
