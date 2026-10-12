"""Offline B05-C Tag metadata ↔ Dictionary exact object inventory."""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint

from dante.platform.database.mappings import MAPPED_TABLES

_ROOT = Path(__file__).resolve().parents[3] / "docs/database/dictionary/tables"
_TAG_TABLES = (
    "product_tag",
    "product_tag_operation",
    "activity_tag",
    "event_tag",
    "activity_tag_operation",
    "event_tag_operation",
)


def test_b05_tag_tables_have_exact_dictionary_structure_and_no_owner_relationships() -> None:
    mapped = {table.name: table for table in MAPPED_TABLES}
    assert len(mapped) == 135
    for name in _TAG_TABLES:
        entry = json.loads((_ROOT / f"{name}.json").read_text(encoding="utf-8"))
        table = mapped[name]
        structure = entry["structure"]
        assert {column.name for column in table.columns} == {
            column["name"] for column in structure["columns"]
        }
        assert {
            constraint.name
            for constraint in table.constraints
            if isinstance(constraint, PrimaryKeyConstraint)
        } == {structure["primary_key"]["name"]}
        assert {
            constraint.name
            for constraint in table.constraints
            if isinstance(constraint, ForeignKeyConstraint)
        } == {item["name"] for item in structure["foreign_keys"]}
        assert {
            constraint.name
            for constraint in table.constraints
            if isinstance(constraint, CheckConstraint)
        } == {item["name"] for item in structure["check_constraints"]}
        assert {index.name for index in table.indexes} == {
            index["name"] for index in structure["indexes"] if index["source"] == "explicit_index"
        }
        assert all(len(str(constraint.name)) <= 63 for constraint in table.constraints)
