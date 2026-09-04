"""Current post-CP6 catalog, mapping, ACL and Dictionary reconciliation."""

from __future__ import annotations

import importlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory

from dante.platform.database.mappings import MAPPED_TABLES
from dante.platform.database.mappings.views import VIEW_METADATA
from dante.platform.database.metadata import Base

pytestmark = pytest.mark.postgres

_CURRENT_REVISION = "20260904_17"
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"
_RUNTIME_ROLE = "dante_runtime"
_TABLE_PRIVILEGES = ("SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "REFERENCES", "TRIGGER")
_COLUMN_PRIVILEGES = ("SELECT", "INSERT", "UPDATE", "REFERENCES")


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


def _expected_runtime_acl(entry: dict[str, Any]) -> tuple[set[str], dict[str, set[str]]]:
    table_privileges: set[str] = set()
    column_privileges: dict[str, set[str]] = {}
    for grant in entry["security"]["expected_grants"]:
        if grant["grantee"] != _RUNTIME_ROLE:
            continue
        privilege = str(grant["privilege"])
        columns = {str(column) for column in grant["columns"]}
        if columns:
            column_privileges.setdefault(privilege, set()).update(columns)
        else:
            table_privileges.add(privilege)
    return table_privileges, column_privileges


def test_runtime_table_and_column_acl_matches_dictionary(migrated_database: Any) -> None:
    tables = _entries("tables")

    with _admin(migrated_database) as connection:
        schema_acl = connection.execute(
            "SELECT has_schema_privilege(%s,'dante','USAGE'), "
            "has_schema_privilege(%s,'dante','CREATE')",
            (_RUNTIME_ROLE, _RUNTIME_ROLE),
        ).fetchone()
        assert schema_acl == (True, False)

        for table_name, entry in tables.items():
            table_privileges, column_privileges = _expected_runtime_acl(entry)
            relation = f"dante.{table_name}"

            actual_table = connection.execute(
                "SELECT " + ", ".join("has_table_privilege(%s,%s,%s)" for _ in _TABLE_PRIVILEGES),
                tuple(
                    value
                    for privilege in _TABLE_PRIVILEGES
                    for value in (_RUNTIME_ROLE, relation, privilege)
                ),
            ).fetchone()
            assert actual_table == tuple(
                privilege in table_privileges for privilege in _TABLE_PRIVILEGES
            ), table_name

            for column in map(str, (item["name"] for item in entry["structure"]["columns"])):
                actual_column = connection.execute(
                    "SELECT "
                    + ", ".join("has_column_privilege(%s,%s,%s,%s)" for _ in _COLUMN_PRIVILEGES),
                    tuple(
                        value
                        for privilege in _COLUMN_PRIVILEGES
                        for value in (_RUNTIME_ROLE, relation, column, privilege)
                    ),
                ).fetchone()
                expected_column = tuple(
                    privilege in table_privileges
                    or column in column_privileges.get(privilege, set())
                    for privilege in _COLUMN_PRIVILEGES
                )
                assert actual_column == expected_column, f"{table_name}.{column}"


def test_account_security_lock_capability_is_exact(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        function_acl = connection.execute(
            """
            SELECT
              pg_get_userbyid(p.proowner),
              p.prosecdef,
              p.provolatile,
              p.proparallel,
              p.proleakproof,
              p.proconfig,
              has_function_privilege('dante_runtime','dante.acquire_account_security_lock(uuid)','EXECUTE'),
              has_function_privilege('dante_migrator','dante.acquire_account_security_lock(uuid)','EXECUTE'),
              EXISTS (
                SELECT 1
                FROM aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) AS acl
                WHERE acl.grantee = 0 AND acl.privilege_type = 'EXECUTE'
              )
            FROM pg_proc p
            JOIN pg_namespace n ON n.oid = p.pronamespace
            WHERE n.nspname = 'dante'
              AND p.oid = to_regprocedure('dante.acquire_account_security_lock(uuid)')
            """
        ).fetchone()

    assert function_acl is not None
    assert function_acl[0:5] == ("dante_owner", True, "v", "u", False)
    assert function_acl[5] == ["search_path=pg_catalog, dante, pg_temp"]
    assert function_acl[6:9] == (True, False, False)


def test_m3_account_security_lock_is_narrow_and_transaction_scoped(
    migrated_database: Any,
) -> None:
    account_ref = uuid7()
    created_at = datetime.now(UTC)

    with _admin(migrated_database) as connection:
        connection.execute(
            """
            INSERT INTO dante.account(account_ref, status_code, created_at, disabled_at)
            VALUES (%s, 'active', %s, NULL)
            """,
            (account_ref, created_at),
        )

    runtime_kwargs = migrated_database.connection_kwargs(
        "dante_runtime",
        migrated_database.cluster.runtime_password,
    )
    with psycopg.connect(**runtime_kwargs) as runtime_connection:
        with pytest.raises(psycopg.errors.InsufficientPrivilege) as direct_lock_error:
            runtime_connection.execute(
                "SELECT account_ref FROM dante.account WHERE account_ref = %s FOR UPDATE",
                (account_ref,),
            )
        assert direct_lock_error.value.sqlstate == "42501"
        runtime_connection.rollback()

        runtime_connection.execute(
            "SELECT dante.acquire_account_security_lock(%s)",
            (account_ref,),
        )

        with _admin(migrated_database) as contender:
            with pytest.raises(psycopg.errors.LockNotAvailable) as lock_error:
                contender.execute(
                    "SELECT account_ref FROM dante.account WHERE account_ref = %s FOR UPDATE NOWAIT",
                    (account_ref,),
                )
            assert lock_error.value.sqlstate == "55P03"

            runtime_connection.rollback()

            acquired = contender.execute(
                "SELECT account_ref FROM dante.account WHERE account_ref = %s FOR UPDATE NOWAIT",
                (account_ref,),
            ).fetchone()
            assert acquired == (account_ref,)
