"""B13-C forward repair for the execution-policy CHECK identifier."""

from collections.abc import Sequence

from alembic import op

revision: str = "20260929_92"
down_revision: str | None = "20260929_91"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE dante.plan_step_in_state "
        "RENAME CONSTRAINT ck_plan_step_in_state_ck_plan_step_in_state_execution_policy "
        "TO ck_plan_step_in_state_execution_policy"
    )


def downgrade() -> None:
    raise RuntimeError("B13-C CHECK-name repair is forward-only.")
