"""Materialize CP6-M04 owner-bound Routine/Event Recurrence families.

Revision ID: 20260825_04
Revises: 20260825_03
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260825_04"
down_revision: str | None = "20260825_03"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_M4_TABLES = (
    "routine_recurrence_state",
    "routine_recurrence_boundary_state",
    "routine_recurrence_calendar_state",
    "routine_recurrence_calendar_wall_time",
    "routine_recurrence_calendar_weekday",
    "routine_recurrence_calendar_month_day",
    "routine_recurrence_calendar_ordinal_weekday",
    "routine_recurrence_calendar_year_month_day",
    "routine_recurrence_elapsed_state",
    "routine_recurrence_quota_state",
    "routine_recurrence_cyclic_state",
    "routine_recurrence_cycle_position",
    "routine_recurrence_current_history",
    "event_recurrence_state",
    "event_recurrence_boundary_state",
    "event_recurrence_calendar_state",
    "event_recurrence_calendar_wall_time",
    "event_recurrence_calendar_weekday",
    "event_recurrence_calendar_month_day",
    "event_recurrence_calendar_ordinal_weekday",
    "event_recurrence_calendar_year_month_day",
    "event_recurrence_elapsed_state",
    "event_recurrence_quota_state",
    "event_recurrence_cyclic_state",
    "event_recurrence_cycle_position",
    "event_recurrence_current_history",
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


def _create_recurrence_family(
    prefix: str,
    owner_ref: str,
    owner_table: str,
) -> None:
    state = f"{prefix}_recurrence_state"
    boundary = f"{prefix}_recurrence_boundary_state"
    calendar = f"{prefix}_recurrence_calendar_state"
    wall_time = f"{prefix}_recurrence_calendar_wall_time"
    weekday = f"{prefix}_recurrence_calendar_weekday"
    month_day = f"{prefix}_recurrence_calendar_month_day"
    ordinal_weekday = f"{prefix}_recurrence_calendar_ordinal_weekday"
    year_month_day = f"{prefix}_recurrence_calendar_year_month_day"
    elapsed = f"{prefix}_recurrence_elapsed_state"
    quota = f"{prefix}_recurrence_quota_state"
    cyclic = f"{prefix}_recurrence_cyclic_state"
    cycle_position = f"{prefix}_recurrence_cycle_position"
    history = f"{prefix}_recurrence_current_history"

    op.create_table(
        state,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(owner_ref, postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("family_code", sa.Text(), nullable=False),
        sa.Column("range_kind", sa.Text(), nullable=False),
        sa.Column("expected_occurrence_count", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f(f"pk_{state}"),
        ),
        sa.CheckConstraint(
            "family_code IN "
            "('calendar_wall_clock','elapsed_interval','quota_per_period','cyclic_positional')",
            name=op.f(f"ck_{state}_family_code"),
        ),
        sa.CheckConstraint(
            "range_kind IN ('open','until_boundary','expected_count')",
            name=op.f(f"ck_{state}_range_kind"),
        ),
        sa.CheckConstraint(
            "((range_kind='expected_count' "
            "AND expected_occurrence_count IS NOT NULL "
            "AND expected_occurrence_count > 0) OR "
            "(range_kind IN ('open','until_boundary') "
            "AND expected_occurrence_count IS NULL))",
            name=op.f(f"ck_{state}_expected_count"),
        ),
        _fk(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name=f"fk_{state}_state_address",
        ),
        _fk(
            [owner_ref],
            [f"dante.{owner_table}.{owner_ref}"],
            name=f"fk_{state}_{owner_ref}_{owner_table}",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        f"ix_{state}_{owner_ref}",
        state,
        [owner_ref],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        boundary,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("boundary_role", sa.Text(), nullable=False),
        sa.Column("boundary_kind", sa.Text(), nullable=False),
        sa.Column("inclusive", sa.Boolean(), nullable=True),
        sa.Column("date_value", sa.Date(), nullable=True),
        sa.Column("local_value", sa.DateTime(timezone=False), nullable=True),
        sa.Column("zone_id", sa.Text(), nullable=True),
        sa.Column("instant_value", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "boundary_role",
            name=op.f(f"pk_{boundary}"),
        ),
        sa.CheckConstraint(
            "boundary_role IN ('pattern_anchor','effective_from','effective_until')",
            name=op.f(f"ck_{boundary}_boundary_role"),
        ),
        sa.CheckConstraint(
            "boundary_kind IN "
            "('date','floating_local','named_zone_local','absolute_instant')",
            name=op.f(f"ck_{boundary}_boundary_kind"),
        ),
        sa.CheckConstraint(
            "((boundary_kind='date' "
            "AND date_value IS NOT NULL AND isfinite(date_value) "
            "AND local_value IS NULL AND zone_id IS NULL "
            "AND instant_value IS NULL AND resolved_at IS NULL) OR "
            "(boundary_kind='floating_local' "
            "AND local_value IS NOT NULL AND isfinite(local_value) "
            "AND date_value IS NULL AND zone_id IS NULL "
            "AND instant_value IS NULL AND resolved_at IS NULL) OR "
            "(boundary_kind='named_zone_local' "
            "AND local_value IS NOT NULL AND isfinite(local_value) "
            "AND zone_id IS NOT NULL AND date_value IS NULL "
            "AND instant_value IS NULL "
            "AND (resolved_at IS NULL OR isfinite(resolved_at))) OR "
            "(boundary_kind='absolute_instant' "
            "AND instant_value IS NOT NULL AND isfinite(instant_value) "
            "AND date_value IS NULL AND local_value IS NULL "
            "AND zone_id IS NULL AND resolved_at IS NULL))",
            name=op.f(f"ck_{boundary}_boundary_payload"),
        ),
        sa.CheckConstraint(
            "((boundary_role='pattern_anchor' AND inclusive IS NULL) OR "
            "(boundary_role IN ('effective_from','effective_until') "
            "AND inclusive IS NOT NULL))",
            name=op.f(f"ck_{boundary}_inclusive_role"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{state}.material_state_ref"],
            name=f"fk_{boundary}_recurrence_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        calendar,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pattern_code", sa.Text(), nullable=False),
        sa.Column("interval_count", sa.Integer(), nullable=False),
        sa.Column("clock_basis_code", sa.Text(), nullable=False),
        sa.Column("zone_id", sa.Text(), nullable=True),
        sa.Column("step_unit_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f(f"pk_{calendar}"),
        ),
        sa.CheckConstraint(
            "pattern_code IN "
            "('daily','weekly_weekdays','monthly_month_days',"
            "'monthly_ordinal_weekdays','yearly_month_days','anchor_step')",
            name=op.f(f"ck_{calendar}_pattern_code"),
        ),
        sa.CheckConstraint(
            "interval_count > 0",
            name=op.f(f"ck_{calendar}_interval_positive"),
        ),
        sa.CheckConstraint(
            "clock_basis_code IN ('floating_local','named_zone','absolute_utc')",
            name=op.f(f"ck_{calendar}_clock_basis"),
        ),
        sa.CheckConstraint(
            "((clock_basis_code='named_zone' AND zone_id IS NOT NULL) OR "
            "(clock_basis_code IN ('floating_local','absolute_utc') "
            "AND zone_id IS NULL))",
            name=op.f(f"ck_{calendar}_zone_basis"),
        ),
        sa.CheckConstraint(
            "((pattern_code='anchor_step' "
            "AND step_unit_code IN ('day','week','month','year')) OR "
            "(pattern_code<>'anchor_step' AND step_unit_code IS NULL))",
            name=op.f(f"ck_{calendar}_step_unit"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{state}.material_state_ref"],
            name=f"fk_{calendar}_recurrence_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        wall_time,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("wall_time", sa.Time(timezone=False), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "wall_time",
            name=op.f(f"pk_{wall_time}"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{calendar}.material_state_ref"],
            name=f"fk_{wall_time}_calendar_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        weekday,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("weekday_number", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "weekday_number",
            name=op.f(f"pk_{weekday}"),
        ),
        sa.CheckConstraint(
            "weekday_number BETWEEN 1 AND 7",
            name=op.f(f"ck_{weekday}_weekday_range"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{calendar}.material_state_ref"],
            name=f"fk_{weekday}_calendar_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        month_day,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("month_day", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "month_day",
            name=op.f(f"pk_{month_day}"),
        ),
        sa.CheckConstraint(
            "(month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1)",
            name=op.f(f"ck_{month_day}_month_day_range"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{calendar}.material_state_ref"],
            name=f"fk_{month_day}_calendar_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        ordinal_weekday,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("weekday_number", sa.SmallInteger(), nullable=False),
        sa.Column("ordinal", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "weekday_number",
            "ordinal",
            name=op.f(f"pk_{ordinal_weekday}"),
        ),
        sa.CheckConstraint(
            "weekday_number BETWEEN 1 AND 7",
            name=op.f(f"ck_{ordinal_weekday}_weekday_range"),
        ),
        sa.CheckConstraint(
            "ordinal BETWEEN -5 AND 5 AND ordinal <> 0",
            name=op.f(f"ck_{ordinal_weekday}_ordinal_range"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{calendar}.material_state_ref"],
            name=f"fk_{ordinal_weekday}_calendar_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        year_month_day,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("month_number", sa.SmallInteger(), nullable=False),
        sa.Column("month_day", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "month_number",
            "month_day",
            name=op.f(f"pk_{year_month_day}"),
        ),
        sa.CheckConstraint(
            "month_number BETWEEN 1 AND 12",
            name=op.f(f"ck_{year_month_day}_month_range"),
        ),
        sa.CheckConstraint(
            "(month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1)",
            name=op.f(f"ck_{year_month_day}_month_day_range"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{calendar}.material_state_ref"],
            name=f"fk_{year_month_day}_calendar_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        elapsed,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("elapsed_seconds", sa.Numeric(), nullable=False),
        sa.Column("anchor_mode_code", sa.Text(), nullable=False),
        sa.Column("anchor_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f(f"pk_{elapsed}"),
        ),
        sa.CheckConstraint(
            "elapsed_seconds NOT IN "
            "('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric) "
            "AND elapsed_seconds > 0",
            name=op.f(f"ck_{elapsed}_elapsed_positive"),
        ),
        sa.CheckConstraint(
            "anchor_mode_code IN ('fixed_anchor','previous_expected')",
            name=op.f(f"ck_{elapsed}_anchor_mode"),
        ),
        sa.CheckConstraint(
            "isfinite(anchor_at)",
            name=op.f(f"ck_{elapsed}_anchor_at"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{state}.material_state_ref"],
            name=f"fk_{elapsed}_recurrence_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        quota,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quota_count", sa.Integer(), nullable=False),
        sa.Column("period_unit_code", sa.Text(), nullable=False),
        sa.Column("period_span", sa.Integer(), nullable=False),
        sa.Column("frame_code", sa.Text(), nullable=False),
        sa.Column("zone_id", sa.Text(), nullable=True),
        sa.Column("week_start", sa.SmallInteger(), nullable=True),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f(f"pk_{quota}"),
        ),
        sa.CheckConstraint(
            "quota_count > 0",
            name=op.f(f"ck_{quota}_quota_positive"),
        ),
        sa.CheckConstraint(
            "period_span > 0",
            name=op.f(f"ck_{quota}_period_span_positive"),
        ),
        sa.CheckConstraint(
            "period_unit_code IN ('day','week','month','year')",
            name=op.f(f"ck_{quota}_period_unit"),
        ),
        sa.CheckConstraint(
            "frame_code IN ('floating_local','named_zone','absolute_utc')",
            name=op.f(f"ck_{quota}_frame"),
        ),
        sa.CheckConstraint(
            "((frame_code='named_zone' AND zone_id IS NOT NULL) OR "
            "(frame_code IN ('floating_local','absolute_utc') "
            "AND zone_id IS NULL))",
            name=op.f(f"ck_{quota}_zone_basis"),
        ),
        sa.CheckConstraint(
            "((period_unit_code='week' AND week_start BETWEEN 1 AND 7) OR "
            "(period_unit_code<>'week' AND week_start IS NULL))",
            name=op.f(f"ck_{quota}_week_start"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{state}.material_state_ref"],
            name=f"fk_{quota}_recurrence_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        cyclic,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cycle_length", sa.Integer(), nullable=False),
        sa.Column("position_unit_code", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            name=op.f(f"pk_{cyclic}"),
        ),
        sa.CheckConstraint(
            "cycle_length > 0",
            name=op.f(f"ck_{cyclic}_cycle_length_positive"),
        ),
        sa.CheckConstraint(
            "position_unit_code IN ('day','week')",
            name=op.f(f"ck_{cyclic}_position_unit"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{state}.material_state_ref"],
            name=f"fk_{cyclic}_recurrence_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        cycle_position,
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("position_index", sa.Integer(), nullable=False),
        sa.Column("generates_expected", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint(
            "material_state_ref",
            "position_index",
            name=op.f(f"pk_{cycle_position}"),
        ),
        sa.CheckConstraint(
            "position_index >= 0",
            name=op.f(f"ck_{cycle_position}_position_nonnegative"),
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{cyclic}.material_state_ref"],
            name=f"fk_{cycle_position}_cyclic_state",
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        history,
        sa.Column(owner_ref, postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("material_state_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_from_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_until_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            owner_ref,
            "current_from_at",
            name=op.f(f"pk_{history}"),
        ),
        sa.CheckConstraint(
            "isfinite(current_from_at) AND "
            "(current_until_at IS NULL OR "
            "(isfinite(current_until_at) "
            "AND current_until_at > current_from_at))",
            name=op.f(f"ck_{history}_current_interval"),
        ),
        _fk(
            [owner_ref],
            [f"dante.{owner_table}.{owner_ref}"],
            name=f"fk_{history}_{owner_ref}_{owner_table}",
        ),
        _fk(
            ["material_state_ref"],
            [f"dante.{state}.material_state_ref"],
            name=f"fk_{history}_recurrence_state",
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        f"ux_{history}_open",
        history,
        [owner_ref],
        unique=True,
        schema=_DANTE_SCHEMA,
        postgresql_where=sa.text("current_until_at IS NULL"),
    )
    op.create_index(
        f"ix_{history}_material_state_ref",
        history,
        ["material_state_ref"],
        schema=_DANTE_SCHEMA,
    )


def _drop_recurrence_family(prefix: str) -> None:
    for suffix in (
        "current_history",
        "cycle_position",
        "cyclic_state",
        "quota_state",
        "elapsed_state",
        "calendar_year_month_day",
        "calendar_ordinal_weekday",
        "calendar_month_day",
        "calendar_weekday",
        "calendar_wall_time",
        "calendar_state",
        "boundary_state",
        "state",
    ):
        op.drop_table(f"{prefix}_recurrence_{suffix}", schema=_DANTE_SCHEMA)


def _deny_runtime_access_to_new_relations() -> None:
    for table_name in _M4_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_DANTE_SCHEMA}.{table_name} "
                f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
            )
        )


def upgrade() -> None:
    """Create exactly the CP6-M04 twenty-six-table Recurrence surface."""
    _create_recurrence_family("routine", "routine_ref", "routine")
    _create_recurrence_family("event", "event_ref", "event")
    _deny_runtime_access_to_new_relations()


def downgrade() -> None:
    """Remove only the CP6-M04 Recurrence surface."""
    _drop_recurrence_family("event")
    _drop_recurrence_family("routine")
