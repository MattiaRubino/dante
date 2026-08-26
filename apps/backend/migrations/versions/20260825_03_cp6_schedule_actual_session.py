"""Materialize CP6-M03 Schedule/Actual/Session companion families.

Revision ID: 20260825_03
Revises: 20260825_02
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260825_03"
down_revision: str | None = "20260825_02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_M3_TABLES = (
    "schedule_placement_state",
    "schedule_placement_date_state",
    "schedule_placement_floating_local_state",
    "schedule_placement_named_zone_state",
    "schedule_placement_absolute_state",
    "schedule_placement_current_history",
    "session_timing_state",
    "session_timing_absolute",
    "session_timing_elapsed",
    "session_timing_pause",
    "session_timing_current_history",
    "actual_realization_state",
    "actual_realization_timing",
    "actual_realization_session_basis",
    "actual_realization_current_history",
)


def _fk(
    local_columns: list[str],
    remote_columns: list[str],
    *,
    name: str,
) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        local_columns,
        remote_columns,
        name=op.f(name),
        match="SIMPLE",
        onupdate="NO ACTION",
        ondelete="NO ACTION",
        deferrable=False,
    )


def _deny_runtime_access_to_new_relations() -> None:
    for table_name in _M3_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_DANTE_SCHEMA}.{table_name} "
                f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
            )
        )


def upgrade() -> None:
    """Create exactly the CP6-M03 fifteen-table companion-state surface."""
    op.create_table(
        "schedule_placement_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("temporal_form_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_placement_state"),
        ),
        sa.CheckConstraint(
            "temporal_form_code IN "
            "('date_span','floating_local','named_zone_local','absolute')",
            name=op.f("ck_schedule_placement_state_temporal_form"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_schedule_placement_state_state_address",
        ),
        _fk(
            ["schedule_ref"],
            ["dante.schedule.schedule_ref"],
            name="fk_schedule_placement_state_schedule_ref_schedule",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_schedule_placement_state_schedule_ref",
        "schedule_placement_state",
        ["schedule_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "schedule_placement_date_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("date_span", postgresql.DATERANGE(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_placement_date_state"),
        ),
        sa.CheckConstraint(
            "NOT isempty(date_span) "
            "AND NOT lower_inf(date_span) "
            "AND NOT upper_inf(date_span) "
            "AND lower_inc(date_span) "
            "AND NOT upper_inc(date_span) "
            "AND isfinite(lower(date_span)) "
            "AND isfinite(upper(date_span))",
            name=op.f("ck_schedule_placement_date_state_date_span"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_date_state_placement_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "schedule_placement_floating_local_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("extent_code", sa.Text(), nullable=False),
        sa.Column("starts_local_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("ends_local_at", sa.DateTime(timezone=False), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_placement_floating_local_state"),
        ),
        sa.CheckConstraint(
            "extent_code IN ('point','start_only','interval')",
            name=op.f("ck_schedule_placement_floating_local_state_extent"),
        ),
        sa.CheckConstraint(
            "isfinite(starts_local_at) AND ("
            "(extent_code IN ('point','start_only') AND ends_local_at IS NULL) OR "
            "(extent_code='interval' AND ends_local_at IS NOT NULL "
            "AND isfinite(ends_local_at) AND ends_local_at > starts_local_at))",
            name=op.f(
                "ck_schedule_placement_floating_local_state_interval_order"
            ),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_floating_local_state_placement_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "schedule_placement_named_zone_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("extent_code", sa.Text(), nullable=False),
        sa.Column("starts_local_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("ends_local_at", sa.DateTime(timezone=False), nullable=True),
        sa.Column("zone_id", sa.Text(), nullable=False),
        sa.Column("resolved_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_end_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_placement_named_zone_state"),
        ),
        sa.CheckConstraint(
            "extent_code IN ('point','start_only','interval')",
            name=op.f("ck_schedule_placement_named_zone_state_extent"),
        ),
        sa.CheckConstraint(
            "isfinite(starts_local_at) AND ("
            "(extent_code IN ('point','start_only') AND ends_local_at IS NULL) OR "
            "(extent_code='interval' AND ends_local_at IS NOT NULL "
            "AND isfinite(ends_local_at) AND ends_local_at > starts_local_at))",
            name=op.f("ck_schedule_placement_named_zone_state_interval_order"),
        ),
        sa.CheckConstraint(
            "(resolved_start_at IS NULL OR isfinite(resolved_start_at)) AND ("
            "resolved_end_at IS NULL OR "
            "(resolved_start_at IS NOT NULL AND extent_code='interval' "
            "AND isfinite(resolved_end_at) "
            "AND resolved_end_at > resolved_start_at))",
            name=op.f("ck_schedule_placement_named_zone_state_resolved_pair"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_named_zone_state_placement_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "schedule_placement_absolute_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("extent_code", sa.Text(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_schedule_placement_absolute_state"),
        ),
        sa.CheckConstraint(
            "extent_code IN ('point','start_only','interval')",
            name=op.f("ck_schedule_placement_absolute_state_extent"),
        ),
        sa.CheckConstraint(
            "isfinite(starts_at) AND ("
            "(extent_code IN ('point','start_only') AND ends_at IS NULL) OR "
            "(extent_code='interval' AND ends_at IS NOT NULL "
            "AND isfinite(ends_at) AND ends_at > starts_at))",
            name=op.f("ck_schedule_placement_absolute_state_interval_order"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_absolute_state_placement_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "schedule_placement_current_history",
        sa.Column("schedule_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "schedule_ref",
            "current_from_at",
            name=op.f("pk_schedule_placement_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name=op.f(
                "ck_schedule_placement_current_history_current_interval"
            ),
        ),
        _fk(
            ["schedule_ref"],
            ["dante.schedule.schedule_ref"],
            name="fk_schedule_placement_current_history_schedule_ref_schedule",
        ),
        _fk(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_current_history_placement_state",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ux_schedule_placement_current_history_open",
        "schedule_placement_current_history",
        ["schedule_ref"],
        unique=True,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_schedule_placement_current_history_material_state_ref",
        "schedule_placement_current_history",
        ["material_state_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "session_timing_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("session_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timing_form_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_session_timing_state"),
        ),
        sa.CheckConstraint(
            "timing_form_code IN ('absolute','elapsed_only')",
            name=op.f("ck_session_timing_state_timing_form"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_session_timing_state_state_address",
        ),
        _fk(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_session_timing_state_session_ref_session",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_session_timing_state_session_ref",
        "session_timing_state",
        ["session_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "session_timing_absolute",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("start_precision_code", sa.Text(), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_precision_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_session_timing_absolute"),
        ),
        sa.CheckConstraint(
            "start_precision_code IN ('exact','approximate','rounded') "
            "AND isfinite(started_at)",
            name=op.f("ck_session_timing_absolute_start_precision"),
        ),
        sa.CheckConstraint(
            "(ended_at IS NULL AND end_precision_code IS NULL) OR "
            "(ended_at IS NOT NULL AND isfinite(ended_at) "
            "AND end_precision_code IN ('exact','approximate','rounded'))",
            name=op.f("ck_session_timing_absolute_end_precision"),
        ),
        sa.CheckConstraint(
            "ended_at IS NULL OR ended_at > started_at",
            name=op.f("ck_session_timing_absolute_interval_order"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_timing_absolute_timing_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "session_timing_elapsed",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("elapsed_seconds", sa.Numeric(), nullable=False),
        sa.Column("elapsed_precision_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_session_timing_elapsed"),
        ),
        sa.CheckConstraint(
            "elapsed_seconds NOT IN "
            "('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
            "AND elapsed_seconds > 0",
            name=op.f("ck_session_timing_elapsed_elapsed_positive"),
        ),
        sa.CheckConstraint(
            "elapsed_precision_code IN ('exact','approximate','rounded')",
            name=op.f("ck_session_timing_elapsed_elapsed_precision"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_timing_elapsed_timing_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "session_timing_pause",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("paused_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("pause_precision_code", sa.Text(), nullable=False),
        sa.Column("resumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resume_precision_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "paused_at",
            name=op.f("pk_session_timing_pause"),
        ),
        sa.CheckConstraint(
            "pause_precision_code IN ('exact','approximate','rounded') "
            "AND isfinite(paused_at)",
            name=op.f("ck_session_timing_pause_pause_precision"),
        ),
        sa.CheckConstraint(
            "resume_precision_code IS NULL OR "
            "resume_precision_code IN ('exact','approximate','rounded')",
            name=op.f("ck_session_timing_pause_resume_precision"),
        ),
        sa.CheckConstraint(
            "(resumed_at IS NULL AND resume_precision_code IS NULL) OR "
            "(resumed_at IS NOT NULL AND isfinite(resumed_at) "
            "AND resume_precision_code IS NOT NULL AND resumed_at > paused_at)",
            name=op.f("ck_session_timing_pause_resume_pair"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.session_timing_absolute.material_state_ref"],
            name="fk_session_timing_pause_timing_absolute",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ux_session_timing_pause_open",
        "session_timing_pause",
        ["material_state_ref"],
        unique=True,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("resumed_at IS NULL"),
    )

    op.create_table(
        "session_timing_current_history",
        sa.Column("session_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "session_ref",
            "current_from_at",
            name=op.f("pk_session_timing_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name=op.f("ck_session_timing_current_history_current_interval"),
        ),
        _fk(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_session_timing_current_history_session_ref_session",
        ),
        _fk(
            ["material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_session_timing_current_history_timing_state",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ux_session_timing_current_history_open",
        "session_timing_current_history",
        ["session_ref"],
        unique=True,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_session_timing_current_history_material_state_ref",
        "session_timing_current_history",
        ["material_state_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "actual_realization_state",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("realization_occurred", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_actual_realization_state"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_actual_realization_state_state_address",
        ),
        _fk(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_actual_realization_state_actual_ref_actual",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_actual_realization_state_actual_ref",
        "actual_realization_state",
        ["actual_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "actual_realization_timing",
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("extent_code", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f("pk_actual_realization_timing"),
        ),
        sa.CheckConstraint(
            "extent_code IN ('instant','start_only','interval')",
            name=op.f("ck_actual_realization_timing_extent"),
        ),
        sa.CheckConstraint(
            "isfinite(started_at) AND ("
            "(extent_code IN ('instant','start_only') AND ended_at IS NULL) OR "
            "(extent_code='interval' AND ended_at IS NOT NULL "
            "AND isfinite(ended_at) AND ended_at > started_at))",
            name=op.f("ck_actual_realization_timing_interval_order"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_actual_realization_timing_actual_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "actual_realization_session_basis",
        sa.Column(
            "actual_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("session_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "session_timing_material_state_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "actual_material_state_ref",
            "session_ref",
            name=op.f("pk_actual_realization_session_basis"),
        ),
        _fk(
            ["actual_material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_actual_realization_session_basis_actual_state",
        ),
        _fk(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_actual_realization_session_basis_session_ref_session",
        ),
        _fk(
            ["session_timing_material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_actual_realization_session_basis_timing_state",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_actual_realization_session_basis_session_ref",
        "actual_realization_session_basis",
        ["session_ref"],
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_actual_realization_session_basis_timing_state",
        "actual_realization_session_basis",
        ["session_timing_material_state_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "actual_realization_current_history",
        sa.Column("actual_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "actual_ref",
            "current_from_at",
            name=op.f("pk_actual_realization_current_history"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name=op.f("ck_actual_realization_current_history_current_interval"),
        ),
        _fk(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_actual_realization_current_history_actual_ref_actual",
        ),
        _fk(
            ["material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_actual_realization_current_history_actual_state",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ux_actual_realization_current_history_open",
        "actual_realization_current_history",
        ["actual_ref"],
        unique=True,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        "ix_actual_realization_current_history_material_state_ref",
        "actual_realization_current_history",
        ["material_state_ref"],
        schema=_DANTE_SCHEMA,
    )

    _deny_runtime_access_to_new_relations()


def downgrade() -> None:
    """Return from CP6-M03 to the closed CP6-M02 schema."""
    for table_name in reversed(_M3_TABLES):
        op.drop_table(table_name, schema=_DANTE_SCHEMA)
