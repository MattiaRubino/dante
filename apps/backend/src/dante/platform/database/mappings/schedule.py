"""SQLAlchemy row mappings for the materialized Schedule family."""

from datetime import date, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, text
from sqlalchemy.dialects.postgresql import DATERANGE, Range
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ScheduleRow(Base):
    """Persistence row for dante.schedule; not a Domain model class."""

    __tablename__ = "schedule"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(schedule_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        ForeignKeyConstraint(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_schedule_subject_native_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_schedule_subject_native_ref", "subject_native_ref"),
    )

    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class SchedulePlacementStateRow(Base):
    """Schedule placement MaterialState envelope."""

    __tablename__ = "schedule_placement_state"
    __table_args__ = (
        CheckConstraint(
            "temporal_form_code IN "
            "('date_span','floating_local','named_zone_local','absolute')",
            name="temporal_form",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_schedule_placement_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["schedule_ref"],
            ["dante.schedule.schedule_ref"],
            name="fk_schedule_placement_state_schedule_ref_schedule",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_schedule_placement_state_schedule_ref", "schedule_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    temporal_form_code: Mapped[str] = mapped_column(Text, nullable=False)


class SchedulePlacementDateStateRow(Base):
    """Date-span placement payload."""

    __tablename__ = "schedule_placement_date_state"
    __table_args__ = (
        CheckConstraint(
            "NOT isempty(date_span) "
            "AND NOT lower_inf(date_span) "
            "AND NOT upper_inf(date_span) "
            "AND lower_inc(date_span) "
            "AND NOT upper_inc(date_span) "
            "AND isfinite(lower(date_span)) "
            "AND isfinite(upper(date_span))",
            name="date_span",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_date_state_placement_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    date_span: Mapped[Range[date]] = mapped_column(DATERANGE, nullable=False)


class SchedulePlacementFloatingLocalStateRow(Base):
    """Floating-local placement payload."""

    __tablename__ = "schedule_placement_floating_local_state"
    __table_args__ = (
        CheckConstraint(
            "extent_code IN ('point','start_only','interval')",
            name="extent",
        ),
        CheckConstraint(
            "isfinite(starts_local_at) AND ("
            "(extent_code IN ('point','start_only') AND ends_local_at IS NULL) OR "
            "(extent_code='interval' AND ends_local_at IS NOT NULL "
            "AND isfinite(ends_local_at) AND ends_local_at > starts_local_at))",
            name="interval_order",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_floating_local_state_placement_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    extent_code: Mapped[str] = mapped_column(Text, nullable=False)
    starts_local_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    ends_local_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))


class SchedulePlacementNamedZoneStateRow(Base):
    """Named-zone local placement payload."""

    __tablename__ = "schedule_placement_named_zone_state"
    __table_args__ = (
        CheckConstraint(
            "extent_code IN ('point','start_only','interval')",
            name="extent",
        ),
        CheckConstraint(
            "isfinite(starts_local_at) AND ("
            "(extent_code IN ('point','start_only') AND ends_local_at IS NULL) OR "
            "(extent_code='interval' AND ends_local_at IS NOT NULL "
            "AND isfinite(ends_local_at) AND ends_local_at > starts_local_at))",
            name="interval_order",
        ),
        CheckConstraint(
            "(resolved_start_at IS NULL OR isfinite(resolved_start_at)) AND ("
            "resolved_end_at IS NULL OR "
            "(resolved_start_at IS NOT NULL AND extent_code='interval' "
            "AND isfinite(resolved_end_at) "
            "AND resolved_end_at > resolved_start_at))",
            name="resolved_pair",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_named_zone_state_placement_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    extent_code: Mapped[str] = mapped_column(Text, nullable=False)
    starts_local_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    ends_local_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))
    zone_id: Mapped[str] = mapped_column(Text, nullable=False)
    resolved_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SchedulePlacementAbsoluteStateRow(Base):
    """Absolute placement payload."""

    __tablename__ = "schedule_placement_absolute_state"
    __table_args__ = (
        CheckConstraint(
            "extent_code IN ('point','start_only','interval')",
            name="extent",
        ),
        CheckConstraint(
            "isfinite(starts_at) AND ("
            "(extent_code IN ('point','start_only') AND ends_at IS NULL) OR "
            "(extent_code='interval' AND ends_at IS NOT NULL "
            "AND isfinite(ends_at) AND ends_at > starts_at))",
            name="interval_order",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_absolute_state_placement_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    extent_code: Mapped[str] = mapped_column(Text, nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SchedulePlacementCurrentHistoryRow(Base):
    """Schedule placement currentness history."""

    __tablename__ = "schedule_placement_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name="current_interval",
        ),
        ForeignKeyConstraint(
            ["schedule_ref"],
            ["dante.schedule.schedule_ref"],
            name="fk_schedule_placement_current_history_schedule_ref_schedule",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.schedule_placement_state.material_state_ref"],
            name="fk_schedule_placement_current_history_placement_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_schedule_placement_current_history_open",
            "schedule_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_schedule_placement_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    schedule_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
