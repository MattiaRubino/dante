"""B06-C Occurrence checkpoint, extra, skip and exclusion mappings."""

from datetime import date, datetime, time

import sqlalchemy as sa
from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef


class OccurrenceCheckpointOperationRow(Base):
    __tablename__ = "occurrence_checkpoint_operation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_checkpoint_operation_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_checkpoint_operation_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("source_family IN ('routine','event')", name="source_family"),
        CheckConstraint(
            "isfinite(start_date) AND isfinite(end_date_exclusive) AND end_date_exclusive>start_date AND end_date_exclusive-start_date<=62",
            name="range",
        ),
        CheckConstraint(
            "effective_zone_id=btrim(effective_zone_id) AND effective_zone_id<>'' AND char_length(effective_zone_id)<=200",
            name="zone",
        ),
        Index(
            "ix_occurrence_checkpoint_operation_source_range",
            "source_native_ref",
            "start_date",
            "end_date_exclusive",
            "accepted_at",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    source_family: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date_exclusive: Mapped[date] = mapped_column(Date, nullable=False)
    effective_zone_id: Mapped[str] = mapped_column(Text, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OccurrenceCheckpointResultRow(Base):
    __tablename__ = "occurrence_checkpoint_result"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref", "operation_id"],
            [
                "dante.occurrence_checkpoint_operation.self_person_ref",
                "dante.occurrence_checkpoint_operation.operation_id",
            ],
            name="fk_occurrence_checkpoint_result_operation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_checkpoint_result_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_occurrence_checkpoint_result_occurrence", "occurrence_ref"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)


class OccurrenceExtraOperationRow(Base):
    __tablename__ = "occurrence_extra_operation"
    __table_args__ = (
        UniqueConstraint("occurrence_ref", name="uq_occurrence_extra_operation_occurrence"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_extra_operation_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_extra_operation_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_extra_operation_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint("source_family IN ('routine','event')", name="source_family"),
        Index("ix_occurrence_extra_operation_source_accepted", "source_native_ref", "accepted_at"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    source_family: Mapped[str] = mapped_column(Text, nullable=False)
    occurrence_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OccurrenceSkipRow(Base):
    __tablename__ = "occurrence_skip"
    __table_args__ = (
        UniqueConstraint("self_person_ref", "operation_id", name="uq_occurrence_skip_operation"),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_skip_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_skip_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "reason IS NULL OR (reason=btrim(reason) AND reason<>'' AND char_length(reason)<=500)",
            name="reason",
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    operation_id: Mapped[str] = mapped_column(Text, nullable=False)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    skipped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OccurrenceExclusionRow(Base):
    __tablename__ = "occurrence_exclusion"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_exclusion_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_exclusion_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_occurrence_exclusion_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "uuid_extract_version(exclusion_ref) IS NOT DISTINCT FROM 7", name="uuidv7"
        ),
        CheckConstraint(
            "family_code IN ('calendar_wall_clock','elapsed_interval','cyclic_positional')",
            name="family",
        ),
        CheckConstraint(
            "(family_code='calendar_wall_clock' AND generated_date IS NOT NULL AND expected_at IS NULL AND position_index IS NULL) OR (family_code='elapsed_interval' AND generated_date IS NULL AND generated_wall_time IS NULL AND expected_at IS NOT NULL AND position_index IS NULL) OR (family_code='cyclic_positional' AND generated_date IS NOT NULL AND generated_wall_time IS NULL AND expected_at IS NULL AND position_index IS NOT NULL)",
            name="coordinate",
        ),
        CheckConstraint("generated_date IS NULL OR isfinite(generated_date)", name="date"),
        CheckConstraint("expected_at IS NULL OR isfinite(expected_at)", name="instant"),
        CheckConstraint("position_index IS NULL OR position_index>=0", name="position"),
        Index(
            "ix_occurrence_exclusion_source_state",
            "source_native_ref",
            "governing_recurrence_state_ref",
            "family_code",
        ),
        Index(
            "uq_occurrence_exclusion_calendar",
            "source_native_ref",
            "governing_recurrence_state_ref",
            "generated_date",
            "generated_wall_time",
            unique=True,
            postgresql_nulls_not_distinct=True,
            postgresql_where=sa.text("family_code='calendar_wall_clock'"),
        ),
        Index(
            "uq_occurrence_exclusion_elapsed",
            "source_native_ref",
            "governing_recurrence_state_ref",
            "expected_at",
            unique=True,
            postgresql_where=sa.text("family_code='elapsed_interval'"),
        ),
        Index(
            "uq_occurrence_exclusion_cyclic",
            "source_native_ref",
            "governing_recurrence_state_ref",
            "generated_date",
            "position_index",
            unique=True,
            postgresql_where=sa.text("family_code='cyclic_positional'"),
        ),
    )

    exclusion_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    self_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    governing_recurrence_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    family_code: Mapped[str] = mapped_column(Text, nullable=False)
    generated_date: Mapped[date | None] = mapped_column(Date)
    generated_wall_time: Mapped[time | None] = mapped_column(Time(timezone=False))
    expected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    position_index: Mapped[int | None] = mapped_column(Integer)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OccurrenceExclusionOperationRow(Base):
    __tablename__ = "occurrence_exclusion_operation"
    __table_args__ = (
        UniqueConstraint("exclusion_ref", name="uq_occurrence_exclusion_operation_ref"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_occurrence_exclusion_operation_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["exclusion_ref"],
            ["dante.occurrence_exclusion.exclusion_ref"],
            name="fk_occurrence_exclusion_operation_exclusion",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    exclusion_ref: Mapped[NativeRef] = mapped_column(nullable=False)
