"""B08 Session authority lock for identity, timing, subject edge, and HTTP surface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest
from pydantic import ValidationError

from dante.bootstrap.openapi_export import openapi_document
from dante.modules.temporal.session_api import (
    SessionEndCommand,
    SessionTransitionCommand,
)
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


def test_b08_reuses_session_timing_and_adds_only_the_typed_subject_edge() -> None:
    """B08 keeps the CP6 identity/timing substrate and a bounded subject edge."""
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

    subject = _table("session_execution_subject")
    subject_columns = [column["name"] for column in subject["structure"]["columns"]]
    assert subject_columns == ["session_ref", "subject_native_ref"]


def test_b08_sqlalchemy_session_mappings_match_the_delivered_substrate() -> None:
    mapped = {table.name for table in MAPPED_TABLES}
    assert set(_SESSION_TABLES) <= mapped
    assert "session_execution_subject" in mapped
    pause = next(table for table in MAPPED_TABLES if table.name == "session_timing_pause")
    history = next(
        table for table in MAPPED_TABLES if table.name == "session_timing_current_history"
    )
    assert any(index.name == "ux_session_timing_pause_open" for index in pause.indexes)
    assert any(index.name == "ux_session_timing_current_history_open" for index in history.indexes)


def test_b08_session_http_operations_and_duration_contract_are_explicit() -> None:
    document = openapi_document()
    paths = document["paths"]
    assert isinstance(paths, dict)
    session_paths = {
        path
        for path in paths
        if path.startswith("/api/v1/temporal/") and "session" in path
    }
    assert session_paths == {
        "/api/v1/temporal/activities/{activity_ref}/sessions",
        "/api/v1/temporal/occurrences/{occurrence_ref}/sessions",
        "/api/v1/temporal/sessions/{session_ref}",
        "/api/v1/temporal/sessions/{session_ref}/end",
        "/api/v1/temporal/sessions/{session_ref}/pause",
        "/api/v1/temporal/sessions/{session_ref}/resume",
    }

    schemas = document["components"]["schemas"]
    response = schemas["SessionResponse"]
    required = set(response["required"])
    assert {
        "session_ref",
        "subject_native_ref",
        "timing_material_state_ref",
        "started_at",
        "ended_at",
        "open",
        "replayed",
        "paused",
        "evaluated_at",
        "elapsed_seconds",
        "paused_seconds",
        "active_seconds",
        "duration_evaluations",
    } <= required


def test_session_transitions_accept_json_uuid_string_and_reject_invalid_refs() -> None:
    material_state_ref = "0199a8c0-7e73-7de2-8cf2-c4062517839f"
    payload = {
        "operation_id": "session-transition-json",
        "expected_material_state_ref": material_state_ref,
    }
    for command in (SessionTransitionCommand, SessionEndCommand):
        validated = command.model_validate(payload)
        assert validated.expected_material_state_ref == UUID(material_state_ref)
        with pytest.raises(ValidationError):
            command.model_validate(
                {**payload, "expected_material_state_ref": "not-a-uuid"}
            )
        with pytest.raises(ValidationError):
            command.model_validate({**payload, "unexpected_field": True})
