"""Keep the B11-C catalog objects visible at the current candidate head."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import psycopg
import pytest

from dante.platform.database.mappings import MAPPED_TABLES

pytestmark = pytest.mark.postgres

_CURRENT_REVISION = "20260928_88"
_REPO_ROOT = Path(__file__).resolve().parents[5]
_DICTIONARY_ROOT = _REPO_ROOT / "docs" / "database" / "dictionary"
_B11_C_TABLES = {
    "schedule_reminder",
    "schedule_reminder_configuration_state",
    "schedule_reminder_current_history",
    "schedule_reminder_operation",
}
_B11_C_ROUTINES = {
    "_self_schedule_reminder_owned",
    "_schedule_reminder_start",
    "get_self_schedule_reminder",
    "configure_self_schedule_reminder",
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


def _dictionary_names(kind: str) -> set[str]:
    return {path.stem for path in (_DICTIONARY_ROOT / kind).glob("*.json")}


def _print_delta(label: str, values: set[str]) -> None:
    print(f"B11_CATALOG_{label}=" + json.dumps(sorted(values), separators=(",", ":")))


def test_b11_catalog_reconciliation_probe(migrated_database: Any) -> None:
    """Emit live-vs-Dictionary deltas while retaining B11-C object assertions."""
    dictionary = {
        kind: _dictionary_names(kind)
        for kind in ("tables", "views", "routines")
    }
    with _admin(migrated_database) as connection:
        revision = connection.execute(
            "SELECT version_num FROM dante.alembic_version"
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
        live = {
            "tables": {
                str(row[0])
                for row in connection.execute(
                    "SELECT tablename FROM pg_tables WHERE schemaname='dante' AND tablename<>'alembic_version'"
                )
            },
            "views": {
                str(row[0])
                for row in connection.execute(
                    "SELECT viewname FROM pg_views WHERE schemaname='dante'"
                )
            },
            "routines": {
                str(row[0])
                for row in connection.execute(
                    "SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'"
                )
            },
            "constraints": {
                str(row[0])
                for row in connection.execute(
                    "SELECT con.conname FROM pg_constraint con JOIN pg_class c ON c.oid=con.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND c.relname<>'alembic_version' AND con.contype IN ('p','u','f','c')"
                )
            },
            "indexes": {
                str(row[0])
                for row in connection.execute(
                    "SELECT indexname FROM pg_indexes WHERE schemaname='dante' AND tablename<>'alembic_version'"
                )
            },
            "triggers": {
                str(row[0])
                for row in connection.execute(
                    "SELECT t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante' AND NOT t.tgisinternal"
                )
            },
        }

    assert revision == (_CURRENT_REVISION,)
    assert topology is not None
    assert _B11_C_TABLES <= live["tables"]
    assert _B11_C_ROUTINES <= live["routines"]
    assert _B11_C_TABLES <= {table.name for table in MAPPED_TABLES}

    print("B11_CATALOG_REVISION=" + revision[0])
    print("B11_CATALOG_TOPOLOGY=" + "|".join(str(value) for value in topology))
    for kind in ("tables", "views", "routines"):
        _print_delta(f"LIVE_{kind.upper()}_MINUS_DICTIONARY", live[kind] - dictionary[kind])
        _print_delta(f"DICTIONARY_{kind.upper()}_MINUS_LIVE", dictionary[kind] - live[kind])
