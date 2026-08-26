"""CP6-05 final catalog, Dictionary, SQLAlchemy and Alembic reconciliation."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import psycopg
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory

from dante.platform.database.metadata import Base
from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.mappings.views import VIEW_METADATA

pytestmark = pytest.mark.postgres

_FINAL_REVISION = "20260826_08"
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"
_EXPECTED_STAGES = [f"CP6-M0{stage}" for stage in range(1, 8)]


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


def _validate_dictionary(
    tables: dict[str, dict[str, Any]],
    views: dict[str, dict[str, Any]],
    routines: dict[str, dict[str, Any]],
) -> tuple[set[str], set[str], set[str]]:
    indexes: set[str] = set()
    constraints: set[str] = set()
    triggers: set[str] = set()
    for kind, entries in (("table", tables), ("view", views), ("routine", routines)):
        for name, entry in entries.items():
            assert entry["object"]["key"] == f"{kind}:dante.{name}"
            columns = {str(column["name"]) for column in entry["structure"]["columns"]}
            assert len(columns) == len(entry["structure"]["columns"])
            for grant in entry["security"]["expected_grants"]:
                assert set(map(str, grant["columns"])) <= columns
            if kind != "table":
                continue
            primary_key = entry["structure"]["primary_key"]
            assert primary_key is not None
            constraints.add(str(primary_key["name"]))
            assert set(map(str, primary_key["columns"])) <= columns
            for group in ("unique_constraints", "check_constraints"):
                for constraint in entry["structure"][group]:
                    constraint_name = str(constraint["name"])
                    assert constraint_name not in constraints
                    constraints.add(constraint_name)
            for foreign_key in entry["structure"]["foreign_keys"]:
                constraint_name = str(foreign_key["name"])
                assert constraint_name not in constraints
                constraints.add(constraint_name)
                assert set(map(str, foreign_key["columns"])) <= columns
                target = foreign_key["target"]
                target_columns = {
                    str(column["name"])
                    for column in tables[str(target["table"])]["structure"]["columns"]
                }
                assert set(map(str, target["columns"])) <= target_columns
            for index in entry["structure"]["indexes"]:
                index_name = str(index["name"])
                assert index_name not in indexes
                indexes.add(index_name)
                assert set(map(str, index["keys"])) <= columns
                assert set(map(str, index["include"])) <= columns
            for trigger in entry["structure"]["triggers"]:
                trigger_name = str(trigger["name"])
                assert trigger_name not in triggers
                triggers.add(trigger_name)
                routine_name = str(trigger["routine"]).removeprefix("dante.")
                assert routine_name in routines
                assert routines[routine_name]["structure"]["routine"]["return_type"] == "trigger"
    return indexes, constraints, triggers


def test_cp6_final_environment_topology_and_cross_representation(migrated_database: Any) -> None:
    tables, views, routines = _entries("tables"), _entries("views"), _entries("routines")
    expected_indexes, expected_constraints, expected_triggers = _validate_dictionary(
        tables, views, routines
    )
    scope = json.loads((_DICTIONARY_ROOT / "scope.json").read_text(encoding="utf-8"))
    with _admin(migrated_database) as connection:
        environment = connection.execute(
            "SELECT current_setting('server_version_num'),current_setting('server_encoding'),"
            "current_setting('max_identifier_length')"
        ).fetchone()
        topology = connection.execute(
            """
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
            """
        ).fetchone()
        live_tables = {str(row[0]) for row in connection.execute("SELECT tablename FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'")}
        live_views = {str(row[0]) for row in connection.execute("SELECT viewname FROM pg_views WHERE schemaname='dante'")}
        live_routines = {str(row[0]) for row in connection.execute("SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'")}
        live_constraints = {str(row[0]) for row in connection.execute("SELECT con.conname FROM pg_constraint con JOIN pg_class c ON c.oid=con.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version' AND con.contype IN ('p','u','f','c')")}
        live_indexes = {str(row[0]) for row in connection.execute("SELECT indexname FROM pg_indexes WHERE schemaname='dante' AND tablename<>'alembic_version'")}
        live_triggers = {str(row[0]) for row in connection.execute("SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal")}
        owners = {str(row[0]) for row in connection.execute("SELECT DISTINCT pg_get_userbyid(c.relowner) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version'")}
        extensions = dict(connection.execute("SELECT extname,extversion FROM pg_extension WHERE extname IN ('postgis','vector','pg_trgm','unaccent','pg_stat_statements')"))
    assert environment == ("180006", "UTF8", "63")
    assert topology == (68, 5, 14, 75, 95, 68, 120, 0, 0, 0)
    assert (len(tables), len(views), len(routines)) == (68, 5, 14)
    assert live_tables == set(tables) and live_views == set(views) and live_routines == set(routines)
    assert live_constraints == expected_constraints
    assert live_indexes == expected_indexes
    assert live_triggers == expected_triggers
    assert owners == {"dante_owner"}
    assert extensions["postgis"] == "3.6.4" and extensions["vector"] == "0.8.6"
    assert set(extensions) == {"postgis", "vector", "pg_trgm", "unaccent", "pg_stat_statements"}
    assert scope["current_materialization"]["completed_stages"] == _EXPECTED_STAGES
    assert len(MAPPED_TABLES) == len(Base.registry.mappers) == len(Base.metadata.tables) == 68
    assert all(len(mapper.relationships) == 0 for mapper in Base.registry.mappers)
    assert set(VIEW_METADATA.tables) == {f"dante.{name}" for name in views}
    for name, entry in tables.items():
        mapping = entry["implementation"]["sqlalchemy"]
        row = getattr(importlib.import_module(str(mapping["module"])), str(mapping["symbol"]))
        assert row.__table__.name == name and row.__table__.schema == "dante"
    config = Config(toml_file=str(_REPO_ROOT / "apps" / "backend" / "pyproject.toml"))
    scripts = ScriptDirectory.from_config(config)
    assert scripts.get_heads() == [_FINAL_REVISION]
