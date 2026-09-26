"""SQLAlchemy row mappings for the B10-C Confirmation attestation family."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base
from dante.platform.database.references import MaterialStateRef, NativeRef, ScopedRecordRef


class ConfirmationRow(Base):
    """Scoped Confirmation owner pinned to one exact Outcome disposition state."""

    __tablename__ = "confirmation"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(confirmation_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "purpose_code=btrim(purpose_code) AND purpose_code<>'' "
            "AND char_length(purpose_code)<=120 "
            "AND purpose_code ~ '^[a-z0-9][a-z0-9._:-]*$'",
            name="purpose",
        ),
        UniqueConstraint(
            "outcome_disposition_material_state_ref",
            "confirmer_person_ref",
            "purpose_code",
            name="uq_confirmation_target_actor_purpose",
        ),
        UniqueConstraint(
            "confirmation_ref",
            "outcome_ref",
            name="uq_confirmation_ref_outcome",
        ),
        ForeignKeyConstraint(
            ["outcome_ref"],
            ["dante.outcome.outcome_ref"],
            name="fk_confirmation_outcome_ref_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_ref", "outcome_disposition_material_state_ref"],
            [
                "dante.outcome_disposition_state.outcome_ref",
                "dante.outcome_disposition_state.material_state_ref",
            ],
            name="fk_confirmation_outcome_disposition",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["confirmer_person_ref"],
            ["dante.person.person_ref"],
            name="fk_confirmation_confirmer_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_confirmation_outcome_ref", "outcome_ref"),
    )

    confirmation_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_disposition_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        nullable=False
    )
    confirmer_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)


class ConfirmationAttestationStateRow(Base):
    """Immutable contextual attestation stance for one Confirmation owner."""

    __tablename__ = "confirmation_attestation_state"
    __table_args__ = (
        CheckConstraint(
            "stance_code=btrim(stance_code) AND stance_code<>'' "
            "AND char_length(stance_code)<=120 "
            "AND stance_code ~ '^[a-z0-9][a-z0-9._:-]*$'",
            name="stance",
        ),
        UniqueConstraint(
            "confirmation_ref",
            "material_state_ref",
            name="uq_confirmation_attestation_state_confirmation_material",
        ),
        ForeignKeyConstraint(
            ["material_state_ref"],
            ["dante.material_state_address.material_state_ref"],
            name="fk_confirmation_attestation_state_state_address",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["confirmation_ref"],
            ["dante.confirmation.confirmation_ref"],
            name="fk_confirmation_attestation_state_confirmation",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_confirmation_attestation_state_confirmation_ref", "confirmation_ref"),
    )

    material_state_ref: Mapped[MaterialStateRef] = mapped_column(primary_key=True)
    confirmation_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    stance_code: Mapped[str] = mapped_column(Text, nullable=False)


class ConfirmationAttestationCurrentHistoryRow(Base):
    """Explicit accepted-current history for Confirmation attestation."""

    __tablename__ = "confirmation_attestation_current_history"
    __table_args__ = (
        CheckConstraint(
            "isfinite(current_from_at) AND (current_until_at IS NULL OR "
            "(isfinite(current_until_at) AND current_until_at>current_from_at))",
            name="interval",
        ),
        ForeignKeyConstraint(
            ["confirmation_ref", "material_state_ref"],
            [
                "dante.confirmation_attestation_state.confirmation_ref",
                "dante.confirmation_attestation_state.material_state_ref",
            ],
            name="fk_confirmation_attestation_current_history_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index(
            "ux_confirmation_attestation_current_history_open",
            "confirmation_ref",
            unique=True,
            postgresql_where=text("current_until_at IS NULL"),
        ),
        Index(
            "ix_confirmation_attestation_current_history_material_state_ref",
            "material_state_ref",
        ),
    )

    confirmation_ref: Mapped[ScopedRecordRef] = mapped_column(primary_key=True)
    material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    current_from_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    current_until_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ConfirmationAttestationOperationRow(Base):
    """Immutable idempotency receipt; operation id is never Confirmation identity."""

    __tablename__ = "confirmation_attestation_operation"
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
            name="fk_confirmation_attestation_operation_self_person",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["confirmation_ref", "outcome_ref"],
            ["dante.confirmation.confirmation_ref", "dante.confirmation.outcome_ref"],
            name="fk_confirmation_attestation_operation_confirmation_outcome",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["outcome_disposition_material_state_ref"],
            ["dante.outcome_disposition_state.material_state_ref"],
            name="fk_confirmation_attestation_operation_outcome_disposition",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["confirmation_ref", "expected_material_state_ref"],
            [
                "dante.confirmation_attestation_state.confirmation_ref",
                "dante.confirmation_attestation_state.material_state_ref",
            ],
            name="fk_confirmation_attestation_operation_expected_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["confirmation_ref", "resulting_material_state_ref"],
            [
                "dante.confirmation_attestation_state.confirmation_ref",
                "dante.confirmation_attestation_state.material_state_ref",
            ],
            name="fk_confirmation_attestation_operation_resulting_state",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "resulting_material_state_ref",
            name="uq_confirmation_attestation_operation_resulting_state",
        ),
    )

    self_person_ref: Mapped[NativeRef] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column(Text, primary_key=True)
    intent_fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    confirmation_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_ref: Mapped[ScopedRecordRef] = mapped_column(nullable=False)
    outcome_disposition_material_state_ref: Mapped[MaterialStateRef] = mapped_column(
        nullable=False
    )
    confirmer_person_ref: Mapped[NativeRef] = mapped_column(nullable=False)
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)
    expected_material_state_ref: Mapped[MaterialStateRef | None] = mapped_column(nullable=True)
    resulting_material_state_ref: Mapped[MaterialStateRef] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
