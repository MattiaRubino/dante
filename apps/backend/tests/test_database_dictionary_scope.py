from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"
_SCOPE_PATH = _DICTIONARY_ROOT / "scope.json"
_SCOPE_SCHEMA_PATH = _DICTIONARY_ROOT / "schema" / "scope-v1.schema.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    assert isinstance(value, dict)
    return value


def _entry_count(directory: str) -> int:
    return len(tuple((_DICTIONARY_ROOT / directory).glob("*.json")))


def test_dictionary_scope_matches_declared_scope_schema_contract() -> None:
    scope = _load_json(_SCOPE_PATH)
    schema = _load_json(_SCOPE_SCHEMA_PATH)

    current = scope["current_materialization"]
    completed_stages = current["completed_stages"]

    completed_schema = schema["properties"]["current_materialization"]["properties"][
        "completed_stages"
    ]
    admitted_stages = set(completed_schema["items"]["enum"])

    assert len(completed_stages) == len(set(completed_stages))
    assert set(completed_stages) <= admitted_stages
    assert len(completed_stages) <= completed_schema["maxItems"]

    materialized_rule = next(
        rule
        for rule in schema["allOf"]
        if rule["if"]["properties"]["status"].get("const") == "materialized"
    )
    materialized_stages = materialized_rule["then"]["properties"][
        "current_materialization"
    ]["properties"]["completed_stages"]["const"]

    if scope["status"] == "materialized":
        assert completed_stages == materialized_stages


def test_dictionary_scope_current_counts_match_entry_tree() -> None:
    scope = _load_json(_SCOPE_PATH)
    standalone = scope["current_materialization"]["standalone_entries"]

    tables = _entry_count("tables")
    views = _entry_count("views")
    routines = _entry_count("routines")

    assert standalone["tables"] == tables
    assert standalone["views"] == views
    assert standalone["routines"] == routines
    assert standalone["total"] == tables + views + routines


def test_dictionary_scope_preserves_frozen_cp6_baseline() -> None:
    scope = _load_json(_SCOPE_PATH)
    baseline = scope["expected_baseline"]

    assert baseline == {
        "standalone_entries": {
            "tables": 68,
            "views": 5,
            "routines": 14,
            "total": 87,
        },
        "embedded_objects": {"triggers": 75, "physical_indexes": 95},
        "constraints": {"foreign_keys": 68, "check_constraints": 120},
    }
