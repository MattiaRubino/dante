"""B03-A Event migration integrity proof on real PostgreSQL."""

from typing import Any
from uuid import uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import DBAPIError

pytestmark = pytest.mark.postgres

_HEAD = "20260916_27"
_PARENT = "20260915_26"


def _current_revision(database: Any) -> str:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        row = connection.execute(
            "SELECT version_num FROM dante.alembic_version"
        ).fetchone()
    assert row is not None
    return str(row[0])


def test_b03_event_downgrade_refuses_to_discard_canonical_expectation(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, "head")
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
            SELECT event_ref,title,replayed
            FROM dante.create_self_event(%s,%s,%s,%s,%s)
            """,
            (
                person_ref,
                "migration-proof:b03-a",
                "e" * 64,
                event_ref,
                "Canonical Event downgrade guard",
            ),
        ).fetchone()
        assert created == (event_ref, "Canonical Event downgrade guard", False)

    with pytest.raises(DBAPIError, match="B03-A downgrade refused"):
        command.downgrade(alembic_config, _PARENT)

    assert _current_revision(provisioned_database) == _HEAD

    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.event WHERE event_ref=%s),
              (SELECT count(*) FROM dante.native_address
                 WHERE native_ref=%s AND owner_family='event'),
              (SELECT count(*) FROM dante.event_expectation
                 WHERE event_ref=%s AND self_person_ref=%s),
              (SELECT count(*) FROM dante.event_create_operation
                 WHERE event_ref=%s AND self_person_ref=%s
                   AND operation_id='migration-proof:b03-a')
            """,
            (
                event_ref,
                event_ref,
                event_ref,
                person_ref,
                event_ref,
                person_ref,
            ),
        ).fetchone()

    assert preserved == (1, 1, 1, 1)
