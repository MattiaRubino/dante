"""Retire calendar timing from named Activity Sessions.

Revision ID: 20261014_146
Revises: 20261013_145

The existing linked Session identity remains provenance for a named internal
Session.  This revision removes the last database admission that treated that
identity as a second Schedule window: real execution can start before or after
its Activity interval.  Activity intervals remain the UI availability signal.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261014_146"
down_revision: str | None = "20261013_145"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_GUARD = r"""    IF NOT result.replayed AND EXISTS (
        SELECT 1 FROM dante.schedule_current_placement current
        JOIN dante.schedule_placement_state state
          ON state.material_state_ref=current.material_state_ref
        LEFT JOIN dante.schedule_placement_absolute_state absolute
          ON absolute.material_state_ref=state.material_state_ref
        LEFT JOIN dante.schedule_placement_named_zone_state zoned
          ON zoned.material_state_ref=state.material_state_ref
        WHERE current.scoped_owner_ref=requested_schedule_ref
          AND COALESCE(absolute.starts_at,zoned.resolved_start_at)
              > clock_timestamp()
    ) THEN
        RAISE EXCEPTION USING ERRCODE='23514',
          CONSTRAINT='session_internal_before_planned_start',
          MESSAGE='Internal Session cannot start before planned start';
    END IF;
"""


def upgrade() -> None:
    bind = op.get_bind()
    definition = bind.exec_driver_sql(
        "SELECT pg_get_functiondef("
        "'dante.start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)'"
        "::regprocedure)"
    ).scalar_one()
    if definition.count(_GUARD) != 1:
        raise RuntimeError("Unexpected named Session start guard at lifecycle v2")
    bind.exec_driver_sql(definition.replace(_GUARD, "").replace("%", "%%"))
    signature = "dante.start_self_planned_activity_session(uuid,text,text,uuid,uuid,uuid,uuid)"
    bind.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    bind.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Named Session execution history is forward-only")
