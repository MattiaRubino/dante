"""B03-B migration proof: Event-owned Schedule data cannot be stranded at _27."""

from typing import Any
from uuid import uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import DBAPIError

pytestmark = pytest.mark.postgres

_HEAD = "20260917_28"
_PARENT = "20260916_27"
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


def test_b03b_downgrade_refuses_to_strand_event_owned_schedule(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HEAD)
    assert _current_revision(provisioned_database) == _HEAD

    person_ref = uuid7()
    event_ref = uuid7()
    schedule_ref = uuid7()
    state_ref = uuid7()
    connection_kwargs = provisioned_database.connection_kwargs(
        "dante_migrator",
        provisioned_database.cluster.migrator_password,
    )

    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (person_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (person_ref,),
        )
        created = connection.execute(
            "SELECT event_ref FROM dante.create_self_event(%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b03-b:event",
                "e" * 64,
                event_ref,
                "B03-B downgrade guard",
            ),
        ).fetchone()
        assert created == (event_ref,)
        scheduled = connection.execute(
            """
            SELECT subject_native_ref,schedule_ref,material_state_ref,replayed
              FROM dante.establish_self_schedule_placement(
                %s,%s,%s,%s,%s,%s,
                '{"kind":"floating_local_interval","starts_local_at":"2026-09-17T18:30:00.000000","ends_local_at":"2026-09-17T20:00:00.000000"}'::jsonb
              )
            """,
            (
                person_ref,
                "migration-proof:b03-b:schedule",
                "f" * 64,
                event_ref,
                schedule_ref,
                state_ref,
            ),
        ).fetchone()
        assert scheduled == (event_ref, schedule_ref, state_ref, False)

    with pytest.raises(DBAPIError, match="B03-B downgrade refused"):
        command.downgrade(alembic_config, _PARENT)

    assert _current_revision(provisioned_database) == _HEAD
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.event_expectation WHERE event_ref=%s),
              (SELECT count(*) FROM dante.schedule
                 WHERE schedule_ref=%s AND subject_native_ref=%s),
              (SELECT count(*) FROM dante.scoped_current_material_state
                 WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
                   AND material_state_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                 WHERE schedule_ref=%s AND material_state_ref=%s)
            """,
            (
                event_ref,
                schedule_ref,
                event_ref,
                schedule_ref,
                state_ref,
                schedule_ref,
                state_ref,
            ),
        ).fetchone()
    assert preserved == (1, 1, 1, 1)
