"""Provider-neutral direct-evaluation primitives for DANTE model candidates.

This module is intentionally isolated under tooling/ai-evals. It does not own
DANTE domain/runtime semantics and must not be imported by production code.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Final

DANTE_WORKLOAD_FAMILIES: Final[frozenset[str]] = frozenset(
    f"DANTE-E{i:02d}" for i in range(1, 15)
)

MAX_HARD_CALLS: Final = 30
MAX_HARD_OUTPUT_TOKENS_PER_CALL: Final = 512
MAX_HARD_INPUT_CHARS_PER_FIXTURE: Final = 16_000


class TrialVerdict(StrEnum):
    PASS = "PASS"
    HARD_FAIL = "HARD_FAIL"
    QUALITY_FAIL = "QUALITY_FAIL"
    INVALID_FIXTURE = "INVALID_FIXTURE"
    INVALID_GRADER = "INVALID_GRADER"
    INVALID_HARNESS = "INVALID_HARNESS"
    PROVIDER_INFRA_FAILURE = "PROVIDER_INFRA_FAILURE"
    INCONCLUSIVE = "INCONCLUSIVE"


class AssertionSeverity(StrEnum):
    HARD = "hard"
    QUALITY = "quality"


@dataclass(frozen=True, slots=True)
class AssertionSpec:
    kind: str
    path: str
    expected: Any
    severity: AssertionSeverity


@dataclass(frozen=True, slots=True)
class EvalFixture:
    fixture_id: str
    family: str
    locale: str
    description: str
    requires_model: bool
    input_text: str
    instructions: str
    max_output_tokens: int
    response_schema: dict[str, Any] | None
    assertions: tuple[AssertionSpec, ...]


@dataclass(frozen=True, slots=True)
class EvalSuite:
    suite_id: str
    version: int
    description: str
    fixtures: tuple[EvalFixture, ...]


@dataclass(frozen=True, slots=True)
class CandidateResult:
    output_text: str | None
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    provider_request_id: str | None
    provider_response_id: str | None
    latency_ms: int
    provider_status: str | None = None
    error_class: str | None = None
    error_code: str | None = None


@dataclass(frozen=True, slots=True)
class AssertionFailure:
    kind: str
    path: str
    severity: AssertionSeverity
    expected: Any
    observed: Any


@dataclass(frozen=True, slots=True)
class GradeResult:
    verdict: TrialVerdict
    failures: tuple[AssertionFailure, ...]
    parsed_output: Any | None


@dataclass(frozen=True, slots=True)
class Pricing:
    input_eur_per_million: float
    output_eur_per_million: float


@dataclass(slots=True)
class BudgetGuard:
    max_calls: int
    max_cost_eur: float | None
    pricing: Pricing | None
    calls_used: int = 0
    input_tokens_used: int = 0
    output_tokens_used: int = 0
    estimated_cost_eur: float = 0.0

    def __post_init__(self) -> None:
        if not 1 <= self.max_calls <= MAX_HARD_CALLS:
            raise ValueError(f"max_calls must be between 1 and {MAX_HARD_CALLS}")
        if self.max_cost_eur is not None and self.max_cost_eur <= 0:
            raise ValueError("max_cost_eur must be positive")
        if self.max_cost_eur is not None and self.pricing is None:
            raise ValueError("pricing is required when max_cost_eur is set")

    def assert_can_dispatch(self, fixture: EvalFixture) -> None:
        if self.calls_used >= self.max_calls:
            raise RuntimeError("call_budget_exhausted")
        if fixture.max_output_tokens > MAX_HARD_OUTPUT_TOKENS_PER_CALL:
            raise RuntimeError("fixture_output_cap_exceeds_hard_limit")
        if len(fixture.input_text) + len(fixture.instructions) > MAX_HARD_INPUT_CHARS_PER_FIXTURE:
            raise RuntimeError("fixture_input_chars_exceed_hard_limit")

        if self.max_cost_eur is not None and self.pricing is not None:
            # Conservative pre-dispatch estimate. Character/3 deliberately
            # overestimates many ordinary English/Italian prompts; actual
            # provider usage replaces it after the call. This is a guardrail,
            # not billing authority.
            estimated_input_tokens = (
                len(fixture.input_text) + len(fixture.instructions) + 2
            ) // 3
            estimated_next = (
                estimated_input_tokens * self.pricing.input_eur_per_million
                + fixture.max_output_tokens * self.pricing.output_eur_per_million
            ) / 1_000_000
            if self.estimated_cost_eur + estimated_next > self.max_cost_eur:
                raise RuntimeError("estimated_cost_budget_would_be_exceeded")

    def record(self, result: CandidateResult) -> None:
        self.calls_used += 1
        if result.input_tokens is not None:
            self.input_tokens_used += result.input_tokens
        if result.output_tokens is not None:
            self.output_tokens_used += result.output_tokens

        if self.pricing is not None:
            self.estimated_cost_eur = (
                self.input_tokens_used * self.pricing.input_eur_per_million
                + self.output_tokens_used * self.pricing.output_eur_per_million
            ) / 1_000_000


def _require_string(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _parse_assertion(document: Any) -> AssertionSpec:
    if not isinstance(document, dict):
        raise ValueError("assertion must be an object")
    kind = _require_string(document.get("kind"), field="assertion.kind")
    if kind not in {"equals", "not_equals", "set_equals", "contains", "not_contains"}:
        raise ValueError(f"unsupported assertion kind: {kind}")
    path = _require_string(document.get("path"), field="assertion.path")
    try:
        severity = AssertionSeverity(document.get("severity"))
    except ValueError as exc:
        raise ValueError("assertion.severity must be hard or quality") from exc
    if "expected" not in document:
        raise ValueError("assertion.expected is required")
    return AssertionSpec(
        kind=kind,
        path=path,
        expected=document["expected"],
        severity=severity,
    )


def _parse_fixture(document: Any) -> EvalFixture:
    if not isinstance(document, dict):
        raise ValueError("fixture must be an object")

    fixture_id = _require_string(document.get("id"), field="fixture.id")
    family = _require_string(document.get("family"), field=f"{fixture_id}.family")
    if family not in DANTE_WORKLOAD_FAMILIES:
        raise ValueError(f"{fixture_id}: unknown workload family {family}")

    locale = _require_string(document.get("locale"), field=f"{fixture_id}.locale")
    if locale not in {"it-IT", "en-US"}:
        raise ValueError(f"{fixture_id}: locale must be it-IT or en-US")

    requires_model = document.get("requires_model")
    if not isinstance(requires_model, bool):
        raise ValueError(f"{fixture_id}: requires_model must be boolean")

    input_text = document.get("input", "")
    instructions = document.get("instructions", "")
    if not isinstance(input_text, str) or not isinstance(instructions, str):
        raise ValueError(f"{fixture_id}: input/instructions must be strings")

    max_output_tokens = document.get("max_output_tokens", 256)
    if (
        not isinstance(max_output_tokens, int)
        or max_output_tokens < 1
        or max_output_tokens > MAX_HARD_OUTPUT_TOKENS_PER_CALL
    ):
        raise ValueError(
            f"{fixture_id}: max_output_tokens must be 1..{MAX_HARD_OUTPUT_TOKENS_PER_CALL}"
        )

    response_schema = document.get("response_schema")
    if response_schema is not None and not isinstance(response_schema, dict):
        raise ValueError(f"{fixture_id}: response_schema must be object or null")

    assertions_document = document.get("assertions", [])
    if not isinstance(assertions_document, list):
        raise ValueError(f"{fixture_id}: assertions must be a list")
    assertions = tuple(_parse_assertion(item) for item in assertions_document)

    if requires_model and response_schema is None:
        raise ValueError(f"{fixture_id}: model fixtures require response_schema")
    if requires_model and not assertions:
        raise ValueError(f"{fixture_id}: model fixtures require assertions")

    if len(input_text) + len(instructions) > MAX_HARD_INPUT_CHARS_PER_FIXTURE:
        raise ValueError(f"{fixture_id}: fixture exceeds hard input character cap")

    return EvalFixture(
        fixture_id=fixture_id,
        family=family,
        locale=locale,
        description=_require_string(document.get("description"), field=f"{fixture_id}.description"),
        requires_model=requires_model,
        input_text=input_text,
        instructions=instructions,
        max_output_tokens=max_output_tokens,
        response_schema=response_schema,
        assertions=assertions,
    )


def _load_suite_document(path: Path, *, seen: frozenset[Path]) -> dict[str, Any]:
    resolved = path.resolve()
    if resolved in seen:
        raise ValueError("suite inheritance cycle detected")

    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("suite document must be an object")

    if "base_suite" not in document:
        return document

    if "fixtures" in document:
        raise ValueError("overlay suite cannot define both base_suite and fixtures")

    base_suite = _require_string(document.get("base_suite"), field="base_suite")
    base_relative = Path(base_suite)
    if base_relative.is_absolute() or ".." in base_relative.parts:
        raise ValueError("base_suite must be a sibling fixture filename")

    base_document = _load_suite_document(
        path.parent / base_relative,
        seen=seen | {resolved},
    )
    base_fixtures = base_document.get("fixtures")
    if not isinstance(base_fixtures, list) or not base_fixtures:
        raise ValueError("base suite fixtures must be a non-empty list")

    replacements_document = document.get("fixture_replacements", [])
    if not isinstance(replacements_document, list) or not replacements_document:
        raise ValueError("overlay suite fixture_replacements must be a non-empty list")

    replacements: dict[str, dict[str, Any]] = {}
    for replacement in replacements_document:
        if not isinstance(replacement, dict):
            raise ValueError("fixture replacement must be an object")
        fixture_id = _require_string(
            replacement.get("id"),
            field="fixture_replacement.id",
        )
        if fixture_id in replacements:
            raise ValueError(f"duplicate fixture replacement: {fixture_id}")
        replacements[fixture_id] = replacement

    base_ids = {
        _require_string(fixture.get("id"), field="base fixture.id")
        for fixture in base_fixtures
        if isinstance(fixture, dict)
    }
    if len(base_ids) != len(base_fixtures):
        raise ValueError("base suite contains invalid or duplicate fixture ids")

    unknown = sorted(set(replacements) - base_ids)
    if unknown:
        raise ValueError(f"overlay replaces unknown fixture(s): {', '.join(unknown)}")

    materialized = dict(base_document)
    materialized["suite_id"] = document.get("suite_id")
    materialized["version"] = document.get("version")
    materialized["description"] = document.get("description")
    materialized["fixtures"] = [
        replacements.get(_require_string(fixture.get("id"), field="base fixture.id"), fixture)
        for fixture in base_fixtures
    ]
    return materialized


def load_suite(path: Path) -> EvalSuite:
    document = _load_suite_document(path, seen=frozenset())
    fixtures_document = document.get("fixtures")
    if not isinstance(fixtures_document, list) or not fixtures_document:
        raise ValueError("suite.fixtures must be a non-empty list")
    fixtures = tuple(_parse_fixture(item) for item in fixtures_document)

    fixture_ids = [fixture.fixture_id for fixture in fixtures]
    if len(set(fixture_ids)) != len(fixture_ids):
        raise ValueError("fixture ids must be unique")

    return EvalSuite(
        suite_id=_require_string(document.get("suite_id"), field="suite_id"),
        version=int(document.get("version")),
        description=_require_string(document.get("description"), field="description"),
        fixtures=fixtures,
    )


def _resolve_path(document: Any, path: str) -> Any:
    current = document
    for segment in path.split("."):
        if isinstance(current, dict) and segment in current:
            current = current[segment]
            continue
        raise KeyError(path)
    return current


def _evaluate_assertion(document: Any, assertion: AssertionSpec) -> AssertionFailure | None:
    try:
        observed = _resolve_path(document, assertion.path)
    except KeyError:
        return AssertionFailure(
            kind=assertion.kind,
            path=assertion.path,
            severity=assertion.severity,
            expected=assertion.expected,
            observed="<missing>",
        )

    passed = False
    if assertion.kind == "equals":
        passed = observed == assertion.expected
    elif assertion.kind == "not_equals":
        passed = observed != assertion.expected
    elif assertion.kind == "set_equals":
        passed = (
            isinstance(observed, list)
            and isinstance(assertion.expected, list)
            and set(observed) == set(assertion.expected)
        )
    elif assertion.kind == "contains":
        passed = isinstance(observed, list) and assertion.expected in observed
    elif assertion.kind == "not_contains":
        passed = isinstance(observed, list) and assertion.expected not in observed

    if passed:
        return None
    return AssertionFailure(
        kind=assertion.kind,
        path=assertion.path,
        severity=assertion.severity,
        expected=assertion.expected,
        observed=observed,
    )


def grade_output(fixture: EvalFixture, output_text: str | None) -> GradeResult:
    if not fixture.requires_model:
        return GradeResult(
            verdict=TrialVerdict.INCONCLUSIVE,
            failures=(),
            parsed_output=None,
        )

    if output_text is None or not output_text.strip():
        return GradeResult(
            verdict=TrialVerdict.QUALITY_FAIL,
            failures=(
                AssertionFailure(
                    kind="non_empty_output",
                    path="$",
                    severity=AssertionSeverity.QUALITY,
                    expected="schema-conforming JSON",
                    observed=output_text,
                ),
            ),
            parsed_output=None,
        )

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        return GradeResult(
            verdict=TrialVerdict.QUALITY_FAIL,
            failures=(
                AssertionFailure(
                    kind="valid_json",
                    path="$",
                    severity=AssertionSeverity.QUALITY,
                    expected="valid JSON",
                    observed=output_text[:500],
                ),
            ),
            parsed_output=None,
        )

    failures = tuple(
        failure
        for assertion in fixture.assertions
        if (failure := _evaluate_assertion(parsed, assertion)) is not None
    )

    if any(failure.severity is AssertionSeverity.HARD for failure in failures):
        verdict = TrialVerdict.HARD_FAIL
    elif failures:
        verdict = TrialVerdict.QUALITY_FAIL
    else:
        verdict = TrialVerdict.PASS
    return GradeResult(verdict=verdict, failures=failures, parsed_output=parsed)
