"""B14 Create closure: remove superseded Routine policy overload.

Revision ID: 20261006_115
Revises: 20261006_114

20261006_111 introduced the JSONB template-aware five-argument setter but left
the four-argument 20261005_107 overload in pg_proc. The runtime uses only the
five-argument canonical capability. Remove the superseded overload so the
Database Dictionary retains one entry per routine name.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261006_115"
down_revision: str | None = "20261006_114"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.get_bind().exec_driver_sql(
        "DROP FUNCTION dante.set_self_routine_occurrence_policy("
        "uuid,uuid,integer,integer)"
    )


def downgrade() -> None:
    raise RuntimeError(
        "20261006_115 is forward-only after the superseded Routine policy overload is retired"
    )
