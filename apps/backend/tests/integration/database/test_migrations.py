"""Real PostgreSQL acceptance tests for Alembic authority and drift detection."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

pytestmark = pytest.mark.postgres

_EXPECTED_HEAD = "20260904_17"
_CP6_HEAD = "20260826_08"
_RECOVERY_HEAD = "20260830_09"
_ACCESS_HEAD = "20260904_16"
_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


def _current_revisions(database: Any) -> set[str]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        identity = connection.execute(
            "SELECT session_user, current_user, current_setting('search_path')"
        ).fetchone()
        assert identity is not None
        assert identity[0:2] == ("dante_migrator", "dante_migrator")
        assert str(identity[2]).replace(" ", "") == _TRUSTED_SEARCH_PATH

        connection.execute("SET ROLE dante_owner")
        elevated = connection.execute(
            "SELECT session_user, current_user, current_setting('search_path')"
        ).fetchone()
        assert elevated is not None
        assert elevated[0:2] == ("dante_migrator", "dante_owner")
        assert str(elevated[2]).replace(" ", "") == _TRUSTED_SEARCH_PATH

        rows = connection.execute(
            "SELECT version_num FROM dante.alembic_version ORDER BY version_num"
        ).fetchall()
        return {str(row[0]) for row in rows}


def _recovery_row_snapshot(
    connection: psycopg.Connection[Any],
    *,
    person_ref: UUID,
    live_session_ref: UUID,
    live_state_ref: UUID,
    retired_session_ref: UUID,
    retired_state_ref: UUID,
    suppression_ref: UUID,
) -> tuple[Any, ...]:
    row = connection.execute(
        """
        SELECT
          (SELECT count(*) FROM dante.person WHERE person_ref=%s),
          (SELECT count(*) FROM dante.session WHERE session_ref=%s),
          (SELECT started_at FROM dante.session_timing_absolute WHERE material_state_ref=%s),
          (SELECT count(*) FROM dante.native_current_material_state
             WHERE native_owner_ref=%s AND facet_code='session.timing'
               AND material_state_ref=%s),
          (SELECT count(*) FROM dante.session_timing_current_history
             WHERE session_ref=%s AND material_state_ref=%s),
          (SELECT count(*) FROM dante.session WHERE session_ref=%s),
          (SELECT retirement_code FROM dante.material_state_retirement
             WHERE material_state_ref=%s AND recovery_suppression_ref=%s),
          (SELECT count(*) FROM dante.session_timing_absolute WHERE material_state_ref=%s),
          (SELECT count(*) FROM dante.native_current_material_state
             WHERE native_owner_ref=%s AND facet_code='session.timing'
               AND material_state_ref=%s),
          (SELECT count(*) FROM dante.session_timing_current_history
             WHERE session_ref=%s AND material_state_ref=%s)
        """,
        (
            person_ref,
            live_session_ref,
            live_state_ref,
            live_session_ref,
            live_state_ref,
            live_session_ref,
            live_state_ref,
            retired_session_ref,
            retired_state_ref,
            suppression_ref,
            retired_state_ref,
            retired_session_ref,
            retired_state_ref,
            retired_session_ref,
            retired_state_ref,
        ),
    ).fetchone()
    assert row is not None
    return tuple(row)


def test_fresh_database_reaches_the_single_repository_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    with psycopg.connect(
        host=provisioned_database.cluster.host,
        port=provisioned_database.cluster.port,
        dbname=provisioned_database.name,
        user=provisioned_database.cluster.admin_user,
        password=provisioned_database.cluster.admin_password,
    ) as connection:
        before = connection.execute("SELECT to_regclass('dante.alembic_version')").fetchone()
        assert before == (None,)

    script = ScriptDirectory.from_config(alembic_config)
    assert script.get_heads() == [_EXPECTED_HEAD]

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_EXPECTED_HEAD}


def test_repository_head_round_trips_head_base_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_EXPECTED_HEAD}

    command.downgrade(alembic_config, "base")
    assert _current_revisions(provisioned_database) == set()

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_EXPECTED_HEAD}


def test_recovery_history_remains_independently_reachable(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _RECOVERY_HEAD)
    assert _current_revisions(provisioned_database) == {_RECOVERY_HEAD}

    command.downgrade(alembic_config, _CP6_HEAD)
    assert _current_revisions(provisioned_database) == {_CP6_HEAD}

    command.upgrade(alembic_config, _RECOVERY_HEAD)
    assert _current_revisions(provisioned_database) == {_RECOVERY_HEAD}


def test_existing_access_head_converges_forward_to_merge_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _ACCESS_HEAD)
    assert _current_revisions(provisioned_database) == {_ACCESS_HEAD}

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_EXPECTED_HEAD}


def test_existing_recovery_head_converges_forward_to_merge_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _RECOVERY_HEAD)
    assert _current_revisions(provisioned_database) == {_RECOVERY_HEAD}

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_EXPECTED_HEAD}


def test_existing_recovery_rows_survive_forward_convergence_to_merge_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    """Prove Access/Email additions do not overwrite accepted Recovery-era rows."""

    command.upgrade(alembic_config, _RECOVERY_HEAD)
    assert _current_revisions(provisioned_database) == {_RECOVERY_HEAD}

    person_ref = uuid7()
    live_session_ref = uuid7()
    live_state_ref = uuid7()
    retired_session_ref = uuid7()
    retired_state_ref = uuid7()
    suppression_ref = uuid7()
    live_started_at = datetime(2026, 9, 4, 8, 0, tzinfo=UTC)
    retired_started_at = datetime(2026, 9, 4, 8, 5, tzinfo=UTC)
    retired_at = datetime(2026, 9, 4, 8, 10, tzinfo=UTC)

    connection_kwargs = provisioned_database.connection_kwargs(
        "dante_migrator",
        provisioned_database.cluster.migrator_password,
    )
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.person(person_ref) VALUES (%s)",
                (person_ref,),
            )

            for session_ref, state_ref, started_at in (
                (live_session_ref, live_state_ref, live_started_at),
                (retired_session_ref, retired_state_ref, retired_started_at),
            ):
                connection.execute(
                    "INSERT INTO dante.session(session_ref) VALUES (%s)",
                    (session_ref,),
                )
                connection.execute(
                    "INSERT INTO dante.native_address(native_ref,owner_family) "
                    "VALUES (%s,'session')",
                    (session_ref,),
                )
                connection.execute(
                    "INSERT INTO dante.material_state_address"
                    "(material_state_ref,native_owner_ref,facet_code) "
                    "VALUES (%s,%s,'session.timing')",
                    (state_ref, session_ref),
                )
                connection.execute(
                    "INSERT INTO dante.session_timing_state"
                    "(material_state_ref,session_ref,timing_form_code) "
                    "VALUES (%s,%s,'absolute')",
                    (state_ref, session_ref),
                )
                connection.execute(
                    "INSERT INTO dante.session_timing_absolute"
                    "(material_state_ref,started_at,start_precision_code) "
                    "VALUES (%s,%s,'exact')",
                    (state_ref, started_at),
                )
                connection.execute(
                    "INSERT INTO dante.native_current_material_state"
                    "(native_owner_ref,facet_code,material_state_ref) "
                    "VALUES (%s,'session.timing',%s)",
                    (session_ref, state_ref),
                )
                connection.execute(
                    "INSERT INTO dante.session_timing_current_history"
                    "(session_ref,material_state_ref,current_from_at) VALUES (%s,%s,%s)",
                    (session_ref, state_ref, started_at),
                )

        with connection.transaction():
            connection.execute(
                "INSERT INTO dante.material_state_retirement"
                "(material_state_ref,retirement_code,retired_at,recovery_suppression_ref) "
                "VALUES (%s,'redacted',%s,%s)",
                (retired_state_ref, retired_at, suppression_ref),
            )
            connection.execute(
                "DELETE FROM dante.session_timing_absolute WHERE material_state_ref=%s",
                (retired_state_ref,),
            )

        before = _recovery_row_snapshot(
            connection,
            person_ref=person_ref,
            live_session_ref=live_session_ref,
            live_state_ref=live_state_ref,
            retired_session_ref=retired_session_ref,
            retired_state_ref=retired_state_ref,
            suppression_ref=suppression_ref,
        )

    assert before == (
        1,
        1,
        live_started_at,
        1,
        1,
        1,
        "redacted",
        0,
        1,
        1,
    )

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_EXPECTED_HEAD}

    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        after = _recovery_row_snapshot(
            connection,
            person_ref=person_ref,
            live_session_ref=live_session_ref,
            live_state_ref=live_state_ref,
            retired_session_ref=retired_session_ref,
            retired_state_ref=retired_state_ref,
            suppression_ref=suppression_ref,
        )

    assert after == before


def test_alembic_check_reports_no_dante_schema_drift_with_extensions_present(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, "head")
    command.check(alembic_config)

    with psycopg.connect(
        host=provisioned_database.cluster.host,
        port=provisioned_database.cluster.port,
        dbname=provisioned_database.name,
        user=provisioned_database.cluster.admin_user,
        password=provisioned_database.cluster.admin_password,
    ) as connection:
        extensions = {
            str(row[0])
            for row in connection.execute(
                "SELECT extname FROM pg_extension "
                "WHERE extname IN "
                "('postgis', 'vector', 'pg_trgm', 'unaccent', 'pg_stat_statements')"
            )
        }

    assert extensions == {
        "postgis",
        "vector",
        "pg_trgm",
        "unaccent",
        "pg_stat_statements",
    }


def test_alembic_rejects_injected_non_migrator_identity(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    alembic_config.attributes["database_url"] = provisioned_database.sqlalchemy_url(
        provisioned_database.cluster.admin_user,
        provisioned_database.cluster.admin_password,
    )

    with pytest.raises(RuntimeError, match="authenticate exactly as dante_migrator"):
        command.upgrade(alembic_config, "head")
