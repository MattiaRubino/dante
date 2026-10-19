"""Real PostgreSQL acceptance tests for Alembic authority and drift detection."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy.exc import DBAPIError

pytestmark = pytest.mark.postgres

# The current head is forward-only; the earlier B01/B02 downgrade guard
# fixtures intentionally exercise the last historically reversible snapshot.
_CURRENT_HEAD = "20261019_161"
_HISTORICAL_REVERSIBLE_HEAD = "20260917_29"
_B02_REVISION_PARENT = "20260909_21"
_B02_SCHEMA_HEAD = "20260909_20"
_PRE_B02_HEAD = "20260908_19"
_PRE_B01_HEAD = "20260906_18"
_PRE_VERTICAL_BASE_HEAD = "20260904_17"
_CP6_HEAD = "20260826_08"
_RECOVERY_HEAD = "20260830_09"
_ACCESS_HEAD = "20260904_16"
_TRUSTED_SEARCH_PATH = "pg_catalog,dante,pg_temp"


def test_activity_lifecycle_functions_expose_only_bounded_runtime_capabilities(
    migrated_database: Any,
) -> None:
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        grants = connection.execute("""
            SELECT has_function_privilege(
                       'dante_runtime',
                       'dante.delete_self_activity_lifecycle_graph(uuid,uuid,text,uuid)',
                       'EXECUTE'),
                   has_function_privilege(
                       'dante_runtime',
                       'dante.delete_self_activity_sessions(uuid,uuid,text)',
                       'EXECUTE'),
                   has_function_privilege(
                       'dante_runtime',
                       'dante.delete_self_activity_hard(uuid,uuid,text)',
                       'EXECUTE'),
                   has_function_privilege(
                       'dante_runtime',
                       'dante.delete_self_activity_session_attempt(uuid,uuid,uuid,text)',
                       'EXECUTE'),
                   has_table_privilege('dante_runtime','dante.session','DELETE'),
                   has_table_privilege('dante_runtime','dante.activity','DELETE')
        """).fetchone()
        assert grants == (False, True, True, True, False, False)


def _floating_local(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    # A floating-local Schedule value intentionally has no timezone/offset.
    return datetime(year, month, day, hour, minute)  # noqa: DTZ001


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
    assert script.get_heads() == [_CURRENT_HEAD]

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}


def test_historical_reversible_head_round_trips_to_base_and_back(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    assert _current_revisions(provisioned_database) == {_HISTORICAL_REVERSIBLE_HEAD}

    command.downgrade(alembic_config, "base")
    assert _current_revisions(provisioned_database) == set()

    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    assert _current_revisions(provisioned_database) == {_HISTORICAL_REVERSIBLE_HEAD}


def test_current_repository_head_refuses_downgrade_by_design(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    """Protect the current forward-only migration and its canonical schema."""
    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}

    # The current forward-only head refuses rollback; older guards are
    # exercised separately at their own historical revisions.
    with pytest.raises(RuntimeError, match="20261019_161 is forward-only"):
        command.downgrade(alembic_config, "-1")

    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}


def test_previous_elapsed_anchor_forward_only_guard_remains_enforced(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    """Keep the historical _144 downgrade guard independently testable."""
    command.upgrade(alembic_config, "20261013_144")
    with pytest.raises(RuntimeError, match="Elapsed Recurrence anchors must remain non-null"):
        command.downgrade(alembic_config, "-1")
    assert _current_revisions(provisioned_database) == {"20261013_144"}


def test_relative_recurrence_anchor_and_policy_indexes_match_current_contract(
    migrated_database: Any,
) -> None:
    """The conditional anchor shape and lookup indexes survive fresh migration."""
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        for prefix in ("routine", "event"):
            elapsed = f"{prefix}_recurrence_elapsed_state"
            policy = f"{prefix}_occurrence_policy"
            nullable = connection.execute(
                "SELECT attnotnull FROM pg_attribute "
                "WHERE attrelid=%s::regclass AND attname='anchor_at'",
                (f"dante.{elapsed}",),
            ).fetchone()
            assert nullable == (False,)
            index = connection.execute(
                "SELECT indisunique, pg_get_indexdef(indexrelid) FROM pg_index "
                "WHERE indexrelid=%s::regclass",
                (f"dante.ix_{policy}_{prefix}",),
            ).fetchone()
            assert index is not None
            assert index[0] is False
            assert f"({prefix}_ref)" in index[1]
            assert "self_person_ref" not in index[1]


def test_previous_routine_replay_forward_only_guard_remains_enforced(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    """Repaired Routine replay cannot be rolled back by newer heads."""
    command.upgrade(alembic_config, "20261012_143")
    assert _current_revisions(provisioned_database) == {"20261012_143"}
    with pytest.raises(RuntimeError, match="Routine replay qualification must remain canonical"):
        command.downgrade(alembic_config, "-1")
    assert _current_revisions(provisioned_database) == {"20261012_143"}


def test_previous_forward_only_review_queue_guard_remains_enforced(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    """The prior review-queue migration still refuses rollback independently."""
    command.upgrade(alembic_config, "20261011_142")
    assert _current_revisions(provisioned_database) == {"20261011_142"}
    with pytest.raises(RuntimeError, match="Owner-only derived review queue is forward-only"):
        command.downgrade(alembic_config, "-1")
    assert _current_revisions(provisioned_database) == {"20261011_142"}


def test_schedule_unschedule_downgrade_refuses_to_discard_receipts(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    person_ref = uuid7()
    activity_ref = uuid7()
    schedule_ref = uuid7()
    first_state_ref = uuid7()
    restored_state_ref = uuid7()
    connection_kwargs = provisioned_database.connection_kwargs(
        "dante_migrator",
        provisioned_database.cluster.migrator_password,
    )

    with psycopg.connect(**connection_kwargs) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute(
            "INSERT INTO dante.person(person_ref) VALUES (%s)",
            (person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (person_ref,),
        )
        connection.execute(
            "SELECT activity_ref FROM dante.create_self_activity(%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-d-activity",
                "a" * 64,
                activity_ref,
                "B02-D guard",
            ),
        )
        connection.execute(
            "SELECT schedule_ref FROM dante.establish_self_floating_schedule"
            "(%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-d-establish",
                "b" * 64,
                activity_ref,
                schedule_ref,
                first_state_ref,
                _floating_local(2026, 9, 9, 10, 0),
                _floating_local(2026, 9, 9, 11, 0),
            ),
        )
        connection.execute(
            "SELECT schedule_ref FROM dante.unschedule_self_schedule(%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-d-unschedule",
                "c" * 64,
                schedule_ref,
                first_state_ref,
            ),
        )
        connection.execute(
            "SELECT schedule_ref FROM dante.undo_self_schedule_unschedule(%s,%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-d-undo",
                "d" * 64,
                schedule_ref,
                "migration-proof:b02-d-unschedule",
                restored_state_ref,
            ),
        )

    with pytest.raises(DBAPIError, match="B02-D downgrade refused"):
        command.downgrade(alembic_config, "20260913_22")

    assert _current_revisions(provisioned_database) == {_HISTORICAL_REVERSIBLE_HEAD}
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.schedule_unschedule_operation
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.schedule_unschedule_undo_operation
                WHERE schedule_ref=%s AND material_state_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s),
              (SELECT count(*) FROM dante.scoped_current_material_state
                WHERE scoped_owner_ref=%s
                  AND facet_code='schedule.placement'
                  AND material_state_ref=%s)
            """,
            (
                schedule_ref,
                schedule_ref,
                restored_state_ref,
                schedule_ref,
                schedule_ref,
                restored_state_ref,
            ),
        ).fetchone()
    assert preserved == (1, 1, 2, 1)


def test_schedule_revision_downgrade_refuses_to_discard_revision_receipts(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    person_ref = uuid7()
    activity_ref = uuid7()
    schedule_ref = uuid7()
    first_state_ref = uuid7()
    revised_state_ref = uuid7()
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
        connection.execute(
            "SELECT activity_ref FROM dante.create_self_activity(%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-c-activity",
                "a" * 64,
                activity_ref,
                "B02-C guard",
            ),
        )
        connection.execute(
            "SELECT schedule_ref FROM dante.establish_self_floating_schedule"
            "(%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-c-establish",
                "b" * 64,
                activity_ref,
                schedule_ref,
                first_state_ref,
                _floating_local(2026, 9, 9, 10, 0),
                _floating_local(2026, 9, 9, 11, 0),
            ),
        )
        revised = connection.execute(
            "SELECT schedule_ref,previous_material_state_ref,material_state_ref "
            "FROM dante.revise_self_floating_schedule"
            "(%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-c-revise",
                "c" * 64,
                schedule_ref,
                first_state_ref,
                revised_state_ref,
                _floating_local(2026, 9, 9, 12, 0),
                _floating_local(2026, 9, 9, 13, 30),
            ),
        ).fetchone()
        assert revised == (schedule_ref, first_state_ref, revised_state_ref)

    with pytest.raises(DBAPIError, match="B02-C downgrade refused"):
        command.downgrade(alembic_config, _B02_REVISION_PARENT)

    assert _current_revisions(provisioned_database) == {_HISTORICAL_REVERSIBLE_HEAD}
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.schedule_revision_operation
                WHERE schedule_ref=%s AND material_state_ref=%s),
              (SELECT count(*) FROM dante.scoped_current_material_state
                WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
                  AND material_state_ref=%s),
              (SELECT count(*) FROM dante.schedule_placement_current_history
                WHERE schedule_ref=%s)
            """,
            (
                schedule_ref,
                revised_state_ref,
                schedule_ref,
                revised_state_ref,
                schedule_ref,
            ),
        ).fetchone()
    assert preserved == (1, 1, 2)


def test_schedule_downgrade_refuses_to_discard_canonical_history(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    person_ref = uuid7()
    activity_ref = uuid7()
    schedule_ref = uuid7()
    material_state_ref = uuid7()
    starts_local_at = _floating_local(2026, 9, 9, 18, 0)
    ends_local_at = _floating_local(2026, 9, 9, 19, 0)
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
            "SELECT activity_ref FROM dante.create_self_activity(%s,%s,%s,%s,%s)",
            (
                person_ref,
                "migration-proof:b02-activity",
                "a" * 64,
                activity_ref,
                "B02 guard",
            ),
        ).fetchone()
        assert created == (activity_ref,)
        scheduled = connection.execute(
            """
            SELECT subject_native_ref,schedule_ref,material_state_ref,starts_local_at,ends_local_at,replayed
            FROM dante.establish_self_floating_schedule(%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                person_ref,
                "migration-proof:b02-schedule",
                "b" * 64,
                activity_ref,
                schedule_ref,
                material_state_ref,
                starts_local_at,
                ends_local_at,
            ),
        ).fetchone()
        assert scheduled == (
            activity_ref,
            schedule_ref,
            material_state_ref,
            starts_local_at,
            ends_local_at,
            False,
        )

    with pytest.raises(DBAPIError, match="B02-A downgrade refused"):
        command.downgrade(alembic_config, _PRE_B02_HEAD)

    # A failed multi-revision downgrade may already have reverted the ACL-only child.
    # Re-upgrade to the historical reversible head and prove B02 state survived.
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    assert _current_revisions(provisioned_database) == {_HISTORICAL_REVERSIBLE_HEAD}
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.schedule_establish_operation
                 WHERE self_person_ref=%s AND operation_id='migration-proof:b02-schedule'
                   AND schedule_ref=%s AND material_state_ref=%s),
              (SELECT count(*) FROM dante.schedule WHERE schedule_ref=%s AND subject_native_ref=%s),
              (SELECT count(*) FROM dante.scoped_current_material_state
                 WHERE scoped_owner_ref=%s AND facet_code='schedule.placement'
                   AND material_state_ref=%s)
            """,
            (
                person_ref,
                schedule_ref,
                material_state_ref,
                schedule_ref,
                activity_ref,
                schedule_ref,
                material_state_ref,
            ),
        ).fetchone()
    assert preserved == (1, 1, 1)


def test_activity_downgrade_refuses_to_discard_canonical_intention(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    command.downgrade(alembic_config, _PRE_B02_HEAD)
    assert _current_revisions(provisioned_database) == {_PRE_B02_HEAD}

    person_ref = uuid7()
    activity_ref = uuid7()
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
            SELECT activity_ref,title,replayed
            FROM dante.create_self_activity(%s,%s,%s,%s,%s)
            """,
            (
                person_ref,
                "migration-proof:b01",
                "a" * 64,
                activity_ref,
                "Canonical downgrade guard",
            ),
        ).fetchone()
        assert created == (activity_ref, "Canonical downgrade guard", False)

    with pytest.raises(DBAPIError, match="B01 downgrade refused"):
        command.downgrade(alembic_config, _PRE_B01_HEAD)

    assert _current_revisions(provisioned_database) == {_PRE_B02_HEAD}
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.activity WHERE activity_ref=%s),
              (SELECT count(*) FROM dante.native_address
                 WHERE native_ref=%s AND owner_family='activity'),
              (SELECT count(*) FROM dante.activity_intention
                 WHERE activity_ref=%s AND self_person_ref=%s),
              (SELECT count(*) FROM dante.activity_create_operation
                 WHERE activity_ref=%s AND self_person_ref=%s
                   AND operation_id='migration-proof:b01')
            """,
            (
                activity_ref,
                activity_ref,
                activity_ref,
                person_ref,
                activity_ref,
                person_ref,
            ),
        ).fetchone()
    assert preserved == (1, 1, 1, 1)


def test_context_downgrade_refuses_to_orphan_live_account_person_binding(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _HISTORICAL_REVERSIBLE_HEAD)
    assert _current_revisions(provisioned_database) == {_HISTORICAL_REVERSIBLE_HEAD}

    command.downgrade(alembic_config, _PRE_B01_HEAD)
    assert _current_revisions(provisioned_database) == {_PRE_B01_HEAD}

    account_ref = uuid7()
    person_ref = uuid7()
    created_at = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
    connection_kwargs = provisioned_database.connection_kwargs(
        "dante_migrator",
        provisioned_database.cluster.migrator_password,
    )

    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute(
            """
            INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at)
            VALUES (%s,'active',%s,NULL)
            """,
            (account_ref, created_at),
        )
        context = connection.execute(
            """
            SELECT account_ref,self_person_ref,timezone_mode,fixed_zone_id
            FROM dante.ensure_account_application_context(%s,%s)
            """,
            (account_ref, person_ref),
        ).fetchone()
        assert context == (account_ref, person_ref, "follow_device", None)

    with pytest.raises(DBAPIError, match="PV-02 downgrade refused"):
        command.downgrade(alembic_config, _PRE_VERTICAL_BASE_HEAD)

    assert _current_revisions(provisioned_database) == {_PRE_B01_HEAD}
    with psycopg.connect(**connection_kwargs, autocommit=True) as connection:
        connection.execute("SET ROLE dante_owner")
        preserved = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.account_application_context
                 WHERE account_ref=%s AND self_person_ref=%s),
              (SELECT count(*) FROM dante.person WHERE person_ref=%s),
              (SELECT count(*) FROM dante.native_address
                 WHERE native_ref=%s AND owner_family='person')
            """,
            (account_ref, person_ref, person_ref, person_ref),
        ).fetchone()
    assert preserved == (1, 1, 1)


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


def test_existing_access_head_converges_forward_to_current_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _ACCESS_HEAD)
    assert _current_revisions(provisioned_database) == {_ACCESS_HEAD}

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}


def test_existing_recovery_head_converges_forward_to_current_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _RECOVERY_HEAD)
    assert _current_revisions(provisioned_database) == {_RECOVERY_HEAD}

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}


def test_existing_pre_vertical_base_converges_forward_to_current_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    command.upgrade(alembic_config, _PRE_VERTICAL_BASE_HEAD)
    assert _current_revisions(provisioned_database) == {_PRE_VERTICAL_BASE_HEAD}

    command.upgrade(alembic_config, "head")
    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}


def test_existing_recovery_rows_survive_forward_convergence_to_current_head(
    provisioned_database: Any,
    alembic_config: Config,
) -> None:
    """Prove later additions do not overwrite accepted Recovery-era rows."""

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
    assert _current_revisions(provisioned_database) == {_CURRENT_HEAD}

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
