"""B08-A lock: Session authority is frozen without new persistence or HTTP surface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dante.bootstrap.openapi_export import openapi_document
from dante.platform.database.mappings import MAPPED_TABLES

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DICTIONARY_TABLES = _REPO_ROOT / "docs" / "database" / "dictionary" / "tables"
_SESSION_TABLES = (
    "session",
    "session_timing_state",
    "session_timing_absolute",
    "session_timing_elapsed",
    "session_timing_pause",
    "session_timing_current_history",
)
_TIMER_INDEXES = {
    "session_timing_pause": "ux_session_timing_pause_open",
    "session_timing_current_history": "ux_session_timing_current_history_open",
}


def _table(name: str) -> dict[str, Any]:
    payload = json.loads((_DICTIONARY_TABLES / f"{name}.json").read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_b08_a_reuses_the_existing_session_dictionary_substrate() -> None:
    """The freeze reuses CP6 Session identity and timing. It does not add a subject edge."""
    session = _table("session")
    structure = session["structure"]
    assert isinstance(structure, dict)
    columns = structure["columns"]
    assert isinstance(columns, list)
    assert [column["name"] for column in columns] == ["session_ref"]

    for name in _SESSION_TABLES:
        entry = _table(name)
        assert entry["object"]["name"] == name
        assert "Session" in entry["semantic_traceability"]["domain_concepts"]

    timing = _table("session_timing_state")
    timing_structure = timing["structure"]
    assert isinstance(timing_structure, dict)
    checks = timing_structure["check_constraints"]
    assert isinstance(checks, list)
    form = next(check for check in checks if check["name"] == "ck_session_timing_state_timing_form")
    assert form["expression_contract"] == "timing_form_code IN ('absolute','elapsed_only')"

    for table_name, index_name in _TIMER_INDEXES.items():
        indexed = _table(table_name)
        indexed_structure = indexed["structure"]
        assert isinstance(indexed_structure, dict)
        indexes = indexed_structure["indexes"]
        assert isinstance(indexes, list)
        assert any(index["name"] == index_name and index["unique"] is True for index in indexes)

    assert not (_DICTIONARY_TABLES / "session_execution_subject.json").exists()
    for path in _DICTIONARY_TABLES.glob("*.json"):
        if path.stem in {"session", *_SESSION_TABLES}:
            continue
        entry = json.loads(path.read_text(encoding="utf-8"))
        column_names = {column["name"] for column in entry["structure"]["columns"]}
        assert "session_ref" not in column_names or not column_names.intersection(
            {"activity_ref", "occurrence_ref", "subject_native_ref"}
        )


def test_b08_a_sqlalchemy_session_mappings_match_the_frozen_substrate() -> None:
    mapped = {table.name for table in MAPPED_TABLES}
    assert set(_SESSION_TABLES) <= mapped
    pause = next(table for table in MAPPED_TABLES if table.name == "session_timing_pause")
    history = next(
        table for table in MAPPED_TABLES if table.name == "session_timing_current_history"
    )
    assert any(index.name == "ux_session_timing_pause_open" for index in pause.indexes)
    assert any(index.name == "ux_session_timing_current_history_open" for index in history.indexes)


def test_b08_a_adds_no_session_http_operations() -> None:
    """B08-B owns the frozen route inventory. B08-A must not publish it early."""
    document = openapi_document()
    paths = document["paths"]
    assert isinstance(paths, dict)
    session_paths = [
        path for path in paths if path.startswith("/api/v1/temporal/") and "session" in path
    ]
    assert session_paths == []
