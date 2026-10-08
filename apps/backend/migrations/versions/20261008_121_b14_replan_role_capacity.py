"""Keep immutable planning roles while allowing repeated post-create edits.

The product limit remains 100 *current* rows per role. Historical Schedule
identities retain their original role and order after unscheduling, so a
lifetime limit of 100 role slots would prevent ordinary add/remove cycles.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261008_121"
down_revision: str | None = "20261007_120"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        "ck_activity_schedule_role_ck_activity_schedule_role_order",
        "activity_schedule_role", schema="dante", type_="check",
    )
    op.create_check_constraint(
        "ck_activity_schedule_role_order", "activity_schedule_role",
        "(role_code='envelope' AND presentation_order=0) OR "
        "(role_code IN ('planned','interval') AND presentation_order BETWEEN 1 AND 2147483647)",
        schema="dante",
    )
    bind = op.get_bind()
    definition = bind.exec_driver_sql("""
        SELECT pg_get_functiondef(
            'dante.set_self_activity_schedule_role(uuid,uuid,uuid,text,integer,text)'::regprocedure
        )
    """).scalar_one()
    old = "requested_presentation_order BETWEEN 1 AND 100"
    if definition.count(old) != 1:
        raise RuntimeError("Activity role capacity source differs from the accepted revision")
    bind.exec_driver_sql(definition.replace(old, "requested_presentation_order BETWEEN 1 AND 2147483647"))


def downgrade() -> None:
    raise RuntimeError("Historical Activity roles cannot be reduced to 100 slots safely")
