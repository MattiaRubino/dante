"""Current whole-database PostgreSQL/Dictionary/SQLAlchemy/Alembic reconciliation."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import psycopg
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Table

from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.mappings.views import VIEW_METADATA
from dante.platform.database.metadata import Base

pytestmark = pytest.mark.postgres

_CURRENT_REVISION = "20260904_17"
_CURRENT_TOPOLOGY = (88, 5, 16, 76, 172, 89, 270, 0, 0, 0)
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def _entries(kind: str) -> dict[str, dict[str, Any]]:
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((_DICTIONARY_ROOT / kind).glob("*.json"))
    }


def _dictionary_identifiers(
    tables: dict[str, dict[str, Any]], routines: dict[str, dict[str, Any]]
) -> tuple[set[str], set[str], set[str]]:
    indexes: set[str] = set()
    constraints: set[str] = set()
    triggers: set[str] = set()
    for name, entry in tables.items():
        assert entry["object"]["key"] == f"table:dante.{name}"
        columns = {str(column["name"]) for column in entry["structure"]["columns"]}
        assert len(columns) == len(entry["structure"]["columns"])
        primary_key = entry["structure"]["primary_key"]
        assert primary_key is not None
        constraints.add(str(primary_key["name"]))
        for group in ("unique_constraints", "check_constraints"):
            for constraint in entry["structure"][group]:
                identifier = str(constraint["name"])
                assert identifier not in constraints
                constraints.add(identifier)
        for foreign_key in entry["structure"]["foreign_keys"]:
            identifier = str(foreign_key["name"])
            assert identifier not in constraints
            constraints.add(identifier)
        for index in entry["structure"]["indexes"]:
            identifier = str(index["name"])
            assert identifier not in indexes
            indexes.add(identifier)
        for trigger in entry["structure"]["triggers"]:
            identifier = str(trigger["name"])
            assert identifier not in triggers
            triggers.add(identifier)
            assert str(trigger["routine"]).removeprefix("dante.") in routines
    return indexes, constraints, triggers


def test_current_database_cross_representation_is_exact(migrated_database: Any) -> None:
    tables = _entries("tables")
    views = _entries("views")
    routines = _entries("routines")
    expected_indexes, expected_constraints, expected_triggers = _dictionary_identifiers(
        tables, routines
    )
    scope = json.loads((_DICTIONARY_ROOT / "scope.json").read_text(encoding="utf-8"))
    with _admin(migrated_database) as connection:
        environment = connection.execute(
            "SELECT current_setting('server_version_num'),current_setting('server_encoding'),current_setting('max_identifier_length')"
        ).fetchone()
        topology = connection.execute("""
            SELECT
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='r' AND c.relname<>'alembic_version'),
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind='v'),
              (SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'),
              (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal),
              (SELECT count(*) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version'),
              (SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='f'),
              (SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='dante' AND c.contype='c'),
              (SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace WHERE n.nspname='dante' AND t.typtype IN ('d','e')),
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relkind IN ('S','m','p')),
              (SELECT count(*) FROM pg_policy p JOIN pg_class c ON c.oid=p.polrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante')
        """).fetchone()
        live_tables = {
            str(r[0])
            for r in connection.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        live_views = {
            str(r[0])
            for r in connection.execute("SELECT viewname FROM pg_views WHERE schemaname='dante'")
        }
        live_routines = {
            str(r[0])
            for r in connection.execute(
                "SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'"
            )
        }
        live_constraints = {
            str(r[0])
            for r in connection.execute(
                "SELECT con.conname FROM pg_constraint con JOIN pg_class c ON c.oid=con.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version' AND con.contype IN ('p','u','f','c')"
            )
        }
        live_indexes = {
            str(r[0])
            for r in connection.execute(
                "SELECT indexname FROM pg_indexes WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        live_triggers = {
            str(r[0])
            for r in connection.execute(
                "SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal"
            )
        }
        owners = {
            str(r[0])
            for r in connection.execute(
                "SELECT DISTINCT pg_get_userbyid(c.relowner) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version'"
            )
        }
        extensions = dict(
            connection.execute(
                "SELECT extname,extversion FROM pg_extension WHERE extname IN ('postgis','vector','pg_trgm','unaccent','pg_stat_statements')"
            )
        )
        current_revision = connection.execute(
            "SELECT version_num FROM dante.alembic_version"
        ).fetchone()
    assert environment == ("180006", "UTF8", "63")
    assert topology == _CURRENT_TOPOLOGY
    assert current_revision == (_CURRENT_REVISION,)
    assert (len(tables), len(views), len(routines)) == (88, 5, 16)
    assert live_tables == set(tables)
    assert live_views == set(views)
    assert live_routines == set(routines)
    assert live_constraints == expected_constraints
    assert live_indexes == expected_indexes
    assert live_triggers == expected_triggers
    assert owners == {"dante_owner"}
    assert extensions["postgis"] == "3.6.4"
    assert extensions["vector"] == "0.8.6"
    assert set(extensions) == {"postgis", "vector", "pg_trgm", "unaccent", "pg_stat_statements"}
    current = scope["current_materialization"]
    assert current["completed_stages"] == [
        "CP6-M01",
        "CP6-M02",
        "CP6-M03",
        "CP6-M04",
        "CP6-M05",
        "CP6-M06",
        "CP6-M07",
    ]
    assert current["standalone_entries"] == {"tables": 88, "views": 5, "routines": 16, "total": 109}
    assert current["embedded_objects"] == {"triggers": 76, "physical_indexes": 172}
    assert current["constraints"] == {"foreign_keys": 89, "check_constraints": 270}
    assert len(MAPPED_TABLES) == len(Base.registry.mappers) == len(Base.metadata.tables) == 88
    assert all(len(mapper.relationships) == 0 for mapper in Base.registry.mappers)
    assert set(VIEW_METADATA.tables) == {f"dante.{name}" for name in views}
    assert {table.name for table in MAPPED_TABLES} == set(tables)
    for name, entry in tables.items():
        mapping = entry["implementation"]["sqlalchemy"]
        row = getattr(importlib.import_module(str(mapping["module"])), str(mapping["symbol"]))
        assert isinstance(row.__table__, Table)
        assert row.__table__.name == name
        assert row.__table__.schema == "dante"
    config = Config(toml_file=str(_REPO_ROOT / "apps" / "backend" / "pyproject.toml"))
    scripts = ScriptDirectory.from_config(config)
    assert scripts.get_heads() == [_CURRENT_REVISION]
