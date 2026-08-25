"""Real PostgreSQL acceptance tests for Alembic authority and drift detection."""

from typing import Any

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

pytestmark = pytest.mark.postgres

_EXPECTED_HEAD = "20260825_05"
_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


def _current_revision(database: Any) -> str | None:
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

        row = connection.execute("SELECT version_num FROM dante.alembic_version").fetchone()
        return None if row is None else str(row[0])


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
    assert _current_revision(provisioned_database) == _EXPECTED_HEAD


def test_cp6_head_round_trips_head_base_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, "head")
    assert _current_revision(provisioned_database) == _EXPECTED_HEAD

    command.downgrade(alembic_config, "base")
    assert _current_revision(provisioned_database) is None

    command.upgrade(alembic_config, "head")
    assert _current_revision(provisioned_database) == _EXPECTED_HEAD


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

    assert extensions == {"postgis", "vector", "pg_trgm", "unaccent", "pg_stat_statements"}


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
