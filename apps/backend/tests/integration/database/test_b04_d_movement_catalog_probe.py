"""Focused catalog/ACL proof for B04-D Movement Policy and governed Schedule moves."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

pytestmark = pytest.mark.postgres

# Current candidate must still preserve every B04-D table and runtime ACL.
_EXPECTED_REVISION = "20260920_46"
_EXPECTED_TOPOLOGY = (123, 5, 54, 90, 245, 170, 354, 0, 0, 0)

_B04_D_TABLES = {
    "schedule_movement_policy_state",
    "schedule_movement_policy_current_history",
    "schedule_movement_policy_mutation_operation",
    "schedule_move_proposal",
    "schedule_move_request_operation",
    "schedule_move_accept_operation",
}

_RUNTIME_ENTRYPOINTS = {
    "mutate_self_schedule_movement_policy(uuid,text,text,text,uuid,uuid,uuid,text,text)",
    "resolve_self_schedule_movement_policy(uuid,uuid)",
    "request_self_absolute_schedule_move(uuid,text,text,uuid,uuid,timestamp with time zone,timestamp with time zone,uuid,uuid)",
    "accept_self_absolute_schedule_move_proposal(uuid,text,text,uuid,uuid)",
}

_INTERNAL_ROUTINES = {
    "enforce_schedule_movement_policy_history()",
    "assert_absolute_schedule_move_hard_admissible(uuid,timestamp with time zone,timestamp with time zone)",
    "apply_governed_absolute_schedule_move(uuid,uuid,uuid,timestamp with time zone,timestamp with time zone,timestamp with time zone)",
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


@pytest.mark.postgres
def test_b04_d_revision_and_topology(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        revision = connection.execute("SELECT version_num FROM dante.alembic_version").fetchone()
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
               WHERE n.nspname='dante' AND t.typtype='e'),
              (SELECT count(*) FROM pg_type t JOIN pg_namespace n ON n.oid=t.typnamespace
               WHERE n.nspname='dante' AND t.typtype='d'),
              (SELECT count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='dante' AND c.relkind IN ('m','p'))
            """
        ).fetchone()
        tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname='dante'"
            )
        }

    assert revision == (_EXPECTED_REVISION,)
    assert topology == _EXPECTED_TOPOLOGY
    assert _B04_D_TABLES <= tables


@pytest.mark.postgres
def test_b04_d_runtime_has_capabilities_not_table_mutation(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        for table in sorted(_B04_D_TABLES):
            relation = f"dante.{table}"
            privileges = connection.execute(
                """
                SELECT has_table_privilege('dante_runtime',%s,'SELECT'),
                       has_table_privilege('dante_runtime',%s,'INSERT'),
                       has_table_privilege('dante_runtime',%s,'UPDATE'),
                       has_table_privilege('dante_runtime',%s,'DELETE')
                """,
                (relation, relation, relation, relation),
            ).fetchone()
            assert privileges == (False, False, False, False), table

        for signature in sorted(_RUNTIME_ENTRYPOINTS):
            privileges = connection.execute(
                """
                SELECT has_function_privilege('dante_runtime','dante.' || %s,'EXECUTE'),
                       has_function_privilege('dante_migrator','dante.' || %s,'EXECUTE')
                """,
                (signature, signature),
            ).fetchone()
            assert privileges == (True, False), signature

        for signature in sorted(_INTERNAL_ROUTINES):
            privileges = connection.execute(
                """
                SELECT has_function_privilege('dante_runtime','dante.' || %s,'EXECUTE'),
                       EXISTS (
                         SELECT 1
                           FROM pg_proc p
                           JOIN pg_namespace n ON n.oid=p.pronamespace
                           CROSS JOIN LATERAL aclexplode(COALESCE(p.proacl, acldefault('f',p.proowner))) acl
                          WHERE n.nspname='dante'
                            AND p.oid=to_regprocedure('dante.' || %s)
                            AND acl.grantee=0
                            AND acl.privilege_type='EXECUTE'
                       )
                """,
                (signature, signature),
            ).fetchone()
            assert privileges == (False, False), signature
