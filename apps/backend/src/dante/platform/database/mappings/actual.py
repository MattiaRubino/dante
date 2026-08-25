"""SQLAlchemy row mappings for the materialized Actual family."""

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ActualRow(Base):
    """Persistence row for dante.actual; not a Domain model class."""

    __tablename__ = "actual"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(actual_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        ForeignKeyConstraint(
            ["subject_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_actual_subject_native_ref_native_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_actual_subject_native_ref", "subject_native_ref"),
    )

    actual_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    subject_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class ActualRealizationStateRow(Base):
    """Actual realization MaterialState envelope."""

    __tablename__ = "actual_realization_state"
    __table_args__ = (
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_actual_realization_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_actual_realization_state_actual_ref_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_actual_realization_state_actual_ref", "actual_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    actual_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    realization_occurred: Mapped[bool] = mapped_column(Boolean, nullable=False)


class ActualRealizationTimingRow(Base):
    """Optional realized Actual timing payload."""

    __tablename__ = "actual_realization_timing"
    __table_args__ = (
        CheckConstraint(
            "extent_code IN ('instant','start_only','interval')",
            name="extent",
        ),
        CheckConstraint(
            "isfinite(started_at) AND ("
            "(extent_code IN ('instant','start_only') AND ended_at IS NULL) OR "
            "(extent_code='interval' AND ended_at IS NOT NULL "
            "AND isfinite(ended_at) AND ended_at > started_at))",
            name="interval_order",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_actual_realization_timing_actual_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    extent_code: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ActualRealizationSessionBasisRow(Base):
    """Historical Session/timing-state basis for an Actual state."""

    __tablename__ = "actual_realization_session_basis"
    __table_args__ = (
        ForeignKeyConstraint(
            ["actual_material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_actual_realization_session_basis_actual_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["session_ref"],
            ["dante.session.session_ref"],
            name="fk_actual_realization_session_basis_session_ref_session",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["session_timing_material_state_ref"],
            ["dante.session_timing_state.material_state_ref"],
            name="fk_actual_realization_session_basis_timing_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_actual_realization_session_basis_session_ref", "session_ref"),
        Index(
            "ix_actual_realization_session_basis_timing_state",
            "session_timing_material_state_ref",
        ),
    )

    actual_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        primary_key=True
    )
    session_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    session_timing_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        nullable=False
    )


class ActualRealizationCurrentHistoryRow(Base):
    """Actual realization currentness history."""

    __tablename__ = "actual_realization_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at > current_from_at))",
            name="current_interval",
        ),
        ForeignKeyConstraint(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_actual_realization_current_history_actual_ref_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_actual_realization_current_history_actual_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_actual_realization_current_history_open",
            "actual_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_actual_realization_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    actual_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
