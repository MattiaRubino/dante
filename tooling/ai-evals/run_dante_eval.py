"""Run a bounded, provider-neutral DANTE direct-evaluation suite."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Final

from dante_eval_core import (
    MAX_HARD_CALLS,
    AssertionFailure,
    BudgetGuard,
    EvalFixture,
    Pricing,
    TrialVerdict,
    grade_output,
    load_suite,
)

_TOOL_ROOT: Final = Path(__file__).resolve().parent
_DEFAULT_SUITE: Final = _TOOL_ROOT / "fixtures" / "mini-baseline-v1.json"
_DEFAULT_TIMEOUT_SECONDS: Final = 60.0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Bounded DANTE model-candidate evaluation. Dry-run is the default; "
            "use --execute to permit paid provider calls."
        )
    )
    parser.add_argument("--suite", type=Path, default=_DEFAULT_SUITE)
    parser.add_argument(
        "--candidate",
        choices=[
            "azure-openai-responses",
            "google-gemini-openai-compat",
        ],
        default="azure-openai-responses",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="FIXTURE_ID",
        help="Run only the named fixture; repeat to select multiple fixtures.",
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--max-calls", type=int, default=13)
    parser.add_argument("--timeout-seconds", type=float, default=_DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-cost-eur", type=float)
    parser.add_argument("--input-eur-per-million", type=float)
    parser.add_argument("--output-eur-per-million", type=float)
    parser.add_argument(
        "--allow-unpriced",
        action="store_true",
        help=(
            "Allow execution without configured token prices. Call/output hard caps "
            "still apply, but there is no euro-denominated pre-dispatch guard."
        ),
    )
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--include-output",
        action="store_true",
        help="Include model JSON output in the local report. Off by default.",
    )
    return parser


def _pricing(args: argparse.Namespace) -> Pricing | None:
    supplied = (
        args.input_eur_per_million is not None,
        args.output_eur_per_million is not None,
    )
    if any(supplied) and not all(supplied):
        raise ValueError(
            "input and output EUR-per-million prices must be supplied together"
        )
    if not any(supplied):
        return None
    if args.input_eur_per_million < 0 or args.output_eur_per_million < 0:
        raise ValueError("token prices cannot be negative")
    return Pricing(
        input_eur_per_million=args.input_eur_per_million,
        output_eur_per_million=args.output_eur_per_million,
    )


def _selected_fixtures(
    fixtures: tuple[EvalFixture, ...], selected_ids: list[str]
) -> tuple[EvalFixture, ...]:
    if not selected_ids:
        return fixtures
    wanted = set(selected_ids)
    known = {fixture.fixture_id for fixture in fixtures}
    unknown = sorted(wanted - known)
    if unknown:
        raise ValueError(f"unknown fixture id(s): {', '.join(unknown)}")
    return tuple(fixture for fixture in fixtures if fixture.fixture_id in wanted)


def _failure_document(failure: AssertionFailure) -> dict[str, Any]:
    return {
        "kind": failure.kind,
        "path": failure.path,
        "severity": failure.severity.value,
        "expected": failure.expected,
        "observed": failure.observed,
    }


def _emit(document: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(document, ensure_ascii=False, sort_keys=True) + "\n")


def _write_report(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _candidate_from_environment(candidate_id: str) -> Any:
    if candidate_id == "azure-openai-responses":
        from azure_candidate_config import AzureCandidateConfig
        from azure_openai_responses_candidate import AzureOpenAIResponsesCandidate

        return AzureOpenAIResponsesCandidate(AzureCandidateConfig.from_environment())

    if candidate_id == "google-gemini-openai-compat":
        from gemini_candidate_config import GeminiCandidateConfig
        from gemini_openai_compat_candidate import GeminiOpenAICompatCandidate

        return GeminiOpenAICompatCandidate(GeminiCandidateConfig.from_environment())

    raise ValueError(f"unsupported candidate: {candidate_id}")


async def _execute(args: argparse.Namespace) -> int:
    suite = load_suite(args.suite)
    fixtures = _selected_fixtures(suite.fixtures, args.only)
    model_fixtures = tuple(fixture for fixture in fixtures if fixture.requires_model)

    if args.max_calls < 1 or args.max_calls > MAX_HARD_CALLS:
        raise ValueError(f"max-calls must be 1..{MAX_HARD_CALLS}")
    if len(model_fixtures) > args.max_calls:
        raise ValueError(
            f"selected suite requires {len(model_fixtures)} calls but max-calls={args.max_calls}"
        )
    if args.timeout_seconds <= 0 or args.timeout_seconds > 90:
        raise ValueError("timeout-seconds must be >0 and <=90")

    pricing = _pricing(args)
    if args.execute and pricing is None and not args.allow_unpriced:
        raise ValueError(
            "paid execution is blocked without prices; provide both token prices "
            "or explicitly use --allow-unpriced"
        )
    if args.max_cost_eur is not None and pricing is None:
        raise ValueError("max-cost-eur requires token prices")

    plan = {
        "mode": "EXECUTE" if args.execute else "DRY_RUN",
        "suite_id": suite.suite_id,
        "suite_version": suite.version,
        "candidate": args.candidate,
        "selected_fixtures": len(fixtures),
        "planned_provider_calls": len(model_fixtures),
        "max_calls": args.max_calls,
        "hard_call_cap": MAX_HARD_CALLS,
        "max_cost_eur": args.max_cost_eur,
        "priced": pricing is not None,
        "fixture_ids": [fixture.fixture_id for fixture in fixtures],
    }

    if not args.execute:
        _emit({"status": "READY", "plan": plan})
        return 0

    budget = BudgetGuard(
        max_calls=args.max_calls,
        max_cost_eur=args.max_cost_eur,
        pricing=pricing,
    )
    candidate = _candidate_from_environment(args.candidate)

    trials: list[dict[str, Any]] = []
    started_at = datetime.now(UTC)

    try:
        for fixture in fixtures:
            if not fixture.requires_model:
                trials.append(
                    {
                        "fixture_id": fixture.fixture_id,
                        "family": fixture.family,
                        "locale": fixture.locale,
                        "execution_state": "SKIPPED_MODEL_AVOIDANCE",
                        "verdict": None,
                        "note": (
                            "E01/model-avoidance is a DANTE runtime-routing proof, "
                            "not a model-candidate call. No provider request was sent."
                        ),
                    }
                )
                continue

            try:
                budget.assert_can_dispatch(fixture)
            except RuntimeError as exc:
                trials.append(
                    {
                        "fixture_id": fixture.fixture_id,
                        "family": fixture.family,
                        "locale": fixture.locale,
                        "execution_state": "BLOCKED_BUDGET",
                        "verdict": TrialVerdict.INCONCLUSIVE.value,
                        "reason": str(exc),
                    }
                )
                break

            result = await candidate.invoke(
                fixture,
                timeout_seconds=args.timeout_seconds,
            )
            budget.record(result)

            if result.error_class is None and result.provider_status != "completed":
                trial = {
                    "fixture_id": fixture.fixture_id,
                    "family": fixture.family,
                    "locale": fixture.locale,
                    "execution_state": "PROVIDER_NOT_COMPLETED",
                    "verdict": TrialVerdict.INCONCLUSIVE.value,
                    "latency_ms": result.latency_ms,
                    "provider_status": result.provider_status,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "total_tokens": result.total_tokens,
                    "provider_request_id": result.provider_request_id,
                    "provider_response_id": result.provider_response_id,
                }
                trials.append(trial)
                _emit({"trial": trial})
                continue

            if result.error_class is not None:
                trial = {
                    "fixture_id": fixture.fixture_id,
                    "family": fixture.family,
                    "locale": fixture.locale,
                    "execution_state": "PROVIDER_ERROR",
                    "verdict": TrialVerdict.PROVIDER_INFRA_FAILURE.value,
                    "latency_ms": result.latency_ms,
                    "error_class": result.error_class,
                    "error_code": result.error_code,
                    "provider_request_id": result.provider_request_id,
                }
                trials.append(trial)
                _emit({"trial": trial})
                continue

            grade = grade_output(fixture, result.output_text)
            trial = {
                "fixture_id": fixture.fixture_id,
                "family": fixture.family,
                "locale": fixture.locale,
                "execution_state": "COMPLETED",
                "verdict": grade.verdict.value,
                "latency_ms": result.latency_ms,
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
                "total_tokens": result.total_tokens,
                "provider_request_id": result.provider_request_id,
                "provider_response_id": result.provider_response_id,
                "provider_status": result.provider_status,
                "assertion_failures": [
                    _failure_document(failure) for failure in grade.failures
                ],
            }
            if args.include_output:
                trial["output"] = grade.parsed_output
            trials.append(trial)
            _emit({"trial": trial})
    finally:
        await candidate.close()

    counts: dict[str, int] = {}
    for trial in trials:
        verdict = trial.get("verdict")
        if isinstance(verdict, str):
            counts[verdict] = counts.get(verdict, 0) + 1

    completed_verdicts = [
        trial.get("verdict")
        for trial in trials
        if trial.get("execution_state") != "SKIPPED_MODEL_AVOIDANCE"
    ]
    failed = any(
        verdict
        in {
            TrialVerdict.HARD_FAIL.value,
            TrialVerdict.QUALITY_FAIL.value,
            TrialVerdict.PROVIDER_INFRA_FAILURE.value,
            TrialVerdict.INVALID_FIXTURE.value,
            TrialVerdict.INVALID_GRADER.value,
            TrialVerdict.INVALID_HARNESS.value,
        }
        for verdict in completed_verdicts
    )

    report = {
        "schema": "dante-direct-eval-report-v1",
        "suite_id": suite.suite_id,
        "suite_version": suite.version,
        "candidate": candidate.identity,
        "started_at": started_at.isoformat(),
        "finished_at": datetime.now(UTC).isoformat(),
        "plan": plan,
        "budget": {
            "calls_used": budget.calls_used,
            "input_tokens_used": budget.input_tokens_used,
            "output_tokens_used": budget.output_tokens_used,
            "estimated_cost_eur": round(budget.estimated_cost_eur, 8)
            if pricing is not None
            else None,
            "pricing": asdict(pricing) if pricing is not None else None,
            "billing_authority": False,
        },
        "summary": {
            "counts": counts,
            "model_calls_completed": budget.calls_used,
            "model_avoidance_fixtures_skipped": sum(
                1
                for trial in trials
                if trial.get("execution_state") == "SKIPPED_MODEL_AVOIDANCE"
            ),
            "overall": "FAIL" if failed else "PASS_OR_INCONCLUSIVE",
        },
        "trials": trials,
        "non_claims": [
            "This report is model-candidate evidence, not production qualification.",
            "E01 model-avoidance requires DANTE runtime-routing proof and is not graded here.",
            "Estimated cost is not a cloud billing authority.",
            "No private or production DANTE data is permitted in this suite.",
        ],
    }

    _emit({"summary": report["summary"], "budget": report["budget"]})
    if args.report is not None:
        _write_report(args.report, report)
        _emit({"report_written": str(args.report)})

    return 1 if failed else 0


def main() -> int:
    args = _parser().parse_args()
    try:
        return asyncio.run(_execute(args))
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        _emit({"status": "BLOCKED", "reason": str(exc)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
