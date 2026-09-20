"""Focused PostgreSQL catalog/ACL proof for B04-E duration constraints."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

pytestmark = pytest.mark.postgres

_EXPECTED_REVISION = "20260920_42"
_EXPECTED_TOPOLOGY = (116, 5, 44, 90, 233, 153, 331, 0, 0, 0)


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


@pytest.mark.postgres
def test_b04_e_duration_catalog_and_acl(migrated_database: Any) -> None:
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
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname='dante'"
            )
        }
        routines = {
            row[0]
            for row in connection.execute(
                "SELECT p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='dante'"
            )
        }
        triggers = {
            row[0]
            for row in connection.execute(
                """
                SELECT t.tgname
                  FROM pg_trigger t
                  JOIN pg_class c ON c.oid=t.tgrelid
                  JOIN pg_namespace n ON n.oid=c.relnamespace
                 WHERE n.nspname='dante' AND NOT t.tgisinternal
                """
            )
        }
        family_check = connection.execute(
            """
            SELECT pg_get_constraintdef(c.oid)
              FROM pg_constraint c
              JOIN pg_class r ON r.oid=c.conrelid
              JOIN pg_namespace n ON n.oid=r.relnamespace
             WHERE n.nspname='dante'
               AND r.relname='temporal_constraint_state'
               AND c.conname='ck_temporal_constraint_state_family'
            """
        ).fetchone()
        runtime_table_acl = connection.execute(
            """
            SELECT has_table_privilege('dante_runtime','dante.temporal_constraint_duration_state','SELECT'),
                   has_table_privilege('dante_runtime','dante.temporal_constraint_duration_state','INSERT'),
                   has_table_privilege('dante_runtime','dante.temporal_constraint_duration_state','UPDATE'),
                   has_table_privilege('dante_runtime','dante.temporal_constraint_duration_state','DELETE')
            """
        ).fetchone()
        private_acl = connection.execute(
            """
            SELECT has_table_privilege('dante_runtime','dante.temporal_constraint_current_history','SELECT'),
                   has_table_privilege('dante_runtime','dante.temporal_constraint_mutation_operation','SELECT')
            """
        ).fetchone()
        runtime_mutate = connection.execute(
            """
            SELECT has_function_privilege(
              'dante_runtime',
              'dante.mutate_self_schedule_duration_constraint(uuid,text,text,text,uuid,uuid,uuid,uuid,text,text,text,bigint)',
              'EXECUTE'
            )
            """
        ).fetchone()
        runtime_assert = connection.execute(
            """
            SELECT has_function_privilege(
              'dante_runtime',
              'dante.assert_absolute_schedule_move_hard_admissible(uuid,timestamp with time zone,timestamp with time zone)',
              'EXECUTE'
            )
            """
        ).fetchone()

    assert revision == (_EXPECTED_REVISION,)
    assert topology == _EXPECTED_TOPOLOGY
    print("B04_E_LIVE_TOPOLOGY=" + "|".join(str(value) for value in topology))
    assert "temporal_constraint_duration_state" in tables
    assert "mutate_self_schedule_duration_constraint" in routines
    assert "assert_absolute_schedule_move_hard_admissible" in routines
    assert "ctrg_temporal_constraint_duration_state_rule_totality" in triggers
    assert family_check is not None and "duration" in family_check[0]
    assert runtime_table_acl == (True, False, False, False)
    assert private_acl == (False, False)
    assert runtime_mutate == (True,)
    assert runtime_assert == (False,)
