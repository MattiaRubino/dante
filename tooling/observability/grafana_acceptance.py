#!/usr/bin/env python3
"""Plan or apply the source-controlled DANTE Grafana acceptance assets.

Grafana 12 stores dashboards through its dashboard.grafana.app/v2 resource
model, while the stable dashboard HTTP API still accepts the classic import
model owned by this repository.  This command deliberately uses that HTTP API:
the server performs the conversion and operators never paste one model over the
other in the JSON editor.

The command is fail-closed and non-destructive by default.  It performs reads
unless ``--allow-write`` is supplied, updates only stable DANTE UIDs, preserves
unrelated dashboards/rules and backs up every replaced object locally.  The
temporary synthetic rule can only be removed when its exact acceptance labels
are still present.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Never
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DASHBOARD_ROOT = _REPO_ROOT / "infra" / "observability" / "grafana" / "dashboards"
_ALERT_CATALOG = (
    _REPO_ROOT / "infra" / "observability" / "grafana" / "alerts" / "dante-alerts.json"
)
_DEFAULT_TOKEN_FILE = (
    _REPO_ROOT / "infra" / "compose" / "secrets" / "grafana_service_account_token.local"
)
_BACKUP_ROOT = _REPO_ROOT / ".dante" / "observability" / "grafana-backups"
_FOLDER_UID = "dante-observability"
_FOLDER_TITLE = "DANTE"
_RULE_GROUP = "DANTE production"
_SYNTHETIC_GROUP = "DANTE acceptance temporary"
_SYNTHETIC_UID = "dante-acceptance-synthetic"
_SYNTHETIC_TITLE = "DANTE acceptance · synthetic notification"
_RUNBOOK_URL = (
    "https://github.com/MattiaRubino/dante/blob/feature/platform-observability/"
    "docs/development/observability-runbook.md"
)
_MAX_RESPONSE_BYTES = 8 * 1024 * 1024
_DATASOURCE_VARIABLES = {
    "DS_PROMETHEUS": "prometheus",
    "DS_LOKI": "loki",
    "DS_TEMPO": "tempo",
}
_UID_PATTERN = re.compile(r"dante-[a-z0-9-]{1,32}")


class AcceptanceFailure(RuntimeError):
    """One safe, operator-actionable acceptance failure."""


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated operator inputs for one bounded Grafana operation."""

    grafana_url: str
    token_file: Path
    datasource_uids: Mapping[str, str | None]
    receiver: str | None
    allow_write: bool
    with_synthetic: bool
    cleanup_synthetic: bool
    environment: str


@dataclass(frozen=True, slots=True)
class ApiResponse:
    """Bounded decoded response from the Grafana HTTP API."""

    status: int
    payload: Any


def _fail(message: str) -> Never:
    raise AcceptanceFailure(message)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        _fail(f"required source artifact is missing: {path.relative_to(_REPO_ROOT)}")
    except json.JSONDecodeError as error:
        _fail(f"invalid JSON in {path.relative_to(_REPO_ROOT)}: {error}")


def _validate_grafana_url(value: str) -> str:
    candidate = value.strip().rstrip("/")
    parsed = urlsplit(candidate)
    if parsed.scheme != "https" or not parsed.hostname:
        _fail("--grafana-url must be an absolute HTTPS Grafana stack URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        _fail("--grafana-url must not contain credentials, query text or a fragment")
    if parsed.path not in {"", "/"}:
        _fail("--grafana-url must identify the stack root, without an API path")
    return candidate


def _read_token(path: Path) -> str:
    try:
        metadata = path.stat()
    except FileNotFoundError:
        _fail(
            "Grafana service-account token file is missing. Create the one-time, "
            f"local-only file at {path} with mode 0600; never reuse the Alloy "
            "ingestion token."
        )
    if not stat.S_ISREG(metadata.st_mode):
        _fail(f"Grafana token path is not a regular file: {path}")
    if stat.S_IMODE(metadata.st_mode) & 0o077:
        _fail(f"Grafana token file must be private (chmod 600): {path}")
    raw = path.read_text(encoding="utf-8")
    if raw != raw.strip() or "\n" in raw or "\r" in raw:
        _fail("Grafana token file must contain exactly one token without whitespace")
    if len(raw) < 20:
        _fail("Grafana token file does not look like a service-account token")
    return raw


class GrafanaClient:
    """Minimal authenticated client with bounded responses and sanitized errors."""

    def __init__(
        self, base_url: str, token: str, timeout_seconds: float = 15.0
    ) -> None:
        self._base_url = base_url
        self._token = token
        self._timeout_seconds = timeout_seconds

    def request(
        self,
        method: str,
        path: str,
        payload: Mapping[str, Any] | None = None,
        *,
        accepted: Iterable[int] = (200,),
    ) -> ApiResponse:
        body = None
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}",
            "User-Agent": "dante-observability-acceptance/1",
        }
        if payload is not None:
            body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(
            f"{self._base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        accepted_statuses = frozenset(accepted)
        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:  # noqa: S310
                raw = response.read(_MAX_RESPONSE_BYTES + 1)
                if len(raw) > _MAX_RESPONSE_BYTES:
                    _fail(
                        f"Grafana response exceeded {_MAX_RESPONSE_BYTES} bytes: {path}"
                    )
                decoded = _decode_payload(raw)
                if response.status not in accepted_statuses:
                    _fail(f"Grafana {method} {path} returned HTTP {response.status}")
                return ApiResponse(response.status, decoded)
        except HTTPError as error:
            raw = error.read(4096)
            if error.code in accepted_statuses:
                return ApiResponse(error.code, _decode_payload(raw))
            detail = _safe_error_detail(raw)
            suffix = f" ({detail})" if detail else ""
            _fail(f"Grafana {method} {path} returned HTTP {error.code}{suffix}")
        except URLError as error:
            _fail(
                f"Grafana API is unreachable at the configured stack URL: {error.reason}"
            )


def _decode_payload(raw: bytes) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _safe_error_detail(raw: bytes) -> str:
    payload = _decode_payload(raw)
    if not isinstance(payload, Mapping):
        return ""
    for key in ("message", "error"):
        value = payload.get(key)
        if isinstance(value, str):
            return value[:300].replace("\n", " ")
    return ""


def _parse_args() -> Settings:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grafana-url",
        default=os.environ.get("DANTE_GRAFANA_URL"),
        help="Grafana stack root URL (or set DANTE_GRAFANA_URL; never includes a token)",
    )
    parser.add_argument(
        "--token-file",
        type=Path,
        default=_DEFAULT_TOKEN_FILE,
        help="private service-account token file (default: repository-local ignored file)",
    )
    parser.add_argument("--prometheus-uid", help="explicit Metrics datasource UID")
    parser.add_argument("--loki-uid", help="explicit Logs datasource UID")
    parser.add_argument("--tempo-uid", help="explicit Traces datasource UID")
    parser.add_argument(
        "--receiver",
        help="existing, already-tested Grafana contact-point name",
    )
    parser.add_argument(
        "--environment",
        default=os.environ.get("DANTE_OBSERVABILITY_ENVIRONMENT", "local"),
        help="telemetry environment label to materialize (default: local)",
    )
    parser.add_argument(
        "--allow-write",
        action="store_true",
        help="required acknowledgement before dashboard/rule writes",
    )
    parser.add_argument(
        "--with-synthetic",
        action="store_true",
        help="also create the exact temporary LOCAL notification rule",
    )
    parser.add_argument(
        "--cleanup-synthetic",
        action="store_true",
        help="remove only the exact DANTE temporary acceptance rule",
    )
    args = parser.parse_args()
    if not args.grafana_url:
        parser.error("pass --grafana-url or set DANTE_GRAFANA_URL")
    if args.with_synthetic and not args.receiver:
        parser.error("--with-synthetic requires --receiver")
    if (args.with_synthetic or args.cleanup_synthetic) and not args.allow_write:
        parser.error("synthetic-rule changes require --allow-write")
    if args.cleanup_synthetic and args.with_synthetic:
        parser.error("--cleanup-synthetic and --with-synthetic are mutually exclusive")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,31}", args.environment):
        parser.error("--environment must be a bounded lowercase telemetry label")
    return Settings(
        grafana_url=_validate_grafana_url(args.grafana_url),
        token_file=args.token_file.resolve(),
        datasource_uids={
            "prometheus": args.prometheus_uid,
            "loki": args.loki_uid,
            "tempo": args.tempo_uid,
        },
        receiver=args.receiver,
        allow_write=args.allow_write,
        with_synthetic=args.with_synthetic,
        cleanup_synthetic=args.cleanup_synthetic,
        environment=args.environment,
    )


def _discover_datasources(
    client: GrafanaClient, explicit: Mapping[str, str | None]
) -> dict[str, str]:
    response = client.request("GET", "/api/datasources")
    if not isinstance(response.payload, list):
        _fail("Grafana datasource response is not a list")
    discovered: dict[str, str] = {}
    for datasource_type in _DATASOURCE_VARIABLES.values():
        matches = [
            item
            for item in response.payload
            if isinstance(item, Mapping) and item.get("type") == datasource_type
        ]
        selected_uid = explicit.get(datasource_type)
        if selected_uid:
            selected = [item for item in matches if item.get("uid") == selected_uid]
            if len(selected) != 1:
                _fail(
                    f"explicit {datasource_type} UID is absent or has the wrong type: "
                    f"{selected_uid}"
                )
            discovered[datasource_type] = selected_uid
            continue
        if len(matches) != 1:
            choices = (
                ", ".join(f"{item.get('name')}={item.get('uid')}" for item in matches)
                or "none"
            )
            _fail(
                f"expected one {datasource_type} datasource, found {len(matches)} "
                f"({choices}); pass --{datasource_type}-uid explicitly"
            )
        uid = matches[0].get("uid")
        if not isinstance(uid, str) or not uid:
            _fail(f"Grafana {datasource_type} datasource has no stable UID")
        discovered[datasource_type] = uid
    return discovered


def _ensure_receiver(client: GrafanaClient, receiver: str | None) -> None:
    if receiver is None:
        return
    response = client.request("GET", "/api/v1/provisioning/contact-points")
    if not isinstance(response.payload, list):
        _fail("Grafana contact-point response is not a list")
    names = {
        item.get("name")
        for item in response.payload
        if isinstance(item, Mapping) and isinstance(item.get("name"), str)
    }
    if receiver not in names:
        _fail(
            f"contact point does not exist: {receiver}. Create and test it in Grafana first."
        )


def _ensure_folder(client: GrafanaClient, allow_write: bool) -> None:
    path = f"/api/folders/{quote(_FOLDER_UID, safe='')}"
    response = client.request("GET", path, accepted=(200, 404))
    if response.status == 200:
        if not isinstance(response.payload, Mapping):
            _fail("Grafana folder response is malformed")
        if response.payload.get("title") != _FOLDER_TITLE:
            _fail(
                f"folder UID {_FOLDER_UID} already belongs to a different title: "
                f"{response.payload.get('title')}"
            )
        return
    if not allow_write:
        print(f"PLAN: create folder {_FOLDER_TITLE!r} ({_FOLDER_UID})")
        return
    client.request(
        "POST",
        "/api/folders",
        {"uid": _FOLDER_UID, "title": _FOLDER_TITLE},
        accepted=(200,),
    )
    print(f"APPLIED: folder {_FOLDER_TITLE!r} ({_FOLDER_UID})")


def _replace_variables(value: Any, replacements: Mapping[str, str]) -> Any:
    if isinstance(value, dict):
        return {
            key: _replace_variables(child, replacements)
            for key, child in value.items()
            if key != "__inputs"
        }
    if isinstance(value, list):
        return [_replace_variables(child, replacements) for child in value]
    if isinstance(value, str):
        replaced = value
        for name, uid in replacements.items():
            replaced = replaced.replace(f"${{{name}}}", uid)
        return replaced
    return value


def _materialize_dashboard(
    source: Mapping[str, Any], uids: Mapping[str, str]
) -> dict[str, Any]:
    replacements = {
        name: uids[datasource_type]
        for name, datasource_type in _DATASOURCE_VARIABLES.items()
    }
    dashboard = _replace_variables(source, replacements)
    if not isinstance(dashboard, dict):
        _fail("dashboard source did not materialize to an object")
    dashboard["id"] = None
    serialized = json.dumps(dashboard, sort_keys=True)
    if "${DS_" in serialized:
        _fail(
            f"dashboard {dashboard.get('uid')} retained an unresolved datasource input"
        )
    return dashboard


def _dashboard_signature(dashboard: Mapping[str, Any]) -> tuple[Any, ...]:
    panels = dashboard.get("panels")
    if not isinstance(panels, list):
        _fail(f"dashboard {dashboard.get('uid')} has no panel list")
    panel_signature: list[tuple[Any, ...]] = []
    for panel in panels:
        if not isinstance(panel, Mapping):
            _fail(f"dashboard {dashboard.get('uid')} contains a malformed panel")
        queries: list[tuple[str, str, str]] = []
        targets = panel.get("targets", [])
        if isinstance(targets, list):
            for target in targets:
                if not isinstance(target, Mapping):
                    continue
                for key in ("expr", "query"):
                    value = target.get(key)
                    if isinstance(value, str):
                        queries.append((str(target.get("refId", "")), key, value))
        datasource = panel.get("datasource")
        datasource_uid = (
            datasource.get("uid") if isinstance(datasource, Mapping) else None
        )
        panel_signature.append(
            (
                panel.get("id"),
                panel.get("title"),
                panel.get("type"),
                datasource_uid,
                tuple(sorted(queries)),
            )
        )
    return (
        dashboard.get("uid"),
        dashboard.get("title"),
        tuple(sorted(panel_signature, key=lambda item: int(item[0]))),
    )


def _backup_payload(run_directory: Path, filename: str, payload: Any) -> None:
    run_directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(run_directory, 0o700)
    path = run_directory / filename
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    path.chmod(0o600)


def _apply_dashboards(
    client: GrafanaClient,
    datasource_uids: Mapping[str, str],
    allow_write: bool,
    backup_directory: Path,
) -> None:
    for source_path in sorted(_DASHBOARD_ROOT.glob("*.json")):
        source = _read_json(source_path)
        if not isinstance(source, Mapping):
            _fail(f"dashboard root must be an object: {source_path.name}")
        dashboard = _materialize_dashboard(source, datasource_uids)
        uid = dashboard.get("uid")
        if not isinstance(uid, str) or not _UID_PATTERN.fullmatch(uid):
            _fail(f"dashboard source has an invalid UID: {source_path.name}")
        endpoint = f"/api/dashboards/uid/{quote(uid, safe='')}"
        existing = client.request("GET", endpoint, accepted=(200, 404))
        action = "update" if existing.status == 200 else "create"
        if not allow_write:
            print(
                f"PLAN: {action} dashboard {uid} ({len(dashboard.get('panels', []))} panels)"
            )
            continue
        if existing.status == 200:
            _backup_payload(backup_directory, f"dashboard-{uid}.json", existing.payload)
        client.request(
            "POST",
            "/api/dashboards/db",
            {
                "dashboard": dashboard,
                "folderUid": _FOLDER_UID,
                "message": "DANTE source-controlled observability acceptance",
                "overwrite": True,
            },
            accepted=(200,),
        )
        verified = client.request("GET", endpoint)
        if not isinstance(verified.payload, Mapping) or not isinstance(
            verified.payload.get("dashboard"), Mapping
        ):
            _fail(f"Grafana did not return the stored dashboard model for {uid}")
        if _dashboard_signature(verified.payload["dashboard"]) != _dashboard_signature(
            dashboard
        ):
            _fail(
                f"stored dashboard signature differs from source after {action}: {uid}"
            )
        print(f"APPLIED: {action}d dashboard {uid}; source signature verified")


def _threshold_model(
    ref_id: str, expression: str, evaluator: str, threshold: float
) -> dict[str, Any]:
    return {
        "conditions": [
            {
                "evaluator": {"params": [threshold], "type": evaluator},
                "operator": {"type": "and"},
                "query": {"params": [ref_id]},
                "reducer": {"params": [], "type": "last"},
                "type": "query",
            }
        ],
        "datasource": {"type": "__expr__", "uid": "__expr__"},
        "expression": expression,
        "intervalMs": 1000,
        "maxDataPoints": 43200,
        "refId": ref_id,
        "type": "threshold",
    }


def _rule_payload(
    rule: Mapping[str, Any],
    prometheus_uid: str,
    receiver: str | None,
    environment: str,
) -> dict[str, Any]:
    identifier = rule.get("id")
    evaluator = rule.get("evaluator")
    if not isinstance(identifier, str) or not isinstance(evaluator, Mapping):
        _fail("alert catalog contains a malformed rule")
    evaluator_type = evaluator.get("type")
    threshold = evaluator.get("threshold")
    if evaluator_type not in {"gt", "lt"} or not isinstance(threshold, int | float):
        _fail(f"alert {identifier} has an invalid evaluator")
    lookback = rule.get("lookback_seconds")
    if not isinstance(lookback, int) or lookback <= 0:
        _fail(f"alert {identifier} has an invalid lookback")
    payload: dict[str, Any] = {
        "uid": identifier,
        "title": rule["title"],
        "ruleGroup": _RULE_GROUP,
        "folderUID": _FOLDER_UID,
        "condition": "C",
        "data": [
            {
                "refId": "A",
                "queryType": "",
                "relativeTimeRange": {"from": lookback, "to": 0},
                "datasourceUid": prometheus_uid,
                "model": {
                    "datasource": {"type": "prometheus", "uid": prometheus_uid},
                    "editorMode": "code",
                    "expr": str(rule["expr"]).replace('"prod"', f'"{environment}"'),
                    "instant": True,
                    "intervalMs": 1000,
                    "legendFormat": "__auto",
                    "maxDataPoints": 43200,
                    "range": False,
                    "refId": "A",
                },
            },
            {
                "refId": "B",
                "queryType": "",
                "relativeTimeRange": {"from": 0, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [],
                    "datasource": {"type": "__expr__", "uid": "__expr__"},
                    "expression": "A",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "reducer": "last",
                    "refId": "B",
                    "settings": {"mode": "dropNN"},
                    "type": "reduce",
                },
            },
            {
                "refId": "C",
                "queryType": "",
                "relativeTimeRange": {"from": 0, "to": 0},
                "datasourceUid": "__expr__",
                "model": _threshold_model("C", "B", evaluator_type, float(threshold)),
            },
        ],
        "noDataState": "Alerting" if rule["no_data_state"] == "alerting" else "OK",
        "execErrState": "Error",
        "for": rule["for"],
        "annotations": {
            "description": rule["description"],
            "runbook_url": f"{_RUNBOOK_URL}#{rule['runbook_anchor']}",
        },
        "labels": {
            "application": "dante",
            "environment": environment,
            "severity": rule["severity"],
        },
        "isPaused": False,
    }
    if receiver is not None:
        payload["notification_settings"] = {
            "receiver": receiver,
            "group_by": ["grafana_folder", "alertname"],
            "group_wait": "30s",
            "group_interval": "5m",
            "repeat_interval": "4h",
        }
    return payload


def _synthetic_rule(prometheus_uid: str, receiver: str) -> dict[str, Any]:
    payload = _rule_payload(
        {
            "id": _SYNTHETIC_UID,
            "title": _SYNTHETIC_TITLE,
            "severity": "warning",
            "expr": "vector(1)",
            "lookback_seconds": 60,
            "evaluator": {"type": "gt", "threshold": 0},
            "for": "0s",
            "no_data_state": "alerting",
            "description": (
                "Temporary LOCAL acceptance probe. It proves notification delivery and "
                "must be removed immediately after real receipt."
            ),
            "runbook_anchor": "integrated-operational-acceptance-procedure",
        },
        prometheus_uid,
        receiver,
        "local",
    )
    payload["ruleGroup"] = _SYNTHETIC_GROUP
    payload["labels"] = {
        "acceptance": "synthetic",
        "application": "dante",
        "environment": "local",
        "severity": "warning",
    }
    return payload


def _rule_signature(rule: Mapping[str, Any]) -> tuple[Any, ...]:
    data = rule.get("data")
    query_expression: str | None = None
    evaluator_type: str | None = None
    evaluator_threshold: float | None = None
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, Mapping):
                continue
            model = item.get("model")
            if not isinstance(model, Mapping):
                continue
            if item.get("refId") == "A" and isinstance(model.get("expr"), str):
                query_expression = model["expr"]
            if item.get("refId") != "C":
                continue
            conditions = model.get("conditions")
            if not isinstance(conditions, list) or not conditions:
                continue
            condition = conditions[0]
            if not isinstance(condition, Mapping):
                continue
            evaluator = condition.get("evaluator")
            if not isinstance(evaluator, Mapping):
                continue
            if isinstance(evaluator.get("type"), str):
                evaluator_type = evaluator["type"]
            parameters = evaluator.get("params")
            if (
                isinstance(parameters, list)
                and parameters
                and isinstance(parameters[0], int | float)
            ):
                evaluator_threshold = float(parameters[0])
    notification_settings = rule.get("notification_settings")
    receiver = (
        notification_settings.get("receiver")
        if isinstance(notification_settings, Mapping)
        else None
    )
    labels = rule.get("labels")
    normalized_labels = (
        tuple(sorted((str(key), str(value)) for key, value in labels.items()))
        if isinstance(labels, Mapping)
        else ()
    )
    return (
        rule.get("uid"),
        rule.get("title"),
        rule.get("ruleGroup"),
        rule.get("folderUID"),
        rule.get("condition"),
        rule.get("for"),
        rule.get("noDataState"),
        normalized_labels,
        query_expression,
        evaluator_type,
        evaluator_threshold,
        receiver,
    )


def _upsert_rule(
    client: GrafanaClient,
    payload: Mapping[str, Any],
    allow_write: bool,
    backup_directory: Path,
) -> None:
    uid = payload["uid"]
    endpoint = f"/api/v1/provisioning/alert-rules/{quote(uid, safe='')}"
    existing = client.request("GET", endpoint, accepted=(200, 404))
    action = "update" if existing.status == 200 else "create"
    if not allow_write:
        print(f"PLAN: {action} alert rule {uid}")
        return
    if existing.status == 200:
        _backup_payload(backup_directory, f"alert-{uid}.json", existing.payload)
        client.request("PUT", endpoint, payload, accepted=(200, 202))
    else:
        client.request(
            "POST", "/api/v1/provisioning/alert-rules", payload, accepted=(201, 202)
        )
    verified = client.request("GET", endpoint)
    if not isinstance(verified.payload, Mapping):
        _fail(f"Grafana did not return the stored alert rule for {uid}")
    if _rule_signature(verified.payload) != _rule_signature(payload):
        _fail(f"stored alert-rule signature differs from source after {action}: {uid}")
    print(f"APPLIED: {action}d alert rule {uid}; source signature verified")


def _apply_alerts(
    client: GrafanaClient,
    prometheus_uid: str,
    receiver: str | None,
    allow_write: bool,
    with_synthetic: bool,
    environment: str,
    backup_directory: Path,
) -> None:
    catalog = _read_json(_ALERT_CATALOG)
    if not isinstance(catalog, Mapping) or catalog.get("schema_version") != 2:
        _fail("alert catalog must use DANTE schema_version 2")
    rules = catalog.get("rules")
    if not isinstance(rules, list) or len(rules) != 8:
        _fail(
            "the governed DANTE production alert catalog must contain exactly 8 rules"
        )
    for rule in rules:
        if not isinstance(rule, Mapping):
            _fail("alert catalog contains a non-object rule")
        _upsert_rule(
            client,
            _rule_payload(rule, prometheus_uid, receiver, environment),
            allow_write,
            backup_directory,
        )
    if with_synthetic:
        if receiver is None:
            _fail("synthetic notification rule requires a verified receiver")
        _upsert_rule(
            client,
            _synthetic_rule(prometheus_uid, receiver),
            allow_write,
            backup_directory,
        )


def _cleanup_synthetic(client: GrafanaClient, allow_write: bool) -> None:
    endpoint = f"/api/v1/provisioning/alert-rules/{_SYNTHETIC_UID}"
    existing = client.request("GET", endpoint, accepted=(200, 404))
    if existing.status == 404:
        print("CLEANUP: temporary synthetic rule is already absent")
        return
    if not isinstance(existing.payload, Mapping):
        _fail("synthetic alert response is malformed")
    labels = existing.payload.get("labels")
    if (
        existing.payload.get("title") != _SYNTHETIC_TITLE
        or existing.payload.get("ruleGroup") != _SYNTHETIC_GROUP
        or not isinstance(labels, Mapping)
        or labels.get("acceptance") != "synthetic"
        or labels.get("environment") != "local"
    ):
        _fail("refusing to delete a rule that is not the exact DANTE synthetic probe")
    if not allow_write:
        print(f"PLAN: remove temporary alert rule {_SYNTHETIC_UID}")
        return
    client.request("DELETE", endpoint, accepted=(204,))
    verification = client.request("GET", endpoint, accepted=(404,))
    if verification.status != 404:
        _fail("Grafana still returns the temporary rule after cleanup")
    print("CLEANUP PASS: exact temporary synthetic rule removed")


def main() -> int:
    """Plan or execute one governed Grafana acceptance operation."""
    try:
        settings = _parse_args()
        token = _read_token(settings.token_file)
        client = GrafanaClient(settings.grafana_url, token)
        if settings.cleanup_synthetic:
            _cleanup_synthetic(client, settings.allow_write)
            return 0

        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        backup_directory = _BACKUP_ROOT / timestamp
        datasource_uids = _discover_datasources(client, settings.datasource_uids)
        _ensure_receiver(client, settings.receiver)
        _ensure_folder(client, settings.allow_write)
        _apply_dashboards(
            client, datasource_uids, settings.allow_write, backup_directory
        )
        _apply_alerts(
            client,
            datasource_uids["prometheus"],
            settings.receiver,
            settings.allow_write,
            settings.with_synthetic,
            settings.environment,
            backup_directory,
        )
        mode = "APPLY" if settings.allow_write else "PLAN"
        print(
            f"Grafana acceptance {mode}: PASS "
            "(2 dashboards, 8 production alerts"
            f"{', 1 temporary synthetic alert' if settings.with_synthetic else ''})"
        )
        if settings.with_synthetic:
            print(
                "WAITING FOR HUMAN EVIDENCE: confirm real notification receipt, then run "
                "observability:grafana:cleanup-synthetic immediately."
            )
        return 0
    except AcceptanceFailure as error:
        print(f"Grafana acceptance failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
