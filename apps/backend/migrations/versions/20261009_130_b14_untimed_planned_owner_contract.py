"""Permit an unplaced Schedule only for an explicitly planned Activity row.

The existing deferred owner trigger still requires a current placement for
every other new Schedule. No placeholder placement or false history is written.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261009_130"
down_revision: str | None = "20261009_129"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    definition = bind.exec_driver_sql("""
        SELECT pg_get_functiondef(
            'dante.enforce_owner_creation_completeness()'::regprocedure
        )
    """).scalar_one()
    old = (
        "IF TG_TABLE_NAME='schedule' THEN owner_ref:=NEW.schedule_ref; "
        "SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state "
        "WHERE scoped_owner_ref=owner_ref AND facet_code='schedule.placement') INTO ok;"
    )
    new = (
        "IF TG_TABLE_NAME='schedule' THEN owner_ref:=NEW.schedule_ref; "
        "SELECT EXISTS (SELECT 1 FROM dante.scoped_current_material_state "
        "WHERE scoped_owner_ref=owner_ref AND facet_code='schedule.placement') "
        "OR EXISTS (SELECT 1 FROM dante.activity_schedule_role AS role "
        "WHERE role.schedule_ref=owner_ref AND role.role_code='planned') INTO ok;"
    )
    if definition.count(old) != 1:
        raise RuntimeError("Schedule owner completeness source differs from reviewed contract")
    bind.exec_driver_sql(definition.replace(old, new))


def downgrade() -> None:
    raise RuntimeError("Untimed planned Schedule owners require a reviewed forward migration")
