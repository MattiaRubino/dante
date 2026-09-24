"""B08-A PostgreSQL proof for the Session core substrate and bounded capabilities."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

pytestmark = pytest.mark.postgres

_EXPECTED_REVISION = "20260924_60"
_SESSION_TABLES = frozenset(
    {
        "session",
        "session_timing_state",
        "session_timing_absolute",
        "session_timing_elapsed",
        "session_timing_pause",
        "session_timing_current_history",
    }
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


def test_b08_a_session_catalog_reuses_cp6_and_adds_bounded_subject_capabilities(
    migrated_database: Any,
) -> None:
    with _admin(migrated_database) as connection:
        revision = connection.execute("SELECT version_num FROM dante.alembic_version").fetchone()
        assert revision is not None
        assert revision[0] == _EXPECTED_REVISION

        tables = {
            row[0]
            for row in connection.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'dante'"
            )
        }
        assert _SESSION_TABLES <= tables

        session_columns = [
            row[0]
            for row in connection.execute(
                """
                SELECT column_name
                  FROM information_schema.columns
                 WHERE table_schema = 'dante' AND table_name = 'session'
                 ORDER BY ordinal_position
                """
            )
        ]
        assert session_columns == ["session_ref"]

        form = connection.execute(
            """
            SELECT pg_get_constraintdef(constraint_.oid)
              FROM pg_constraint AS constraint_
              JOIN pg_class AS relation ON relation.oid = constraint_.conrelid
              JOIN pg_namespace AS namespace ON namespace.oid = relation.relnamespace
             WHERE namespace.nspname = 'dante'
               AND relation.relname = 'session_timing_state'
               AND constraint_.conname = 'ck_session_timing_state_timing_form'
            """
        ).fetchone()
        assert form is not None
        definition = str(form[0])
        assert "timing_form_code" in definition
        assert "absolute" in definition
        assert "elapsed_only" in definition

        indexes = {
            row[0]
            for row in connection.execute(
                """
                SELECT indexname
                  FROM pg_indexes
                 WHERE schemaname = 'dante'
                   AND indexname IN (
                     'ux_session_timing_pause_open',
                     'ux_session_timing_current_history_open'
                   )
                """
            )
        }
        assert indexes == {
            "ux_session_timing_pause_open",
            "ux_session_timing_current_history_open",
        }

        subject_edges = connection.execute(
            """
            SELECT relation.relname
              FROM pg_class AS relation
              JOIN pg_namespace AS namespace ON namespace.oid = relation.relnamespace
             WHERE namespace.nspname = 'dante'
               AND relation.relkind = 'r'
               AND EXISTS (
                 SELECT 1
                   FROM pg_attribute AS session_column
                  WHERE session_column.attrelid = relation.oid
                    AND session_column.attname = 'session_ref'
                    AND NOT session_column.attisdropped
               )
               AND EXISTS (
                 SELECT 1
                   FROM pg_attribute AS subject_column
                  WHERE subject_column.attrelid = relation.oid
                    AND subject_column.attname IN (
                      'activity_ref', 'occurrence_ref', 'subject_native_ref'
                    )
                    AND NOT subject_column.attisdropped
               )
            """
        ).fetchall()
        assert {row[0] for row in subject_edges} == {
            "session_execution_subject",
            "session_start_operation",
        }

        absent = connection.execute(
            """
            SELECT procedure.proname
              FROM pg_proc AS procedure
              JOIN pg_namespace AS namespace ON namespace.oid = procedure.pronamespace
             WHERE namespace.nspname = 'dante'
               AND procedure.proname IN (
                 'start_self_activity_session',
                 'start_self_occurrence_session',
                 'pause_self_session',
                 'resume_self_session'
               )
            """
        ).fetchall()
        assert absent == []

        present = {
            row[0]
            for row in connection.execute(
                """
                SELECT procedure.proname
                  FROM pg_proc AS procedure
                  JOIN pg_namespace AS namespace ON namespace.oid = procedure.pronamespace
                 WHERE namespace.nspname = 'dante'
                   AND procedure.proname IN (
                     'start_self_session',
                     'end_self_session',
                     'list_self_subject_sessions',
                     'get_self_session'
                   )
                """
            )
        }
        assert present == {
            "start_self_session",
            "end_self_session",
            "list_self_subject_sessions",
            "get_self_session",
        }

        start_signatures = connection.execute(
            """
            SELECT pg_get_function_identity_arguments(procedure.oid)
              FROM pg_proc AS procedure
              JOIN pg_namespace AS namespace ON namespace.oid = procedure.pronamespace
             WHERE namespace.nspname = 'dante'
               AND procedure.proname = 'start_self_session'
            """
        ).fetchall()
        assert len(start_signatures) == 1
        assert str(start_signatures[0][0]).endswith(
            "requested_material_state_ref uuid, requested_subject_family text, "
            "requested_subject_native_ref uuid"
        )

        end_signatures = connection.execute(
            """
            SELECT pg_get_function_identity_arguments(procedure.oid)
              FROM pg_proc AS procedure
              JOIN pg_namespace AS namespace ON namespace.oid = procedure.pronamespace
             WHERE namespace.nspname = 'dante'
               AND procedure.proname = 'end_self_session'
            """
        ).fetchall()
        assert len(end_signatures) == 1
        assert str(end_signatures[0][0]).endswith(
            "requested_session_ref uuid, requested_expected_material_state_ref uuid, "
            "requested_resulting_material_state_ref uuid"
        )

        result_fk = connection.execute(
            """
            SELECT pg_get_constraintdef(constraint_.oid)
              FROM pg_constraint AS constraint_
              JOIN pg_class AS relation ON relation.oid = constraint_.conrelid
              JOIN pg_namespace AS namespace ON namespace.oid = relation.relnamespace
             WHERE namespace.nspname='dante'
               AND relation.relname='session_end_operation'
               AND constraint_.conname='fk_session_end_operation_resulting_state_address'
            """
        ).fetchone()
        assert result_fk is not None
        assert "resulting_material_state_ref" in str(result_fk[0])
        assert "material_state_address" in str(result_fk[0])
