"""Current post-CP6 catalog, mapping, ACL and Dictionary reconciliation."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import psycopg
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory

from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.mappings.views import VIEW_METADATA
from dante.platform.database.metadata import Base

pytestmark = pytest.mark.postgres

_CURRENT_REVISION = "20260827_09"
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"


def _entries(kind: str) -> dict[str, dict[str, Any]]:
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((_DICTIONARY_ROOT / kind).glob("*.json"))
    }


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def _dictionary_sets(
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

            for group in ("unique_constraints", "check_constraints"):
                for constraint in entry["structure"][group]:
                    name_ = str(constraint["name"])
                    assert name_ not in constraints
                    constraints.add(name_)

            for foreign_key in entry["structure"]["foreign_keys"]:
                name_ = str(foreign_key["name"])
                assert name_ not in constraints
                constraints.add(name_)
                target = foreign_key["target"]
                assert str(target["table"]) in tables

            for index in entry["structure"]["indexes"]:
                name_ = str(index["name"])
                assert name_ not in indexes
                indexes.add(name_)

            for trigger in entry["structure"]["triggers"]:
                name_ = str(trigger["name"])
                assert name_ not in triggers
                triggers.add(name_)
                assert str(trigger["routine"]).removeprefix("dante.") in routines

    return indexes, constraints, triggers


def test_current_catalog_matches_dictionary_sqlalchemy_and_alembic(
    migrated_database: Any,
) -> None:
    tables = _entries("tables")
    views = _entries("views")
    routines = _entries("routines")
    expected_indexes, expected_constraints, expected_triggers = _dictionary_sets(
        tables,
        views,
        routines,
    )
    scope = json.loads((_DICTIONARY_ROOT / "scope.json").read_text(encoding="utf-8"))

    with _admin(migrated_database) as connection:
        topology = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relkind='r'
                 AND c.relname<>'alembic_version'),
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relkind='v'),
              (SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
               WHERE n.nspname='dante'),
              (SELECT count(*) FROM pg_trigger t
               JOIN pg_class c ON c.oid=t.tgrelid
               JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND NOT t.tgisinternal),
              (SELECT count(*) FROM pg_index i
               JOIN pg_class c ON c.oid=i.indrelid
               JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relname<>'alembic_version'),
              (SELECT count(*) FROM pg_constraint c
               JOIN pg_namespace n ON n.oid=c.connamespace
               WHERE n.nspname='dante' AND c.contype='f'),
              (SELECT count(*) FROM pg_constraint c
               JOIN pg_namespace n ON n.oid=c.connamespace
               WHERE n.nspname='dante' AND c.contype='c')
            """
        ).fetchone()
        live_tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        live_views = {
            str(row[0])
            for row in connection.execute("SELECT viewname FROM pg_views WHERE schemaname='dante'")
        }
        live_routines = {
            str(row[0])
            for row in connection.execute(
                "SELECT p.proname FROM pg_proc p "
                "JOIN pg_namespace n ON n.oid=p.pronamespace "
                "WHERE n.nspname='dante'"
            )
        }
        live_constraints = {
            str(row[0])
            for row in connection.execute(
                "SELECT con.conname FROM pg_constraint con "
                "JOIN pg_class c ON c.oid=con.conrelid "
                "JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname='dante' AND c.relname<>'alembic_version' "
                "AND con.contype IN ('p','u','f','c')"
            )
        }
        live_indexes = {
            str(row[0])
            for row in connection.execute(
                "SELECT indexname FROM pg_indexes "
                "WHERE schemaname='dante' AND tablename<>'alembic_version'"
            )
        }
        live_triggers = {
            str(row[0])
            for row in connection.execute(
                "SELECT t.tgname FROM pg_trigger t "
                "JOIN pg_class c ON c.oid=t.tgrelid "
                "JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname='dante' AND NOT t.tgisinternal"
            )
        }
        owners = {
            str(row[0])
            for row in connection.execute(
                "SELECT DISTINCT pg_get_userbyid(c.relowner) "
                "FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                "WHERE n.nspname='dante' AND c.relname<>'alembic_version'"
            )
        }

    current = scope["current_materialization"]
    expected_topology = (
        current["standalone_entries"]["tables"],
        current["standalone_entries"]["views"],
        current["standalone_entries"]["routines"],
        current["embedded_objects"]["triggers"],
        current["embedded_objects"]["physical_indexes"],
        current["constraints"]["foreign_keys"],
        current["constraints"]["check_constraints"],
    )

    assert topology == expected_topology
    assert len(tables) == expected_topology[0]
    assert len(views) == expected_topology[1]
    assert len(routines) == expected_topology[2]
    assert live_tables == set(tables)
    assert live_views == set(views)
    assert live_routines == set(routines)
    assert live_constraints == expected_constraints
    assert live_indexes == expected_indexes
    assert live_triggers == expected_triggers
    assert owners == {"dante_owner"}

    mapped = {table.name: table for table in MAPPED_TABLES}
    assert set(mapped) == set(tables)
    assert len(MAPPED_TABLES) == len(Base.registry.mappers) == len(Base.metadata.tables)
    assert set(VIEW_METADATA.tables) == {f"dante.{name}" for name in views}

    for name, entry in tables.items():
        mapping = entry["implementation"]["sqlalchemy"]
        row = getattr(
            importlib.import_module(str(mapping["module"])),
            str(mapping["symbol"]),
        )
        assert row.__table__.name == name
        assert row.__table__.schema == "dante"

    config = Config(toml_file=str(_REPO_ROOT / "apps" / "backend" / "pyproject.toml"))
    scripts = ScriptDirectory.from_config(config)
    assert scripts.get_heads() == [_CURRENT_REVISION]


def test_m3_auth_runtime_acl_is_exact(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        table_privileges = connection.execute(
            """
            SELECT
              has_table_privilege('dante_runtime','dante.account','SELECT'),
              has_table_privilege('dante_runtime','dante.account','INSERT'),
              has_table_privilege('dante_runtime','dante.account','UPDATE'),
              has_table_privilege('dante_runtime','dante.account','DELETE'),
              has_table_privilege('dante_runtime','dante.email_identity','SELECT'),
              has_table_privilege('dante_runtime','dante.email_identity','INSERT'),
              has_table_privilege('dante_runtime','dante.email_identity','UPDATE'),
              has_table_privilege('dante_runtime','dante.email_identity','DELETE'),
              has_table_privilege('dante_runtime','dante.password_credential','SELECT'),
              has_table_privilege('dante_runtime','dante.password_credential','INSERT'),
              has_table_privilege('dante_runtime','dante.password_credential','UPDATE'),
              has_table_privilege('dante_runtime','dante.password_credential','DELETE'),
              has_table_privilege('dante_runtime','dante.auth_session','SELECT'),
              has_table_privilege('dante_runtime','dante.auth_session','INSERT'),
              has_table_privilege('dante_runtime','dante.auth_session','UPDATE'),
              has_table_privilege('dante_runtime','dante.auth_session','DELETE')
            """
        ).fetchone()
        password_columns = connection.execute(
            """
            SELECT
              has_column_privilege(
                'dante_runtime','dante.password_credential','verifier','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.password_credential','pepper_key_id','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.password_credential','updated_at','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.password_credential','account_ref','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.password_credential','password_credential_ref','UPDATE'
              )
            """
        ).fetchone()
        session_columns = connection.execute(
            """
            SELECT
              has_column_privilege(
                'dante_runtime','dante.auth_session','last_user_activity_at','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.auth_session','revoked_at','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.auth_session','revocation_reason_code','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.auth_session','secret_verifier','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.auth_session','account_ref','UPDATE'
              ),
              has_column_privilege(
                'dante_runtime','dante.auth_session','auth_session_ref','UPDATE'
              )
            """
        ).fetchone()

    assert table_privileges == (
        True, False, False, False,
        True, False, False, False,
        True, False, False, False,
        True, True, False, False,
    )
    assert password_columns == (True, True, True, False, False)
    assert session_columns == (True, True, True, False, False, False)
