"""Immutable per-Objective verification, independent of Activity/Event completion."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261107_178"
down_revision: str | None = "20261107_177"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "temporal_objective_verification_revision",
        sa.Column("objective_ref", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.BigInteger(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("mode_code", sa.Text(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("objective_ref", "revision", name="pk_temporal_objective_verification_revision"),
        sa.UniqueConstraint("self_person_ref", "operation_id", name="uq_temporal_objective_verification_operation"),
        sa.ForeignKeyConstraint(["objective_ref"], ["dante.temporal_objective.objective_ref"], name="fk_temporal_objective_verification_objective"),
        sa.ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_temporal_objective_verification_person"),
        sa.CheckConstraint("revision>=1", name=op.f("ck_temporal_objective_verification_revision_positive")),
        sa.CheckConstraint("mode_code IN ('none','review_on_end')", name=op.f("ck_temporal_objective_verification_revision_mode")),
        sa.CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name=op.f("ck_temporal_objective_verification_revision_fingerprint")),
        sa.CheckConstraint("operation_id=btrim(operation_id) AND char_length(operation_id) BETWEEN 1 AND 200", name=op.f("ck_temporal_objective_verification_revision_operation")),
        sa.CheckConstraint("isfinite(accepted_at)", name=op.f("ck_temporal_objective_verification_revision_time")),
        schema="dante",
    )
    op.create_table(
        "temporal_objective_verification_series",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("source_native_ref", sa.Uuid(), nullable=False),
        sa.Column("selected_occurrence_ref", sa.Uuid(), nullable=False),
        sa.Column("template_slot", sa.Integer(), nullable=False),
        sa.Column("effective_zone_id", sa.Text(), nullable=False),
        sa.Column("anchor_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("include_selected", sa.Boolean(), nullable=False),
        sa.Column("mode_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("self_person_ref", "operation_id", name="pk_temporal_objective_verification_series"),
        sa.ForeignKeyConstraint(["source_native_ref"], ["dante.native_address.native_ref"], name="fk_temporal_objective_verification_series_source"),
        sa.ForeignKeyConstraint(["selected_occurrence_ref"], ["dante.occurrence.occurrence_ref"], name="fk_temporal_objective_verification_series_occurrence"),
        sa.ForeignKeyConstraint(["self_person_ref"], ["dante.person.person_ref"], name="fk_temporal_objective_verification_series_person"),
        sa.CheckConstraint("mode_code IN ('none','review_on_end')", name=op.f("ck_temporal_objective_verification_series_mode")),
        sa.CheckConstraint("template_slot BETWEEN 0 AND 99 AND isfinite(anchor_at) AND isfinite(accepted_at)", name=op.f("ck_temporal_objective_verification_series_shape")),
        schema="dante",
    )
    op.create_index(
        "ix_temporal_objective_verification_series_source",
        "temporal_objective_verification_series",
        ["source_native_ref", "template_slot", "accepted_at"],
        schema="dante",
    )
    conn = op.get_bind()
    for name in ("temporal_objective_verification_revision", "temporal_objective_verification_series"):
        conn.exec_driver_sql(f"ALTER TABLE dante.{name} OWNER TO dante_owner")
        conn.exec_driver_sql(f"REVOKE ALL ON dante.{name} FROM PUBLIC,dante_runtime,dante_migrator")
    for sql in (_GET, _SET, _APPLY_SERIES):
        conn.exec_driver_sql(sql)
    for signature in (
        "get_self_objective_verification(uuid,uuid)",
        "set_self_objective_verification(uuid,uuid,text,text,bigint,text)",
        "apply_self_objective_verification_series(uuid,uuid,text,text)",
    ):
        conn.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        conn.exec_driver_sql(f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator")
        conn.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("Per-Objective verification is forward-only")


