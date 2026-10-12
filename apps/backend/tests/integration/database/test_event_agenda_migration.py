"""B03-D migration proof for Event-internal Agenda persistence."""

from typing import Any
from uuid import uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import DBAPIError

pytestmark = pytest.mark.postgres

_HEAD = "20260917_29"
_PARENT = "20260917_28"
_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


def _current_revision(database: Any) -> str:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        identity = connection.execute(
            "SELECT session_user,current_user,current_setting('search_path')"
        ).fetchone()
        assert identity is not None
        assert identity[0:2] == ("dante_migrator", "dante_migrator")
        assert str(identity[2]).replace(" ", "") == _TRUSTED_SEARCH_PATH
        connection.execute("SET ROLE dante_owner")
        row = connection.execute(
            "SELECT version_num FROM dante.alembic_version"
        ).fetchone()
    assert row is not None
    return str(row[0])


def test_b03d_empty_head_round_trips_to_parent_and_back(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HEAD)
    assert _current_revision(provisioned_database) == _HEAD

    command.downgrade(alembic_config, _PARENT)
    assert _current_revision(provisioned_database) == _PARENT

    with psycopg.connect(
        host=provisioned_database.cluster.host,
        port=provisioned_database.cluster.port,
        dbname=provisioned_database.name,
        user=provisioned_database.cluster.admin_user,
        password=provisioned_database.cluster.admin_password,
    ) as connection:
        absent = connection.execute(
            """
            SELECT
              to_regclass('dante.event_agenda_part'),
              to_regclass('dante.event_agenda_current'),
              to_regclass('dante.event_agenda_mutation_operation'),
              to_regprocedure('dante.create_self_event_with_agenda(uuid,text,text,uuid,text,text[])'),
              to_regprocedure('dante.replace_self_event_agenda(uuid,text,text,uuid,bigint,text[])')
            """
        ).fetchone()
    assert absent == (None, None, None, None, None)

    command.upgrade(alembic_config, _HEAD)
    assert _current_revision(provisioned_database) == _HEAD


def test_b03d_downgrade_refuses_to_discard_canonical_event_agenda(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HEAD)
    assert _current_revision(provisioned_database) == _HEAD

    person_ref = uuid7()
    event_ref = uuid7()
    connection_kwargs = provisioned_database.connection_kwargs(
        "dante_migrator",
        provisioned_database.cluster.migrator_password,
    )

    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute(
            "INSERT INTO dante.person(person_ref) VALUES (%s)",
            (person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (person_ref,),
        )
        created = connection.execute(
            """
            SELECT event_ref,agenda_revision,agenda_parts,replayed
              FROM dante.create_self_event_with_agenda(%s,%s,%s,%s,%s,%s)
            """,
            (
                person_ref,
                "migration-proof:b03-d:event",
                "a" * 64,
                event_ref,
                "B03-D downgrade guard",
                ["Apertura", "Decisione"],
            ),
        ).fetchone()
        assert created == (event_ref, 0, ["Apertura", "Decisione"], False)

    with pytest.raises(DBAPIError, match="B03-D downgrade refused"):
        command.downgrade(alembic_config, _PARENT)

    assert _current_revision(provisioned_database) == _HEAD
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.event_expectation WHERE event_ref=%s),
              (SELECT array_agg(content ORDER BY position)
                 FROM dante.event_agenda_part WHERE event_ref=%s),
              (SELECT accepted_agenda_parts
                 FROM dante.event_create_operation
                WHERE self_person_ref=%s
                  AND operation_id='migration-proof:b03-d:event')
            """,
            (event_ref, event_ref, person_ref),
        ).fetchone()
    assert preserved == (1, ["Apertura", "Decisione"], ["Apertura", "Decisione"])
