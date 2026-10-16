"""Retire the abandoned direct Timeline withdrawal and receipt capabilities.

Revision ID: 20261015_159
Revises: 20261015_158

Historical Schedule operations remain intact; the former direct Activity and
Event Timeline commands are no longer exposed or executable.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261015_159"
down_revision: str | None = "20261015_158"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    db = op.get_bind()
    for signature in (
        "dante.list_self_event_timeline_undo(uuid,uuid)",
        "dante.list_self_event_timeline_schedules(uuid,uuid)",
        "dante.undo_self_activity_timeline(uuid,text,text,uuid,text,uuid,uuid,text)",
        "dante.list_self_activity_timeline_undo(uuid,uuid)",
        "dante.undo_self_activity_schedule_coordinated(uuid,text,text,uuid,text,uuid)",
    ):
        db.exec_driver_sql(f"DROP FUNCTION IF EXISTS {signature}")


def downgrade() -> None:
    raise RuntimeError("Retired Timeline withdrawal capabilities are forward-only")
