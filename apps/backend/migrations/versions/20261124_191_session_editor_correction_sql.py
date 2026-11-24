"""Disambiguate timing history columns in Session recording corrections."""

from collections.abc import Sequence

from alembic import op

revision: str = "20261124_191"
down_revision: str | None = "20261124_190"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SIGNATURE = (
    "dante.write_self_activity_session_editor("
    "uuid,text,text,uuid,uuid,uuid,uuid,uuid,timestamptz,timestamptz,jsonb)"
)
_OLD = """UPDATE dante.session_timing_current_history SET current_until_at=recorded_at
         WHERE session_ref=requested_session AND material_state_ref=requested_expected_state
           AND current_until_at IS NULL;"""
_NEW = """UPDATE dante.session_timing_current_history AS history SET current_until_at=recorded_at
         WHERE history.session_ref=requested_session
           AND history.material_state_ref=requested_expected_state
           AND history.current_until_at IS NULL;"""


def upgrade() -> None:
    database = op.get_bind()
    definition = database.exec_driver_sql(
        "SELECT pg_get_functiondef(%s::regprocedure)", (_SIGNATURE,)
    ).scalar_one()
    if definition.count(_OLD) != 1 or _NEW in definition:
        raise RuntimeError("Unexpected Session editor function body")
    database.exec_driver_sql(definition.replace(_OLD, _NEW).replace("%", "%%"))


def downgrade() -> None:
    raise RuntimeError("Factual Session correction requires a reviewed forward migration")
