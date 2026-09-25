"""SQLAlchemy row mappings for the materialized B10-B Outcome family."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class OutcomeRow(Base):
    """Scoped contextual Outcome owner for one (Actual, vocabulary) pair."""

    __tablename__ = "outcome"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(outcome_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "vocabulary_code=btrim(vocabulary_code) "
            "AND vocabulary_code ~ '^[a-z][a-z0-9._-]{0,99}$'",
            name="vocabulary_code",
        ),
        UniqueConstraint(
            "actual_ref",
            "vocabulary_code",
            name="uq_outcome_actual_ref_vocabulary_code",
        ),
        ForeignKeyConstraint(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_outcome_actual_ref_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_outcome_actual_ref", "actual_ref"),
    )

    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    actual_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    vocabulary_code: Mapped[str] = mapped_column(Text, nullable=False)


class OutcomeResultStateRow(Base):
    """Immutable contextual result state for one Outcome owner."""

    __tablename__ = "outcome_result_state"
    __table_args__ = (
        CheckConstraint(
            "result_code=btrim(result_code) "
            "AND result_code ~ '^[a-z][a-z0-9._-]{0,99}$'",
            name="result_code",
        ),
        CheckConstraint(
            "note IS NULL OR (note=btrim(note) AND note<>'' AND char_length(note)<=2000)",
            name="note",
        ),
        UniqueConstraint(
            "outcome_ref",
            "material_state_ref",
            name="uq_outcome_result_state_outcome_material",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_outcome_result_state_material_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref"],
            ["dante.outcome.outcome_ref"],
            name="fk_outcome_result_state_outcome_ref_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_outcome_result_state_outcome_ref", "outcome_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    result_code: Mapped[str] = mapped_column(Text, nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


class OutcomeResultCurrentHistoryRow(Base):
    """Explicit accepted-current history for contextual Outcome result state."""

    __tablename__ = "outcome_result_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        UniqueConstraint(
            "material_state_ref",
            name="uq_outcome_result_current_history_material_state_ref",
        ),
        ForeignKeyConstraint(
            ["outcome_ref"],
            ["dante.outcome.outcome_ref"],
            name="fk_outcome_result_current_history_outcome_ref_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.outcome_result_state.material_state_ref"],
            name="fk_outcome_result_current_history_material_state_ref_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "uq_outcome_result_current_history_open",
            "outcome_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
    )

    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OutcomeResultOperationRow(Base):
    """Immutable idempotency receipt; operation id is never Outcome identity."""

    __tablename__ = "outcome_result_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        CheckConstraint(
            "vocabulary_code=btrim(vocabulary_code) "
            "AND vocabulary_code ~ '^[a-z][a-z0-9._-]{0,99}$'",
            name="vocabulary_code",
        ),
        CheckConstraint("isfinite(created_at)", name="created_at"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_outcome_result_operation_self_person_ref_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_outcome_result_operation_actual_ref_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref"],
            ["dante.outcome.outcome_ref"],
            name="fk_outcome_result_operation_outcome_ref_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["expected_material_state_ref"],
            ["dante.outcome_result_state.material_state_ref"],
            name="fk_outcome_result_operation_expected_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["resulting_material_state_ref"],
            ["dante.outcome_result_state.material_state_ref"],
            name="fk_outcome_result_operation_resulting_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "resulting_material_state_ref",
            name="uq_outcome_result_operation_resulting_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    actual_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    vocabulary_code: Mapped[str] = mapped_column(Text, nullable=False)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
