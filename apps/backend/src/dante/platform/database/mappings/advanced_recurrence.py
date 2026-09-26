"""SQLAlchemy row mappings for B11-A advanced Recurrence persistence."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef


class RoutineRecurrenceElapsedAnchorSourceRow(Base):
    __tablename__ = "routine_recurrence_elapsed_anchor_source"
    __table_args__ = (
        CheckConstraint("anchor_source_family IN ('routine','event')", name="family"),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.routine_recurrence_elapsed_state.material_state_ref"],
            name="fk_routine_recurrence_elapsed_anchor_source_elapsed_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["anchor_source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_routine_recurrence_elapsed_anchor_source_native_address",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    anchor_source_family: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class EventRecurrenceElapsedAnchorSourceRow(Base):
    __tablename__ = "event_recurrence_elapsed_anchor_source"
    __table_args__ = (
        CheckConstraint("anchor_source_family IN ('routine','event')", name="family"),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.event_recurrence_elapsed_state.material_state_ref"],
            name="fk_event_recurrence_elapsed_anchor_source_elapsed_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["anchor_source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_event_recurrence_elapsed_anchor_source_native_address",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    anchor_source_family: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)


class OccurrenceGenerationActualAnchorRow(Base):
    __tablename__ = "occurrence_generation_actual_anchor"
    __table_args__ = (
        CheckConstraint(
            "relation_code IN ('previous_completion','anchor_stream')",
            name="relation",
        ),
        CheckConstraint(
            "isfinite(anchor_completed_at) AND isfinite(expected_at) AND expected_at>anchor_completed_at",
            name="time",
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence_generation.occurrence_ref"],
            name="fk_occurrence_generation_actual_anchor_generation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_occurrence_generation_actual_anchor_recurrence_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["anchor_source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_occurrence_generation_actual_anchor_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["anchor_occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_occurrence_generation_actual_anchor_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["anchor_actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_occurrence_generation_actual_anchor_actual",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["anchor_actual_material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_occurrence_generation_actual_anchor_actual_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        Index(
            "ix_occurrence_generation_actual_anchor_state_expected",
            "governing_recurrence_state_ref",
            "expected_at",
            "occurrence_ref",
        ),
    )

    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    governing_recurrence_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    relation_code: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    anchor_occurrence_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    anchor_actual_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    anchor_actual_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    anchor_completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AdvancedRecurrenceCheckpointOperationRow(Base):
    __tablename__ = "advanced_recurrence_checkpoint_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint(
            "intent_fingerprint ~ '^[0-9a-f]{64}$'",
            name="fingerprint",
        ),
        CheckConstraint(
            "source_family IN ('routine','event')",
            name="source_family",
        ),
        CheckConstraint(
            "isfinite(start_at) AND isfinite(end_at_exclusive) AND end_at_exclusive>start_at AND end_at_exclusive-start_at<=interval '62 days'",
            name="window",
        ),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_advanced_recurrence_checkpoint_person",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["source_native_ref"],
            ["dante.native_address.native_ref"],
            name="fk_advanced_recurrence_checkpoint_source",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["governing_recurrence_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_advanced_recurrence_checkpoint_state",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    source_native_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    source_family: Mapped[str] = mapped_column(Text, nullable=False)
    governing_recurrence_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at_exclusive: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AdvancedRecurrenceCheckpointResultRow(Base):
    __tablename__ = "advanced_recurrence_checkpoint_result"
    __table_args__ = (
        ForeignKeyConstraint(
            ["self_person_ref", "operation_id"],
            [
                "dante.advanced_recurrence_checkpoint_operation.self_person_ref",
                "dante.advanced_recurrence_checkpoint_operation.operation_id",
            ],
            name="fk_advanced_recurrence_checkpoint_result_operation",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
        ForeignKeyConstraint(
            ["occurrence_ref"],
            ["dante.occurrence.occurrence_ref"],
            name="fk_advanced_recurrence_checkpoint_result_occurrence",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    occurrence_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
