"""B14: preserve unassigned Routine organization in the routine listing.

Optional Life Area is a valid Routine state. The listing capability must expose the
absence as assignment revision zero, rather than a nullable value that breaks
canonical readback after creation.

Revision ID: 20261006_109
Revises: 20261005_108
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261006_109"
down_revision: str | None = "20261005_108"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _definition() -> str:
    value = op.get_bind().exec_driver_sql(
        """
        SELECT pg_get_functiondef(routine.oid)
          FROM pg_proc AS routine
          JOIN pg_namespace AS namespace ON namespace.oid=routine.pronamespace
         WHERE namespace.nspname='dante'
           AND routine.proname='list_self_routines'
           AND routine.pronargs=1
        """
    ).scalar_one()
    if not isinstance(value, str):
        raise RuntimeError("B14 Routine listing capability is unavailable")
    return value


def upgrade() -> None:
    definition = _definition()
    old = "area.life_area_ref,area.revision,area.assigned_at"
    new = "area.life_area_ref,COALESCE(area.revision,0)::bigint,area.assigned_at"
    if definition.count(old) != 1:
        raise RuntimeError("B14 optional Routine listing patch point did not match exactly once")
    connection = op.get_bind()
    connection.exec_driver_sql(definition.replace(old, new).replace("%", "%%"))
    connection.exec_driver_sql(
        "ALTER FUNCTION dante.list_self_routines(uuid) OWNER TO dante_owner"
    )
    connection.exec_driver_sql(
        "REVOKE ALL PRIVILEGES ON FUNCTION dante.list_self_routines(uuid) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(
        "GRANT EXECUTE ON FUNCTION dante.list_self_routines(uuid) TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError(
        "20261006_109 is forward-only after optional Routine organization becomes valid"
    )
