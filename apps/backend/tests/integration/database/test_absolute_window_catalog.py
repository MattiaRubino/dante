"""Focused live-catalog proof for the B04-C absolute-window activation."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.platform.database.mappings import MAPPED_TABLES

pytestmark = pytest.mark.postgres

_CURRENT_REVISION = "20260919_36"
_WINDOW_TABLES = {
    "temporal_constraint_window_state",
    "temporal_constraint_window_absolute_state",
}
_WINDOW_MUTATE_SIGNATURE = (
    "dante.mutate_self_absolute_window_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,text,text,timestamptz,timestamptz)"
)


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def test_b04_c_window_catalog_probe(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        revision = connection.execute(
            "SELECT version_num FROM dante.alembic_version"
        ).fetchone()
        topology = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relkind='r' AND c.relname<>'alembic_version'),
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relkind='v'),
              (SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
               WHERE n.nspname='dante'),
              (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid
               JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND NOT t.tgisinternal),
              (SELECT count(*) FROM pg_index i JOIN pg_class c ON c.oid=i.indrelid
               JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relname<>'alembic_version'),
              (SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace
               WHERE n.nspname='dante' AND c.contype='f'),
              (SELECT count(*) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace
               WHERE n.nspname='dante' AND c.contype='c'),
              (SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
               WHERE n.nspname='dante' AND t.typtype IN ('d','e')),
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relkind IN ('S','m','p')),
              (SELECT count(*) FROM pg_policy p JOIN pg_class c ON c.oid=p.polrelid
               JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='dante')
            """
        ).fetchone()
        table_owners = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT tablename,tableowner FROM pg_tables "
                "WHERE schemaname='dante' AND tablename = ANY(%s)",
                (sorted(_WINDOW_TABLES),),
            )
        }
        window_acl = {
            str(row[0]): tuple(bool(value) for value in row[1:])
            for row in connection.execute(
                """
                SELECT c.relname,
                       has_table_privilege('dante_runtime',c.oid,'SELECT'),
                       has_table_privilege('dante_runtime',c.oid,'INSERT'),
                       has_table_privilege('dante_runtime',c.oid,'UPDATE'),
                       has_table_privilege('dante_runtime',c.oid,'DELETE')
                FROM pg_class c
                JOIN pg_namespace n ON n.oid=c.relnamespace
                WHERE n.nspname='dante' AND c.relname = ANY(%s)
                """,
                (sorted(_WINDOW_TABLES),),
            )
        }
        private_acl = connection.execute(
            """
            SELECT
              has_table_privilege('dante_runtime','dante.temporal_constraint_current_history','SELECT'),
              has_table_privilege('dante_runtime','dante.temporal_constraint_mutation_operation','SELECT')
            """
        ).fetchone()
        mutate_security = connection.execute(
            """
            SELECT pg_get_userbyid(p.proowner),p.prosecdef,p.provolatile,p.proparallel,
                   p.proleakproof,p.proconfig,
                   has_function_privilege('dante_runtime',p.oid,'EXECUTE'),
                   has_function_privilege('dante_migrator',p.oid,'EXECUTE'),
                   EXISTS (
                     SELECT 1 FROM aclexplode(COALESCE(p.proacl,acldefault('f',p.proowner))) acl
                     WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE'
                   )
            FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
            WHERE n.nspname='dante' AND p.oid=to_regprocedure(%s)
            """,
            (_WINDOW_MUTATE_SIGNATURE,),
        ).fetchone()
        trigger_names = {
            str(row[0])
            for row in connection.execute(
                """
                SELECT t.tgname FROM pg_trigger t
                JOIN pg_class c ON c.oid=t.tgrelid
                JOIN pg_namespace n ON n.oid=c.relnamespace
                WHERE n.nspname='dante' AND c.relname = ANY(%s) AND NOT t.tgisinternal
                """,
                (sorted(_WINDOW_TABLES),),
            )
        }

    assert revision == (_CURRENT_REVISION,)
    assert topology is not None
    print("B04_C_LIVE_TOPOLOGY=" + "|".join(str(value) for value in topology))
    assert table_owners == {(table, "dante_owner") for table in _WINDOW_TABLES}
    assert window_acl == {
        table: (True, False, False, False) for table in _WINDOW_TABLES
    }
    assert private_acl == (False, False)
    assert mutate_security == (
        "dante_owner",
        True,
        "v",
        "u",
        False,
        ["search_path=pg_catalog, dante, pg_temp"],
        True,
        False,
        False,
    )
    assert trigger_names == {
        "ctrg_temporal_constraint_window_state_rule_totality",
        "ctrg_temporal_constraint_window_absolute_state_rule_totality",
    }

    mapped = {table.name for table in MAPPED_TABLES}
    assert _WINDOW_TABLES <= mapped
