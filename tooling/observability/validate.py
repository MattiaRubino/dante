#!/usr/bin/env python3
"""Fail-fast static validation for DANTE observability-owned artifacts."""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Never

_REPO_ROOT = Path(__file__).resolve().parents[2]
_ALLOY = _REPO_ROOT / "infra" / "observability" / "alloy" / "config.alloy"
_COMPOSE = _REPO_ROOT / "infra" / "compose" / "local.yaml"
_ENV_EXAMPLE = _REPO_ROOT / "infra" / "observability" / ".env.example"
_DASHBOARD_ROOT = _REPO_ROOT / "infra" / "observability" / "grafana" / "dashboards"
_ALERTS = (
    _REPO_ROOT / "infra" / "observability" / "grafana" / "alerts" / "dante-alerts.json"
)
_DICTIONARY_SCOPE = _REPO_ROOT / "docs" / "database" / "dictionary" / "scope.json"
_DICTIONARY_SCHEMA = (
    _REPO_ROOT / "docs" / "database" / "dictionary" / "schema" / "scope-v1.schema.json"
)
_ALLOY_IMAGE = "grafana/alloy:v1.19.2@sha256:b8ec653c44235fbe910879145dac3597d66b0aaecf60bcbbe82580767771a839"
_SAFE_SEVERITIES = frozenset({"warning", "critical"})
_GRAFANA_RUNTIME_JOBS = frozenset(
    {
        "integrations/self",
        "integrations/postgres",
        "integrations/blackbox/dante-backend-ready",
    }
)
_STALE_LOCAL_JOB_NAMES = frozenset({"dante-alloy", "dante-postgres", "dante-blackbox"})
_FORBIDDEN_TELEMETRY_LABELS = re.compile(
    r"(?:account|actor|email|identity|person|session|token|user)[_-]?(?:id|ref|key)?",
    re.IGNORECASE,
)


class ValidationFailure(RuntimeError):
    """One actionable repository-owned artifact failure."""


@dataclass(frozen=True, slots=True)
class DashboardSummary:
    path: Path
    uid: str
    panel_ids: tuple[int, ...]


def _fail(message: str) -> Never:
    raise ValidationFailure(message)


def _read(path: Path) -> str:
    if not path.is_file():
        _fail(f"required artifact is missing: {path.relative_to(_REPO_ROOT)}")
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> Any:
    try:
        return json.loads(_read(path))
    except json.JSONDecodeError as error:
        _fail(f"invalid JSON in {path.relative_to(_REPO_ROOT)}: {error}")


def _walk(value: object) -> Iterable[object]:
    yield value
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield key
            yield from _walk(child)
    elif isinstance(value, list | tuple):
        for child in value:
            yield from _walk(child)


def _validate_alloy() -> None:
    alloy = _read(_ALLOY)
    compose = _read(_COMPOSE)
    environment = _read(_ENV_EXAMPLE)

    required_fragments = (
        'otelcol.processor.memory_limiter "bounded"',
        "sending_queue {",
        "block_on_overflow = false",
        'max_elapsed_time     = "2m"',
        'otelcol.auth.headers "grafana_cloud"',
        'filename  = "/run/secrets/grafana_cloud_otlp_authorization"',
        "auth               = otelcol.auth.headers.grafana_cloud.handler",
        'prometheus.relabel "postgres_privacy_budget"',
        '"database",',
        "pg_long_running_transactions.*",
        "max_streams = 64",
        "rate_limiting {",
        'prometheus.exporter.self "alloy"',
    )
    for fragment in required_fragments:
        if fragment not in alloy:
            _fail(f"Alloy safety contract is missing: {fragment}")

    forbidden_fragments = (
        "include_query = true",
        "db.statement",
        "http.url",
        "url.query",
        "request.body",
        "response.body",
        '"stat_statements",',
        "stat_statements {",
        "otelcol.auth.basic.grafana_cloud.handler",
    )
    for fragment in forbidden_fragments:
        if fragment in alloy:
            _fail(f"Alloy contains forbidden telemetry content: {fragment}")

    if (
        "forward_to      = [prometheus.relabel.postgres_privacy_budget.receiver]"
        not in alloy
    ):
        _fail("PostgreSQL metrics must pass through the privacy/budget allowlist")

    if _ALLOY_IMAGE not in compose:
        _fail("Compose must pin the reviewed Alloy version and multi-platform digest")
    if "127.0.0.1:4317:4317" not in compose or "127.0.0.1:12347:12347" not in compose:
        _fail("collector ingestion ports must remain published on loopback only")
    if (
        "no-new-privileges:true" not in compose
        or "cap_drop:\n      - ALL" not in compose
    ):
        _fail("Alloy container hardening is incomplete")
    if "grafana_cloud_otlp_authorization" not in compose:
        _fail("Compose must project the private OTLP authorization header")

    alloy_environment = set(re.findall(r'sys\.env\("([A-Z0-9_]+)"\)', alloy))
    declared_environment = {
        line.split("=", maxsplit=1)[0]
        for line in environment.splitlines()
        if line and not line.startswith("#") and "=" in line
    }
    missing_environment = alloy_environment - declared_environment
    if missing_environment:
        _fail(f"Alloy environment example is missing: {sorted(missing_environment)}")


def _panel_queries(panel: Mapping[str, Any]) -> Iterable[str]:
    for target in panel.get("targets", []):
        if isinstance(target, Mapping):
            for key in ("expr", "query"):
                value = target.get(key)
                if isinstance(value, str):
                    yield value
    for child in panel.get("panels", []):
        if isinstance(child, Mapping):
            yield from _panel_queries(child)


def _validate_dashboard(path: Path) -> DashboardSummary:
    raw = _json(path)
    if not isinstance(raw, dict):
        _fail(f"dashboard root must be an object: {path.relative_to(_REPO_ROOT)}")
    uid = raw.get("uid")
    if not isinstance(uid, str) or not re.fullmatch(r"dante-[a-z0-9-]{1,32}", uid):
        _fail(f"dashboard has an invalid stable uid: {path.relative_to(_REPO_ROOT)}")
    if not isinstance(raw.get("title"), str) or int(raw.get("schemaVersion", 0)) < 39:
        _fail(f"dashboard metadata is incomplete: {path.relative_to(_REPO_ROOT)}")

    panel_ids: list[int] = []
    for panel in raw.get("panels", []):
        if not isinstance(panel, dict) or not isinstance(panel.get("id"), int):
            _fail(
                f"dashboard panel lacks an integer id: {path.relative_to(_REPO_ROOT)}"
            )
        panel_ids.append(panel["id"])
        for query in _panel_queries(panel):
            if _FORBIDDEN_TELEMETRY_LABELS.search(query):
                _fail(f"dashboard query uses an identity-like label: {query}")
    if len(panel_ids) != len(set(panel_ids)) or not panel_ids:
        _fail(
            f"dashboard panel ids must be non-empty and unique: {path.relative_to(_REPO_ROOT)}"
        )
    return DashboardSummary(path=path, uid=uid, panel_ids=tuple(panel_ids))


def _validate_grafana_assets() -> None:
    dashboard_paths = sorted(_DASHBOARD_ROOT.glob("*.json"))
    if len(dashboard_paths) < 2:
        _fail("at least service and telemetry-pipeline dashboards are required")
    summaries = [_validate_dashboard(path) for path in dashboard_paths]
    if len({summary.uid for summary in summaries}) != len(summaries):
        _fail("Grafana dashboard UIDs must be unique")

    raw_alerts = _json(_ALERTS)
    if not isinstance(raw_alerts, dict) or raw_alerts.get("schema_version") != 1:
        _fail("alert catalog must use DANTE schema_version 1")
    rules = raw_alerts.get("rules")
    if not isinstance(rules, list) or not rules:
        _fail("alert catalog must contain rules")
    identifiers: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict):
            _fail("every alert rule must be an object")
        identifier = rule.get("id")
        expression = rule.get("expr")
        if not isinstance(identifier, str) or identifier in identifiers:
            _fail("alert rule ids must be non-empty and unique")
        identifiers.add(identifier)
        if rule.get("severity") not in _SAFE_SEVERITIES:
            _fail(f"alert {identifier} has an unsupported severity")
        if rule.get("no_data_state") not in {"alerting", "ok"}:
            _fail(f"alert {identifier} must define an explicit no-data policy")
        if not isinstance(expression, str) or not expression.strip():
            _fail(f"alert {identifier} has no PromQL expression")
        if _FORBIDDEN_TELEMETRY_LABELS.search(expression):
            _fail(f"alert {identifier} uses an identity-like label")

    runtime_query_sources = [
        *dashboard_paths,
        _ALERTS,
        _REPO_ROOT / "docs" / "development" / "observability-runbook.md",
    ]
    runtime_query_text = "\n".join(_read(path) for path in runtime_query_sources)
    for job in _GRAFANA_RUNTIME_JOBS:
        if (
            f'job=\\"{job}\\"' not in runtime_query_text
            and f'job="{job}"' not in runtime_query_text
        ):
            _fail(f"Grafana runtime label contract is missing observed job: {job}")
    for job in _STALE_LOCAL_JOB_NAMES:
        if (
            f'job=\\"{job}\\"' in runtime_query_text
            or f'job="{job}"' in runtime_query_text
        ):
            _fail(f"Grafana query source still uses superseded local job: {job}")


def _validate_database_contract() -> None:
    scope = _json(_DICTIONARY_SCOPE)
    schema = _json(_DICTIONARY_SCHEMA)
    expected_roles = [
        "dante_owner",
        "dante_migrator",
        "dante_runtime",
        "dante_observer",
    ]
    try:
        scope_roles = scope["technical_foundation"]["roles"]
        schema_roles = schema["properties"]["technical_foundation"]["properties"][
            "roles"
        ]["const"]
    except (KeyError, TypeError) as error:
        _fail(f"Dictionary technical-role contract is malformed: {error}")
    if scope_roles != expected_roles or schema_roles != expected_roles:
        _fail("Dictionary scope/schema must agree on the exact technical role topology")


def main() -> int:
    """Validate static artifacts; the pinned Alloy binary remains a separate CI gate."""
    try:
        _validate_alloy()
        _validate_grafana_assets()
        _validate_database_contract()
    except ValidationFailure as error:
        print(f"observability validation failed: {error}", file=sys.stderr)
        return 1
    print("observability static artifacts: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
