"""SQLAlchemy row mappings for the B10-B Outcome disposition family."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class OutcomeRow(Base):
    """Scoped Outcome owner for exactly one Actual."""

    __tablename__ = "outcome"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(outcome_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        UniqueConstraint("actual_ref", name="uq_outcome_actual_ref"),
        UniqueConstraint("outcome_ref", "actual_ref", name="uq_outcome_ref_actual_ref"),
        ForeignKeyConstraint(
            ["actual_ref"],
            ["dante.actual.actual_ref"],
            name="fk_outcome_actual_ref_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
    )

    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    actual_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)


class OutcomeDispositionStateRow(Base):
    """Immutable contextual disposition pinned to one exact Actual state."""

    __tablename__ = "outcome_disposition_state"
    __table_args__ = (
        CheckConstraint(
            "disposition_code=btrim(disposition_code) AND disposition_code<>'' "
            "AND char_length(disposition_code)<=120 "
            "AND disposition_code ~ '^[a-z0-9][a-z0-9._:-]*$'",
            name="code",
        ),
        UniqueConstraint(
            "outcome_ref",
            "material_state_ref",
            name="uq_outcome_disposition_state_outcome_material",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_outcome_disposition_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref"],
            ["dante.outcome.outcome_ref"],
            name="fk_outcome_disposition_state_outcome_ref_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_outcome_disposition_state_actual_realization",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_outcome_disposition_state_outcome_ref", "outcome_ref"),
        Index(
            "ix_outcome_disposition_state_actual_realization",
            "actual_realization_material_state_ref",
        ),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    actual_realization_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    disposition_code: Mapped[str] = mapped_column(Text, nullable=False)


class OutcomeDispositionCurrentHistoryRow(Base):
    """Explicit accepted-current history for Outcome disposition."""

    __tablename__ = "outcome_disposition_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["outcome_ref", "material_state_ref"],
            [
                "dante.outcome_disposition_state.outcome_ref",
                "dante.outcome_disposition_state.material_state_ref",
            ],
            name="fk_outcome_disposition_current_history_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_outcome_disposition_current_history_open",
            "outcome_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_outcome_disposition_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OutcomeDispositionOperationRow(Base):
    """Immutable idempotency receipt; operation id is never Outcome identity."""

    __tablename__ = "outcome_disposition_operation"
    __table_args__ = (
        CheckConstraint(
            "operation_id=btrim(operation_id) AND operation_id<>'' "
            "AND char_length(operation_id)<=200",
            name="operation_id",
        ),
        CheckConstraint("intent_fingerprint ~ '^[0-9a-f]{64}$'", name="fingerprint"),
        ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_outcome_disposition_operation_self_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref", "actual_ref"],
            ["dante.outcome.outcome_ref", "dante.outcome.actual_ref"],
            name="fk_outcome_disposition_operation_outcome_actual",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["actual_realization_material_state_ref"],
            ["dante.actual_realization_state.material_state_ref"],
            name="fk_outcome_disposition_operation_actual_realization",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref", "expected_material_state_ref"],
            [
                "dante.outcome_disposition_state.outcome_ref",
                "dante.outcome_disposition_state.material_state_ref",
            ],
            name="fk_outcome_disposition_operation_expected_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref", "resulting_material_state_ref"],
            [
                "dante.outcome_disposition_state.outcome_ref",
                "dante.outcome_disposition_state.material_state_ref",
            ],
            name="fk_outcome_disposition_operation_resulting_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "resulting_material_state_ref",
            name="uq_outcome_disposition_operation_resulting_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    actual_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    actual_realization_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
