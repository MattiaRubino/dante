"""Repair routine create replay after optional Life Area assignment.

The replay branch calls routine_life_area_assignment from a RETURNS TABLE
function with an OUT column named routine_ref. Qualify the SQL columns so
PL/pgSQL cannot confuse them with the function output parameter. Keep the
function's complete logic, execution grants, and live accepted data intact.

Revision ID: 20261012_143
Revises: 20261011_142
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261012_143"
down_revision: str | None = "20261011_142"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SIGNATURE = "uuid,text,text,uuid,text,uuid,uuid[],date,time without time zone"
_OLD = (
    "SELECT revision FROM dante.routine_life_area_assignment "
    "WHERE self_person_ref=requested_self_person_ref "
    "AND routine_ref=previous.routine_ref"
)
_NEW = (
    "SELECT assignment.revision FROM dante.routine_life_area_assignment AS assignment "
    "WHERE assignment.self_person_ref=requested_self_person_ref "
    "AND assignment.routine_ref=previous.routine_ref"
)


def upgrade() -> None:
    connection = op.get_bind()
    definition = connection.exec_driver_sql(
        """
        SELECT pg_get_functiondef(routine.oid)
          FROM pg_proc AS routine
          JOIN pg_namespace AS namespace ON namespace.oid = routine.pronamespace
         WHERE namespace.nspname = 'dante'
           AND routine.proname = 'create_self_routine'
           AND routine.pronargs = 9
        """
    ).scalar_one()
    if not isinstance(definition, str) or definition.count(_OLD) != 1:
        raise RuntimeError("Routine replay SQL qualification point is not unique")

    # Keep all previously authorized function behavior and ACLs unchanged;
    # update only the ambiguous replay subquery in the function definition.
    definition = definition.replace(_OLD, _NEW)
    connection.exec_driver_sql(definition.replace("%", "%%"))
    connection.exec_driver_sql(
        f"ALTER FUNCTION dante.create_self_routine({_SIGNATURE}) OWNER TO dante_owner"
    )
    connection.exec_driver_sql(
        f"REVOKE ALL PRIVILEGES ON FUNCTION dante.create_self_routine({_SIGNATURE}) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(
        f"GRANT EXECUTE ON FUNCTION dante.create_self_routine({_SIGNATURE}) TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError(
        "20261012_143 is forward-only: Routine replay qualification must remain canonical"
    )
