"""Apply CP6-05 final QA hardening without changing the frozen DB topology.

Revision ID: 20260826_08
Revises: 20260826_07
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260826_08"
down_revision: str | None = "20260826_07"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_ROLE13 = "enforce_occurrence_generation_integrity"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_SOURCE_FAMILY_BASE = r"""    IF source_family NOT IN ('routine','event') THEN
        bad := true;
    END IF;"""

_SOURCE_FAMILY_LOCKED = r"""    IF source_family NOT IN ('routine','event') THEN
        bad := true;
    ELSIF g.origin_code='recurrence_generated' THEN
        -- CP6-05: Role-13 independently acquires the exact source generation lock.
        -- The digest is the first 56 bits of SHA-256('dante-lock-v2' || UUID bytes),
        -- matching dante.platform.database.locking.advisory_lock_key().
        PERFORM pg_catalog.pg_advisory_xact_lock(
            ((CASE WHEN source_family='routine' THEN 6 ELSE 7 END)::bigint << 56)
            |
            (
                (pg_catalog.get_byte(lock_digest.digest,0)::bigint << 48)
                | (pg_catalog.get_byte(lock_digest.digest,1)::bigint << 40)
                | (pg_catalog.get_byte(lock_digest.digest,2)::bigint << 32)
                | (pg_catalog.get_byte(lock_digest.digest,3)::bigint << 24)
                | (pg_catalog.get_byte(lock_digest.digest,4)::bigint << 16)
                | (pg_catalog.get_byte(lock_digest.digest,5)::bigint << 8)
                | pg_catalog.get_byte(lock_digest.digest,6)::bigint
            )
        )
        FROM (
            SELECT pg_catalog.sha256(
                pg_catalog.convert_to('dante-lock-v2','UTF8')
                || pg_catalog.uuid_send(g.source_native_ref)
            ) AS digest
        ) AS lock_digest;
    END IF;"""

_M7_ROUTINE_MARKER = (
    "NULL; -- CP6-M07: Part-14 advisory locks are acquired by the accepted operation boundary for Routine generation"
)
_M7_EVENT_MARKER = (
    "NULL; -- CP6-M07: Part-14 advisory locks are acquired by the accepted operation boundary for Event generation"
)
_FINAL_ROUTINE_MARKER = (
    "NULL; -- CP6-05: Role-13 already holds the exact Routine occurrence-generation advisory lock"
)
_FINAL_EVENT_MARKER = (
    "NULL; -- CP6-05: Role-13 already holds the exact Event occurrence-generation advisory lock"
)


def _replace_routine_fragment(old: str, new: str, *, failure: str) -> None:
    connection = op.get_bind()
    definition = connection.exec_driver_sql(
        """
        SELECT pg_get_functiondef(p.oid)
        FROM pg_proc AS p
        JOIN pg_namespace AS n ON n.oid = p.pronamespace
        WHERE n.nspname = 'dante'
          AND p.proname = %s
          AND p.pronargs = 0
        """,
        (_ROLE13,),
    ).scalar_one()
    if definition.count(old) != 1:
        raise RuntimeError(failure)
    connection.exec_driver_sql(definition.replace(old, new).replace("%", "%%"))


def _reassert_role13_security() -> None:
    connection = op.get_bind()
    connection.exec_driver_sql(f"ALTER FUNCTION dante.{_ROLE13}() OWNER TO dante_owner")
    connection.exec_driver_sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.{_ROLE13}() "
        f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
    )


def upgrade() -> None:
    """Make Role-13 use the exact cross-language advisory lock before final validation."""
    _replace_routine_fragment(
        _SOURCE_FAMILY_BASE,
        _SOURCE_FAMILY_LOCKED,
        failure="CP6-05 Role-13 source-family insertion point did not match exactly once",
    )
    _replace_routine_fragment(
        _M7_ROUTINE_MARKER,
        _FINAL_ROUTINE_MARKER,
        failure="CP6-05 Routine M7 advisory marker did not match exactly once",
    )
    _replace_routine_fragment(
        _M7_EVENT_MARKER,
        _FINAL_EVENT_MARKER,
        failure="CP6-05 Event M7 advisory marker did not match exactly once",
    )
    _reassert_role13_security()


def downgrade() -> None:
    """Return exactly to the accepted M7 Role-13 definition."""
    _replace_routine_fragment(
        _FINAL_EVENT_MARKER,
        _M7_EVENT_MARKER,
        failure="CP6-05 Event final advisory marker did not match exactly once",
    )
    _replace_routine_fragment(
        _FINAL_ROUTINE_MARKER,
        _M7_ROUTINE_MARKER,
        failure="CP6-05 Routine final advisory marker did not match exactly once",
    )
    _replace_routine_fragment(
        _SOURCE_FAMILY_LOCKED,
        _SOURCE_FAMILY_BASE,
        failure="CP6-05 Role-13 locked source-family fragment did not match exactly once",
    )
    _reassert_role13_security()
