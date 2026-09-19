"""HEAD-level PostgreSQL structural proof for the B04 Temporal Constraint core."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import psycopg
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory

from dante.platform.database.mappings import MAPPED_TABLES

pytestmark = pytest.mark.postgres

_CURRENT_REVISION = "20260919_36"
_REPO_ROOT = Path(__file__).resolve().parents[5]
_B04_TABLES = {
    "temporal_constraint",
    "temporal_constraint_state",
    "temporal_constraint_boundary_state",
    "temporal_constraint_boundary_absolute_state",
    "temporal_constraint_window_state",
    "temporal_constraint_window_absolute_state",
    "temporal_constraint_current_history",
    "temporal_constraint_mutation_operation",
}
_B04_RUNTIME_READ_TABLES = {
    "temporal_constraint",
    "temporal_constraint_state",
    "temporal_constraint_boundary_state",
    "temporal_constraint_boundary_absolute_state",
    "temporal_constraint_window_state",
    "temporal_constraint_window_absolute_state",
}
_B04_TRIGGERS = {
    "trg_temporal_constraint_native_ref": (
        False, False, False, "enforce_native_ref_eligibility"
    ),
    "ctrg_temporal_constraint_owner_complete": (
        True, True, True, "enforce_owner_creation_completeness"
    ),
    "ctrg_temporal_constraint_state_state_totality": (
        True, True, True, "enforce_material_state_totality"
    ),
    "ctrg_temporal_constraint_state_rule_totality": (
        True, True, True, "enforce_temporal_constraint_rule_totality"
    ),
    "ctrg_temporal_constraint_boundary_state_rule_totality": (
        True, True, True, "enforce_temporal_constraint_rule_totality"
    ),
    "ctrg_temporal_constraint_boundary_absolute_state_rule_totality": (
        True, True, True, "enforce_temporal_constraint_rule_totality"
    ),
    "ctrg_temporal_constraint_window_state_rule_totality": (
        True, True, True, "enforce_temporal_constraint_rule_totality"
    ),
    "ctrg_temporal_constraint_window_absolute_state_rule_totality": (
        True, True, True, "enforce_temporal_constraint_rule_totality"
    ),
    "ctrg_temporal_constraint_current_history_equivalence": (
        True, True, True, "enforce_current_history_equivalence"
    ),
}
_MUTATE_SIGNATURES = (
    "dante.mutate_self_absolute_earliest_start_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,timestamptz)",
    "dante.mutate_self_absolute_boundary_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,text,text,timestamptz)",
    "dante.mutate_self_absolute_window_constraint("
    "uuid,text,text,text,uuid,uuid,uuid,uuid,text,text,text,timestamptz,timestamptz)",
)
_SHARED_ROUTINES = (
    "dante.enforce_scoped_address_owner()",
    "dante.enforce_native_ref_eligibility()",
    "dante.enforce_material_state_totality()",
    "dante.enforce_current_history_equivalence()",
    "dante.enforce_owner_creation_completeness()",
    "dante.enforce_temporal_constraint_rule_totality()",
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


def _routine_security(
    connection: psycopg.Connection[Any], signature: str
) -> tuple[object, ...] | None:
    return connection.execute(
        """
        SELECT
          pg_get_userbyid(p.proowner),
          p.prosecdef,
          p.provolatile,
          p.proparallel,
          p.proleakproof,
          p.proconfig,
          has_function_privilege('dante_runtime',p.oid,'EXECUTE'),
          has_function_privilege('dante_migrator',p.oid,'EXECUTE'),
          EXISTS (
            SELECT 1
            FROM aclexplode(COALESCE(p.proacl,acldefault('f',p.proowner))) acl
            WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE'
          )
        FROM pg_proc p
        JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE n.nspname='dante' AND p.oid=to_regprocedure(%s)
        """,
        (signature,),
    ).fetchone()


def test_b04_catalog_surface_and_live_topology(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        revision = connection.execute(
            "SELECT version_num FROM dante.alembic_version"
        ).fetchone()
        b04_tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname='dante' AND tablename LIKE 'temporal_constraint%'"
            )
        }
        owners = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT tablename,tableowner FROM pg_tables "
                "WHERE schemaname='dante' AND tablename LIKE 'temporal_constraint%'"
            )
        }
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

    assert revision == (_CURRENT_REVISION,)
    assert b04_tables == _B04_TABLES
    assert owners == {(table, "dante_owner") for table in _B04_TABLES}
    assert topology is not None
    assert topology == (109, 5, 35, 87, 214, 131, 312, 0, 0, 0)
    print("B04_LIVE_TOPOLOGY=" + "|".join(str(value) for value in topology))

    config = Config(toml_file=str(_REPO_ROOT / "apps" / "backend" / "pyproject.toml"))
    scripts = ScriptDirectory.from_config(config)
    assert scripts.get_heads() == [_CURRENT_REVISION]


def test_b04_triggers_and_routine_acl_are_exact(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        trigger_rows = {
            str(row[0]): (bool(row[1]), bool(row[2]), bool(row[3]), str(row[4]))
            for row in connection.execute(
                """
                SELECT t.tgname,
                       t.tgconstraint<>0,
                       COALESCE(con.condeferrable,false),
                       COALESCE(con.condeferred,false),
                       p.proname
                FROM pg_trigger t
                JOIN pg_class c ON c.oid=t.tgrelid
                JOIN pg_namespace n ON n.oid=c.relnamespace
                JOIN pg_proc p ON p.oid=t.tgfoid
                LEFT JOIN pg_constraint con ON con.oid=t.tgconstraint
                WHERE n.nspname='dante'
                  AND c.relname = ANY(%s)
                  AND NOT t.tgisinternal
                """,
                (sorted(_B04_TABLES),),
            )
        }
        direct_acl = {
            (str(row[0]), str(row[1]), str(row[2]))
            for row in connection.execute(
                """
                SELECT c.relname,COALESCE(r.rolname,'PUBLIC'),acl.privilege_type
                FROM pg_class c
                JOIN pg_namespace n ON n.oid=c.relnamespace
                CROSS JOIN LATERAL aclexplode(
                    COALESCE(c.relacl,acldefault('r',c.relowner))
                ) acl
                LEFT JOIN pg_roles r ON r.oid=acl.grantee
                WHERE n.nspname='dante'
                  AND c.relname = ANY(%s)
                  AND (acl.grantee=0 OR r.rolname IN ('dante_runtime','dante_migrator'))
                """,
                (sorted(_B04_TABLES),),
            )
        }
        mutation_security = {
            signature: _routine_security(connection, signature)
            for signature in _MUTATE_SIGNATURES
        }
        shared_security = {
            signature: _routine_security(connection, signature)
            for signature in _SHARED_ROUTINES
        }

    assert trigger_rows == _B04_TRIGGERS
    assert direct_acl == {
        (table, "dante_runtime", "SELECT") for table in _B04_RUNTIME_READ_TABLES
    }
    assert all(
        security
        == (
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
        for security in mutation_security.values()
    )
    assert all(
        security
        == (
            "dante_owner",
            False,
            "v",
            "u",
            False,
            ["search_path=pg_catalog, dante, pg_temp"],
            False,
            False,
            False,
        )
        for security in shared_security.values()
    )


def test_b04_sqlalchemy_registration_is_exact() -> None:
    mapped = {table.name: table for table in MAPPED_TABLES}
    assert _B04_TABLES <= set(mapped)
    assert {name for name in mapped if name.startswith("temporal_constraint")} == _B04_TABLES
    assert all(mapped[name].schema == "dante" for name in _B04_TABLES)
